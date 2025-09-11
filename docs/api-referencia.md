# Referencia API - Analizador de Comentarios IA

## Arquitectura de la API Interna

El sistema está construido con Clean Architecture, proporcionando una API interna bien definida entre capas.

## 🏗️ Capa de Dominio (Domain)

### Entidades

#### Comentario
```python
from src.domain.entities.comentario import Comentario

class Comentario:
    """Entidad principal que representa un comentario"""
    
    def __init__(self, texto: str, fecha: Optional[datetime] = None, 
                 calificacion: Optional[int] = None):
        self.id: str                    # UUID único
        self.texto: str                 # Contenido del comentario
        self.fecha: Optional[datetime]  # Fecha del comentario
        self.calificacion: Optional[int] # Calificación 1-10
        self.fecha_creacion: datetime   # Timestamp de creación
        
    def es_valido(self) -> bool:
        """Valida que el comentario tenga contenido válido"""
        
    def obtener_longitud_texto(self) -> int:
        """Retorna la longitud del texto del comentario"""
```

#### AnalisisComentario
```python
from src.domain.entities.analisis_comentario import AnalisisComentario

class AnalisisComentario:
    """Entidad que representa el análisis de un comentario"""
    
    def __init__(self, comentario_id: str, sentimiento: Sentimiento,
                 emocion_principal: Emocion, temas: List[TemaPrincipal]):
        self.comentario_id: str
        self.sentimiento: Sentimiento
        self.emocion_principal: Emocion
        self.emociones_secundarias: List[Emocion]
        self.temas: List[TemaPrincipal]
        self.puntos_dolor: List[PuntoDolor]
        self.confianza: float           # 0.0 - 1.0
        self.fecha_analisis: datetime
        
    def es_analisis_confiable(self, umbral: float = 0.8) -> bool:
        """Determina si el análisis es confiable según umbral"""
```

### Value Objects

#### Sentimiento
```python
from src.domain.value_objects.sentimiento import Sentimiento, TipoSentimiento

class TipoSentimiento(Enum):
    POSITIVO = "positivo"
    NEGATIVO = "negativo" 
    NEUTRAL = "neutral"

class Sentimiento:
    def __init__(self, tipo: TipoSentimiento, intensidad: float):
        self.tipo: TipoSentimiento      # Tipo de sentimiento
        self.intensidad: float          # 0.0 - 1.0
        
    def es_muy_positivo(self) -> bool:
        """Retorna True si es positivo con alta intensidad (>0.8)"""
        
    def es_muy_negativo(self) -> bool:
        """Retorna True si es negativo con alta intensidad (>0.8)"""
```

#### Emocion
```python
from src.domain.value_objects.emocion import Emocion, TipoEmocion

class TipoEmocion(Enum):
    ALEGRIA = "alegria"
    TRISTEZA = "tristeza"
    FRUSTRACION = "frustracion"
    SATISFACCION = "satisfaccion"
    ENOJO = "enojo"
    GRATITUD = "gratitud"
    PREOCUPACION = "preocupacion"
    CONFIANZA = "confianza"
    DECEPCION = "decepcion"
    ESPERANZA = "esperanza"
    # ... hasta 20+ emociones

class Emocion:
    def __init__(self, tipo: TipoEmocion, intensidad: float):
        self.tipo: TipoEmocion
        self.intensidad: float          # 0.0 - 10.0
        
    def es_emocion_intensa(self, umbral: float = 7.0) -> bool:
        """Determina si la emoción es intensa"""
```

#### PuntoDolor
```python
from src.domain.value_objects.punto_dolor import PuntoDolor, SeveridadDolor

class SeveridadDolor(Enum):
    BAJA = "baja"
    MEDIA = "media"
    ALTA = "alta"
    CRITICA = "critica"

class PuntoDolor:
    def __init__(self, descripcion: str, severidad: SeveridadDolor,
                 categoria: str, frecuencia: int = 1):
        self.descripcion: str
        self.severidad: SeveridadDolor
        self.categoria: str             # e.g., "tecnico", "atencion", "precio"
        self.frecuencia: int            # Cuántas veces se menciona
        
    def requiere_atencion_inmediata(self) -> bool:
        """True si severidad es ALTA o CRITICA"""
```

### Servicios de Dominio

