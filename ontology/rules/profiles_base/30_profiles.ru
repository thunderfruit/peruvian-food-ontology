# Perfiles cualitativos, versión base: solo técnica de cocción y categorías directas.
PREFIX pf: <https://thunderfruit.github.io/peruvian-food-ontology/ontology#>
INSERT { ?dish a pf:PlatoBajoEnCalorias }
WHERE  { ?dish a pf:Plato ; pf:tecnicaDeCoccion/pf:esTecnicaSaludable true
         FILTER NOT EXISTS { ?dish pf:tieneIngrediente ?ing . ?ing pf:tipoDeAlimento ?t
                             VALUES ?t { "grasa" "grasa_animal" "carne_grasa" } } } ;
INSERT { ?dish a pf:PlatoAltoEnProteinas }
WHERE  { ?dish a pf:Plato ; pf:tieneIngrediente ?ing . ?ing pf:tipoDeAlimento ?t
         VALUES ?t { "carne" "carne_grasa" "ave" "pescado" "marisco" "huevo" "legumbre" } } ;
INSERT { ?dish a pf:PlatoAptoParaPerdidaDePeso }
WHERE  { ?dish a pf:PlatoBajoEnCalorias, pf:PlatoAltoEnProteinas } ;
INSERT { ?dish a pf:PlatoAptoParaMantenimientoDePeso }
WHERE  { ?dish a pf:Plato ; pf:tecnicaDeCoccion ?tech
         FILTER (?tech != pf:tecnica_frito)
         FILTER NOT EXISTS { ?dish pf:tieneIngrediente ?ing . ?ing pf:tipoDeAlimento "carne_grasa" } }
