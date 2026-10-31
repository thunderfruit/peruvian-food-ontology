# Resultados de la evaluación

30 consultas x 100 platos = 3000 pares consulta-plato.

| Versión | Precision | Recall | F1 | TP | FP | FN | TN |
|---|---|---|---|---|---|---|---|
| base | 0.676 | 0.909 | 0.738 | 1124 | 399 | 55 | 1422 |
| refined | 0.913 | 0.987 | 0.938 | 1170 | 49 | 9 | 1772 |

## Matriz de confusión agregada (filas: real, columnas: recomendado)

**base**

| | Recomendado | No recomendado |
|---|---|---|
| Compatible | 1124 (TP) | 55 (FN) |
| No compatible | 399 (FP) | 1422 (TN) |

**refined**

| | Recomendado | No recomendado |
|---|---|---|
| Compatible | 1170 (TP) | 9 (FN) |
| No compatible | 49 (FP) | 1772 (TN) |

## Comparación base vs refinada (alfa = 0,05)

| Métrica | Shapiro-Wilk p (diferencias) | Prueba | Estadístico | p |
|---|---|---|---|---|
| precision | 0.0021 | Wilcoxon | 0.0000 | 0.0000 |
| recall | 0.0000 | Wilcoxon | 1.0000 | 0.0173 |
| f1 | 0.0022 | Wilcoxon | 0.0000 | 0.0000 |
