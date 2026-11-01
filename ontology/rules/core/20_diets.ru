# Supuesto de mundo cerrado sobre la lista de ingredientes (equivale a un axioma de cierre).
PREFIX pf: <https://thunderfruit.github.io/peruvian-food-ontology/ontology#>
INSERT { ?dish a pf:PlatoVegetariano }
WHERE  { ?dish a pf:Plato
         FILTER NOT EXISTS { ?dish pf:tieneIngrediente ?ing . ?ing pf:tipoDeAlimento ?t
                             VALUES ?t { "carne" "carne_grasa" "grasa_animal" "ave" "pescado" "marisco" } } } ;
INSERT { ?dish a pf:PlatoVegano }
WHERE  { ?dish a pf:PlatoVegetariano
         FILTER NOT EXISTS { ?dish pf:tieneIngrediente ?ing . ?ing pf:tipoDeAlimento ?t
                             VALUES ?t { "lacteo" "huevo" "miel" } } }
