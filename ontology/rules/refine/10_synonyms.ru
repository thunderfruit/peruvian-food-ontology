# Un ingrediente escrito con su sinónimo regional hereda el ingrediente canónico.
PREFIX pf: <http://unitru.edu.pe/ai2/peruvian-food#>
INSERT { ?dish pf:tieneIngrediente ?canonical }
WHERE  { ?dish pf:tieneIngrediente ?alias . ?alias pf:sinonimoDe ?canonical }
