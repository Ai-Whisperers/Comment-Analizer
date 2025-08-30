# Guía de Instalación - Analizador de Comentarios Personal Paraguay

Instrucciones completas para instalar y configurar el sistema profesional de análisis de comentarios con arquitectura multi-página.

---

## 🎯 **Requisitos del Sistema**

### **Hardware Mínimo**:
- **RAM**: 4GB mínimo, 8GB recomendado
- **Almacenamiento**: 500MB espacio libre
- **Procesador**: Intel i3 / AMD Ryzen 3 o superior
- **Conexión**: Internet estable (para análisis IA)

### **Software Requerido**:
- **Python**: 3.9, 3.10, 3.11, o 3.12
- **Sistema Operativo**: Windows 10+, macOS 10.15+, Ubuntu 20.04+
- **Navegador**: Chrome 90+, Firefox 88+, Edge 90+ 

---

## 🚀 **Método 1: Instalación Rápida**

### **Windows (Recomendado)**:
```batch
# 1. Descargar proyecto
git clone https://github.com/tu-repo/Comment-Analizer.git
cd Comment-Analizer

# 2. Instalación automática
pip install -r requirements.txt

# 3. Ejecutar aplicación
streamlit run streamlit_app.py
```

### **macOS/Linux**:
```bash
# 1. Descargar proyecto
git clone https://github.com/tu-repo/Comment-Analizer.git
cd Comment-Analizer

# 2. Crear entorno virtual (recomendado)
python3 -m venv comment_analyzer_env
source comment_analyzer_env/bin/activate  # Linux/macOS

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar aplicación
streamlit run streamlit_app.py
```

---

## 📦 **Método 2: Instalación Detallada**

### **Paso 1: Verificar Python**
```bash
# Verificar versión de Python
python --version
# o
python3 --version

# Resultado esperado: Python 3.9.x, 3.10.x, 3.11.x, o 3.12.x
```

