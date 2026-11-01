# Contaminación cruzada: por seguridad, lo que el plato puede contener cuenta como alérgeno.
PREFIX pf: <https://thunderfruit.github.io/peruvian-food-ontology/ontology#>
INSERT { ?dish pf:contieneAlergeno ?allergen }
WHERE  { ?dish pf:puedeContener ?allergen }
