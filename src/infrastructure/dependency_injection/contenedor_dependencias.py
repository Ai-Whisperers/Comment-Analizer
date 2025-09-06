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
from ..external_services.analizador_maestro_ia import AnalizadorMaestroIA
from ..file_handlers.lector_archivos_excel import LectorArchivosExcel
from ..repositories.repositorio_comentarios_memoria import RepositorioComentariosMemoria
from ..text_processing.procesador_texto_basico import ProcesadorTextoBasico
# DetectorTemasHibrido eliminated - Pure IA system


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
    
    # Caso de uso estándar eliminado - Solo sistema IA maestro
    
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
    
    # Detector temas eliminado - Sistema IA maestro lo maneja internamente
    
    def obtener_servicio_sentimientos(self) -> ServicioAnalisisSentimientos:
        """
        Obtiene el servicio de análisis de sentimientos con analizadores configurados
        """
        return self._obtener_singleton('servicio_sentimientos',
                                     lambda: self._crear_servicio_sentimientos())
    
    def obtener_analizador_maestro_ia(self) -> AnalizadorMaestroIA:
        """
        Obtiene el analizador maestro IA para análisis completo
        """
        return self._obtener_singleton('analizador_maestro_ia',
                                     lambda: self._crear_analizador_maestro_ia())
    
    def obtener_caso_uso_maestro(self):
        """
        Obtiene el caso de uso maestro IA
        """
        try:
            from ...application.use_cases.analizar_excel_maestro_caso_uso import AnalizarExcelMaestroCasoUso
            return self._obtener_singleton('caso_uso_maestro',
                                         lambda: AnalizarExcelMaestroCasoUso(
                                             repositorio_comentarios=self.obtener_repositorio_comentarios(),
                                             lector_archivos=self.obtener_lector_archivos(),
                                             analizador_maestro=self.obtener_analizador_maestro_ia(),
                                             max_comments_per_batch=self.configuracion.get('max_comments', 42)
                                         ))
        except ImportError as e:
            logger.error(f"Error importando caso de uso maestro: {str(e)}")
            return None
    
    def obtener_caso_uso_analisis(self):
        """
        Obtiene el caso de uso de análisis - Alias para mantener compatibilidad
        con aplicacion_principal.py que espera este método
        """
        # Sistema refactorizado para usar solo IA maestro
        # Este método es un alias para mantener compatibilidad hacia atrás
        return self.obtener_caso_uso_maestro()
    
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
        
        # Pure IA system - no fallback rules
        if not analizadores:
            logger.error("No hay analizadores IA disponibles. OpenAI API key requerida.")
            raise ValueError("Sistema IA requiere OpenAI API key configurada")
        
        return ServicioAnalisisSentimientos(analizadores)
    
    def _crear_analizador_maestro_ia(self) -> AnalizadorMaestroIA:
        """
        Crea el analizador maestro IA con configuración optimizada
        """
        openai_key = self.configuracion.get('openai_api_key')
        if not openai_key:
            raise ValueError("OpenAI API key es requerida para análisis IA")
        
        try:
            analizador = AnalizadorMaestroIA(
                api_key=openai_key,
                modelo=self.configuracion.get('openai_modelo', 'gpt-4'),
                usar_cache=True,
                temperatura=self.configuracion.get('openai_temperatura', 0.0),
                cache_ttl=self.configuracion.get('cache_ttl', 3600),
                max_tokens=self.configuracion.get('openai_max_tokens', 8000)
            )
            
            if analizador.disponible:
                logger.info("AnalizadorMaestroIA configurado exitosamente")
                return analizador
            else:
                raise ValueError("AnalizadorMaestroIA no está disponible")
                
        except Exception as e:
            logger.error(f"Error configurando AnalizadorMaestroIA: {str(e)}")
            raise ValueError(f"Error en configuración IA: {str(e)}")
    
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