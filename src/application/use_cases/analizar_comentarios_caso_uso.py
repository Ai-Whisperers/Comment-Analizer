"""
Caso de uso principal para análisis de comentarios
"""
from typing import List, Dict, Any
from dataclasses import dataclass
from datetime import datetime

from ...domain.entities.comentario import Comentario
from ...domain.repositories.repositorio_comentarios import IRepositorioComentarios
from ...domain.services.analizador_sentimientos import ServicioAnalisisSentimientos
from ...domain.value_objects.calidad_comentario import CalidadComentario
from ...domain.value_objects.nivel_urgencia import NivelUrgencia
from ..interfaces.lector_archivos import ILectorArchivos
from ..interfaces.procesador_texto import IProcesadorTexto
from ..interfaces.detector_temas import IDetectorTemas
from ..dtos.resultado_analisis import ResultadoAnalisis


@dataclass
class ComandoAnalisisComentarios:
    """Comando que encapsula los parámetros para el análisis"""
    archivo_cargado: Any
    nombre_archivo: str
    incluir_analisis_avanzado: bool = True
    limpiar_repositorio: bool = True


class AnalizarComentariosCasoUso:
    """
    Caso de uso principal que orquesta el análisis completo de comentarios
    """
    
    def __init__(
        self,
        repositorio_comentarios: IRepositorioComentarios,
        lector_archivos: ILectorArchivos,
        procesador_texto: IProcesadorTexto,
        detector_temas: IDetectorTemas,
        servicio_sentimientos: ServicioAnalisisSentimientos
    ):
        self.repositorio_comentarios = repositorio_comentarios
        self.lector_archivos = lector_archivos
        self.procesador_texto = procesador_texto
        self.detector_temas = detector_temas
        self.servicio_sentimientos = servicio_sentimientos
    
    def ejecutar(self, comando: ComandoAnalisisComentarios) -> ResultadoAnalisis:
        """
        Ejecuta el análisis completo de comentarios
        """
        try:
            # 1. Limpiar repositorio si se requiere
            if comando.limpiar_repositorio:
                self.repositorio_comentarios.limpiar()
            
            # 2. Leer y procesar archivo
            comentarios_raw = self.lector_archivos.leer_comentarios(comando.archivo_cargado)
            
            if not comentarios_raw:
                return self._crear_resultado_error("No se encontraron comentarios válidos en el archivo")
            
            # 3. Procesar y limpiar textos
            comentarios = self._crear_entidades_comentarios(comentarios_raw)
            
            # 4. Análisis de sentimientos
            comentarios = self.servicio_sentimientos.analizar_lote_comentarios(comentarios)
            
            # 5. Análisis avanzado si se requiere
            if comando.incluir_analisis_avanzado:
                comentarios = self._realizar_analisis_avanzado(comentarios)
            
            # 6. Guardar en repositorio
            self.repositorio_comentarios.guardar_lote(comentarios)
            
            # 7. Generar resultado
            return self._generar_resultado_analisis(comentarios, comando.nombre_archivo)
            
        except Exception as e:
            return self._crear_resultado_error(f"Error durante el análisis: {str(e)}")
    
    def _crear_entidades_comentarios(self, comentarios_raw: List[Dict[str, Any]]) -> List[Comentario]:
        """
        Crea entidades de comentarios a partir de datos raw
        """
        comentarios = []
        
        for i, raw in enumerate(comentarios_raw):
            # Extraer texto y datos básicos
            texto = str(raw.get('comentario', raw.get('texto', ''))).strip()
            
            if not texto:
                continue
            
            # Limpiar texto
            texto_limpio = self.procesador_texto.limpiar_texto(texto)
            
            # Crear comentario
            comentario = Comentario(
                id=f"comentario_{i}_{hash(texto)}",
                texto=texto,
                texto_limpio=texto_limpio,
                frecuencia=raw.get('frecuencia', 1),
                calificacion_nps=raw.get('nps'),
                calificacion_nota=raw.get('nota'),
                fecha_analisis=datetime.now()
            )
            
            comentarios.append(comentario)
        
        # Remover duplicados y consolidar frecuencias
        comentarios = self.procesador_texto.consolidar_duplicados(comentarios)
        
        return comentarios
    
    def _realizar_analisis_avanzado(self, comentarios: List[Comentario]) -> List[Comentario]:
        """
        Realiza análisis avanzado: temas, calidad, urgencia
        """
        for comentario in comentarios:
            # Detectar temas
            temas = self.detector_temas.detectar_temas(comentario.texto_limpio)
            comentario.temas = temas.temas_principales
            comentario.puntos_dolor = temas.puntos_dolor
            comentario.emociones = temas.emociones_detectadas
            comentario.competidores = temas.competidores_mencionados
            
            # Evaluar calidad
            comentario.calidad = CalidadComentario.evaluar_desde_texto(
                comentario.texto, 
                len(comentario.temas)
            )
            
            # Evaluar urgencia
            comentario.urgencia = NivelUrgencia.evaluar_urgencia(
                comentario.puntos_dolor,
                comentario.sentimiento.es_negativo() if comentario.sentimiento else False,
                comentario.sentimiento.confianza if comentario.sentimiento else 0.5
            )
        
        return comentarios
    
    def _generar_resultado_analisis(self, comentarios: List[Comentario], nombre_archivo: str) -> ResultadoAnalisis:
        """
        Genera el resultado final del análisis
        """
        # Estadísticas básicas
        total_comentarios = len(comentarios)
        estadisticas_sentimientos = self.servicio_sentimientos.obtener_estadisticas_sentimientos(comentarios)
        
        # Análisis de urgencia
        comentarios_criticos = [c for c in comentarios if c.es_critico()]
        
        # Análisis de temas
        todos_los_temas = []
        for c in comentarios:
            todos_los_temas.extend(c.temas)
        
        from collections import Counter
        temas_frecuentes = Counter(todos_los_temas).most_common(10)
        
        # Análisis de calidad
        comentarios_alta_calidad = [c for c in comentarios if c.calidad and c.calidad.es_alta_calidad()]
        
        return ResultadoAnalisis(
            exito=True,
            mensaje="Análisis completado exitosamente",
            total_comentarios=total_comentarios,
            estadisticas_sentimientos=estadisticas_sentimientos,
            comentarios_criticos=len(comentarios_criticos),
            temas_principales=dict(temas_frecuentes),
            comentarios_alta_calidad=len(comentarios_alta_calidad),
            nombre_archivo=nombre_archivo,
            fecha_analisis=datetime.now(),
            metodos_utilizados=self._obtener_metodos_utilizados(),
            comentarios=comentarios  # Para procesamiento posterior
        )
    
    def _crear_resultado_error(self, mensaje: str) -> ResultadoAnalisis:
        """
        Crea un resultado de error
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
    
    def _obtener_metodos_utilizados(self) -> Dict[str, str]:
        """
        Obtiene información sobre los métodos utilizados en el análisis
        """
        return {
            'lector_archivos': type(self.lector_archivos).__name__,
            'procesador_texto': type(self.procesador_texto).__name__,
            'detector_temas': type(self.detector_temas).__name__,
            'analizadores_sentimiento': [type(a).__name__ for a in self.servicio_sentimientos.analizadores]
        }