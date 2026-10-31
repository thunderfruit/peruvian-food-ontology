"""Run the test queries on each version and compare with the gold standard.

Usage:
  python scripts/evaluate.py                      # local files ontology/peruvian_food_<v>.ttl
  python scripts/evaluate.py --endpoint URL       # Fuseki, URL with {version}, e.g.
                                                  # https://host/{version}/query
Writes queries/sparql/Qxx.rq, results/metrics_<v>.csv and results/summary.md.
"""
import argparse
import csv
import json
import statistics
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from build import PF, read_csv, slug, split  # noqa: E402

VERSIONS = ["base", "refined"]
DIET = {"vegetariano": ("vegetarian", "PlatoVegetariano"), "vegano": ("vegan", "PlatoVegano")}
PROFILE = {"PlatoBajoEnCalorias": "low_calorie", "PlatoAltoEnProteinas": "high_protein",
           "PlatoAptoParaPerdidaDePeso": "weight_loss",
           "PlatoAptoParaMantenimientoDePeso": "weight_maintenance"}


def to_sparql(q):
    lines = [f"PREFIX pf: <{PF}>", "SELECT DISTINCT ?plato WHERE {", "  ?plato a pf:Plato ."]
    if q["region"]:
        lines.append(f"  ?plato pf:region pf:{q['region'].capitalize()} .")
    if q["city"]:
        lines.append(f'  ?plato pf:ciudad "{q["city"]}" .')
    if q["diet"]:
        lines.append(f"  ?plato a pf:{DIET[q['diet']][1]} .")
    if q["profile"]:
        lines.append(f"  ?plato a pf:{q['profile']} .")
    allergens = split(q["exclude_allergens"])
    if allergens:
        values = " ".join(f"pf:alergeno_{slug(a)}" for a in allergens)
        lines.append(f"  FILTER NOT EXISTS {{ ?plato pf:contieneAlergeno ?a . VALUES ?a {{ {values} }} }}")
    lines.append("}")
    return "\n".join(lines) + "\n"


def expected_dishes(q, dishes, gold):
    excluded = set(split(q["exclude_allergens"]))
    result = set()
    for d in dishes:
        g = gold[d["id"]]
        if q["region"] and d["region"] != q["region"]:
            continue
        if q["city"] and d["city"] != q["city"]:
            continue
        if q["diet"] and g[DIET[q["diet"]][0]] != "1":
            continue
        if q["profile"] and g[PROFILE[q["profile"]]] != "1":
            continue
        if excluded & set(split(g["allergens"])):
            continue
        result.add(d["id"])
    return result


def run_local(version):
    from rdflib import Graph
    g = Graph()
    g.parse(ROOT / "ontology" / f"peruvian_food_{version}.ttl")
    return lambda text: {str(row[0]) for row in g.query(text)}


