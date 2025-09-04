"""
Contenedor de inyección de dependencias
"""
import logging
from typing import Dict, Any, Optional

from ...domain.services.analizador_sentimientos import ServicioAnalisisSentimientos, IAnalizadorSentimientos
from ...domain.repositories.repositorio_comentarios import IRepositorioComentarios
from ...application.use_cases.analizar_comentarios_caso_uso import AnalizarComentariosCasoUso
from ...application.interfaces.lector_archivos import ILectorArchivos
from ...application.interfaces.procesador_texto import IProcesadorTexto
from ...application.interfaces.detector_temas import IDetectorTemas

from ..external_services.analizador_openai import AnalizadorOpenAI
from ..external_services.analizador_reglas import AnalizadorReglas
from ..file_handlers.lector_archivos_excel import LectorArchivosExcel
from ..repositories.repositorio_comentarios_memoria import RepositorioComentariosMemoria
from ..text_processing.procesador_texto_basico import ProcesadorTextoBasico
from ..text_processing.detector_temas_hibrido import DetectorTemasHibrido


logger = logging.getLogger(__name__)


class ContenedorDependencias:
    """
    Contenedor de inyección de dependencias que maneja la creación 
    e inyección de todas las dependencias del sistema
    """
    
    def __init__(self, configuracion: Dict[str, Any]):
        """
        Inicializa el contenedor con la configuración del sistema
        """
        self.configuracion = configuracion
        self._servicios_registrados = {}
        self._instancias_singleton = {}
        
        # Registrar servicios por defecto
        self._registrar_servicios_por_defecto()
    
    def obtener_caso_uso_analisis(self) -> AnalizarComentariosCasoUso:
        """
        Obtiene el caso de uso principal configurado con todas sus dependencias
        """
        return AnalizarComentariosCasoUso(
            repositorio_comentarios=self.obtener_repositorio_comentarios(),
            lector_archivos=self.obtener_lector_archivos(),
            procesador_texto=self.obtener_procesador_texto(),
            detector_temas=self.obtener_detector_temas(),
            servicio_sentimientos=self.obtener_servicio_sentimientos()
        )
    
    def obtener_repositorio_comentarios(self) -> IRepositorioComentarios:
        """
        Obtiene la implementación del repositorio de comentarios
        """
        return self._obtener_singleton('repositorio_comentarios', 
                                     lambda: RepositorioComentariosMemoria())
    
    def obtener_lector_archivos(self) -> ILectorArchivos:
        """
        Obtiene la implementación del lector de archivos
        """
        return self._obtener_singleton('lector_archivos',
                                     lambda: LectorArchivosExcel())
    
    def obtener_procesador_texto(self) -> IProcesadorTexto:
        """
        Obtiene la implementación del procesador de texto
        """
        return self._obtener_singleton('procesador_texto',
                                     lambda: ProcesadorTextoBasico())
    
    def obtener_detector_temas(self) -> IDetectorTemas:
        """
        Obtiene la implementación del detector de temas
        """
        openai_key = self.configuracion.get('openai_api_key')
        return self._obtener_singleton('detector_temas',
                                     lambda: DetectorTemasHibrido(openai_key))
    
    def obtener_servicio_sentimientos(self) -> ServicioAnalisisSentimientos:
        """
        Obtiene el servicio de análisis de sentimientos con analizadores configurados
        """
        return self._obtener_singleton('servicio_sentimientos',
                                     lambda: self._crear_servicio_sentimientos())
    
    def _crear_servicio_sentimientos(self) -> ServicioAnalisisSentimientos:
        """
        Crea el servicio de sentimientos con los analizadores apropiados
        """
        analizadores = []
        
        # Intentar crear analizador OpenAI si hay API key
        openai_key = self.configuracion.get('openai_api_key')
        if openai_key:
            try:
                analizador_openai = AnalizadorOpenAI(
                    api_key=openai_key,
                    modelo=self.configuracion.get('openai_modelo', 'gpt-4'),
                    usar_cache=True
                )
                
                if analizador_openai.es_disponible():
                    analizadores.append(analizador_openai)
                    logger.info("✅ Analizador OpenAI configurado exitosamente")
                else:
                    logger.warning("⚠️ Analizador OpenAI no está disponible")
                    
            except Exception as e:
                logger.error(f"❌ Error configurando OpenAI: {str(e)}")
        
        # Siempre agregar analizador de reglas como fallback
        analizador_reglas = AnalizadorReglas()
        analizadores.append(analizador_reglas)
        logger.info("✅ Analizador de reglas configurado como fallback")
        
        return ServicioAnalisisSentimientos(analizadores)
    
    def _obtener_singleton(self, clave: str, factory_func) -> Any:
        """
        Obtiene una instancia singleton, creándola si no existe
        """
        if clave not in self._instancias_singleton:
            self._instancias_singleton[clave] = factory_func()
        
        return self._instancias_singleton[clave]
    
    def _registrar_servicios_por_defecto(self):
        """
        Registra las implementaciones por defecto de los servicios
        """
        # Esta función puede expandirse para registrar más servicios
        logger.info("🔧 Contenedor de dependencias inicializado")
    
    def registrar_servicio(self, clave: str, implementacion: Any):
        """
        Permite registrar manualmente un servicio
        """
        self._servicios_registrados[clave] = implementacion
        logger.info(f"📝 Servicio '{clave}' registrado manualmente")
    
    def limpiar_cache(self):
        """
        Limpia el cache de instancias singleton
        """
        self._instancias_singleton.clear()
        logger.info("🧹 Cache de dependencias limpiado")
    
    def obtener_estadisticas_configuracion(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas sobre la configuración actual
        """
        return {
            'openai_configurado': bool(self.configuracion.get('openai_api_key')),
            'servicios_registrados': len(self._servicios_registrados),
            'instancias_creadas': len(self._instancias_singleton),
            'configuracion_keys': list(self.configuracion.keys())
        }