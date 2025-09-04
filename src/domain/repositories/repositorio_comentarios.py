"""
Repository interface para gestión de comentarios
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Union, TYPE_CHECKING
from ..entities.comentario import Comentario

if TYPE_CHECKING:
    from ..entities.analisis_comentario import AnalisisComentario


class IRepositorioComentarios(ABC):
    """
    Interface que define las operaciones de persistencia para comentarios
    Soporta tanto Comentario legacy como AnalisisComentario del sistema IA
    """
    
    @abstractmethod
    def guardar(self, comentario: Comentario) -> None:
        """Guarda un comentario"""
        pass
    
    @abstractmethod
    def guardar_lote(self, comentarios: Union[List[Comentario], List['AnalisisComentario']]) -> None:
        """Guarda múltiples comentarios (legacy o IA)"""
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