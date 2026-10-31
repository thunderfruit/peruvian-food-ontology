"""Build the knowledge base: TBox + ABox from data/*.csv + inference rules.

Usage: python scripts/build.py base|refined
Output: ontology/peruvian_food_<version>.ttl (materialized, ready for Fuseki or Protege).
"""
import csv
import re
import sys
import unicodedata
from pathlib import Path

from rdflib import OWL, RDF, RDFS, XSD, Graph, Literal, Namespace

ROOT = Path(__file__).resolve().parent.parent
PF = Namespace("http://unitru.edu.pe/ai2/peruvian-food#")
GROUP_CLASS = {"andino": PF.InsumoAndino, "marino": PF.InsumoMarino,
               "amazonico": PF.InsumoAmazonico, "general": PF.InsumoGeneral}
REGION = {"costa": PF.Costa, "sierra": PF.Sierra, "selva": PF.Selva}
RULE_DIRS = {"base": ["core", "profiles_base"], "refined": ["refine", "core", "profiles_refined"]}


def slug(text):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "_", text).strip("_")


def split(cell):
    return [part.strip() for part in (cell or "").split("|") if part.strip()]


def read_csv(relative_path):
    with open(ROOT / relative_path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def iri(kind, key):
    return PF[f"{kind}_{slug(key)}"]


def build_abox(g):
    errors, warnings = [], []
    allergens = {r["id"] for r in read_csv("data/allergens.csv")}
    techniques = {r["id"] for r in read_csv("data/techniques.csv")}
    ingredient_rows = read_csv("data/ingredients.csv")
    canonical = {slug(r["id"]) for r in ingredient_rows}

    for r in read_csv("data/allergens.csv"):
        node = iri("alergeno", r["id"])
        g.add((node, RDF.type, PF.Alergeno))
        g.add((node, RDFS.label, Literal(r["label"], lang="es")))
    for r in read_csv("data/techniques.csv"):
        node = iri("tecnica", r["id"])
        g.add((node, RDF.type, PF.TecnicaDeCoccion))
        g.add((node, RDFS.label, Literal(r["label"], lang="es")))
        g.add((node, PF.esTecnicaSaludable, Literal(r["healthy"] == "1", datatype=XSD.boolean)))

    known = set(canonical)  # canonical ids plus synonyms
    for r in ingredient_rows:
        node = iri("ingrediente", r["id"])
        if r["group"] not in GROUP_CLASS:
            errors.append(f"ingrediente {r['id']}: grupo desconocido '{r['group']}'")
            continue
        g.add((node, RDF.type, GROUP_CLASS[r["group"]]))
        g.add((node, RDFS.label, Literal(r["label"], lang="es")))
        g.add((node, PF.tipoDeAlimento, Literal(r["food_type"])))
        for a in split(r["allergens"]):
            if a not in allergens:
                errors.append(f"ingrediente {r['id']}: alérgeno desconocido '{a}'")
            g.add((node, PF.contieneAlergeno, iri("alergeno", a)))
        for c in split(r["components"]):
            if slug(c) not in canonical:
                errors.append(f"ingrediente {r['id']}: componente desconocido '{c}'")
            g.add((node, PF.tieneComponente, iri("ingrediente", c)))
        for s in split(r["synonyms"]):
            if slug(s) in known:
                errors.append(f"sinónimo '{s}' repetido o igual a un id")
            known.add(slug(s))
            alias = iri("ingrediente", s)  # alias carries no data: only the refined rules resolve it
            g.add((alias, RDF.type, PF.Ingrediente))
            g.add((alias, RDFS.label, Literal(s, lang="es")))
            g.add((alias, PF.sinonimoDe, node))

    for r in read_csv("data/dishes.csv"):
        node = iri("plato", r["id"])
        g.add((node, RDF.type, PF.Plato))
        g.add((node, RDFS.label, Literal(r["label"], lang="es")))
        if r["region"] not in REGION:
            errors.append(f"plato {r['id']}: región desconocida '{r['region']}'")
        else:
            g.add((node, PF.region, REGION[r["region"]]))
        if r["technique"] not in techniques:
            errors.append(f"plato {r['id']}: técnica desconocida '{r['technique']}'")
        g.add((node, PF.tecnicaDeCoccion, iri("tecnica", r["technique"])))
        if not r["source"]:
            errors.append(f"plato {r['id']}: sin fuente")
        for field, prop in (("city", PF.ciudad), ("dish_type", PF.tipoDePlato), ("source", PF.fuente)):
            if r[field]:
                g.add((node, prop, Literal(r[field])))
        for name in split(r["ingredients"]):
            if slug(name) not in known:
                warnings.append(f"plato {r['id']}: ingrediente '{name}' no está en ingredients.csv")
                g.add((iri("ingrediente", name), RDF.type, PF.Ingrediente))
            g.add((node, PF.tieneIngrediente, iri("ingrediente", name)))
        for a in split(r["may_contain"]):
            if a not in allergens:
                errors.append(f"plato {r['id']}: alérgeno desconocido '{a}'")
            g.add((node, PF.puedeContener, iri("alergeno", a)))
    return errors, warnings


def apply_rules(g, version):
    for folder in RULE_DIRS[version]:
        for rule in sorted((ROOT / "ontology" / "rules" / folder).glob("*.ru")):
            g.update(rule.read_text(encoding="utf-8"))


def metrics(g):
    count = lambda q: int(next(iter(g.query(q)))[0])
    return {
        "triples": len(g),
        "classes": count("SELECT (COUNT(DISTINCT ?c) AS ?n) WHERE { ?c a <%s> }" % OWL.Class),
        "object_properties": count("SELECT (COUNT(?p) AS ?n) WHERE { ?p a <%s> }" % OWL.ObjectProperty),
        "datatype_properties": count("SELECT (COUNT(?p) AS ?n) WHERE { ?p a <%s> }" % OWL.DatatypeProperty),
        "individuals": count("SELECT (COUNT(DISTINCT ?i) AS ?n) WHERE { ?i a ?c . ?c a <%s> }" % OWL.Class),
        "dishes": count("SELECT (COUNT(?d) AS ?n) WHERE { ?d a <%s> }" % PF.Plato),
    }


def main():
    version = sys.argv[1] if len(sys.argv) > 1 else ""
    if version not in RULE_DIRS:
        sys.exit("uso: python scripts/build.py base|refined")
    g = Graph()
    g.bind("pf", PF)
    g.parse(ROOT / "ontology" / "tbox.ttl")
    errors, warnings = build_abox(g)
    classes = set(g.subjects(RDF.type, OWL.Class))
    for s, c in list(g.subject_objects(RDF.type)):
        if c in classes:
            g.add((s, RDF.type, OWL.NamedIndividual))  # OWL tools (Protege, HermiT) need the declaration
    for w in warnings:
        print("AVISO:", w, file=sys.stderr)
    if errors:
        sys.exit("ERRORES en los datos:\n" + "\n".join(errors))
    apply_rules(g, version)
    out = ROOT / "ontology" / f"peruvian_food_{version}.ttl"
    g.serialize(out, format="turtle")
    print(out.relative_to(ROOT), metrics(g))


if __name__ == "__main__":
    main()
