# Resultados de la evaluación

30 consultas x 100 platos = 3000 pares consulta-plato.

| Versión | Precision | Recall | F1 | TP | FP | FN | TN |
|---|---|---|---|---|---|---|---|
| base | 0.710 | 0.911 | 0.768 | 1201 | 357 | 60 | 1382 |
| refined | 0.938 | 0.995 | 0.961 | 1257 | 38 | 4 | 1701 |

## Matriz de confusión agregada (filas: real, columnas: recomendado)

**base**

| | Recomendado | No recomendado |
|---|---|---|
| Compatible | 1201 (TP) | 60 (FN) |
| No compatible | 357 (FP) | 1382 (TN) |

**refined**

| | Recomendado | No recomendado |
|---|---|---|
| Compatible | 1257 (TP) | 4 (FN) |
| No compatible | 38 (FP) | 1701 (TN) |

## Comparación base vs refinada (alfa = 0,05)

| Métrica | Shapiro-Wilk p (diferencias) | Prueba | Estadístico | p |
|---|---|---|---|---|
| precision | 0.0040 | Wilcoxon | 0.0000 | 0.0000 |
| recall | 0.0000 | Wilcoxon | 0.0000 | 0.0180 |
| f1 | 0.0018 | Wilcoxon | 0.0000 | 0.0000 |
