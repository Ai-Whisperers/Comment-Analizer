# Guía de Instalación Técnica - Agosto 2025

## 🎯 **Objetivo**
Esta guía cubre todos los métodos de instalación disponibles para el Analizador de Comentarios, desde instalación automática hasta deployment en producción.

---

## 📋 **Requisitos del Sistema**

### **Mínimos**
- **OS**: Windows 10+, macOS 10.14+, Linux Ubuntu 18.04+
- **Python**: 3.11 o superior  
- **RAM**: 4GB mínimo, 8GB recomendado
- **Almacenamiento**: 1GB libre
- **Internet**: Requerido para análisis IA

### **Recomendados**
- **RAM**: 16GB para archivos grandes
- **SSD**: Para mejor rendimiento
- **Conexión**: Banda ancha para Streamlit Cloud

---

## 🚀 **Método 1: Instalación Automática Windows**

### **Para Usuarios No-Técnicos**

#### **Proceso UN CLIC**:
```batch
# 1. Descargar proyecto completo
# 2. Ejecutar START_HERE.bat
# 3. Seguir instrucciones en pantalla
# 4. ¡Listo!
```

#### **Lo que hace automáticamente**:
1. **Detecta Python**: Verifica instalación existente
2. **Instala Python**: Via winget o descarga directa si no existe
3. **Crea entorno virtual**: Aislamiento de dependencias
4. **Instala dependencias**: Todas las librerías requeridas
5. **Configura OpenAI**: Ayuda interactiva para API key
6. **Inicia aplicación**: Abre navegador automáticamente

#### **Scripts de Soporte**:
- **bootstrap.ps1**: PowerShell avanzado (recomendado)
- **bootstrap.bat**: Command Prompt (fallback)
- **START_HERE.bat**: Launcher inteligente

---

## 💻 **Método 2: Instalación Manual Desarrolladores**

### **Paso a Paso Completo**

#### **1. Preparación del Entorno**
```bash
# Verificar Python
python --version  # Debe ser 3.11+

# Clonar repositorio
git clone https://github.com/Ai-Whisperers/Comment-Analizer.git
cd Comment-Analizer

# Crear entorno virtual (recomendado)
python -m venv venv

# Activar entorno
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

#### **2. Instalación de Dependencias**
```bash
# Instalar desde requirements.txt
pip install -r requirements.txt

# Verificar instalación crítica
python -c "import streamlit, pandas, plotly; print('✅ Dependencias OK')"
```

#### **3. Configuración de Variables**
```bash
# Crear archivo .env en raíz del proyecto
# Windows:
echo OPENAI_API_KEY=tu-clave-aqui > .env

# macOS/Linux:
echo "OPENAI_API_KEY=tu-clave-aqui" > .env
```

#### **4. Verificación de Instalación**
```bash
# Test básico
python -c "from src.config import Config; print('✅ Config OK')"

# Test de importaciones
python verify_imports.py

# Test de UI
python verify_ui_expectations.py
```

#### **5. Ejecución**
```bash
# Método principal
python run.py

# Alternativo
streamlit run streamlit_app.py

# Con puerto específico
streamlit run streamlit_app.py --server.port 8502
```

---

## 🐳 **Método 3: Docker**

### **Para Desarrollo y Producción**

#### **Prerequisitos**:
- Docker 20.10+
- Docker Compose 2.0+

#### **Construcción Básica**:
```dockerfile
# Usar imagen base optimizada
FROM python:3.11-slim

# Configurar directorio de trabajo
WORKDIR /app

# Copiar archivos de configuración
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar aplicación
COPY src/ src/
COPY streamlit_app.py .

# Puerto por defecto
EXPOSE 8501

# Comando de inicio
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

#### **Docker Compose**:
```yaml
version: '3.8'
services:
  comment-analyzer:
    build: .
    ports:
      - "8501:8501"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./data:/app/data
      - ./outputs:/app/outputs
    restart: unless-stopped
```

#### **Comandos de Deployment**:
```bash
# Desarrollo
docker-compose up --build

# Producción
docker-compose -f docker-compose.yml up -d

# Logs
docker-compose logs -f

# Escalamiento
docker-compose up --scale comment-analyzer=3
```

---

## ☁️ **Método 4: Streamlit Cloud**

### **Deployment Automático**

#### **Configuración en Streamlit**:
1. **Conectar repositorio**: GitHub integration
2. **Configurar secrets**: 
   ```toml
   [general]
   OPENAI_API_KEY = "tu-clave-openai"
   ```
3. **Seleccionar entry point**: `streamlit_app.py`
4. **Deploy automático**: Push triggers deployment

#### **Características del Deployment**:
- **URL automática**: https://comment-analizer.streamlit.app
- **SSL incluido**: HTTPS automático
- **Escalamiento**: Automático según tráfico
- **Monitoreo**: Dashboard integrado
- **Logs**: Accesibles via interfaz web

#### **Optimizaciones para Cloud**:
```python
# Límites optimizados para 690MB
MAX_FILE_SIZE_MB = 3
MAX_COMMENTS = 500
CACHE_MAX_ENTRIES = 500

# Gestión de memoria agresiva
optimize_memory() # Llamadas estratégicas
```

---

## ⚙️ **Configuración Avanzada**

### **Variables de Entorno Completas**

#### **Requeridas**:
```env
OPENAI_API_KEY=sk-proj-tu-clave-real-aqui
```

