# Arquitectura del Sistema - Analizador de Comentarios IA

## Visión General

El Analizador de Comentarios IA está construido siguiendo los principios de **Clean Architecture** con un enfoque **IA-First**, utilizando **GPT-4 de OpenAI** como motor principal de análisis.

## 🏗️ Arquitectura Clean Architecture

### Estructura de Capas

```
┌─────────────────────────────────────┐
│         PRESENTATION LAYER          │
│     (Streamlit UI + CSS System)     │
├─────────────────────────────────────┤
│        APPLICATION LAYER            │
│    (Use Cases + DTOs + Interfaces)  │
├─────────────────────────────────────┤
│          DOMAIN LAYER               │
│   (Entities + Value Objects +       │
│    Services + Business Rules)       │
├─────────────────────────────────────┤
│       INFRASTRUCTURE LAYER          │
│ (OpenAI Client + File Handlers +    │
│  Dependency Injection + Repositories)│
└─────────────────────────────────────┘
```

### Principios SOLID Implementados

- **S** - Single Responsibility: Cada clase tiene una responsabilidad específica
- **O** - Open/Closed: Extensible sin modificar código existente
- **L** - Liskov Substitution: Interfaces implementadas correctamente
- **I** - Interface Segregation: Interfaces específicas y cohesivas
- **D** - Dependency Inversion: Dependencias inyectadas, no instanciadas

## 📁 Estructura de Directorio Detallada

```
Comment-Analizer/
├── streamlit_app.py                    # Punto de entrada de la aplicación
├── pages/                              # Páginas de Streamlit
│   ├── 1_Página_Principal.py          # Dashboard con métricas IA
│   └── 2_Subir.py                     # Interfaz de carga y análisis
├── src/                                # Clean Architecture core
│   ├── aplicacion_principal.py        # Fachada principal del sistema
│   │
│   ├── domain/                        # 🎯 CAPA DE DOMINIO
│   │   ├── entities/
│   │   │   ├── comentario.py          # Entidad comentario
│   │   │   └── analisis_comentario.py # Entidad análisis
│   │   ├── value_objects/
│   │   │   ├── sentimiento.py         # VO para sentimientos
│   │   │   ├── emocion.py             # VO para emociones
│   │   │   ├── tema_principal.py      # VO para temas
│   │   │   └── punto_dolor.py         # VO para puntos de dolor
│   │   ├── services/
│   │   │   └── analizador_sentimientos.py # Servicio de dominio
│   │   └── repositories/
│   │       └── repositorio_comentarios.py # Interface repositorio
│   │
│   ├── application/                   # 🚀 CAPA DE APLICACIÓN
│   │   ├── use_cases/
│   │   │   ├── analizar_comentarios_caso_uso.py
│   │   │   └── analizar_excel_maestro_caso_uso.py # Caso uso principal IA
│   │   ├── dtos/
│   │   │   ├── resultado_analisis.py   # DTO resultado general
│   │   │   ├── temas_detectados.py     # DTO temas
│   │   │   └── analisis_completo_ia.py # DTO análisis IA completo
│   │   └── interfaces/
│   │       ├── lector_archivos.py      # Interface lectura archivos
│   │       ├── procesador_texto.py     # Interface procesamiento
│   │       └── detector_temas.py       # Interface detección temas
│   │
│   ├── infrastructure/                # ⚙️ CAPA DE INFRAESTRUCTURA
│   │   ├── external_services/
│   │   │   ├── analizador_openai.py    # Cliente OpenAI básico
│   │   │   ├── analizador_maestro_ia.py # Motor IA principal
│   │   │   ├── ai_progress_tracker.py   # Tracker de progreso IA
│   │   │   ├── retry_strategy.py        # Estrategia de reintentos
│   │   │   └── ai_engine_constants.py   # Constantes del motor IA
│   │   ├── file_handlers/
│   │   │   └── lector_archivos_excel.py # Manejo archivos Excel/CSV
│   │   ├── repositories/
│   │   │   └── repositorio_comentarios_memoria.py # Repo en memoria
│   │   ├── dependency_injection/
│   │   │   └── contenedor_dependencias.py # Container DI principal
│   │   ├── config/
│   │   │   └── ai_configuration_manager.py # Config manager IA
│   │   └── text_processing/
│   │       └── procesador_texto_basico.py # Procesamiento texto
│   │
│   ├── presentation/                  # 🎨 CAPA DE PRESENTACIÓN
│   │   ├── streamlit/
│   │   │   ├── enhanced_css_loader.py  # Sistema CSS avanzado
│   │   │   ├── progress_tracker.py     # UI progress tracker
│   │   │   ├── session_state_manager.py # Manager estado sesión
│   │   │   └── session_validator.py    # Validador de sesión
│   │   └── dto_mappers/                # Mappers DTO <-> UI
│   │
│   └── shared/                        # 📦 UTILIDADES COMPARTIDAS
│       ├── exceptions/
│       │   ├── archivo_exception.py    # Excepciones archivos
│       │   └── ia_exception.py         # Excepciones IA específicas
│       ├── utils/                      # Utilidades generales
│       └── validators/                 # Validadores de datos
│
├── config.py                          # Configuración unificada
├── requirements.txt                    # Dependencias Python
├── static/                             # CSS y archivos estáticos
└── local-reports/                      # Reportes generados localmente
```

## 🤖 Arquitectura del Sistema IA

### Motor Principal: AnalizadorMaestroIA

El corazón del sistema es la clase `AnalizadorMaestroIA` que orquesta todo el análisis:

