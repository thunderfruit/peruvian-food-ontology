# Despliegue en Render

Fuseki sirve las dos versiones de la ontología en modo solo lectura:
`/base/query` y `/refined/query`. Las ontologías van dentro de la imagen; tras cada `build.py` se hace commit y push, y Render reconstruye y vuelve a desplegar.

Servicio: https://peruvian-food-ontology.onrender.com (interfaz de Fuseki en esa misma dirección).

## Local

```bash
podman build -f deploy/Dockerfile -t peruvian-food-fuseki .
podman run --rm -p 8080:8080 peruvian-food-fuseki
python scripts/evaluate.py --endpoint 'http://localhost:8080/{version}/query'
```

Interfaz de Fuseki: http://localhost:8080

## Render

1. En https://dashboard.render.com: **New > Web Service** y conectar el repositorio de GitHub.
2. Configuración:
   - Language: **Docker**
   - Branch: `main`
   - Root Directory: vacío (la raíz del repositorio)
   - Dockerfile Path: `deploy/Dockerfile`
   - Docker Build Context: `.`
   - Instance Type: **Free**
3. **Create Web Service**. Render define la variable `PORT` y el `Dockerfile` la usa.

Con la capa gratuita, el servicio se duerme tras unos 15 minutos sin consultas; la primera consulta después tarda cerca de un minuto en despertarlo.

Evaluación contra la nube:

```bash
python scripts/evaluate.py --endpoint 'https://peruvian-food-ontology.onrender.com/{version}/query'
```

Comprobación rápida (debe responder 200; una operación de actualización, 405):

```bash
curl -s -o /dev/null -w '%{http_code}\n' https://peruvian-food-ontology.onrender.com/\$/ping
```

Evidencias para el informe: captura del panel de Render, de la interfaz de Fuseki con una consulta, del prototipo (`prototype/recommender.html`) y de la salida de `evaluate.py` contra la URL pública.