#### AnalizadorSentimientos
```python
from src.domain.services.analizador_sentimientos import AnalizadorSentimientos

class AnalizadorSentimientos:
    """Servicio de dominio para lógica de análisis de sentimientos"""
    
    def calcular_sentimiento_general(self, comentarios: List[Comentario]) -> Sentimiento:
        """Calcula el sentimiento general de una lista de comentarios"""
        
    def identificar_comentarios_criticos(self, analisis: List[AnalisisComentario]) -> List[str]:
        """Identifica IDs de comentarios que requieren atención inmediata"""
        
    def calcular_distribucion_sentimientos(self, analisis: List[AnalisisComentario]) -> Dict[str, int]:
        """Calcula distribución porcentual de sentimientos"""
```

## 🚀 Capa de Aplicación (Application)

### Casos de Uso

#### AnalizarExcelMaestroCasoUso
```python
from src.application.use_cases.analizar_excel_maestro_caso_uso import AnalizarExcelMaestroCasoUso

class AnalizarExcelMaestroCasoUso:
    """Caso de uso principal para análisis completo de archivos Excel"""
    
    def __init__(self, lector_archivos: LectorArchivos,
                 analizador_maestro: AnalizadorMaestroIA,
                 repositorio: RepositorioComentarios):
        # Inyección de dependencias
        
    async def ejecutar(self, archivo_path: str) -> AnalisisCompletoIA:
        """
        Ejecuta análisis completo de archivo Excel
        
        Args:
            archivo_path: Ruta al archivo Excel/CSV
            
        Returns:
            AnalisisCompletoIA: Resultado completo del análisis
            
        Raises:
            ArchivoException: Error al procesar archivo
            IAException: Error en análisis de IA
        """
        
    def validar_archivo(self, archivo_path: str) -> bool:
        """Valida que el archivo sea procesable"""
        
    def obtener_progreso_actual(self) -> float:
        """Retorna progreso actual del análisis (0.0-1.0)"""
```

### DTOs (Data Transfer Objects)

#### AnalisisCompletoIA
```python
from src.application.dtos.analisis_completo_ia import AnalisisCompletoIA

@dataclass
class AnalisisCompletoIA:
    """DTO principal con resultado completo del análisis IA"""
    
    # Métricas básicas
    total_comentarios: int
    comentarios_validos: int
    confianza_general: float            # 0.0 - 1.0
    tiempo_procesamiento: float         # segundos
    
    # Análisis de sentimientos
    distribucion_sentimientos: Dict[str, int]  # {"positivo": 65, "negativo": 20, ...}
    sentimiento_promedio: float         # -1.0 (muy negativo) a 1.0 (muy positivo)
    
    # Análisis de emociones
    emociones_predominantes: Dict[str, float]  # {"satisfaccion": 8.5, "frustracion": 3.2}
    emociones_por_comentario: List[Dict[str, float]]
    
    # Temas identificados
    temas_mas_relevantes: Dict[str, float]     # {"calidad_servicio": 0.85, "atencion": 0.62}
    temas_por_comentario: List[List[str]]
    
    # Puntos de dolor
    dolores_mas_severos: Dict[str, float]      # {"conectividad": 0.78, "soporte": 0.45}
    puntos_dolor_criticos: List[Dict[str, Any]]
    
    # Insights generados por IA
    resumen_ejecutivo: str              # Narrativa generada por GPT-4
    recomendaciones_principales: List[str]
    comentarios_destacados: List[str]   # Comentarios más relevantes
    
    # Datos adicionales
    tendencias_temporales: Optional[Dict[str, List[float]]]
    correlaciones: Optional[Dict[str, float]]
    metadatos: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        """Convierte DTO a diccionario para serialización"""
        
    @classmethod 
    def from_dict(cls, data: Dict[str, Any]) -> 'AnalisisCompletoIA':
        """Crea DTO desde diccionario"""
        
    def obtener_metricas_clave(self) -> Dict[str, Any]:
        """Retorna métricas principales para dashboard"""
        
    def es_analisis_confiable(self, umbral: float = 0.8) -> bool:
        """Determina si el análisis general es confiable"""
```

#### ResultadoAnalisis
```python
from src.application.dtos.resultado_analisis import ResultadoAnalisis

@dataclass
class ResultadoAnalisis:
    """DTO para resultado de análisis individual"""
    
    comentario_id: str
    texto_original: str
    sentimiento: str                    # "positivo", "negativo", "neutral"
    intensidad_sentimiento: float       # 0.0 - 1.0
    emocion_principal: str
    intensidad_emocion: float           # 0.0 - 10.0
    temas_identificados: List[str]
    puntos_dolor: List[str]
    confianza: float                    # 0.0 - 1.0
    
    def es_comentario_critico(self) -> bool:
        """Determina si el comentario requiere atención inmediata"""
```