```python
class AnalizadorMaestroIA:
    """Motor principal de análisis con GPT-4"""
    
    def analizar_comentarios_completo(self, comentarios: List[str]) -> AnalisisCompletoIA:
        """Análisis completo con una sola llamada a GPT-4"""
        
    def _construir_prompt_maestro(self, comentarios: List[str]) -> str:
        """Construye prompt optimizado para GPT-4"""
        
    def _parsear_respuesta_ia(self, respuesta: str) -> Dict:
        """Parsea y valida respuesta de IA"""
```

### Flujo de Análisis IA

```
1. Usuario carga archivo Excel/CSV
2. FileHandler valida y procesa archivo
3. CasoUsoMaestro orquesta análisis
4. AnalizadorMaestroIA llama a GPT-4
5. Sistema parsea y valida respuesta
6. DTOs transportan datos entre capas
7. UI muestra resultados procesados
8. ExportManager genera reporte Excel
```

### Capacidades IA Implementadas

- **Análisis de Sentimientos**: Positivo, Negativo, Neutral con intensidad
- **Detección de Emociones**: 20+ emociones con scoring 0-10
- **Identificación de Temas**: Automática con relevancia y frecuencia
- **Puntos de Dolor**: Severidad y categorización automática
- **Recomendaciones**: Estratégicas y accionables generadas por IA
- **Resumen Ejecutivo**: Narrativa comprehensiva contextual

## 🏛️ Patrones de Diseño Aplicados

### 1. Dependency Injection
```python
# Contenedor principal que inyecta todas las dependencias
class ContenedorDependencias:
    def obtener_caso_uso_maestro(self) -> AnalizarExcelMaestroCasoUso
    def obtener_analizador_maestro(self) -> AnalizadorMaestroIA
    def obtener_lector_archivos(self) -> LectorArchivosExcel
```

### 2. Repository Pattern
```python
# Abstracción de persistencia
class RepositorioComentarios(ABC):
    @abstractmethod
    def guardar_comentarios(self, comentarios: List[Comentario])
    
    @abstractmethod
    def obtener_todos(self) -> List[Comentario]
```

### 3. Strategy Pattern
```python
# Diferentes estrategias de análisis (actualmente solo IA)
class RetryStrategy:
    def ejecutar_con_reintentos(self, operacion: Callable)
    def manejar_rate_limits(self, exception: Exception)
```

### 4. Factory Pattern
```python
# Factory para crear instancias de análisis
def crear_aplicacion(config: Dict) -> AplicacionPrincipal:
    """Factory method para crear aplicación configurada"""
```

## 🔄 Flujo de Datos Completo

### 1. Entrada de Datos
```
Usuario → Upload Component → FileHandler → Validación → DTO
```

### 2. Procesamiento IA
```
DTO → CasoUso → AnalizadorMaestroIA → OpenAI GPT-4 → Parsing → DTO
```

### 3. Presentación
```
DTO → Mapper → UI Components → Dashboard → Visualizaciones
```

### 4. Exportación
```
DTO → ExportManager → Excel Generator → Archivo descargable
```

## 🛡️ Manejo de Errores y Excepciones

### Jerarquía de Excepciones
```python
# Excepciones específicas del dominio
class IAException(Exception):
    """Base para errores de IA"""

class OpenAIServiceException(IAException):
    """Errores específicos de OpenAI"""

class ArchivoException(Exception):
    """Errores de procesamiento de archivos"""
```

### Estrategia de Recuperación
- **Rate Limits**: Retry con backoff exponencial
- **Errores de Red**: Reintentos automáticos con timeout
- **Errores de Parsing**: Fallback a formato estructurado
- **Errores de Validación**: Mensajes específicos al usuario

## ⚡ Optimizaciones de Performance

### 1. Análisis en Lote
- Procesamiento de hasta 2000 comentarios por llamada
- Optimización de tokens para GPT-4
- Cache de configuraciones IA

### 2. Gestión de Memoria
- Procesamiento streaming cuando es posible
- Limpieza automática de objetos grandes
- Límites configurables de memoria

### 3. UI Responsiva
- Progress tracking en tiempo real
- Carga asíncrona de componentes CSS
- Estado de sesión optimizado

## 🔧 Configuración y Extensibilidad

### Variables de Configuración IA
```python
# config.py - Configuración centralizada
AI_CONFIG = {
    'model': 'gpt-4',
    'max_tokens': 4000,
    'temperature': 0.7,
    'timeout': 300,
    'max_comments_per_batch': 2000
}
```

### Puntos de Extensión
1. **Nuevos Motores IA**: Implementar interface `ProcesadorTexto`
2. **Formatos de Archivo**: Implementar interface `LectorArchivos`
3. **Tipos de Análisis**: Extender `AnalizadorSentimientos`
4. **Exportadores**: Agregar nuevos `ExportManager`

## 📊 Métricas y Monitoreo

### Logging Estructurado
- Logs por capa con niveles específicos
- Tracking de operaciones IA con métricas
- Monitoreo de performance y errores

### Métricas de Sistema
- Tiempo de procesamiento por análisis
- Uso de tokens OpenAI
- Tasa de éxito/error de análisis IA
- Memoria y CPU utilizada

## 🚀 Escalabilidad y Futuro

### Preparado para Escalar
- Arquitectura desacoplada permite microservicios
- Interface preparada para múltiples motores IA
- Sistema de cache integrable
- API REST extensible

### Roadmap Técnico
1. **Cache Distribuido**: Redis para análisis repetidos
2. **Multi-Model**: Soporte Claude, Gemini, modelos locales
3. **Streaming**: Análisis en tiempo real
4. **API REST**: Servicios web para integración externa

---

**Arquitectura**: Clean Architecture + SOLID + DDD  
**Tecnología IA**: OpenAI GPT-4  
**Framework**: Streamlit + Python 3.12  
**Estado**: ✅ Producción Estable