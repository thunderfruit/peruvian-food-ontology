# Evaluación de usabilidad del prototipo (SUS)

Cuestionario System Usability Scale (Brooke, 1996), traducido al español. Se aplica después de que el participante usa el prototipo:
https://thunderfruit.github.io/peruvian-food-ontology/prototype/recommender.html

## Antes de empezar

- Participantes: 5 a 10 personas que no hayan desarrollado el proyecto (compañeros, familiares).
- Cada participante hace las tres tareas sin ayuda. Solo se anota si la completó y cuánto tardó.
- Luego responde las 10 afirmaciones. No se le explica nada del sistema durante la prueba.

## Tareas

1. Eres alérgico al maní y a los frutos secos y quieres mantener tu peso. Encuentra un plato que puedas pedir.
2. Eres vegetariano y no tomas leche. ¿Cuántos platos de la sierra puedes pedir?
3. Elige cualquier consulta, activa "Comparar con la versión base" y explica con tus palabras por qué la versión refinada descarta uno de los platos.

## Afirmaciones

Escala: 1 = totalmente en desacuerdo, 2 = en desacuerdo, 3 = ni de acuerdo ni en desacuerdo, 4 = de acuerdo, 5 = totalmente de acuerdo.

| N.º | Afirmación                                                                                      |
| --- | ----------------------------------------------------------------------------------------------- |
| 1   | Creo que me gustaría usar este sistema con frecuencia.                                          |
| 2   | Encontré el sistema innecesariamente complejo.                                                  |
| 3   | Pensé que el sistema era fácil de usar.                                                         |
| 4   | Creo que necesitaría el apoyo de una persona con conocimientos técnicos para usar este sistema. |
| 5   | Encontré que las funciones del sistema estaban bien integradas.                                 |
| 6   | Pensé que había demasiada inconsistencia en el sistema.                                         |
| 7   | Imagino que la mayoría de las personas aprendería a usar este sistema muy rápidamente.          |
| 8   | Encontré el sistema muy engorroso de usar.                                                      |
| 9   | Me sentí seguro usando el sistema.                                                              |
| 10  | Necesité aprender muchas cosas antes de poder usar este sistema.                                |

## Registro y cálculo

Con Google Forms: un formulario con las 10 afirmaciones en el mismo orden, cada una como "Escala lineal" de 1 a 5. En la pestaña Respuestas, "Descargar respuestas (.csv)" y luego:

```bash
python3 scripts/sus_score.py ~/Downloads/<archivo>.csv   # copia a results/sus_responses.csv y escribe results/sus_summary.md
```

Sin formulario: cada participante es una fila de `results/sus_responses.csv` (`participant,q1,...,q10`, valores de 1 a 5) y se corre `python3 scripts/sus_score.py`.

El puntaje va de 0 a 100: los ítems impares suman (respuesta - 1), los pares (5 - respuesta), y la suma se multiplica por 2,5. Un puntaje de 68 es el promedio de la escala.

Referencia: J. Brooke, "SUS: A 'quick and dirty' usability scale," en *Usability Evaluation in Industry*, P. W. Jordan, B. Thomas, B. A. Weerdmeester y I. L. McClelland, Eds. London, U.K.: Taylor & Francis, 1996, pp. 189-194.
