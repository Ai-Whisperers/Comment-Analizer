# Guía de Solución de Problemas - Analizador de Comentarios IA

## Problemas de Instalación y Configuración

### Error: "Python no encontrado" o "Command not found: python"

**Síntomas**:
```bash
'python' is not recognized as an internal or external command
bash: python: command not found
```

**Causas**:
- Python no está instalado
- Python no está en el PATH del sistema
- Se instaló Python pero no se reinició la terminal

**Soluciones**:

#### Windows:
```bash
# Verificar instalación
py --version
python3 --version

# Si no funciona, descargar desde python.org
# Asegurar marcar "Add Python to PATH" durante instalación

# Añadir manualmente al PATH si es necesario:
# Buscar "Environment Variables" en Windows
# Agregar: C:\Python312\ y C:\Python312\Scripts\
```

#### macOS:
```bash
# Instalar con Homebrew
brew install python@3.12

# O verificar si está instalado
python3 --version
which python3

# Crear alias si es necesario
echo "alias python=python3" >> ~/.zshrc
source ~/.zshrc
```

#### Linux (Ubuntu/Debian):
```bash
# Instalar Python
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Verificar instalación
python3 --version
which python3
```

---

### Error: "ModuleNotFoundError: No module named 'streamlit'"

**Síntomas**:
```
ModuleNotFoundError: No module named 'streamlit'
ModuleNotFoundError: No module named 'openai'
```

**Causas**:
- Dependencias no instaladas
- Entorno virtual no activado
- Instalación incompleta de requirements.txt

**Soluciones**:

#### 1. Verificar Entorno Virtual:
```bash
# Verificar si el entorno virtual está activado
# Debe mostrar (venv) al inicio del prompt
which pip
# Debe mostrar ruta que incluye venv/

# Si no está activado:
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate
```

#### 2. Reinstalar Dependencias:
```bash
# Actualizar pip primero
pip install --upgrade pip

# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall

# Si persiste, instalar individualmente:
pip install streamlit>=1.39.0
pip install openai>=1.50.0
pip install pandas>=2.1.0
```

#### 3. Crear Nuevo Entorno Virtual:
```bash
# Desactivar entorno actual
deactivate

# Eliminar entorno corrupto
rm -rf venv/  # Linux/macOS
rmdir /s venv\  # Windows

# Crear nuevo entorno
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt
```

---

## Problemas de API de OpenAI

### Error: "OpenAI API key es requerida para esta aplicación IA"

**Síntomas**:
- Mensaje de error en la interfaz web
- Aplicación no puede inicializar análisis IA

**Causas**:
- API key no configurada
- Archivo .env no existe o tiene formato incorrecto
- Variable de entorno no se está cargando

**Soluciones**:

#### 1. Verificar Archivo .env:
```bash
# Verificar que existe el archivo
ls -la .env  # Linux/macOS
dir .env     # Windows

# Verificar contenido
cat .env     # Linux/macOS
type .env    # Windows

# Debe contener:
OPENAI_API_KEY=sk-proj-tu-clave-aqui
```

#### 2. Crear/Corregir Archivo .env:
```bash
# Crear archivo .env
echo "OPENAI_API_KEY=sk-proj-tu-clave-aqui" > .env

# Verificar formato correcto (sin espacios extra)
# Correcto: OPENAI_API_KEY=sk-proj-abc123
# Incorrecto: OPENAI_API_KEY = sk-proj-abc123
```

#### 3. Verificar Carga de Variables:
```python
# Test en Python
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
key = os.getenv('OPENAI_API_KEY')
if key:
    print(f'✅ API Key cargada: {key[:20]}...')
else:
    print('❌ API Key no encontrada')
"
```

---

### Error: "Error de servicio IA" o "OpenAI API Error"

**Síntomas**:
```
Error de servicio IA: Authentication Error
Error de servicio IA: Rate limit exceeded
Error de servicio IA: Service unavailable
```

**Causas**:
- API key inválida o expirada
- Créditos de OpenAI agotados
- Rate limits excedidos
- Problemas de conectividad

**Soluciones**:

