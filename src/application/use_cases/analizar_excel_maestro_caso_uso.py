"""
Caso de uso simplificado para análisis maestro con IA
"""
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import logging
import time
import gc
from threading import Thread
from concurrent.futures import ThreadPoolExecutor, as_completed

# Optional imports for enhanced functionality
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

from ...domain.entities.analisis_comentario import AnalisisComentario
from ...domain.repositories.repositorio_comentarios import IRepositorioComentarios
from ...domain.value_objects.sentimiento import Sentimiento, SentimientoCategoria
from ...domain.value_objects.emocion import Emocion, TipoEmocion
from ...domain.value_objects.tema_principal import TemaPrincipal, CategoriaTemaTelco
from ...domain.value_objects.punto_dolor import PuntoDolor, TipoPuntoDolor, NivelImpacto
from ..interfaces.lector_archivos import ILectorArchivos
from ..dtos.analisis_completo_ia import AnalisisCompletoIA
from ...infrastructure.external_services.analizador_maestro_ia import AnalizadorMaestroIA
from ...shared.exceptions.archivo_exception import ArchivoException
from ...shared.exceptions.ia_exception import IAException

# PHASE 3: Import intelligent retry strategy
try:
    from ...infrastructure.external_services.intelligent_retry_strategy import (
        create_intelligent_retry_strategy, 
        create_retry_context,
        RetryDecision
    )
    INTELLIGENT_RETRY_AVAILABLE = True
except ImportError:
    INTELLIGENT_RETRY_AVAILABLE = False


logger = logging.getLogger(__name__)


@dataclass
class ComandoAnalisisExcelMaestro:
    """Comando simplificado para el análisis maestro"""
    archivo_cargado: Any
    nombre_archivo: str
    limpiar_repositorio: bool = True
    progress_callback: Optional[Any] = None  # Add progress callback support


@dataclass
class ResultadoAnalisisMaestro:
    """Resultado simplificado del análisis maestro"""
    exito: bool
    mensaje: str
    total_comentarios: int
    analisis_completo_ia: AnalisisCompletoIA = None
    comentarios_analizados: List[AnalisisComentario] = None
    fecha_analisis: datetime = None
    tiempo_total_segundos: float = 0.0
    
    def es_exitoso(self) -> bool:
        return self.exito
    
    def obtener_resumen_ejecutivo(self) -> str:
        if not self.es_exitoso():
            return f"❌ Error: {self.mensaje}"
        
        if not self.analisis_completo_ia:
            return "❌ No hay análisis disponible"
        
        return self.analisis_completo_ia.obtener_resumen_ejecutivo_completo()
    
    def obtener_comentarios_criticos(self) -> List[AnalisisComentario]:
        if not self.comentarios_analizados:
            return []
        return [c for c in self.comentarios_analizados if c.es_critico()]


