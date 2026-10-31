# Un plato contiene los alérgenos de sus ingredientes.
PREFIX pf: <http://unitru.edu.pe/ai2/peruvian-food#>
INSERT { ?dish pf:contieneAlergeno ?allergen }
WHERE  { ?dish a pf:Plato ; pf:tieneIngrediente ?ing . ?ing pf:contieneAlergeno ?allergen }
