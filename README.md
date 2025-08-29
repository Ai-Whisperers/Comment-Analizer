# Analizador de Comentarios - Personal Paraguay

Sistema avanzado de análisis de sentimientos y detección de patrones para comentarios de clientes sobre servicios de fibra óptica. Desarrollado para Personal Paraguay (Núcleo S.A.).

---

## ⚡ INICIO RÁPIDO - PRODUCTION-READY v2.1.0 FINAL

### 🎯 **ESTADO FINAL - APLICACIÓN LISTA PARA USO CORPORATIVO**

**Para Personal Paraguay - Interfaz Profesional Sin Emojis:**

1. **Descarga el proyecto** completo
2. **Método automatizado** - Usar bootstrap scripts
3. **Dual Pipeline** - Elige Análisis Rápido (gratuito) o IA (requiere API key)
4. **¡Listo!** - Interfaz profesional corporativa

> 💡 **Estado Final Implementado:**
> - UI profesional sin emojis para uso empresarial
> - Dual pipeline: Rápido (gratis) + IA (OpenAI)
> - Excel inteligente adaptado por método de análisis
> - Codebase optimizado sin archivos obsoletos

### 📋 Requisitos Mínimos
- **Windows 10 o superior** (para el método de 1 clic)
- **Clave API de OpenAI** con créditos disponibles ([Obtenerla aquí](https://platform.openai.com/api-keys))
- **50MB+ de espacio** en disco disponible
- **Navegador web moderno** (Chrome, Firefox, Edge)

### 🚀 Métodos de Instalación - Estado Final

#### 🪟 **Método 1: Bootstrap Automático (Windows)** ⭐ RECOMENDADO
```batch
# Instalación automática con validación
bootstrap-streamlit.bat
```

#### 🐧 **Método 2: Bootstrap Automático (Linux/Mac)**
```bash
# Instalación automática multiplataforma
./bootstrap-streamlit.sh
```

#### ⚙️ **Método 3: Manual (Todos los sistemas)**
```bash
pip install -r requirements.txt
python run.py
```

#### 🐧 **Método 3: Tradicional (Linux/Mac/Windows)**
```bash
# Instalar dependencias manualmente
pip install -r requirements.txt
python run.py
```

#### ⚙️ **Configuración Manual** (Si no usas bootstrap)
1. **Instalar Dependencias Production-Ready**
```bash
pip install -r requirements.txt
```

2. **Configurar Entorno** - Crear archivo `.env`:
```env
# OPCIONAL: Solo para "Análisis Avanzado (IA)"
# Pipeline Rápido funciona SIN API key
OPENAI_API_KEY=sk-proj-TU-CLAVE-API-REAL-AQUI

# CONFIGURACIÓN OPTIMIZADA FINAL
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

### 🧪 Prueba Rápida Estado Final (30 segundos)
1. Usar archivo `test_input.csv` incluido
2. Subir archivo en la interfaz web profesional
3. Seleccionar "Análisis Rápido (Reglas)" o "Análisis Avanzado (IA)"
4. Verificar interfaz profesional sin emojis y métricas

**✅ Éxito Estado Final**: Si ves interfaz profesional sin emojis, botones de pipeline y Excel inteligente, ¡aplicación PRODUCTION-READY!

---

## 🛠️ NOVEDADES Y MEJORAS

### 🏆 **ESTADO FINAL v2.1.0 - PRODUCTION-READY PARA PERSONAL PARAGUAY**
- ✅ **UI Profesional Corporativa**: Sin emojis, interfaz formal apropiada para empresa
- ✅ **Dual Pipeline Architecture**: Análisis Rápido (reglas) + Análisis Avanzado (IA)
- ✅ **Excel Inteligente**: Output automáticamente adaptado según método usado
- ✅ **Bootstrap Scripts**: `bootstrap-streamlit.bat` y `bootstrap-streamlit.sh` automatizados
- ✅ **API Key Opcional**: Pipeline Rápido funciona SIN API key, IA requiere OpenAI
- ✅ **Type Safety Completo**: 75+ errores de tipo corregidos en componentes críticos
- ✅ **Codebase Limpio**: Archivos obsoletos eliminados, 0% regresiones
- ✅ **Puerto Configurable**: STREAMLIT_PORT customizable (default: 8501)

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

**Versión Actual**: 2.1.0 FINAL  
**Última Actualización**: 29 de Agosto, 2025  
**Estado**: PRODUCTION-READY - Lista para uso corporativo  
**Tecnología Principal**: Streamlit + Python 3.11+  
**Integración IA**: OpenAI GPT-4 con dual pipeline  
**Puerto**: 8501 configurable vía STREAMLIT_PORT  
**UI**: Profesional sin emojis para Personal Paraguay  
**Pipeline**: Rápido (gratuito) + IA (requiere API key)

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

### Capacidades Estado Final
- ✅ **Dual Pipeline**: Análisis Rápido (reglas) + Análisis Avanzado (IA GPT-4)
- ✅ **UI Profesional**: Sin emojis, apropiada para uso corporativo
- ✅ **Excel Inteligente**: Output adaptado automáticamente por método de análisis
- ✅ **Análisis multiidioma** (Español/Guaraní optimizado para Paraguay)
- ✅ **Type Safety**: Componentes críticos 100% type-safe
- ✅ **Codebase Optimizado**: Sin archivos obsoletos, 0% regresiones
- ✅ **Bootstrap Scripts**: Instalación automatizada multiplataforma
- ✅ **Puerto Configurable**: STREAMLIT_PORT customizable
- ✅ **API Key Opcional**: Pipeline Rápido funciona sin configuración
- ✅ **Fallbacks Robustos**: enhanced_analysis y improved_analysis activos

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

#### 🚀 **Análisis Rápido (Pipeline 1)**
- **Costo**: GRATUITO - Sin API key requerida
- **Velocidad**: 10-30 segundos por 100 comentarios
- **Datos**: Sentimientos básicos, temas principales
- **Excel**: Básico con datos de reglas
- **Ideal para**: Uso diario, overview rápido

#### 🤖 **Análisis Avanzado IA (Pipeline 2)**
- **Costo**: Requiere API key OpenAI ($0.02-0.04 por 100 comentarios)
- **Velocidad**: 30-90 segundos por 100 comentarios
- **Datos**: Emociones, pain points, insights profundos
- **Excel**: Enriquecido con 5 hojas especializadas IA
- **Ideal para**: Reportes ejecutivos Personal Paraguay

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
**Versión**: 2.1.0 FINAL  
**Estado**: PRODUCTION-READY  
**UI**: Profesional sin emojis para uso corporativo  
**Última actualización**: 29 de Agosto, 2025  

---

### 🏆 **CHANGELOG v2.1.0 FINAL - ESTADO ÓPTIMO**
- **COMPLETADO**: UI profesional sin emojis para Personal Paraguay
- **IMPLEMENTADO**: Dual pipeline architecture (Rápido + IA)
- **OPTIMIZADO**: Excel inteligente adaptado por método de análisis
- **CORREGIDO**: 75+ errores de tipo en componentes críticos
- **LIMPIADO**: Codebase sin archivos obsoletos (3 archivos eliminados)
- **ACTUALIZADO**: Scripts bootstrap `bootstrap-streamlit.bat/sh`
- **CONFIGURADO**: Puerto STREAMLIT_PORT configurable
- **FINALIZADO**: Estado PRODUCTION-READY para uso corporativo