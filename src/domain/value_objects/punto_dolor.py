"""
Value Object para representar puntos de dolor con severidad
"""
from dataclasses import dataclass
from enum import Enum
from typing import Optional, List


class TipoPuntoDolor(Enum):
    """Tipos específicos de puntos de dolor en telecomunicaciones"""
    # Problemas técnicos críticos
    SIN_SERVICIO = "sin_servicio"
    INTERMITENCIAS = "intermitencias" 
    VELOCIDAD_LENTA = "velocidad_lenta"
    CORTES_FRECUENTES = "cortes_frecuentes"
    MALA_CALIDAD = "mala_calidad"
    
    # Problemas de servicio al cliente
    MAL_SERVICIO_CLIENTE = "mal_servicio_cliente"
    DEMORAS_ATENCION = "demoras_atencion"  
    NO_RESUELVEN_PROBLEMAS = "no_resuelven_problemas"
    PERSONAL_NO_CAPACITADO = "personal_no_capacitado"
    DIFICULTAD_CONTACTO = "dificultad_contacto"
    
    # Problemas comerciales/facturación
    COBROS_INCORRECTOS = "cobros_incorrectos"
    PRECIOS_ALTOS = "precios_altos"
    PROMOCIONES_ENGAÑOSAS = "promociones_engañosas"
    CONTRATOS_ABUSIVOS = "contratos_abusivos"
    CARGOS_OCULTOS = "cargos_ocultos"
    
    # Problemas de instalación/equipos
    DEMORAS_INSTALACION = "demoras_instalacion"
    EQUIPOS_DEFECTUOSOS = "equipos_defectuosos"
    INSTALACION_DEFICIENTE = "instalacion_deficiente"
    PROBLEMAS_CONFIGURACION = "problemas_configuracion"
    
    # Otros
    FALTA_TRANSPARENCIA = "falta_transparencia"
    PROCESO_CANCELACION = "proceso_cancelacion"
    OTROS = "otros"


class NivelImpacto(Enum):
    """Nivel de impacto del punto de dolor"""
    CRITICO = "critico"        # Impide usar el servicio
    ALTO = "alto"              # Afecta significativamente la experiencia
    MODERADO = "moderado"      # Molestia notable pero usable
    BAJO = "bajo"              # Inconveniente menor


