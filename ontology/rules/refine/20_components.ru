# Cadena de propiedades: tieneIngrediente o tieneComponente+ -> tieneIngrediente (ingredientes derivados).
PREFIX pf: <http://unitru.edu.pe/ai2/peruvian-food#>
INSERT { ?dish pf:tieneIngrediente ?part }
WHERE  { ?dish pf:tieneIngrediente/pf:tieneComponente+ ?part }
