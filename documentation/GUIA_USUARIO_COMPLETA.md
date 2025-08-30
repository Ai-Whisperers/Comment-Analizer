# Guía Completa del Usuario - Analizador de Comentarios

## 📋 **Índice**
1. [Introducción](#introducción)
2. [Instalación](#instalación)  
3. [Primer Uso](#primer-uso)
4. [Análisis de Sentimientos](#análisis-de-sentimientos)
5. [Gestión de Memoria](#gestión-de-memoria)
6. [Exportación y Reportes](#exportación-y-reportes)
7. [Resolución de Problemas](#resolución-de-problemas)
8. [Preguntas Frecuentes](#preguntas-frecuentes)

---

## 🎯 **Introducción**

El Analizador de Comentarios es una herramienta profesional que permite analizar automáticamente comentarios de clientes para identificar sentimientos, patrones y tendencias.

### **Casos de Uso Principales**
- **Análisis de satisfacción**: Entender qué piensan los clientes
- **Detección de problemas**: Identificar quejas recurrentes  
- **Monitoreo de calidad**: Seguimiento de métricas de servicio
- **Reportes ejecutivos**: Dashboards con insights accionables

### **Beneficios Clave**
- ⚡ **Automatización**: Análisis en segundos vs horas manuales
- 🎯 **Precisión**: IA entrenada para español de Paraguay
- 📊 **Visualización**: Gráficos interactivos y dashboards
- 📝 **Reportes**: Exportación profesional a Excel

---

## 💻 **Instalación**

### **Opción 1: UN SOLO CLIC (Recomendado para Windows)**

Para usuarios **sin conocimientos técnicos**:

1. **Descargar** el proyecto completo
2. **Ejecutar** `START_HERE.bat`  
3. **Esperar** que se instale automáticamente
4. **¡Listo!** Se abre el navegador automáticamente

**El script automático hace todo por ti:**
- ✅ Instala Python si no está presente
- ✅ Instala todas las dependencias
- ✅ Te ayuda a configurar OpenAI API (opcional)
- ✅ Inicia la aplicación automáticamente

### **Opción 2: Instalación Manual (Desarrolladores)**

```bash
# 1. Clonar repositorio
git clone https://github.com/Ai-Whisperers/Comment-Analizer.git
cd Comment-Analizer

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar variables (opcional)
# Crear archivo .env con:
OPENAI_API_KEY=tu-clave-aqui

# 4. Ejecutar
python run.py
```

### **Opción 3: Streamlit Cloud (Sin instalación)**

**Acceso directo**: https://comment-analizer.streamlit.app

**Ventajas**:
- Sin instalación local
- Siempre actualizado
- Acceso desde cualquier dispositivo
- Sin consumo de recursos locales

**Limitaciones**:
- Archivos máximo 3MB
- Máximo 500 comentarios por archivo
- Requiere conexión a internet

---

## 🚀 **Primer Uso**

### **Paso 1: Preparar tus Datos**

#### **Formato de Archivo Requerido**
Tu archivo Excel debe tener **al menos una columna con comentarios de texto**:

| Comentario Final | Fecha | Cliente |
|------------------|-------|---------|
| Excelente servicio de Internet, muy rápido | 01/08/2024 | Juan P. |
| La conexión se corta frecuentemente | 02/08/2024 | María G. |
| Buena atención al cliente | 03/08/2024 | Carlos R. |

#### **Nombres de Columna Detectados Automáticamente**
El sistema reconoce estas columnas:
- `comentario final`, `comentario`, `comentarios`
- `comment`, `comments`, `feedback`
- `texto`, `observacion`, `opinion`
- `mensaje`, `respuesta`

**💡 Tip**: Si tu columna tiene otro nombre, el sistema usará la primera columna de texto que encuentre.

### **Paso 2: Cargar el Archivo**

1. **Arrastra y suelta** tu archivo Excel en la zona de carga
2. **O haz clic** en "Browse files" para seleccionar
3. **Espera** a que aparezca la vista previa
4. **Verifica** que se detectó correctamente la columna

### **Paso 3: Seleccionar Método de Análisis**

#### **Análisis Rápido (Gratuito)**
- ⚡ **Velocidad**: Resultados en 30-60 segundos
- 💰 **Costo**: Completamente gratuito
- 🎯 **Precisión**: Buena para español básico
- 📊 **Incluye**: Sentimientos, temas básicos, estadísticas

#### **Análisis Avanzado (IA)**
- 🧠 **Potencia**: OpenAI GPT-4
- 💰 **Costo**: ~$0.02-0.10 por archivo (según tamaño)
- 🎯 **Precisión**: Excelente para contextos complejos
- 📊 **Incluye**: Emociones detalladas, insights, recomendaciones

### **Paso 4: Revisar Resultados**

El dashboard te muestra:
- **Distribución de sentimientos** (% positivo/negativo/neutral)
- **Gráficos interactivos** con tendencias
- **Temas principales** detectados automáticamente
- **Comentarios representativos** por categoría

---

## 📊 **Análisis de Sentimientos**

### **Tipos de Sentimientos Detectados**

#### **Análisis Rápido**
- **Positivo**: Comentarios favorables, satisfacción
- **Neutral**: Comentarios informativos, neutros
- **Negativo**: Quejas, insatisfacción, problemas

#### **Análisis Avanzado (IA)**
Incluye **emociones específicas**:
- 😊 **Satisfacción**: Clientes contentos con el servicio
- 😤 **Frustración**: Problemas técnicos, demoras
- 😐 **Neutralidad**: Comentarios informativos
- 😕 **Decepción**: Expectativas no cumplidas
- 😡 **Enojo**: Problemas graves, mala atención

### **Métricas Clave**

#### **Puntuación Global**
- **Score de Satisfacción**: 0-100%
- **Índice de Problemas**: % de comentarios negativos
- **Tendencia**: Mejorando/Estable/Empeorando

#### **Análisis por Temas**
- **Servicio al Cliente**: Atención, respuesta, profesionalismo
- **Calidad Técnica**: Internet, velocidad, estabilidad  
- **Precios**: Costos, tarifas, promociones
- **Instalación**: Proceso, técnicos, tiempos

### **Interpretación de Resultados**

#### **Semáforo de Alerta**
- 🟢 **Verde (>70% positivos)**: Excelente satisfacción
- 🟡 **Amarillo (50-70%)**: Satisfacción moderada, áreas de mejora
- 🔴 **Rojo (<50%)**: Problemas críticos requieren atención inmediata

#### **Acciones Recomendadas**
El sistema sugiere:
- **Prioridades de mejora** basadas en frecuencia de quejas
- **Fortalezas a mantener** según comentarios positivos  
- **Tendencias a monitorear** en próximos períodos

---

## 🧹 **Gestión de Memoria**

### **¿Por Qué Es Importante?**
En Streamlit Cloud, la memoria está limitada. Una gestión adecuada asegura:
- ✅ **Rendimiento consistente** sin crashes
- ✅ **Capacidad de procesar múltiples archivos**
- ✅ **Experiencia de usuario fluida**

### **Panel de Gestión de Memoria**

El panel muestra:
- **Uso actual**: MB utilizados en tiempo real
- **Porcentaje**: % del límite total (690MB)
- **Estado visual**: 🟢 Verde / 🟡 Amarillo / 🔴 Rojo

#### **Interpretación de Colores**
- 🟢 **Verde (<60%)**: Memoria saludable
- 🟡 **Amarillo (60-80%)**: Precaución, considerar limpiar
- 🔴 **Rojo (>80%)**: Limpiar inmediatamente

### **Cuándo Limpiar Memoria**

#### **Limpieza Recomendada**:
- ✅ **Después de cada análisis completado**
- ✅ **Antes de procesar un archivo grande**
- ✅ **Cuando el indicador esté en amarillo/rojo**
- ✅ **Si la app funciona lenta**

#### **Cómo Limpiar**:
1. **Expandir** el panel "🧹 Gestión de Memoria"
2. **Hacer clic** en "Limpiar Resultados"  
3. **Confirmar** el mensaje de éxito
4. **Verificar** que el uso de memoria bajó

### **Limpieza Automática**

El sistema limpia automáticamente:
- **Durante el procesamiento**: Cada 200 comentarios
- **Entre etapas**: Después de cada fase
- **En errores**: Limpieza de emergencia

---

## 📋 **Exportación y Reportes**

### **Tipos de Reportes Disponibles**

#### **Reporte Básico (Análisis Rápido)**
**Incluye**:
- ✅ Resumen ejecutivo con métricas principales
- ✅ Tabla de comentarios con sentimientos asignados
- ✅ Distribución por categorías  
- ✅ Gráficos de barras y sectores
- ✅ Lista de temas detectados

**Formato**: Excel (.xlsx) con 3-4 hojas

#### **Reporte Avanzado (Análisis IA)**
**Incluye todo lo anterior PLUS**:
- ✅ **Emociones específicas** por comentario
- ✅ **Insights y recomendaciones** de IA
- ✅ **Análisis de patrones** complejos
- ✅ **Scoring de calidad** del análisis
- ✅ **Comentarios representativos** por emoción

**Formato**: Excel (.xlsx) con 5-6 hojas + dashboard

### **Estructura del Excel Exportado**

#### **Hoja 1: Resumen Ejecutivo**
- Métricas principales en dashboard visual
- KPIs destacados con formato profesional
- Recomendaciones de acción

#### **Hoja 2: Análisis Detallado**  
- Cada comentario con su sentimiento asignado
- Confianza del análisis (%)
- Temas detectados por comentario

#### **Hoja 3: Gráficos y Visualizaciones**
- Gráficos de distribución
- Tendencias temporales (si hay fechas)
- Word clouds de temas principales

#### **Hoja 4: Datos Raw**
- Comentarios originales sin procesar
- Metadatos del archivo (fecha, tamaño, etc.)
- Estadísticas técnicas del análisis

### **Personalización del Reporte**

El reporte se adapta automáticamente:
- **Idioma**: Español con contexto paraguayo
- **Fecha**: Formato DD/MM/YYYY
- **Moneda**: Guaraníes (si aplica)
- **Temas**: Específicos del sector telecom

### **Uso Profesional del Excel**

#### **Para Presentaciones Ejecutivas**
- **Copiar gráficos** directamente a PowerPoint
- **Usar métricas del resumen** en reportes gerenciales
- **Destacar insights clave** en reuniones

#### **Para Análisis Técnico**
- **Filtrar comentarios** por sentimiento
- **Crear pivots** con datos detallados
- **Hacer análisis temporal** si tienes fechas

---

## 🛠️ **Resolución de Problemas**

### **Problemas de Instalación**

#### **"Python no se encuentra"**
**Windows**:
```batch
# Instalar desde Microsoft Store o python.org
# Luego ejecutar START_HERE.bat nuevamente
```

**Solución alternativa**:
- Usar la versión Streamlit Cloud (sin instalación)

#### **"ModuleNotFoundError"**
```bash
# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall
```

### **Problemas de Carga de Archivos**

#### **"Archivo demasiado grande"**
**Límites**:
- **Streamlit Cloud**: 3MB máximo
- **Local**: Sin límite (depende de RAM disponible)

**Soluciones**:
1. **Reducir tamaño**: Eliminar columnas innecesarias
2. **Dividir archivo**: Procesar por partes
3. **Usar local**: Instalar localmente para archivos grandes

#### **"No se detectan comentarios"**
**Causas comunes**:
- Columna mal nombrada
- Datos en formato no-texto
- Archivo corrupto

**Soluciones**:
1. **Renombrar columna** a "comentario" o "comentario final"
2. **Verificar datos**: Que sean texto, no números
3. **Probar con archivo nuevo**: Usar plantilla de ejemplo

### **Problemas de Análisis**

#### **"Análisis IA no funciona"**
**Verificaciones**:
1. **API Key configurada**: Revisar archivo `.env` o secrets
2. **Créditos disponibles**: Verificar saldo en OpenAI
3. **Conexión internet**: Requerida para IA

**Fallback**:
- Usar "Análisis Rápido" que no requiere API

#### **"App se congela durante análisis"**
**Causas**:
- Memoria insuficiente
- Archivo muy grande
- Demasiados comentarios

**Soluciones**:
1. **Limpiar memoria** antes del análisis
2. **Reducir tamaño** del archivo
3. **Reiniciar aplicación**

### **Problemas de Rendimiento**

#### **"App muy lenta"**
**Optimizaciones**:
1. **Limpiar resultados** anteriores
2. **Cerrar otras pestañas** del navegador
3. **Usar archivos más pequeños**
4. **Reiniciar navegador**

#### **"Memoria llena constantemente"**
**Monitoreo**:
- Observar panel de memoria en sidebar
- Limpiar después de cada análisis
- No procesar múltiples archivos grandes consecutivamente

---

## ❓ **Preguntas Frecuentes**

### **Generales**

#### **¿Es gratuito?**
- **Análisis Rápido**: Completamente gratuito
- **Análisis IA**: Requiere créditos OpenAI (~$0.02-0.10 por archivo)
- **Instalación y uso**: Gratuito

#### **¿Funciona offline?**
- **Análisis Rápido**: Sí, funciona completamente offline
- **Análisis IA**: No, requiere conexión para OpenAI
- **Streamlit Cloud**: No, requiere internet

#### **¿Qué idiomas soporta?**
- **Español**: Optimizado para Paraguay (principal)
- **Guaraní**: Detección básica
- **Inglés**: Funcionalidad limitada

### **Técnicas**

#### **¿Qué tan preciso es el análisis?**
- **Análisis Rápido**: ~80-85% precisión en español
- **Análisis IA**: ~92-95% precisión con GPT-4
- **Contexto paraguayo**: Optimizado para modismos locales

#### **¿Cuántos comentarios puede procesar?**
- **Streamlit Cloud**: Máximo 500 comentarios
- **Instalación local**: Sin límite (depende de RAM)
- **Recomendado**: 100-300 comentarios para mejor experiencia

#### **¿Guarda mis datos?**
- **No**: Todos los datos se procesan en memoria temporalmente
- **Privacidad**: Nada se almacena permanentemente
- **OpenAI**: Solo se envía texto para análisis IA (política OpenAI aplica)

### **Comerciales**

#### **¿Puede usarse comercialmente?**
- **Sí**: Sin restricciones de uso comercial
- **Licencia**: Open source con atribución
- **Personalización**: Disponible para necesidades específicas

#### **¿Hay soporte técnico?**
- **Documentación**: Completa y actualizada
- **GitHub Issues**: Para reportar problemas
- **Comunidad**: Foro de usuarios disponible

---

## 📞 **Soporte y Recursos**

### **Documentación Adicional**
- **Guía técnica**: `/documentation/` carpeta completa
- **Reportes de análisis**: `/local-reports/` con detalles técnicos
- **Código fuente**: GitHub con comentarios extensivos

### **Enlaces Útiles**
- **App en vivo**: https://comment-analizer.streamlit.app
- **Repositorio**: https://github.com/Ai-Whisperers/Comment-Analizer
- **Issues/Bugs**: https://github.com/Ai-Whisperers/Comment-Analizer/issues

### **Contacto**
- **Email técnico**: via GitHub Issues
- **Documentación**: Primera línea de soporte
- **Comunidad**: Usuarios activos en repositorio

---

*Guía actualizada: 30 de Agosto, 2025*  
*Versión de la aplicación: 2.0 - Optimizada*  
*Próxima actualización: Septiembre 2025*