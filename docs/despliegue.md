# Guía de Despliegue - Analizador de Comentarios IA

## Opciones de Despliegue

### 1. Streamlit Cloud (Recomendado)
- ✅ **Gratuito** para uso personal/pequeño
- ✅ **Deploy automático** desde GitHub
- ✅ **Escalamiento** automático
- ✅ **SSL/HTTPS** incluido
- ✅ **Secrets management** integrado

### 2. Docker + Servidor VPS
- ✅ **Control completo** del entorno
- ✅ **Escalamiento** manual
- ⚙️ **Configuración** más compleja
- 💰 **Costo** del servidor

### 3. Heroku
- ✅ **Deploy fácil** con git
- ✅ **Add-ons** disponibles
- 💰 **Costo** por recursos

### 4. AWS/Google Cloud/Azure
- ✅ **Máxima escalabilidad**
- ✅ **Servicios** integrados
- ⚙️ **Configuración** avanzada
- 💰 **Costo** variable

---

## 🚀 Despliegue en Streamlit Cloud

### Preparación del Repositorio

#### 1. Verificar Archivos Requeridos
```bash
# Archivos obligatorios
requirements.txt        ✅
streamlit_app.py       ✅
README.md             ✅

# Archivos de configuración (opcional)
.streamlit/config.toml
.streamlit/secrets.toml
```

#### 2. Configurar .gitignore
```bash
# .gitignore
.env
.streamlit/secrets.toml
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
local-reports/
*.log
.DS_Store
```

#### 3. Optimizar requirements.txt para Cloud
```txt
# requirements.txt optimizado para Streamlit Cloud
streamlit>=1.39.0
pandas>=2.1.0
numpy>=1.25.0
openai>=1.50.0
openpyxl>=3.1.5
plotly>=5.18.0
python-dotenv>=1.0.1
langdetect>=1.0.9
requests>=2.32.0
xlsxwriter>=3.2.0
```

### Configuración en Streamlit Cloud

