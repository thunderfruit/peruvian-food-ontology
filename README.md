# Ontología gastronómica peruana (Trujillo, 2026)

Proyecto de investigación formativa del curso Inteligencia Artificial II (UNT, 2026-II).

Ontología OWL 2 de platos de la cocina peruana (costa, sierra y selva, con énfasis en Trujillo) que recomienda platos según alergias, restricciones alimentarias y perfiles nutricionales cualitativos de control de peso. Se evalúa con Precision, Recall y F1 sobre consultas SPARQL, comparando una versión base y una versión refinada del motor de inferencia.

## Estructura

| Carpeta | Contenido |
|---|---|
| `data/` | Conjunto de datos de platos e ingredientes |
| `ontology/` | Ontología (`.ttl` / `.owl`) en sus versiones base y refinada |
| `queries/` | Consultas SPARQL y conjunto esperado (gold standard) |
| `scripts/` | Programas en Python: poblado de la ontología y evaluación |
| `results/` | Resultados por consulta y versión, estadísticos y gráficos |
| `deploy/` | Despliegue de Apache Jena Fuseki en Google Cloud |
| `report/` | Informe en LaTeX (formato IEEE) |

## Autores

- Avila Sanchez Ulises Medardo
- Quispe Ishuiza Cristopher
- Reyes Casana Valentino
