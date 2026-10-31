# Despliegue en Google Cloud (Cloud Run)

Fuseki sirve las dos versiones de la ontología en modo solo lectura:
`/base/query` y `/refined/query`. Las ontologías van dentro de la imagen; tras cada `build.py`, se reconstruye y se vuelve a desplegar.

## Local

```bash
podman build -f deploy/Dockerfile -t peruvian-food-fuseki .
podman run --rm -p 8080:8080 peruvian-food-fuseki
python scripts/evaluate.py --endpoint 'http://localhost:8080/{version}/query'
```

Interfaz de Fuseki: http://localhost:8080

## Cloud Run

Requisitos: proyecto de Google Cloud con facturación (Cloud Run tiene capa gratuita) y `gcloud` instalado.

```bash
PROJECT=<id-del-proyecto>
REGION=southamerica-west1
IMAGE=$REGION-docker.pkg.dev/$PROJECT/peruvian-food/fuseki

gcloud config set project $PROJECT
gcloud services enable run.googleapis.com artifactregistry.googleapis.com
gcloud artifacts repositories create peruvian-food --repository-format=docker --location=$REGION

gcloud auth print-access-token | podman login -u oauth2accesstoken --password-stdin https://$REGION-docker.pkg.dev
podman build -f deploy/Dockerfile -t $IMAGE .
podman push $IMAGE

gcloud run deploy peruvian-food-fuseki --image $IMAGE --region $REGION \
  --allow-unauthenticated --memory 512Mi --max-instances 1
```

El último comando imprime la URL del servicio. Evaluación contra la nube:

```bash
python scripts/evaluate.py --endpoint 'https://<url-del-servicio>/{version}/query'
```

Evidencias para el informe: captura de la consola de Cloud Run, de la interfaz de Fuseki con una consulta y de la salida de `evaluate.py` contra la URL pública.
