# Guía de Instalación - Analizador de Comentarios IA

## Requisitos del Sistema

### Requisitos de Hardware
- **RAM**: Mínimo 2GB, recomendado 4GB+
- **Almacenamiento**: 500MB libres para el sistema + espacio para archivos
- **Procesador**: Cualquier CPU moderna (Intel/AMD x64)
- **Conexión**: Internet estable para acceso a OpenAI API

### Requisitos de Software
- **Python**: Versión 3.9 a 3.13 (recomendado 3.12)
- **Sistema Operativo**: Windows 10+, macOS 10.14+, Linux Ubuntu 18.04+
- **Navegador**: Chrome, Firefox, Safari o Edge (versiones recientes)

### Verificación de Python

```bash
# Verificar versión de Python
python --version
# Debe mostrar: Python 3.9.x a 3.13.x

# Si usas Python 3 específicamente
python3 --version
```

## 📋 Instalación Paso a Paso

### Método 1: Instalación Estándar (Recomendado)

#### 1. Descargar el Proyecto
```bash
# Opción A: Desde repositorio Git
git clone [URL_DEL_REPOSITORIO]
cd Comment-Analizer

# Opción B: Descargar ZIP y extraer
# Descargar archivo ZIP del proyecto
# Extraer y navegar a la carpeta
cd Comment-Analizer
```

#### 2. Crear Entorno Virtual (Recomendado)
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate

# En macOS/Linux:
source venv/bin/activate

# Verificar activación (debe mostrar (venv) al inicio)
```

#### 3. Instalar Dependencias
```bash
# Actualizar pip
pip install --upgrade pip

# Instalar dependencias del proyecto
pip install -r requirements.txt

# Verificar instalación crítica
pip list | grep streamlit
pip list | grep openai
```

#### 4. Configurar API de OpenAI

**Opción A: Archivo .env (Recomendado)**
```bash
# Crear archivo .env en la raíz del proyecto
echo "OPENAI_API_KEY=tu-clave-api-aqui" > .env

# En Windows usar:
echo OPENAI_API_KEY=tu-clave-api-aqui > .env
```

**Opción B: Variable de Entorno del Sistema**
```bash
# Windows (Command Prompt)
set OPENAI_API_KEY=tu-clave-api-aqui

# Windows (PowerShell)
$env:OPENAI_API_KEY="tu-clave-api-aqui"

# macOS/Linux (Bash)
export OPENAI_API_KEY="tu-clave-api-aqui"

# Para hacerlo permanente, agregalo a tu .bashrc o .zshrc:
echo 'export OPENAI_API_KEY="tu-clave-api-aqui"' >> ~/.bashrc
```

#### 5. Ejecutar la Aplicación
```bash
# Ejecutar aplicación
streamlit run streamlit_app.py

# La aplicación se abrirá automáticamente en:
# http://localhost:8501
```

### Método 2: Instalación con Docker

#### Requisitos Adicionales
- Docker Desktop instalado y ejecutándose
- 4GB RAM disponible para containers

#### 1. Construir Imagen Docker
```bash
# Clonar proyecto
git clone [URL_DEL_REPOSITORIO]
cd Comment-Analizer

# Construir imagen
docker build -t comment-analyzer:latest .
```

#### 2. Ejecutar con Docker
```bash
# Ejecutar container con variable de entorno
docker run -p 8501:8501 -e OPENAI_API_KEY=tu-clave-api-aqui comment-analyzer:latest

# O usando archivo .env
docker run -p 8501:8501 --env-file .env comment-analyzer:latest
```

#### 3. Docker Compose (Recomendado)
```bash
# Crear archivo .env con tu API key
echo "OPENAI_API_KEY=tu-clave-api-aqui" > .env

# Ejecutar con docker-compose
docker-compose up -d

# Ver logs
docker-compose logs -f
```

## 🔧 Configuración Avanzada

### Variables de Entorno Completas

Crear archivo `.env` con todas las configuraciones:

```env
# API de OpenAI (OBLIGATORIO)
OPENAI_API_KEY=sk-proj-tu-clave-openai-aqui
OPENAI_MODEL=gpt-4
OPENAI_MAX_TOKENS=4000
OPENAI_TEMPERATURE=0.7

