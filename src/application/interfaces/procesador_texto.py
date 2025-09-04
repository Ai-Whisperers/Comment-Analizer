"""
Interface para procesamiento de texto
"""
from abc import ABC, abstractmethod
from typing import List
from ...domain.entities.comentario import Comentario


class IProcesadorTexto(ABC):
    """
    Interface para servicios de procesamiento de texto
    """
    
    @abstractmethod
    def limpiar_texto(self, texto: str) -> str:
        """
        Limpia y normaliza un texto
        """
        pass
    
    @abstractmethod
    def consolidar_duplicados(self, comentarios: List[Comentario]) -> List[Comentario]:
        """
        Consolida comentarios duplicados sumando sus frecuencias
        """
        pass
    
    @abstractmethod
    def detectar_idioma(self, texto: str) -> str:
        """
        Detecta el idioma del texto
        """
        pass