Si Python no está instalado:
- **Windows**: Descargar desde [python.org](https://python.org/downloads)
- **macOS**: `brew install python3` (con Homebrew)
- **Ubuntu/Debian**: `sudo apt-get install python3 python3-pip`
- **CentOS/RHEL**: `sudo yum install python3 python3-pip`

### **Paso 2: Descargar Proyecto**
```bash
# Opción A: Con Git
git clone https://github.com/tu-repo/Comment-Analizer.git
cd Comment-Analizer

# Opción B: Descarga directa
# Descargar ZIP desde GitHub y extraer
# Navegar a la carpeta extraída
```

### **Paso 3: Crear Entorno Virtual** (Recomendado)
```bash
# Windows
python -m venv comment_analyzer_env
comment_analyzer_env\Scripts\activate

# macOS/Linux  
python3 -m venv comment_analyzer_env
source comment_analyzer_env/bin/activate

# Verificar activación (terminal debe mostrar (comment_analyzer_env))
```

### **Paso 4: Instalar Dependencias**
```bash
# Actualizar pip primero
pip install --upgrade pip

# Instalar todas las dependencias
pip install -r requirements.txt

# Verificar instalación principal
pip show streamlit pandas plotly
```

### **Paso 5: Configuración Básica**
```bash
# Crear archivo de configuración (opcional para IA)
echo "OPENAI_API_KEY=tu-clave-aqui" > .env

# Verificar estructura de archivos
ls -la  # Linux/macOS
dir     # Windows

# Verificar archivos clave:
# ✅ streamlit_app.py (punto de entrada)
# ✅ pages/ (interfaz multi-página)
# ✅ shared/ (lógica de negocio)
# ✅ requirements.txt (dependencias)
# ✅ .streamlit/config.toml (configuración)
```

---

## ⚙️ **Configuración Avanzada**

### **Archivo `.env` (Variables de Entorno)**:
```env
# === CONFIGURACIÓN IA (OPCIONAL) ===
OPENAI_API_KEY=sk-proj-tu-clave-real-aqui
OPENAI_MODEL=gpt-4
OPENAI_MAX_TOKENS=2000
OPENAI_TEMPERATURE=0.7

# === CONFIGURACIÓN DE LA APLICACIÓN ===
STREAMLIT_PORT=8501
LOG_LEVEL=INFO
DEBUG_MODE=False

# === OPTIMIZACIÓN DE RENDIMIENTO ===
MAX_FILE_SIZE_MB=1.5
MAX_COMMENTS=200
CACHE_TTL_SECONDS=3600

# === CONFIGURACIÓN DE MEMORIA ===
MEMORY_LIMIT_MB=690
ENABLE_MEMORY_MONITORING=True
```

### **Configuración de Streamlit (`.streamlit/config.toml`)**:
```toml
[theme]
primaryColor = "#4ea4ff"          # Web3 Blue Primary
backgroundColor = "#0f1419"       # Dark Professional Base
secondaryBackgroundColor = "#18202a"  # Glass Background
textColor = "#e6edf3"            # High Contrast Text
font = "sans serif"

[server]
headless = true                   # Modo servidor
port = 8501                      # Puerto por defecto
maxUploadSize = 50               # 50MB límite total
enableCORS = true                # Permitir CORS
enableXsrfProtection = false     # Desactivar XSRF para desarrollo

[browser]
gatherUsageStats = false         # No enviar estadísticas
serverAddress = "0.0.0.0"       # Escuchar en todas las interfaces

[global]
developmentMode = false          # Modo producción
suppressDeprecationWarnings = true  # Logging limpio
showWarningOnDirectExecution = false

[runner]
magicEnabled = true              # Habilitar magic commands
```

---

## 🧪 **Verificación de Instalación**

### **Test Básico de Funcionalidad**:
```bash
# 1. Ejecutar aplicación
streamlit run streamlit_app.py

# 2. Abrir navegador en: http://localhost:8501

# 3. Verificar elementos:
# ✅ Interfaz carga correctamente
# ✅ Sidebar con navegación visible
# ✅ Tema oscuro aplicado
# ✅ Efectos Web3 funcionando

# 4. Test de navegación:
# ✅ "Cargar Archivo" accesible
# ✅ "Procesar y Analizar" accesible  
# ✅ "Ver Resultados" accesible
```

### **Test de Componentes Core**:
```python
# Crear test_installation.py
import sys
import os

def test_core_modules():
    """Test de módulos principales"""
    try:
        # Test imports principales
        import streamlit as st
        import pandas as pd
        import plotly.express as px
        import numpy as np
        print("✅ Módulos principales: OK")
        
        # Test módulos del proyecto
        sys.path.append(os.path.dirname(__file__))
        from shared.business.file_processor import FileProcessor
        from shared.business.analysis_engine import analyze_sentiment_simple
        from shared.styling.theme_manager_full import ThemeManager
        print("✅ Módulos del proyecto: OK")
        
        # Test funcionalidad básica
        processor = FileProcessor()
        sentiment = analyze_sentiment_simple("Excelente servicio")
        theme_manager = ThemeManager()
        print("✅ Funcionalidad básica: OK")
        
        print("\n🎉 INSTALACIÓN VERIFICADA CORRECTAMENTE")
        return True
        
    except Exception as e:
        print(f"❌ Error en instalación: {e}")
        return False

if __name__ == "__main__":
    test_core_modules()
```

```bash
# Ejecutar test
python test_installation.py
```

### **Test de Análisis IA** (Opcional):
```python
# test_ai_integration.py
import os
from shared.business.analysis_engine import create_recommendations

def test_ai_functionality():
    """Test de funcionalidad IA si está configurada"""
    if not os.getenv('OPENAI_API_KEY'):
        print("⚠️  OpenAI no configurado - Solo análisis rápido disponible")
        return True
        
    try:
        # Test datos de ejemplo
        test_results = {
            'sentiment_percentages': {'positivo': 60.0, 'neutral': 25.0, 'negativo': 15.0},
            'theme_counts': {'velocidad': 5, 'servicio': 3},
            'insights': {'customer_satisfaction_index': 75.0, 'emotional_intensity': 'alto'}
        }
        
        # Test recomendaciones IA
        recommendations = create_recommendations(test_results, enhanced_ai=True)
        print(f"✅ IA funcionando: {len(recommendations)} recomendaciones generadas")
        return True
        
    except Exception as e:
        print(f"❌ Error IA: {e}")
        return False

if __name__ == "__main__":
    test_ai_functionality()
```

---

## 🐳 **Instalación con Docker** (Opcional)

### **Método Docker Compose** (Recomendado):
```yaml
# docker-compose.yml
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

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copiar y instalar requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY . .

# Exponer puerto
EXPOSE 8501

# Comando de inicio
CMD ["streamlit", "run", "streamlit_app.py", "--server.address", "0.0.0.0"]
```

```bash
# Construcción y ejecución
docker-compose up --build -d

# Verificar funcionamiento
docker logs comment-analyzer_comment-analyzer_1
```

---

## 🔧 **Configuración de Desarrollo**

### **Herramientas de Desarrollo** (Opcional):
```bash
# Instalar herramientas adicionales
pip install black flake8 pytest jupyter

# Configurar pre-commit hooks
pip install pre-commit
pre-commit install
```

### **Variables de Entorno para Desarrollo**:
```env
# .env.development
DEBUG_MODE=True
LOG_LEVEL=DEBUG
STREAMLIT_PORT=8502
RELOAD_ON_CHANGE=True
SHOW_WARNINGS=True
```

### **Estructura de Testing**:
```bash
# Crear estructura de tests
mkdir tests
cd tests

# Tests básicos
touch test_file_processor.py
touch test_analysis_engine.py  
touch test_ui_components.py
touch test_integration.py
```

---

## ⚠️ **Solución de Problemas de Instalación**

### **Errores Comunes y Soluciones**:

#### **Python No Encontrado**:
```bash
# Error: 'python' is not recognized as an internal or external command
# Solución Windows:
# 1. Reinstalar Python con "Add to PATH" marcado
# 2. O usar python.exe directamente desde ruta de instalación

# Solución macOS/Linux:
which python3  # Verificar ruta
alias python=python3  # Crear alias temporal
```

#### **Problemas con Pip**:
```bash
# Error: pip no funciona
# Solución:
python -m ensurepip --upgrade
python -m pip install --upgrade pip

# Error: Permission denied
# Solución Linux/macOS:
pip install --user -r requirements.txt
```

#### **Dependencias Conflictivas**:
```bash
# Error: Dependency conflict
# Solución:
pip install --force-reinstall -r requirements.txt

# O recrear entorno virtual:
deactivate
rm -rf comment_analyzer_env
python -m venv comment_analyzer_env
source comment_analyzer_env/bin/activate  # Linux/macOS
pip install -r requirements.txt
```

#### **Streamlit No Inicia**:
```bash
# Error: Address already in use
# Solución:
streamlit run streamlit_app.py --server.port 8502

# Error: ModuleNotFoundError
# Solución:
export PYTHONPATH="${PYTHONPATH}:$(pwd)"  # Linux/macOS
set PYTHONPATH=%PYTHONPATH%;%cd%          # Windows
```

#### **Problemas de Memoria**:
```bash
# Error: Out of memory
# Solución:
export STREAMLIT_SERVER_MAX_UPLOAD_SIZE=50  # MB
export STREAMLIT_SERVER_MAX_MESSAGE_SIZE=50  # MB
```

---

## 📊 **Verificación de Rendimiento**

### **Test de Carga**:
```python
# performance_test.py
import time
import pandas as pd
from shared.business.file_processor import FileProcessor

def performance_test():
    """Test de rendimiento básico"""
    # Crear datos de prueba
    test_data = pd.DataFrame({
        'Comentario Final': [
            'Excelente servicio, muy rápido',
            'La conexión se corta frecuentemente',
            'Buena atención al cliente'
        ] * 50  # 150 comentarios total
    })
    
    # Guardar archivo temporal
    test_data.to_excel('test_performance.xlsx', index=False)
    
    # Test procesamiento
    processor = FileProcessor()
    start_time = time.time()
    
    try:
        with open('test_performance.xlsx', 'rb') as f:
            results = processor.process_uploaded_file(f, use_ai_insights=False)
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        print(f"✅ Test de rendimiento:")
        print(f"   📊 Comentarios procesados: {results['total']}")
        print(f"   ⏱️  Tiempo total: {processing_time:.2f}s")
        print(f"   🚀 Velocidad: {results['total']/processing_time:.1f} comentarios/s")
        
        # Limpiar archivo temporal
        os.remove('test_performance.xlsx')
        
        return processing_time < 30  # Debe procesar en <30s
        
    except Exception as e:
        print(f"❌ Error en test de rendimiento: {e}")
        return False

if __name__ == "__main__":
    performance_test()
```

---

## 🎯 **Configuración para Producción**

### **Optimizaciones de Producción**:
```toml
# .streamlit/config.toml (Producción)
[server]
headless = true
enableCORS = false
enableXsrfProtection = true
maxUploadSize = 2
port = 8501

[global]
developmentMode = false
suppressDeprecationWarnings = true
disableWatchdogWarning = true
```

### **Variables de Entorno Producción**:
```env
# .env.production
APP_ENV=production
LOG_LEVEL=INFO
DEBUG_MODE=False
CACHE_TTL_SECONDS=7200
ENABLE_METRICS=True
SECURE_MODE=True
```

### **Servicio Systemd** (Linux):
```ini
# /etc/systemd/system/comment-analyzer.service
[Unit]
Description=Comment Analyzer Streamlit App
After=network.target

[Service]
Type=simple
User=appuser
WorkingDirectory=/opt/comment-analyzer
Environment=PATH=/opt/comment-analyzer/venv/bin
ExecStart=/opt/comment-analyzer/venv/bin/streamlit run streamlit_app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Activar servicio
sudo systemctl enable comment-analyzer
sudo systemctl start comment-analyzer
sudo systemctl status comment-analyzer
```

---

## ✅ **Checklist Final de Instalación**

### **Verificación Completa**:
- [ ] **Python 3.9+ instalado** y funcional
- [ ] **Dependencias instaladas** sin errores
- [ ] **Streamlit ejecutándose** en http://localhost:8501
- [ ] **Interfaz cargando** con tema oscuro Web3
- [ ] **Navegación funcionando** entre las 3 páginas
- [ ] **Carga de archivos** operativa
- [ ] **Análisis rápido** procesando correctamente
- [ ] **Exportación Excel** generando reportes
- [ ] **Memoria optimizada** para archivos <1.5MB
- [ ] **OpenAI configurado** (opcional, para análisis IA)

### **Configuraciones Opcionales Completadas**:
- [ ] **Variables de entorno** configuradas
- [ ] **Docker setup** (si aplica)
- [ ] **Tests automatizados** funcionando
- [ ] **Monitoreo** habilitado
- [ ] **Logging** configurado
- [ ] **Backup/restore** procedimientos documentados

---

## 📞 **Soporte Post-Instalación**

### **Recursos de Ayuda**:
- **Documentación**: `/docs` folder con guías completas
- **Logs**: Streamlit console output para debugging
- **Tests**: Scripts de verificación incluidos
- **Ejemplos**: Archivos de datos de prueba

### **Comandos de Diagnóstico**:
```bash
# Verificar estado de la aplicación
streamlit doctor

# Ver logs detallados
streamlit run streamlit_app.py --logger.level debug

# Test conexión red
curl http://localhost:8501/_stcore/health

# Verificar memoria
python -c "import psutil; print(f'RAM disponible: {psutil.virtual_memory().available/1024/1024:.0f}MB')"
```

---

**Instalación documentada**: 30 de Agosto, 2025  
**Versión compatible**: Python 3.9+ / Streamlit 1.28+  
**Sistema**: Comment Analyzer v3.0 Multi-página  
**Estado**: Guía completa para instalación en producción