# Analizador de Comentarios - Personal Paraguay

Sistema avanzado de análisis de sentimientos y detección de patrones para comentarios de clientes sobre servicios de fibra óptica. Desarrollado para Personal Paraguay (Núcleo S.A.).

---

## ⚡ INICIO RÁPIDO - FUNCIONANDO EN 3 MINUTOS

### 📋 Requisitos Previos
- Python 3.11 o superior instalado
- Clave API de OpenAI con créditos disponibles
- 5MB+ de espacio en disco disponible
- Navegador web moderno (Chrome, Firefox, Edge)

### 🚀 Instalación Rápida (3 Pasos)

#### Paso 1: Instalar Dependencias
```bash
pip install -r requirements.txt
```

#### Paso 2: Configurar Entorno
Crear archivo `.env` en el directorio raíz:
```env
# REQUERIDO: Tu clave API real de OpenAI
OPENAI_API_KEY=sk-proj-TU-CLAVE-API-REAL-AQUI

# CONFIGURACIÓN OPTIMIZADA PARA USO INMEDIATO
OPENAI_MODEL=gpt-4
OPENAI_MAX_TOKENS=2000
OPENAI_TEMPERATURE=0.7
STREAMLIT_PORT=8501
LOG_LEVEL=INFO
```

#### Paso 3: Lanzar Aplicación
```bash
python run.py
```
Luego abrir: **http://localhost:8501**

### 🧪 Prueba Rápida (30 segundos)
1. Crear archivo `test_data.xlsx` con los datos de ejemplo (ver sección abajo)
2. Subir archivo en la interfaz web
3. Hacer clic en "🚀 Análisis Rápido"
4. Verificar que aparezcan gráficos de sentimientos y métricas

**✅ Éxito**: Si ves gráficos coloridos y métricas de sentimientos, ¡todo está listo!

---

## 📦 LISTA DE VERIFICACIÓN PARA TESTERS

### ✅ ANTES DE COMPARTIR CON TESTERS

#### Archivos Críticos Requeridos:
- [ ] **`.env`** - Con clave API real de OpenAI (no placeholder)
- [ ] **`README.md`** - Esta guía completa
- [ ] **`requirements.txt`** - Todas las dependencias listadas
- [ ] **`run.py`** - Lanzador de aplicación
- [ ] **`src/`** - Directorio completo del código fuente
- [ ] **`test_data.xlsx`** - Archivo de datos de muestra para pruebas

#### Verificación de API Key:
- [ ] Reemplazaste `TU-CLAVE-API-REAL-AQUI` con clave real
- [ ] La clave empieza con `sk-proj-` o `sk-`
- [ ] Verificaste que la clave tiene créditos suficientes ($5+ recomendado)
- [ ] Probaste localmente - la aplicación inicia sin errores

#### Comandos de Verificación:
```bash
# Verificación rápida de configuración
python -c "from src.config import Config; print('✅ API configurada' if Config.OPENAI_API_KEY else '❌ API faltante')"

# Debe iniciar sin errores
python run.py  
```

### 🎯 CASOS DE PRUEBA PARA TESTERS

1. **✅ Inicio Básico**: La aplicación se lanza y carga la interfaz
2. **✅ Carga de Archivos**: Acepta archivos Excel/CSV, muestra vista previa
3. **✅ Análisis**: Procesa datos, muestra gráficos de sentimientos (30-60 segundos)
4. **✅ Exportación**: Genera reporte Excel descargable

#### Resultados Esperados:
- **Tiempo de instalación**: 2-3 minutos
- **Primer análisis exitoso**: Menos de 5 minutos
- **Archivo de muestra (50 comentarios)**: 30-60 segundos de procesamiento
- **Costo API**: ~$0.02-0.04 USD por prueba

