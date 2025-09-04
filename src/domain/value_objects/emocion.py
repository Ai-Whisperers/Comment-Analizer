"""
Value Object para representar emociones con intensidad granular
"""
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class TipoEmocion(Enum):
    """Tipos de emociones granulares detectables"""
    # Emociones positivas
    SATISFACCION = "satisfaccion"
    ALEGRIA = "alegria"
    ENTUSIASMO = "entusiasmo"
    GRATITUD = "gratitud"
    CONFIANZA = "confianza"
    
    # Emociones negativas
    FRUSTRACION = "frustracion"
    ENOJO = "enojo"
    DECEPCION = "decepcion"
    PREOCUPACION = "preocupacion"
    IRRITACION = "irritacion"
    ANSIEDAD = "ansiedad"
    TRISTEZA = "tristeza"
    
    # Emociones neutras/mixtas
    CONFUSION = "confusion"
    ESPERANZA = "esperanza"
    CURIOSIDAD = "curiosidad"
    IMPACIENCIA = "impaciencia"


@dataclass(frozen=True)
class Emocion:
    """
    Value Object que representa una emoción con intensidad granular
    
    A diferencia de Sentimiento (solo 3 categorías), las emociones son granulares
    y DEBEN tener intensidades variables para capturar matices emocionales.
    """
    tipo: TipoEmocion
    intensidad: float      # 0.0-1.0 - qué tan intensa es la emoción
    confianza: float       # 0.0-1.0 - qué tan seguro está el análisis
    contexto: str = ""     # contexto específico donde se detectó
    
    def __post_init__(self):
        # Validar intensidad
        if not (0.0 <= self.intensidad <= 1.0):
            raise ValueError("La intensidad debe estar entre 0.0 y 1.0")
        
        # Validar confianza
        if not (0.0 <= self.confianza <= 1.0):
            raise ValueError("La confianza debe estar entre 0.0 y 1.0")
    
    @classmethod
    def crear_positiva(cls, tipo: TipoEmocion, intensidad: float, 
                      confianza: float = 0.8, contexto: str = "") -> 'Emocion':
        """Factory method para emociones positivas"""
        if tipo not in [TipoEmocion.SATISFACCION, TipoEmocion.ALEGRIA, 
                       TipoEmocion.ENTUSIASMO, TipoEmocion.GRATITUD, TipoEmocion.CONFIANZA]:
            raise ValueError(f"{tipo.value} no es una emoción positiva")
        
        return cls(tipo, intensidad, confianza, contexto)
    
    @classmethod  
    def crear_negativa(cls, tipo: TipoEmocion, intensidad: float,
                      confianza: float = 0.8, contexto: str = "") -> 'Emocion':
        """Factory method para emociones negativas"""
        if tipo not in [TipoEmocion.FRUSTRACION, TipoEmocion.ENOJO, TipoEmocion.DECEPCION,
                       TipoEmocion.PREOCUPACION, TipoEmocion.IRRITACION, TipoEmocion.ANSIEDAD,
                       TipoEmocion.TRISTEZA]:
            raise ValueError(f"{tipo.value} no es una emoción negativa")
        
        return cls(tipo, intensidad, confianza, contexto)
    
    @classmethod
    def crear_neutra(cls, tipo: TipoEmocion, intensidad: float,
                    confianza: float = 0.7, contexto: str = "") -> 'Emocion':
        """Factory method para emociones neutras/mixtas"""
        if tipo not in [TipoEmocion.CONFUSION, TipoEmocion.ESPERANZA,
                       TipoEmocion.CURIOSIDAD, TipoEmocion.IMPACIENCIA]:
            raise ValueError(f"{tipo.value} no es una emoción neutra")
        
        return cls(tipo, intensidad, confianza, contexto)
    
    def es_positiva(self) -> bool:
        """Determina si la emoción es de valencia positiva"""
        return self.tipo in [TipoEmocion.SATISFACCION, TipoEmocion.ALEGRIA,
                            TipoEmocion.ENTUSIASMO, TipoEmocion.GRATITUD, TipoEmocion.CONFIANZA]
    
    def es_negativa(self) -> bool:
        """Determina si la emoción es de valencia negativa"""
        return self.tipo in [TipoEmocion.FRUSTRACION, TipoEmocion.ENOJO, TipoEmocion.DECEPCION,
                            TipoEmocion.PREOCUPACION, TipoEmocion.IRRITACION, 
                            TipoEmocion.ANSIEDAD, TipoEmocion.TRISTEZA]
    
    def es_neutra(self) -> bool:
        """Determina si la emoción es neutra/mixta"""
        return not (self.es_positiva() or self.es_negativa())
    
    def es_intensa(self, umbral: float = 0.7) -> bool:
        """Determina si la emoción tiene alta intensidad"""
        return self.intensidad >= umbral
    
    def es_confiable(self, umbral: float = 0.6) -> bool:
        """Verifica si la detección es confiable"""
        return self.confianza >= umbral
    
    def requiere_atencion(self) -> bool:
        """
        Determina si esta emoción requiere atención especial
        (emociones negativas intensas y confiables)
        """
        return (self.es_negativa() and 
                self.es_intensa(0.6) and 
                self.es_confiable(0.7))
    
    def obtener_descripcion_intensidad(self) -> str:
        """Obtiene una descripción textual de la intensidad"""
        if self.intensidad >= 0.8:
            return "muy intensa"
        elif self.intensidad >= 0.6:
            return "intensa"
        elif self.intensidad >= 0.4:
            return "moderada"
        elif self.intensidad >= 0.2:
            return "leve"
        else:
            return "muy leve"
    
    def __str__(self) -> str:
        """Representación textual de la emoción"""
        descripcion = f"{self.tipo.value.replace('_', ' ')}"
        intensidad_desc = self.obtener_descripcion_intensidad()
        return f"{descripcion} ({intensidad_desc}, confianza: {self.confianza:.2f})"
    
    def to_dict(self) -> dict:
        """Convierte la emoción a diccionario para serialización"""
        return {
            'tipo': self.tipo.value,
            'intensidad': round(self.intensidad, 3),
            'confianza': round(self.confianza, 3),
            'contexto': self.contexto,
            'es_positiva': self.es_positiva(),
            'es_negativa': self.es_negativa(),
            'requiere_atencion': self.requiere_atencion()
        }