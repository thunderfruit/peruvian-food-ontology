"""SUS (System Usability Scale) scores from results/sus_responses.csv.

CSV columns: participant,q1,...,q10 with answers 1 (totalmente en desacuerdo) to 5 (totalmente de acuerdo).
Writes results/sus_summary.md.

    python3 scripts/sus_score.py                      # uses results/sus_responses.csv
    python3 scripts/sus_score.py forms_export.csv     # Google Forms export: Timestamp + the 10 items, in order
"""
import csv
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def sus_score(answers):
    """Brooke (1996): odd items x-1, even items 5-x, sum x 2.5 -> 0..100."""
    if len(answers) != 10 or any(a not in (1, 2, 3, 4, 5) for a in answers):
        raise ValueError(f"se esperan 10 respuestas entre 1 y 5: {answers}")
    return 2.5 * sum(a - 1 if i % 2 == 0 else 5 - a for i, a in enumerate(answers))


assert sus_score([3] * 10) == 50 and sus_score([5, 1] * 5) == 100 and sus_score([1, 5] * 5) == 0


def import_forms(path):
    """Copy a Google Forms export (last 10 columns = SUS items 1..10) into results/sus_responses.csv."""
    with open(path, encoding="utf-8-sig") as f:
        data = list(csv.reader(f))[1:]
    rows = [{"participant": f"P{n:02d}", **{f"q{i + 1}": int(v) for i, v in enumerate(r[-10:])}}
            for n, r in enumerate(data, 1) if any(r)]
    with open(ROOT / "results" / "sus_responses.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["participant"] + [f"q{i}" for i in range(1, 11)], lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def main():
    if len(sys.argv) > 1:
        import_forms(sys.argv[1])
    with open(ROOT / "results" / "sus_responses.csv", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise SystemExit("results/sus_responses.csv no tiene respuestas todavía")
    scores = {r["participant"]: sus_score([int(r[f"q{i}"]) for i in range(1, 11)]) for r in rows}
    mean = statistics.mean(scores.values())
    sd = statistics.stdev(scores.values()) if len(scores) > 1 else 0.0
    lines = ["# Usabilidad del prototipo (SUS)", "", f"{len(scores)} participantes. Media {mean:.1f}, desviación estándar {sd:.1f} (referencia: 68 es el promedio de la escala).", "",
             "| Participante | Puntaje SUS |", "|---|---|"] + [f"| {p} | {s:.1f} |" for p, s in scores.items()]
    (ROOT / "results" / "sus_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
