# Perfiles cualitativos, versión refinada (tras el análisis de errores de la versión base):
# - Bajo en calorías: técnica saludable; se admite aceite vegetal en poca cantidad, pero no grasa animal,
#   carne grasa, azúcar añadido, maní o frutos secos, ni dos o más lácteos.
# - Alto en proteínas: fuente proteica principal (carne, ave, pescado, marisco o legumbre); el huevo y los
#   lácteos como acompañamiento no cuentan; no aplica a postres ni bebidas.
# - Mantenimiento: sin fritura, sin carne grasa ni grasa animal y sin azúcar añadido.
PREFIX pf: <https://thunderfruit.github.io/peruvian-food-ontology/ontology#>
INSERT { ?dish a pf:PlatoBajoEnCalorias }
WHERE  { ?dish a pf:Plato ; pf:tecnicaDeCoccion/pf:esTecnicaSaludable true
         FILTER NOT EXISTS { ?dish pf:tieneIngrediente ?ing . ?ing pf:tipoDeAlimento ?t
                             VALUES ?t { "grasa_animal" "carne_grasa" "azucar" } }
         FILTER NOT EXISTS { ?dish pf:tieneIngrediente ?ing . ?ing pf:contieneAlergeno ?a
                             VALUES ?a { pf:alergeno_mani pf:alergeno_frutos_secos } }
         FILTER NOT EXISTS { ?dish pf:tieneIngrediente ?d1, ?d2 .
                             ?d1 pf:tipoDeAlimento "lacteo" . ?d2 pf:tipoDeAlimento "lacteo"
                             FILTER (?d1 != ?d2) } } ;
INSERT { ?dish a pf:PlatoAltoEnProteinas }
WHERE  { ?dish a pf:Plato ; pf:tieneIngrediente ?ing . ?ing pf:tipoDeAlimento ?t
         VALUES ?t { "carne" "carne_grasa" "ave" "pescado" "marisco" "legumbre" }
         FILTER NOT EXISTS { ?dish pf:tipoDePlato ?type FILTER (?type IN ("postre", "bebida")) } } ;
INSERT { ?dish a pf:PlatoAptoParaPerdidaDePeso }
WHERE  { ?dish a pf:PlatoBajoEnCalorias, pf:PlatoAltoEnProteinas } ;
INSERT { ?dish a pf:PlatoAptoParaMantenimientoDePeso }
WHERE  { ?dish a pf:Plato ; pf:tecnicaDeCoccion ?tech
         FILTER (?tech != pf:tecnica_frito)
         FILTER NOT EXISTS { ?dish pf:tieneIngrediente ?ing . ?ing pf:tipoDeAlimento ?t
                             VALUES ?t { "carne_grasa" "grasa_animal" "azucar" } } }