### Interfaces

#### LectorArchivos
```python
from src.application.interfaces.lector_archivos import LectorArchivos

class LectorArchivos(ABC):
    """Interface para lectura de archivos"""
    
    @abstractmethod
    async def leer_archivo(self, archivo_path: str) -> List[Comentario]:
        """Lee archivo y retorna lista de comentarios"""
        
    @abstractmethod
    def validar_archivo(self, archivo_path: str) -> bool:
        """Valida formato y estructura del archivo"""
        
    @abstractmethod
    def detectar_columnas(self, archivo_path: str) -> Dict[str, str]:
        """Detecta automáticamente columnas de comentarios, fecha, calificación"""
        
    @abstractmethod
    def obtener_metadatos(self, archivo_path: str) -> Dict[str, Any]:
        """Obtiene metadatos del archivo (tamaño, filas, etc.)"""
```

#### ProcesadorTexto
```python
from src.application.interfaces.procesador_texto import ProcesadorTexto

class ProcesadorTexto(ABC):
    """Interface para procesamiento de texto con IA"""
    
    @abstractmethod
    async def analizar_sentimientos(self, textos: List[str]) -> List[Sentimiento]:
        """Analiza sentimientos de lista de textos"""
        
    @abstractmethod
    async def detectar_emociones(self, textos: List[str]) -> List[List[Emocion]]:
        """Detecta emociones en textos"""
        
    @abstractmethod
    async def identificar_temas(self, textos: List[str]) -> List[List[str]]:
        """Identifica temas principales en textos"""
        
    @abstractmethod
    async def analizar_completo(self, textos: List[str]) -> AnalisisCompletoIA:
        """Análisis completo con una sola llamada (GPT-4)"""
```

## ⚙️ Capa de Infraestructura (Infrastructure)

### Servicios Externos

#### AnalizadorMaestroIA
```python
from src.infrastructure.external_services.analizador_maestro_ia import AnalizadorMaestroIA

class AnalizadorMaestroIA:
    """Motor principal de IA que implementa ProcesadorTexto"""
    
    def __init__(self, client: OpenAI, config_manager: AIConfigurationManager):
        self.client = client
        self.config_manager = config_manager
        self.progress_tracker = AIProgressTracker()
        self.retry_strategy = IntelligentRetryStrategy()
        
    async def analizar_comentarios_completo(self, comentarios: List[str], 
                                          callback_progreso: Optional[Callable] = None) -> AnalisisCompletoIA:
        """
        Análisis completo con GPT-4 en una sola llamada
        
        Args:
            comentarios: Lista de textos a analizar
            callback_progreso: Función callback para updates de progreso
            
        Returns:
            AnalisisCompletoIA: Resultado completo del análisis
            
        Raises:
            OpenAIServiceException: Error de servicio OpenAI
            IAException: Error de procesamiento IA
        """
        
    def _construir_prompt_maestro(self, comentarios: List[str]) -> str:
        """Construye prompt optimizado para GPT-4"""
        
    def _parsear_respuesta_ia(self, respuesta: str) -> Dict[str, Any]:
        """Parsea y valida respuesta JSON de GPT-4"""
        
    def _validar_respuesta_ia(self, data: Dict) -> bool:
        """Valida estructura de respuesta IA"""
        
    def obtener_configuracion_actual(self) -> Dict[str, Any]:
        """Retorna configuración actual del motor IA"""
        
    def estimar_costo_analisis(self, num_comentarios: int) -> float:
        """Estima costo en USD para análisis de N comentarios"""
```

#### LectorArchivosExcel
```python
from src.infrastructure.file_handlers.lector_archivos_excel import LectorArchivosExcel

class LectorArchivosExcel:
    """Implementación concreta de LectorArchivos para Excel/CSV"""
    
    def __init__(self):
        self.columnas_detectadas = {}
        self.metadatos = {}
        
    async def leer_archivo(self, archivo_path: str) -> List[Comentario]:
        """Implementación de lectura de archivos Excel/CSV"""
        
    def detectar_columnas(self, archivo_path: str) -> Dict[str, str]:
        """
        Detecta automáticamente columnas relevantes
        
        Returns:
            Dict con keys: 'comentario', 'fecha', 'calificacion'
        """
        
    def _detectar_columna_comentarios(self, df: pd.DataFrame) -> Optional[str]:
        """Detecta columna que contiene comentarios"""
        
    def _detectar_columna_fechas(self, df: pd.DataFrame) -> Optional[str]:
        """Detecta columna que contiene fechas"""
        
    def _limpiar_texto_comentario(self, texto: str) -> str:
        """Limpia y normaliza texto de comentarios"""
        
    def obtener_estadisticas_archivo(self, archivo_path: str) -> Dict[str, Any]:
        """Obtiene estadísticas del archivo cargado"""
```

