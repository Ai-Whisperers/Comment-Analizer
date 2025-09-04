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
    
    def guardar_lote(self, comentarios: List[Comentario]) -> None:
        """
        Guarda múltiples comentarios
        """
        comentarios_validos = 0
        comentarios_invalidos = 0
        
        for comentario in comentarios:
            try:
                self.guardar(comentario)
                comentarios_validos += 1
            except ValueError:
                comentarios_invalidos += 1
                logger.warning(f"⚠️ Comentario inválido omitido: {comentario.id}")
        
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
                comentario.sentimiento.tipo.value == tipo_sentimiento):
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