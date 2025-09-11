# Guía de Usuario - Analizador de Comentarios IA

## Introducción

El Analizador de Comentarios IA es un sistema profesional que utiliza **Inteligencia Artificial GPT-4** para analizar automáticamente comentarios de clientes, proporcionando insights valiosos para la toma de decisiones empresariales.

## 🚀 Inicio Rápido

### 1. Acceso al Sistema
- Navega a la URL proporcionada por tu administrador
- O ejecuta localmente: `streamlit run streamlit_app.py`
- Accede desde tu navegador (por defecto: http://localhost:8501)

### 2. Interface Principal
La aplicación tiene dos páginas principales:
- **📊 Página Principal**: Dashboard con resultados y métricas
- **📤 Subir**: Carga de archivos y análisis IA

## 📋 Preparación de Datos

### Formatos de Archivo Soportados

#### Excel (.xlsx, .xls)
```
Columna A: Comentario Final
Columna B: Fecha (opcional)
Columna C: Calificación (opcional)
```

#### CSV (.csv)
```
"Comentario Final","Fecha","Calificación"
"Excelente servicio","01/12/2024","9"
"Muy lento el internet","02/12/2024","3"
```

### Ejemplo de Datos de Entrada
```
Comentario Final                                    | Fecha      | Calificación
---------------------------------------------------|-----------|-----------
"Servicio de fibra óptica excelente y estable"     | 01/12/2024| 9
"Conexión se corta frecuentemente por las noches"  | 02/12/2024| 2
"Atención al cliente muy profesional"              | 03/12/2024| 8
"Internet lento en horarios pico"                  | 04/12/2024| 4
"Técnicos muy capacitados en la instalación"      | 05/12/2024| 9
```

### Límites del Sistema
- **Tamaño de archivo**: Máximo 5MB
- **Número de comentarios**: Hasta 2,000 por análisis
- **Formatos**: Solo Excel (.xlsx, .xls) y CSV (.csv)
- **Encoding**: UTF-8 recomendado para caracteres especiales

## 📤 Proceso de Análisis

### Paso 1: Carga de Archivo

1. Ve a la página **"📤 Subir"**
2. Haz clic en **"Browse files"** o arrastra tu archivo
3. El sistema validará automáticamente:
   - Formato del archivo
   - Tamaño (< 5MB)
   - Estructura de datos
   - Detección automática de columnas

### Paso 2: Configuración Automática

El sistema detecta automáticamente:
- **Columna de comentarios**: Busca "comentario", "comment", "feedback", "observacion"
- **Columna de fecha**: Busca "fecha", "date", "timestamp"
- **Columna de calificación**: Busca "calificacion", "rating", "nota", "puntuacion"

### Paso 3: Análisis IA

Una vez cargado el archivo:

1. **Inicia análisis**: Haz clic en "🚀 Iniciar Análisis IA"
2. **Progreso en tiempo real**: Verás una barra de progreso con:
   - Estado actual del análisis
   - Tiempo estimado restante
   - Información sobre el procesamiento
3. **Tiempo de análisis**: 30 segundos a 2 minutos (según cantidad de comentarios)

#### ¿Qué hace la IA durante el análisis?
- Analiza cada comentario con GPT-4
- Detecta sentimientos (positivo, negativo, neutral)
- Identifica emociones específicas (alegría, frustración, satisfacción, etc.)
- Encuentra temas principales automáticamente
- Detecta puntos de dolor críticos
- Genera recomendaciones estratégicas

## 📊 Interpretación de Resultados

### Dashboard Principal

Una vez completado el análisis, verás:

#### 1. Métricas Generales
```
📊 Total de Comentarios Analizados: 150
📈 Sentimiento General: 68% Positivo
⭐ Calificación Promedio: 7.2/10
🎯 Confianza del Análisis IA: 94%
```

#### 2. Distribución de Sentimientos
- **Gráfico de barras** con porcentajes
- **Positivo**: Comentarios satisfactorios
- **Negativo**: Comentarios con quejas o problemas
- **Neutral**: Comentarios informativos sin carga emocional

#### 3. Análisis de Emociones
Emociones detectadas con intensidad 0-10:
- **Satisfacción**: Nivel de contentamiento
- **Frustración**: Grado de molestia o enojo
- **Gratitud**: Expresiones de agradecimiento
- **Preocupación**: Inquietudes sobre el servicio
- **Confianza**: Nivel de seguridad en la marca

#### 4. Temas Más Relevantes
Identificación automática de temas como:
- **Calidad del Servicio** (85% de comentarios)
- **Atención al Cliente** (62% de comentarios)
- **Problemas Técnicos** (38% de comentarios)
- **Precios y Tarifas** (29% de comentarios)

#### 5. Puntos de Dolor Críticos
Problemas ordenados por severidad:
- **Severidad Alta**: Requieren atención inmediata
- **Severidad Media**: Problemas recurrentes a resolver
- **Severidad Baja**: Mejoras menores sugeridas

### Gráficos Interactivos

#### Gráfico de Sentimientos por Tiempo
- Visualiza evolución de sentimientos en el tiempo
- Identifica patrones temporales
- Permite detectar momentos críticos

#### Distribución de Calificaciones
- Histograma de calificaciones numéricas
- Correlación con análisis de sentimientos IA
- Identificación de outliers

## 📊 Insights y Recomendaciones IA

### Resumen Ejecutivo Generado por IA

El sistema proporciona un resumen narrativo como:

```
"Análisis de 150 comentarios de clientes de Personal Paraguay revela 
un 68% de sentimientos positivos, destacando la calidad del servicio 
de fibra óptica. Sin embargo, se identifican problemas recurrentes 
de conectividad en horarios pico (23% de comentarios negativos) y 
oportunidades de mejora en el servicio de atención telefónica."
```

### Recomendaciones Estratégicas

La IA genera recomendaciones accionables:

1. **Prioridad Alta**
   - "Implementar monitoreo proactivo de conectividad en horarios pico"
   - "Capacitar equipo de soporte en resolución rápida de incidencias"

2. **Prioridad Media**
   - "Desarrollar comunicación proactiva sobre mantenimientos"
   - "Crear programa de seguimiento post-instalación"

3. **Oportunidades**
   - "Aprovechar alta satisfacción para programa de referidos"
   - "Documentar mejores prácticas del equipo técnico"

### Comentarios Críticos Destacados

El sistema identifica automáticamente comentarios que requieren atención inmediata:

```
🚨 CRÍTICO: "Internet sin funcionar hace 3 días, sin respuesta del soporte"
⚠️  IMPORTANTE: "Prometen velocidad que nunca entregan, muy decepcionante"
```

## 📥 Exportación de Resultados

### Reporte Excel Completo

Haz clic en **"📥 Descargar Reporte Excel"** para obtener:

#### Hoja 1: Resumen Ejecutivo
- Métricas principales
- Gráficos de distribución
- Resumen narrativo de IA
- Recomendaciones principales

#### Hoja 2: Análisis Detallado
- Lista completa de comentarios
- Sentimiento por comentario
- Emociones detectadas
- Temas identificados
- Puntos de dolor específicos

#### Hoja 3: Métricas y Tendencias
- Evolución temporal de sentimientos
- Correlaciones entre variables
- Estadísticas descriptivas

#### Hoja 4: Comentarios Críticos
- Solo comentarios que requieren atención inmediata
- Clasificados por severidad
- Con recomendaciones específicas de acción

### Formato del Reporte

El archivo Excel incluye:
- **Formato profesional** con colores y estilos
- **Gráficos integrados** para visualización
- **Filtros automáticos** en todas las tablas
- **Comentarios explicativos** en celdas relevantes

## 🔍 Consejos de Uso Avanzado

### Preparación de Datos para Mejores Resultados

#### ✅ Buenas Prácticas
- **Comentarios completos**: Evita textos muy cortos (< 10 palabras)
- **Contexto claro**: Incluye información suficiente para análisis
- **Fechas consistentes**: Usa formato DD/MM/YYYY
- **Encoding UTF-8**: Para caracteres especiales y acentos

#### ❌ Evitar
- Datos duplicados exactos
- Comentarios solo con números o símbolos
- Mezcla de idiomas sin contexto
- Archivos con celdas combinadas o formatos complejos

### Interpretación de Confianza IA

La **Confianza del Análisis** indica:
- **90-100%**: Análisis muy confiable, resultados sólidos
- **80-89%**: Análisis confiable con pequeñas incertidumbres
- **70-79%**: Análisis aceptable, verificar comentarios ambiguos
- **< 70%**: Revisar calidad de datos de entrada

### Casos de Uso Recomendados

#### 1. Análisis Mensual de Satisfacción
- Cargar comentarios del mes
- Comparar con períodos anteriores
- Identificar tendencias y patrones

#### 2. Evaluación Post-Campaña
- Analizar feedback después de campañas
- Medir impacto en percepción de marca
- Ajustar estrategias futuras

#### 3. Detección de Problemas Emergentes
- Análisis semanal para identificar nuevos issues
- Monitoreo de puntos de dolor recurrentes
- Respuesta proactiva a problemas

## 🆘 Solución de Problemas Comunes

### Errores de Carga de Archivo

#### "Archivo muy grande"
- **Problema**: Archivo > 5MB
- **Solución**: Dividir en archivos más pequeños o comprimir Excel

#### "Formato no soportado"
- **Problema**: Archivo no es .xlsx, .xls, o .csv
- **Solución**: Convertir a formato Excel o CSV

#### "No se detectaron comentarios"
- **Problema**: Columna de comentarios no reconocida
- **Solución**: Renombrar columna a "Comentario", "Comment" o "Feedback"

### Errores de Análisis IA

#### "Error de servicio IA"
- **Problema**: Problemas con OpenAI o conectividad
- **Solución**: Intentar nuevamente en unos minutos

#### "Tiempo de espera agotado"
- **Problema**: Análisis muy complejo o archivo muy grande
- **Solución**: Reducir número de comentarios (< 1000)

### Problemas de Visualización

#### "Gráficos no se muestran"
- **Problema**: Problemas de conexión o navegador
- **Solución**: Refrescar página, usar Chrome/Firefox actualizado

#### "Datos incompletos en dashboard"
- **Problema**: Análisis parcial o interrumpido
- **Solución**: Ejecutar análisis nuevamente

## 📞 Soporte y Contacto

### Recursos de Ayuda
- **Esta documentación**: Referencia completa del sistema
- **Troubleshooting**: Ver `troubleshooting.md` para problemas específicos
- **Ejemplos**: Archivos de ejemplo en carpeta `examples/`

### Información del Sistema
- **Versión actual**: 3.0.0-ia-pure
- **Motor IA**: OpenAI GPT-4
- **Última actualización**: Septiembre 2025

---

## 🎯 Resumen de Funcionalidades

✅ **Análisis IA Automático** con GPT-4  
✅ **Detección de Sentimientos** granular  
✅ **Identificación de Emociones** específicas  
✅ **Temas Principales** automáticos  
✅ **Puntos de Dolor** clasificados por severidad  
✅ **Recomendaciones Estratégicas** accionables  
✅ **Exportación Excel** profesional  
✅ **Dashboard Interactivo** con gráficos  
✅ **Análisis en Español** nativo  

**¡El futuro del análisis de comentarios está aquí, potenciado por Inteligencia Artificial!**