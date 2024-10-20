# Motivo de este repositorio

Este repositorio es una demostración para exponer una API desplegada en Cloud Run y exponerla en Api Gateway, protegiendp el acceso a traves de una cuenta de servivio (service account).

## Preparación

Una vez clone este repositorio deberas ejecutar

```bash
poetry init
poetry install
```

Ejecutar localmente

```bash
make start
```

## Configuración y Despliegue en GCP

### Configuración Inicial

Establecer la cuenta de Google Cloud

```bash
gcloud config set account [ACCOUNT_EMAIL]
```

Establecer el proyecto de Google Cloud

```bash
gcloud config set project [PROJECT_ID]
```

### Construcción y Despliegue de la Imagen Docker

Construir la imagen Docker

```bash
docker build --platform linux/amd64 -t gcr.io/[PROJECT_ID]/products-api:[VERSION] ./
```

Iniciar sesión en Google Container Registry

```bash
docker login gcr.io
```

Subir la imagen Docker a Google Container Registry

```bash
docker push gcr.io/[PROJECT_ID]/products-api:[VERSION]
```

Desplegar la imagen en Cloud Run

```bash
gcloud run deploy cr-products-api \
    --image gcr.io/[PROJECT_ID]/products-api:[VERSION] \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated
```

### Configuración de API Gateway

Crear una nueva API

```bash
gcloud api-gateway apis create api-products-api --project=[PROJECT_ID]
```

Crear una configuración de API

```bash
gcloud api-gateway api-configs create agcnf-products-api \
--api=api-products-api --openapi-spec=open-api-api-gateway.yaml \
--project=[PROJECT_ID] \
--backend-auth-service-account=[SERVICE_ACCOUNT_EMAIL]
```

Crear un gateway de API

```bash
gcloud api-gateway gateways create ag-products-api \
  --api-config=agcnf-products-api \
  --location=us-central1 \
  --project=[PROJECT_ID]
```

### Gestión de Cuentas de Servicio

Crear una cuenta de servicio

```bash
gcloud iam service-accounts create sa-products-api \
  --display-name="Mi Cuenta de Servicio para API Gateway" \
  --project=[PROJECT_ID]
```

Asignar el rol 'roles/run.invoker' a la cuenta de servicio

```bash
gcloud projects add-iam-policy-binding [PROJECT_ID] \
  --member="serviceAccount:[SERVICE_ACCOUNT_EMAIL]" \
  --role="roles/run.invoker"
```

Asignar el rol 'roles/iam.serviceAccountTokenCreator' a la cuenta de servicio

```bash
gcloud projects add-iam-policy-binding [PROJECT_ID] \
  --member="serviceAccount:[SERVICE_ACCOUNT_EMAIL]" \
  --role="roles/iam.serviceAccountTokenCreator"
```

Listar los roles de la cuenta de servicio

```bash
gcloud projects get-iam-policy [PROJECT_ID] \
  --filter="bindings.members:serviceAccount:[SERVICE_ACCOUNT_EMAIL]" \
  --format="table(bindings.role)"
```

Crear una clave privada para la cuenta de servicio

```bash
gcloud iam service-accounts keys create sa-products-api.json \
  --iam-account=[SERVICE_ACCOUNT_EMAIL] \
  --project=[PROJECT_ID]
```

### Actualización de la Configuración del API Gateway

Crear una nueva configuración de API

```bash
gcloud api-gateway api-configs create agcnf-products-api-v2 \
--api=api-products-api --openapi-spec=open-api-api-gateway.yaml \
--project=[PROJECT_ID] \
--backend-auth-service-account=[SERVICE_ACCOUNT_EMAIL]
```

Actualizar la configuración del gateway de API

```bash
gcloud api-gateway gateways update ag-products-api \
--api-config=agcnf-products-api-v2 --api=api-products-api \
--location=us-central1 --project=[PROJECT_ID]
```
