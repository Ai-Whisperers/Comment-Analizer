"""
Value Object para representar la calidad de un comentario
"""
from dataclasses import dataclass
from enum import Enum


class NivelCalidad(Enum):
    """Niveles de calidad posibles"""
    ALTA = "alta"
    MEDIA = "media"
    BAJA = "baja"


@dataclass(frozen=True)
class CalidadComentario:
    """
    Value Object que representa la calidad de un comentario
    """
    nivel: NivelCalidad
    es_informativo: bool
    nivel_detalle: str  # "alto", "medio", "bajo"
    longitud_caracteres: int
    
    def __post_init__(self):
        # Validaciones
        if self.longitud_caracteres < 0:
            raise ValueError("La longitud no puede ser negativa")
        
        if self.nivel_detalle not in ["alto", "medio", "bajo"]:
            raise ValueError("Nivel de detalle debe ser 'alto', 'medio' o 'bajo'")
    
    @classmethod
    def evaluar_desde_texto(cls, texto: str, temas_detectados: int = 0) -> 'CalidadComentario':
        """
        Factory method que evalúa la calidad basada en el texto y temas detectados
        """
        longitud = len(texto.strip())
        
        # Determinar nivel de detalle por longitud
        if longitud > 100:
            nivel_detalle = "alto"
        elif longitud > 50:
            nivel_detalle = "medio"
        else:
            nivel_detalle = "bajo"
        
        # Determinar si es informativo
        es_informativo = temas_detectados > 1 or longitud > 30
        
        # Determinar nivel de calidad
        if es_informativo and longitud > 100 and temas_detectados > 2:
            nivel = NivelCalidad.ALTA
        elif es_informativo and longitud > 50 and temas_detectados > 1:
            nivel = NivelCalidad.MEDIA
        else:
            nivel = NivelCalidad.BAJA
        
        return cls(nivel, es_informativo, nivel_detalle, longitud)
    
    def es_alta_calidad(self) -> bool:
        """Verifica si el comentario es de alta calidad"""
        return self.nivel == NivelCalidad.ALTA
    
    def requiere_atencion_especial(self) -> bool:
        """Determina si merece atención especial por ser muy informativo"""
        return self.es_informativo and self.es_alta_calidad()
    
    def puntuacion_calidad(self) -> float:
        """
        Retorna una puntuación numérica de calidad (0.0 - 1.0)
        """
        base_score = {
            NivelCalidad.ALTA: 0.8,
            NivelCalidad.MEDIA: 0.6,
            NivelCalidad.BAJA: 0.3
        }[self.nivel]
        
        # Bonus por ser informativo
        if self.es_informativo:
            base_score += 0.2
        
        return min(base_score, 1.0)
    
    def __str__(self) -> str:
        return f"Calidad {self.nivel.value} ({'informativo' if self.es_informativo else 'básico'})"