# Guía de Usuario - Analizador de Comentarios IA

## 📱 Introducción

Bienvenido al **Personal Paraguay Analizador de Comentarios**, una aplicación de **Inteligencia Artificial avanzada** que analiza automáticamente comentarios de clientes usando GPT-4 de OpenAI.

### 🎯 **¿Qué hace esta aplicación?**
- **Analiza sentimientos** (positivo, negativo, neutral) con precisión superior
- **Identifica emociones específicas** (frustración, satisfacción, enojo, etc.) con intensidades
- **Detecta temas principales** automáticamente (servicio, precio, calidad, etc.)
- **Encuentra puntos de dolor** críticos que requieren atención inmediata
- **Genera recomendaciones** accionables para mejorar tu negocio
- **Crea reportes Excel** profesionales automáticamente

### 🏢 **Ideal para:**
- **Telecomunicaciones**: Análisis de satisfacción con internet y servicios
- **Retail**: Comentarios sobre productos y experiencia de compra  
- **Servicios**: Feedback sobre atención al cliente
- **Cualquier negocio** que reciba comentarios de clientes

---

## 🚀 Cómo Usar la Aplicación

### **Paso 1: Acceder a la Aplicación**
1. Abre tu navegador web
2. Ve a la URL de la aplicación
3. La página principal se cargará automáticamente

### **Paso 2: Verificar Estado del Sistema**
En la **página principal** verás:
- **Estado del sistema**: Debe mostrar "Sistema activo"
- **OpenAI**: Debe mostrar "Configurado" 
- **Comentarios**: Número de análisis en memoria

Si hay problemas, contacta al administrador.

### **Paso 3: Ir a la Página de Análisis**
1. En la **barra lateral izquierda**, haz clic en **"Subir"**
2. Llegarás a la página de carga de archivos

### **Paso 4: Preparar tu Archivo**
Tu archivo debe contener **comentarios de clientes** en uno de estos formatos:

#### **Formatos Soportados:**
- **Excel**: `.xlsx`, `.xls`  
- **CSV**: `.csv`

#### **Estructura Requerida:**
- **Una columna con comentarios** (puede llamarse: "comentario", "comment", "feedback", "review", etc.)
- **Opcionalmente**: Columnas con calificaciones NPS o notas numéricas
- **Máximo**: 5MB de tamaño de archivo

#### **Ejemplo de Estructura:**
| Comentario | NPS | Nota |
|------------|-----|------|
| El servicio es excelente, muy satisfecho | 9 | 4.5 |
| Internet muy lento, no funciona bien | 3 | 2.0 |
| Atención al cliente muy amable | 8 | 4.0 |

### **Paso 5: Subir y Analizar**

#### **Subir Archivo:**
1. Haz clic en **"Selecciona tu archivo"**
2. Elige tu archivo Excel o CSV
3. Verás una **vista previa** automática con las primeras 5 filas
4. Confirma que los datos se ven correctos

#### **Analizar con IA:**
1. Haz clic en **"Analizar con Inteligencia Artificial"** 
2. La aplicación procesará todos los comentarios con GPT-4
3. Espera mientras se completa el análisis (típicamente 30-60 segundos)
4. ¡Verás una celebración cuando termine!

---

## 📊 Entender los Resultados

### **Métricas Principales**
Verás 4 métricas principales en la parte superior:

#### **Total Comentarios**
- Cantidad de comentarios válidos procesados
- Excluye comentarios vacíos o inválidos

#### **Tiempo IA**
- Segundos que tomó el análisis con GPT-4
- Indicador de complejidad del análisis

#### **IA: Positivos / IA: Negativos**
- Comentarios clasificados como positivos o negativos por la IA
- Los neutrales no se muestran en métricas principales

### **Insights de Inteligencia Artificial**

#### **Temas Principales Detectados por IA**
- **Lista automática** de temas más relevantes
- **Puntuación de relevancia** (0.0 - 1.0)
- **Ordenados por importancia** según IA

*Ejemplo:*
- **servicio al cliente**: Relevancia 0.85
- **velocidad internet**: Relevancia 0.73  
- **precio mensual**: Relevancia 0.64

#### **Emociones Identificadas por IA**
- **Emociones específicas** detectadas en los comentarios
- **Intensidad medida** (0.0 - 10.0)
- **Análisis psicológico** profundo

*Ejemplo:*
- **frustración**: Intensidad 7.2
- **satisfacción**: Intensidad 8.1
- **preocupación**: Intensidad 5.4

