# Analizador de Comentarios - Sistema de Análisis de Feedback de Clientes

Sistema sofisticado de análisis de sentimientos y detección de patrones multilingüe diseñado para analizar comentarios de clientes sobre servicios de fibra óptica al hogar. Desarrollado específicamente para Personal Paraguay (Núcleo S.A.) para proporcionar inteligencia empresarial accionable a partir del feedback de clientes.

## 📚 Documentación Técnica

Para documentación técnica completa, guías de desarrollo y especificaciones arquitectónicas, visite el **[Centro de Documentación Técnica](./documentation/README.md)** (en inglés).

## 🚀 Características Principales

### Capacidades Fundamentales
- **Soporte Multilingüe**: Soporte completo para español (dialecto paraguayo) y detección de guaraní
- **Análisis de Sentimientos Avanzado**: Detección de emociones y puntuación de sentimientos usando OpenAI GPT-4
- **Reconocimiento de Patrones**: Identificación automática de temas y análisis de tendencias
- **Panel Interactivo**: Visualización en tiempo real con interfaz Streamlit
- **Reportes Profesionales**: Exportaciones a Excel con múltiples hojas, análisis detallados y visualizaciones

### Características Técnicas
- **Integración con IA**: OpenAI GPT-4 para análisis avanzado
- **Optimización de Rendimiento**: Caché inteligente y procesamiento por lotes
- **Control de Costos**: Monitoreo integrado del uso de API
- **Diseño Responsivo**: Interfaz adaptable para móviles con tema profesional
- **Seguridad**: Validación de entrada y manejo seguro de API

## 📦 Instalación Rápida

### Requisitos Previos
- Python 3.9 o superior
- Clave de API de OpenAI (GPT-4)
- 4GB RAM mínimo recomendado

### Pasos de Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/aiwhispererwvdp/Comment-Analizer.git
   cd Comment-Analizer
   ```

2. **Crear entorno virtual** (recomendado)
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**
   
   Crear archivo `.env` en la raíz del proyecto:
   ```env
   # Requerido: Clave API de OpenAI
   OPENAI_API_KEY=tu_clave_api_aqui
   
   # Opcional: Configuración adicional
   OPENAI_MODEL=gpt-4
   OPENAI_MAX_TOKENS=4000
   OPENAI_TEMPERATURE=0.7
   LOG_LEVEL=INFO
   ```

## 🎯 Uso Rápido

### Iniciar la Aplicación

```bash
# Opción 1: Usando Streamlit directamente
streamlit run src/main.py

# Opción 2: Usando el script de inicio
python run.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

### Cómo Usar la Aplicación

1. **Acceder a la interfaz**: Navegar a http://localhost:8501
2. **Cargar archivo**: Usar el cargador para subir Excel con comentarios
3. **Analizar**: Hacer clic en "🚀 Análisis Rápido"
4. **Ver resultados**: Explorar el panel interactivo con métricas y gráficos
5. **Exportar**: Descargar reportes profesionales en Excel

## 📊 Formato de Datos de Entrada

### Archivos Soportados
- **Excel** (.xlsx, .xls) - Formato recomendado
- **CSV** (.csv) - Soporte alternativo

### Estructura Requerida
El archivo debe contener al menos una columna con comentarios de texto:

| Columna | Tipo | Requerido | Descripción |
|---------|------|-----------|-------------|
| Comentario | Texto | ✅ Sí | Feedback del cliente |
| Fecha | Fecha | ⚪ No | Timestamp del comentario |
| Nota | Número | ⚪ No | Calificación numérica |
| NPS | Texto | ⚪ No | Categoría NPS |
| Cliente | Texto | ⚪ No | Identificador del cliente |

**Nota**: El sistema detecta automáticamente columnas con nombres como "Comentario Final", "Observaciones", "Feedback", etc.

## 📈 Capacidades de Análisis

### Análisis Disponibles
- **Sentimiento**: Positivo, Negativo, Neutro con puntuación de confianza
- **Emociones**: Detección de alegría, enojo, tristeza, miedo, sorpresa
- **Temas Clave**: Identificación automática de tópicos recurrentes
- **Tendencias**: Análisis temporal de cambios en sentimiento
- **Métricas NPS**: Cálculos automáticos de Net Promoter Score

