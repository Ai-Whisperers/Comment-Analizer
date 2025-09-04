"""
Value Object para representar temas principales con relevancia
"""
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class CategoriaTemaTelco(Enum):
    """Categorías de temas específicos para telecomunicaciones"""
    # Servicio técnico
    VELOCIDAD = "velocidad"
    CONECTIVIDAD = "conectividad"  
    ESTABILIDAD = "estabilidad"
    COBERTURA = "cobertura"
    CALIDAD_SEÑAL = "calidad_señal"
    
    # Servicio comercial
    PRECIO = "precio"
    PLANES = "planes"
    PROMOCIONES = "promociones"
    FACTURACION = "facturacion"
    CONTRATOS = "contratos"
    
    # Atención al cliente
    SERVICIO_CLIENTE = "servicio_cliente"
    SOPORTE_TECNICO = "soporte_tecnico"
    TIEMPO_RESPUESTA = "tiempo_respuesta"
    RESOLUCION_PROBLEMAS = "resolucion_problemas"
    
    # Instalación y equipos
    INSTALACION = "instalacion"
    EQUIPOS = "equipos"
    CONFIGURACION = "configuracion"
    MANTENIMIENTO = "mantenimiento"
    
    # Comparación y competencia
    COMPETENCIA = "competencia"
    CAMBIO_PROVEEDOR = "cambio_proveedor"
    RECOMENDACIONES = "recomendaciones"
    
    # General
    SATISFACCION_GENERAL = "satisfaccion_general"
    OTROS = "otros"


