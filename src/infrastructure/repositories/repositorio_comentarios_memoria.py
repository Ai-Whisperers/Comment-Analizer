"""
Implementación en memoria del repositorio de comentarios
"""
from typing import List, Optional, Dict
import logging

from ...domain.entities.comentario import Comentario
from ...domain.repositories.repositorio_comentarios import IRepositorioComentarios


logger = logging.getLogger(__name__)


class RepositorioComentariosMemoria(IRepositorioComentarios):
    """
    Implementación en memoria del repositorio de comentarios
    Ideal para sesiones de análisis temporal
    """
    
    def __init__(self):
        self._comentarios: Dict[str, Comentario] = {}
        logger.info("📝 Repositorio de comentarios en memoria inicializado")
    
    def guardar(self, comentario: Comentario) -> None:
        """
        Guarda un comentario en memoria
        """
        if not comentario.es_valido():
            raise ValueError(f"Comentario inválido: {comentario.id}")
        
        self._comentarios[comentario.id] = comentario
        logger.debug(f"💾 Comentario guardado: {comentario.id}")
    
    def guardar_lote(self, comentarios) -> None:
        """
        Guarda múltiples comentarios (soporta Comentario y AnalisisComentario)
        """
        comentarios_validos = 0
        comentarios_invalidos = 0
        
        for comentario in comentarios:
            try:
                # Handle both Comentario and AnalisisComentario types
                if hasattr(comentario, 'texto_original'):
                    # AnalisisComentario from IA system
                    comentario_simple = self._convertir_analisis_a_comentario(comentario)
                    self.guardar(comentario_simple)
                else:
                    # Comentario legacy
                    self.guardar(comentario)
                    
                comentarios_validos += 1
            except Exception as e:
                comentarios_invalidos += 1
                logger.warning(f"⚠️ Comentario inválido omitido: {getattr(comentario, 'id', 'unknown')}: {str(e)}")
        
        logger.info(f"📦 Lote guardado: {comentarios_validos} válidos, {comentarios_invalidos} omitidos")
    
    def obtener_por_id(self, id_comentario: str) -> Optional[Comentario]:
        """
        Obtiene un comentario por su ID
        """
        return self._comentarios.get(id_comentario)
    
    def obtener_todos(self) -> List[Comentario]:
        """
        Obtiene todos los comentarios
        """
        return list(self._comentarios.values())
    
    def buscar_por_sentimiento(self, tipo_sentimiento: str) -> List[Comentario]:
        """
        Busca comentarios por tipo de sentimiento
        """
        comentarios_encontrados = []
        
        for comentario in self._comentarios.values():
            if (comentario.sentimiento and 
                comentario.sentimiento.categoria.value == tipo_sentimiento):
                comentarios_encontrados.append(comentario)
        
        return comentarios_encontrados
    
    def buscar_criticos(self) -> List[Comentario]:
        """
        Busca comentarios que requieren atención crítica
        """
        comentarios_criticos = []
        
        for comentario in self._comentarios.values():
            if comentario.es_critico():
                comentarios_criticos.append(comentario)
        
        # Ordenar por urgencia (P0 primero)
        comentarios_criticos.sort(
            key=lambda c: (
                c.urgencia.prioridad.value if c.urgencia else "P3",
                -c.urgencia.puntuacion if c.urgencia else 0
            )
        )
        
        return comentarios_criticos
    
    def limpiar(self) -> None:
        """
        Limpia todos los comentarios del repositorio
        """
        cantidad_anterior = len(self._comentarios)
        self._comentarios.clear()
        logger.info(f"🧹 Repositorio limpiado: {cantidad_anterior} comentarios removidos")
    
    def obtener_estadisticas(self) -> Dict[str, int]:
        """
        Obtiene estadísticas del repositorio
        """
        total = len(self._comentarios)
        
        if total == 0:
            return {
                'total': 0,
                'con_sentimiento': 0,
                'criticos': 0,
                'alta_calidad': 0
            }
        
        con_sentimiento = sum(1 for c in self._comentarios.values() if c.sentimiento)
        criticos = len(self.buscar_criticos())
        alta_calidad = sum(1 for c in self._comentarios.values() 
                          if c.calidad and c.calidad.es_alta_calidad())
        
        return {
            'total': total,
            'con_sentimiento': con_sentimiento,
            'criticos': criticos,
            'alta_calidad': alta_calidad
        }
    
    def _convertir_analisis_a_comentario(self, analisis_comentario) -> Comentario:
        """
        Convierte AnalisisComentario a Comentario para compatibility con Repository
        """
        from ...domain.entities.comentario import Comentario
        from ...domain.value_objects.calidad_comentario import CalidadComentario
        from ...domain.value_objects.nivel_urgencia import NivelUrgencia
        
        # Extract basic data
        id_comentario = analisis_comentario.id
        texto = analisis_comentario.texto_original
        texto_limpio = texto.lower().strip()  # Basic cleaning
        
        # Convert IA analysis to legacy format
        comentario = Comentario(
            id=id_comentario,
            texto=texto,
            texto_limpio=texto_limpio,
            frecuencia=1,
            fecha_analisis=analisis_comentario.fecha_analisis
        )
        
        # Map sentimiento (same structure)
        comentario.sentimiento = analisis_comentario.sentimiento
        
        # Map calidad from IA analysis richness
        num_temas = len(analisis_comentario.temas)
        comentario.calidad = CalidadComentario.evaluar_desde_texto(texto, num_temas)
        
        # Map urgencia from puntos_dolor severity
        puntos_dolor_texto = [p.descripcion for p in analisis_comentario.puntos_dolor if hasattr(p, 'descripcion')]
        es_negativo = analisis_comentario.sentimiento.es_negativo() if analisis_comentario.sentimiento else False
        confianza_sentimiento = analisis_comentario.sentimiento.confianza if analisis_comentario.sentimiento else 0.5
        
        comentario.urgencia = NivelUrgencia.evaluar_urgencia(
            puntos_dolor_texto, 
            es_negativo, 
            confianza_sentimiento
        )
        
        # Add temas as simple list
        comentario.temas = [t.categoria.value for t in analisis_comentario.temas]
        comentario.puntos_dolor = puntos_dolor_texto
        comentario.emociones = [e.tipo.value for e in analisis_comentario.emociones]
        
        # Add original ratings if available
        comentario.calificacion_nps = getattr(analisis_comentario, 'calificacion_nps', None)
        comentario.calificacion_nota = getattr(analisis_comentario, 'calificacion_nota', None)
        
        return comentario