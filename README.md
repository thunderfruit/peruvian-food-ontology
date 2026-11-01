# Ontología gastronómica peruana (Trujillo, 2026)

Proyecto de investigación formativa del curso Inteligencia Artificial II (UNT, 2026-II).

Ontología OWL 2 de platos de la cocina peruana (costa, sierra y selva, con énfasis en Trujillo) que recomienda platos según alergias, restricciones alimentarias y perfiles nutricionales cualitativos de control de peso. Se evalúa con Precision, Recall y F1 sobre consultas SPARQL, comparando una versión base y una versión refinada del motor de inferencia.

**Prototipo:** https://thunderfruit.github.io/peruvian-food-ontology/prototype/recommender.html

**Ontología en WebProtégé:** https://webprotege.stanford.edu/#projects/99469a5d-e3c7-441f-973f-9bf499b1798e/edit/Classes (requiere iniciar sesión)

**Informe (PDF):** [`report/AI2_U2_Research_Activity.pdf`](report/AI2_U2_Research_Activity.pdf)

## Estructura

| Carpeta | Contenido |
|---|---|
| `data/` | Conjunto de datos de platos e ingredientes |
| `ontology/` | Ontología (`.ttl` / `.owl`) en sus versiones base y refinada |
| `queries/` | Consultas SPARQL y conjunto esperado (gold standard) |
| `scripts/` | Programas en Python: poblado de la ontología y evaluación |
| `results/` | Resultados por consulta y versión, estadísticos y gráficos |
| `deploy/` | Despliegue de Apache Jena Fuseki en Render |
| `prototype/` | Interfaz web del recomendador (`recommender.html`), consulta el servicio desplegado |
| `report/` | Informe en LaTeX (formato IEEE) |
| `docs/` | Plan del proyecto y cuestionario de usabilidad (SUS) |

## Uso

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/build.py base       # ontology/peruvian_food_base.ttl
.venv/bin/python scripts/build.py refined    # ontology/peruvian_food_refined.ttl
.venv/bin/python scripts/evaluate.py         # results/metrics_*.csv y results/summary.md
.venv/bin/python scripts/check_consistency.py  # HermiT (necesita Java): results/consistency.txt
.venv/bin/python scripts/figures.py          # report/figures/*.pdf
cd report && pdflatex -output-directory=build main.tex  # dos veces, por las referencias
```

Despliegue: `deploy/README.md`.

## Cómo funciona

- `data/*.csv` es la única fuente de datos. `build.py` la valida, la convierte en individuos OWL sobre `ontology/tbox.ttl` y aplica las reglas de inferencia (SPARQL Update), con lo que el resultado queda materializado.
- **Base** = `rules/core` (alérgenos de los ingredientes, dietas) + `rules/profiles_base` (perfiles solo por técnica y categorías directas).
- **Refinada** = `rules/refine` (sinónimos regionales, ingredientes derivados con la cadena `tieneIngrediente o tieneComponente`, contaminación cruzada) + `rules/core` + `rules/profiles_refined` (perfiles que además tienen en cuenta azúcar, grasa animal, maní y frutos secos, varios lácteos y la fuente proteica principal).
- Las consultas (`queries/queries.csv`) son las mismas para ambas versiones. El gold standard sale de `data/gold_dishes.csv`, que se anota a mano, plato por plato, sin mirar la ontología, y lo valida el nutricionista.
- Datos: 100 platos (50 costa, 30 sierra, 20 selva; 9 de Trujillo), 146 ingredientes con 59 sinónimos, 30 consultas (12, 12 y 6 criterios).
- **Fuentes:** cada plato de `dishes.csv` cita en `source` al menos una fuente institucional (INEI, PromPerú, Andina, Ministerio de Cultura, INS o TV Perú); la receta citada define sus ingredientes.
- **Pendiente del equipo:** `gold_dishes.csv` lo anotó el equipo a partir de esas recetas; falta validarlo con especialistas en nutrición. Si cambian los datos, se vuelven a correr todos los scripts y se actualizan las cifras del informe.
