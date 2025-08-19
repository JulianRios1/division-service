#!/usr/bin/env python3
"""
🔐 Script para verificar la configuración de credenciales GCP
Útil para debugging y setup de desarrollo
"""

import os
import sys
import json
from pathlib import Path

# Agregar el directorio src al path para importar módulos
sys.path.append(str(Path(__file__).parent.parent / 'src'))

try:
    from shared_utils.config import config
    from google.cloud import storage
    from google.cloud import pubsub_v1
    import psycopg2
    print("✅ Todas las librerías importadas correctamente")
except ImportError as e:
    print(f"❌ Error importando librerías: {e}")
    print("Ejecuta: pip install -r requirements.txt")
    sys.exit(1)

def check_environment_variables():
    """Verifica variables de entorno críticas"""
    print("\n🔍 Verificando variables de entorno...")
    
    required_vars = [
        'GOOGLE_CLOUD_PROJECT',
        'GOOGLE_APPLICATION_CREDENTIALS'
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing_vars.append(var)
            print(f"❌ {var}: No configurada")
        else:
            if var == 'GOOGLE_APPLICATION_CREDENTIALS':
                print(f"✅ {var}: {value}")
                # Verificar si el archivo existe
                if not Path(value).exists():
                    print(f"⚠️  ADVERTENCIA: El archivo {value} no existe")
                    missing_vars.append(var)
            else:
                print(f"✅ {var}: {value}")
    
    return len(missing_vars) == 0

def check_credentials_file():
    """Verifica el archivo de credenciales JSON"""
    print("\n🔍 Verificando archivo de credenciales...")
    
    creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if not creds_path:
        print("❌ GOOGLE_APPLICATION_CREDENTIALS no está configurada")
        return False
    
    creds_file = Path(creds_path)
    if not creds_file.exists():
        print(f"❌ Archivo de credenciales no existe: {creds_path}")
        return False
    
    try:
        with open(creds_file, 'r') as f:
            creds_data = json.load(f)
            
        required_keys = ['type', 'project_id', 'private_key', 'client_email']
        missing_keys = [key for key in required_keys if key not in creds_data]
        
        if missing_keys:
            print(f"❌ Faltan claves en el archivo JSON: {missing_keys}")
            return False
            
        print(f"✅ Archivo de credenciales válido")
        print(f"   - Tipo: {creds_data.get('type')}")
        print(f"   - Proyecto: {creds_data.get('project_id')}")
        print(f"   - Email: {creds_data.get('client_email')}")
        
        return True
        
    except json.JSONDecodeError:
        print(f"❌ El archivo {creds_path} no es un JSON válido")
        return False
    except Exception as e:
        print(f"❌ Error leyendo credenciales: {e}")
        return False

def check_gcp_connection():
    """Verifica conexión a GCP"""
    print("\n🔍 Verificando conexión a Google Cloud Storage...")
    
    try:
        client = storage.Client()
        print(f"✅ Cliente GCS creado exitosamente")
        print(f"   - Proyecto: {client.project}")
        
        # Intentar listar buckets (solo los primeros 5)
        buckets = list(client.list_buckets(max_results=5))
        print(f"✅ Acceso a buckets verificado ({len(buckets)} buckets encontrados)")
        
        return True
    except Exception as e:
        print(f"❌ Error conectando a GCS: {e}")
        return False

def check_pubsub_connection():
    """Verifica conexión a Pub/Sub"""
    print("\n🔍 Verificando conexión a Google Cloud Pub/Sub...")
    
    try:
        publisher = pubsub_v1.PublisherClient()
        project_path = publisher.common_project_path(config.GOOGLE_CLOUD_PROJECT)
        
        # Intentar listar topics
        topics = list(publisher.list_topics(request={"project": project_path}))
        print(f"✅ Acceso a Pub/Sub verificado ({len(topics)} topics encontrados)")
        
        return True
    except Exception as e:
        print(f"❌ Error conectando a Pub/Sub: {e}")
        return False

def check_database_connection():
    """Verifica conexión a PostgreSQL"""
    print("\n🔍 Verificando conexión a PostgreSQL...")
    
    try:
        db_url = config.get_database_url()
        # Solo verificar que se puede construir la URL, no conectar realmente
        # ya que la DB puede no estar disponible en desarrollo
        print(f"✅ URL de base de datos construida correctamente")
        print(f"   - Host: {config.DB_HOST}")
        print(f"   - Puerto: {config.DB_PORT}")
        print(f"   - Base de datos: {config.DB_NAME}")
        
        return True
    except Exception as e:
        print(f"❌ Error con configuración de base de datos: {e}")
        return False

def main():
    """Función principal de verificación"""
    print("🔐 VERIFICADOR DE CREDENCIALES GCP")
    print("=" * 50)
    
    checks = [
        ("Variables de entorno", check_environment_variables),
        ("Archivo de credenciales", check_credentials_file),
        ("Conexión a GCS", check_gcp_connection),
        ("Conexión a Pub/Sub", check_pubsub_connection),
        ("Configuración de DB", check_database_connection),
    ]
    
    results = {}
    for name, check_func in checks:
        results[name] = check_func()
    
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE VERIFICACIONES:")
    
    all_passed = True
    for name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {status} - {name}")
        if not passed:
            all_passed = False
    
    if all_passed:
        print("\n🎉 ¡Todas las verificaciones pasaron! El servicio está listo para funcionar.")
        print("\n💡 Para ejecutar el servicio:")
        print("   python src/main.py")
    else:
        print("\n⚠️  Algunas verificaciones fallaron. Revisa la configuración.")
        print("\n📚 Consulta el archivo credentials/README.md para instrucciones")
    
    sys.exit(0 if all_passed else 1)

if __name__ == "__main__":
    main()