### Contenedor de Dependencias

#### ContenedorDependencias
```python
from src.infrastructure.dependency_injection.contenedor_dependencias import ContenedorDependencias

class ContenedorDependencias:
    """Contenedor principal de inyección de dependencias"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self._instances = {}
        self._configurar_dependencias()
        
    def obtener_caso_uso_maestro(self) -> AnalizarExcelMaestroCasoUso:
        """Retorna caso de uso principal configurado con dependencias"""
        
    def obtener_analizador_maestro(self) -> AnalizadorMaestroIA:
        """Retorna analizador IA configurado"""
        
    def obtener_lector_archivos(self) -> LectorArchivos:
        """Retorna lector de archivos configurado"""
        
    def obtener_repositorio_comentarios(self) -> RepositorioComentarios:
        """Retorna repositorio de comentarios"""
        
    def obtener_openai_client(self) -> OpenAI:
        """Retorna cliente OpenAI configurado"""
        
    def reconfigurar(self, nueva_config: Dict[str, Any]):
        """Reconfigura contenedor con nuevos parámetros"""
        
    def limpiar_cache(self):
        """Limpia cache interno de instancias"""
```

## 🎨 Capa de Presentación (Presentation)

### Sistema CSS

#### EnhancedCSSLoader
```python
from src.presentation.streamlit.enhanced_css_loader import ensure_css_loaded, load_custom_css

def ensure_css_loaded():
    """Asegura que el CSS esté cargado en Streamlit"""
    
def load_custom_css(css_content: str):
    """Carga CSS personalizado"""
    
def apply_glassmorphism_theme():
    """Aplica tema glassmorphism al sistema"""
    
def get_available_themes() -> List[str]:
    """Retorna temas CSS disponibles"""
```

### Progress Tracking

#### ProgressTracker
```python
from src.presentation.streamlit.progress_tracker import ProgressTracker

class ProgressTracker:
    """Maneja visualización de progreso en Streamlit"""
    
    def __init__(self):
        self.progreso_actual = 0.0
        self.mensaje_actual = ""
        self.container = None
        
    def inicializar(self, container: st.container):
        """Inicializa tracker con container de Streamlit"""
        
    def actualizar_progreso(self, progreso: float, mensaje: str):
        """
        Actualiza progreso visual
        
        Args:
            progreso: 0.0 - 1.0
            mensaje: Mensaje descriptivo de estado actual
        """
        
    def finalizar(self, mensaje_final: str = "Análisis completado"):
        """Finaliza tracking con mensaje final"""
        
    def mostrar_error(self, error: str):
        """Muestra error en UI de progreso"""
```

## 📊 Utilidades y Helpers

### Validadores

```python
from src.shared.validators.archivo_validator import ArchivoValidator
from src.shared.validators.comentario_validator import ComentarioValidator

class ArchivoValidator:
    @staticmethod
    def validar_tamaño(archivo_path: str, max_mb: float) -> bool:
        """Valida tamaño de archivo"""
        
    @staticmethod
    def validar_formato(archivo_path: str) -> bool:
        """Valida formato de archivo (Excel/CSV)"""
        
    @staticmethod
    def validar_contenido(df: pd.DataFrame) -> bool:
        """Valida que el DataFrame tenga contenido válido"""

class ComentarioValidator:
    @staticmethod
    def es_comentario_valido(texto: str) -> bool:
        """Valida que el texto sea un comentario válido"""
        
    @staticmethod
    def limpiar_comentario(texto: str) -> str:
        """Limpia y normaliza comentario"""
```

### Excepciones Personalizadas