def run_endpoint(url):
    def run(text):
        data = urllib.parse.urlencode({"query": text}).encode()
        req = urllib.request.Request(url, data=data,
                                     headers={"Accept": "application/sparql-results+json"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            rows = json.load(resp)["results"]["bindings"]
        return {r["plato"]["value"] for r in rows}
    return run


def scores(retrieved, expected, total):
    tp = len(retrieved & expected)
    fp = len(retrieved - expected)
    fn = len(expected - retrieved)
    tn = total - tp - fp - fn
    # 0/0 cases: no recommendations is only perfect when nothing was expected
    precision = tp / (tp + fp) if retrieved else (1.0 if not expected else 0.0)
    recall = tp / (tp + fn) if expected else 1.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return dict(tp=tp, fp=fp, fn=fn, tn=tn, precision=precision, recall=recall, f1=f1)


def compare(base, refined):
    try:
        from scipy import stats
    except ImportError:
        return ["(instala scipy para las pruebas estadísticas)"]
    lines = ["| Métrica | Shapiro-Wilk p (diferencias) | Prueba | Estadístico | p |", "|---|---|---|---|---|"]
    for metric in ("precision", "recall", "f1"):
        a = [r[metric] for r in base]
        b = [r[metric] for r in refined]
        diffs = [y - x for x, y in zip(a, b)]
        if len(set(diffs)) <= 1:
            lines.append(f"| {metric} | - | sin variación | - | - |")
            continue
        shapiro_p = stats.shapiro(diffs).pvalue if len(diffs) >= 3 else float("nan")
        if shapiro_p > 0.05:
            name, res = "t pareada", stats.ttest_rel(b, a)
        else:
            name, res = "Wilcoxon", stats.wilcoxon(b, a)
        lines.append(f"| {metric} | {shapiro_p:.4f} | {name} | {res.statistic:.4f} | {res.pvalue:.4f} |")
    return lines


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--endpoint", help="URL del endpoint SPARQL con {version}")
    args = parser.parse_args()

    dishes = read_csv("data/dishes.csv")
    gold = {r["dish_id"]: r for r in read_csv("data/gold_dishes.csv")}
    missing = [d["id"] for d in dishes if d["id"] not in gold]
    if missing:
        sys.exit(f"Faltan en gold_dishes.csv: {missing}")
    queries = read_csv("queries/queries.csv")

    sparql_dir = ROOT / "queries" / "sparql"
    sparql_dir.mkdir(exist_ok=True)
    for q in queries:
        (sparql_dir / f"{q['id']}.rq").write_text(to_sparql(q), encoding="utf-8")
        if not expected_dishes(q, dishes, gold):
            print(f"AVISO: {q['id']} no tiene platos esperados; revisa la consulta", file=sys.stderr)

    results = {}
    for version in VERSIONS:
        run = run_endpoint(args.endpoint.format(version=version)) if args.endpoint else run_local(version)
        rows = []
        for q in queries:
            retrieved = {iri.rsplit("#plato_", 1)[-1] for iri in run(to_sparql(q))}
            expected = expected_dishes(q, dishes, gold)
            criteria = len(split(q["exclude_allergens"])) + sum(bool(q[k]) for k in ("diet", "profile", "region", "city"))
            rows.append(dict(query=q["id"], criteria=criteria, **scores(retrieved, expected, len(dishes)),
                             false_positives="|".join(sorted(retrieved - expected)),
                             false_negatives="|".join(sorted(expected - retrieved))))
        results[version] = rows
        with open(ROOT / "results" / f"metrics_{version}.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)

    md = ["# Resultados de la evaluación", "",
          f"{len(queries)} consultas x {len(dishes)} platos = {len(queries) * len(dishes)} pares consulta-plato.", "",
          "| Versión | Precision | Recall | F1 | TP | FP | FN | TN |", "|---|---|---|---|---|---|---|---|"]
    for version, rows in results.items():
        mean = {m: statistics.mean(r[m] for r in rows) for m in ("precision", "recall", "f1")}
        total = {m: sum(r[m] for r in rows) for m in ("tp", "fp", "fn", "tn")}
        md.append(f"| {version} | {mean['precision']:.3f} | {mean['recall']:.3f} | {mean['f1']:.3f} | "
                  f"{total['tp']} | {total['fp']} | {total['fn']} | {total['tn']} |")
    md += ["", "## Matriz de confusión agregada (filas: real, columnas: recomendado)", ""]
    for version, rows in results.items():
        total = {m: sum(r[m] for r in rows) for m in ("tp", "fp", "fn", "tn")}
        md += [f"**{version}**", "", "| | Recomendado | No recomendado |", "|---|---|---|",
               f"| Compatible | {total['tp']} (TP) | {total['fn']} (FN) |",
               f"| No compatible | {total['fp']} (FP) | {total['tn']} (TN) |", ""]
    md += ["## Comparación base vs refinada (alfa = 0,05)", ""] + compare(results["base"], results["refined"])
    (ROOT / "results" / "summary.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
