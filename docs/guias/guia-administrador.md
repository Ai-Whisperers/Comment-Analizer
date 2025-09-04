# Guía de Administrador - Sistema IA Personal Paraguay

## 👨‍💼 Introducción para Administradores

Esta guía está dirigida a **administradores de sistemas** y **personal técnico** responsable de configurar, deployar y mantener el **Personal Paraguay Analizador IA** en entornos empresariales.

**Versión**: 3.0.0-ia-pure  
**Arquitectura**: Clean Architecture + GPT-4 obligatorio

---

## 🔧 Responsabilidades del Administrador

### **📋 Checklist de Responsabilidades**:
- ✅ **Configuración OpenAI**: API keys, billing, límites
- ✅ **Deploy en Streamlit Cloud**: Secrets, configuración, monitoreo  
- ✅ **Monitoreo IA**: Uso tokens, performance, errores
- ✅ **Gestión Usuarios**: Acceso, training, soporte
- ✅ **Backup/Recovery**: Datos análisis, configuración
- ✅ **Seguridad**: API keys, acceso, logs

---

## 🚀 Setup Inicial Sistema IA

### **Paso 1: Preparación Cuentas**

#### **A. Cuenta OpenAI (CRÍTICO)**
1. **Crear cuenta**: platform.openai.com  
2. **Verificar billing**: Agregar método de pago válido
3. **Generar API key**: Dashboard → API Keys → Create new
4. **Configurar límites**: Usage limits → Set monthly budget ($50+ recomendado)
5. **Probar key**: Test con curl o Python antes de configurar

#### **B. Cuenta Streamlit Cloud**  
1. **Crear cuenta**: streamlit.io/cloud
2. **Conectar GitHub**: Autorizar acceso a repositorio
3. **Verificar límites**: Community vs Teams según necesidades

### **Paso 2: Configuración OpenAI Enterprise**

#### **🔐 Gestión Segura de API Keys**:
```bash
# Testing API key válida
curl -H "Authorization: Bearer sk-proj-tu-key" \
     -H "Content-Type: application/json" \
     -d '{"model": "gpt-4", "messages": [{"role": "user", "content": "test"}], "max_tokens": 5}' \
     https://api.openai.com/v1/chat/completions

# Response exitoso indica key válida
```

#### **💰 Configuración Billing**:
- **Budget mensual**: $100-500 según volumen esperado
- **Hard limits**: Configurar para evitar gastos excesivos  
- **Alertas**: Email cuando alcance 50%, 80% del budget
- **Usage tracking**: Monitor daily tokens consumption

#### **⚙️ Configuración Modelo**:
```json
{
    "model": "gpt-4",
    "max_tokens": 4000,           // Análisis comprehensivo
    "temperature": 0.7,           // Balance creatividad/precisión
    "top_p": 1.0,                // Coherencia máxima
    "frequency_penalty": 0.1      // Evitar repeticiones
}
```

---

## ☁️ Deploy en Streamlit Cloud

### **Configuración Secrets (CRÍTICO)**

#### **Método Recomendado - Interface Web**:
1. **Dashboard**: streamlit.io/cloud → tu app
2. **Settings**: ⚙️ → Advanced settings → Secrets
3. **Configurar**:
```toml
# OBLIGATORIO para sistema IA
OPENAI_API_KEY = "sk-proj-tu-api-key-empresarial"

# OPCIONAL - tuning avanzado
OPENAI_MODEL = "gpt-4"
OPENAI_MAX_TOKENS = 4000
OPENAI_TEMPERATURE = 0.7
MAX_COMMENTS = 2000
DEBUG_MODE = false
```

#### **Variables de Entorno Adicionales**:
```toml
# Performance tuning
STREAMLIT_SERVER_MAX_UPLOAD_SIZE = 50
STREAMLIT_SERVER_ENABLE_STATIC_SERVING = false

# Logging
LOG_LEVEL = "WARNING"             # Producción
STREAMLIT_LOGGER_LEVEL = "ERROR"  # Solo errores críticos
```

### **Configuración Runtime**:
```toml  
# runtime.txt (Python version)
3.12

# .streamlit/config.toml
[server]
port = 8501
enableCORS = false
maxUploadSize = 50

[theme]  
primaryColor = "#8B5CF6"         # Purple IA theme
backgroundColor = "#0f1419"      # Professional dark
textColor = "#e6edf3"           # High contrast

[logger]
level = "warning"                # Solo warnings en prod
```

---

## 📊 Monitoreo Sistema IA

### **Métricas Críticas a Monitorear**:

#### **A. OpenAI Usage**
- **Daily tokens**: Tracking automático OpenAI dashboard
- **Monthly cost**: Budget vs consumption real
- **Rate limits**: Requests per minute (RPM)
- **Model performance**: Latencia promedio GPT-4

#### **B. Streamlit Application**
- **Uptime**: % disponibilidad aplicación  
- **Response time**: Tiempo carga páginas
- **Error rate**: % análisis IA fallidos
- **Memory usage**: Consumo RAM Streamlit Cloud

