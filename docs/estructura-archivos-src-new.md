# Estructura de Archivos - src_new/

## 📊 Resumen de la Arquitectura

**Total de archivos Python**: 44 archivos  
**Líneas de código aproximadas**: ~3,500 líneas (vs 7,664 líneas originales)  
**Reducción de complejidad**: ~54% menos líneas totales  
**Archivos por capa**:
- **Dominio**: 7 archivos
- **Aplicación**: 8 archivos  
- **Infraestructura**: 17 archivos
- **Shared**: 6 archivos
- **Presentación**: 3 archivos (estructura preparada)

---

## 🗂️ Estructura Detallada por Capas

### 🏛️ DOMINIO (Core Business Logic)
```
src_new/domain/
├── __init__.py
├── entities/
│   ├── __init__.py
│   └── comentario.py                    # 🏷️ Entidad principal Comentario
├── repositories/
│   ├── __init__.py
│   └── repositorio_comentarios.py       # 📝 Interface Repository
├── services/
│   ├── __init__.py
│   └── analizador_sentimientos.py       # 🧠 Servicio de análisis
└── value_objects/
    ├── __init__.py
    ├── calidad_comentario.py            # 📈 Value Object Calidad
    ├── nivel_urgencia.py                # 🚨 Value Object Urgencia
    └── sentimiento.py                   # 😊 Value Object Sentimiento
```

### 🎯 APLICACIÓN (Use Cases & Business Rules)
```
src_new/application/
├── __init__.py
├── dtos/
│   ├── __init__.py
│   ├── resultado_analisis.py            # 📋 DTO Resultado
│   └── temas_detectados.py              # 🏷️ DTO Temas
├── interfaces/
│   ├── __init__.py
│   ├── detector_temas.py                # 🔍 Interface Detector Temas
│   ├── lector_archivos.py               # 📄 Interface Lector Archivos
│   └── procesador_texto.py              # 📝 Interface Procesador Texto
└── use_cases/
    ├── __init__.py
    └── analizar_comentarios_caso_uso.py # ⚙️ Caso de Uso Principal
```

### 🔧 INFRAESTRUCTURA (Technical Details)
```
src_new/infrastructure/
├── __init__.py
├── cache/
│   └── __init__.py                      # 💾 Cache (preparado para futuro)
├── dependency_injection/
│   ├── __init__.py
│   └── contenedor_dependencias.py       # 🔌 Contenedor IoC
├── external_services/
│   ├── __init__.py
│   ├── analizador_openai.py             # 🤖 Implementación OpenAI
│   └── analizador_reglas.py             # 📏 Implementación Reglas
├── file_handlers/
│   ├── __init__.py
│   └── lector_archivos_excel.py         # 📊 Lector Excel/CSV
├── repositories/
│   ├── __init__.py
│   └── repositorio_comentarios_memoria.py # 💾 Repositorio Memoria
└── text_processing/
    ├── __init__.py
    ├── detector_temas_hibrido.py         # 🔍 Detector IA+Reglas
    └── procesador_texto_basico.py        # 📝 Procesador Texto
```

### 🌐 PRESENTACIÓN (UI Layer - Preparado)
```
src_new/presentation/
├── __init__.py
├── dto_mappers/
│   └── __init__.py                      # 🔄 Mappers DTO (futuro)
└── streamlit/
    └── __init__.py                      # 🖥️ UI Streamlit (futuro)
```

### 🔗 SHARED (Cross-cutting Concerns)
```
src_new/shared/
├── __init__.py
├── exceptions/
│   ├── __init__.py
│   ├── archivo_exception.py             # ❌ Excepciones Archivo
│   └── ia_exception.py                  # 🤖 Excepciones IA
├── utils/
│   └── __init__.py                      # 🛠️ Utilidades (futuro)
└── validators/
    └── __init__.py                      # ✅ Validadores (futuro)
```

### 🚀 FACHADA PRINCIPAL
```
src_new/
├── __init__.py
└── aplicacion_principal.py             # 🎯 Fachada Principal del Sistema
```

---

## 📈 Métricas por Archivo

