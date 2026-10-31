"""Check each ontology version with the HermiT reasoner (bundled with owlready2, needs Java).

Usage: python scripts/check_consistency.py
Writes results/consistency.txt.
"""
import tempfile
from pathlib import Path

import owlready2
from rdflib import Graph

ROOT = Path(__file__).resolve().parent.parent


def check(version):
    g = Graph()
    g.parse(ROOT / "ontology" / f"peruvian_food_{version}.ttl")
    with tempfile.NamedTemporaryFile(suffix=".owl", delete=False) as tmp:
        g.serialize(tmp.name, format="xml")  # owlready2 does not read Turtle
    world = owlready2.World()
    onto = world.get_ontology(f"file://{tmp.name}").load()
    try:
        with onto:
            owlready2.sync_reasoner_hermit(world, infer_property_values=False, debug=0)
    except owlready2.OwlReadyInconsistentOntologyError:
        return f"{version}: INCONSISTENTE"
    finally:
        Path(tmp.name).unlink()
    unsatisfiable = list(world.inconsistent_classes())
    return (f"{version}: consistente (HermiT); clases: {len(list(onto.classes()))}, "
            f"individuos: {len(list(onto.individuals()))}, clases insatisfacibles: {len(unsatisfiable)}")


if __name__ == "__main__":
    lines = [check(v) for v in ("base", "refined")]
    (ROOT / "results" / "consistency.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
