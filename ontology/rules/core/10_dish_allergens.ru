# Un plato contiene los alérgenos de sus ingredientes.
PREFIX pf: <https://thunderfruit.github.io/peruvian-food-ontology/ontology#>
INSERT { ?dish pf:contieneAlergeno ?allergen }
WHERE  { ?dish a pf:Plato ; pf:tieneIngrediente ?ing . ?ing pf:contieneAlergeno ?allergen }
