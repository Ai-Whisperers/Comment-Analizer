# 🔗 Personal Paraguay - Complete Component Dependencies Map

**Updated Analysis:** December 2024  
**Total Components:** 75+ (Enterprise Grade)  
**Architecture:** Clean Architecture + Advanced UI + Cache Infrastructure  

## 🧬 Complete Dependency Graph by Layer

### 🎨 CONFIGURATION LAYER Dependencies (NEWLY DISCOVERED)

```
.env
├── OPENAI_API_KEY, OPENAI_MODEL, OPENAI_TEMPERATURE
├── MAX_COMMENTS_PER_BATCH, CACHE_TTL_SECONDS  
├── APP_ENV, DEBUG_MODE, LOG_LEVEL
└── Performance & Security Settings

.streamlit/config.toml
├── server.enableStaticServing = true (for CSS system)
├── server.maxUploadSize = 5
├── server.headless = true (production)
├── runner.magicEnabled = false
└── theme.primaryColor = "#8B5CF6"

requirements.txt (32 Dependencies)
├── streamlit>=1.39.0 (UI framework)
├── openai>=1.50.0 (AI engine)
├── pandas>=2.1.0 (data processing)
├── openpyxl>=3.0.0 (Excel generation)
├── python-dotenv>=1.0.0 (environment)
└── 27 additional production dependencies

runtime.txt
└── python-3.12 (specified version)

Multi-Source Config Manager
├── Environment variables (primary)
├── Streamlit secrets (cloud fallback)  
├── Default values (system fallback)
└── Type conversion & validation
```

### 📱 PRESENTATION LAYER Dependencies (EXPANDED TO 22 COMPONENTS)

```
streamlit_app.py (ENHANCED with Multi-Config)
├── os, dotenv (environment management)
├── streamlit (UI framework)
├── pathlib (file system)
├── src.aplicacion_principal (app facade)
├── src.infrastructure.dependency_injection.contenedor_dependencias
├── src.shared.exceptions (ArchivoException, IAException)
└── src.presentation.streamlit.css_loader

pages/1_Página_Principal.py (ENHANCED with Glass Effects)
├── streamlit (UI framework)
├── pathlib (path management)
└── src.presentation.streamlit.enhanced_css_loader

pages/2_Subir.py (SOPHISTICATED UI + Analysis)
├── streamlit (UI framework)
├── pandas (data preview & processing)
├── datetime (timestamps)
├── pathlib (file handling)
├── openpyxl (Excel generation)
├── src.shared.exceptions (ArchivoException, IAException)
├── src.presentation.streamlit.enhanced_css_loader (CSS orchestration)
├── src.presentation.streamlit.session_validator (state management)
└── src.application.use_cases.analizar_excel_maestro_caso_uso

src/presentation/streamlit/session_validator.py (ADVANCED Session Management)
├── streamlit (session state)
├── logging (diagnostics)
└── typing (type safety)

src/presentation/streamlit/css_loader.py (BASIC CSS Utilities)
├── streamlit (HTML injection)
├── pathlib (file access)
└── typing (type safety)

src/presentation/streamlit/enhanced_css_loader.py (SOPHISTICATED CSS System)
├── streamlit (HTML injection)
├── pathlib (file system)
├── logging (CSS load tracking)
├── typing (type safety)
├── re (import statement processing)
└── CSS Cascade Management:
    ├── static/css/base/variables.css (design tokens)
    ├── static/css/base/reset.css (modern reset)
    ├── static/css/components/*.css (4 component files)
    ├── static/css/animations/keyframes.css (animations)
    ├── static/css/utils/utilities.css (atomic utilities)
    ├── static/glassmorphism.css (glass effects)
    ├── static/main.css (main entry)
    └── static/styles.css (legacy compatibility)
```

---

### 🧪 APPLICATION LAYER Dependencies

```
src/aplicacion_principal.py (Application Facade)
├── typing, datetime
├── src.infrastructure.dependency_injection.contenedor_dependencias
├── src.application.use_cases.analizar_comentarios_caso_uso
├── src.application.dtos.resultado_analisis
├── src.shared.exceptions.archivo_exception
└── src.shared.exceptions.ia_exception

src/application/use_cases/analizar_excel_maestro_caso_uso.py ⭐ CORE
├── typing, dataclasses, datetime, logging
├── src.domain.entities.analisis_comentario
├── src.domain.repositories.repositorio_comentarios
├── src.domain.value_objects.sentimiento
├── src.domain.value_objects.emocion  
├── src.domain.value_objects.tema_principal
├── src.domain.value_objects.punto_dolor
├── src.application.interfaces.lector_archivos
├── src.application.dtos.analisis_completo_ia
├── src.infrastructure.external_services.analizador_maestro_ia
├── src.shared.exceptions.archivo_exception
└── src.shared.exceptions.ia_exception

src/application/use_cases/analizar_comentarios_caso_uso.py (Legacy)
├── typing, dataclasses, datetime
├── src.domain.entities.comentario
├── src.domain.repositories.repositorio_comentarios
├── src.domain.services.analizador_sentimientos
├── src.domain.value_objects.calidad_comentario
├── src.domain.value_objects.nivel_urgencia
├── src.application.interfaces (lector_archivos, procesador_texto, detector_temas)
└── src.application.dtos.resultado_analisis

src/application/dtos/analisis_completo_ia.py ⭐ CORE DTO
├── dataclasses
├── datetime
└── typing

src/application/dtos/resultado_analisis.py
├── dataclasses  
├── datetime
└── typing

src/application/dtos/temas_detectados.py
├── dataclasses
└── typing

src/application/interfaces/*.py (Contracts)
├── abc (abstract base classes)
├── typing
└── domain references
```

