"""
Value Object para representar el sentimiento categórico de un comentario
"""
from dataclasses import dataclass
from enum import Enum


class SentimientoCategoria(Enum):
    """Solo 3 categorías de sentimiento - simple y determinista"""
    POSITIVO = "positivo"
    NEUTRAL = "neutral"  
    NEGATIVO = "negativo"


@dataclass(frozen=True)
class Sentimiento:
    """
    Value Object que representa SOLO la categoría de sentimiento de un comentario.
    
    IMPORTANTE: Este es categórico (solo 3 opciones), no granular.
    Para análisis granular usar el value object Emocion.
    """
    categoria: SentimientoCategoria
    confianza: float        # 0.0-1.0 - qué tan seguro está el análisis categórico
    fuente: str = "ia"      # "ia", "reglas", "manual"
    
    def __post_init__(self):
        # Validar confianza
        if not (0.0 <= self.confianza <= 1.0):
            raise ValueError("La confianza debe estar entre 0.0 y 1.0")
        
        # Validar fuente
        if self.fuente not in ["ia", "reglas", "manual"]:
            raise ValueError("Fuente debe ser 'ia', 'reglas' o 'manual'")
    
    @classmethod
    def crear_positivo(cls, confianza: float, fuente: str = "ia") -> 'Sentimiento':
        """Factory method para crear sentimiento positivo"""
        return cls(SentimientoCategoria.POSITIVO, confianza, fuente)
    
    @classmethod
    def crear_negativo(cls, confianza: float, fuente: str = "ia") -> 'Sentimiento':
        """Factory method para crear sentimiento negativo"""
        return cls(SentimientoCategoria.NEGATIVO, confianza, fuente)
    
    @classmethod
    def crear_neutral(cls, confianza: float, fuente: str = "ia") -> 'Sentimiento':
        """Factory method para crear sentimiento neutral"""
        return cls(SentimientoCategoria.NEUTRAL, confianza, fuente)
    
    def es_positivo(self) -> bool:
        """Verifica si el sentimiento es positivo"""
        return self.categoria == SentimientoCategoria.POSITIVO
    
    def es_negativo(self) -> bool:
        """Verifica si el sentimiento es negativo"""
        return self.categoria == SentimientoCategoria.NEGATIVO
    
    def es_neutral(self) -> bool:
        """Verifica si el sentimiento es neutral"""
        return self.categoria == SentimientoCategoria.NEUTRAL
    
    def es_muy_negativo(self) -> bool:
        """Determina si es un sentimiento muy negativo (alta confianza)"""
        return self.es_negativo() and self.confianza >= 0.8
    
    def es_confiable(self, umbral: float = 0.7) -> bool:
        """Verifica si la confianza del análisis supera el umbral"""
        return self.confianza >= umbral
    
    def obtener_valencia_numerica(self) -> float:
        """
        Obtiene valencia numérica simple para cálculos estadísticos
        -1.0 (negativo), 0.0 (neutral), 1.0 (positivo)
        """
        if self.es_positivo():
            return 1.0
        elif self.es_negativo():
            return -1.0
        else:
            return 0.0
    
    def __str__(self) -> str:
        return f"{self.categoria.value} (conf: {self.confianza:.2f})"
    
    def to_dict(self) -> dict:
        """Convierte el sentimiento a diccionario para serialización"""
        return {
            'categoria': self.categoria.value,
            'confianza': round(self.confianza, 3),
            'fuente': self.fuente,
            'valencia_numerica': self.obtener_valencia_numerica()
        }