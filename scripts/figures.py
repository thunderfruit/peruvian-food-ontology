"""Generate the report figures (PDF) from the dataset and results/metrics_*.csv.

Usage: python scripts/figures.py   (run after evaluate.py)
Output: report/figures/*.pdf
"""
import collections
import csv
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from build import read_csv, split  # noqa: E402

OUT = ROOT / "report" / "figures"
REGION_COLOR = {"costa": "#2a78d6", "sierra": "#eb6834", "selva": "#1baf7a"}  # validated palette
VERSION_COLOR = {"base": "#eb6834", "refined": "#2a78d6"}
VERSION_LABEL = {"base": "Base", "refined": "Refinada"}
INK, MUTED, GRID = "#1f1f1e", "#6b6a64", "#e4e3df"

plt.rcParams.update({
    "font.family": "serif", "font.size": 8, "axes.edgecolor": MUTED, "axes.labelcolor": INK,
    "xtick.color": MUTED, "ytick.color": MUTED, "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.5, "axes.axisbelow": True,
})


def save(fig, name):
    fig.tight_layout()
    fig.savefig(OUT / f"{name}.pdf")
    plt.close(fig)


def bar_labels(ax, bars):
    for b in bars:
        if b.get_height():
            ax.annotate(f"{int(b.get_height())}", (b.get_x() + b.get_width() / 2, b.get_height()),
                        ha="center", va="bottom", fontsize=6.5, color=INK, xytext=(0, 1), textcoords="offset points")


def dataset_by_type(dishes):
    types = ["entrada", "fondo", "sopa", "postre", "bebida"]
    fig, ax = plt.subplots(figsize=(3.4, 2.1))
    width = 0.26
    for i, region in enumerate(REGION_COLOR):
        counts = [sum(d["region"] == region and d["dish_type"] == t for d in dishes) for t in types]
        bars = ax.bar([x + (i - 1) * (width + 0.02) for x in range(len(types))], counts, width,
                      color=REGION_COLOR[region], label=region.capitalize())
        bar_labels(ax, bars)
    ax.set_xticks(range(len(types)), [t.capitalize() for t in types])
    ax.set_ylabel("Platos")
    ax.set_ylim(0, max(b.get_height() for b in ax.patches) * 1.25)
    ax.legend(frameon=False, ncol=3, loc="upper right", fontsize=7)
    save(fig, "dataset_by_type")


def allergen_frequency(gold, allergens):
    counts = collections.Counter(a for g in gold for a in split(g["allergens"]))
    items = sorted(((counts[a["id"]], a["id"]) for a in allergens), reverse=True)
    fig, ax = plt.subplots(figsize=(3.4, 2.2))
    pretty = {"crustaceos": "crustáceos", "mani": "maní", "sesamo": "sésamo", "frutos_secos": "frutos secos"}
    bars = ax.barh([pretty.get(name, name) for _, name in items], [n for n, _ in items], color="#2a78d6", height=0.6)
    ax.invert_yaxis()
    ax.set_xlabel("Platos")
    ax.grid(axis="y", visible=False)
    for b in bars:
        ax.annotate(f"{int(b.get_width())}", (b.get_width(), b.get_y() + b.get_height() / 2),
                    va="center", fontsize=6.5, color=INK, xytext=(2, 0), textcoords="offset points")
    save(fig, "allergen_frequency")


def technique_frequency(dishes):
    counts = collections.Counter(d["technique"] for d in dishes)
    items = counts.most_common()
    fig, ax = plt.subplots(figsize=(3.4, 2.0))
    bars = ax.barh([t.replace("_", " ") for t, _ in items], [n for _, n in items], color="#2a78d6", height=0.6)
    ax.invert_yaxis()
    ax.set_xlabel("Platos")
    ax.grid(axis="y", visible=False)
    for b in bars:
        ax.annotate(f"{int(b.get_width())}", (b.get_width(), b.get_y() + b.get_height() / 2),
                    va="center", fontsize=6.5, color=INK, xytext=(2, 0), textcoords="offset points")
    save(fig, "technique_frequency")


def metric_by_query(results, metric, name, label):
    queries = [r["query"] for r in results["base"]]
    fig, ax = plt.subplots(figsize=(7.0, 2.1))
    width = 0.4
    for i, version in enumerate(("base", "refined")):
        values = [float(r[metric]) for r in results[version]]
        ax.bar([x + (i - 0.5) * (width + 0.03) for x in range(len(queries))], values, width,
               color=VERSION_COLOR[version], label=VERSION_LABEL[version])
    ax.set_xticks(range(len(queries)), queries, rotation=90)
    ax.set_ylim(0, 1.05)
    ax.set_ylabel(label)
    ax.legend(frameon=False, ncol=2, loc="lower right", bbox_to_anchor=(1, 1), fontsize=7)
    save(fig, name)


def confusion_matrices(results):
    fig, axes = plt.subplots(1, 2, figsize=(3.4, 1.8))
    for ax, version in zip(axes, ("base", "refined")):
        t = {m: sum(int(r[m]) for r in results[version]) for m in ("tp", "fp", "fn", "tn")}
        matrix = [[t["tp"], t["fn"]], [t["fp"], t["tn"]]]
        ax.imshow(matrix, cmap="Blues", vmin=0, vmax=2000)
        for i in range(2):
            for j in range(2):
                ax.text(j, i, f"{['TP', 'FN', 'FP', 'TN'][i * 2 + j]}\n{matrix[i][j]}", ha="center", va="center",
                        fontsize=7, color="white" if matrix[i][j] > 1000 else INK)
        ax.set_title(VERSION_LABEL[version], fontsize=8, color=INK)
        ax.set_xticks([0, 1], ["Recom.", "No recom."])
        ax.set_yticks([0, 1], ["Compatible", "No compat."] if version == "base" else ["", ""])
        ax.grid(False)
        for spine in ax.spines.values():
            spine.set_visible(False)
    save(fig, "confusion_matrices")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    dishes = read_csv("data/dishes.csv")
    gold = read_csv("data/gold_dishes.csv")
    dataset_by_type(dishes)
    allergen_frequency(gold, read_csv("data/allergens.csv"))
    technique_frequency(dishes)
    results = {v: read_csv(f"results/metrics_{v}.csv") for v in ("base", "refined")}
    metric_by_query(results, "precision", "precision_by_query", "Precision")
    metric_by_query(results, "f1", "f1_by_query", "F1")
    confusion_matrices(results)
    print("figuras en", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