---

### 🏢 DOMAIN LAYER Dependencies

```
src/domain/entities/analisis_comentario.py ⭐ CORE ENTITY
├── dataclasses, typing, datetime
├── src.domain.value_objects.sentimiento
├── src.domain.value_objects.emocion
├── src.domain.value_objects.tema_principal
├── src.domain.value_objects.punto_dolor
├── src.domain.value_objects.calidad_comentario
└── src.domain.value_objects.nivel_urgencia

src/domain/entities/comentario.py (Legacy Entity)
├── dataclasses
├── datetime
├── src.domain.value_objects.sentimiento
└── src.domain.value_objects.calidad_comentario

src/domain/value_objects/sentimiento.py
├── dataclasses
├── enum
└── typing

src/domain/value_objects/emocion.py  
├── dataclasses
├── enum
└── typing

src/domain/value_objects/tema_principal.py
├── dataclasses
├── enum
└── typing

src/domain/value_objects/punto_dolor.py
├── dataclasses
├── enum
└── typing

src/domain/value_objects/calidad_comentario.py
├── dataclasses
└── enum

src/domain/value_objects/nivel_urgencia.py
├── dataclasses
├── enum
└── typing

src/domain/services/analizador_sentimientos.py
├── abc (abstractions)
├── typing
├── src.domain.entities.comentario
└── src.domain.value_objects.sentimiento

src/domain/repositories/repositorio_comentarios.py
├── abc
├── typing
├── src.domain.entities.comentario
└── src.domain.entities.analisis_comentario
```

---

### ⚙️ INFRASTRUCTURE LAYER Dependencies

```
src/infrastructure/external_services/analizador_maestro_ia.py ⭐ AI ENGINE (ENHANCED)
├── openai (OpenAI Python SDK)
├── json, time, hashlib (core utilities)
├── typing, datetime, logging (infrastructure)
├── collections.OrderedDict (LRU cache implementation)
├── src.application.dtos.analisis_completo_ia
├── src.shared.exceptions.ia_exception
└── ADVANCED CACHE SYSTEM:
    ├── LRU Cache Manager (OrderedDict-based)
    ├── TTL Management (configurable expiration)
    ├── Cache Key Generation (deterministic hashing)
    ├── Memory Usage Optimization (50 entry limit)
    └── Cache Statistics Tracking

src/infrastructure/external_services/analizador_openai.py (Legacy)
├── openai
├── json, time, logging
├── typing
├── src.domain.services.analizador_sentimientos
├── src.domain.value_objects.sentimiento
└── src.shared.exceptions.ia_exception

src/infrastructure/file_handlers/lector_archivos_excel.py
├── pandas (Excel/CSV processing)
├── typing, logging
├── src.application.interfaces.lector_archivos
└── src.shared.exceptions.archivo_exception

src/infrastructure/text_processing/procesador_texto_basico.py
├── re (regex patterns)
├── typing, logging
├── collections (defaultdict)
├── src.domain.entities.comentario
└── src.application.interfaces.procesador_texto

src/infrastructure/repositories/repositorio_comentarios_memoria.py
├── typing, logging
├── src.domain.entities.comentario
├── src.domain.entities.analisis_comentario
└── src.domain.repositories.repositorio_comentarios

src/infrastructure/dependency_injection/contenedor_dependencias.py ⭐ DI CONTAINER
├── typing, logging
├── src.domain.services.analizador_sentimientos
├── src.domain.repositories.repositorio_comentarios
├── src.application.use_cases.analizar_comentarios_caso_uso
├── src.application.interfaces (lector_archivos, procesador_texto)
├── src.infrastructure.external_services.analizador_openai
├── src.infrastructure.external_services.analizador_maestro_ia
├── src.infrastructure.file_handlers.lector_archivos_excel
├── src.infrastructure.repositories.repositorio_comentarios_memoria
└── src.infrastructure.text_processing.procesador_texto_basico
```