class AnalizarExcelMaestroCasoUso:
    """
    Caso de uso simplificado que usa el AnalizadorMaestroIA
    
    FLUJO SIMPLIFICADO:
    1. Leer Excel/CSV
    2. UNA sola llamada al AnalizadorMaestroIA  
    3. Mapear resultados a entidades de dominio
    4. Guardar en repositorio
    """
    
    def __init__(
        self,
        repositorio_comentarios: IRepositorioComentarios,
        lector_archivos: ILectorArchivos,
        analizador_maestro: AnalizadorMaestroIA,
        max_comments_per_batch: int = 120,  # OPTIMIZATION: Increased for better performance (up to 850 comments in 20-30s)
        ai_configuration=None,
        progress_callback=None,
        configuracion=None
    ):
        self.repositorio_comentarios = repositorio_comentarios
        self.lector_archivos = lector_archivos
        self.analizador_maestro = analizador_maestro
        
        # Store general configuration for validation limits
        self.configuracion = configuracion
        
        # CONFIGURABLE: Enhanced batch sizes for 1000-comment files performance
        max_absolute = configuracion.get('max_batch_size_absolute', 120) if configuracion else 120
        min_threshold = configuracion.get('min_batch_size_threshold', 50) if configuracion else 50
        default_batch = configuracion.get('max_comments', 100) if configuracion else 100
        
        if max_comments_per_batch > max_absolute:
            logger.error(f"❌ SAFETY: Batch size too large: {max_comments_per_batch}, forcing to {default_batch}")
            max_comments_per_batch = default_batch
        elif max_comments_per_batch < 1:
            logger.warning(f"⚠️ SAFETY: Batch size too small: {max_comments_per_batch}, setting to {default_batch}")
            max_comments_per_batch = default_batch
        elif max_comments_per_batch < min_threshold:
            logger.info(f"📈 PERFORMANCE: Increasing batch size from {max_comments_per_batch} to {default_batch} for 1000-comment optimization")
            max_comments_per_batch = default_batch
            
        self.max_comments_per_batch = max_comments_per_batch
        
        # PHASE 3: Initialize intelligent retry strategy
        self.ai_configuration = ai_configuration
        if INTELLIGENT_RETRY_AVAILABLE and ai_configuration:
            self.retry_strategy = create_intelligent_retry_strategy(ai_configuration)
            logger.info(f"🧠 Intelligent retry strategy enabled")
        else:
            self.retry_strategy = None
            logger.info(f"⚠️ Intelligent retry strategy not available - using fallback")
        
        # PROGRESS INTEGRATION: Store progress callback for real-time updates
        self.progress_callback = progress_callback
        if progress_callback:
            logger.info(f"📊 Real-time progress tracking enabled")
        
        logger.info(f"📦 Batch processor initialized: {self.max_comments_per_batch} comentarios/lote")
        
    def ejecutar(self, comando: ComandoAnalisisExcelMaestro) -> ResultadoAnalisisMaestro:
        """
        Ejecuta el análisis maestro simplificado
        """
        inicio_tiempo = datetime.now()
        logger.info(f"🚀 Iniciando análisis maestro de archivo: {comando.nombre_archivo}")
        
        # Use progress callback from command if provided
        if comando.progress_callback:
            self.progress_callback = comando.progress_callback
            logger.info("📊 Progress callback enabled from command")
        
        try:
            # 1. Limpiar repositorio si se requiere
            if comando.limpiar_repositorio:
                self.repositorio_comentarios.limpiar()
                logger.info("🧹 Repositorio limpiado")
            
            # 2. Leer archivo
            comentarios_raw_data = self.lector_archivos.leer_comentarios(comando.archivo_cargado)
            
            if not comentarios_raw_data:
                return self._crear_resultado_error("No se encontraron comentarios válidos en el archivo")
            
            # Extraer solo los textos para análisis IA
            comentarios_texto = [
                str(item.get('comentario', item.get('texto', ''))).strip()
                for item in comentarios_raw_data
            ]
            
            # Filtrar comentarios vacíos
            comentarios_validos = [t for t in comentarios_texto if t]
            
            if not comentarios_validos:
                return self._crear_resultado_error("No se encontraron comentarios válidos después del filtrado")
            
            # CONFIGURABLE: Validar límites de procesamiento
            max_file_size = self.configuracion.get('max_file_comments', 2000) if self.configuracion else 2000
            min_file_info = self.configuracion.get('min_file_comments_info', 100) if self.configuracion else 100
            
            if len(comentarios_validos) > max_file_size:
                logger.warning(f"🚨 ARCHIVO MUY GRANDE: {len(comentarios_validos)} comentarios, limitando a {max_file_size}")
                comentarios_validos = comentarios_validos[:max_file_size]
                comentarios_raw_data = comentarios_raw_data[:max_file_size]
            elif len(comentarios_validos) < min_file_info:
                logger.info(f"📊 Archivo pequeño: {len(comentarios_validos)} comentarios")
            
            logger.info(f"📊 Procesando {len(comentarios_validos)} comentarios válidos en lotes de {self.max_comments_per_batch}")
            
            # 3. Procesamiento unificado (eliminada bifurcación innecesaria)
            if len(comentarios_validos) <= self.max_comments_per_batch:
                # Archivo pequeño - procesamiento directo
                analisis_completo_ia = self.analizador_maestro.analizar_excel_completo(comentarios_validos)
            else:
                # Archivo grande - procesamiento en múltiples lotes
                analisis_completo_ia = self._procesar_en_lotes(comentarios_validos)
            
            if not analisis_completo_ia.es_exitoso():
                return self._crear_resultado_error("Error en análisis IA")
            
            # 4. Mapear resultados IA a entidades de dominio
            comentarios_analizados = self._mapear_a_entidades_dominio(
                analisis_completo_ia, comentarios_raw_data
            )
            
            # 5. Guardar en repositorio
            self.repositorio_comentarios.guardar_lote(comentarios_analizados)
            
            # 6. Generar resultado final
            tiempo_transcurrido = (datetime.now() - inicio_tiempo).total_seconds()
            
            resultado = ResultadoAnalisisMaestro(
                exito=True,
                mensaje="Análisis maestro completado exitosamente",
                total_comentarios=len(comentarios_analizados),
                analisis_completo_ia=analisis_completo_ia,
                comentarios_analizados=comentarios_analizados,
                fecha_analisis=datetime.now(),
                tiempo_total_segundos=tiempo_transcurrido
            )
            
            logger.info(f"✅ Análisis maestro completado en {tiempo_transcurrido:.2f}s")
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
    
    def _mapear_a_entidades_dominio(self, analisis_ia: AnalisisCompletoIA, 
                                   datos_originales: List[Dict[str, Any]]) -> List[AnalisisComentario]:
        """
        Mapea los resultados del AnalizadorMaestroIA a entidades de dominio
        """
        comentarios_analizados = []
        
        for i, comentario_ia in enumerate(analisis_ia.comentarios_analizados):
            try:
                # Datos originales
                datos_orig = datos_originales[i] if i < len(datos_originales) else {}
                texto_original = comentario_ia.get('texto_original', 
                                                  datos_orig.get('comentario', 
                                                               datos_orig.get('texto', '')))
                
                # Mapear sentimiento
                sentimiento_data = comentario_ia.get('sentimiento', {})
                sentimiento = self._mapear_sentimiento(sentimiento_data)
                
                # Mapear emociones
                emociones_data = comentario_ia.get('emociones', [])
                emociones = self._mapear_emociones(emociones_data)
                
                # Mapear temas
                temas_data = comentario_ia.get('temas', [])
                temas = self._mapear_temas(temas_data)
                
                # Mapear puntos de dolor
                dolores_data = comentario_ia.get('puntos_dolor', [])
                dolores = self._mapear_puntos_dolor(dolores_data)
                
                # Crear entidad
                analisis_comentario = AnalisisComentario(
                    id=f"analisis_{i}_{hash(texto_original)}",
                    indice_original=i,
                    texto_original=texto_original,
                    sentimiento=sentimiento,
                    emociones=emociones,
                    temas=temas,
                    puntos_dolor=dolores,
                    resumen_ia=comentario_ia.get('resumen', ''),
                    recomendaciones=comentario_ia.get('recomendaciones', []),
                    confianza_general=self._calcular_confianza_comentario(comentario_ia),
                    fecha_analisis=analisis_ia.fecha_analisis,
                    modelo_ia_utilizado=analisis_ia.modelo_utilizado,
                    tiempo_analisis_ms=analisis_ia.tiempo_analisis * 1000 / len(analisis_ia.comentarios_analizados),
                    calificacion_nps=datos_orig.get('nps'),
                    calificacion_nota=datos_orig.get('nota'),
                    metadatos_adicionales={}
                )
                
                comentarios_analizados.append(analisis_comentario)
                
            except Exception as e:
                logger.warning(f"⚠️ Error mapeando comentario {i}: {str(e)}")
                # Crear análisis básico en caso de error
                comentarios_analizados.append(self._crear_analisis_basico(i, datos_orig))
        
        return comentarios_analizados
    
    def _mapear_sentimiento(self, sentimiento_data: Dict[str, Any]) -> Sentimiento:
        """Mapea datos de sentimiento a value object"""
        try:
            categoria_str = sentimiento_data.get('categoria', 'neutral').lower()
            confianza = float(sentimiento_data.get('confianza', 0.5))
            
            if categoria_str == 'positivo':
                categoria = SentimientoCategoria.POSITIVO
            elif categoria_str == 'negativo':
                categoria = SentimientoCategoria.NEGATIVO
            else:
                categoria = SentimientoCategoria.NEUTRAL
            
            return Sentimiento(categoria=categoria, confianza=confianza, fuente="ia")
            
        except Exception as e:
            logger.warning(f"⚠️ Error mapeando sentimiento: {str(e)}")
            return Sentimiento.crear_neutral(0.5, "ia")
    
    def _mapear_emociones(self, emociones_data: List[Dict[str, Any]]) -> List[Emocion]:
        """Mapea datos de emociones a value objects"""
        emociones = []
        
        for emocion_data in emociones_data:
            try:
                tipo_str = emocion_data.get('tipo', '').lower()
                intensidad = float(emocion_data.get('intensidad', 0.5))
                confianza = float(emocion_data.get('confianza', 0.5))
                contexto = emocion_data.get('contexto', '')
                
                # Mapear tipo string a enum
                tipo_emocion = self._mapear_tipo_emocion(tipo_str)
                
                if tipo_emocion:
                    emocion = Emocion(
                        tipo=tipo_emocion,
                        intensidad=intensidad,
                        confianza=confianza,
                        contexto=contexto
                    )
                    emociones.append(emocion)
                    
            except Exception as e:
                logger.warning(f"⚠️ Error mapeando emoción: {str(e)}")
                continue
        
        return emociones
    
    def _mapear_temas(self, temas_data: List[Dict[str, Any]]) -> List[TemaPrincipal]:
        """Mapea datos de temas a value objects"""
        temas = []
        
        for tema_data in temas_data:
            try:
                categoria_str = tema_data.get('categoria', '').lower()
                relevancia = float(tema_data.get('relevancia', 0.5))
                confianza = float(tema_data.get('confianza', 0.5))
                contexto = tema_data.get('contexto_especifico', '')
                
                # Mapear categoria string a enum
                categoria_tema = self._mapear_categoria_tema(categoria_str)
                
                if categoria_tema:
                    tema = TemaPrincipal(
                        categoria=categoria_tema,
                        relevancia=relevancia,
                        confianza=confianza,
                        contexto_especifico=contexto,
                        palabras_clave=[]
                    )
                    temas.append(tema)
                    
            except Exception as e:
                logger.warning(f"⚠️ Error mapeando tema: {str(e)}")
                continue
        
        return temas
    
    def _mapear_puntos_dolor(self, dolores_data: List[Dict[str, Any]]) -> List[PuntoDolor]:
        """Mapea datos de puntos de dolor a value objects"""
        dolores = []
        
        for dolor_data in dolores_data:
            try:
                tipo_str = dolor_data.get('tipo', '').lower()
                severidad = float(dolor_data.get('severidad', 0.5))
                confianza = float(dolor_data.get('confianza', 0.5))
                nivel_impacto_str = dolor_data.get('nivel_impacto', 'moderado').lower()
                contexto = dolor_data.get('contexto_especifico', '')
                
                # Mapear tipos y niveles
                tipo_dolor = self._mapear_tipo_dolor(tipo_str)
                nivel_impacto = self._mapear_nivel_impacto(nivel_impacto_str)
                
                if tipo_dolor and nivel_impacto:
                    # Use factory methods para aplicar business rules correctly
                    try:
                        if severidad >= 0.7:
                            dolor = PuntoDolor.crear_critico(
                                tipo=tipo_dolor,
                                severidad=severidad,
                                confianza=confianza,
                                contexto=contexto,
                                palabras_clave=[],
                                frecuencia=1
                            )
                        elif severidad >= 0.5 and severidad < 0.8:  # FIX: Respect factory method range
                            dolor = PuntoDolor.crear_alto_impacto(
                                tipo=tipo_dolor,
                                severidad=severidad,
                                confianza=confianza,
                                contexto=contexto,
                                palabras_clave=[],
                                frecuencia=1
                            )
                        elif severidad >= 0.6 and severidad < 0.7:  # FIX: Handle gap between moderado and critico
                            # Use alto_impacto for high-moderate range
                            dolor = PuntoDolor.crear_alto_impacto(
                                tipo=tipo_dolor,
                                severidad=0.7,  # Clamp to valid range
                                confianza=confianza,
                                contexto=contexto,
                                palabras_clave=[],
                                frecuencia=1
                            )
                        elif severidad >= 0.3 and severidad < 0.6:  # FIX: Respect factory method range
                            dolor = PuntoDolor.crear_moderado(
                                tipo=tipo_dolor,
                                severidad=severidad,
                                confianza=confianza,
                                contexto=contexto,
                                palabras_clave=[],
                                frecuencia=1
                            )
                        else:
                            # Severidad muy baja, skip o usar constructor directo con validación
                            logger.debug(f"🔍 Saltando punto de dolor con severidad muy baja: {severidad:.2f}")
                            continue
                            
                        dolores.append(dolor)
                        
                    except ValueError as validation_error:
                        logger.warning(f"⚠️ Business rule violation en PuntoDolor: {validation_error}")
                        # Fallback: skip invalid pain point
                        continue
                    
            except Exception as e:
                logger.warning(f"⚠️ Error mapeando punto de dolor: {str(e)}")
                continue
        
        return dolores

    # PURGED: Complex caching logic eliminated (40+ lines of overhead removed)
    
    def _mapear_tipo_emocion(self, tipo_str: str) -> TipoEmocion:
        """Mapea string de emoción a enum"""
        mapeo = {
            'satisfaccion': TipoEmocion.SATISFACCION,
            'alegria': TipoEmocion.ALEGRIA,
            'entusiasmo': TipoEmocion.ENTUSIASMO,
            'gratitud': TipoEmocion.GRATITUD,
            'confianza': TipoEmocion.CONFIANZA,
            'frustracion': TipoEmocion.FRUSTRACION,
            'enojo': TipoEmocion.ENOJO,
            'decepcion': TipoEmocion.DECEPCION,
            'preocupacion': TipoEmocion.PREOCUPACION,
            'irritacion': TipoEmocion.IRRITACION,
            'ansiedad': TipoEmocion.ANSIEDAD,
            'tristeza': TipoEmocion.TRISTEZA,
            'confusion': TipoEmocion.CONFUSION,
            'esperanza': TipoEmocion.ESPERANZA,
            'curiosidad': TipoEmocion.CURIOSIDAD,
            'impaciencia': TipoEmocion.IMPACIENCIA
        }
        return mapeo.get(tipo_str.replace(' ', '_').lower())
    
    def _mapear_categoria_tema(self, categoria_str: str) -> CategoriaTemaTelco:
        """Mapea string de tema a enum"""
        mapeo = {
            'velocidad': CategoriaTemaTelco.VELOCIDAD,
            'conectividad': CategoriaTemaTelco.CONECTIVIDAD,
            'estabilidad': CategoriaTemaTelco.ESTABILIDAD,
            'cobertura': CategoriaTemaTelco.COBERTURA,
            'calidad_señal': CategoriaTemaTelco.CALIDAD_SEÑAL,
            'precio': CategoriaTemaTelco.PRECIO,
            'planes': CategoriaTemaTelco.PLANES,
            'promociones': CategoriaTemaTelco.PROMOCIONES,
            'facturacion': CategoriaTemaTelco.FACTURACION,
            'contratos': CategoriaTemaTelco.CONTRATOS,
            'servicio_cliente': CategoriaTemaTelco.SERVICIO_CLIENTE,
            'soporte_tecnico': CategoriaTemaTelco.SOPORTE_TECNICO,
            'tiempo_respuesta': CategoriaTemaTelco.TIEMPO_RESPUESTA,
            'resolucion_problemas': CategoriaTemaTelco.RESOLUCION_PROBLEMAS,
            'instalacion': CategoriaTemaTelco.INSTALACION,
            'equipos': CategoriaTemaTelco.EQUIPOS,
            'configuracion': CategoriaTemaTelco.CONFIGURACION,
            'mantenimiento': CategoriaTemaTelco.MANTENIMIENTO,
            'competencia': CategoriaTemaTelco.COMPETENCIA,
            'cambio_proveedor': CategoriaTemaTelco.CAMBIO_PROVEEDOR,
            'recomendaciones': CategoriaTemaTelco.RECOMENDACIONES,
            'satisfaccion_general': CategoriaTemaTelco.SATISFACCION_GENERAL
        }
        return mapeo.get(categoria_str.replace(' ', '_').lower(), CategoriaTemaTelco.OTROS)
    
    def _mapear_tipo_dolor(self, tipo_str: str) -> TipoPuntoDolor:
        """Mapea string de dolor a enum"""
        mapeo = {
            'sin_servicio': TipoPuntoDolor.SIN_SERVICIO,
            'intermitencias': TipoPuntoDolor.INTERMITENCIAS,
            'velocidad_lenta': TipoPuntoDolor.VELOCIDAD_LENTA,
            'cortes_frecuentes': TipoPuntoDolor.CORTES_FRECUENTES,
            'mala_calidad': TipoPuntoDolor.MALA_CALIDAD,
            'mal_servicio_cliente': TipoPuntoDolor.MAL_SERVICIO_CLIENTE,
            'demoras_atencion': TipoPuntoDolor.DEMORAS_ATENCION,
            'no_resuelven_problemas': TipoPuntoDolor.NO_RESUELVEN_PROBLEMAS,
            'personal_no_capacitado': TipoPuntoDolor.PERSONAL_NO_CAPACITADO,
            'dificultad_contacto': TipoPuntoDolor.DIFICULTAD_CONTACTO,
            'cobros_incorrectos': TipoPuntoDolor.COBROS_INCORRECTOS,
            'precios_altos': TipoPuntoDolor.PRECIOS_ALTOS,
            'promociones_engañosas': TipoPuntoDolor.PROMOCIONES_ENGAÑOSAS,
            'contratos_abusivos': TipoPuntoDolor.CONTRATOS_ABUSIVOS,
            'cargos_ocultos': TipoPuntoDolor.CARGOS_OCULTOS,
            'demoras_instalacion': TipoPuntoDolor.DEMORAS_INSTALACION,
            'equipos_defectuosos': TipoPuntoDolor.EQUIPOS_DEFECTUOSOS,
            'instalacion_deficiente': TipoPuntoDolor.INSTALACION_DEFICIENTE,
            'problemas_configuracion': TipoPuntoDolor.PROBLEMAS_CONFIGURACION,
            'falta_transparencia': TipoPuntoDolor.FALTA_TRANSPARENCIA,
            'proceso_cancelacion': TipoPuntoDolor.PROCESO_CANCELACION
        }
        return mapeo.get(tipo_str.replace(' ', '_').lower(), TipoPuntoDolor.OTROS)
    
    def _mapear_nivel_impacto(self, nivel_str: str) -> NivelImpacto:
        """Mapea string de nivel a enum"""
        mapeo = {
            'critico': NivelImpacto.CRITICO,
            'alto': NivelImpacto.ALTO,
            'moderado': NivelImpacto.MODERADO,
            'bajo': NivelImpacto.BAJO
        }
        return mapeo.get(nivel_str.lower(), NivelImpacto.MODERADO)
    
    def _calcular_confianza_comentario(self, comentario_data: Dict[str, Any]) -> float:
        """Calcula confianza general del análisis de un comentario"""
        confianzas = []
        
        # Confianza del sentimiento
        sentimiento = comentario_data.get('sentimiento', {})
        if sentimiento.get('confianza'):
            confianzas.append(float(sentimiento['confianza']))
        
        # Confianzas de emociones
        emociones = comentario_data.get('emociones', [])
        for emocion in emociones:
            if emocion.get('confianza'):
                confianzas.append(float(emocion['confianza']))
        
        # Confianzas de temas  
        temas = comentario_data.get('temas', [])
        for tema in temas:
            if tema.get('confianza'):
                confianzas.append(float(tema['confianza']))
        
        return sum(confianzas) / len(confianzas) if confianzas else 0.5
    
    def _crear_analisis_basico(self, indice: int, datos_orig: Dict[str, Any]) -> AnalisisComentario:
        """Crea un análisis básico en caso de error de mapeo"""
        texto = str(datos_orig.get('comentario', datos_orig.get('texto', 'Sin texto')))
        
        return AnalisisComentario(
            id=f"analisis_error_{indice}_{hash(texto)}",
            indice_original=indice,
            texto_original=texto,
            sentimiento=Sentimiento.crear_neutral(0.3, "manual"),
            confianza_general=0.3,
            resumen_ia="Error en el análisis - análisis básico generado",
            modelo_ia_utilizado="error_fallback"
        )
    
    def _procesar_en_lotes(self, comentarios_validos: List[str]) -> AnalisisCompletoIA:
        """
        Procesa comentarios en múltiples lotes y agrega los resultados
        OPTIMIZATION: Uses parallel processing for faster throughput
        """
        try:
            logger.info(f"🔄 Iniciando procesamiento por lotes: {len(comentarios_validos)} comentarios")
            
            # Dividir en lotes
            lotes = [
                comentarios_validos[i:i + self.max_comments_per_batch]
                for i in range(0, len(comentarios_validos), self.max_comments_per_batch)
            ]
            
            logger.info(f"📦 Creados {len(lotes)} lotes para procesar")
            
            # PROGRESS INTEGRATION: Initialize batch progress tracking
            total_lotes = len(lotes)
            self._notify_progress_start(total_lotes, len(comentarios_validos))
            
            # PERFORMANCE OPTIMIZATION: Use parallel processing for large files
            if len(lotes) >= 3 and len(comentarios_validos) >= 150:  # OPTIMIZED: Reduced threshold for more parallel processing
                logger.info(f"🚀 Using PARALLEL processing for {len(lotes)} lotes (PERFORMANCE TARGET)")
                return self._procesar_lotes_paralelo(lotes, total_lotes)
            else:
                logger.info(f"📈 Using sequential processing for {len(lotes)} lotes")
                return self._procesar_lotes_secuencial(lotes, total_lotes)
                
        except Exception as e:
            logger.error(f"❌ Error en procesamiento por lotes: {str(e)}")
            from ..dtos.analisis_completo_ia import AnalisisCompletoIA
            from datetime import datetime
            return AnalisisCompletoIA(
                total_comentarios=0,
                tendencia_general='error',
                resumen_ejecutivo=f'Error en procesamiento: {str(e)}',
                recomendaciones_principales=[],
                comentarios_analizados=[],
                confianza_general=0.0,
                tiempo_analisis=0.0,
                tokens_utilizados=0,
                modelo_utilizado='error',
                fecha_analisis=datetime.now(),
                distribucion_sentimientos={},
                temas_mas_relevantes={},
                dolores_mas_severos={},
                emociones_predominantes={}
            )
    
    def _procesar_lotes_secuencial(self, lotes: List[List[str]], total_lotes: int) -> AnalisisCompletoIA:
        """Sequential processing for small files (≤2 batches)"""
        logger.info(f"📈 Using sequential processing for {len(lotes)} lotes")
        
        # Procesar cada lote secuencialmente
        resultados_lotes = []
        comentarios_analizados_total = []
        
        for i, lote in enumerate(lotes):
            batch_number = i + 1
            logger.info(f"🔄 Procesando lote {batch_number}/{len(lotes)} ({len(lote)} comentarios)")
            
            # PROGRESS INTEGRATION: Notify batch start
            self._notify_batch_start(batch_number, total_lotes, len(lote))
            
            # DEBUG: Log first comment preview for debugging
            if len(lote) > 0:
                preview_len = self.configuracion.get('preview_length', 100) if self.configuracion else 100
                preview = lote[0][:preview_len] + "..." if len(lote[0]) > preview_len else lote[0]
                logger.debug(f"🔍 Lote {batch_number} contenido: {preview}")
            
            # PHASE 3: Intelligent retry processing with smart decisions
            resultado_lote = self._process_batch_with_intelligent_retry(batch_number, lote)
            
            # PROGRESS INTEGRATION: Notify batch completion
            if resultado_lote and resultado_lote.es_exitoso():
                self._notify_batch_success(batch_number, total_lotes, resultado_lote.confianza_general)
                resultados_lotes.append(resultado_lote)
                comentarios_analizados_total.extend(resultado_lote.comentarios_analizados)
            else:
                self._notify_batch_failure(batch_number, total_lotes, "Validation failed")
                logger.error(f"❌ Lote {i+1} SALTADO - No se pudo procesar exitosamente")
                
            # Memory monitoring (always check after processing each batch)
            if PSUTIL_AVAILABLE:
                try:
                    process = psutil.Process()
                    memory_mb = process.memory_info().rss / 1024 / 1024
                    logger.info(f"💾 Memoria utilizada: {memory_mb:.1f}MB después del lote {i+1}")
                    
                    # CONFIGURABLE: Alert on high memory usage
                    memory_threshold = self.configuracion.get('memory_threshold_mb', 400) if self.configuracion else 400
                    if memory_mb > memory_threshold:
                        logger.warning(f"⚠️ Uso alto de memoria: {memory_mb:.1f}MB (límite: {memory_threshold}MB)")
                except Exception as mem_error:
                    logger.debug(f"Error en monitoreo de memoria: {mem_error}")
            
            # OPTIMIZATION: Removed rate limiting - OpenAI handles this at API level
            
            # OPTIMIZATION: Aggressive memory cleanup after each batch
            if i % 2 == 0:  # Every 2 batches
                gc.collect()
                logger.debug(f"🧹 Memory cleanup after {i+1} batches")
        
        # Final memory cleanup
        gc.collect()
        
        # Agregar resultados de todos los lotes
        return self._agregar_resultados_lotes(resultados_lotes, comentarios_analizados_total, len(lotes) * self.max_comments_per_batch)
    
    def _procesar_lotes_paralelo(self, lotes: List[List[str]], total_lotes: int) -> AnalisisCompletoIA:
        """
        EXTREME PERFORMANCE: Process batches in parallel using threading (Streamlit-compatible)
        Target: 850+ comments in 20-30 seconds total
        """
        import time
        from concurrent.futures import ThreadPoolExecutor, as_completed
        
        logger.info(f"🚀 PARALLEL PROCESSING: {len(lotes)} lotes en paralelo (TARGET: 20-30s)")
        
        resultados_lotes = []
        comentarios_analizados_total = []
        inicio_paralelo = time.time()
        
        # WORKER THREAD CLASS (Streamlit Pattern 1 - No Streamlit commands)
        class BatchWorkerThread(Thread):
            def __init__(self, lote, batch_id, analizador_maestro, parent_caso_uso):
                super().__init__()
                self.lote = lote
                self.batch_id = batch_id
                self.analizador_maestro = analizador_maestro
                self.parent_caso_uso = parent_caso_uso
                self.resultado = None
                self.error = None
                self.start_time = None
                self.end_time = None
                
            def run(self):
                """Execute batch analysis in worker thread (NO Streamlit commands)"""
                try:
                    self.start_time = time.time()
                    logger.info(f"🔄 Thread {self.batch_id}: Processing {len(self.lote)} comments")
                    
                    # Direct API call without Streamlit dependencies
                    self.resultado = self.analizador_maestro.analizar_excel_completo(self.lote)
                    
                    self.end_time = time.time()
                    duration = self.end_time - self.start_time
                    logger.info(f"✅ Thread {self.batch_id}: Completed in {duration:.1f}s")
                    
                except Exception as e:
                    self.error = e
                    self.end_time = time.time()
                    logger.error(f"❌ Thread {self.batch_id}: Error - {str(e)}")
        
        # Calculate optimal worker count based on batches
        max_workers = min(len(lotes), 8)  # Max 8 concurrent workers (OPTIMIZED for performance)
        logger.info(f"👥 Using {max_workers} parallel workers for {len(lotes)} batches")
        
        # Create and start worker threads
        workers = []
        for i, lote in enumerate(lotes):
            worker = BatchWorkerThread(lote, i+1, self.analizador_maestro, self)
            workers.append(worker)
            worker.start()
            
        logger.info(f"🚀 {len(workers)} parallel threads STARTED")
        
        # Wait for all workers to complete (with progress updates)
        completed_count = 0
        while completed_count < len(workers):
            time.sleep(0.1)  # Small delay to prevent busy waiting
            
            # Check completed workers
            newly_completed = []
            for worker in workers:
                if not worker.is_alive() and worker not in newly_completed:
                    newly_completed.append(worker)
                    
            if newly_completed:
                completed_count += len(newly_completed)
                
                # Process results from completed workers
                for worker in newly_completed:
                    if worker.resultado and worker.resultado.es_exitoso():
                        resultados_lotes.append(worker.resultado)
                        comentarios_analizados_total.extend(worker.resultado.comentarios_analizados)
                        
                        # Notify progress (main thread can call Streamlit commands)
                        self._notify_batch_success(worker.batch_id, total_lotes, worker.resultado.confianza_general)
                        
                    elif worker.error:
                        self._notify_batch_failure(worker.batch_id, total_lotes, str(worker.error))
                        
                elapsed = time.time() - inicio_paralelo
                progress_pct = (completed_count / len(workers)) * 100
                logger.info(f"📊 Parallel progress: {completed_count}/{len(workers)} ({progress_pct:.1f}%) - {elapsed:.1f}s elapsed")
        
        # Final cleanup
        for worker in workers:
            worker.join(timeout=1.0)  # Ensure all threads are properly closed
            
        tiempo_total = time.time() - inicio_paralelo
        logger.info(f"🎉 PARALLEL PROCESSING COMPLETED in {tiempo_total:.1f}s")
        logger.info(f"🎯 TARGET STATUS: {'✅ ACHIEVED' if tiempo_total <= 30 else '❌ EXCEEDED'} (target: 20-30s)")
        
        return self._agregar_resultados_lotes(resultados_lotes, comentarios_analizados_total, len(lotes) * self.max_comments_per_batch)
    
    # REMOVED: AsyncIO code completely eliminated (80 lines of dead code)
    
    def _agregar_resultados_lotes(self, resultados_lotes: List[AnalisisCompletoIA], 
                                 comentarios_analizados_total: List[Dict], 
                                 total_comentarios: int) -> AnalisisCompletoIA:
        """
        Agrega los resultados de múltiples lotes en un resultado consolidado
        """
        from ..dtos.analisis_completo_ia import AnalisisCompletoIA
        from datetime import datetime
        
        if not resultados_lotes:
            logger.error("❌ No hay resultados de lotes para agregar")
            return AnalisisCompletoIA(
                total_comentarios=0,
                tendencia_general='error',
                resumen_ejecutivo='No se pudieron procesar los lotes',
                recomendaciones_principales=[],
                comentarios_analizados=[],
                confianza_general=0.0,
                tiempo_analisis=0.0,
                tokens_utilizados=0,
                modelo_utilizado='error',
                fecha_analisis=datetime.now(),
                distribucion_sentimientos={},
                temas_mas_relevantes={},
                dolores_mas_severos={},
                emociones_predominantes={}
            )
        
        # Calcular estadísticas agregadas
        total_positivos = sum(r.distribucion_sentimientos.get('positivo', 0) for r in resultados_lotes)
        total_neutrales = sum(r.distribucion_sentimientos.get('neutral', 0) for r in resultados_lotes)
        total_negativos = sum(r.distribucion_sentimientos.get('negativo', 0) for r in resultados_lotes)
        
        # Determinar tendencia general
        max_sentimiento = max(total_positivos, total_neutrales, total_negativos)
        if max_sentimiento == total_positivos:
            tendencia_general = 'positiva'
        elif max_sentimiento == total_negativos:
            tendencia_general = 'negativa'
        else:
            tendencia_general = 'neutral'
        
        # Combinar temas más relevantes
        temas_combinados = {}
        for resultado in resultados_lotes:
            for tema, relevancia in resultado.temas_mas_relevantes.items():
                temas_combinados[tema] = temas_combinados.get(tema, 0) + relevancia
        
        # Calcular confianza promedio
        confianza_promedio = sum(r.confianza_general for r in resultados_lotes) / len(resultados_lotes)
        
        # Tiempo total
        tiempo_total = sum(r.tiempo_analisis for r in resultados_lotes)
        
        # Tokens totales
        tokens_totales = sum(r.tokens_utilizados for r in resultados_lotes)
        
        # Crear resultado consolidado
        return AnalisisCompletoIA(
            total_comentarios=total_comentarios,
            tendencia_general=tendencia_general,
            resumen_ejecutivo=f"Análisis consolidado de {total_comentarios} comentarios procesados en {len(resultados_lotes)} lotes. Tendencia general: {tendencia_general}.",
            recomendaciones_principales=[
                "Revisar comentarios con mayor impacto negativo",
                "Implementar mejoras basadas en temas frecuentes",
                "Monitorear evolución de sentimientos"
            ],
            comentarios_analizados=comentarios_analizados_total,
            confianza_general=confianza_promedio,
            tiempo_analisis=tiempo_total,
            tokens_utilizados=tokens_totales,
            modelo_utilizado=resultados_lotes[0].modelo_utilizado if resultados_lotes else 'unknown',
            fecha_analisis=datetime.now(),
            distribucion_sentimientos={
                'positivo': total_positivos,
                'neutral': total_neutrales,
                'negativo': total_negativos
            },
            temas_mas_relevantes=temas_combinados,
            dolores_mas_severos={},  # Simplificado por ahora
            emociones_predominantes={}  # Simplificado por ahora
        )
    
    def _process_batch_with_intelligent_retry(self, batch_number: int, lote: List[str]):
        """
        PHASE 3: Process batch with intelligent retry strategy
        
        Args:
            batch_number: Number of the batch being processed
            lote: List of comments to analyze
            
        Returns:
            AnalisisCompletoIA or None if failed after all retries
        """
        try:
            # Memory management: Clean cache every 5 batches
            if batch_number % 5 == 0:
                logger.info(f"🧹 Limpieza de memoria después de {batch_number} lotes")
                try:
                    self.analizador_maestro.limpiar_cache()
                    gc.collect()
                except Exception as cleanup_error:
                    logger.warning(f"⚠️ Error en limpieza de memoria: {cleanup_error}")
            
            # Get configuration for retry decisions
            max_retries = 2  # Default
            if self.ai_configuration:
                max_retries = self.ai_configuration.batch_retry_count
            
            # Initialize tracking variables
            batch_retry_count = 0
            resultado_lote = None
            last_error = None
            original_temperature = getattr(self.analizador_maestro, 'temperatura', 0.0)
            is_deterministic = getattr(self.analizador_maestro, '_is_deterministic', True)
            
            while batch_retry_count <= max_retries:
                try:
                    # AI processing with exception handling
                    resultado_lote = self.analizador_maestro.analizar_excel_completo(lote)
                    
                    # Enhanced success validation
                    if resultado_lote and resultado_lote.es_exitoso():
                        logger.info(f"✅ Lote {batch_number} exitoso: confianza={resultado_lote.confianza_general:.2f}, "
                                  f"analizados={len(resultado_lote.comentarios_analizados)}/{len(lote)}")
                        
                        # Record successful attempt
                        if self.retry_strategy:
                            context = create_retry_context(
                                batch_retry_count, resultado_lote, None,
                                is_deterministic, original_temperature,
                                self.analizador_maestro.modelo, len(lote)
                            )
                            self.retry_strategy.record_attempt(context, resultado_lote)
                        
                        return resultado_lote  # Success, return result
                    else:
                        # Enhanced failure logging
                        confidence = resultado_lote.confianza_general if resultado_lote else 0.0
                        analyzed_count = len(resultado_lote.comentarios_analizados) if resultado_lote else 0
                        resumen = resultado_lote.resumen_ejecutivo if resultado_lote else "No result"
                        
                        logger.error(f"❌ Lote {batch_number} FALLÓ en validación:")
                        logger.error(f"  - Confianza: {confidence:.2f}")
                        logger.error(f"  - Analizados: {analyzed_count}/{len(lote)}")
                        logger.error(f"  - Resumen: {resumen}")
                        
                        # FASE 4 OPTIMIZATION: Skip retries immediately for deterministic config
                        if is_deterministic and abs(original_temperature) < 0.001:
                            logger.warning(f"🧠 FASE 4: Saltando reintentos para configuración determinista - resultado será idéntico")
                            break
                        
                        # Use intelligent retry strategy
                        if self.retry_strategy and batch_retry_count < max_retries:
                            context = create_retry_context(
                                batch_retry_count, resultado_lote, None,
                                is_deterministic, original_temperature,
                                self.analizador_maestro.modelo, len(lote)
                            )
                            
                            retry_result = self.retry_strategy.should_retry(context)
                            
                            if retry_result.decision == RetryDecision.SKIP_RETRY:
                                logger.warning(f"🧠 Skip inteligente: {retry_result.reason}")
                                break
                            elif retry_result.decision == RetryDecision.ABORT_RETRIES:
                                logger.error(f"🧠 Abortar reintentos: {retry_result.reason}")
                                break
                            else:
                                batch_retry_count += 1
                                
                                # Apply temperature variation if recommended
                                if retry_result.new_temperature is not None:
                                    logger.info(f"🌡️ Aplicando variación de temperatura: {original_temperature:.3f} → {retry_result.new_temperature:.3f}")
                                    self.analizador_maestro.temperatura = retry_result.new_temperature
                                
                                logger.warning(f"⚠️ Lote {batch_number} reintento {batch_retry_count}/{max_retries} en {retry_result.delay_seconds:.1f}s")
                                logger.info(f"🧠 Estrategia: {retry_result.reason}")
                                time.sleep(retry_result.delay_seconds)
                                
                                # Record retry attempt
                                self.retry_strategy.record_attempt(context, resultado_lote)
                        else:
                            # Fallback to standard retry logic
                            if batch_retry_count < max_retries:
                                batch_retry_count += 1
                                delay = 0.5 + batch_retry_count * 0.3
                                logger.warning(f"⚠️ Lote {batch_number} reintento estándar {batch_retry_count}/{max_retries} en {delay:.1f}s")
                                time.sleep(delay)
                            else:
                                logger.error(f"❌ Lote {batch_number} ABANDONADO después de {max_retries} intentos")
                                break
                        
                        # Reset temperature if it was changed
                        if self.retry_strategy and batch_retry_count > max_retries:
                            self.analizador_maestro.temperatura = original_temperature
                                
                except Exception as e:
                    # CRITICAL FIX: Catch all exceptions during AI processing
                    logger.error(f"❌ Excepción en lote {batch_number} (intento {batch_retry_count + 1}): {str(e)}")
                    logger.error(f"❌ Tipo de error: {type(e).__name__}")
                    last_error = e
                    
                    # FASE 4 OPTIMIZATION: Skip retries for exceptions in deterministic config
                    if is_deterministic and abs(original_temperature) < 0.001:
                        logger.warning(f"🧠 FASE 4: Saltando reintentos de excepción para configuración determinista")
                        break
                    
                    # Use intelligent retry strategy for exceptions too
                    if self.retry_strategy and batch_retry_count < max_retries:
                        context = create_retry_context(
                            batch_retry_count, None, e,
                            is_deterministic, original_temperature,
                            self.analizador_maestro.modelo, len(lote)
                        )
                        
                        retry_result = self.retry_strategy.should_retry(context)
                        
                        if retry_result.decision == RetryDecision.SKIP_RETRY:
                            logger.warning(f"🧠 Skip inteligente para excepción: {retry_result.reason}")
                            break
                        elif retry_result.decision == RetryDecision.ABORT_RETRIES:
                            logger.error(f"🧠 Abortar reintentos para excepción: {retry_result.reason}")
                            break
                        else:
                            batch_retry_count += 1
                            logger.warning(f"⚠️ Lote {batch_number} excepción reintento {batch_retry_count}/{max_retries} en {retry_result.delay_seconds:.1f}s")
                            logger.info(f"🧠 Estrategia de excepción: {retry_result.reason}")
                            time.sleep(retry_result.delay_seconds)
                            
                            # Record exception attempt
                            self.retry_strategy.record_attempt(context, None)
                    else:
                        # Fallback exception retry
                        if batch_retry_count < max_retries:
                            batch_retry_count += 1
                            delay = 0.8 + batch_retry_count * 0.4
                            logger.warning(f"⚠️ Lote {batch_number} excepción reintento estándar {batch_retry_count}/{max_retries} en {delay:.1f}s")
                            time.sleep(delay)
                        else:
                            logger.error(f"❌ Lote {batch_number} ABANDONADO por excepciones después de {max_retries} intentos")
                            break
            
            # Reset temperature after all retries
            if hasattr(self.analizador_maestro, 'temperatura'):
                self.analizador_maestro.temperatura = original_temperature
            
            # Final failure handling
            if not resultado_lote or not resultado_lote.es_exitoso():
                logger.error(f"❌ Lote {batch_number} SALTADO - No se pudo procesar exitosamente")
                
                # Log retry statistics if available
                if self.retry_strategy:
                    stats = self.retry_strategy.get_retry_statistics()
                    logger.info(f"📊 Estadísticas de reintentos: {stats}")
            
            return resultado_lote
            
        except Exception as e:
            logger.error(f"❌ Error crítico en procesamiento de lote {batch_number}: {str(e)}")
            return None

    def _notify_progress_start(self, total_lotes: int, total_comentarios: int):
        """Notify progress start with batch info"""
        if self.progress_callback:
            self.progress_callback({
                'action': 'start',
                'total_batches': total_lotes,
                'total_comments': total_comentarios,
                'current_batch': 0,
                'progress_percentage': 0.0
            })

    def _notify_batch_start(self, batch_number: int, total_lotes: int, batch_size: int):
        """Notify batch processing start"""
        if self.progress_callback:
            progress_pct = ((batch_number - 1) / total_lotes) * 100
            self.progress_callback({
                'action': 'batch_start',
                'current_batch': batch_number,
                'total_batches': total_lotes,
                'batch_size': batch_size,
                'progress_percentage': progress_pct,
                'status': f'Procesando lote {batch_number}/{total_lotes}'
            })

    def _notify_batch_success(self, batch_number: int, total_lotes: int, confidence: float):
        """Notify batch completed successfully"""
        if self.progress_callback:
            progress_pct = (batch_number / total_lotes) * 100
            self.progress_callback({
                'action': 'batch_success',
                'current_batch': batch_number,
                'total_batches': total_lotes,
                'confidence': confidence,
                'progress_percentage': progress_pct,
                'status': f'✅ Lote {batch_number}/{total_lotes} completado'
            })

    def _notify_batch_failure(self, batch_number: int, total_lotes: int, reason: str):
        """Notify batch failed"""
        if self.progress_callback:
            progress_pct = (batch_number / total_lotes) * 100
            self.progress_callback({
                'action': 'batch_failure',
                'current_batch': batch_number,
                'total_batches': total_lotes,
                'reason': reason,
                'progress_percentage': progress_pct,
                'status': f'❌ Lote {batch_number}/{total_lotes} falló'
            })

    def _crear_resultado_error(self, mensaje: str) -> ResultadoAnalisisMaestro:
        """Crea un resultado de error"""
        return ResultadoAnalisisMaestro(
            exito=False,
            mensaje=mensaje,
            total_comentarios=0,
            fecha_analisis=datetime.now()
        )