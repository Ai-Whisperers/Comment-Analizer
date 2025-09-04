# Deployment en Streamlit Cloud - Sistema IA Puro

## 📋 Resumen de Deployment

Esta guía cubre el deployment completo del **Analizador de Comentarios IA** en Streamlit Cloud. El sistema está optimizado para **análisis IA puro** y requiere configuración específica de OpenAI.

---

## 🔧 Prerequisitos

### **Cuentas Requeridas**
- ✅ **Cuenta GitHub** con acceso al repositorio
- ✅ **Cuenta Streamlit Cloud** (streamlit.io/cloud)  
- ✅ **Cuenta OpenAI** con API key activa
- ✅ **Créditos OpenAI** suficientes para GPT-4

### **Configuración Local de Desarrollo**
- **Python 3.12** (recomendado, soporta 3.9-3.13)
- **Git** configurado y autenticado
- **OpenAI API key** para testing local

---

## 🚀 Proceso de Deployment

### **Paso 1: Preparación del Repositorio**

#### **Verificar Archivos Críticos**
Asegúrate de que estos archivos estén en el repositorio:
```
Comment-Analizer/
├── streamlit_app.py          # ✅ Entry point
├── requirements.txt          # ✅ Dependencies v3.0.0
├── runtime.txt              # ✅ python-3.12
├── .streamlit/config.toml   # ✅ Streamlit config
├── pages/                   # ✅ 2 páginas
│   ├── 1_Página_Principal.py
│   └── 2_Subir.py
├── src/                     # ✅ Clean Architecture IA
└── static/                  # ✅ CSS glassmorphism
```

#### **Verificar Configuración**
```toml
# .streamlit/config.toml debe contener:
[server]
enableStaticServing = true  # Para CSS
maxUploadSize = 5
```

### **Paso 2: Deployment en Streamlit Cloud**