#### **C. User Experience**
- **Análisis exitosos**: % completados sin error
- **File upload success**: % archivos procesados ok
- **Excel export**: % reportes generados correctamente

### **🔍 Comandos de Diagnóstico**:
```bash
# Verificar estado aplicación
curl -I https://tu-app.streamlit.app/

# Test OpenAI desde servidor
python -c "
import openai
client = openai.OpenAI(api_key='tu-key')
response = client.models.list()
print('OpenAI OK' if response.data else 'OpenAI ERROR')
"

# Test análisis completo (en local)
streamlit run streamlit_app.py &
# Navegar y probar análisis con archivo test
```

---

## 🚨 Manejo de Errores IA

### **Errores Comunes y Soluciones**:

#### **🔴 "Error de servicio IA"**
**Causa**: OpenAI API down o rate limits  
**Acción**: Verificar status.openai.com + ajustar rate limits

#### **🟡 "Análisis IA incompleto"**
**Causa**: Timeout o archivo muy grande  
**Acción**: Reducir MAX_COMMENTS o aumentar timeout

#### **🔴 "Créditos OpenAI insuficientes"**
**Causa**: Budget agotado o billing suspended  
**Acción**: Recargar créditos + verificar método de pago

### **📧 Alertas Automáticas**:
```python
# Configurar en OpenAI dashboard:
- Email alert: 80% budget monthly
- SMS alert: API errors > 10% daily  
- Slack webhook: Sistema down > 5 min
```

---

## 👥 Gestión de Usuarios

### **Tipos de Usuario**:

#### **👤 Usuario Final**  
- **Acceso**: Solo interfaz web
- **Capabilities**: Upload archivos, ver resultados IA
- **Training**: Guía básica uso sistema IA
- **Support**: Email/chat para problemas

#### **👨‍💼 Analista Business**
- **Acceso**: Interfaz + reportes Excel
- **Capabilities**: Análisis IA + interpretación insights
- **Training**: Workshop uso avanzado + interpretación IA
- **Support**: Soporte técnico prioritario

#### **👨‍💻 Desarrollador/Admin**
- **Acceso**: Código + logs + configuración
- **Capabilities**: Deploy, debug, monitoreo
- **Training**: Documentación técnica completa
- **Support**: Documentación + GitHub issues

---

## 💾 Backup y Recovery

### **Datos a Respaldar**:
```bash
# Configuración crítica
.env                          # API keys (local)
.streamlit/secrets.toml      # Secrets (si exists)
.streamlit/config.toml       # App configuration

# Reportes generados
local-reports/               # Análisis técnicos
# Nota: Análisis IA no se guarda (system stateless)
```

### **Procedimiento Recovery**:
1. **Restaurar configuración**: .env + secrets
2. **Redeploy aplicación**: Streamlit Cloud auto-rebuild
3. **Verificar OpenAI**: Test API key functionality  
4. **Test completo**: Upload archivo + análisis IA + export

---

## 📈 Optimización Performance

### **Tuning para Alto Volumen**:
```env
# Configuración para empresas grandes
MAX_COMMENTS=1500               # Balance performance/calidad
OPENAI_MAX_TOKENS=3000         # Optimizar costo
BATCH_SIZE=100                 # Si procesas múltiples archivos
CACHE_ANALYSIS_HOURS=24        # Cache resultados similares (futuro)
```

### **Monitoring Setup**:
```python
# Métricas para dashboards admin (futuro):
- analysis_duration_avg: 45s
- tokens_per_comment_avg: 25  
- success_rate: 95%+
- cost_per_analysis: $0.15 avg
```

---

## 🎯 Checklist Go-Live

### **✅ Pre-Producción**:
- [ ] OpenAI API key configurada y probada
- [ ] Billing OpenAI activo con límites apropiados
- [ ] Streamlit Cloud secrets configurados correctamente  
- [ ] Testing E2E: upload → análisis IA → export Excel
- [ ] CSS glassmorphism funcionando correctamente
- [ ] Logs configurados para monitoreo

### **✅ Post-Producción**:
- [ ] Dashboard OpenAI monitoring activo
- [ ] Alerts configuradas para budgets y errors
- [ ] Training básico usuarios completado
- [ ] Documentación actualizada distribuida
- [ ] Canal support establecido

---

## 📞 Support Escalation

### **Niveles de Soporte**:
1. **Usuario Final** → Troubleshooting guide
2. **Issues Técnicos** → Admin review logs  
3. **OpenAI Problems** → platform.openai.com/support
4. **Streamlit Issues** → docs.streamlit.io + community forum

### **Contactos Críticos**:
- **OpenAI Support**: support@openai.com (billing/API issues)
- **Streamlit Support**: Community forum + enterprise support
- **Internal escalation**: [Tu proceso interno aquí]

---

*Guía administrativa para sistema IA puro versión 3.0.0*  
*Personal Paraguay | Enterprise IA Operations | Septiembre 2025*