@dataclass(frozen=True)
class PuntoDolor:
    """
    Value Object que representa un punto de dolor detectado con su severidad
    
    La severidad PUEDE variar para capturar qué tan impactante
    es este problema específico en el comentario.
    """
    tipo: TipoPuntoDolor
    severidad: float             # 0.0-1.0 - qué tan severo es este problema
    confianza: float            # 0.0-1.0 - qué tan seguro está el análisis
    nivel_impacto: NivelImpacto # nivel categórico del impacto
    contexto_especifico: str    # contexto donde se menciona el problema
    palabras_clave: List[str] = None  # palabras que llevaron a la detección
    frecuencia_mencion: int = 1       # cuántas veces se menciona en el comentario
    
    def __post_init__(self):
        # Validar severidad
        if not (0.0 <= self.severidad <= 1.0):
            raise ValueError("La severidad debe estar entre 0.0 y 1.0")
        
        # Validar confianza
        if not (0.0 <= self.confianza <= 1.0):
            raise ValueError("La confianza debe estar entre 0.0 y 1.0")
        
        # Inicializar palabras_clave si es None
        if self.palabras_clave is None:
            object.__setattr__(self, 'palabras_clave', [])
        
        # Validar frecuencia
        if self.frecuencia_mencion < 1:
            raise ValueError("La frecuencia de mención debe ser al menos 1")
    
    @classmethod
    def crear_critico(cls, tipo: TipoPuntoDolor, severidad: float,
                     confianza: float = 0.9, contexto: str = "",
                     palabras_clave: List[str] = None, frecuencia: int = 1) -> 'PuntoDolor':
        """Factory method para puntos de dolor críticos"""
        if severidad < 0.7:
            raise ValueError("Un punto de dolor crítico debe tener severidad >= 0.7")
        
        return cls(tipo, severidad, confianza, NivelImpacto.CRITICO, 
                  contexto, palabras_clave or [], frecuencia)
    
    @classmethod
    def crear_alto_impacto(cls, tipo: TipoPuntoDolor, severidad: float,
                          confianza: float = 0.8, contexto: str = "",
                          palabras_clave: List[str] = None, frecuencia: int = 1) -> 'PuntoDolor':
        """Factory method para puntos de dolor de alto impacto"""
        if not (0.5 <= severidad < 0.8):
            raise ValueError("Un punto de dolor alto debe tener severidad entre 0.5 y 0.8")
        
        return cls(tipo, severidad, confianza, NivelImpacto.ALTO,
                  contexto, palabras_clave or [], frecuencia)
    
    @classmethod
    def crear_moderado(cls, tipo: TipoPuntoDolor, severidad: float,
                      confianza: float = 0.7, contexto: str = "",
                      palabras_clave: List[str] = None, frecuencia: int = 1) -> 'PuntoDolor':
        """Factory method para puntos de dolor moderados"""
        if not (0.3 <= severidad < 0.6):
            raise ValueError("Un punto de dolor moderado debe tener severidad entre 0.3 y 0.6")
        
        return cls(tipo, severidad, confianza, NivelImpacto.MODERADO,
                  contexto, palabras_clave or [], frecuencia)
    
    def es_tecnico(self) -> bool:
        """Determina si es un punto de dolor técnico"""
        return self.tipo in [TipoPuntoDolor.SIN_SERVICIO, TipoPuntoDolor.INTERMITENCIAS,
                            TipoPuntoDolor.VELOCIDAD_LENTA, TipoPuntoDolor.CORTES_FRECUENTES,
                            TipoPuntoDolor.MALA_CALIDAD]
    
    def es_servicio_cliente(self) -> bool:
        """Determina si es un problema de atención al cliente"""
        return self.tipo in [TipoPuntoDolor.MAL_SERVICIO_CLIENTE, TipoPuntoDolor.DEMORAS_ATENCION,
                            TipoPuntoDolor.NO_RESUELVEN_PROBLEMAS, TipoPuntoDolor.PERSONAL_NO_CAPACITADO,
                            TipoPuntoDolor.DIFICULTAD_CONTACTO]
    
    def es_comercial(self) -> bool:
        """Determina si es un problema comercial/facturación"""
        return self.tipo in [TipoPuntoDolor.COBROS_INCORRECTOS, TipoPuntoDolor.PRECIOS_ALTOS,
                            TipoPuntoDolor.PROMOCIONES_ENGAÑOSAS, TipoPuntoDolor.CONTRATOS_ABUSIVOS,
                            TipoPuntoDolor.CARGOS_OCULTOS]
    
    def es_critico(self) -> bool:
        """Determina si es crítico (impide usar servicio)"""
        return self.nivel_impacto == NivelImpacto.CRITICO or self.severidad >= 0.8
    
    def es_muy_severo(self, umbral: float = 0.7) -> bool:
        """Determina si tiene alta severidad"""
        return self.severidad >= umbral
    
    def es_confiable(self, umbral: float = 0.6) -> bool:
        """Verifica si la detección es confiable"""
        return self.confianza >= umbral
    
    def es_recurrente(self) -> bool:
        """Determina si se menciona múltiples veces"""
        return self.frecuencia_mencion > 1
    
    def requiere_atencion_inmediata(self) -> bool:
        """
        Determina si requiere atención inmediata
        (crítico + confiable + técnico/servicio)
        """
        return (self.es_critico() and 
                self.es_confiable(0.7) and 
                (self.es_tecnico() or self.es_servicio_cliente()))
    
    def obtener_descripcion_severidad(self) -> str:
        """Obtiene descripción textual de la severidad"""
        if self.severidad >= 0.8:
            return "muy severo"
        elif self.severidad >= 0.6:
            return "severo"
        elif self.severidad >= 0.4:
            return "moderado"
        elif self.severidad >= 0.2:
            return "leve"
        else:
            return "muy leve"
    
    def obtener_area_problema(self) -> str:
        """Obtiene el área general del problema"""
        if self.es_tecnico():
            return "técnico"
        elif self.es_servicio_cliente():
            return "servicio cliente"
        elif self.es_comercial():
            return "comercial/facturación"
        else:
            return "general"
    
    def calcular_prioridad(self) -> float:
        """
        Calcula prioridad basada en severidad, impacto y frecuencia
        0.0-1.0 donde 1.0 es máxima prioridad
        """
        base_prioridad = self.severidad * self.confianza
        
        # Bonus por nivel de impacto
        if self.nivel_impacto == NivelImpacto.CRITICO:
            base_prioridad *= 1.3
        elif self.nivel_impacto == NivelImpacto.ALTO:
            base_prioridad *= 1.1
        
        # Bonus por frecuencia
        if self.frecuencia_mencion > 1:
            base_prioridad *= (1 + 0.1 * (self.frecuencia_mencion - 1))
        
        return min(1.0, base_prioridad)
    
    def __str__(self) -> str:
        """Representación textual del punto de dolor"""
        tipo_name = self.tipo.value.replace('_', ' ')
        severidad_desc = self.obtener_descripcion_severidad()
        return f"{tipo_name} ({severidad_desc}, {self.nivel_impacto.value})"
    
    def to_dict(self) -> dict:
        """Convierte el punto de dolor a diccionario"""
        return {
            'tipo': self.tipo.value,
            'severidad': round(self.severidad, 3),
            'confianza': round(self.confianza, 3),
            'nivel_impacto': self.nivel_impacto.value,
            'contexto_especifico': self.contexto_especifico,
            'palabras_clave': self.palabras_clave,
            'frecuencia_mencion': self.frecuencia_mencion,
            'area_problema': self.obtener_area_problema(),
            'es_critico': self.es_critico(),
            'requiere_atencion_inmediata': self.requiere_atencion_inmediata(),
            'prioridad': round(self.calcular_prioridad(), 3)
        }