---

### 🛡️ SHARED LAYER Dependencies

```
src/shared/exceptions/archivo_exception.py
└── (Pure Python - no dependencies)

src/shared/exceptions/ia_exception.py  
└── (Pure Python - no dependencies)

src/shared/utils/ (Empty - Future)
└── TBD

src/shared/validators/ (Empty - Future) 
└── TBD
```

---

## 🔄 Critical Dependency Chains

### 1. **Main Analysis Flow**
```
streamlit_app.py 
  → ContenedorDependencias
    → AnalizarExcelMaestroCasoUso 
      → AnalizadorMaestroIA
        → OpenAI API
          → AnalisisCompletoIA
            → Domain Objects
              → UI Display
```

### 2. **File Processing Chain**
```
pages/2_Subir.py
  → lector_archivos_excel.py
    → pandas DataFrame
      → procesador_texto_basico.py  
        → Clean Text
          → AI Analysis
```

### 3. **AI Response Chain**
```
OpenAI API Response
  → _procesar_respuesta_maestra()
    → AnalisisCompletoIA DTO
      → _mapear_a_entidades_dominio()
        → Value Objects Creation
          → AnalisisComentario Entity
            → Repository Storage
```

### 4. **Configuration Chain**
```
Environment Variables / Streamlit Secrets
  → streamlit_app.py config dict
    → ContenedorDependencias
      → Service Configuration
        → AI Engine Parameters
```

---

## 📦 External Package Dependencies

### Core Libraries
```yaml
# AI & ML
openai: ">=1.50.0"              # OpenAI API client

# Data Processing  
pandas: ">=2.0.0"               # Excel/CSV processing
openpyxl: ">=3.0.0"            # Excel generation

# Web Framework
streamlit: ">=1.28.0"          # UI framework

# Utilities
python-dotenv: ">=1.0.0"      # Environment variables
```

### Python Standard Library
```yaml
# Core modules used throughout
- dataclasses                   # DTO definitions
- typing                        # Type annotations
- datetime                      # Timestamps
- logging                       # System logging
- abc                          # Abstract base classes
- enum                         # Enumerations
- json                         # JSON processing
- re                           # Regular expressions
- pathlib                      # File path handling
- collections                  # Data structures
- hashlib                      # Hashing for cache keys
- time                         # Performance timing
- gc                           # Garbage collection
```

---

## 🎯 Dependency Injection Points

### Configuration Injection
```python
# streamlit_app.py
config = {
    'openai_api_key': openai_key,
    'openai_modelo': os.getenv('OPENAI_MODEL') or st.secrets.get('OPENAI_MODEL'),
    'openai_temperatura': float(os.getenv('OPENAI_TEMPERATURE', '0.0')),
    'openai_max_tokens': int(os.getenv('OPENAI_MAX_TOKENS', '8000')),
    'max_comments': int(os.getenv('MAX_COMMENTS_PER_BATCH', '40')),
    'cache_ttl': int(os.getenv('CACHE_TTL_SECONDS', '3600'))
}
```

### Service Injection  
```python
# ContenedorDependencias
def obtener_caso_uso_maestro(self):
    return AnalizarExcelMaestroCasoUso(
        repositorio_comentarios=self.obtener_repositorio_comentarios(),
        lector_archivos=self.obtener_lector_archivos(),
        analizador_maestro=self.obtener_analizador_maestro_ia(),
        max_comments_per_batch=self.configuracion.get('max_comments', 42)
    )
```

---

## 🧩 Interface Implementations

### Domain Interfaces → Infrastructure
```python
IRepositorioComentarios → repositorio_comentarios_memoria.py
ILectorArchivos → lector_archivos_excel.py  
IProcesadorTexto → procesador_texto_basico.py
IAnalizadorSentimientos → analizador_openai.py
IDetectorTemas → [Not implemented - handled by AI]
```

### Clean Architecture Compliance
- ✅ Domain layer has no external dependencies
- ✅ Application layer depends only on domain interfaces  
- ✅ Infrastructure implements domain interfaces
- ✅ Dependency inversion principle enforced
- ✅ UI depends on application layer only

---

## 🚨 Critical Dependencies

### Must-Have for System Function
1. **OpenAI API** - Core AI functionality
2. **streamlit** - UI framework
3. **pandas** - Data processing
4. **ContenedorDependencias** - Dependency injection
5. **AnalizadorMaestroIA** - AI processing engine

### High-Risk Dependencies  
- **OpenAI API availability** - Single point of failure
- **Token limits** - Rate limiting constraints
- **Memory usage** - Large file processing
- **Internet connectivity** - Cloud API dependency

---

This dependency map provides a complete view of how all 45+ components interact within the Personal Paraguay AI pipeline system.