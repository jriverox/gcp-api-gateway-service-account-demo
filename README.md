# Demo Protegiendo GCP Api Gateway usando Service Account

## Motivo de este repositorio

Este repositorio es una demostración para exponer una API desplegada en Cloud Run y exponerla en Api Gateway, protegiendo el acceso a traves de una cuenta de servivio (service account).

Caso de uso para una Cuenta de Servicio: Proteger el aceso a una API y permitir que otros servicios consuman el API protegida usando un token el cual está firmado por la private key de la cuenta de servicio. [Para saber más](https://cloud.google.com/api-gateway/docs/authenticate-service-account)

A pesar de que el objetivo principal de este repositorio es usar una cuenta de servicio para proteger el acceso del Api que se expone a través de Api Gateway cuando tienes un Sitio Web estático (típico SPA sea en react, vue, etc) no es aconsejable porque tendrías que exponer el archivo que contiene la llave privada. Para estos casos, existen otras soluciones como usar Firbase Authentication o un Api Key. En este caso por razones de simplicidad del demo yo he usado un Api key, por esta razón notarás que en la sección securityDefinitions del archivo *open-api-api-gateway.yaml* existe una definición para *api_key*. Si quieres saber más como crear un Api Key para un Api Gateway y restringir su uso para tu servicio te recomiendo mirar la [documentación](https://cloud.google.com/api-gateway/docs/authenticate-api-keys)

## Preparación

Una vez clones este repositorio deberas ejecutar

```bash
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

Desplegar la imagen en **Cloud Run**

```bash
gcloud run deploy cr-products-api \
    --image gcr.io/[PROJECT_ID]/products-api:[VERSION] \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated
```

**Nota:** El parametro *allow-unauthenticated* permite que cualquiera pueda aceder al API desplegada, por ahora está bien para probar el despliegue, pero luego necesitarás ejecutar el comando ***gcloud run services update*** sin el parametro *allow-unauthenticated*

## Configuración de GCP API Gateway

En resumen para crear un API Gateway se necesitan 7 pasos:

1. Crear un API con el comando ***gcloud api-gateway apis create***
2. Crear un Gateway para el api del punto anterior, comando: ***gcloud api-gateway gateways create***
3. Crear una Cuenta de Servicio
4. Asignar los roles: *run.invoker* y *roles/iam.serviceAccountTokenCreator*
5. Crear una configuracion usando un archivo Open Api .yaml con el comando ***gcloud api-gateway api-configs create***
6. Crear una private key de la cuenta de servicio y descargarla con el comando ***gcloud iam service-accounts keys create*** Este archivo es el que deberás utilizar para generar el token que se enviará en cada solicitud, ver el codigo en [generate_token_demo.py](generate_token_demo.py) o también la [documentación](https://cloud.google.com/api-gateway/docs/authenticate-service-account#making_an_authenticated_request)
7. Asignar la configuración al Gateway con el comando ***gcloud api-gateway gateways update***

***Nota:*** El token generado deberás enviarlo en el header, revisa el ejemplo en el link del paso 6.

Crear una nueva API

```bash
gcloud api-gateway apis create api-products-api --project=[PROJECT_ID]
```

Crear una configuración del API usando el achivo [open-api-api-gateway.yaml](open-api-api-gateway.yaml). En este archivo deberás agregar el valor de la cuenta de servicio que crearás más adelante.

```bash
gcloud api-gateway api-configs create agcnf-products-api \
--api=api-products-api --openapi-spec=open-api-api-gateway.yaml \
--project=[PROJECT_ID] \
--backend-auth-service-account=[SERVICE_ACCOUNT_EMAIL]
```

Crear un Gateway

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
