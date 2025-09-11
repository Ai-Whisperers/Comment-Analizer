# Configuración del Sistema - Analizador de Comentarios IA

## Variables de Entorno

### Variables Obligatorias

#### OPENAI_API_KEY
```env
OPENAI_API_KEY=sk-proj-tu-clave-openai-aqui
```
- **Descripción**: Clave de API de OpenAI para acceso a GPT-4
- **Obligatorio**: ✅ Sí - El sistema no funcionará sin esta clave
- **Formato**: Debe empezar con `sk-proj-` o `sk-`
- **Obtención**: Desde [platform.openai.com/api-keys](https://platform.openai.com/api-keys)

### Variables de Configuración IA

#### OPENAI_MODEL
```env
OPENAI_MODEL=gpt-4
```
- **Descripción**: Modelo de IA a utilizar
- **Valor por defecto**: `gpt-4`
- **Opciones**: `gpt-4`, `gpt-4-turbo`, `gpt-3.5-turbo`
- **Recomendado**: `gpt-4` para mejor calidad de análisis

#### OPENAI_MAX_TOKENS
```env
OPENAI_MAX_TOKENS=4000
```
- **Descripción**: Número máximo de tokens por análisis
- **Valor por defecto**: `4000`
- **Rango**: 1000-8000
- **Recomendado**: 4000 para análisis completos

#### OPENAI_TEMPERATURE
```env
OPENAI_TEMPERATURE=0.7
```
- **Descripción**: Nivel de creatividad del modelo IA
- **Valor por defecto**: `0.7`
- **Rango**: 0.0-1.0
- **Interpretación**:
  - `0.0`: Más determinístico y consistente
  - `0.7`: Balance entre creatividad y consistencia
  - `1.0`: Más creativo pero menos predecible

### Variables del Sistema

#### LOG_LEVEL
```env
LOG_LEVEL=INFO
```
- **Descripción**: Nivel de detalle en los logs
- **Valor por defecto**: `INFO`
- **Opciones**: `DEBUG`, `INFO`, `WARNING`, `ERROR`
- **Uso**:
  - `DEBUG`: Para desarrollo y debugging
  - `INFO`: Para producción normal
  - `WARNING`: Solo advertencias y errores
  - `ERROR`: Solo errores críticos

#### MAX_FILE_SIZE_MB
```env
MAX_FILE_SIZE_MB=5.0
```
- **Descripción**: Tamaño máximo de archivo en MB
- **Valor por defecto**: `5.0`
- **Rango**: 1.0-50.0
- **Consideraciones**: Archivos más grandes requieren más memoria

#### MAX_COMMENTS
```env
MAX_COMMENTS=2000
```
- **Descripción**: Número máximo de comentarios por análisis
- **Valor por defecto**: `2000`
- **Rango**: 50-5000
- **Recomendado**: 1000-2000 para balance performance/costo

### Variables de Streamlit

#### STREAMLIT_PORT
```env
STREAMLIT_PORT=8501
```
- **Descripción**: Puerto para la aplicación web
- **Valor por defecto**: `8501`
- **Rango**: 1024-65535

#### STREAMLIT_HOST
```env
STREAMLIT_HOST=localhost
```
- **Descripción**: Host de la aplicación
- **Valor por defecto**: `localhost`
- **Opciones**: `localhost`, `0.0.0.0` (para acceso externo)

## Archivos de Configuración

### Archivo .env (Configuración Local)

**Ubicación**: Raíz del proyecto
**Nombre**: `.env`

```env
# === CONFIGURACIÓN OBLIGATORIA ===
OPENAI_API_KEY=sk-proj-tu-clave-openai-aqui

# === CONFIGURACIÓN IA ===
OPENAI_MODEL=gpt-4
OPENAI_MAX_TOKENS=4000
OPENAI_TEMPERATURE=0.7

# === CONFIGURACIÓN SISTEMA ===
LOG_LEVEL=INFO
MAX_FILE_SIZE_MB=5.0
MAX_COMMENTS=2000

# === CONFIGURACIÓN STREAMLIT ===
STREAMLIT_PORT=8501
STREAMLIT_HOST=localhost

# === CONFIGURACIÓN AVANZADA ===
# Timeout para llamadas a OpenAI (segundos)
OPENAI_TIMEOUT=300

# Número de reintentos en caso de error
OPENAI_MAX_RETRIES=3

# Tiempo de espera entre reintentos (segundos)  
OPENAI_RETRY_DELAY=2
```

### Configuración Streamlit

#### .streamlit/config.toml

**Ubicación**: `.streamlit/config.toml`

```toml
[theme]
# Colores del tema
primaryColor = "#8B5CF6"                # Purple para botones principales
backgroundColor = "#0f1419"             # Fondo oscuro principal
secondaryBackgroundColor = "#1c2128"    # Fondo secundario (sidebar, etc.)
textColor = "#e6edf3"                   # Color del texto principal

[server]
# Configuración del servidor
port = 8501
address = "localhost"
maxUploadSize = 50                      # MB - Tamaño máximo de archivos
enableCORS = false
enableXsrfProtection = true

[browser]
# Configuración del navegador
gatherUsageStats = false                # No enviar estadísticas a Streamlit
serverPort = 8501
serverAddress = "localhost"

[global]
# Configuración global
developmentMode = false
logLevel = "info"
```

#### .streamlit/secrets.toml (Para Streamlit Cloud)

**Ubicación**: `.streamlit/secrets.toml`
**Uso**: Solo para despliegue en Streamlit Cloud

```toml
# Secrets para Streamlit Cloud
OPENAI_API_KEY = "sk-proj-tu-clave-openai-aqui"
OPENAI_MODEL = "gpt-4"
LOG_LEVEL = "INFO"
MAX_FILE_SIZE_MB = "5.0"
MAX_COMMENTS = "2000"
```

### config.py (Configuración Centralizada)

El archivo `config.py` unifica toda la configuración:

```python
import os
from typing import Dict, Any
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def get_config() -> Dict[str, Any]:
    """Obtener configuración unificada del sistema"""
    return {
        # OpenAI Configuration
        'openai_api_key': os.getenv('OPENAI_API_KEY', ''),
        'openai_model': os.getenv('OPENAI_MODEL', 'gpt-4'),
        'openai_max_tokens': int(os.getenv('OPENAI_MAX_TOKENS', '4000')),
        'openai_temperature': float(os.getenv('OPENAI_TEMPERATURE', '0.7')),
        'openai_timeout': int(os.getenv('OPENAI_TIMEOUT', '300')),
        'openai_max_retries': int(os.getenv('OPENAI_MAX_RETRIES', '3')),
        'openai_retry_delay': int(os.getenv('OPENAI_RETRY_DELAY', '2')),
        
        # System Configuration
        'log_level': os.getenv('LOG_LEVEL', 'INFO'),
        'max_file_size_mb': float(os.getenv('MAX_FILE_SIZE_MB', '5.0')),
        'max_comments': int(os.getenv('MAX_COMMENTS', '2000')),
        
        # Streamlit Configuration
        'streamlit_port': int(os.getenv('STREAMLIT_PORT', '8501')),
        'streamlit_host': os.getenv('STREAMLIT_HOST', 'localhost'),
        
        # Cache Configuration
        'enable_cache': os.getenv('ENABLE_CACHE', 'true').lower() == 'true',
        'cache_ttl': int(os.getenv('CACHE_TTL', '3600')),  # 1 hour
        
        # Performance Configuration
        'batch_size': int(os.getenv('BATCH_SIZE', '100')),
        'processing_timeout': int(os.getenv('PROCESSING_TIMEOUT', '600')),
    }

# Configuración global
config = get_config()
```

## Configuraciones por Entorno

### Desarrollo Local

```env
# .env para desarrollo
OPENAI_API_KEY=sk-proj-tu-clave-desarrollo
OPENAI_MODEL=gpt-4
LOG_LEVEL=DEBUG
MAX_FILE_SIZE_MB=2.0
MAX_COMMENTS=100
STREAMLIT_HOST=localhost
ENABLE_CACHE=false
```

### Staging/Testing

```env
# .env para testing
OPENAI_API_KEY=sk-proj-tu-clave-testing
OPENAI_MODEL=gpt-4
LOG_LEVEL=INFO
MAX_FILE_SIZE_MB=5.0
MAX_COMMENTS=500
STREAMLIT_HOST=0.0.0.0
ENABLE_CACHE=true
```

### Producción

```env
# .env para producción
OPENAI_API_KEY=sk-proj-tu-clave-produccion
OPENAI_MODEL=gpt-4
OPENAI_MAX_TOKENS=4000
LOG_LEVEL=WARNING
MAX_FILE_SIZE_MB=10.0
MAX_COMMENTS=2000
STREAMLIT_HOST=0.0.0.0
ENABLE_CACHE=true
OPENAI_TIMEOUT=600
```

## Configuración para Diferentes Casos de Uso

### Análisis Rápido (Pocos Comentarios)

```env
# Optimizado para < 100 comentarios
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_MAX_TOKENS=2000
OPENAI_TEMPERATURE=0.5
MAX_COMMENTS=100
BATCH_SIZE=50
```

### Análisis Profundo (Muchos Comentarios)

```env
# Optimizado para 1000+ comentarios
OPENAI_MODEL=gpt-4
OPENAI_MAX_TOKENS=6000
OPENAI_TEMPERATURE=0.7
MAX_COMMENTS=2000
BATCH_SIZE=200
OPENAI_TIMEOUT=900
```

### Análisis Económico (Reducir Costos)

```env
# Optimizado para minimizar costo
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_MAX_TOKENS=3000
MAX_COMMENTS=500
BATCH_SIZE=100
```

## Monitoreo y Logging

### Configuración de Logging

```python
# logging.conf
[loggers]
keys=root,openai,streamlit

[handlers]
keys=consoleHandler,fileHandler

[formatters]
keys=simpleFormatter,detailedFormatter

[logger_root]
level=INFO
handlers=consoleHandler,fileHandler

[logger_openai]
level=DEBUG
handlers=fileHandler
qualname=openai
propagate=0

[handler_consoleHandler]
class=StreamHandler
level=INFO
formatter=simpleFormatter
args=(sys.stdout,)

[handler_fileHandler]
class=FileHandler
level=DEBUG
formatter=detailedFormatter
args=('app.log',)

[formatter_simpleFormatter]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s

[formatter_detailedFormatter]
format=%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s
```

### Variables de Monitoreo

```env
# Logging avanzado
LOG_FILE=app.log
LOG_MAX_SIZE=10MB
LOG_BACKUP_COUNT=5
ENABLE_PERFORMANCE_LOGGING=true
ENABLE_OPENAI_LOGGING=true
```

## Seguridad

### Variables de Seguridad

```env
# Configuración de seguridad
ENABLE_AUTH=false                       # Para futuras implementaciones
SESSION_TIMEOUT=3600                    # Timeout de sesión en segundos
MAX_CONCURRENT_ANALYSES=5               # Análisis concurrentes por usuario
RATE_LIMIT_REQUESTS_PER_MINUTE=60      # Límite de requests por minuto
```

### Mejores Prácticas de Seguridad

#### 1. Manejo de API Keys
```bash
# NUNCA hagas commit de API keys
echo ".env" >> .gitignore
echo ".streamlit/secrets.toml" >> .gitignore

# Usar variables de entorno en producción
export OPENAI_API_KEY="sk-proj-tu-clave"

# Rotar claves regularmente
# Usar diferentes claves para dev/staging/prod
```

#### 2. Validación de Configuración

```python
def validar_configuracion():
    """Validar configuración al inicio"""
    required_vars = ['OPENAI_API_KEY']
    
    for var in required_vars:
        if not os.getenv(var):
            raise ValueError(f"Variable requerida {var} no encontrada")
    
    # Validar formato de API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key.startswith(('sk-', 'sk-proj-')):
        raise ValueError("Formato de OPENAI_API_KEY inválido")
    
    # Validar rangos numéricos
    max_tokens = int(os.getenv('OPENAI_MAX_TOKENS', '4000'))
    if not 1000 <= max_tokens <= 8000:
        raise ValueError("OPENAI_MAX_TOKENS debe estar entre 1000 y 8000")
```

## Configuración de Performance

### Optimización de Memoria

```env
# Configuración de memoria
STREAMLIT_SERVER_MAX_UPLOAD_SIZE=50     # MB
PANDAS_MEMORY_LIMIT=1000                # MB  
ENABLE_GARBAGE_COLLECTION=true
GC_THRESHOLD_0=700
GC_THRESHOLD_1=10
GC_THRESHOLD_2=10
```

### Configuración de Cache

```env
# Configuración de caché
ENABLE_CACHE=true
CACHE_TTL=3600                          # 1 hora
CACHE_MAX_SIZE=100                      # Máximo elementos
CACHE_TYPE=memory                       # memory|redis|disk
```

### Configuración de Timeout

```env
# Timeouts del sistema
OPENAI_TIMEOUT=300                      # 5 minutos
HTTP_TIMEOUT=60                         # 1 minuto
FILE_PROCESSING_TIMEOUT=120             # 2 minutos
UI_RESPONSE_TIMEOUT=30                  # 30 segundos
```

## Configuración Docker

### docker-compose.yml

```yaml
version: '3.8'
services:
  comment-analyzer:
    build: .
    ports:
      - "${STREAMLIT_PORT:-8501}:8501"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - OPENAI_MODEL=${OPENAI_MODEL:-gpt-4}
      - LOG_LEVEL=${LOG_LEVEL:-INFO}
      - MAX_FILE_SIZE_MB=${MAX_FILE_SIZE_MB:-5.0}
      - MAX_COMMENTS=${MAX_COMMENTS:-2000}
    volumes:
      - ./local-reports:/app/local-reports
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### Dockerfile

```dockerfile
FROM python:3.12-slim

# Configuración de argumentos
ARG OPENAI_API_KEY
ARG LOG_LEVEL=INFO

# Variables de entorno
ENV OPENAI_API_KEY=${OPENAI_API_KEY}
ENV LOG_LEVEL=${LOG_LEVEL}
ENV PYTHONPATH=/app
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

CMD ["streamlit", "run", "streamlit_app.py", "--server.address=0.0.0.0"]
```

## Validación de Configuración

### Script de Validación

```bash
# validate_config.py
python -c "
import os
from dotenv import load_dotenv
load_dotenv()

# Verificar variables críticas
required_vars = {
    'OPENAI_API_KEY': 'sk-',
    'OPENAI_MODEL': ['gpt-4', 'gpt-3.5-turbo'],
    'LOG_LEVEL': ['DEBUG', 'INFO', 'WARNING', 'ERROR']
}

for var, expected in required_vars.items():
    value = os.getenv(var)
    if not value:
        print(f'❌ {var} no configurada')
    elif isinstance(expected, str) and not value.startswith(expected):
        print(f'❌ {var} formato incorrecto')  
    elif isinstance(expected, list) and value not in expected:
        print(f'❌ {var} valor no válido: {value}')
    else:
        print(f'✅ {var} configurada correctamente')

print('\\n✅ Validación de configuración completada')
"
```

### Comando de Diagnóstico

```bash
# Crear script diagnóstico
python -c "
import streamlit as st
import openai
import pandas as pd
import sys
import os
from dotenv import load_dotenv

load_dotenv()

print('🔍 DIAGNÓSTICO DEL SISTEMA')
print('=' * 40)

# Python version
print(f'Python: {sys.version.split()[0]}')

# Package versions  
print(f'Streamlit: {st.__version__}')
print(f'OpenAI: {openai.__version__}')
print(f'Pandas: {pd.__version__}')

# Configuration
api_key = os.getenv('OPENAI_API_KEY')
print(f'API Key: {\"✅ Configurada\" if api_key else \"❌ No configurada\"}')
print(f'Model: {os.getenv(\"OPENAI_MODEL\", \"No configurado\")}')
print(f'Log Level: {os.getenv(\"LOG_LEVEL\", \"No configurado\")}')

print('\\n✅ Diagnóstico completado')
"
```

---

**Configuración validada**: Todos los entornos (desarrollo, staging, producción)  
**Última actualización**: Septiembre 2025  
**Estado**: ✅ Documentación completa y probada