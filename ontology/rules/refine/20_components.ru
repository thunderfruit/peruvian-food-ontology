# Cadena de propiedades: tieneIngrediente o tieneComponente+ -> tieneIngrediente (ingredientes derivados).
PREFIX pf: <https://thunderfruit.github.io/peruvian-food-ontology/ontology#>
INSERT { ?dish pf:tieneIngrediente ?part }
WHERE  { ?dish pf:tieneIngrediente/pf:tieneComponente+ ?part }
