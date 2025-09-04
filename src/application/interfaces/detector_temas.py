"""
Interface para detección de temas
"""
from abc import ABC, abstractmethod
from typing import List
from ..dtos.temas_detectados import TemasDetectados


class IDetectorTemas(ABC):
    """
    Interface para servicios de detección de temas y análisis de contenido
    """
    
    @abstractmethod
    def detectar_temas(self, texto: str) -> TemasDetectados:
        """
        Detecta temas, puntos de dolor, emociones y competidores en un texto
        """
        pass
    
    @abstractmethod
    def detectar_temas_lote(self, textos: List[str]) -> List[TemasDetectados]:
        """
        Detecta temas para múltiples textos de manera eficiente
        """
        pass