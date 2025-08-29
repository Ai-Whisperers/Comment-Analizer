# Analizador de Comentarios - Personal Paraguay

Sistema avanzado de análisis de sentimientos y detección de patrones para comentarios de clientes sobre servicios de fibra óptica. Desarrollado para Personal Paraguay (Núcleo S.A.).

---

## ⚡ INICIO RÁPIDO - FUNCIONANDO EN 3 MINUTOS

### 🎯 **SUPER FÁCIL - UN SOLO CLIC** (Windows)

Para usuarios que quieren la experiencia más simple posible:

1. **Descarga el proyecto** completo
2. **Doble clic en** `START_HERE.bat`
3. **Sigue las instrucciones** en pantalla
4. **¡Listo!** - El navegador se abrirá automáticamente

> 💡 **¿Qué hace automáticamente?**
> - Instala Python si no lo tienes
> - Instala todas las dependencias necesarias
> - Te ayuda a configurar tu clave API de OpenAI
> - Inicia la aplicación en tu navegador

### 📋 Requisitos Mínimos
- **Windows 10 o superior** (para el método de 1 clic)
- **Clave API de OpenAI** con créditos disponibles ([Obtenerla aquí](https://platform.openai.com/api-keys))
- **50MB+ de espacio** en disco disponible
- **Navegador web moderno** (Chrome, Firefox, Edge)

### 🚀 Métodos de Instalación

#### 🪟 **Método 1: Ultra Fácil (Windows)** ⭐ RECOMENDADO
```batch
# Simplemente hacer doble clic:
START_HERE.bat
```

#### 🪟 **Método 2: Scripts Bootstrap (Windows)**
```powershell
# PowerShell (Más funciones)
.\bootstrap.ps1

# O usando Command Prompt
.\bootstrap.bat
```

#### 🐧 **Método 3: Tradicional (Linux/Mac/Windows)**
```bash
# Instalar dependencias manualmente
pip install -r requirements.txt
python run.py
```

#### ⚙️ **Configuración Manual** (Si no usas bootstrap)
1. **Instalar Dependencias**
```bash
pip install -r requirements.txt
```

2. **Configurar Entorno** - Crear archivo `.env`:
```env
# REQUERIDO: Tu clave API real de OpenAI
OPENAI_API_KEY=sk-proj-TU-CLAVE-API-REAL-AQUI

# CONFIGURACIÓN OPTIMIZADA
OPENAI_MODEL=gpt-4
OPENAI_MAX_TOKENS=2000
OPENAI_TEMPERATURE=0.7
STREAMLIT_PORT=8501
LOG_LEVEL=INFO
```

3. **Lanzar Aplicación**
```bash
python run.py
```

**Acceder en:** http://localhost:8501

### 🧪 Prueba Rápida (30 segundos)
1. Crear archivo `test_data.xlsx` con los datos de ejemplo (ver sección abajo)
2. Subir archivo en la interfaz web
3. Hacer clic en "🚀 Análisis Rápido"
4. Verificar que aparezcan gráficos de sentimientos y métricas

**✅ Éxito**: Si ves gráficos coloridos y métricas de sentimientos, ¡todo está listo!

---

## 🛠️ NOVEDADES Y MEJORAS

### 🎉 **Nuevas Características v2.0 - Experiencia Sin Código**
- ✅ **START_HERE.bat**: Launcher de 1 clic para usuarios no técnicos
- ✅ **Instalación Automática de Python**: Detecta y descarga Python automáticamente
- ✅ **Configuración Guiada de API**: Asistente interactivo para clave OpenAI
- ✅ **Scripts Bootstrap Mejorados**: `bootstrap.ps1` y `bootstrap.bat` completamente automatizados
- ✅ **Mensajes de Error Amigables**: Explicaciones claras en español, no jerga técnica
- ✅ **Múltiples Métodos de Fallback**: Si un método falla, prueba automáticamente otros
- ✅ **Validación Inteligente**: Verifica cada paso antes de continuar
- ✅ **Interface Visual Mejorada**: Experiencia profesional con indicadores de progreso

### 📊 **Mejoras en Análisis**
- ✅ **Análisis de Emociones Avanzado**: Detección de hasta 15+ emociones diferentes
- ✅ **Temas Inteligentes**: Categorización automática con IA para telecomunicaciones
- ✅ **Exportes Profesionales**: Reportes listos para presentación ejecutiva
- ✅ **Cache Inteligente**: Optimización de velocidad y reducción de costos API

---

## 📦 LISTA DE VERIFICACIÓN PARA TESTERS

### ✅ ANTES DE COMPARTIR CON TESTERS

#### Archivos Críticos Requeridos:
- [ ] **`START_HERE.bat`** - Launcher de 1 clic para usuarios (NUEVO v2.0)
- [ ] **`bootstrap.ps1`** - Script PowerShell automático para Windows (MEJORADO v2.0)
- [ ] **`bootstrap.bat`** - Script CMD automático para Windows (MEJORADO v2.0)
- [ ] **`run.py`** - Lanzador de aplicación con mejor UX (MEJORADO)
- [ ] **`requirements.txt`** - Todas las dependencias listadas
- [ ] **`README.md`** - Esta guía completa (ACTUALIZADA)
- [ ] **`src/`** - Directorio completo del código fuente
- [ ] **`test_data.xlsx`** - Archivo de datos de muestra para pruebas
- [ ] **`.env`** - Con clave API real de OpenAI (se crea automáticamente)

#### Verificación de API Key:
- [ ] Reemplazaste `TU-CLAVE-API-REAL-AQUI` con clave real
- [ ] La clave empieza con `sk-proj-` o `sk-`
- [ ] Verificaste que la clave tiene créditos suficientes ($5+ recomendado)
- [ ] Probaste localmente - la aplicación inicia sin errores

#### Comandos de Verificación:

**🪟 Windows (Automático):**
```powershell
# PowerShell - Incluye verificación automática
.\bootstrap.ps1

# Command Prompt - Incluye verificación automática  
bootstrap.bat
```

**🐧 Linux/Mac (Manual):**
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

**🪟 Método START_HERE.bat (Recomendado):**
- **"No funciona el doble clic"** → Hacer clic derecho → "Ejecutar como administrador"
- **"Scripts bloqueados"** → Si PowerShell falla, automáticamente prueba Command Prompt
- **"Descarga lenta"** → El sistema descarga Python automáticamente, puede tomar 5-10 minutos

**🪟 Métodos Bootstrap Avanzados:**
- **"Scripts deshabilitados"** → `START_HERE.bat` maneja esto automáticamente
- **"Python no reconocido"** → Los scripts instalan Python automáticamente (Windows 10+)
- **Bootstrap falla** → Usar `START_HERE.bat` que prueba múltiples métodos

**🔑 Configuración de API:**
- **"Clave API inválida"** → Los scripts validan que empiece con `sk-` y tenga longitud correcta
- **"No tengo clave API"** → El sistema te guía a https://platform.openai.com/api-keys
- **"Archivo .env no existe"** → Se crea automáticamente durante la configuración guiada

**🌐 Problemas Generales:**
- **"Port 8501 already in use"** → El sistema detecta automáticamente puertos disponibles
- **"ModuleNotFoundError"** → Los bootstrap instalan todas las dependencias automáticamente
- **Errores de análisis** → Verificar formato de datos y columnas requeridas (ver sección abajo)

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
**Última Actualización**: 29 de Agosto, 2025  
**Tecnología Principal**: Streamlit + Python 3.11+  
**Integración IA**: OpenAI GPT-4  
**Puerto Predeterminado**: 8501 (configurable vía STREAMLIT_PORT)  
**Soporte Windows**: Scripts Bootstrap PowerShell y CMD

### Arquitectura del Sistema

```
Comment-Analizer/
├── src/                    # Código fuente principal
│   ├── main.py            # Punto de entrada Streamlit
│   ├── config.py          # Configuración del sistema
│   ├── ai_overseer.py     # Validador de IA
│   ├── i18n/              # Sistema multi-idioma mejorado
│   │   └── translations.py# Soporte ES/EN/PT/GN expandido
│   ├── professional_excel_export.py # Exportación avanzada
│   ├── api/               # Integraciones API
│   ├── components/        # Componentes UI
│   ├── services/          # Lógica de negocio
│   ├── sentiment_analysis/# Motores de análisis
│   ├── data_processing/   # Procesamiento de datos
│   ├── utils/             # Utilidades compartidas
│   └── theme/             # Sistema de temas UI
├── tests/                  # Suite de pruebas (92+ tests)
├── documentation/          # Documentación técnica
├── bootstrap.ps1           # 🪟 Script PowerShell (NUEVO)
├── bootstrap.bat           # 🪟 Script Command Prompt (NUEVO)
├── requirements.txt        # Dependencias Python
├── run.py                 # Lanzador de aplicación
└── .env                   # Configuración (crear manualmente)
```

---

## 🎯 CARACTERÍSTICAS PRINCIPALES

### Capacidades Actuales
- ✅ **Análisis de sentimientos** (Español/Guaraní/Inglés/Portugués)
- ✅ **Insights potenciados por IA** con GPT-4
- ✅ **Detección de patrones** y análisis de tendencias
- ✅ **Exportación profesional** a Excel (16 hojas especializadas)
- ✅ **Visualizaciones interactivas** con Plotly
- ✅ **Procesamiento por lotes** de grandes volúmenes
- ✅ **Cache inteligente** para optimización de API
- ✅ **Modo oscuro/claro** personalizable
- ✅ **Bootstrap automático** para Windows (PowerShell + CMD)
- ✅ **Configuración inteligente** de entorno multiplataforma

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
**Última actualización**: 29 de Agosto, 2025  

---

### 🆕 **CHANGELOG v2.0**
- **NUEVO**: Scripts bootstrap para Windows (`bootstrap.ps1`, `bootstrap.bat`)
- **MEJORADO**: Sistema de traducciones expandido (ES/EN/PT/GN)  
- **MEJORADO**: Exportación Excel profesional con 16 hojas especializadas
- **MEJORADO**: Detección automática y configuración de entorno Windows
- **OPTIMIZADO**: Rendimiento general y experiencia de usuario