# Configuración del Sistema
LOG_LEVEL=INFO
MAX_FILE_SIZE_MB=5.0
MAX_COMMENTS=2000

# Configuración Streamlit
STREAMLIT_PORT=8501
STREAMLIT_HOST=localhost
```

### Configuración de Streamlit

#### Archivo `.streamlit/config.toml`
```toml
[theme]
primaryColor = "#8B5CF6"
backgroundColor = "#0f1419"
secondaryBackgroundColor = "#1c2128"
textColor = "#e6edf3"

[server]
port = 8501
address = "localhost"
maxUploadSize = 50
enableCORS = false

[browser]
gatherUsageStats = false
```

#### Archivo `.streamlit/secrets.toml` (Para Streamlit Cloud)
```toml
OPENAI_API_KEY = "sk-proj-tu-clave-openai-aqui"
OPENAI_MODEL = "gpt-4"
LOG_LEVEL = "INFO"
```

## 🌐 Despliegue en Streamlit Cloud

### 1. Preparar Repositorio
```bash
# Asegurar que tienes estos archivos:
# - requirements.txt
# - streamlit_app.py
# - .streamlit/secrets.toml (opcional)

# Subir a GitHub
git add .
git commit -m "Preparar para Streamlit Cloud"
git push origin main
```

### 2. Configurar en Streamlit Cloud
1. Ve a [share.streamlit.io](https://share.streamlit.io)
2. Conecta tu cuenta de GitHub
3. Selecciona tu repositorio
4. Main branch: `main`
5. Main file path: `streamlit_app.py`

### 3. Configurar Secrets
En Streamlit Cloud, ve a Settings > Secrets y agrega:
```toml
OPENAI_API_KEY = "sk-proj-tu-clave-openai-aqui"
```

### 4. Deploy Automático
- Streamlit Cloud deployará automáticamente
- La aplicación estará disponible en: `https://tu-usuario-comment-analyzer-streamlit-app-hash.streamlit.app`

## 🧪 Verificación de Instalación

### Test Básico de Funcionamiento

#### 1. Verificar Importaciones
```bash
python -c "import streamlit as st; import openai; import pandas as pd; print('✅ Importaciones OK')"
```

#### 2. Test de Conectividad OpenAI
```bash
python -c "
import openai
import os
from dotenv import load_dotenv
load_dotenv()

client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
response = client.models.list()
print('✅ Conexión OpenAI OK')
"
```

#### 3. Test de Aplicación
```bash
# En una terminal separada
streamlit run streamlit_app.py

# Verificar que:
# 1. Se abre el navegador automáticamente
# 2. Se muestra la página principal sin errores
# 3. Se puede navegar a la página "Subir"
```

#### 4. Test Completo con Archivo de Ejemplo

Crear archivo `test_data.csv`:
```csv
Comentario,Fecha,Calificacion
"Excelente servicio de internet",01/01/2025,9
"Muy lento en horarios pico",02/01/2025,3
"Atención al cliente profesional",03/01/2025,8
```

Luego:
1. Abrir aplicación
2. Ir a página "Subir"
3. Cargar archivo `test_data.csv`
4. Iniciar análisis
5. Verificar que se generen resultados

## 🔍 Solución de Problemas de Instalación

### Error: "Command 'python' not found"

**Problema**: Python no está instalado o no está en PATH

**Soluciones**:
```bash
# Verificar si Python está instalado
which python3
which python

# En Windows, usar Python Launcher
py --version

# Reinstalar Python desde python.org
# Asegurar marcar "Add Python to PATH"
```

### Error: "ModuleNotFoundError: No module named 'streamlit'"

**Problema**: Dependencias no instaladas correctamente

**Soluciones**:
```bash
# Verificar entorno virtual activado
which pip
# Debe mostrar ruta con venv/

# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall

# Si persiste, crear nuevo entorno virtual
deactivate
rm -rf venv/
python -m venv venv
source venv/bin/activate  # o venv\Scripts\activate en Windows
pip install -r requirements.txt
```

