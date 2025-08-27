# Analizador de Comentarios - Sistema de Análisis de Feedback de Clientes

Sistema avanzado de análisis de sentimientos y detección de patrones diseñado para analizar comentarios de clientes sobre servicios de fibra óptica. Desarrollado específicamente para Personal Paraguay (Núcleo S.A.) para proporcionar inteligencia de negocios accionable a partir del feedback de clientes.

---

## 🚀 INICIO RÁPIDO - GUÍA DE USO

### Requisitos Previos
- Python 3.8 o superior
- Clave API de OpenAI (GPT-4)
- 2GB RAM mínimo
- Navegador web moderno (Chrome, Firefox, Edge)

### Instalación en 3 Pasos

#### 1️⃣ **Clonar el Repositorio**
```bash
git clone https://github.com/aiwhispererwvdp/Comment-Analizer.git
cd Comment-Analizer
```

#### 2️⃣ **Instalar Dependencias**
```bash
# Windows
pip install -r requirements.txt

# Linux/Mac
pip3 install -r requirements.txt
```

#### 3️⃣ **Configurar API Key**
Crear archivo `.env` en la carpeta raíz:
```env
OPENAI_API_KEY=tu_clave_api_aqui
```

### 🎯 Ejecutar la Aplicación

```bash
# Método 1: Comando directo
streamlit run src/main.py

# Método 2: Script de inicio
python run.py
```

La aplicación se abrirá automáticamente en: **http://localhost:8501**

### 📊 Cómo Usar la Aplicación

1. **Abrir el Navegador**: Ir a http://localhost:8501
2. **Cargar Archivo Excel**: 
   - Click en "Examinar archivos" o arrastra tu archivo
   - Formatos soportados: `.xlsx`, `.xls`, `.csv`
3. **Analizar**: Click en el botón "Analizar Comentarios"
4. **Ver Resultados**: 
   - Gráficos interactivos de sentimientos
   - Métricas detalladas
   - Temas principales detectados
5. **Descargar Reporte**: Click en "Descargar Reporte Excel" para obtener análisis completo

### 📁 Formato del Archivo de Entrada

Tu archivo Excel/CSV debe contener:
- **Columna de Comentarios** (obligatorio): Texto del feedback
- **Columna de Fecha** (opcional): Fecha del comentario
- **Columna de Calificación** (opcional): Puntuación numérica

Ejemplo de estructura:
| Comentario Final | Fecha | Nota |
|-----------------|-------|------|
| Excelente servicio | 2024-01-15 | 9 |
| Internet muy lento | 2024-01-16 | 3 |

### 🐳 Opción Docker (Alternativa)

```bash
# Construcción segura
docker build -f Dockerfile.secure -t comment-analyzer .

# Ejecutar con seguridad mejorada
docker run -p 8501:8501 \
  -e OPENAI_API_KEY=tu_clave_api \
  --read-only \
  --security-opt=no-new-privileges \
  comment-analyzer
```

### ⚡ Consejos de Uso

- **Mejor rendimiento**: Archivos de menos de 10,000 comentarios
- **Idiomas soportados**: Español (incluye dialecto paraguayo)
- **Corrección automática**: El sistema corrige errores ortográficos comunes
- **Caché inteligente**: Análisis repetidos son más rápidos
- **Límite de archivo**: Máximo 50MB por archivo

### 🆘 Solución de Problemas Comunes

| Problema | Solución |
|----------|----------|
| "No se encontró columna de comentarios" | Renombra tu columna a "Comentario Final" o "Comment" |
| "Error de API Key" | Verifica que tu clave OpenAI esté correcta en `.env` |
| "Memoria insuficiente" | Reduce el tamaño del archivo o aumenta la RAM disponible |
| Puerto 8501 ocupado | Ejecuta con: `streamlit run src/main.py --server.port 8502` |

---

## 🔧 DETALLES TÉCNICOS E IMPLEMENTACIÓN

### 📐 Arquitectura del Sistema

