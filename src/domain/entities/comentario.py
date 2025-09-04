"""
Entidad de dominio Comentario - Representa un comentario de cliente
"""
from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime

from ..value_objects.sentimiento import Sentimiento
from ..value_objects.calidad_comentario import CalidadComentario
from ..value_objects.nivel_urgencia import NivelUrgencia


@dataclass
class Comentario:
    """
    Entidad de dominio que representa un comentario de cliente
    """
    id: str
    texto: str
    texto_limpio: str
    frecuencia: int = 1
    fecha_analisis: Optional[datetime] = None
    
    # Análisis de sentimiento
    sentimiento: Optional[Sentimiento] = None
    
    # Calidad del comentario
    calidad: Optional[CalidadComentario] = None
    
    # Nivel de urgencia
    urgencia: Optional[NivelUrgencia] = None
    
    # Temas detectados
    temas: List[str] = None
    
    # Puntos de dolor identificados
    puntos_dolor: List[str] = None
    
    # Emociones detectadas
    emociones: List[str] = None
    
    # Competidores mencionados
    competidores: List[str] = None
    
    # Calificación original (si existe)
    calificacion_nps: Optional[int] = None
    calificacion_nota: Optional[float] = None
    
    def __post_init__(self):
        if self.temas is None:
            self.temas = []
        if self.puntos_dolor is None:
            self.puntos_dolor = []
        if self.emociones is None:
            self.emociones = []
        if self.competidores is None:
            self.competidores = []
        if self.fecha_analisis is None:
            self.fecha_analisis = datetime.now()
    
    def es_valido(self) -> bool:
        """Valida que el comentario tenga los datos mínimos necesarios"""
        return bool(self.texto and self.texto.strip())
    
    def tiene_analisis_completo(self) -> bool:
        """Verifica si el comentario tiene análisis completo"""
        return (
            self.sentimiento is not None and
            self.calidad is not None and
            self.urgencia is not None
        )
    
    def agregar_tema(self, tema: str) -> None:
        """Agrega un tema si no existe ya"""
        if tema and tema not in self.temas:
            self.temas.append(tema)
    
    def agregar_punto_dolor(self, punto: str) -> None:
        """Agrega un punto de dolor si no existe ya"""
        if punto and punto not in self.puntos_dolor:
            self.puntos_dolor.append(punto)
    
    def es_critico(self) -> bool:
        """Determina si el comentario requiere atención crítica"""
        return (
            self.urgencia and self.urgencia.es_critico() or
            self.sentimiento and self.sentimiento.es_muy_negativo()
        )