```python
from src.shared.exceptions.ia_exception import IAException, OpenAIServiceException
from src.shared.exceptions.archivo_exception import ArchivoException

class IAException(Exception):
    """Excepción base para errores de IA"""
    def __init__(self, message: str, code: str = None):
        self.message = message
        self.code = code
        super().__init__(self.message)

class OpenAIServiceException(IAException):
    """Excepción específica para errores de OpenAI"""
    def __init__(self, message: str, status_code: int = None, 
                 rate_limited: bool = False):
        super().__init__(message)
        self.status_code = status_code
        self.rate_limited = rate_limited

class ArchivoException(Exception):
    """Excepción para errores de procesamiento de archivos"""
    def __init__(self, message: str, file_path: str = None):
        self.message = message
        self.file_path = file_path
        super().__init__(self.message)
```

## 🔧 Configuración y Factory

### Factory Principal

```python
from src.aplicacion_principal import crear_aplicacion, AplicacionPrincipal

def crear_aplicacion(config: Dict[str, Any]) -> AplicacionPrincipal:
    """
    Factory method principal para crear aplicación configurada
    
    Args:
        config: Diccionario de configuración del sistema
        
    Returns:
        AplicacionPrincipal: Instancia configurada de la aplicación
        
    Raises:
        ConfigurationException: Error en configuración
    """

class AplicacionPrincipal:
    """Fachada principal del sistema"""
    
    def __init__(self, contenedor: ContenedorDependencias):
        self.contenedor = contenedor
        
    async def analizar_archivo_excel(self, archivo_path: str) -> AnalisisCompletoIA:
        """Método principal para análisis de archivos"""
        
    def obtener_configuracion_actual(self) -> Dict[str, Any]:
        """Retorna configuración actual del sistema"""
        
    def validar_sistema(self) -> bool:
        """Valida que el sistema esté correctamente configurado"""
```

## 🧪 Testing Helpers

### Mocks y Fixtures

```python
# Para testing
from src.infrastructure.external_services.mock_analizador_ia import MockAnalizadorIA

class MockAnalizadorIA:
    """Mock del analizador IA para testing"""
    
    def __init__(self, respuestas_predefinidas: List[AnalisisCompletoIA] = None):
        self.respuestas = respuestas_predefinidas or []
        self.llamadas = []
        
    async def analizar_comentarios_completo(self, comentarios: List[str]) -> AnalisisCompletoIA:
        """Mock de análisis que retorna respuesta predefinida"""
        self.llamadas.append(comentarios)
        return self.respuestas[0] if self.respuestas else self._generar_respuesta_mock()
```

## 📖 Ejemplos de Uso

### Uso Básico del API

```python
# Ejemplo de uso del API interno
import asyncio
from src.aplicacion_principal import crear_aplicacion
from config import config

async def ejemplo_uso_basico():
    # 1. Crear aplicación
    app = crear_aplicacion(config)
    
    # 2. Analizar archivo
    resultado = await app.analizar_archivo_excel("datos/comentarios.xlsx")
    
    # 3. Procesar resultados
    print(f"Comentarios analizados: {resultado.total_comentarios}")
    print(f"Sentimiento general: {resultado.sentimiento_promedio}")
    
    # 4. Obtener métricas clave
    metricas = resultado.obtener_metricas_clave()
    print(f"Métricas: {metricas}")

# Ejecutar ejemplo
asyncio.run(ejemplo_uso_basico())
```

### Uso Avanzado con Callbacks

```python
async def ejemplo_con_progreso():
    app = crear_aplicacion(config)
    
    def callback_progreso(progreso: float, mensaje: str):
        print(f"Progreso: {progreso:.1%} - {mensaje}")
    
    # Obtener caso de uso con callback
    caso_uso = app.contenedor.obtener_caso_uso_maestro()
    
    # Ejecutar con callback de progreso
    resultado = await caso_uso.ejecutar(
        "datos/comentarios.xlsx",
        callback_progreso=callback_progreso
    )
    
    print(f"Análisis completado: {resultado.resumen_ejecutivo}")
```

### Configuración Personalizada

```python
def ejemplo_configuracion_personalizada():
    config_custom = {
        'openai_model': 'gpt-3.5-turbo',  # Modelo más rápido
        'openai_max_tokens': 3000,        # Menos tokens
        'max_comments': 500,              # Menos comentarios
        'log_level': 'DEBUG'              # Más logging
    }
    
    app = crear_aplicacion(config_custom)
    
    # Verificar configuración
    config_actual = app.obtener_configuracion_actual()
    print(f"Configuración aplicada: {config_actual}")
    
    return app
```

---

**Documentación API**: Completa con ejemplos prácticos  
**Cobertura**: Todas las capas de Clean Architecture  
**Estado**: ✅ Funcional y probado  
**Versión**: 3.0.0-ia-pure