```
┌─────────────────┐     ┌──────────────┐     ┌─────────────┐
│   Frontend      │────▶│   Backend    │────▶│  AI Engine  │
│   (Streamlit)   │     │   (Python)   │     │  (OpenAI)   │
└─────────────────┘     └──────────────┘     └─────────────┘
         │                      │                     │
         ▼                      ▼                     ▼
┌─────────────────┐     ┌──────────────┐     ┌─────────────┐
│  Visualización  │     │ Procesamiento│     │  Análisis   │
│    (Plotly)     │     │   (Pandas)   │     │ Sentimientos│
└─────────────────┘     └──────────────┘     └─────────────┘
```

### 🏗️ Estructura del Proyecto

```
Comment-Analyzer/
├── src/                        # Código fuente principal
│   ├── main.py                # Punto de entrada de la aplicación
│   ├── ai_overseer.py         # Supervisor de calidad IA
│   ├── config.py              # Configuración y variables de entorno
│   ├── ui_styling.py          # Estilos y temas de la interfaz
│   ├── api/                   # Integraciones con APIs externas
│   │   ├── api_client.py      # Cliente OpenAI
│   │   ├── cache_manager.py   # Sistema de caché
│   │   └── monitoring.py      # Monitoreo de uso de API
│   ├── components/            # Componentes de UI reutilizables
│   │   ├── enhanced_results_ui.py
│   │   └── optimized_file_upload_ui.py
│   ├── data_processing/       # Procesamiento de datos
│   │   ├── comment_reader.py  # Lector de archivos
│   │   └── language_detector.py # Detección de idioma
│   ├── sentiment_analysis/    # Motor de análisis
│   │   ├── openai_analyzer.py # Análisis con GPT-4
│   │   └── enhanced_analyzer.py # Análisis mejorado
│   ├── pattern_detection/     # Detección de patrones
│   │   └── pattern_detector.py # Identificación de temas
│   ├── services/              # Lógica de negocio
│   │   ├── analysis_service.py
│   │   └── file_upload_service.py
│   ├── theme/                 # Temas visuales
│   │   ├── dark_theme.py
│   │   └── modern_theme.py
│   ├── utils/                 # Utilidades
│   │   ├── validators.py      # Validación de datos
│   │   ├── memory_manager.py  # Gestión de memoria
│   │   └── exceptions.py      # Manejo de errores
│   └── visualization/         # Exportación y gráficos
│       └── export_manager.py  # Generación de reportes
├── tests/                     # Suite de pruebas
├── data/                      # Almacenamiento de datos
├── outputs/                   # Resultados generados
├── documentation/             # Documentación técnica
├── local-reports/            # Reportes de auditoría
├── Dockerfile.secure         # Contenedor seguro
├── docker-compose.secure.yml # Orquestación segura
└── requirements.txt          # Dependencias Python
```

### 🛠️ Stack Tecnológico

#### Backend & Procesamiento
- **Python 3.12**: Lenguaje principal
- **Pandas**: Manipulación de datos
- **NumPy**: Operaciones numéricas
- **OpenAI GPT-4**: Motor de IA para análisis

#### Frontend & Visualización
- **Streamlit**: Framework de aplicación web
- **Plotly**: Gráficos interactivos
- **XlsxWriter**: Generación de Excel profesional
- **CSS Personalizado**: Tema oscuro moderno

#### Seguridad & DevOps
- **Docker**: Contenedorización
- **python-dotenv**: Gestión de configuración
- **Logging**: Sistema de auditoría
- **Rate Limiting**: Control de uso de API

### 🔐 Características de Seguridad

#### Implementadas
- ✅ Validación de entrada en todos los puntos de entrada
- ✅ Manejo seguro de API keys (variables de entorno)
- ✅ Contenedor Docker con usuario no-root
- ✅ Sistema de caché para reducir llamadas API
- ✅ Logging de auditoría para seguimiento
- ✅ Límites de tamaño de archivo (50MB)
- ✅ Sanitización de datos de entrada

#### En Desarrollo
- 🔄 Encriptación de secrets en reposo
- 🔄 Rate limiting avanzado
- 🔄 Autenticación de usuarios
- 🔄 Cifrado end-to-end

### 📊 Capacidades de Análisis

#### Análisis de Sentimientos
- **Clasificación**: Positivo, Neutral, Negativo
- **Confianza**: Score de 0 a 1
- **Emociones**: Alegría, Enojo, Tristeza, Miedo, Sorpresa
- **Intensidad**: Gradación del sentimiento