#### 1. Conectar Repositorio
1. Ve a [share.streamlit.io](https://share.streamlit.io)
2. **Conecta tu cuenta de GitHub**
3. **Autoriza Streamlit** para acceder a repositorios
4. **Selecciona tu repositorio**: `tu-usuario/Comment-Analizer`

#### 2. Configurar Deploy
```yaml
Repository: tu-usuario/Comment-Analizer
Branch: main
Main file path: streamlit_app.py
App URL: https://tu-usuario-comment-analyzer-main-streamlit-app-hash.streamlit.app
```

#### 3. Configurar Secrets
En la sección **Settings > Secrets**, agregar:
```toml
OPENAI_API_KEY = "sk-proj-tu-clave-openai-aqui"
OPENAI_MODEL = "gpt-4"
LOG_LEVEL = "INFO"
MAX_FILE_SIZE_MB = "10.0"
MAX_COMMENTS = "2000"
```

#### 4. Advanced Settings (Opcional)
```toml
# .streamlit/config.toml
[server]
maxUploadSize = 50
enableCORS = false
enableXsrfProtection = true

[theme]
primaryColor = "#8B5CF6"
backgroundColor = "#0f1419"
secondaryBackgroundColor = "#1c2128" 
textColor = "#e6edf3"

[browser]
gatherUsageStats = false
```

### Deploy Automático
1. **Hacer push** al repositorio
2. **Streamlit detecta** cambios automáticamente
3. **Deploy automático** en 2-3 minutos
4. **Aplicación disponible** en URL asignada

### Verificación Post-Deploy

#### 1. Verificar Estado
```bash
# Verificar que la app está corriendo
curl -I https://tu-app-url.streamlit.app
# Debe retornar: HTTP/2 200
```

#### 2. Test de Funcionalidad
1. **Acceder a la URL** de la aplicación
2. **Verificar carga** de página principal
3. **Probar navegación** entre páginas
4. **Cargar archivo** de prueba pequeño
5. **Ejecutar análisis** IA de prueba

#### 3. Monitorear Logs
- **Ver logs** en tiempo real en Streamlit Cloud dashboard
- **Verificar** que no hay errores de importación
- **Confirmar** conexión exitosa a OpenAI

---

## 🐳 Despliegue con Docker

### Dockerfile Optimizado

```dockerfile
FROM python:3.12-slim

# Metadatos
LABEL maintainer="tu-email@domain.com"
LABEL version="3.0.0"
LABEL description="Comment Analyzer AI - Streamlit App"

# Variables de entorno
ENV PYTHONPATH=/app
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
ENV STREAMLIT_SERVER_ENABLE_CORS=false

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar requirements y instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY . .

# Crear directorios necesarios
RUN mkdir -p local-reports static docs

# Exponer puerto
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Usuario no-root para seguridad
RUN useradd -m -u 1001 streamlit
RUN chown -R streamlit:streamlit /app
USER streamlit

# Comando de inicio
CMD ["streamlit", "run", "streamlit_app.py", "--server.address=0.0.0.0", "--server.port=8501"]
```

### Docker Compose

#### docker-compose.yml
```yaml
version: '3.8'

services:
  comment-analyzer:
    build: .
    container_name: comment-analyzer-ai
    ports:
      - "8501:8501"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - OPENAI_MODEL=${OPENAI_MODEL:-gpt-4}
      - LOG_LEVEL=${LOG_LEVEL:-INFO}
      - MAX_FILE_SIZE_MB=${MAX_FILE_SIZE_MB:-10.0}
      - MAX_COMMENTS=${MAX_COMMENTS:-2000}
    volumes:
      - ./local-reports:/app/local-reports
      - ./static:/app/static
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 5s
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.comment-analyzer.rule=Host(`comment-analyzer.tu-dominio.com`)"
      - "traefik.http.services.comment-analyzer.loadbalancer.server.port=8501"

  # Opcional: Nginx reverse proxy
  nginx:
    image: nginx:alpine
    container_name: comment-analyzer-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - comment-analyzer
    restart: unless-stopped
```

#### docker-compose.override.yml (Para desarrollo)
```yaml
version: '3.8'

services:
  comment-analyzer:
    build:
      context: .
      dockerfile: Dockerfile.dev
    volumes:
      - .:/app
      - /app/venv
    environment:
      - LOG_LEVEL=DEBUG
      - STREAMLIT_SERVER_RUN_ON_SAVE=true
    command: streamlit run streamlit_app.py --server.runOnSave=true
```

### Comandos de Despliegue Docker

#### Build y Run
```bash
# Construir imagen
docker build -t comment-analyzer:latest .

# Ejecutar container individual
docker run -d \
  --name comment-analyzer \
  -p 8501:8501 \
  -e OPENAI_API_KEY=tu-clave-aqui \
  comment-analyzer:latest

# Con Docker Compose
docker-compose up -d

# Ver logs
docker-compose logs -f comment-analyzer

# Actualizar
docker-compose pull
docker-compose up -d --build
```

#### Configuración con .env
```env
# .env para Docker Compose
OPENAI_API_KEY=sk-proj-tu-clave-openai
OPENAI_MODEL=gpt-4
LOG_LEVEL=INFO
MAX_FILE_SIZE_MB=10.0
MAX_COMMENTS=2000
COMPOSE_PROJECT_NAME=comment-analyzer
```

---

## ☁️ Despliegue en Heroku

### Preparación para Heroku

#### 1. Archivos Adicionales Requeridos

**Procfile**
```
web: streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0
```

**runtime.txt**
```
python-3.12.0
```

**app.json** (Para Heroku Button)
```json
{
  "name": "Comment Analyzer AI",
  "description": "AI-powered comment analysis with GPT-4",
  "repository": "https://github.com/tu-usuario/comment-analyzer",
  "logo": "https://ejemplo.com/logo.png",
  "keywords": ["streamlit", "ai", "gpt-4", "nlp", "sentiment-analysis"],
  "env": {
    "OPENAI_API_KEY": {
      "description": "OpenAI API Key for GPT-4 access",
      "required": true
    },
    "OPENAI_MODEL": {
      "description": "OpenAI model to use",
      "value": "gpt-4"
    }
  },
  "formation": {
    "web": {
      "quantity": 1,
      "size": "basic"
    }
  },
  "buildpacks": [
    {
      "url": "heroku/python"
    }
  ]
}
```

### Deploy en Heroku

#### 1. Heroku CLI
```bash
# Instalar Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Crear aplicación
heroku create tu-comment-analyzer

# Configurar variables de entorno
heroku config:set OPENAI_API_KEY=sk-proj-tu-clave
heroku config:set OPENAI_MODEL=gpt-4

# Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main

# Abrir aplicación
heroku open
```

#### 2. Deploy desde GitHub (Recomendado)
1. **Conectar repositorio** en Heroku Dashboard
2. **Habilitar deploy automático** desde branch main
3. **Configurar variables** de entorno en Settings > Config Vars
4. **Manual deploy** la primera vez

### Configuración de Variables Heroku
```bash
# Variables obligatorias
heroku config:set OPENAI_API_KEY=sk-proj-tu-clave
heroku config:set OPENAI_MODEL=gpt-4

# Variables opcionales
heroku config:set LOG_LEVEL=INFO
heroku config:set MAX_FILE_SIZE_MB=10.0
heroku config:set MAX_COMMENTS=2000

# Ver todas las variables
heroku config
```

---

## 🌐 Despliegue en VPS (Servidor Privado)

### Configuración del Servidor

#### 1. Preparar Servidor Ubuntu 22.04
```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependencias
sudo apt install -y python3 python3-pip python3-venv nginx git curl

# Instalar Docker (opcional)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

#### 2. Configurar Usuario de Aplicación
```bash
# Crear usuario dedicado
sudo useradd -m -s /bin/bash streamlit-app
sudo su - streamlit-app

# Clonar repositorio
git clone https://github.com/tu-usuario/comment-analyzer.git
cd comment-analyzer

# Configurar entorno virtual
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 3. Configurar Variables de Entorno
```bash
# Crear archivo .env
cat > .env << EOF
OPENAI_API_KEY=sk-proj-tu-clave-openai
OPENAI_MODEL=gpt-4
LOG_LEVEL=INFO
MAX_FILE_SIZE_MB=10.0
MAX_COMMENTS=2000
STREAMLIT_HOST=0.0.0.0
STREAMLIT_PORT=8501
EOF

# Proteger archivo
chmod 600 .env
```

### Configurar Nginx Reverse Proxy

#### nginx.conf
```nginx
server {
    listen 80;
    server_name tu-dominio.com www.tu-dominio.com;
    
    # Redirect HTTP to HTTPS
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name tu-dominio.com www.tu-dominio.com;
    
    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/tu-dominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/tu-dominio.com/privkey.pem;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
    
    # Gzip compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml;
    
    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;
    }
    
    # Static files (optional)
    location /static {
        alias /home/streamlit-app/comment-analyzer/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

### Configurar Servicio Systemd

#### streamlit-app.service
```ini
[Unit]
Description=Streamlit Comment Analyzer AI
After=network.target

[Service]
Type=simple
User=streamlit-app
WorkingDirectory=/home/streamlit-app/comment-analyzer
Environment=PATH=/home/streamlit-app/comment-analyzer/venv/bin
ExecStart=/home/streamlit-app/comment-analyzer/venv/bin/streamlit run streamlit_app.py --server.address=0.0.0.0 --server.port=8501
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### Activar Servicio
```bash
# Instalar servicio
sudo cp streamlit-app.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable streamlit-app
sudo systemctl start streamlit-app

# Verificar estado
sudo systemctl status streamlit-app

# Ver logs
sudo journalctl -u streamlit-app -f
```

### SSL con Let's Encrypt

```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx

# Obtener certificado
sudo certbot --nginx -d tu-dominio.com -d www.tu-dominio.com

# Renovación automática
sudo crontab -e
# Agregar línea:
# 0 12 * * * /usr/bin/certbot renew --quiet
```

---

## 📊 Monitoreo y Logs

### Configuración de Logs

#### 1. Logs de Aplicación
```python
# logging_config.py
import logging
import logging.handlers

def configurar_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('/var/log/streamlit-app/app.log'),
            logging.StreamHandler(),
            logging.handlers.RotatingFileHandler(
                '/var/log/streamlit-app/app.log',
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5
            )
        ]
    )
```

#### 2. Monitoreo con Prometheus (Opcional)
```yaml
# docker-compose.monitoring.yml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      
  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin123
```

### Health Checks

#### 1. Health Check Endpoint
```python
# En streamlit_app.py
import streamlit as st

def health_check():
    """Endpoint de salud para monitoreo"""
    try:
        # Verificar componentes críticos
        from src.aplicacion_principal import crear_aplicacion
        from config import config
        
        app = crear_aplicacion(config)
        if app.validar_sistema():
            return {"status": "healthy", "timestamp": datetime.now().isoformat()}
        else:
            return {"status": "unhealthy", "timestamp": datetime.now().isoformat()}
    except Exception as e:
        return {"status": "error", "error": str(e), "timestamp": datetime.now().isoformat()}
```

#### 2. Monitoring Script
```bash
#!/bin/bash
# monitor.sh

# Verificar que el servicio está corriendo
if ! systemctl is-active --quiet streamlit-app; then
    echo "❌ Streamlit app no está corriendo"
    sudo systemctl restart streamlit-app
    exit 1
fi

# Verificar respuesta HTTP
if ! curl -f -s http://localhost:8501/_stcore/health > /dev/null; then
    echo "❌ Health check falló"
    sudo systemctl restart streamlit-app
    exit 1
fi

echo "✅ Sistema funcionando correctamente"
```

---

## 🚀 CI/CD Pipeline

### GitHub Actions

#### .github/workflows/deploy.yml
```yaml
name: Deploy to Production

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        
    - name: Run tests
      run: |
        python -m pytest tests/ -v
        
    - name: Lint code
      run: |
        pip install flake8
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to Streamlit Cloud
      run: |
        # Streamlit Cloud deploy automático al hacer push
        echo "Deploy automático activado"
        
    - name: Deploy to Heroku
      uses: akhileshns/heroku-deploy@v3.12.12
      with:
        heroku_api_key: ${{secrets.HEROKU_API_KEY}}
        heroku_app_name: "tu-comment-analyzer"
        heroku_email: "tu-email@domain.com"
```

---

## 🔒 Consideraciones de Seguridad

### 1. Secrets Management
- **Nunca hardcodear** API keys
- **Usar secrets** de la plataforma (Streamlit/Heroku/etc.)
- **Rotar claves** regularmente
- **Monitorear** uso de API keys

### 2. Network Security
```nginx
# Configuración de seguridad en Nginx
# Rate limiting
limit_req_zone $binary_remote_addr zone=api:10m rate=30r/m;
limit_req zone=api burst=5;

# IP blocking (ejemplo)
deny 192.168.1.1;
allow all;
```

### 3. Backup y Recuperación
```bash
#!/bin/bash
# backup.sh

# Backup de configuración
tar -czf backup-$(date +%Y%m%d).tar.gz \
  .env \
  .streamlit/ \
  nginx.conf \
  streamlit-app.service

# Subir a storage (S3, etc.)
# aws s3 cp backup-$(date +%Y%m%d).tar.gz s3://tu-bucket/backups/
```

---

## 📈 Escalamiento y Performance

### 1. Configuración para Alto Tráfico
```yaml
# docker-compose.scale.yml
version: '3.8'

services:
  comment-analyzer:
    deploy:
      replicas: 3
    environment:
      - MAX_COMMENTS=1000  # Reducir para mejor performance
      - LOG_LEVEL=WARNING  # Menos logs
```

### 2. Load Balancer
```nginx
upstream streamlit_backend {
    server 127.0.0.1:8501;
    server 127.0.0.1:8502;
    server 127.0.0.1:8503;
}

server {
    location / {
        proxy_pass http://streamlit_backend;
    }
}
```

### 3. Caching Strategy
```python
# Implementar Redis para cache
import redis

cache = redis.Redis(host='localhost', port=6379, db=0)

def cache_analisis(comentarios_hash: str, resultado: AnalisisCompletoIA):
    """Cachear resultado de análisis"""
    cache.setex(comentarios_hash, 3600, resultado.to_json())  # 1 hora
```

---

**Estado**: Documentación completa de despliegue  
**Plataformas soportadas**: Streamlit Cloud, Heroku, VPS, Docker  
**Última actualización**: Septiembre 2025