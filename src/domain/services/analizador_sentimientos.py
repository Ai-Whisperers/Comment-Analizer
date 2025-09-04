"""
Servicio de dominio para análisis de sentimientos
"""
from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.comentario import Comentario
from ..value_objects.sentimiento import Sentimiento


class IAnalizadorSentimientos(ABC):
    """
    Interfaz para servicios de análisis de sentimientos
    """
    
    @abstractmethod
    def analizar_sentimiento(self, texto: str) -> Sentimiento:
        """Analiza el sentimiento de un texto individual"""
        pass
    
    @abstractmethod
    def analizar_lote(self, textos: List[str]) -> List[Sentimiento]:
        """Analiza el sentimiento de múltiples textos"""
        pass
    
    @abstractmethod
    def es_disponible(self) -> bool:
        """Verifica si el analizador está disponible"""
        pass


class ServicioAnalisisSentimientos:
    """
    Servicio de dominio que orquesta el análisis de sentimientos
    con múltiples estrategias (IA, reglas, etc.)
    """
    
    def __init__(self, analizadores: List[IAnalizadorSentimientos]):
        """
        Inicializa el servicio con una lista de analizadores ordenados por prioridad
        """
        self.analizadores = analizadores
    
    def analizar_comentario(self, comentario: Comentario) -> Comentario:
        """
        Analiza el sentimiento de un comentario usando el mejor analizador disponible
        """
        if not comentario.es_valido():
            raise ValueError("El comentario no es válido para análisis")
        
        # Buscar el primer analizador disponible
        for analizador in self.analizadores:
            if analizador.es_disponible():
                try:
                    sentimiento = analizador.analizar_sentimiento(comentario.texto_limpio)
                    comentario.sentimiento = sentimiento
                    return comentario
                except Exception:
                    # Si falla, intentar con el siguiente
                    continue
        
        # Si todos fallan, usar sentimiento neutral por defecto
        comentario.sentimiento = Sentimiento.crear_neutral(0.5, "fallback")
        return comentario
    
    def analizar_lote_comentarios(self, comentarios: List[Comentario]) -> List[Comentario]:
        """
        Analiza el sentimiento de múltiples comentarios de manera eficiente
        """
        if not comentarios:
            return []
        
        # Filtrar comentarios válidos
        comentarios_validos = [c for c in comentarios if c.es_valido()]
        
        if not comentarios_validos:
            return comentarios
        
        # Intentar análisis por lotes con el primer analizador disponible
        for analizador in self.analizadores:
            if analizador.es_disponible():
                try:
                    textos = [c.texto_limpio for c in comentarios_validos]
                    sentimientos = analizador.analizar_lote(textos)
                    
                    # Asignar sentimientos a comentarios
                    for comentario, sentimiento in zip(comentarios_validos, sentimientos):
                        comentario.sentimiento = sentimiento
                    
                    return comentarios
                except Exception:
                    # Si falla el análisis por lotes, intentar individual
                    continue
        
        # Fallback: análisis individual
        for comentario in comentarios_validos:
            self.analizar_comentario(comentario)
        
        return comentarios
    
    def obtener_estadisticas_sentimientos(self, comentarios: List[Comentario]) -> dict:
        """
        Calcula estadísticas de sentimientos para un conjunto de comentarios
        """
        comentarios_con_sentimiento = [
            c for c in comentarios 
            if c.sentimiento is not None
        ]
        
        if not comentarios_con_sentimiento:
            return {
                'total': 0,
                'positivos': 0,
                'negativos': 0,
                'neutrales': 0,
                'porcentaje_positivos': 0.0,
                'porcentaje_negativos': 0.0,
                'porcentaje_neutrales': 0.0,
                'confianza_promedio': 0.0
            }
        
        total = len(comentarios_con_sentimiento)
        positivos = sum(1 for c in comentarios_con_sentimiento if c.sentimiento.es_positivo())
        negativos = sum(1 for c in comentarios_con_sentimiento if c.sentimiento.es_negativo())
        neutrales = sum(1 for c in comentarios_con_sentimiento if c.sentimiento.es_neutral())
        
        confianza_promedio = sum(c.sentimiento.confianza for c in comentarios_con_sentimiento) / total
        
        return {
            'total': total,
            'positivos': positivos,
            'negativos': negativos,
            'neutrales': neutrales,
            'porcentaje_positivos': round((positivos / total) * 100, 1),
            'porcentaje_negativos': round((negativos / total) * 100, 1),
            'porcentaje_neutrales': round((neutrales / total) * 100, 1),
            'confianza_promedio': round(confianza_promedio, 3)
        }