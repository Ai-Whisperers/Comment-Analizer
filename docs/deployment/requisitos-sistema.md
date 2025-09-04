# Requisitos del Sistema - Personal Paraguay IA

## 📋 Especificaciones Técnicas del Sistema IA

Requisitos completos para ejecutar el **Personal Paraguay Analizador de Comentarios IA** tanto en desarrollo local como en producción Streamlit Cloud.

**Versión**: 3.0.0-ia-pure  
**Fecha**: Septiembre 2025

---

## 🖥️ Requisitos de Hardware

### **Desarrollo Local**:
```
CPU:    2+ cores (recomendado 4+)
RAM:    4GB mínimo (recomendado 8GB)  
Disco:  1GB espacio libre
Red:    Conexión estable para OpenAI API
```

### **Streamlit Cloud (Automático)**:
```
CPU:    Shared vCPUs
RAM:    1GB límite
Disco:  500MB espacio app
Red:    Conexión dedicada cloud
```

---

## 🐍 Requisitos de Software

### **Python y Dependencias**:
```
Python:         3.9 ≤ versión ≤ 3.13 (recomendado 3.12)
pip:            ≥ 21.0
Git:            ≥ 2.0 (para deploy)

Dependencias críticas IA:
├── streamlit ≥ 1.39.0        # Framework aplicación
├── openai ≥ 1.50.0          # ¡OBLIGATORIO para IA!
├── pandas ≥ 2.1.0           # Procesamiento datos
├── plotly ≥ 5.18.0          # Visualizaciones
├── openpyxl ≥ 3.1.5         # Export Excel
└── python-dotenv ≥ 1.0.1    # Variables entorno
```

### **Verificación Dependencias**:
```bash
# Verificar Python compatible
python --version  # Should be 3.9-3.13

# Verificar pip actualizado  
pip --version

# Test instalación dependencias críticas
pip install streamlit openai pandas plotly openpyxl

# Verificar funcionamiento
python -c "
import streamlit; print(f'Streamlit: {streamlit.__version__}')
import openai; print(f'OpenAI: {openai.__version__}')  
import pandas; print(f'Pandas: {pandas.__version__}')
"
```

---

## 🔑 Requisitos de Cuentas y Accesos

### **OpenAI Platform (OBLIGATORIO)**:
```
Cuenta:         OpenAI Developer Account
API Access:     GPT-4 habilitado
Billing:        Método de pago activo
Budget:         $20+ mensual mínimo
Rate Limits:    Tier 1+ (3 RPM mínimo)
```

#### **Cálculo Budget OpenAI**:
```
Uso estimado según volumen:

Empresa Pequeña (≤100 comentarios/día):
├── Tokens/día: ~15,000
├── Costo/día: ~$0.20
└── Budget mensual: $10-15

Empresa Mediana (≤500 comentarios/día):  
├── Tokens/día: ~75,000
├── Costo/día: ~$1.00
└── Budget mensual: $40-60

Empresa Grande (≤2000 comentarios/día):
├── Tokens/día: ~300,000  
├── Costo/día: ~$4.00
└── Budget mensual: $150-200
```

### **Streamlit Cloud**:
```
Plan:           Community (gratis) o Teams ($20/mes)
Repos:          GitHub connection required
Resources:      1GB RAM, shared CPU
Apps:           3 apps Community, unlimited Teams
```

### **GitHub**:
```
Account:        Personal o Organization
Repository:     Private recomendado para empresa
Access:         Read/Write para Streamlit Cloud
Webhooks:       Auto-deploy on push
```

---

## 🌐 Requisitos de Red

### **Conectividad Requerida**:
```
OpenAI API:     https://api.openai.com (puerto 443)
GitHub:         https://github.com (puerto 443)  
Streamlit:      https://share.streamlit.io (puerto 443)
PyPI:           https://pypi.org (para pip install)

Bandwidth:      1 Mbps mínimo
Latencia:       <500ms a OpenAI API
Firewall:       HTTPS outbound permitido
```

### **Testing Conectividad**:
```bash
# Test OpenAI API accessibility
curl -I https://api.openai.com/v1/models

# Test Streamlit Cloud
curl -I https://share.streamlit.io

# Test GitHub API  
curl -I https://api.github.com
```

