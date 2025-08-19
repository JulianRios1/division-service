# 🚀 division-service

## Shipments Processing Platform - Independent Cloud Run Service

### 🏗️ **Arquitectura**
- **Patrón**: Microservicio independiente
- **Deploy**: Cloud Run
- **Scaling**: Serverless (0-1000 instancias)
- **Monitoring**: Cloud Monitoring + Structured Logging

### 🚀 **Quick Deploy**
```bash
# Deploy directo a Cloud Run
gcloud run deploy division-service \
    --source . \
    --region us-central1 \
    --allow-unauthenticated

# Via GitHub Actions (recomendado)
git push origin main
```

### 🔧 **Development**
```bash
# Setup local
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run locally
python src/main.py
```

### 📊 **Endpoints**
- `GET /health` - Health check
- `GET /status` - Detailed status
- Ver `src/main.py` para endpoints específicos

### 🏷️ **Versioning**
- **Current**: v2.0.0
- **Strategy**: Semantic Versioning
- **Releases**: Automated via GitHub Actions

### 🔗 **Dependencies**
- **Shared Libraries**: Auto-included in build
- **External Services**: Ver `.env.example`
- **GCP Services**: Cloud Run, Cloud Storage, Cloud SQL

### 📝 **Logs**
```bash
# Ver logs en tiempo real
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=division-service" --limit=50

# Logs de errores
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=division-service AND severity>=ERROR" --limit=20
```

### 🚨 **Troubleshooting**
- **Logs**: Cloud Console → Logging
- **Metrics**: Cloud Console → Cloud Run → division-service
- **Health**: `curl https://SERVICE_URL/health`

---
**🏗️ Part of Shipments Processing Platform**  
**☁️ Cloud Run Ready**  
**🔄 CI/CD Enabled**