### Error: "OpenAI API key es requerida"

**Problema**: API key no configurada correctamente

**Soluciones**:
```bash
# Verificar archivo .env existe
ls -la .env

# Verificar contenido del archivo .env
cat .env
# Debe mostrar: OPENAI_API_KEY=sk-proj-...

# Verificar variable de entorno se carga
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('OPENAI_API_KEY')[:20] + '...')"
```

### Error: "Permission denied" en macOS/Linux

**Problema**: Permisos de archivos

**Soluciones**:
```bash
# Dar permisos de ejecución
chmod +x streamlit_app.py

# Si es problema de instalación de paquetes
pip install --user -r requirements.txt
```

### Error: Puerto 8501 ya en uso

**Problema**: Otra aplicación usando el puerto

**Soluciones**:
```bash
# Ver qué proceso usa el puerto
# macOS/Linux:
lsof -i :8501

# Windows:
netstat -ano | findstr :8501

# Terminar proceso o usar puerto diferente
streamlit run streamlit_app.py --server.port 8502
```

## 📱 Instalación en Diferentes Sistemas Operativos

### Windows 10/11

```powershell
# Instalar Python desde Microsoft Store o python.org
# Verificar instalación
python --version

# Clonar proyecto
git clone [URL_REPOSITORIO]
cd Comment-Analizer

# Crear entorno virtual
python -m venv venv
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar API key
echo OPENAI_API_KEY=tu-clave-aqui > .env

# Ejecutar
streamlit run streamlit_app.py
```

### macOS

```bash
# Instalar Python con Homebrew
brew install python@3.12

# Clonar proyecto
git clone [URL_REPOSITORIO]
cd Comment-Analizer

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar API key
echo "OPENAI_API_KEY=tu-clave-aqui" > .env

# Ejecutar
streamlit run streamlit_app.py
```

### Ubuntu/Debian Linux

```bash
# Actualizar sistema e instalar Python
sudo apt update
sudo apt install python3 python3-pip python3-venv git

# Clonar proyecto
git clone [URL_REPOSITORIO]
cd Comment-Analizer

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar API key
echo "OPENAI_API_KEY=tu-clave-aqui" > .env

# Ejecutar
streamlit run streamlit_app.py
```

## 🚀 Optimización Post-Instalación

### Configuración de Performance

#### Para análisis frecuentes (> 500 comentarios)
```env
# En archivo .env
OPENAI_MAX_TOKENS=6000
MAX_COMMENTS=2000
LOG_LEVEL=WARNING  # Menos logs para mejor performance
```

#### Para archivos grandes
```env
MAX_FILE_SIZE_MB=10.0
STREAMLIT_SERVER_MAX_UPLOAD_SIZE=50
```

### Configuración de Memoria

En `.streamlit/config.toml`:
```toml
[server]
maxUploadSize = 50
runOnSave = false
```

## ✅ Checklist Final de Instalación

- [ ] Python 3.9-3.13 instalado y verificado
- [ ] Entorno virtual creado y activado
- [ ] Dependencias instaladas sin errores
- [ ] API key de OpenAI configurada
- [ ] Aplicación se ejecuta sin errores
- [ ] Se puede cargar página principal
- [ ] Se puede navegar entre páginas
- [ ] Test con archivo CSV pequeño funciona
- [ ] Análisis IA completa correctamente
- [ ] Exportación Excel funciona
- [ ] Sin errores en consola de navegador

## 📞 Soporte de Instalación

Si tienes problemas durante la instalación:

1. **Revisa esta guía** completa paso a paso
2. **Consulta troubleshooting.md** para problemas específicos
3. **Verifica logs** en consola para errores detallados
4. **Contacta soporte técnico** con información del sistema:
   - Versión de Python
   - Sistema operativo
   - Mensaje de error completo
   - Logs de instalación

---

**Estado**: Guía probada con Python 3.12 en Windows 11, macOS Big Sur, Ubuntu 22.04  
**Última actualización**: Septiembre 2025