### ⚠️ Problemas Comunes y Soluciones
- **"OPENAI_API_KEY not found"** → Verificar que existe archivo `.env` en directorio raíz
- **"Port 8501 already in use"** → Ejecutar: `streamlit run src/main.py --server.port 8502`
- **"ModuleNotFoundError"** → Ejecutar: `pip install -r requirements.txt`
- **Errores de análisis** → Verificar formato de datos y columnas requeridas

---

## 📊 FORMATO DE DATOS DE ENTRADA

### Estructura del Archivo Excel

El sistema está optimizado para procesar archivos Excel con comentarios de clientes.

#### Columnas Principales

| Nombre de Columna | Tipo de Dato | Obligatorio | Descripción | Ejemplo |
|-------------------|--------------|-------------|-------------|---------|
| **Comentario Final** | Texto | ✅ Sí | Comentario del cliente | "Excelente servicio, muy rápido" |
| **Fecha** | Fecha/Hora | ⚪ No | Fecha del comentario | 27/12/2024 |
| **Nota** | Número (1-10) | ⚪ No | Calificación numérica | 8 |
| **NPS** | Texto | ⚪ No | Categoría NPS | "Promotor" |
| **ID Cliente** | Texto/Número | ⚪ No | Identificador único | "C12345" |
| **Región** | Texto | ⚪ No | Ubicación geográfica | "Asunción" |

### Archivo de Prueba Ejemplo

Crear `test_data.xlsx` con estos datos:

| Comentario Final | Fecha | Nota |
|------------------|-------|------|
| Excelente servicio de Internet, muy rápido | 01/12/2024 | 9 |
| La conexión se corta frecuentemente | 02/12/2024 | 3 |
| Buena atención al cliente, resolvieron rápido | 03/12/2024 | 8 |
| Precio muy alto para el servicio ofrecido | 04/12/2024 | 4 |
| Instalación eficiente, técnicos profesionales | 05/12/2024 | 9 |
| Internet lento durante las noches | 06/12/2024 | 5 |
| Servicio estable, sin problemas | 07/12/2024 | 7 |
| Mala señal en días de lluvia | 08/12/2024 | 4 |
| Soporte técnico muy útil | 09/12/2024 | 8 |
| Velocidad constante, cumple lo prometido | 10/12/2024 | 9 |

#### Nombres de Columna Reconocidos Automáticamente

**Para Comentarios:**
- Comentario Final
- Comentarios
- Observaciones
- Feedback
- Opinión
- Sugerencias

**Para Calificaciones:**
- Nota
- Puntuación
- Rating
- Calificación
- Score

**Para Fechas:**
- Fecha
- Fecha de Registro
- Timestamp
- Fecha_Registro

---

## 🏗️ INFORMACIÓN DEL SISTEMA

### Especificaciones Técnicas

**Versión Actual**: 2.0.0  
**Última Actualización**: 27 de Diciembre, 2024  
**Tecnología Principal**: Streamlit + Python 3.12  
**Integración IA**: OpenAI GPT-4  
**Puerto Predeterminado**: 8501 (configurable vía STREAMLIT_PORT)

### Arquitectura del Sistema

```
Comment-Analizer/
├── src/                    # Código fuente principal
│   ├── main.py            # Punto de entrada Streamlit
│   ├── config.py          # Configuración del sistema
│   ├── ai_overseer.py     # Validador de IA
│   ├── api/               # Integraciones API
│   ├── components/        # Componentes UI
│   ├── services/          # Lógica de negocio
│   ├── sentiment_analysis/# Motores de análisis
│   ├── data_processing/   # Procesamiento de datos
│   ├── utils/             # Utilidades compartidas
│   └── theme/             # Sistema de temas UI
├── tests/                  # Suite de pruebas (92+ tests)
├── documentation/          # Documentación técnica
├── requirements.txt        # Dependencias Python
├── run.py                 # Lanzador de aplicación
└── .env                   # Configuración (crear manualmente)
```

---

## 🎯 CARACTERÍSTICAS PRINCIPALES

