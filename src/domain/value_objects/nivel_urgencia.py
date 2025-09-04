"""
Value Object para representar el nivel de urgencia de un comentario
"""
from dataclasses import dataclass
from enum import Enum
from typing import List


class PrioridadUrgencia(Enum):
    """Niveles de prioridad de urgencia"""
    P0 = "P0"  # Crítico - Sin servicio
    P1 = "P1"  # Alto - Problema grave
    P2 = "P2"  # Medio - Problema moderado
    P3 = "P3"  # Bajo - Consulta general


@dataclass(frozen=True)
class NivelUrgencia:
    """
    Value Object que representa el nivel de urgencia de un comentario
    """
    prioridad: PrioridadUrgencia
    indicadores: List[str]
    puntuacion: float  # 0.0 - 10.0
    
    def __post_init__(self):
        # Validaciones
        if not (0.0 <= self.puntuacion <= 10.0):
            raise ValueError("La puntuación debe estar entre 0.0 y 10.0")
        
        # Convertir a lista inmutable
        object.__setattr__(self, 'indicadores', tuple(self.indicadores))
    
    @classmethod
    def evaluar_urgencia(cls, puntos_dolor: List[str], sentimiento_negativo: bool = False, 
                        confianza: float = 0.5) -> 'NivelUrgencia':
        """
        Factory method que evalúa la urgencia basada en puntos de dolor
        """
        # Indicadores críticos (P0)
        indicadores_criticos = [
            'sin servicio', 'no funciona', 'cortado', 'emergencia',
            'no tengo internet', 'caído', 'desconectado'
        ]
        
        # Indicadores altos (P1)
        indicadores_altos = [
            'muy lento', 'problema grave', 'urgente', 'inmediato',
            'no puedo trabajar', 'pérdida de dinero'
        ]
        
        # Indicadores medios (P2)
        indicadores_medios = [
            'lento', 'problema', 'falla', 'intermitente',
            'a veces no funciona', 'irregular'
        ]
        
        puntuacion = 0.0
        indicadores_encontrados = []
        
        # Evaluar puntos de dolor
        for punto in puntos_dolor:
            punto_lower = punto.lower()
            
            # Críticos
            if any(critico in punto_lower for critico in indicadores_criticos):
                puntuacion += 4.0
                indicadores_encontrados.append(punto)
            # Altos
            elif any(alto in punto_lower for alto in indicadores_altos):
                puntuacion += 2.5
                indicadores_encontrados.append(punto)
            # Medios
            elif any(medio in punto_lower for medio in indicadores_medios):
                puntuacion += 1.5
                indicadores_encontrados.append(punto)
        
        # Ajuste por sentimiento negativo
        if sentimiento_negativo and confianza > 0.8:
            puntuacion += 1.0
        
        # Ajuste por confianza
        puntuacion *= confianza
        
        # Determinar prioridad
        if puntuacion >= 6.0:
            prioridad = PrioridadUrgencia.P0
        elif puntuacion >= 4.0:
            prioridad = PrioridadUrgencia.P1
        elif puntuacion >= 2.0:
            prioridad = PrioridadUrgencia.P2
        else:
            prioridad = PrioridadUrgencia.P3
        
        return cls(prioridad, indicadores_encontrados, min(puntuacion, 10.0))
    
    def es_critico(self) -> bool:
        """Verifica si requiere atención crítica inmediata"""
        return self.prioridad == PrioridadUrgencia.P0
    
    def es_alta_prioridad(self) -> bool:
        """Verifica si es de alta prioridad"""
        return self.prioridad in [PrioridadUrgencia.P0, PrioridadUrgencia.P1]
    
    def tiempo_respuesta_objetivo_horas(self) -> int:
        """
        Retorna el tiempo objetivo de respuesta en horas
        """
        tiempos = {
            PrioridadUrgencia.P0: 1,    # 1 hora
            PrioridadUrgencia.P1: 4,    # 4 horas
            PrioridadUrgencia.P2: 24,   # 24 horas
            PrioridadUrgencia.P3: 72    # 72 horas
        }
        return tiempos[self.prioridad]
    
    def accion_recomendada(self) -> str:
        """
        Retorna la acción recomendada según la urgencia
        """
        acciones = {
            PrioridadUrgencia.P0: "Respuesta técnica inmediata - Contactar al cliente",
            PrioridadUrgencia.P1: "Escalamiento técnico - Resolver dentro de 4 horas",
            PrioridadUrgencia.P2: "Seguimiento estándar - Resolver en 24 horas",
            PrioridadUrgencia.P3: "Proceso normal - Responder en 72 horas"
        }
        return acciones[self.prioridad]
    
    def __str__(self) -> str:
        return f"{self.prioridad.value} (Score: {self.puntuacion:.1f})"