#### **Resumen Ejecutivo (Generado por IA)**
- **Análisis narrativo** escrito por GPT-4
- **Conclusiones principales** en lenguaje natural
- **Contexto y insights** que solo IA puede detectar

#### **Recomendaciones de IA**
- **Acciones específicas** sugeridas por la IA
- **Priorizadas automáticamente** por impacto
- **Basadas en análisis completo** de todos los comentarios

### **Comentarios Críticos**
Si hay comentarios que requieren **atención inmediata**:
- Aparecerá una sección expandible
- **Lista de comentarios urgentes** identificados por IA
- **Acciones recomendadas** específicas para cada caso

---

## 📥 Exportar Resultados

### **Excel con Análisis IA**
1. Haz clic en **"Generar Excel con Resultados IA"**
2. Se creará automáticamente un reporte Excel completo
3. Haz clic en **"Descargar Excel"** para obtener el archivo

#### **Contenido del Excel:**
- **Resumen ejecutivo** generado por IA
- **Distribución de sentimientos** con conteos
- **Temas más relevantes** con puntuaciones
- **Emociones predominantes** con intensidades  
- **Recomendaciones principales** priorizadas
- **Metadatos del análisis** (modelo, tiempo, confianza)

### **Nombre del Archivo**
- Formato: `analisis_ia_YYYYMMDD_HHMMSS.xlsx`
- Ejemplo: `analisis_ia_20250124_143022.xlsx`

---

## ❗ Solución de Problemas Comunes

### **"Sistema no inicializado"**
**Problema**: La aplicación no se cargó correctamente  
**Solución**: Recarga la página completamente (F5)

### **"OpenAI API key es requerida"**
**Problema**: No hay API key configurada  
**Solución**: Contacta al administrador del sistema

### **"Error de servicio IA"**
**Problema**: Problemas con la conexión a OpenAI  
**Soluciones**:
- Verifica tu conexión a internet
- Intenta nuevamente en unos minutos
- Si persiste, contacta soporte técnico

### **"Archivo muy grande"**
**Problema**: El archivo supera los 5MB  
**Soluciones**:
- Reduce el tamaño del archivo
- Elimina columnas innecesarias
- Divide en múltiples archivos más pequeños

### **"No se pudo generar vista previa"**  
**Problema**: El archivo tiene formato incorrecto
**Soluciones**:
- Verifica que sea Excel (.xlsx, .xls) o CSV
- Asegúrate de que tenga una columna con comentarios de texto
- Revisa que no esté corrupto

---

## 💡 Consejos para Mejores Resultados

### **Preparación de Datos**
- **Comentarios claros**: Textos completos funcionan mejor que palabras sueltas
- **Idioma consistente**: Español, inglés o guaraní (IA detecta automáticamente)
- **Sin datos personales**: Remover emails, teléfonos, nombres antes de subir

### **Interpretación de Resultados**
- **Confianza IA**: Valores más altos (>0.8) indican análisis más certero
- **Intensidades emocionales**: 7+ indica emociones muy fuertes
- **Relevancia de temas**: 0.7+ indica temas muy importantes para tus clientes

### **Uso de Recomendaciones**
- Las **recomendaciones de IA** están priorizadas por impacto
- **Implementa primero** las recomendaciones que aparecen al inicio
- **Combina recomendaciones** relacionadas para mayor efecto

---

## 📞 Soporte

### **Para Problemas Técnicos**
- Revisa esta guía primero
- Consulta la sección de troubleshooting
- Contacta al administrador del sistema

### **Para Dudas sobre Resultados**
- Los resultados son generados por **GPT-4**, la IA más avanzada disponible
- La IA analiza **contexto, matices y emociones** que humanos podrían pasar por alto
- **Confía en los insights de IA** - están basados en análisis de millones de textos

### **Para Solicitudes de Nuevas Funcionalidades**
- Esta aplicación está optimizada para **análisis IA puro**
- Las mejoras se enfocan en **mejor integración con IA** 
- No se agregan **funcionalidades manuales o de reglas**

---

## 🎉 ¡Disfruta del Poder de la IA!

Esta aplicación te da acceso a **análisis de comentarios de nivel enterprise** usando la **Inteligencia Artificial más avanzada** del mundo. 

**Cada análisis** es único, profundo y te proporcionará **insights que transformarán** cómo entiendes a tus clientes.

---

*Guía de usuario v3.0.0-ia-pure*  
*Personal Paraguay | 2025*