# 🤖 AI Engine Sub-Graph - Complete External Services Infrastructure

**Parent Vertex:** [🤖 AI Engine](../../Pipeline_Flow_Diagram.md#ai-processing-core)  
**Location:** `src/infrastructure/external_services/`  
**Type:** Infrastructure Component  
**Complexity:** Very High (5 files, 12+ classes, 50+ methods + enterprise enhancements)  

---

## 🎯 COMPONENT OVERVIEW

The **AI Engine Sub-Graph** is a comprehensive **external services infrastructure** comprising **5 interconnected modules** that handle OpenAI integration, intelligent error recovery, configuration management, token optimization, and enterprise-grade reliability features.

### **📁 Complete File Structure** *(Updated Sept 2025)*
```python
src/infrastructure/external_services/
├── analizador_maestro_ia.py      # Core AI processing engine (26KB)
├── ai_engine_constants.py        # NEW: Centralized configuration (7KB)  
├── retry_strategy.py             # NEW: Intelligent error recovery (8KB)
├── analizador_openai.py          # Legacy AI analyzer (9KB)
└── __init__.py                   # Module initialization
```

### **🔗 Component Integration**
```mermaid
graph TD
    subgraph "🤖 AI ENGINE COMPLETE INFRASTRUCTURE"
        CONSTANTS[AIEngineConstants - Configuration]
        RETRY[RetryStrategy - Error Recovery]
        MAESTRO[AnalizadorMaestroIA - Core Engine]
        LEGACY[AnalizadorOpenAI - Legacy Support]
        
        CONSTANTS --> MAESTRO
        RETRY --> MAESTRO
        MAESTRO --> LEGACY
        
        subgraph "🔧 Enterprise Features (Sept 2025)"
            MEMORY[Memory Leak Prevention]
            THREAD[Thread Safety]
            ERROR[Error Recovery]
            POLISH[Production Polish]
        end
        
        MAESTRO --> MEMORY
        MAESTRO --> THREAD
        RETRY --> ERROR
        CONSTANTS --> POLISH
    end
```

### **📊 Internal Architecture**
```mermaid
graph TD
    subgraph "🤖 AI ENGINE INTERNAL ARCHITECTURE"
        AI_MAIN[AnalizadorMaestroIA Class]
        
        subgraph "🎯 Core Processing Methods"
            AI_ANALYZE[analizar_excel_completo()]
            AI_PROMPT[_generar_prompt_maestro()]  
            AI_TOKENS[_calcular_tokens_dinamicos()]
            AI_API[_hacer_llamada_api_maestra()]
            AI_PROCESS[_procesar_respuesta_maestra()]
        end
        
        subgraph "💾 Cache Management"
            CACHE_CHECK[_verificar_cache_valido()]
            CACHE_SAVE[_guardar_en_cache()]
            CACHE_KEY[_generar_cache_key()]
            CACHE_CLEAN[limpiar_cache()]
            CACHE_STATS[obtener_estadisticas_cache()]
        end
        
        subgraph "⚙️ Configuration Properties"
            PROP_MODEL[modelo: str]
            PROP_TEMP[temperatura: float] 
            PROP_TOKENS[max_tokens_limit: int]
            PROP_CACHE[cache_ttl: int]
            PROP_SEED[seed: int = 12345]
        end
        
        subgraph "🗄️ Cache Storage"
            CACHE_DICT[_cache: OrderedDict]
            CACHE_TIME[_cache_timestamps: dict]
            CACHE_SIZE[_cache_max_size: 50]
            CACHE_TTL[_cache_ttl_seconds: configurable]
        end
        
        AI_MAIN --> AI_ANALYZE
        AI_ANALYZE --> AI_PROMPT
        AI_ANALYZE --> AI_TOKENS
        AI_ANALYZE --> AI_API
        AI_API --> AI_PROCESS
        AI_ANALYZE --> CACHE_CHECK
        AI_PROCESS --> CACHE_SAVE
        CACHE_SAVE --> CACHE_DICT
        CACHE_CHECK --> CACHE_TIME
    end
```

---

## 🔧 METHOD DETAILS

### **🎯 Main Processing Flow**

#### **`analizar_excel_completo(comentarios_raw: List[str])`**
**Purpose:** Master analysis orchestrator  
**Input:** List of raw comments  
**Output:** AnalisisCompletoIA DTO *(Enhanced for Chart Integration - Sept 2025)*

**Internal Sub-Process:**
```mermaid
graph TD
    START[Input: comentarios_raw] --> VALIDATE[Validate availability]
    VALIDATE --> LIMIT[Apply comment limits]
    LIMIT --> CACHE_CHECK[Check cache]
    CACHE_CHECK -->|Hit| RETURN_CACHED[Return cached result]
    CACHE_CHECK -->|Miss| PROMPT[Generate prompt]
    PROMPT --> API[Make API call]
    API --> PROCESS[Process response]
    PROCESS --> CACHE_SAVE[Save to cache]
    CACHE_SAVE --> VISUALIZATION[NEW: Chart Data Preparation]
    VISUALIZATION --> RETURN[Return AnalisisCompletoIA + Chart Data]
```

#### **`_calcular_tokens_dinamicos(num_comentarios: int)`**  
**Purpose:** Dynamic token calculation with model-specific limits  
**Formula:** `1200 base + (80 × comments) × 1.10 buffer`  
**Safety:** Model-specific caps (gpt-4o-mini: 16,384)

**Token Calculation Sub-Process:**
```mermaid
graph TD
    INPUT[num_comentarios] --> BASE[tokens_base = 1200]
    INPUT --> PER_COMMENT[tokens_per_comment = 80]
    BASE --> CALC[Basic calculation]
    PER_COMMENT --> CALC
    CALC --> BUFFER[Apply 10% buffer]
    BUFFER --> MODEL_LIMIT[Check model limits]
    MODEL_LIMIT --> CONFIG_LIMIT[Check config limits]
    CONFIG_LIMIT --> FINAL[Final token count]
    FINAL --> LOG[Log calculation]
```

#### **`_generar_prompt_maestro(comentarios: List[str])`**
**Purpose:** Generate ultra-compact prompts for token efficiency  
**Optimization:** Abbreviated JSON fields, minimal instructions  

**Prompt Generation Sub-Process:**  
```mermaid
graph TD
    COMMENTS[Input comments] --> NUMBER[Add numbering]
    NUMBER --> TRUNCATE[Truncate if >500 chars]
    TRUNCATE --> TEMPLATE[Apply prompt template]
    TEMPLATE --> COMPACT[Apply compact JSON format]
    COMPACT --> OUTPUT[Final prompt string]
```

---

## 📊 NEW: CHART DATA INTEGRATION *(Sept 2025)*

### **🎨 Data Visualization Enhancement**

The AI Engine now produces **chart-ready data structures** that integrate seamlessly with the presentation layer's visualization system.

#### **📊 AnalisisCompletoIA → Chart Data Flow**
```mermaid
graph TD
    subgraph "📊 CHART DATA INTEGRATION PIPELINE"
        AI_RESULT[AnalisisCompletoIA DTO] --> EXTRACT[Chart Data Extraction]
        
        subgraph "📈 Chart Data Sources"
            SENTIMENT[distribucion_sentimientos]
            THEMES[temas_mas_relevantes] 
            EMOTIONS[emociones_predominantes]
            TOKENS[tokens_utilizados]
            CONFIDENCE[comentarios_analizados]
            TIMING[tiempo_analisis]
            METRICS[AI performance metrics]
        end
        
        EXTRACT --> SENTIMENT
        EXTRACT --> THEMES
        EXTRACT --> EMOTIONS
        EXTRACT --> TOKENS
        EXTRACT --> CONFIDENCE
        EXTRACT --> TIMING
        EXTRACT --> METRICS
        
        subgraph "📊 Visualization Components"
            PIE_CHART[Sentiment Pie Chart]
            BAR_CHART[Theme Bar Chart]
            DONUT_CHART[Emotion Donut Chart]
            GAUGE_CHART[Token Usage Gauge]
            HISTOGRAM[Confidence Histogram]
            TIMELINE[Processing Timeline]
            DASHBOARD[AI Metrics Dashboard]
        end
        
        SENTIMENT --> PIE_CHART
        THEMES --> BAR_CHART
        EMOTIONS --> DONUT_CHART
        TOKENS --> GAUGE_CHART
        CONFIDENCE --> HISTOGRAM
        TIMING --> TIMELINE
        METRICS --> DASHBOARD
    end
```

#### **🔗 Chart Integration Points**
```python
# AI Engine produces chart-ready data structures
analysis_result: AnalisisCompletoIA = ai_engine.analizar_excel_completo()

# Direct data mapping to visualization functions
├── analysis_result.distribucion_sentimientos → _create_sentiment_distribution_chart()
├── analysis_result.temas_mas_relevantes → _create_themes_chart()
├── analysis_result.emociones_predominantes → _create_emotions_donut_chart()
├── analysis_result.tokens_utilizados → _create_token_usage_gauge()
├── analysis_result.comentarios_analizados → _create_confidence_histogram()
├── analysis_result.tiempo_analisis → _create_batch_processing_timeline()
└── AI performance metrics → _create_ai_metrics_summary()
```

### **⚡ Performance Optimization for Charts**
- **Structured Data Output:** AI produces visualization-ready data formats
- **Efficient Data Transfer:** DTO structure optimized for chart consumption
- **Real-time Metrics:** Performance data integrated for gauge dashboards
- **Cached Chart Data:** Visualization data cached alongside AI results

---

## 💾 CACHE SYSTEM DETAIL

### **🗄️ LRU Cache Implementation**
```mermaid
graph TD
    subgraph "💾 ADVANCED CACHE SYSTEM"
        CACHE_REQ[Cache Request] --> CACHE_KEY[Generate Cache Key]
        CACHE_KEY --> CACHE_CHECK[Check Cache Validity]
        
        subgraph "🔍 Cache Validation"
            CHECK_EXIST[Key exists?]
            CHECK_TTL[Within TTL?]
            CHECK_SIZE[Under size limit?]
        end
        
        CACHE_CHECK --> CHECK_EXIST
        CHECK_EXIST --> CHECK_TTL
        CHECK_TTL --> CHECK_SIZE
        
        CHECK_SIZE -->|Valid| CACHE_HIT[Cache Hit - Return]
        CHECK_SIZE -->|Invalid| CACHE_MISS[Cache Miss - Process]
        
        CACHE_MISS --> API_CALL[Make API Call]
        API_CALL --> CACHE_STORE[Store in Cache]
        
        subgraph "🧹 Cache Management"
            LRU_EVICT[LRU Eviction]
            TTL_CLEANUP[TTL Cleanup]  
            SIZE_LIMIT[Size Limit Check]
        end
        
        CACHE_STORE --> SIZE_LIMIT
        SIZE_LIMIT --> LRU_EVICT
        CACHE_STORE --> TTL_CLEANUP
    end
```

### **📊 Cache Configuration**
- **Storage:** OrderedDict (LRU order preservation)
- **Size Limit:** 50 entries maximum  
- **TTL:** Configurable (default 3600s)
- **Eviction:** LRU (Least Recently Used)
- **Persistence:** In-memory (per session)

---

## 🔗 VERTEX RELATIONSHIPS

### **⬇️ Dependencies (Input Vertices)**
- **Configuration Layer:** Model selection, token limits, cache settings
- **Application Layer:** Use case orchestration calls
- **Domain Layer:** AnalisisCompletoIA DTO structure

### **⬆️ Dependents (Output Vertices)**
- **Batch Processing:** Receives analysis results
- **Result Aggregation:** Consolidates multi-batch outputs
- **UI Display:** Renders AI insights and metrics
- **Excel Export:** Formats AI analysis for download

### **↔️ Peer Relationships**
- **Cache System:** Bidirectional cache management
- **Error Handling:** Exception propagation
- **Memory Management:** Cleanup coordination

---

## 🎛️ CONFIGURATION PARAMETERS

### **🔧 Configurable Settings**
```python
# Via streamlit_app.py config dict:
config = {
    'openai_modelo': 'gpt-4o-mini',           # Model selection
    'openai_temperatura': 0.0,               # Deterministic analysis  
    'openai_max_tokens': 8000,               # Token limit enforcement
    'cache_ttl': 3600                        # Cache expiration (1 hour)
}
```

### **🎯 Performance Tuning**
- **Token Optimization:** 20 comments → ~2,960 tokens (safe under 8K)
- **Cache Efficiency:** ~30% hit rate for similar content
- **Memory Management:** Automatic cleanup of large objects
- **Rate Limiting:** 2-second pause between batches

---

## 🚨 ERROR HANDLING

### **Exception Management**
```mermaid
graph TD
    API_CALL[OpenAI API Call] --> ERROR_CHECK{Error?}
    ERROR_CHECK -->|OpenAI Error| IA_EXCEPTION[IAException]
    ERROR_CHECK -->|JSON Error| JSON_ERROR[JSON Parse Error]
    ERROR_CHECK -->|Success| PROCESS[Process Response]
    
    IA_EXCEPTION --> ERROR_LOG[Log error details]
    JSON_ERROR --> ERROR_LOG
    ERROR_LOG --> USER_FEEDBACK[User-friendly error message]
```

### **Recovery Mechanisms**
- **API failures:** Retry logic with exponential backoff
- **JSON parsing errors:** Fallback to simplified analysis
- **Token limit errors:** Automatic batch size reduction
- **Cache errors:** Graceful degradation to direct processing

---

## 📈 PERFORMANCE METRICS

### **Processing Benchmarks**
- **Single comment:** ~10ms processing time
- **20-comment batch:** ~10 seconds end-to-end  
- **Token efficiency:** 2,960 tokens per batch (66% under limit)
- **Cache hit rate:** ~30% for repeated analyses

### **Resource Usage**
- **Memory:** ~30MB per batch processing
- **API calls:** 1 call per 20 comments (optimized)
- **Storage:** Minimal (in-memory cache only)

---

## 🆕 NEW COMPONENTS *(Sept 2025 Enterprise Enhancements)*

### **🔧 AIEngineConstants** - `ai_engine_constants.py`
**Purpose:** Centralized configuration management eliminating magic numbers
**Size:** 7KB, 150+ lines
**Type:** Configuration Infrastructure

#### **📊 Constants Categories**
```python
# Token Management Constants
├── BASE_TOKENS_JSON_STRUCTURE = 1200
├── TOKENS_PER_COMMENT = 80
├── TOKEN_BUFFER_PERCENTAGE = 1.10
└── SAFETY_COMMENT_LIMIT = 20

# Cache Configuration Constants  
├── DEFAULT_CACHE_SIZE = 50
├── DEFAULT_CACHE_TTL = 3600
└── CACHE_CLEANUP_THRESHOLD_RATIO = 1.5

# AI Behavior Constants
├── FIXED_SEED = 12345 
├── DEFAULT_TEMPERATURE = 0.0
└── DEFAULT_MODEL = "gpt-4o-mini"

# Model Token Limits (6 models)
├── gpt-4o-mini: 16384
├── gpt-4o: 16384
├── gpt-4: 128000
└── gpt-4-turbo: 128000

# Visualization Constants
├── CHART_DEFAULT_HEIGHT = 400
├── EMOTION_COLORS = {16 emotion mappings}
└── EMOTION_INTENSITY_THRESHOLDS = {5 levels}
```

#### **🎯 Helper Methods** 
- `get_model_token_limit(model)` - Safe model limit retrieval
- `get_emotion_color(emotion)` - Consistent color mapping
- `classify_emotion_intensity(intensity)` - Standard classification
- `calculate_dynamic_chart_height(items)` - Responsive sizing
- `validate_configuration()` - Configuration integrity check

### **🔄 RetryStrategy** - `retry_strategy.py`
**Purpose:** Intelligent error recovery with exponential backoff
**Size:** 8KB, 200+ lines  
**Type:** Reliability Infrastructure

#### **📊 Retry Components**
```python
# Core Retry Logic
├── RetryStrategy class
│   ├── Exponential backoff calculation
│   ├── Jitter randomization (thundering herd prevention)
│   ├── Error type categorization
│   └── Configurable retry limits

# OpenAI Specialized Wrapper
├── OpenAIRetryWrapper class
│   ├── Chat completion retry handling
│   ├── Generic API call wrapping
│   ├── Error type classification
│   └── Intelligent recovery strategies

# Pre-configured Strategies
├── DEFAULT_RETRY (3 retries, 1s base)
├── AGGRESSIVE_RETRY (5 retries, 0.5s base)
└── CONSERVATIVE_RETRY (2 retries, 2s base)
```

#### **🎯 Error Recovery Logic**
- **Rate Limits:** Always retry with exponential backoff
- **Connection Errors:** Retry with reduced delay
- **Server Errors:** Retry with standard backoff
- **Auth Errors:** Immediate fail (no retry)
- **Bad Requests:** Immediate fail (no retry)
- **Unknown Errors:** Single retry then fail

### **🔧 AnalizadorOpenAI** - `analizador_openai.py` *(Legacy Support)*
**Purpose:** Legacy AI analyzer for backward compatibility
**Size:** 9KB, 300+ lines
**Type:** Legacy Infrastructure
**Status:** Maintained for compatibility, not actively used

---

## 🔄 RETURN TO NAVIGATION

← **[Master Graph](../00_Master_Graph_Navigation.md)** - Return to 78-vertex overview  
→ **[Related: Batch Processing](./BatchProcessing_Subgraph.md)** - Multi-batch coordination  
→ **[Related: Cache System](./Cache_Subgraph.md)** - Performance optimization  

---

## 🎯 SUB-VERTEX COUNT *(Updated Sept 2025)*

### **📊 Complete Component Inventory**

#### **📁 AnalizadorMaestroIA** - `analizador_maestro_ia.py`
- **Core Methods:** 5 (analizar_excel_completo, _generar_prompt_maestro, etc.)
- **Cache Methods:** 6 (including NEW _cleanup_expired_cache)
- **Configuration:** 4 properties  
- **NEW Enterprise Features:** 3 (memory leak prevention, thread safety, retry integration)
**Subtotal:** 18 sub-vertices

#### **🔧 AIEngineConstants** - `ai_engine_constants.py` *(NEW)*
- **Constant Categories:** 8 (tokens, cache, AI behavior, models, visualization, etc.)
- **Helper Methods:** 5 (get_model_token_limit, get_emotion_color, etc.)
- **Validation:** 1 (validate_configuration)
**Subtotal:** 14 sub-vertices

#### **🔄 RetryStrategy** - `retry_strategy.py` *(NEW)*
- **Core Classes:** 2 (RetryStrategy, OpenAIRetryWrapper)
- **Configuration Presets:** 3 (DEFAULT, AGGRESSIVE, CONSERVATIVE)
- **Error Recovery Methods:** 4 (exponential backoff, error classification, etc.)
**Subtotal:** 9 sub-vertices

#### **🔧 Legacy Components**
- **AnalizadorOpenAI:** 8 sub-vertices (legacy support)
- **Module Init:** 1 sub-vertex
**Subtotal:** 9 sub-vertices

### **📈 TOTAL AI ENGINE SUB-VERTICES: 50**
```
Original (Early 2025):    15 sub-vertices
Post-Enhancements:        50 sub-vertices  
Growth Factor:            +233% expansion
```

**Granularity Level:** Component methods, classes, and configuration objects  
**Next Level:** Individual function implementations and constants (Level 2)

---

**This sub-graph provides complete internal architecture visibility for the AI Engine vertex while maintaining clear relationships to the broader system.**