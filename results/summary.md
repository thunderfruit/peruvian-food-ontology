# Resultados de la evaluación

30 consultas x 100 platos = 3000 pares consulta-plato.

| Versión | Precision | Recall | F1 | TP | FP | FN | TN |
|---|---|---|---|---|---|---|---|
| base | 0.667 | 0.909 | 0.735 | 1132 | 393 | 57 | 1418 |
| refined | 0.916 | 0.987 | 0.940 | 1180 | 46 | 9 | 1765 |

## Matriz de confusión agregada (filas: real, columnas: recomendado)

**base**

| | Recomendado | No recomendado |
|---|---|---|
| Compatible | 1132 (TP) | 57 (FN) |
| No compatible | 393 (FP) | 1418 (TN) |

**refined**

| | Recomendado | No recomendado |
|---|---|---|
| Compatible | 1180 (TP) | 9 (FN) |
| No compatible | 46 (FP) | 1765 (TN) |

## Comparación base vs refinada (alfa = 0,05)

| Métrica | Shapiro-Wilk p (diferencias) | Prueba | Estadístico | p |
|---|---|---|---|---|
| precision | 0.0031 | Wilcoxon | 0.0000 | 0.0000 |
| recall | 0.0000 | Wilcoxon | 1.0000 | 0.0173 |
| f1 | 0.0018 | Wilcoxon | 0.0000 | 0.0000 |
