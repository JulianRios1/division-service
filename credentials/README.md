# 🔐 Configuración de Credenciales GCP

## Para Desarrollo Local

### 1. Crear Service Account en GCP Console

1. Ve a [GCP Console > IAM & Admin > Service Accounts](https://console.cloud.google.com/iam-admin/serviceaccounts)
2. Crea un nuevo Service Account con los siguientes permisos:
   - **Storage Admin** (para buckets)
   - **Pub/Sub Admin** (para mensajería)
   - **Cloud SQL Client** (para PostgreSQL)
   - **Cloud Run Developer** (para servicios)
   - **Logs Writer** (para logging)

### 2. Descargar Credenciales JSON

1. En el Service Account creado, ve a **Keys**
2. Clic en **Add Key > Create New Key**
3. Selecciona **JSON** y descarga el archivo
4. Guarda el archivo como `service-account-key.json` en este directorio

### 3. Configurar Variables de Entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar el archivo .env y configurar:
GOOGLE_APPLICATION_CREDENTIALS=./credentials/service-account-key.json
GOOGLE_CLOUD_PROJECT=tu-project-id-real
```

### 4. Verificar Configuración

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar prueba de conexión
python -c "
from src.shared_utils.config import config
from google.cloud import storage
client = storage.Client()
print('✅ Credenciales configuradas correctamente')
print(f'Proyecto: {client.project}')
"
```

## Para Producción (Cloud Run)

En producción, Cloud Run usa **Workload Identity** automáticamente:

1. El deployment se maneja via GitHub Actions
2. Las credenciales se almacenan como secrets en GitHub:
   - `GCP_PROJECT_ID`: ID del proyecto GCP
   - `GCP_SA_KEY`: Contenido completo del JSON del Service Account

## Seguridad

⚠️ **IMPORTANTE:**
- **NUNCA** subas archivos de credenciales al repositorio
- El directorio `credentials/` está incluido en `.gitignore`
- Usa diferentes Service Accounts para desarrollo y producción
- Revisa permisos regularmente y aplica principio de menor privilegio

## Troubleshooting

### Error: "Could not automatically determine credentials"
- Verifica que `GOOGLE_APPLICATION_CREDENTIALS` apunte al archivo correcto
- Verifica que el archivo JSON existe y es válido

### Error: "Permission denied"
- Verifica que el Service Account tenga los permisos necesarios
- Revisa que el proyecto ID sea correcto en las variables de entorno

### Error de conexión a PostgreSQL
- Para desarrollo local, levanta una instancia de PostgreSQL
- Para producción, configura Cloud SQL correctamente
