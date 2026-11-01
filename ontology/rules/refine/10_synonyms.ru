# Un ingrediente escrito con su sinónimo regional hereda el ingrediente canónico.
PREFIX pf: <https://thunderfruit.github.io/peruvian-food-ontology/ontology#>
INSERT { ?dish pf:tieneIngrediente ?canonical }
WHERE  { ?dish pf:tieneIngrediente ?alias . ?alias pf:sinonimoDe ?canonical }
