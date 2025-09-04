"""
Value Object para representar el sentimiento de un comentario
"""
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class TipoSentimiento(Enum):
    """Tipos de sentimiento posibles"""
    POSITIVO = "positivo"
    NEUTRAL = "neutral"
    NEGATIVO = "negativo"


@dataclass(frozen=True)
class Sentimiento:
    """
    Value Object que representa el sentimiento de un comentario con su confianza
    """
    tipo: TipoSentimiento
    confianza: float
    fuente: str = "desconocida"  # "ia", "reglas", "manual"
    
    def __post_init__(self):
        # Validar confianza
        if not (0.0 <= self.confianza <= 1.0):
            raise ValueError("La confianza debe estar entre 0.0 y 1.0")
    
    @classmethod
    def crear_positivo(cls, confianza: float, fuente: str = "desconocida") -> 'Sentimiento':
        """Factory method para crear sentimiento positivo"""
        return cls(TipoSentimiento.POSITIVO, confianza, fuente)
    
    @classmethod
    def crear_negativo(cls, confianza: float, fuente: str = "desconocida") -> 'Sentimiento':
        """Factory method para crear sentimiento negativo"""
        return cls(TipoSentimiento.NEGATIVO, confianza, fuente)
    
    @classmethod
    def crear_neutral(cls, confianza: float, fuente: str = "desconocida") -> 'Sentimiento':
        """Factory method para crear sentimiento neutral"""
        return cls(TipoSentimiento.NEUTRAL, confianza, fuente)
    
    def es_positivo(self) -> bool:
        """Verifica si el sentimiento es positivo"""
        return self.tipo == TipoSentimiento.POSITIVO
    
    def es_negativo(self) -> bool:
        """Verifica si el sentimiento es negativo"""
        return self.tipo == TipoSentimiento.NEGATIVO
    
    def es_neutral(self) -> bool:
        """Verifica si el sentimiento es neutral"""
        return self.tipo == TipoSentimiento.NEUTRAL
    
    def es_muy_negativo(self) -> bool:
        """Determina si es un sentimiento muy negativo (alta confianza)"""
        return self.es_negativo() and self.confianza >= 0.8
    
    def es_confiable(self, umbral: float = 0.7) -> bool:
        """Verifica si la confianza del análisis supera el umbral"""
        return self.confianza >= umbral
    
    def obtener_puntuacion_nps(self) -> int:
        """
        Convierte el sentimiento a una puntuación NPS estimada (0-10)
        """
        if self.es_positivo():
            # Positivo: 7-10 basado en confianza
            return int(7 + (3 * self.confianza))
        elif self.es_negativo():
            # Negativo: 0-6 basado en confianza (inversa)
            return int(6 * (1 - self.confianza))
        else:
            # Neutral: 6-8 basado en confianza
            return int(6 + (2 * self.confianza))
    
    def __str__(self) -> str:
        return f"{self.tipo.value} ({self.confianza:.2f})"