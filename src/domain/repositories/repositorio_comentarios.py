"""
Repository interface para gestión de comentarios
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.comentario import Comentario


class IRepositorioComentarios(ABC):
    """
    Interface que define las operaciones de persistencia para comentarios
    """
    
    @abstractmethod
    def guardar(self, comentario: Comentario) -> None:
        """Guarda un comentario"""
        pass
    
    @abstractmethod
    def guardar_lote(self, comentarios: List[Comentario]) -> None:
        """Guarda múltiples comentarios"""
        pass
    
    @abstractmethod
    def obtener_por_id(self, id_comentario: str) -> Optional[Comentario]:
        """Obtiene un comentario por su ID"""
        pass
    
    @abstractmethod
    def obtener_todos(self) -> List[Comentario]:
        """Obtiene todos los comentarios"""
        pass
    
    @abstractmethod
    def buscar_por_sentimiento(self, tipo_sentimiento: str) -> List[Comentario]:
        """Busca comentarios por tipo de sentimiento"""
        pass
    
    @abstractmethod
    def buscar_criticos(self) -> List[Comentario]:
        """Busca comentarios que requieren atención crítica"""
        pass
    
    @abstractmethod
    def limpiar(self) -> None:
        """Limpia todos los comentarios del repositorio"""
        pass