#### 1. Verificar API Key:
```python
# Test de conectividad OpenAI
python -c "
import openai
import os
from dotenv import load_dotenv

load_dotenv()
client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

try:
    models = client.models.list()
    print('✅ Conexión OpenAI exitosa')
except openai.AuthenticationError:
    print('❌ API key inválida')
except openai.PermissionDeniedError:
    print('❌ Sin permisos para el modelo')
except Exception as e:
    print(f'❌ Error: {str(e)}')
"
```

#### 2. Verificar Créditos y Límites:
- Visita [platform.openai.com/usage](https://platform.openai.com/usage)
- Verifica saldo disponible
- Revisa límites de uso del modelo

#### 3. Manejar Rate Limits:
```env
# En .env, ajustar timeouts
OPENAI_TIMEOUT=600
OPENAI_MAX_RETRIES=5
OPENAI_RETRY_DELAY=5
```

---

## Problemas de Archivos y Datos

### Error: "Archivo muy grande" o "File size exceeds limit"

**Síntomas**:
- Error al cargar archivo Excel/CSV
- Upload se interrumpe

**Causas**:
- Archivo excede límite de 5MB
- Streamlit tiene límite de upload configurado

**Soluciones**:

#### 1. Reducir Tamaño de Archivo:
```bash
# Verificar tamaño del archivo
ls -lh tu_archivo.xlsx  # Linux/macOS
dir tu_archivo.xlsx     # Windows

# Si es > 5MB, opciones:
# - Dividir en archivos más pequeños
# - Eliminar columnas innecesarias
# - Comprimir archivo Excel
```

#### 2. Aumentar Límite (Solo Administradores):
```env
# En .env
MAX_FILE_SIZE_MB=10.0
```

```toml
# En .streamlit/config.toml
[server]
maxUploadSize = 50
```

#### 3. Optimizar Datos:
- Eliminar filas vacías
- Usar formato CSV en lugar de Excel
- Comprimir archivo antes de subir

---

### Error: "No se detectaron comentarios en el archivo"

**Síntomas**:
- Archivo se carga pero no encuentra comentarios
- Análisis no puede comenzar

**Causas**:
- Nombre de columna no reconocido
- Datos en formato incorrecto
- Celdas combinadas o formato complejo

**Soluciones**:

#### 1. Verificar Nombres de Columna:
```
Nombres reconocidos automáticamente:
✅ "Comentario", "comentario", "COMENTARIO"
✅ "Comment", "comment", "COMMENT"  
✅ "Feedback", "feedback", "FEEDBACK"
✅ "Observacion", "observacion", "OBSERVACION"
✅ "Texto", "texto", "TEXTO"

❌ Nombres no reconocidos: "Opinion", "Descripcion", "Detalle"
```

#### 2. Renombrar Columnas:
- Abrir archivo en Excel
- Renombrar primera columna a "Comentario"
- Guardar archivo

#### 3. Formato de Datos Correcto:
```csv
Comentario,Fecha,Calificacion
"El servicio es excelente",01/01/2024,9
"Muy lento el internet",02/01/2024,3
```

---

## Problemas de Performance

### Error: "Tiempo de espera agotado" o "Analysis timeout"

**Síntomas**:
- Análisis se detiene a medio camino
- Mensaje de timeout en la interfaz
- Barra de progreso se congela

**Causas**:
- Archivo muy grande (> 1000 comentarios)
- Conexión lenta a OpenAI
- Timeout configurado muy bajo

**Soluciones**:

#### 1. Dividir Archivo en Lotes:
```bash
# Dividir archivo grande en archivos más pequeños
# Máximo 500-1000 comentarios por archivo
```

#### 2. Aumentar Timeout:
```env
# En .env
OPENAI_TIMEOUT=900  # 15 minutos
PROCESSING_TIMEOUT=1200  # 20 minutos
```

#### 3. Optimizar Configuración:
```env
# Reducir tokens para análisis más rápido
OPENAI_MAX_TOKENS=3000

# Usar modelo más rápido (menos preciso)
OPENAI_MODEL=gpt-3.5-turbo
```

---

### Error: "Memoria insuficiente" o "Out of memory"

**Síntomas**:
- Aplicación se cierra inesperadamente
- Error de memoria en logs
- Sistema lento o no responde

**Causas**:
- Archivo muy grande en memoria
- Análisis de muchos comentarios simultáneamente
- Fuga de memoria en procesamiento

**Soluciones**:

#### 1. Reducir Carga:
```env
# Limitar comentarios por análisis
MAX_COMMENTS=1000
BATCH_SIZE=50
```

#### 2. Limpiar Memoria:
```bash
# Reiniciar aplicación
# Ctrl+C para detener
# Ejecutar nuevamente: streamlit run streamlit_app.py
```

#### 3. Optimizar Sistema:
- Cerrar otras aplicaciones
- Aumentar memoria virtual/swap
- Usar archivos más pequeños

---

## Problemas de Interfaz Web

### Error: "Puerto 8501 ya en uso"

**Síntomas**:
```
OSError: [Errno 48] Address already in use
StreamlitAPIException: Port 8501 is already in use
```

**Causas**:
- Otra instancia de Streamlit ejecutándose
- Otro servicio usando el puerto 8501

**Soluciones**:

#### 1. Terminar Proceso Existente:
```bash
# Linux/macOS:
lsof -i :8501
kill -9 [PID]

# Windows:
netstat -ano | findstr :8501
taskkill /PID [PID] /F
```

#### 2. Usar Puerto Diferente:
```bash
streamlit run streamlit_app.py --server.port 8502
```

#### 3. Configurar Puerto en .env:
```env
STREAMLIT_PORT=8502
```

---

### Problema: "Página en blanco" o "Loading indefinido"

**Síntomas**:
- Página carga pero se queda en blanco
- Spinner de carga gira indefinidamente
- No aparece contenido

**Causas**:
- Error de JavaScript en navegador
- CSS no se carga correctamente
- Problema con componentes Streamlit

**Soluciones**:

#### 1. Limpiar Cache del Navegador:
```bash
# En el navegador:
# Chrome: Ctrl+Shift+R (Windows/Linux), Cmd+Shift+R (macOS)
# Firefox: Ctrl+F5 (Windows/Linux), Cmd+Shift+R (macOS)

# O limpiar cache manualmente:
# Chrome: Settings > Privacy > Clear browsing data
```

#### 2. Verificar Console del Navegador:
```bash
# Abrir Developer Tools: F12
# Ir a Console tab
# Buscar errores en rojo
# Reportar errores específicos
```

#### 3. Probar Navegador Diferente:
- Chrome (recomendado)
- Firefox
- Safari
- Edge

---

## Problemas de Exportación

### Error: "No se puede generar reporte Excel"

**Síntomas**:
- Botón de descarga no funciona
- Error al generar archivo Excel
- Archivo descargado está corrupto

**Causas**:
- Problema con librería openpyxl
- Datos muy grandes para Excel
- Permisos de escritura

**Soluciones**:

#### 1. Verificar Librerías:
```bash
pip install --upgrade openpyxl xlsxwriter
```

#### 2. Verificar Permisos:
```bash
# Linux/macOS:
ls -la local-reports/
chmod 755 local-reports/

# Windows:
# Verificar que la carpeta local-reports tenga permisos de escritura
```

#### 3. Limpiar Datos:
- Reducir número de comentarios
- Eliminar caracteres especiales
- Usar formato CSV como alternativa

---

## Diagnóstico General

### Script de Diagnóstico Completo

```python
# diagnostic.py - Guardar como archivo y ejecutar
import sys
import os
import streamlit as st
import openai
import pandas as pd
from dotenv import load_dotenv

def ejecutar_diagnostico():
    print("🔍 DIAGNÓSTICO COMPLETO DEL SISTEMA")
    print("=" * 50)
    
    # 1. Python y dependencias
    print(f"✓ Python: {sys.version.split()[0]}")
    
    try:
        print(f"✓ Streamlit: {st.__version__}")
    except:
        print("❌ Streamlit no instalado")
    
    try:
        print(f"✓ OpenAI: {openai.__version__}")
    except:
        print("❌ OpenAI no instalado")
        
    try:
        print(f"✓ Pandas: {pd.__version__}")
    except:
        print("❌ Pandas no instalado")
    
    # 2. Configuración
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    
    if api_key:
        print(f"✓ API Key: Configurada ({api_key[:20]}...)")
        
        # Test conexión OpenAI
        try:
            client = openai.OpenAI(api_key=api_key)
            models = client.models.list()
            print("✓ Conexión OpenAI: Exitosa")
        except Exception as e:
            print(f"❌ Conexión OpenAI: Error - {str(e)}")
    else:
        print("❌ API Key: No configurada")
    
    # 3. Archivos de configuración
    archivos_config = ['.env', '.streamlit/config.toml', 'requirements.txt']
    for archivo in archivos_config:
        if os.path.exists(archivo):
            print(f"✓ {archivo}: Existe")
        else:
            print(f"❌ {archivo}: No encontrado")
    
    # 4. Permisos y directorios
    dirs_necesarios = ['local-reports', 'docs', 'src']
    for dir_name in dirs_necesarios:
        if os.path.exists(dir_name):
            print(f"✓ {dir_name}/: Existe")
        else:
            print(f"⚠️  {dir_name}/: No encontrado")
    
    print("\n" + "=" * 50)
    print("✅ Diagnóstico completado")
    print("\nSi hay errores (❌), revisar la sección correspondiente")
    print("en troubleshooting.md para soluciones específicas.")

if __name__ == "__main__":
    ejecutar_diagnostico()
```

### Comando Rápido de Diagnóstico

```bash
# Ejecutar diagnóstico
python -c "
import subprocess
import sys

def verificar_comando(cmd):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        return result.returncode == 0
    except:
        return False

print('🔍 DIAGNÓSTICO RÁPIDO')
print('=' * 30)

# Verificaciones básicas
checks = [
    ('python --version', 'Python'),
    ('pip --version', 'Pip'),
    ('streamlit --version', 'Streamlit'),
]

for cmd, name in checks:
    if verificar_comando(cmd):
        print(f'✅ {name}: OK')
    else:
        print(f'❌ {name}: Error')

print('\n✅ Diagnóstico completado')
"
```

---

## Logs y Debugging

### Habilitar Logs Detallados

```env
# En .env para debugging
LOG_LEVEL=DEBUG
ENABLE_OPENAI_LOGGING=true
ENABLE_PERFORMANCE_LOGGING=true
```

### Ubicación de Logs

```bash
# Logs de la aplicación
tail -f app.log  # Linux/macOS
type app.log     # Windows

# Logs de Streamlit
~/.streamlit/logs/  # Linux/macOS
%USERPROFILE%\.streamlit\logs\  # Windows
```

### Debugging en Desarrollo

```bash
# Ejecutar con debugging
streamlit run streamlit_app.py --logger.level debug

# Ver todos los logs en tiempo real
streamlit run streamlit_app.py --logger.enableCORS false --logger.level debug
```

---

## Contacto y Soporte

### Información para Reporte de Bugs

Cuando reportes un problema, incluye:

1. **Información del Sistema**:
   ```bash
   python --version
   pip list | grep -E "(streamlit|openai|pandas)"
   ```

2. **Logs de Error**:
   - Screenshots del error
   - Logs completos (no solo el mensaje final)
   - Pasos exactos para reproducir

3. **Configuración**:
   - Variables de entorno (SIN API key)
   - Tamaño y tipo de archivo
   - Navegador utilizado

4. **Datos de Contexto**:
   - Número de comentarios
   - Tiempo cuando ocurrió el error
   - Si funcionaba antes o es primera instalación

### Recursos Adicionales

- **Documentación completa**: `/docs/README.md`
- **Guía de instalación**: `/docs/guia-instalacion.md`
- **Configuración**: `/docs/configuracion.md`

---

**Estado**: Guía probada con errores comunes identificados  
**Última actualización**: Septiembre 2025  
**Cobertura**: Windows 10/11, macOS Big Sur+, Ubuntu 20.04+