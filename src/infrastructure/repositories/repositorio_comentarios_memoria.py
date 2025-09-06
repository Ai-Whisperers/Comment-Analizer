"""
Implementación en memoria del repositorio de comentarios
"""
from typing import List, Optional, Dict, Any
from collections import OrderedDict
import sys
import logging

from ...domain.entities.comentario import Comentario
from ...domain.repositories.repositorio_comentarios import IRepositorioComentarios


logger = logging.getLogger(__name__)


class RepositorioComentariosMemoria(IRepositorioComentarios):
    """
    Implementación en memoria del repositorio de comentarios
    CRITICAL FIX: Added memory limits and LRU eviction to prevent memory exhaustion
    """
    
    def __init__(self, max_comentarios: int = 10000, max_memory_mb: int = 100):
        """
        CRITICAL-003 FIX: Initialize repository with memory and count limits
        
        Args:
            max_comentarios: Maximum number of comments to store (default: 10,000)
            max_memory_mb: Maximum memory usage in MB (default: 100MB)
        """
        # Use OrderedDict for LRU eviction capability
        self._comentarios: OrderedDict[str, Comentario] = OrderedDict()
        
        # Memory management settings
        self._max_comentarios = max_comentarios
        self._max_memory_bytes = max_memory_mb * 1024 * 1024
        self._current_memory_estimate = 0
        
        logger.info(f"📝 Memory-limited repository initialized - Max: {max_comentarios} comments, {max_memory_mb}MB")
    
    def _estimate_memory_usage(self, comentario: Comentario) -> int:
        """
        CRITICAL-003 FIX: Estimate memory usage of a comment
        
        Returns:
            int: Estimated memory usage in bytes
        """
        try:
            # Estimate based on text content + object overhead
            text_size = len(comentario.texto.encode('utf-8'))
            
            # Add estimated overhead for Python object, attributes, etc.
            object_overhead = 200  # Conservative estimate for Python object overhead
            
            # Add any additional attribute sizes if they exist
            extra_size = 0
            if hasattr(comentario, 'id') and comentario.id:
                extra_size += len(str(comentario.id).encode('utf-8'))
            
            return text_size + object_overhead + extra_size
        except Exception:
            # Conservative fallback if estimation fails
            return 1000
    
    def _enforce_limits(self) -> None:
        """
        CRITICAL-003 FIX: Enforce memory and count limits using LRU eviction
        """
        removed_count = 0
        
        # Enforce count limit (remove oldest entries)
        while len(self._comentarios) > self._max_comentarios:
            oldest_key, oldest_comment = self._comentarios.popitem(last=False)
            self._current_memory_estimate -= self._estimate_memory_usage(oldest_comment)
            removed_count += 1
        
        # Enforce memory limit (remove oldest entries)
        while (self._current_memory_estimate > self._max_memory_bytes and 
               len(self._comentarios) > 0):
            oldest_key, oldest_comment = self._comentarios.popitem(last=False)
            self._current_memory_estimate -= self._estimate_memory_usage(oldest_comment)
            removed_count += 1
        
        if removed_count > 0:
            logger.warning(f"🗑️ LRU evicted {removed_count} old comments to enforce memory limits")
    
    def guardar(self, comentario: Comentario) -> None:
        """
        Guarda un comentario en memoria
        CRITICAL-003 FIX: Now enforces memory limits and uses LRU eviction
        """
        if not comentario.es_valido():
            raise ValueError(f"Comentario inválido: {comentario.id}")
        
        # Remove existing comment if updating (for LRU order and memory tracking)
        if comentario.id in self._comentarios:
            old_comment = self._comentarios[comentario.id]
            self._current_memory_estimate -= self._estimate_memory_usage(old_comment)
            del self._comentarios[comentario.id]
        
        # Calculate memory usage for new comment
        memory_usage = self._estimate_memory_usage(comentario)
        self._current_memory_estimate += memory_usage
        
        # Store comment (OrderedDict maintains insertion order for LRU)
        self._comentarios[comentario.id] = comentario
        
        # Enforce limits after insertion
        self._enforce_limits()
        
        logger.debug(f"💾 Comment saved: {comentario.id} ({memory_usage} bytes, total: {self._current_memory_estimate} bytes)")
    
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
        CRITICAL-003 FIX: Now also resets memory tracking
        """
        cantidad_anterior = len(self._comentarios)
        self._comentarios.clear()
        self._current_memory_estimate = 0  # Reset memory tracking
        logger.info(f"🧹 Repositorio limpiado: {cantidad_anterior} comentarios removidos, memoria liberada")
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """
        CRITICAL-003 FIX: Get memory usage statistics for monitoring
        
        Returns:
            Dict with memory statistics
        """
        return {
            "total_comments": len(self._comentarios),
            "estimated_memory_mb": round(self._current_memory_estimate / (1024 * 1024), 2),
            "max_comments_limit": self._max_comentarios,
            "max_memory_limit_mb": round(self._max_memory_bytes / (1024 * 1024), 2),
            "memory_utilization_pct": round((self._current_memory_estimate / self._max_memory_bytes) * 100, 1) if self._max_memory_bytes > 0 else 0,
            "count_utilization_pct": round((len(self._comentarios) / self._max_comentarios) * 100, 1) if self._max_comentarios > 0 else 0,
            "avg_comment_size_bytes": round(self._current_memory_estimate / len(self._comentarios)) if len(self._comentarios) > 0 else 0,
            "memory_bounded": True,
            "eviction_strategy": "LRU"
        }
    
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
        puntos_dolor_texto = [p.contexto_especifico for p in analisis_comentario.puntos_dolor if hasattr(p, 'contexto_especifico')]
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