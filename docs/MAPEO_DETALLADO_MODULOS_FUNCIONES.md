# 🗂️ MAPEO DETALLADO: Módulos y Funciones

## 📋 ÍNDICE DE NAVEGACIÓN RÁPIDA
- [PUNTO DE ENTRADA](#punto-de-entrada)
- [PÁGINAS STREAMLIT](#páginas-streamlit)
- [COMPONENTES UI](#componentes-ui)
- [CAPA DE APLICACIÓN](#capa-de-aplicación)
- [CAPA DE DOMINIO](#capa-de-dominio)
- [CAPA DE INFRAESTRUCTURA](#capa-de-infraestructura)
- [UTILIDADES COMPARTIDAS](#utilidades-compartidas)

---

## 🚀 PUNTO DE ENTRADA

### **`streamlit_app.py`** - Inicializador principal
```python
├── _validate_and_log_deployment_config(config) : bool
│   └── Valida configuración y logs de deployment
├── _load_enhanced_fallback_css() : bool  
│   └── CSS fallback para glassmorphism
└── MAIN EXECUTION
    ├── Líneas 122-130: Setup sys.path imports
    ├── Líneas 143-200: Inicialización Clean Architecture
    └── Líneas 200-250: Setup Streamlit config
```

**Variables de Session State creadas:**
- `st.session_state.contenedor` → ContenedorDependencias
- `st.session_state.caso_uso_maestro` → AnalizarExcelMaestroCasoUso  
- `st.session_state.ai_config_manager` → AIConfigurationManager
- `st.session_state.ai_configuration` → AIConfiguration

---

## 📱 PÁGINAS STREAMLIT

### **`pages/1_Página_Principal.py`** - Dashboard principal
```python
├── show_app_info() : None
│   └── Información de la aplicación y arquitectura
├── show_performance_metrics() : None
│   └── Métricas de rendimiento del sistema
└── show_usage_instructions() : None
    └── Instrucciones de uso
```

### **`pages/2_Subir.py`** - ⭐ PÁGINA PRINCIPAL DE ANÁLISIS
```python
├── IMPORTS Y SETUP (líneas 1-100)
│   ├── Importación constantes AI
│   ├── CSS enhanced loader
│   └── Fallback implementations
│
├── _cleanup_previous_analysis() : None (línea 150)
│   └── Limpieza memoria análisis previos
│
├── live_batch_progress() : None (línea 99)
│   └── Progress tracking en tiempo real (Fragment)
│
├── _run_analysis(uploaded_file, analysis_type) : None (línea 200)
│   ├── Obtiene caso_uso_maestro del session_state
│   ├── Crea ComandoAnalisisExcelMaestro
│   ├── LÍNEA 228-242: Setup progress tracker UI
│   ├── LÍNEA 239: 🔥 EJECUCIÓN PRINCIPAL → caso_uso_maestro.ejecutar()
│   ├── LÍNEA 244-270: Procesamiento resultados exitosos
│   └── LÍNEA 250-280: Manejo de errores
│
└── MAIN UI (líneas 300-500)
    ├── File uploader
    ├── Progress tracking display  
    └── Results visualization
```

### **`pages/3_Analisis_Optimizada.py`** - Análisis optimizado
```python
├── display_analysis_results() : None
│   └── Visualización resultados optimizada
├── create_performance_charts() : None
│   └── Gráficos de rendimiento
└── export_results() : None
    └── Exportación de resultados
```

---

## 🎨 COMPONENTES UI

### **`components/progress_tracker.py`** - Sistema de progreso
```python
├── show_batch_progress(total_batches, current_batch, elapsed_time) : None
│   └── @st.fragment - Progress de lotes optimizados
│
├── auto_update_analysis_progress() : None  
│   └── @st.fragment(run_every=1) - Auto-refresh progress
│
├── show_ai_analysis_progress() : None
│   └── @st.fragment(run_every=1) - Progress detallado del análisis IA
│
├── start_progress_tracking(total_batches) : None
│   └── Inicialización tracking en session_state
│
├── update_progress(current_batch, status) : None
│   └── Actualización estado progreso
│
├── finish_progress_tracking() : Dict[str, Any]
│   └── Finalización y métricas finales
│
└── show_performance_comparison(current_time, estimated_old_time) : None
    └── @st.fragment - Comparación rendimiento
```

---

## 🎯 CAPA DE APLICACIÓN

### **`src/application/use_cases/analizar_excel_maestro_caso_uso.py`** - ⭐ MOTOR PRINCIPAL

#### **Clase: AnalizarExcelMaestroCasoUso**
```python
├── __init__(lector_archivos, analizador_maestro_ia, repositorio, ai_config_manager)
│   └── Inyección de dependencias principales
│
├── ejecutar(comando: ComandoAnalisisExcelMaestro) : ResultadoAnalisisMaestro
│   ├── 🔥 MÉTODO PRINCIPAL - ORQUESTADOR COMPLETO
│   ├── Líneas 150-170: Validación entrada
│   ├── Líneas 180-200: Lectura comentarios
│   ├── Líneas 210-250: Creación lotes optimizados
│   ├── Líneas 260-400: Procesamiento por lotes
│   ├── Líneas 410-500: Mapeo a entidades dominio
│   └── Líneas 510-550: Persistencia resultados
│
├── _validar_archivo(archivo_cargado) : None
│   └── Validación formato y contenido archivo
│
├── _leer_comentarios(archivo_cargado, nombre_archivo) : List[str]
│   └── Extracción comentarios del archivo
│
├── _crear_lotes_optimizados(comentarios) : List[List[str]]
│   ├── Algoritmo optimización lotes
│   ├── Límites adaptativos por tamaño
│   └── Balance performance vs seguridad
│
├── _procesar_lotes_secuencial(lotes, total_lotes) : List[AnalisisCompletoIA]
│   ├── Procesamiento secuencial optimizado
│   ├── Progress tracking por lote
│   ├── Manejo de errores robusto
│   └── Memory management
│
├── _mapear_a_entidades_dominio(resultados_ia) : List[AnalisisComentario]
│   ├── Conversión IA response → Domain entities
│   ├── Mapeo sentimientos, emociones, temas
│   └── Validación consistency
│
├── _mapear_comentario_individual(comentario_ia_data) : AnalisisComentario
│   └── Mapeo individual comentario
│
├── _mapear_sentimiento_desde_ia(sentiment_data) : Sentimiento
│   └── Conversión formato IA → Value Object
│
├── _mapear_emocion_desde_ia(emotion_data) : Emocion
│   └── Conversión formato IA → Value Object
│
├── _mapear_tema_desde_ia(tema_data) : TemaPrincipal
│   └── Conversión formato IA → Value Object
│
├── _mapear_punto_dolor_desde_ia(dolor_data) : PuntoDolor
│   └── Conversión formato IA → Value Object
│
├── _consolidar_analisis_completo(resultados_individuales) : AnalisisCompletoIA
│   ├── Agregación resultados de lotes
│   ├── Cálculo estadísticas globales
│   └── Generación resumen ejecutivo
│
├── _guardar_en_repositorio(comentarios_analizados) : None
│   └── Persistencia entidades dominio
│
├── _calcular_estadisticas_globales(comentarios) : Dict
│   └── Estadísticas agregadas
│
└── _generar_metricas_performance(inicio, fin, total_comentarios) : Dict
    └── Métricas rendimiento
```

#### **DTOs (Data Transfer Objects)**

**`src/application/dtos/analisis_completo_ia.py`**
```python
├── Class: AnalisisCompletoIA
│   ├── Campos principales:
│   │   ├── total_comentarios: int
│   │   ├── tendencia_general: str  
│   │   ├── comentarios_analizados: List[Dict]
│   │   ├── distribucion_sentimientos: Dict[str, int]
│   │   ├── emociones_predominantes: Dict[str, float]
│   │   ├── confianza_general: float
│   │   └── tiempo_analisis: float
│   │
│   ├── obtener_resumen_ejecutivo_completo() : str
│   ├── obtener_comentarios_por_sentimiento(sentimiento) : List[Dict]
│   ├── obtener_top_emociones(limit=5) : Dict[str, float]
│   ├── obtener_temas_relevantes(threshold=0.3) : Dict[str, float]
│   ├── calcular_score_satisfaccion() : float
│   └── es_tendencia_positiva() : bool
```

**`src/application/dtos/resultado_analisis.py`**
```python
├── Class: ResultadoAnalisis (Legacy - Compatible)
└── Class: ResultadoAnalisisMaestro (Actual)
    ├── exito: bool
    ├── mensaje: str  
    ├── analisis_completo_ia: AnalisisCompletoIA
    ├── comentarios_analizados: List[AnalisisComentario]
    ├── es_exitoso() : bool
    ├── obtener_resumen_ejecutivo() : str
    └── obtener_comentarios_criticos() : List[AnalisisComentario]
```

---

## 🏛️ CAPA DE DOMINIO

### **Entidades (`src/domain/entities/`)**

**`comentario.py`**
```python
├── Class: Comentario
│   ├── id: str
│   ├── contenido: str
│   ├── fecha_creacion: datetime
│   ├── origen: str
│   ├── es_valido() : bool
│   ├── obtener_longitud() : int
│   └── limpiar_contenido() : str
```

**`analisis_comentario.py`** 
```python
├── Class: AnalisisComentario  
│   ├── comentario: Comentario
│   ├── sentimiento: Sentimiento
│   ├── emociones: List[Emocion]
│   ├── temas_principales: List[TemaPrincipal]
│   ├── puntos_dolor: List[PuntoDolor]
│   ├── confianza_analisis: float
│   ├── es_critico() : bool
│   ├── obtener_score_urgencia() : float
│   ├── obtener_resumen() : str
│   └── requiere_atencion_inmediata() : bool
```

### **Value Objects (`src/domain/value_objects/`)**

**`sentimiento.py`**
```python
├── Enum: SentimientoCategoria
│   ├── POSITIVO
│   ├── NEUTRAL  
│   └── NEGATIVO
│
└── Class: Sentimiento
    ├── categoria: SentimientoCategoria
    ├── confianza: float
    ├── intensidad: float
    ├── es_positivo() : bool
    ├── es_negativo() : bool
    ├── es_neutral() : bool
    └── obtener_descripcion() : str
```

**`emocion.py`**
```python
├── Enum: TipoEmocion
│   ├── SATISFACCION, FRUSTRACION, ALEGRIA
│   ├── ENOJO, DECEPCION, PREOCUPACION
│   └── NEUTRAL, ESPERANZA, CONFUSION
│
└── Class: Emocion
    ├── tipo: TipoEmocion
    ├── intensidad: float
    ├── confianza: float
    ├── es_emocion_positiva() : bool
    ├── es_emocion_negativa() : bool
    ├── obtener_color_representativo() : str
    └── clasificar_intensidad() : str
```

**`tema_principal.py`**
```python  
├── Enum: CategoriaTemaTelco
│   ├── VELOCIDAD, PRECIO, SERVICIO_CLIENTE
│   ├── COBERTURA, FACTURACION, CALIDAD_LLAMADA
│   └── INTERNET, PROMOCIONES, SOPORTE_TECNICO
│
└── Class: TemaPrincipal
    ├── categoria: CategoriaTemaTelco
    ├── relevancia: float
    ├── subtemas: List[str]
    ├── obtener_descripcion_completa() : str
    └── es_tema_critico() : bool
```

### **Servicios de Dominio (`src/domain/services/`)**

**`analizador_sentimientos.py`**
```python
├── Interface: IAnalizadorSentimientos
│   ├── analizar_sentimiento(comentario) : Sentimiento
│   └── es_disponible() : bool
│
└── Class: ServicioAnalisisSentimientos
    ├── analizador: IAnalizadorSentimientos
    ├── procesar_comentario(comentario) : AnalisisComentario
    ├── procesar_lote(comentarios) : List[AnalisisComentario]  
    └── validar_confianza(analisis) : bool
```

### **Repositorios (`src/domain/repositories/`)**

**`repositorio_comentarios.py`**
```python
├── Interface: IRepositorioComentarios
│   ├── guardar(comentario) : None
│   ├── obtener_por_id(id) : Comentario
│   ├── obtener_todos() : List[Comentario]
│   ├── buscar_por_sentimiento(sentimiento) : List[Comentario]
│   ├── limpiar_repositorio() : None
│   └── contar_total() : int
```

---

## ⚙️ CAPA DE INFRAESTRUCTURA

### **Servicios Externos - IA (`src/infrastructure/external_services/`)**

#### **`analizador_maestro_ia.py`** - ⭐ MOTOR IA PRINCIPAL

```python
├── Class: AnalizadorMaestroIA
│   ├── __init__(api_key, modelo, usar_cache, temperatura, cache_ttl, max_tokens, ai_configuration)
│   │   ├── Configuración OpenAI client
│   │   ├── Setup cache LRU + TTL
│   │   ├── Configuración determinística
│   │   └── Inicialización retry strategy
│   │
│   ├── 🔥 analizar_excel_completo(comentarios_raw) : AnalisisCompletoIA
│   │   ├── MÉTODO PRINCIPAL DE ANÁLISIS
│   │   ├── Líneas 228-240: Validación entrada
│   │   ├── Líneas 245-280: Límites seguridad adaptativos
│   │   ├── Líneas 290-330: Pipeline análisis con progress tracking
│   │   └── Retorna AnalisisCompletoIA completo
│   │
│   ├── _calcular_tokens_dinamicos(num_comentarios) : int
│   │   ├── Cálculo inteligente tokens basado en contenido
│   │   ├── Aplicación múltiples safety nets
│   │   ├── Límites por modelo (gpt-4, gpt-4o-mini)
│   │   └── ULTIMATE SAFETY: max 60 comentarios
│   │
│   ├── _generar_prompt_maestro(comentarios) : str
│   │   ├── 🔥 GENERACIÓN PROMPT OPTIMIZADO
│   │   ├── Formato JSON estructurado
│   │   ├── Instrucciones específicas telco
│   │   └── Campos abreviados para eficiencia tokens
│   │
│   ├── _hacer_llamada_api_maestra(prompt, num_comentarios) : Dict[str, Any]
│   │   ├── 🔥 COMUNICACIÓN CON OPENAI
│   │   ├── Configuración determinística (temp=0.0, seed=12345)
│   │   ├── Retry strategy inteligente  
│   │   ├── JSON response format forzado
│   │   └── Token usage tracking
│   │
│   ├── _procesar_respuesta_maestra(respuesta, comentarios_originales, tiempo_analisis) : AnalisisCompletoIA
│   │   ├── Parsing JSON response de OpenAI
│   │   ├── Mapeo a estructura AnalisisCompletoIA
│   │   ├── Validación consistency datos
│   │   └── Cálculo métricas agregadas
│   │
│   ├── _extract_emotions_from_comments(comentarios_analizados) : Dict[str, float]
│   │   ├── Extracción y agregación emociones
│   │   ├── Mapeo abreviaciones → nombres completos
│   │   └── Normalización intensidades
│   │
│   ├── Cache Management:
│   │   ├── _generar_cache_key(comentarios) : str
│   │   ├── _verificar_cache_valido(cache_key) : bool  
│   │   ├── _guardar_en_cache(cache_key, analisis) : None
│   │   ├── _cleanup_expired_cache() : None
│   │   └── limpiar_cache() : None
│   │
│   ├── Availability & Stats:
│   │   ├── _verificar_disponibilidad() : bool
│   │   ├── es_disponible() : bool
│   │   ├── obtener_estadisticas_cache() : Dict[str, Any]
│   │   └── _validate_deterministic_config() : bool
│   │
│   └── Async Methods (Streamlit compatible):
│       ├── analizar_batch_async(comentarios_batch) : AnalisisCompletoIA
│       └── analizar_batches_concurrent(batches) : List[AnalisisCompletoIA]
```

#### **`ai_progress_tracker.py`** - Sistema de progreso IA

```python
├── Class: ProgressStep
│   ├── name, description, weight, estimated_duration
│   ├── started_at, completed_at
│   ├── is_started() : bool
│   ├── is_completed() : bool  
│   └── actual_duration() : float
│
├── Class: AIProgressTracker  
│   ├── __init__(comment_count)
│   │   ├── Definición 6 pasos pipeline:
│   │   │   ├── initialization (2%)
│   │   │   ├── cache_check (3%) 
│   │   │   ├── prompt_generation (10%)
│   │   │   ├── openai_api_call (75%) ← CRÍTICO
│   │   │   ├── response_processing (8%)
│   │   │   └── emotion_extraction (2%)
│   │   └── Estimación tiempo inteligente
│   │
│   ├── start_step(step_name) : None
│   │   ├── Marca inicio paso
│   │   ├── Update session_state para UI
│   │   └── Trigger progress callbacks
│   │
│   ├── complete_step(step_name) : None
│   │   ├── Marca finalización paso
│   │   ├── Calcula tiempo real vs estimado
│   │   └── Update UI state
│   │
│   ├── get_current_progress() : Dict[str, Any]
│   │   ├── Cálculo porcentaje progreso
│   │   ├── ETA inteligente  
│   │   ├── Info paso actual
│   │   └── Pipeline stage human-readable
│   │
│   ├── _calculate_estimated_time(comment_count) : float
│   └── _get_pipeline_stage(progress) : str
│
├── Class: ProgressContext
│   ├── Context manager para tracking automático
│   ├── __enter__() / __exit__()
│   └── Exception handling
│
└── Global Functions:
    ├── create_progress_tracker(comment_count) : AIProgressTracker
    ├── get_current_progress() : Optional[Dict[str, Any]]
    ├── track_step(step_name) : ProgressContext
    └── reset_progress_tracker() : None
```

#### **`ai_engine_constants.py`** - Configuración centralizada

```python
├── Class: AIEngineConstants
│   ├── Token Calculation Constants:
│   │   ├── BASE_TOKENS_JSON_STRUCTURE = 1200
│   │   ├── TOKENS_PER_COMMENT = 80
│   │   ├── TOKEN_BUFFER_PERCENTAGE = 1.10
│   │   └── 🔥 SAFETY_COMMENT_LIMIT = 60
│   │
│   ├── Cache Management:
│   │   ├── DEFAULT_CACHE_SIZE = 50
│   │   ├── DEFAULT_CACHE_TTL = 3600
│   │   └── CACHE_CLEANUP_THRESHOLD_RATIO = 1.5
│   │
│   ├── AI Determinism:
│   │   ├── FIXED_SEED = 12345
│   │   └── DEFAULT_TEMPERATURE = 0.0
│   │
│   ├── Model Token Limits:
│   │   ├── MODEL_TOKEN_LIMITS = {...}
│   │   └── FALLBACK_TOKEN_LIMIT = 16384
│   │
│   ├── Emotion Colors & Classifications:
│   │   ├── EMOTION_COLORS = {...}
│   │   └── Intensity thresholds
│   │
│   ├── Class Methods:
│   │   ├── get_model_token_limit(model) : int
│   │   ├── get_emotion_color(emotion) : str
│   │   ├── classify_emotion_intensity(intensity) : str
│   │   ├── calculate_dynamic_chart_height(item_count) : int
│   │   └── validate_configuration() : bool
```

### **Dependency Injection (`src/infrastructure/dependency_injection/`)**

#### **`contenedor_dependencias.py`** - DI Container

```python
├── Class: ContenedorDependencias
│   ├── __init__(configuracion, ai_configuration)
│   │   ├── Thread-safe initialization (RLock)
│   │   ├── Servicios registry
│   │   ├── Singleton pattern
│   │   └── Configuración IA centralizada
│   │
│   ├── _registrar_servicios_por_defecto() : None
│   │   ├── Registro AnalizadorMaestroIA
│   │   ├── Registro LectorArchivosExcel
│   │   ├── Registro RepositorioComentarios  
│   │   └── Registro casos de uso
│   │
│   ├── registrar(nombre, fabrica, singleton=True) : None
│   │   └── Registro genérico servicios
│   │
│   ├── obtener(nombre) : T
│   │   ├── Resolución dependencias thread-safe
│   │   ├── Pattern factory + singleton
│   │   └── Lazy loading
│   │
│   ├── Getters específicos:
│   │   ├── obtener_analizador_maestro_ia() : AnalizadorMaestroIA
│   │   ├── obtener_caso_uso_maestro() : AnalizarExcelMaestroCasoUso
│   │   ├── obtener_lector_archivos() : ILectorArchivos
│   │   └── obtener_repositorio_comentarios() : IRepositorioComentarios
│   │
│   ├── obtener_estadisticas_configuracion() : Dict[str, Any]
│   └── limpiar_cache() : None
```

### **File Handlers (`src/infrastructure/file_handlers/`)**

#### **`lector_archivos_excel.py`** - Lectura archivos

```python
├── Class: LectorArchivosExcel (implements ILectorArchivos)
│   ├── leer_archivo(archivo_cargado, nombre_archivo) : List[str]
│   │   ├── Detección formato (Excel/CSV)
│   │   ├── Lectura con pandas  
│   │   ├── Extracción columna comentarios
│   │   ├── Limpieza y validación
│   │   └── Conversión a List[str]
│   │
│   ├── _detectar_columna_comentarios(df) : str
│   │   ├── Heurística detección columna
│   │   ├── Búsqueda por nombres comunes
│   │   └── Análisis contenido
│   │
│   ├── _limpiar_comentarios(comentarios) : List[str]
│   │   ├── Eliminación NaN/vacíos
│   │   ├── Strip whitespace
│   │   └── Filtrado por longitud mínima
│   │
│   ├── validar_formato(archivo_cargado) : bool
│   └── obtener_estadisticas_archivo(archivo_cargado) : Dict[str, Any]
```

### **Repositorios (`src/infrastructure/repositories/`)**

#### **`repositorio_comentarios_memoria.py`** - Persistencia en memoria

```python
├── Class: RepositorioComentariosMemoria (implements IRepositorioComentarios)
│   ├── __init__()
│   │   └── Thread-safe storage con Lock
│   │
│   ├── guardar(comentario_analizado) : None
│   ├── obtener_por_id(comentario_id) : Optional[AnalisisComentario] 
│   ├── obtener_todos() : List[AnalisisComentario]
│   ├── buscar_por_sentimiento(sentimiento) : List[AnalisisComentario]
│   ├── buscar_por_emocion(emocion) : List[AnalisisComentario]
│   ├── obtener_estadisticas() : Dict[str, Any]
│   ├── limpiar_repositorio() : None
│   └── contar_total() : int
```

### **Configuration (`src/infrastructure/config/`)**

#### **`ai_configuration_manager.py`** - Gestión configuración IA

```python
├── Class: AIConfiguration
│   ├── api_key, model, temperature, seed
│   ├── max_tokens, max_comments_per_batch
│   ├── cache_ttl_seconds, cache_max_size
│   └── Validation methods
│
├── Class: AIConfigurationManager
│   ├── __init__(secrets_source)
│   ├── get_configuration() : AIConfiguration  
│   ├── validate_configuration() : bool
│   ├── reload_configuration() : None
│   └── get_debug_info() : Dict[str, Any]
│
└── Functions:
    ├── get_ai_configuration_manager(secrets) : AIConfigurationManager
    └── get_ai_configuration(secrets) : AIConfiguration
```

---

## 🔧 UTILIDADES COMPARTIDAS

### **Excepciones (`src/shared/exceptions/`)**

**`archivo_exception.py`**
```python
├── Class: ArchivoException(Exception)
│   ├── Para errores relacionados archivos
│   └── Manejo específico Excel/CSV
```

**`ia_exception.py`** 
```python
├── Class: IAException(Exception)
│   ├── Para errores servicios IA
│   └── OpenAI API errors
```

### **Presentation Layer (`src/presentation/streamlit/`)**

#### **`enhanced_css_loader.py`** - CSS avanzado

```python
├── ensure_css_loaded() : bool
│   └── Carga CSS glassmorphism
├── load_glassmorphism() : None  
│   └── Estilos glass morphism
├── inject_page_css() : None
│   └── CSS específico página
└── THREAD_SAFE_SESSION handling
```

#### **`session_state_manager.py`** - Gestión session state

```python
├── Class: SessionStateManager
│   ├── Thread-safe session management
│   ├── get(), set(), clear()
│   └── Streamlit deployment compatible
```

---

## 🎯 PUNTOS DE ENTRADA CRÍTICOS

### **Para Debugging:**
1. **`pages/2_Subir.py:239`** - Línea ejecución principal
2. **`analizar_excel_maestro_caso_uso.py:150`** - Inicio orquestación  
3. **`analizador_maestro_ia.py:228`** - Análisis IA core
4. **`analizador_maestro_ia.py:370`** - Llamada OpenAI API

### **Para Performance Monitoring:**
1. **`ai_progress_tracker.py:119`** - Progress step tracking
2. **`ai_engine_constants.py:16`** - Safety limits
3. **`analizador_maestro_ia.py:116`** - Token calculation

### **Para Configuration:**
1. **`streamlit_app.py:154`** - AI config initialization
2. **`contenedor_dependencias.py:34`** - DI container setup
3. **`ai_configuration_manager.py`** - Centralized config

---

## 📊 MATRIZ DE RESPONSABILIDADES

| Módulo | Responsabilidad Principal | Entrada | Salida |
|--------|--------------------------|---------|---------|
| `streamlit_app.py` | Bootstrap & DI setup | Config secrets | Session state |
| `pages/2_Subir.py` | UI orchestration | File upload | Analysis results |
| `AnalizarExcelMaestroCasoUso` | Business logic coordination | File + Command | Analysis result |
| `AnalizadorMaestroIA` | AI analysis engine | Comments list | AI analysis |
| `AIProgressTracker` | Progress monitoring | Comment count | Progress data |
| `ContenedorDependencias` | Dependency resolution | Config | Service instances |
| `LectorArchivosExcel` | File processing | Excel/CSV | Comments list |

---

*Mapeo generado automáticamente - Mantener sincronizado con cambios de código*