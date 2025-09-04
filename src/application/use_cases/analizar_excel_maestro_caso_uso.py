"""
Caso de uso simplificado para análisis maestro con IA
"""
from typing import List, Dict, Any
from dataclasses import dataclass
from datetime import datetime
import logging

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


logger = logging.getLogger(__name__)


@dataclass
class ComandoAnalisisExcelMaestro:
    """Comando simplificado para el análisis maestro"""
    archivo_cargado: Any
    nombre_archivo: str
    limpiar_repositorio: bool = True


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
        analizador_maestro: AnalizadorMaestroIA
    ):
        self.repositorio_comentarios = repositorio_comentarios
        self.lector_archivos = lector_archivos
        self.analizador_maestro = analizador_maestro
        
    def ejecutar(self, comando: ComandoAnalisisExcelMaestro) -> ResultadoAnalisisMaestro:
        """
        Ejecuta el análisis maestro simplificado
        """
        inicio_tiempo = datetime.now()
        logger.info(f"🚀 Iniciando análisis maestro de archivo: {comando.nombre_archivo}")
        
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
            
            logger.info(f"📊 Procesando {len(comentarios_validos)} comentarios válidos")
            
            # 3. UNA sola llamada al AnalizadorMaestroIA
            analisis_completo_ia = self.analizador_maestro.analizar_excel_completo(comentarios_validos)
            
            if not analisis_completo_ia.es_exitoso():
                return self._crear_resultado_error("El análisis maestro de IA falló")
            
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
                        elif severidad >= 0.5:
                            dolor = PuntoDolor.crear_alto_impacto(
                                tipo=tipo_dolor,
                                severidad=severidad,
                                confianza=confianza,
                                contexto=contexto,
                                palabras_clave=[],
                                frecuencia=1
                            )
                        elif severidad >= 0.3:
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
            sentimiento=Sentimiento.crear_neutral(0.3, "error"),
            confianza_general=0.3,
            resumen_ia="Error en el análisis - análisis básico generado",
            modelo_ia_utilizado="error_fallback"
        )
    
    def _crear_resultado_error(self, mensaje: str) -> ResultadoAnalisisMaestro:
        """Crea un resultado de error"""
        return ResultadoAnalisisMaestro(
            exito=False,
            mensaje=mensaje,
            total_comentarios=0,
            fecha_analisis=datetime.now()
        )