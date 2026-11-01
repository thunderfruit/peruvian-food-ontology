# Resultados de la evaluación

30 consultas x 100 platos = 3000 pares consulta-plato.

| Versión | Precision | Recall | F1 | TP | FP | FN | TN |
|---|---|---|---|---|---|---|---|
| base | 0.668 | 0.909 | 0.735 | 1128 | 400 | 56 | 1416 |
| refined | 0.918 | 0.987 | 0.942 | 1175 | 45 | 9 | 1771 |

## Matriz de confusión agregada (filas: real, columnas: recomendado)

**base**

| | Recomendado | No recomendado |
|---|---|---|
| Compatible | 1128 (TP) | 56 (FN) |
| No compatible | 400 (FP) | 1416 (TN) |

**refined**

| | Recomendado | No recomendado |
|---|---|---|
| Compatible | 1175 (TP) | 9 (FN) |
| No compatible | 45 (FP) | 1771 (TN) |

## Comparación base vs refinada (alfa = 0,05)

| Métrica | Shapiro-Wilk p (diferencias) | Prueba | Estadístico | p |
|---|---|---|---|---|
| precision | 0.0020 | Wilcoxon | 0.0000 | 0.0000 |
| recall | 0.0000 | Wilcoxon | 1.0000 | 0.0173 |
| f1 | 0.0014 | Wilcoxon | 0.0000 | 0.0000 |