@dataclass(frozen=True)
class TemaPrincipal:
    """
    Value Object que representa un tema detectado con su relevancia
    
    La relevancia PUEDE variar para capturar qué tan importante 
    es este tema en el contexto específico del comentario.
    """
    categoria: CategoriaTemaTelco
    relevancia: float           # 0.0-1.0 - qué tan relevante es este tema en el comentario
    confianza: float           # 0.0-1.0 - qué tan seguro está el análisis de que este tema está presente
    contexto_especifico: str   # contexto específico donde se menciona
    palabras_clave: list = None  # palabras específicas que llevaron a la detección
    
    def __post_init__(self):
        # Validar relevancia
        if not (0.0 <= self.relevancia <= 1.0):
            raise ValueError("La relevancia debe estar entre 0.0 y 1.0")
        
        # Validar confianza
        if not (0.0 <= self.confianza <= 1.0):
            raise ValueError("La confianza debe estar entre 0.0 y 1.0")
        
        # Inicializar palabras_clave si es None
        if self.palabras_clave is None:
            object.__setattr__(self, 'palabras_clave', [])
    
    @classmethod
    def crear_tecnico(cls, categoria: CategoriaTemaTelco, relevancia: float,
                     confianza: float = 0.8, contexto: str = "",
                     palabras_clave: list = None) -> 'TemaPrincipal':
        """Factory method para temas técnicos"""
        if categoria not in [CategoriaTemaTelco.VELOCIDAD, CategoriaTemaTelco.CONECTIVIDAD,
                            CategoriaTemaTelco.ESTABILIDAD, CategoriaTemaTelco.COBERTURA,
                            CategoriaTemaTelco.CALIDAD_SEÑAL]:
            raise ValueError(f"{categoria.value} no es un tema técnico")
        
        return cls(categoria, relevancia, confianza, contexto, palabras_clave or [])
    
    @classmethod  
    def crear_comercial(cls, categoria: CategoriaTemaTelco, relevancia: float,
                       confianza: float = 0.8, contexto: str = "",
                       palabras_clave: list = None) -> 'TemaPrincipal':
        """Factory method para temas comerciales"""
        if categoria not in [CategoriaTemaTelco.PRECIO, CategoriaTemaTelco.PLANES,
                            CategoriaTemaTelco.PROMOCIONES, CategoriaTemaTelco.FACTURACION,
                            CategoriaTemaTelco.CONTRATOS]:
            raise ValueError(f"{categoria.value} no es un tema comercial")
        
        return cls(categoria, relevancia, confianza, contexto, palabras_clave or [])
    
    @classmethod
    def crear_servicio(cls, categoria: CategoriaTemaTelco, relevancia: float,
                      confianza: float = 0.8, contexto: str = "",
                      palabras_clave: list = None) -> 'TemaPrincipal':
        """Factory method para temas de servicio al cliente"""
        if categoria not in [CategoriaTemaTelco.SERVICIO_CLIENTE, CategoriaTemaTelco.SOPORTE_TECNICO,
                            CategoriaTemaTelco.TIEMPO_RESPUESTA, CategoriaTemaTelco.RESOLUCION_PROBLEMAS]:
            raise ValueError(f"{categoria.value} no es un tema de servicio")
        
        return cls(categoria, relevancia, confianza, contexto, palabras_clave or [])
    
    def es_tecnico(self) -> bool:
        """Determina si es un tema técnico"""
        return self.categoria in [CategoriaTemaTelco.VELOCIDAD, CategoriaTemaTelco.CONECTIVIDAD,
                                 CategoriaTemaTelco.ESTABILIDAD, CategoriaTemaTelco.COBERTURA,
                                 CategoriaTemaTelco.CALIDAD_SEÑAL]
    
    def es_comercial(self) -> bool:
        """Determina si es un tema comercial/financiero"""
        return self.categoria in [CategoriaTemaTelco.PRECIO, CategoriaTemaTelco.PLANES,
                                 CategoriaTemaTelco.PROMOCIONES, CategoriaTemaTelco.FACTURACION,
                                 CategoriaTemaTelco.CONTRATOS]
    
    def es_servicio_cliente(self) -> bool:
        """Determina si es un tema de atención al cliente"""
        return self.categoria in [CategoriaTemaTelco.SERVICIO_CLIENTE, CategoriaTemaTelco.SOPORTE_TECNICO,
                                 CategoriaTemaTelco.TIEMPO_RESPUESTA, CategoriaTemaTelco.RESOLUCION_PROBLEMAS]
    
    def es_muy_relevante(self, umbral: float = 0.7) -> bool:
        """Determina si el tema tiene alta relevancia"""
        return self.relevancia >= umbral
    
    def es_confiable(self, umbral: float = 0.6) -> bool:
        """Verifica si la detección es confiable"""
        return self.confianza >= umbral
    
    def requiere_atencion_prioritaria(self) -> bool:
        """
        Determina si este tema requiere atención prioritaria
        (alta relevancia + confiable + técnico)
        """
        return (self.es_muy_relevante(0.6) and 
                self.es_confiable(0.7) and 
                self.es_tecnico())
    
    def obtener_descripcion_relevancia(self) -> str:
        """Obtiene una descripción textual de la relevancia"""
        if self.relevancia >= 0.8:
            return "muy relevante"
        elif self.relevancia >= 0.6:
            return "relevante"
        elif self.relevancia >= 0.4:
            return "moderadamente relevante"
        elif self.relevancia >= 0.2:
            return "poco relevante"
        else:
            return "marginal"
    
    def obtener_tipo_tema(self) -> str:
        """Obtiene el tipo general del tema"""
        if self.es_tecnico():
            return "técnico"
        elif self.es_comercial():
            return "comercial"
        elif self.es_servicio_cliente():
            return "servicio"
        else:
            return "general"
    
    def __str__(self) -> str:
        """Representación textual del tema"""
        categoria_name = self.categoria.value.replace('_', ' ')
        relevancia_desc = self.obtener_descripcion_relevancia()
        return f"{categoria_name} ({relevancia_desc}, {self.obtener_tipo_tema()})"
    
    def to_dict(self) -> dict:
        """Convierte el tema a diccionario para serialización"""
        return {
            'categoria': self.categoria.value,
            'relevancia': round(self.relevancia, 3),
            'confianza': round(self.confianza, 3),
            'contexto_especifico': self.contexto_especifico,
            'palabras_clave': self.palabras_clave,
            'tipo_tema': self.obtener_tipo_tema(),
            'es_muy_relevante': self.es_muy_relevante(),
            'requiere_atencion': self.requiere_atencion_prioritaria()
        }