---

## 🔒 Requisitos de Seguridad

### **Gestión de Secrets**:
```
API Keys:       Nunca en código fuente
.env files:     En .gitignore siempre
Secrets.toml:   Solo en Streamlit Cloud
Rotación:       API keys cada 90 días
Monitoring:     Usage patterns anomalies
```

### **Configuración .gitignore**:
```gitignore
# Secrets y configuración sensible
.env
.streamlit/secrets.toml
*.log
__pycache__/
.venv/
local-reports/sensitive/

# Archivos temporales sistema IA  
temp_analysis/
cache_openai/
*.pkl
*.cache
```

### **Configuración Firewall (si aplica)**:
```
Outbound HTTPS:  Puerto 443 → OpenAI, GitHub, Streamlit  
Inbound HTTP:    Puerto 8501 → Solo desarrollo local
SSH Access:      Puerto 22 → Solo admin authorized
```

---

## 📈 Requisitos de Performance

### **Capacidad Sistema**:
```
Concurrent Users:    5-10 usuarios simultáneos (Streamlit Cloud)
File Size Limit:     5MB por archivo
Comments Limit:      2000 comentarios por análisis
Analysis Time:       30-300 segundos según volumen
Memory Usage:        <1GB durante análisis
```

### **OpenAI Rate Limits**:
```
RPM (Requests/min):  20+ recomendado para uso empresarial
TPM (Tokens/min):    40,000+ para análisis grandes  
Concurrent:          3+ requests paralelas
Queue handling:      Retry logic implementado
```

### **Performance Testing**:
```bash
# Test carga archivo grande
# 1. Crear archivo CSV con 1000+ comentarios
# 2. Upload en aplicación  
# 3. Monitorear tiempo análisis
# 4. Verificar memoria usage

# Expected results:
# ├── Upload time: <30s
# ├── IA analysis: 60-180s  
# ├── Results display: <10s
# └── Excel export: <20s
```

---

## 🎯 Checklist Pre-Producción

### **✅ Configuración Completa**:
- [ ] OpenAI account con billing activo
- [ ] API key generada y probada localmente
- [ ] Streamlit Cloud account configurado
- [ ] GitHub repository con código actual
- [ ] Secrets configurados en Streamlit Cloud
- [ ] .streamlit/config.toml optimizado

### **✅ Testing Completo**:
- [ ] Deploy exitoso en Streamlit Cloud
- [ ] Página principal muestra "Sistema IA Maestro: Activo"  
- [ ] Upload archivo test exitoso
- [ ] Análisis IA completa sin errores
- [ ] Export Excel funciona correctamente
- [ ] CSS glassmorphism carga correctamente

### **✅ Monitoreo Setup**:
- [ ] OpenAI usage alerts configuradas
- [ ] Budget limits establecidos
- [ ] Error monitoring activo
- [ ] Backup configuración documentado

### **✅ Documentación y Training**:
- [ ] Users entrenados en uso sistema IA
- [ ] Troubleshooting guide distribuida
- [ ] Procedimientos escalation definidos
- [ ] Contactos support actualizados

---

## 🚀 Go-Live Process

### **Fase 1: Soft Launch (1-2 semanas)**
1. **Deploy en Cloud**: Configuración inicial
2. **Testing limitado**: 2-3 usuarios power
3. **Monitoreo intensivo**: Daily usage review
4. **Ajustes**: Performance tuning según datos reales

### **Fase 2: Full Production**
1. **Training usuarios**: Sessions grupales
2. **Documentación**: Distribución guías finales
3. **Support**: Canal establecido
4. **Monitoring**: Automated alerts activos

---

## 📞 Contactos y Escalation

### **Support Técnico**:
- **Documentación**: docs/ folder completa
- **OpenAI Issues**: platform.openai.com/support  
- **Streamlit Issues**: docs.streamlit.io + forum
- **GitHub Issues**: Repository issues para bugs

### **Emergency Contacts**:
- **OpenAI Downtime**: status.openai.com
- **Streamlit Outage**: status.streamlit.io
- **Critical Issues**: [Tu escalation process aquí]

---

*Requisitos sistema IA puro versión 3.0.0*  
*Personal Paraguay | Enterprise Requirements | Septiembre 2025*