### Capacidades Actuales
- ✅ **Análisis de sentimientos** (Español/Guaraní)
- ✅ **Insights potenciados por IA** con GPT-4
- ✅ **Detección de patrones** y análisis de tendencias
- ✅ **Exportación profesional** a Excel
- ✅ **Visualizaciones interactivas** con Plotly
- ✅ **Procesamiento por lotes** de grandes volúmenes
- ✅ **Cache inteligente** para optimización de API
- ✅ **Modo oscuro/claro** personalizable

### Métricas Disponibles
- Distribución de sentimientos (Positivo/Neutral/Negativo)
- Score NPS (Promotores/Neutros/Detractores)
- Temas principales identificados
- Análisis temporal de tendencias
- Palabras clave frecuentes
- Patrones de problemas recurrentes
- Recomendaciones basadas en IA

---

## 📈 USO DE LA APLICACIÓN

### Flujo de Trabajo Típico

1. **Preparar Datos**
   - Asegurar que el Excel tenga columna "Comentario Final"
   - Verificar formato de fechas (DD/MM/YYYY)
   - Incluir calificaciones numéricas si están disponibles

2. **Cargar y Analizar**
   - Subir archivo Excel/CSV vía interfaz
   - Seleccionar tipo de análisis (Rápido/Completo)
   - Esperar procesamiento (1-2 min por 100 comentarios)

3. **Revisar Resultados**
   - Explorar dashboard interactivo
   - Filtrar por sentimiento/fecha/categoría
   - Identificar insights clave y patrones

4. **Exportar Reportes**
   - Descargar Excel con análisis completo
   - Generar PDF para presentaciones
   - Exportar gráficos como imágenes

### Opciones de Análisis

#### 🚀 **Análisis Rápido**
- Procesamiento básico de sentimientos
- Métricas esenciales
- Ideal para revisiones diarias
- Tiempo: ~30 seg por 100 comentarios

#### 🔬 **Análisis Completo con IA**
- Análisis profundo con GPT-4
- Detección avanzada de patrones
- Recomendaciones estratégicas
- Insights de negocio detallados
- Tiempo: 2-3 min por 100 comentarios
- Costo estimado: $0.10-0.20 USD por 100 comentarios

---

## 🐳 INSTALACIÓN CON DOCKER

### Opción Rápida con Docker

```bash
# Construir imagen
docker build -t comment-analyzer .

# Ejecutar contenedor
docker run -p 8501:8501 \
  -e OPENAI_API_KEY=tu-clave-api \
  comment-analyzer
```

### Docker Compose (Producción)

```yaml
# docker-compose.yml
version: '3.8'
services:
  analyzer:
    build: .
    ports:
      - "8501:8501"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./data:/app/data
      - ./outputs:/app/outputs
    restart: unless-stopped
```

Ejecutar con:
```bash
docker-compose up -d
```

---

## 🔧 CONFIGURACIÓN AVANZADA

### Variables de Entorno Completas

```env
# === API CONFIGURATION ===
OPENAI_API_KEY=sk-proj-xxx              # Requerido
OPENAI_MODEL=gpt-4                      # Modelo a usar
OPENAI_MAX_TOKENS=2000                  # Límite de tokens
OPENAI_TEMPERATURE=0.7                  # Creatividad (0-1)
OPENAI_TIMEOUT=60                       # Timeout en segundos

# === APPLICATION SETTINGS ===
APP_ENV=production                      # production/testing/development
STREAMLIT_PORT=8501                     # Puerto de la aplicación
LOG_LEVEL=INFO                          # DEBUG/INFO/WARNING/ERROR
DEBUG_MODE=False                        # Modo debug

# === PERFORMANCE TUNING ===
MAX_FILE_SIZE_MB=10                     # Tamaño máximo de archivo
MAX_COMMENTS_PER_BATCH=100              # Comentarios por lote
CACHE_TTL_SECONDS=3600                  # Duración del cache
ENABLE_CACHE=True                       # Habilitar cache

# === SECURITY ===
ENABLE_RATE_LIMITING=True               # Limitar tasa de peticiones
MAX_REQUESTS_PER_MINUTE=60              # Peticiones por minuto
SECURE_HEADERS=True                     # Headers de seguridad
```