### Formatos de Exportación

#### Reporte Excel Profesional
Libro de trabajo completo con 15+ hojas incluyendo:
- Resumen ejecutivo con métricas clave
- Análisis detallado comentario por comentario
- Detección de temas y patrones
- Segmentación de clientes
- Análisis avanzados (riesgo de abandono, emociones)
- Recomendaciones accionables

## 🔒 Seguridad y Privacidad

- ✅ Todo el procesamiento se realiza localmente
- ✅ Las llamadas a API usan conexiones encriptadas
- ✅ No se almacenan datos de clientes permanentemente
- ✅ Políticas configurables de retención de datos
- ✅ Validación y sanitización de entrada

## 🎯 Casos de Uso

### Aplicaciones Empresariales
- **Servicio al Cliente**: Identificar quejas y problemas comunes
- **Desarrollo de Producto**: Entender solicitudes de funcionalidades
- **Marketing**: Medir efectividad de campañas
- **Calidad**: Rastrear tendencias de calidad del servicio
- **Inteligencia de Negocio**: Toma de decisiones basada en datos

## 🧪 Ejecutar Pruebas

```bash
# Ejecutar suite completa de pruebas
pytest tests/

# Ejecutar con cobertura
pytest --cov=src tests/

# Ejecutar pruebas específicas
pytest tests/test_sentiment_analysis.py
```

## 📁 Estructura del Proyecto

```
Comment-Analyzer/
├── src/                    # Código fuente principal
│   ├── main.py            # Punto de entrada de la aplicación
│   ├── ai_overseer.py     # Supervisión de calidad con IA
│   └── [módulos...]       # Componentes del sistema
├── data/                   # Almacenamiento de datos
├── outputs/                # Resultados generados
├── tests/                  # Suite de pruebas
├── documentation/          # Documentación técnica (inglés)
└── local-reports/          # Reportes de análisis internos
```

## 🤝 Soporte

Para soporte, solicitudes de funcionalidades o reportes de errores:
- Contactar al equipo de desarrollo de Personal Paraguay
- Crear un issue en este repositorio
- Revisar la [documentación técnica](./documentation/README.md)

## 📝 Licencia

Software Propietario - Personal Paraguay (Núcleo S.A.)  
Todos los derechos reservados.

## 🚀 Estado del Proyecto

**Versión**: 1.0.0  
**Estado**: Producción  
**Última Actualización**: Agosto 2025  
**Mantenido por**: Equipo de Desarrollo Personal Paraguay

---

## 💡 Inicio Rápido para Diferentes Roles

### Para Analistas de Negocio
1. Instalar siguiendo los pasos anteriores
2. Preparar archivo Excel con comentarios
3. Ejecutar análisis y descargar reportes
4. Revisar [Guía de Usuario](./documentation/guides/USER_GUIDE.md)

### Para Desarrolladores
1. Clonar y configurar entorno de desarrollo
2. Revisar [Documentación Técnica](./documentation/README.md)
3. Ejecutar pruebas para verificar configuración
4. Explorar arquitectura en `/documentation/architecture/`

### Para DevOps
1. Revisar [Guía de Docker](./documentation/deployment/DOCKER_DEPLOYMENT.md)
2. Configurar variables de entorno
3. Desplegar usando contenedores Docker
4. Monitorear health endpoint: `http://localhost:8501/_stcore/health`

---

## 🔄 Actualizaciones Recientes

### Versión 1.0.0 (Agosto 2025)
- ✅ Limpieza completa del código base
- ✅ Optimización de dependencias (-40% tamaño)
- ✅ Mejoras en manejo de errores
- ✅ Documentación actualizada en español
- ✅ Integración mejorada con AI Overseer

### Próximas Mejoras Planificadas
- 🔄 Soporte completo para guaraní
- 🔄 Dashboard de monitoreo en tiempo real
- 🔄 Integración con webhooks
- 🔄 Exportación a formatos adicionales

---

Construido con ❤️ para Personal Paraguay para mejorar la experiencia del cliente a través de insights basados en datos.