#### **Conectar Repositorio**
1. Ve a [streamlit.io/cloud](https://streamlit.io/cloud)
2. Haz clic en **"New app"**
3. Conecta tu **repositorio GitHub**
4. Selecciona el repositorio **Comment-Analizer**
5. **Main file path**: `streamlit_app.py`
6. **Branch**: `main`
7. **Python version**: `3.12` (será detectada por `runtime.txt`)

#### **Configurar Secrets**
**CRÍTICO**: Sin OpenAI API key, la app **fallará inmediatamente**.

1. En la configuración de la app, ve a **"Secrets"**
2. Agrega esta configuración:

```toml
# Streamlit Cloud Secrets Configuration
OPENAI_API_KEY = "tu-api-key-real-aqui"
OPENAI_MODEL = "gpt-4"
OPENAI_MAX_TOKENS = "12000"
OPENAI_TEMPERATURE = "0.7"

# Application Settings
APP_ENV = "production"
DEBUG_MODE = "False"
MAX_FILE_SIZE_MB = "5"
MAX_COMMENTS_PER_BATCH = "2000"

# Performance
CACHE_TTL_SECONDS = "300"
API_RATE_LIMIT_PER_MINUTE = "60"
SESSION_TIMEOUT_MINUTES = "30"

# Security
SECRET_KEY = "genera-una-clave-secreta-aleatoria"

# Language & Export
DEFAULT_LANGUAGE = "es"
ENABLE_TRANSLATION = "True"
EXCEL_MAX_ROWS = "10000"
EXPORT_COMPRESSION = "True"
LOG_LEVEL = "INFO"
```

#### **Deploy**
1. Haz clic en **"Deploy"**
2. Espera 3-5 minutos para build inicial
3. La app estará disponible en: `https://tu-app-name.streamlit.app`

---

## 🔍 Verificación Post-Deployment

### **Tests Básicos**
1. **Página principal carga**: ✅ Sin errores
2. **Estado del sistema**: ✅ "Sistema activo" + "OpenAI: Configurado"
3. **Página Subir carga**: ✅ Sin errores en consola
4. **CSS se aplica**: ✅ Botones con gradiente morado-cyan

### **Test Completo E2E**
1. **Sube archivo test** (Excel/CSV con 3-5 comentarios)
2. **Haz clic "Analizar con Inteligencia Artificial"**
3. **Espera 30-60 segundos** para análisis IA
4. **Verifica resultados**: Métricas + insights + recomendaciones IA
5. **Exporta Excel**: Descarga debe funcionar

### **Indicadores de Éxito**
```
✅ "Análisis con Inteligencia Artificial completado"
✅ Métricas muestran números correctos
✅ "Temas principales detectados por IA" con lista
✅ "Emociones identificadas por IA" con intensidades
✅ "Resumen Ejecutivo (Generado por IA)" con texto
✅ "Recomendaciones de IA" con acciones
✅ Botón "Generar Excel" funciona
✅ Descarga Excel contiene datos IA
```

---

## ⚠️ Problemas Comunes y Soluciones

### **"Error cargando nueva arquitectura"**
**Causa**: Problemas de imports en el código  
**Solución**: 
1. Verifica que todos los archivos `src/` estén en el repositorio
2. Re-deploy desde Streamlit Cloud
3. Contacta soporte técnico

### **"OpenAI API key es requerida"**
**Causa**: API key no configurada o inválida  
**Solución**:
1. Verifica que OPENAI_API_KEY esté en Secrets
2. Confirma que la API key sea válida en OpenAI
3. Verifica que tenga créditos disponibles

### **"Error de servicio IA"**  
**Causas posibles**:
- Rate limit de OpenAI alcanzado
- Créditos OpenAI agotados
- Problemas de conectividad

**Soluciones**:
1. Espera unos minutos y reintenta  
2. Verifica créditos en cuenta OpenAI
3. Contacta administrador si persiste

### **"CSS no se carga correctamente"**
**Causa**: Problemas con static file serving  
**Solución**:
1. Verifica `.streamlit/config.toml` tiene `enableStaticServing = true`
2. Re-deploy la aplicación
3. Clear browser cache

### **Archivo muy grande (>5MB)**
**Soluciones**:
1. **Reduce columnas**: Mantén solo comentarios + NPS/Nota
2. **Filtra filas**: Mantén solo comentarios con texto
3. **Comprime archivo**: Guarda como Excel comprimido
4. **Divide análisis**: Procesa en lotes más pequeños

---

## 📊 Monitoreo y Uso

### **Métricas de Uso**
En la página principal puedes monitorear:
- **Comentarios procesados**: Total acumulado en sesión
- **Sistema IA**: Estado de disponibilidad
- **Versión**: 3.0.0-ia-pure activa

### **Costos Estimados**
**GPT-4 cuesta aproximadamente**:
- **100 comentarios**: ~$0.50-$1.00 USD
- **500 comentarios**: ~$2.50-$5.00 USD  
- **1000 comentarios**: ~$5.00-$10.00 USD

*Costos varían según longitud y complejidad de comentarios*

### **Límites del Sistema**
- **Máximo por archivo**: 5MB (~2000-5000 comentarios típicamente)
- **Rate limit**: 60 análisis por minuto
- **Timeout**: 30 minutos por sesión
- **Cache**: 5 minutos para archivos idénticos

---

## 🎯 Mejores Prácticas

### **Para Administradores**
1. **Monitorea créditos OpenAI** regularmente
2. **Configura alertas** de uso excesivo
3. **Backup periódico** de configuración de secrets
4. **Actualiza API keys** según política de seguridad

### **Para Usuarios Finales**  
1. **Prepara datos limpios** antes de subir
2. **Usa archivos representativos** para mejor análisis
3. **Revisa insights de IA** antes de tomar decisiones
4. **Combina recomendaciones** para planes de acción

### **Para Desarrolladores**
1. **Monitorea logs** de Streamlit Cloud
2. **Optimiza prompts** de IA según feedback
3. **Actualiza DTOs** si cambian respuestas IA
4. **Testing regular** con datos reales

---

## 🔐 Seguridad y Compliance

### **Datos del Cliente**
- **Procesamiento temporal**: Comentarios no se almacenan permanentemente
- **IA analysis only**: OpenAI procesa según sus términos de servicio
- **Sin backup automático**: Datos se eliminan al terminar sesión

### **API Key Security**
- **Nunca compartir** API keys
- **Rotar regularmente** según política
- **Monitorear uso** para detectar acceso no autorizado
- **Usar secrets manager** de Streamlit Cloud

### **Compliance**
- **Revisa términos** de servicio OpenAI para tu industria
- **Considera regulaciones** locales sobre IA  
- **Documenta uso** de IA en procesos de negocio

---

## 📞 Contacto y Soporte

### **Soporte Técnico**
- **Problemas de deployment**: Revisar logs de Streamlit Cloud
- **Errores de aplicación**: Contactar equipo de desarrollo
- **Problemas OpenAI**: Verificar cuenta y créditos

### **Feedback y Mejoras**
- **Sugerencias de funcionalidades**: Enfocadas en mejor IA integration
- **Reportes de bugs**: Con pasos para reproducir
- **Solicitudes de análisis**: Para casos de uso específicos

---

*Guía de deployment v3.0.0-ia-pure*  
*Personal Paraguay | Sistema IA Puro | 2025*