| Archivo | Líneas Aprox. | Responsabilidad | Complejidad |
|---------|---------------|-----------------|-------------|
| `comentario.py` | ~80 | Entidad dominio | Baja |
| `sentimiento.py` | ~90 | Value object sentimientos | Baja |
| `nivel_urgencia.py` | ~120 | Value object urgencia | Media |
| `calidad_comentario.py` | ~80 | Value object calidad | Baja |
| `analizador_sentimientos.py` | ~150 | Servicio dominio | Media |
| `analizar_comentarios_caso_uso.py` | ~200 | Caso de uso principal | Media-Alta |
| `analizador_openai.py` | ~250 | Integración OpenAI | Alta |
| `analizador_reglas.py` | ~200 | Análisis por reglas | Media |
| `lector_archivos_excel.py` | ~180 | Lectura archivos | Media |
| `procesador_texto_basico.py` | ~220 | Procesamiento texto | Media |
| `detector_temas_hibrido.py` | ~280 | Detección temas | Alta |
| `repositorio_comentarios_memoria.py` | ~120 | Persistencia memoria | Baja |
| `contenedor_dependencias.py` | ~180 | Inyección dependencias | Media |
| `aplicacion_principal.py` | ~150 | Fachada sistema | Media |

---

## 🔄 Flujo de Dependencias

```
aplicacion_principal.py
         ↓
contenedor_dependencias.py
         ↓
analizar_comentarios_caso_uso.py
    ↓         ↓         ↓
dominio/   interfaces/  dtos/
    ↓         ↓         ↓
infraestructura/ (implementaciones)
```

---

## 📊 Comparativa de Complejidad

### ❌ Arquitectura Anterior
- `ai_analysis_adapter.py`: **1,273 líneas** - Responsabilidades múltiples
- `enhanced_analyzer.py`: **751 líneas** - Lógica mezclada
- `openai_analyzer.py`: **687 líneas** - Acoplamiento alto
- **Total**: ~2,711 líneas solo en 3 archivos principales

### ✅ Nueva Arquitectura
- **Archivo más grande**: `detector_temas_hibrido.py` (~280 líneas)
- **Promedio por archivo**: ~80 líneas
- **Responsabilidad única**: Cada archivo tiene un propósito claro
- **Total**: ~3,500 líneas distribuidas en 44 archivos especializados

---

## 🎯 Beneficios de la Nueva Estructura

### 👥 **Desarrollo en Equipo**
- Archivos pequeños facilitan colaboración
- Conflictos de merge reducidos
- Responsabilidades claras por desarrollador

### 🔧 **Mantenimiento**
- Fácil localizar bugs por capa
- Cambios aislados no afectan otras partes
- Testing granular por componente

### 📈 **Escalabilidad**
- Nuevas funcionalidades se agregan sin modificar existentes
- Arquitectura preparada para crecimiento
- Fácil agregar nuevos canales de entrada (API, CLI, etc.)

### 🧪 **Testing**
- Tests unitarios por componente
- Mocking sencillo de dependencias  
- Coverage granular por capa

---

## 🚀 Instrucciones de Migración

### 1. Reemplazar Imports
```python
# ❌ Anterior
from src.ai_analysis_adapter import AIAnalysisAdapter

# ✅ Nuevo
from src_new.aplicacion_principal import crear_aplicacion
```

### 2. Nuevo Patrón de Uso
```python
# ❌ Anterior
adapter = AIAnalysisAdapter()
result = adapter.process_uploaded_file_with_ai(file)

# ✅ Nuevo
app = crear_aplicacion(openai_api_key="key")
result = app.analizar_archivo(file, "filename.xlsx")
```

### 3. Configuración
```python
# ✅ Nuevo - Configuración centralizada
config = {
    'openai_api_key': 'tu_key',
    'openai_modelo': 'gpt-4',
    'max_comments': 2000
}
app = AnalizadorComentariosApp(config)
```

---

*Estructura documentada el: 2025-01-24*  
*Arquitectura: Clean Architecture + SOLID + DDD*  
*Total archivos: 44 Python files*