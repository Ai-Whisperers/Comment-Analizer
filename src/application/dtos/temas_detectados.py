"""
DTO para temas detectados
"""
from dataclasses import dataclass
from typing import List


@dataclass
class TemasDetectados:
    """
    DTO que encapsula los diferentes temas y aspectos detectados en un texto
    """
    temas_principales: List[str]
    puntos_dolor: List[str]
    emociones_detectadas: List[str]
    competidores_mencionados: List[str]
    confianza: float = 0.0
    metodo_deteccion: str = "desconocido"