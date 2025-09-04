# Configuración Sistema IA - Personal Paraguay

## 📋 Configuración Completa del Sistema IA

Guía comprehensiva para configurar el **Personal Paraguay Analizador IA** tanto en desarrollo local como en producción Streamlit Cloud.

**Versión**: 3.0.0-ia-pure  
**Sistema**: IA-First puro sin fallbacks

---

## 🔑 Variables de Entorno Obligatorias

### **OpenAI Configuration (CRÍTICO)**
```env
# API Key OpenAI (OBLIGATORIO - Sistema no funciona sin esto)
OPENAI_API_KEY=sk-proj-tu-api-key-completa-aqui

# Configuración modelo IA
OPENAI_MODEL=gpt-4                    # Requerido para análisis avanzado
OPENAI_MAX_TOKENS=4000               # Análisis comprehensivo
OPENAI_TEMPERATURE=0.7               # Balance precisión/creatividad
```

### **Configuración Sistema (Opcional)**
```env
# Límites de procesamiento IA
MAX_FILE_SIZE_MB=5.0                 # Límite upload
MAX_COMMENTS=2000                    # Máximo comentarios por análisis
IA_TIMEOUT_SECONDS=300               # Timeout análisis IA

# Configuración aplicación
STREAMLIT_PORT=8501
LOG_LEVEL=INFO
DEBUG_MODE=false
```

---

## 🏠 Configuración Local

### **Paso 1: Crear Archivo .env**
```bash
# Crear archivo en directorio raíz
cd Comment-Analizer
touch .env

# Agregar configuración mínima
echo 'OPENAI_API_KEY=sk-proj-tu-key-aqui' >> .env
echo 'OPENAI_MODEL=gpt-4' >> .env
echo 'OPENAI_MAX_TOKENS=4000' >> .env
```

### **Paso 2: Instalar Dependencias IA**
```bash
# Instalar todas las dependencias
pip install -r requirements.txt

# Verificar dependencias críticas IA
python -c "import openai; print(f'OpenAI version: {openai.__version__}')"
python -c "import streamlit; print(f'Streamlit version: {streamlit.__version__}')"
```

### **Paso 3: Verificar Configuración**
```bash
# Test básico de OpenAI
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
key = os.getenv('OPENAI_API_KEY')
print(f'API Key configured: {bool(key and key.startswith(\"sk-\"))}')"

# Test streamlit
streamlit doctor
```

### **Paso 4: Ejecutar Sistema IA**
```bash
# Ejecutar aplicación
streamlit run streamlit_app.py

# Verificar en navegador: http://localhost:8501
# Buscar: "✅ Sistema IA Maestro: Activo y Funcional"
```

---

## ☁️ Configuración Streamlit Cloud

### **Paso 1: Configurar Secrets**

#### **Método A: Interface Web**
1. **Dashboard**: Ve a streamlit.io/cloud
2. **App Settings**: Selecciona tu app → ⚙️ Settings  
3. **Secrets**: Agrega en la sección "Secrets":

```toml
# Configuración OBLIGATORIA
OPENAI_API_KEY = "sk-proj-tu-api-key-completa"

# Configuración opcional  
OPENAI_MODEL = "gpt-4"
OPENAI_MAX_TOKENS = 4000
OPENAI_TEMPERATURE = 0.7
MAX_COMMENTS = 2000
```

#### **Método B: Archivo .streamlit/secrets.toml**
```bash
# Crear directorio y archivo (para repo privado)
mkdir -p .streamlit
cat > .streamlit/secrets.toml << 'EOF'
OPENAI_API_KEY = "sk-proj-tu-api-key"
OPENAI_MODEL = "gpt-4"  
OPENAI_MAX_TOKENS = 4000
EOF

# Agregar a .gitignore
echo ".streamlit/secrets.toml" >> .gitignore
```

### **Paso 2: Configurar App Settings**
```toml
# .streamlit/config.toml
[server]
maxUploadSize = 50                   # 50MB límite
enableCORS = false
enableStaticServing = false

[theme]
primaryColor = "#8B5CF6"             # Purple IA
backgroundColor = "#0f1419"          # Dark professional
secondaryBackgroundColor = "#1a1f2e" # Glassmorphism
textColor = "#e6edf3"               # High contrast

[logger]
level = "info"
```

### **Paso 3: Deploy y Verificación**
1. **Push**: Subir cambios a GitHub
2. **Auto-deploy**: Streamlit Cloud detecta cambios
3. **Verificar**: App debe cargar sin errores IA
4. **Test**: Página principal debe mostrar "Sistema IA Maestro: Activo"

---

## 🧪 Variables de Testing

### **Para Desarrollo/QA**
```env
# Testing con datos limitados
MAX_COMMENTS=50                      # Análisis rápido para testing
OPENAI_MAX_TOKENS=1500              # Tokens limitados para dev
DEBUG_MODE=true                      # Logs detallados

# Testing sin créditos OpenAI
MOCK_OPENAI=true                     # Solo para testing unitario
```

### **Para Producción**
```env
# Configuración optimizada producción
MAX_COMMENTS=2000                    # Capacidad completa
OPENAI_MAX_TOKENS=4000              # Análisis comprehensivo
DEBUG_MODE=false                     # Performance optimizado
LOG_LEVEL=WARNING                    # Solo errores importantes
```

---

## 🔐 Seguridad de API Keys

### **Mejores Prácticas**:
- ✅ **Nunca commits** API keys en código
- ✅ **Usar secrets.toml** en Streamlit Cloud  
- ✅ **Rotar keys** regularmente
- ✅ **Monitorear uso** de tokens OpenAI
- ✅ **Límites de rate** configurados en OpenAI

### **Verificación de Seguridad**:
```bash
# Verificar que secrets no están en código
grep -r "sk-" src/ pages/ --exclude-dir=__pycache__

# Verificar .env en .gitignore  
grep ".env" .gitignore
```

---

## 📊 Monitoreo y Métricas

### **Métricas Importantes**:
- **Uso OpenAI**: Tokens por día/semana
- **Latencia IA**: Tiempo promedio análisis  
- **Error Rate**: % análisis fallidos
- **Uptime**: Disponibilidad sistema IA

### **Logs Relevantes**:
```bash
# Logs Streamlit
streamlit run streamlit_app.py --logger.level=debug

# Logs OpenAI (en código)
logger.info(f"Análisis IA completado: {tokens_used} tokens")
logger.warning(f"IA analysis slow: {duration}s")
```

---

## ❌ Troubleshooting Configuración

### **Problem: "OpenAI API key es requerida"**
**Solución**: Verificar OPENAI_API_KEY en .env o secrets

### **Problem: "Error inicializando sistema IA"**  
**Solución**: Verificar formato API key (debe empezar con "sk-")

### **Problem: "No se pudo inicializar sistema IA maestro"**
**Solución**: Revisar créditos OpenAI y conectividad

### **Problem: CSS no carga correctamente**
**Solución**: Verificar static/styles.css y src/presentation/streamlit/

---

## 🎯 Checklist Final

### **✅ Sistema IA Listo para Producción**:
- [ ] OpenAI API key configurada y válida
- [ ] requirements.txt con openai>=1.50.0  
- [ ] .env o secrets.toml configurado
- [ ] CSS glassmorphism funcionando
- [ ] Página principal muestra "Sistema IA Maestro: Activo"
- [ ] Análisis IA completa sin errores
- [ ] Export Excel con insights IA funcional

---

*Configuración sistema IA puro versión 3.0.0*  
*Personal Paraguay | OpenAI GPT-4 + Clean Architecture | 2025*