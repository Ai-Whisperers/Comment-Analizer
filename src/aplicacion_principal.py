"""
Aplicación Principal - Fachada que orquesta todo el sistema
"""
import logging
from typing import Dict, Any, Optional
from datetime import datetime

from .infrastructure.dependency_injection.contenedor_dependencias import ContenedorDependencias
from .application.use_cases.analizar_comentarios_caso_uso import (
    AnalizarComentariosCasoUso, 
    ComandoAnalisisComentarios
)
from .application.dtos.resultado_analisis import ResultadoAnalisis
from .shared.exceptions.archivo_exception import ArchivoException
from .shared.exceptions.ia_exception import IAException


logger = logging.getLogger(__name__)


class AnalizadorComentariosApp:
    """
    Fachada principal de la aplicación que proporciona una interfaz
    simplificada para el análisis de comentarios
    """
    
    def __init__(self, configuracion: Dict[str, Any] = None):
        """
        Inicializa la aplicación con la configuración proporcionada
        """
        self.configuracion = configuracion or {}
        self.contenedor = ContenedorDependencias(self.configuracion)
        self.caso_uso_analisis = self.contenedor.obtener_caso_uso_analisis()
        
        logger.info("🚀 Aplicación de análisis de comentarios inicializada")
        logger.info(f"📊 Estadísticas: {self.contenedor.obtener_estadisticas_configuracion()}")
    
    def analizar_archivo(
        self, 
        archivo_cargado, 
        nombre_archivo: str,
        incluir_analisis_avanzado: bool = True,
        limpiar_datos_anteriores: bool = True
    ) -> ResultadoAnalisis:
        """
        Analiza un archivo de comentarios
        
        Args:
            archivo_cargado: El archivo cargado (Excel/CSV)
            nombre_archivo: Nombre del archivo
            incluir_analisis_avanzado: Si incluir análisis de temas, urgencia, etc.
            limpiar_datos_anteriores: Si limpiar el repositorio antes del análisis
            
        Returns:
            ResultadoAnalisis con los resultados del análisis
        """
        logger.info(f"🔍 Iniciando análisis de archivo: {nombre_archivo}")
        
        try:
            # Validar archivo
            if not self._validar_archivo(archivo_cargado, nombre_archivo):
                return ResultadoAnalisis(
                    exito=False,
                    mensaje="Archivo no válido o formato no soportado",
                    total_comentarios=0,
                    estadisticas_sentimientos={},
                    comentarios_criticos=0,
                    temas_principales={},
                    comentarios_alta_calidad=0,
                    fecha_analisis=datetime.now()
                )
            
            # Crear comando
            comando = ComandoAnalisisComentarios(
                archivo_cargado=archivo_cargado,
                nombre_archivo=nombre_archivo,
                incluir_analisis_avanzado=incluir_analisis_avanzado,
                limpiar_repositorio=limpiar_datos_anteriores
            )
            
            # Ejecutar análisis
            resultado = self.caso_uso_analisis.ejecutar(comando)
            
            # Log resultado
            if resultado.es_exitoso():
                logger.info(f"✅ Análisis exitoso: {resultado.obtener_resumen()}")
            else:
                logger.error(f"❌ Error en análisis: {resultado.mensaje}")
            
            return resultado
            
        except ArchivoException as e:
            logger.error(f"📄 Error de archivo: {str(e)}")
            return self._crear_resultado_error(f"Error procesando archivo: {str(e)}")
            
        except IAException as e:
            logger.error(f"🤖 Error de IA: {str(e)}")
            return self._crear_resultado_error(f"Error en análisis con IA: {str(e)}")
            
        except Exception as e:
            logger.error(f"💥 Error inesperado: {str(e)}")
            return self._crear_resultado_error(f"Error inesperado: {str(e)}")
    
    def obtener_comentarios_criticos(self) -> list:
        """
        Obtiene los comentarios que requieren atención crítica
        """
        try:
            repositorio = self.contenedor.obtener_repositorio_comentarios()
            comentarios_criticos = repositorio.buscar_criticos()
            
            logger.info(f"🚨 Encontrados {len(comentarios_criticos)} comentarios críticos")
            return comentarios_criticos
            
        except Exception as e:
            logger.error(f"Error obteniendo comentarios críticos: {str(e)}")
            return []
    
    def obtener_estadisticas_repositorio(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas del repositorio actual
        """
        try:
            repositorio = self.contenedor.obtener_repositorio_comentarios()
            estadisticas = repositorio.obtener_estadisticas()
            
            return {
                **estadisticas,
                'configuracion': self.contenedor.obtener_estadisticas_configuracion(),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error obteniendo estadísticas: {str(e)}")
            return {}
    
    def limpiar_datos(self) -> bool:
        """
        Limpia todos los datos del repositorio
        """
        try:
            repositorio = self.contenedor.obtener_repositorio_comentarios()
            repositorio.limpiar()
            
            # Limpiar cache de dependencias si es necesario
            self.contenedor.limpiar_cache()
            
            logger.info("🧹 Datos limpiados exitosamente")
            return True
            
        except Exception as e:
            logger.error(f"Error limpiando datos: {str(e)}")
            return False
    
    def configurar_openai(self, api_key: str, modelo: str = "gpt-4") -> bool:
        """
        Configura dinámicamente la API de OpenAI
        """
        try:
            self.configuracion['openai_api_key'] = api_key
            self.configuracion['openai_modelo'] = modelo
            
            # Recrear contenedor con nueva configuración
            self.contenedor = ContenedorDependencias(self.configuracion)
            self.caso_uso_analisis = self.contenedor.obtener_caso_uso_analisis()
            
            logger.info(f"🤖 OpenAI configurado: modelo {modelo}")
            return True
            
        except Exception as e:
            logger.error(f"Error configurando OpenAI: {str(e)}")
            return False
    
    def _validar_archivo(self, archivo_cargado, nombre_archivo: str) -> bool:
        """
        Valida que el archivo sea procesable
        """
        if not archivo_cargado:
            return False
        
        lector = self.contenedor.obtener_lector_archivos()
        return lector.es_formato_soportado(nombre_archivo)
    
    def _crear_resultado_error(self, mensaje: str) -> ResultadoAnalisis:
        """
        Crea un resultado de error estandarizado
        """
        return ResultadoAnalisis(
            exito=False,
            mensaje=mensaje,
            total_comentarios=0,
            estadisticas_sentimientos={},
            comentarios_criticos=0,
            temas_principales={},
            comentarios_alta_calidad=0,
            fecha_analisis=datetime.now()
        )
    
    def obtener_info_sistema(self) -> Dict[str, Any]:
        """
        Obtiene información sobre el estado del sistema
        """
        return {
            'version': '2.0.0-clean-architecture',
            'configuracion_actual': self.contenedor.obtener_estadisticas_configuracion(),
            'repositorio_estadisticas': self.obtener_estadisticas_repositorio(),
            'timestamp': datetime.now().isoformat(),
            'arquitectura': 'Clean Architecture + SOLID + DDD'
        }


# Factory function para facilitar la creación
def crear_aplicacion(openai_api_key: str = None, **configuracion_adicional) -> AnalizadorComentariosApp:
    """
    Factory function para crear una instancia de la aplicación
    """
    configuracion = {
        'openai_api_key': openai_api_key,
        **configuracion_adicional
    }
    
    return AnalizadorComentariosApp(configuracion)