# Contaminación cruzada: por seguridad, lo que el plato puede contener cuenta como alérgeno.
PREFIX pf: <http://unitru.edu.pe/ai2/peruvian-food#>
INSERT { ?dish pf:contieneAlergeno ?allergen }
WHERE  { ?dish pf:puedeContener ?allergen }