#### Detección de Patrones
- **Temas automáticos**: Identificación sin supervisión
- **Categorías predefinidas**:
  - Velocidad/Lentitud
  - Interrupciones del servicio
  - Atención al cliente
  - Precios y tarifas
  - Cobertura
  - Instalación

#### Métricas de Negocio
- **NPS** (Net Promoter Score)
- **CSAT** (Customer Satisfaction)
- **Análisis de tendencias temporales**
- **Segmentación de clientes**
- **Predicción de churn** (experimental)

### 🎯 Casos de Uso Empresariales

1. **Servicio al Cliente**
   - Identificar quejas recurrentes
   - Priorizar tickets por sentimiento
   - Detectar clientes en riesgo

2. **Marketing**
   - Medir impacto de campañas
   - Análisis de percepción de marca
   - Segmentación por sentimiento

3. **Producto**
   - Identificar features solicitados
   - Priorizar mejoras
   - Detectar problemas de calidad

4. **Ejecutivo**
   - Dashboards de satisfacción
   - KPIs en tiempo real
   - Reportes automatizados

### 📈 Formato de Salida - Reporte Excel

El reporte Excel generado contiene:

| Hoja | Contenido |
|------|-----------|
| **Resumen Ejecutivo** | KPIs principales, métricas de calidad |
| **Resumen** | Distribución de sentimientos |
| **Comentarios Completos** | Todos los comentarios con análisis |
| **Análisis de Temas** | Temas detectados y frecuencias |
| **Matriz de Puntos Críticos** | Problemas prioritarios |
| **Validación IA** | Métricas de calidad del análisis |
| **Datos para Gráficos** | Datos para visualización |

### 🔄 Pipeline de Procesamiento

```python
# 1. Carga de datos
archivo → validación → limpieza

# 2. Preprocesamiento
normalización → corrección ortográfica → deduplicación

# 3. Análisis
sentimientos → emociones → temas → patrones

# 4. Validación IA
AI Overseer → validación de calidad → correcciones

# 5. Generación de reportes
métricas → visualizaciones → Excel → descarga
```

### 🧪 Testing y Calidad

```bash
# Ejecutar todas las pruebas
pytest tests/

# Pruebas con cobertura
pytest --cov=src tests/

# Pruebas específicas
pytest tests/test_sentiment_analysis.py

# Análisis de seguridad
./security-check.sh
```

### 🚦 Monitoreo y Performance

#### Métricas Clave
- **Tiempo de respuesta**: < 2s para 100 comentarios
- **Uso de memoria**: < 512MB típico
- **Cache hit rate**: > 80% en uso normal
- **API calls**: Optimizado con batching

#### Límites del Sistema
- Máximo archivo: 50MB
- Máximo comentarios: 50,000 por sesión
- Rate limit API: 60 llamadas/minuto
- Timeout de sesión: 30 minutos

### 🔮 Roadmap Futuro

#### Corto Plazo (1-2 meses)
- [ ] Soporte para Guaraní
- [ ] API REST para integraciones
- [ ] Dashboard en tiempo real
- [ ] Exportación a PowerBI

#### Mediano Plazo (3-6 meses)
- [ ] Machine Learning local
- [ ] Análisis predictivo
- [ ] Multi-tenancy
- [ ] Integración CRM

#### Largo Plazo (6-12 meses)
- [ ] Análisis de voz
- [ ] Procesamiento en edge
- [ ] IA generativa para respuestas
- [ ] Plataforma SaaS completa

### 📞 Soporte y Contacto

**Para asistencia técnica:**
- Email: soporte@personalparaguay.com.py
- Issues: [GitHub Issues](https://github.com/aiwhispererwvdp/Comment-Analizer/issues)
- Documentación: [Centro de Documentación](./documentation/README.md)

### 📄 Licencia

Software Propietario - Personal Paraguay (Núcleo S.A.)  
Todos los derechos reservados © 2025

---

**Versión**: 1.0.0  
**Última Actualización**: Agosto 2025  
**Estado**: Producción

Desarrollado con ❤️ para mejorar la experiencia del cliente a través de insights basados en datos.