#### **Opcionales con Defaults**:
```env
# OpenAI Configuration
OPENAI_MODEL=gpt-4                 # Modelo a usar
OPENAI_MAX_TOKENS=2000             # Tokens máximos por request
OPENAI_TEMPERATURE=0.7             # Creatividad (0.0-1.0)

# Streamlit Configuration  
STREAMLIT_PORT=8501                # Puerto del servidor
STREAMLIT_HOST=localhost           # Host binding

# Application Configuration
LOG_LEVEL=INFO                     # Nivel de logging
MAX_FILE_SIZE_MB=10                # Tamaño máximo archivo (local)
MAX_COMMENTS=1000                  # Comentarios máximos (local)

# Performance Tuning
CACHE_TTL=300                      # TTL cache en segundos
CHUNK_SIZE=100                     # Tamaño chunks procesamiento
MEMORY_CLEANUP_INTERVAL=200        # Interval limpieza memoria
```

### **Configuración de Logging**

#### **Archivo de configuración** (`logging.conf`):
```ini
[loggers]
keys=root,comment_analyzer

[handlers]
keys=consoleHandler,fileHandler

[formatters]
keys=detailedFormatter

[logger_root]
level=INFO
handlers=consoleHandler

[logger_comment_analyzer]
level=INFO
handlers=fileHandler
qualname=comment_analyzer

[handler_consoleHandler]
class=StreamHandler
level=INFO
formatter=detailedFormatter
args=(sys.stdout,)

[handler_fileHandler]
class=handlers.RotatingFileHandler
level=INFO
formatter=detailedFormatter
args=('logs/comment_analyzer.log', 'a', 10485760, 5)

[formatter_detailedFormatter]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

---

## 🛠️ **Troubleshooting Instalación**

### **Errores Comunes Windows**

#### **"python no se reconoce"**
```batch
# Solución 1: Instalar desde Microsoft Store
winget install Python.Python.3.11

# Solución 2: Descargar desde python.org
# Agregar a PATH durante instalación
```

#### **"pip install falla"**
```bash
# Actualizar pip
python -m pip install --upgrade pip

# Reinstalar con cache limpio
pip install -r requirements.txt --no-cache-dir --force-reinstall
```

#### **"ModuleNotFoundError después de instalación"**
```bash
# Verificar entorno virtual activado
echo $VIRTUAL_ENV  # debe mostrar path al venv

# Reinstalar en entorno correcto
pip install -r requirements.txt
```

### **Errores Comunes macOS/Linux**

#### **"Permission denied"**
```bash
# Usar virtualenv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# O instalar para usuario
pip install --user -r requirements.txt
```

#### **"SSL Certificate error"**
```bash
# Actualizar certificados
/Applications/Python\ 3.11/Install\ Certificates.command  # macOS

# O bypass temporal
pip install --trusted-host pypi.org --trusted-host pypi.python.org -r requirements.txt
```

### **Errores Docker**

#### **"Build fails"**
```bash
# Limpiar cache
docker system prune -a

# Build sin cache
docker-compose build --no-cache
```

#### **"Container exits immediately"**
```bash
# Ver logs detallados
docker-compose logs comment-analyzer

# Ejecutar interactivo para debug
docker-compose run --rm comment-analyzer bash
```

---

## 📊 **Verificación Post-Instalación**

### **Tests de Funcionalidad**

#### **Test Básico**:
```bash
# 1. La aplicación inicia
curl http://localhost:8501/_stcore/health

# 2. UI carga correctamente
# Verificar en navegador: http://localhost:8501

# 3. Importaciones funcionan
python -c "from src.main import *; print('✅ Import test passed')"
```

#### **Test de Análisis**:
```bash
# 1. Crear archivo de prueba
echo "comentario,Excelente servicio" > test.csv

# 2. Procesar via interfaz web
# 3. Verificar resultados generados
```

#### **Test de Memoria**:
```bash
# Monitor durante procesamiento
# Verificar que memoria no excede límites configurados
```

### **Benchmarks de Rendimiento**

#### **Tiempos Esperados**:
- **Startup**: 5-10 segundos
- **Import 100 comentarios**: 30-60 segundos
- **Análisis rápido**: 10-30 segundos
- **Análisis IA**: 60-120 segundos
- **Export Excel**: 5-15 segundos

#### **Recursos Esperados**:
- **RAM inicial**: 150-200MB
- **RAM procesando**: 300-500MB (local), <100MB (cloud)
- **CPU**: Bajo (<50%) excepto durante análisis
- **Disco**: <1GB para instalación completa

---

## 🔄 **Actualizaciones y Mantenimiento**

### **Actualizar Aplicación**:
```bash
# Git pull
git pull origin main

# Actualizar dependencias
pip install -r requirements.txt --upgrade

# Verificar cambios breaking
python verify_setup.py
```

### **Backup de Configuración**:
```bash
# Respaldar archivos críticos
cp .env .env.backup
cp -r data/ data_backup/
cp -r outputs/ outputs_backup/
```

### **Monitoreo de Salud**:
```bash
# Health check endpoint
curl http://localhost:8501/_stcore/health

# Logs de aplicación
tail -f logs/comment_analyzer_*.log

# Uso de recursos
htop  # Linux/macOS
tasklist  # Windows
```

---

## 📞 **Soporte Técnico**

### **Recursos de Ayuda**:
- **Documentación completa**: `/documentation/` folder
- **Logs detallados**: `/logs/` folder  
- **Issues GitHub**: Para reportar problemas
- **Código fuente**: Comentarios extensivos en código

### **Información para Reportes**:
Incluir siempre:
```bash
# Versión Python
python --version

# Versiones dependencias
pip freeze > installed_packages.txt

# Logs recientes
tail -50 logs/comment_analyzer_*.log

# Configuración (sin API keys)
env | grep -v API_KEY
```

---

*Guía técnica actualizada: 30 de Agosto, 2025*  
*Versión de aplicación: 2.0 - Optimizada para producción*  
*Próxima revisión: Septiembre 2025*