---

## 🧪 PRUEBAS Y VALIDACIÓN

### Ejecutar Suite de Pruebas

```bash
# Todas las pruebas
pytest tests/

# Con cobertura
pytest --cov=src tests/

# Pruebas específicas
pytest tests/test_sentiment_analysis.py
```

### Validación de Configuración

```bash
# Verificar instalación
python verify_setup.py

# Verificar imports
python verify_imports.py

# Test de integración IA
python test_ai_integration.py
```

---

## 📚 DOCUMENTACIÓN ADICIONAL

### Guías Técnicas Disponibles

Para documentación técnica detallada, consultar la carpeta `documentation/`:

- **Guías de Usuario**: `documentation/guides/USER_GUIDE.md`
- **Arquitectura**: `documentation/architecture/`
- **Instalación Detallada**: `documentation/deployment/INSTALLATION.md`
- **Configuración API**: `documentation/guides/AI_INTEGRATION_COMPLETE_GUIDE.md`
- **Solución de Problemas**: `documentation/guides/CRITICAL_FIXES_QUICKSTART.md`

---

## 🆘 SOPORTE Y RECURSOS

### Recursos Internos
- **Logs de error**: `/logs/comment_analyzer_*.log`
- **Health check**: `http://localhost:8501/_stcore/health`
- **Suite de pruebas**: `pytest tests/`
- **Verificación**: `python verify_setup.py`

### Solución Rápida de Problemas

| Problema | Solución |
|----------|----------|
| API key no funciona | Verificar formato: `sk-proj-...` y créditos disponibles |
| Aplicación no inicia | Revisar puerto 8501 libre, reinstalar dependencias |
| Error de análisis | Verificar formato Excel, columna "Comentario Final" |
| Resultados vacíos | Revisar que haya comentarios no vacíos |
| Exportación falla | Verificar permisos de escritura en `/outputs` |

### Contacto y Soporte
- **Logs detallados**: Revisar `/logs/` para errores específicos
- **Configuración**: Verificar archivo `.env` está completo
- **Dependencias**: Ejecutar `pip install --upgrade -r requirements.txt`

---

## 📊 ESTIMACIÓN DE COSTOS

### Uso de API OpenAI

| Volumen de Comentarios | Tiempo Estimado | Costo Aproximado |
|------------------------|-----------------|------------------|
| 50 comentarios | 30-60 segundos | $0.02-0.04 USD |
| 100 comentarios | 1-2 minutos | $0.05-0.10 USD |
| 500 comentarios | 5-8 minutos | $0.25-0.50 USD |
| 1000 comentarios | 10-15 minutos | $0.50-1.00 USD |

---

## ✅ CHECKLIST FINAL ANTES DE DESPLIEGUE

### Para Producción
- [ ] API Key configurada y con créditos
- [ ] Archivo `.env` completo y seguro
- [ ] Pruebas ejecutadas exitosamente
- [ ] Logs configurados correctamente
- [ ] Backups de datos configurados
- [ ] SSL/HTTPS habilitado (si aplica)
- [ ] Rate limiting configurado
- [ ] Monitoreo activo

### Para Testers
- [ ] Instrucciones claras en español
- [ ] Datos de prueba incluidos
- [ ] Casos de prueba documentados
- [ ] Información de contacto para soporte
- [ ] Estimación de costos comunicada

---

**Sistema desarrollado para**: Personal Paraguay (Núcleo S.A.)  
**Versión**: 2.0.0  
**Última actualización**: 27 de Diciembre, 2024