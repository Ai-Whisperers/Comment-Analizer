"""
Entidad principal que representa el resultado completo del análisis de un comentario
"""
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

from ..value_objects.sentimiento import Sentimiento
from ..value_objects.emocion import Emocion
from ..value_objects.tema_principal import TemaPrincipal
from ..value_objects.punto_dolor import PuntoDolor


@dataclass
class AnalisisComentario:
    """
    Entidad de dominio que representa el análisis completo de un comentario
    
    Esta entidad encapsula TODOS los resultados del análisis IA:
    - Sentimiento categórico (determinista)
    - Emociones granulares (con intensidades)
    - Temas principales (con relevancia)
    - Puntos de dolor (con severidad)
    - Análisis narrativo de IA
    """
    
    # Identificación
    id: str
    indice_original: int           # índice en el archivo original
    texto_original: str
    
    # Análisis categórico (determinista)
    sentimiento: Sentimiento       # Solo 3 categorías: positivo/neutral/negativo
    
    # Análisis granular (con intensidades variables)
    emociones: List[Emocion] = field(default_factory=list)          # Emociones con intensidades
    temas: List[TemaPrincipal] = field(default_factory=list)        # Temas con relevancia
    puntos_dolor: List[PuntoDolor] = field(default_factory=list)    # Problemas con severidad
    
    # Análisis narrativo de IA (variable - debe cambiar entre ejecuciones)
    resumen_ia: str = ""           # Análisis específico de este comentario por IA
    recomendaciones: List[str] = field(default_factory=list)  # Acciones sugeridas para este comentario
    
    # Metadatos del análisis
    confianza_general: float = 0.0      # Confianza global del análisis
    fecha_analisis: datetime = field(default_factory=datetime.now)
    modelo_ia_utilizado: str = "unknown"
    tiempo_analisis_ms: float = 0.0     # Tiempo específico para este comentario
    
    # Datos originales del archivo (si existen)
    calificacion_nps: Optional[int] = None
    calificacion_nota: Optional[float] = None
    metadatos_adicionales: dict = field(default_factory=dict)
    
    def es_valido(self) -> bool:
        """Valida que el análisis tenga los datos mínimos necesarios"""
        return (
            bool(self.texto_original.strip()) and
            self.sentimiento is not None and
            self.confianza_general > 0.0
        )
    
    def tiene_analisis_completo(self) -> bool:
        """Verifica si el comentario tiene análisis completo de IA"""
        return (
            self.es_valido() and
            len(self.emociones) > 0 and
            len(self.temas) > 0 and
            bool(self.resumen_ia.strip())
        )
    
    # === Métodos de consulta de sentimiento ===
    
    def es_positivo(self) -> bool:
        """Verifica si el sentimiento es positivo"""
        return self.sentimiento.es_positivo()
    
    def es_negativo(self) -> bool:
        """Verifica si el sentimiento es negativo"""
        return self.sentimiento.es_negativo()
    
    def es_neutral(self) -> bool:
        """Verifica si el sentimiento es neutral"""
        return self.sentimiento.es_neutral()
    
    # === Métodos de consulta de emociones ===
    
    def obtener_emociones_intensas(self, umbral: float = 0.7) -> List[Emocion]:
        """Obtiene emociones con alta intensidad"""
        return [e for e in self.emociones if e.es_intensa(umbral)]
    
    def obtener_emociones_positivas(self) -> List[Emocion]:
        """Obtiene todas las emociones positivas detectadas"""
        return [e for e in self.emociones if e.es_positiva()]
    
    def obtener_emociones_negativas(self) -> List[Emocion]:
        """Obtiene todas las emociones negativas detectadas"""
        return [e for e in self.emociones if e.es_negativa()]
    
    def tiene_emociones_conflictivas(self) -> bool:
        """Detecta si hay emociones positivas y negativas simultáneamente"""
        return (len(self.obtener_emociones_positivas()) > 0 and 
                len(self.obtener_emociones_negativas()) > 0)
    
    # === Métodos de consulta de temas ===
    
    def obtener_temas_muy_relevantes(self, umbral: float = 0.7) -> List[TemaPrincipal]:
        """Obtiene temas con alta relevancia"""
        return [t for t in self.temas if t.es_muy_relevante(umbral)]
    
    def obtener_temas_tecnicos(self) -> List[TemaPrincipal]:
        """Obtiene todos los temas técnicos"""
        return [t for t in self.temas if t.es_tecnico()]
    
    def obtener_temas_comerciales(self) -> List[TemaPrincipal]:
        """Obtiene todos los temas comerciales"""
        return [t for t in self.temas if t.es_comercial()]
    
    def obtener_temas_servicio_cliente(self) -> List[TemaPrincipal]:
        """Obtiene temas relacionados con servicio al cliente"""
        return [t for t in self.temas if t.es_servicio_cliente()]
    
    # === Métodos de consulta de puntos de dolor ===
    
    def obtener_dolores_criticos(self) -> List[PuntoDolor]:
        """Obtiene puntos de dolor críticos"""
        return [p for p in self.puntos_dolor if p.es_critico()]
    
    def obtener_dolores_tecnicos(self) -> List[PuntoDolor]:
        """Obtiene problemas técnicos"""
        return [p for p in self.puntos_dolor if p.es_tecnico()]
    
    def obtener_dolores_servicio_cliente(self) -> List[PuntoDolor]:
        """Obtiene problemas de atención al cliente"""
        return [p for p in self.puntos_dolor if p.es_servicio_cliente()]
    
    def calcular_severidad_promedio_dolores(self) -> float:
        """Calcula la severidad promedio de todos los puntos de dolor"""
        if not self.puntos_dolor:
            return 0.0
        return sum(p.severidad for p in self.puntos_dolor) / len(self.puntos_dolor)
    
    # === Métodos de criticidad ===
    
    def es_critico(self) -> bool:
        """
        Determina si el comentario requiere atención crítica
        Basado en: sentimiento muy negativo OR puntos de dolor críticos
        """
        return (
            self.sentimiento.es_muy_negativo() or
            len(self.obtener_dolores_criticos()) > 0 or
            len(self.obtener_emociones_intensas(0.8)) > 0
        )
    
    def requiere_atencion_inmediata(self) -> bool:
        """
        Determina si requiere atención inmediata
        (más estricto que crítico)
        """
        return (
            self.es_critico() and
            self.confianza_general >= 0.7 and
            (len(self.obtener_dolores_tecnicos()) > 0 or 
             len(self.obtener_dolores_servicio_cliente()) > 0)
        )
    
    def calcular_prioridad(self) -> float:
        """
        Calcula prioridad del comentario (0.0-1.0)
        Basado en severidad, emociones intensas y confianza
        """
        base_prioridad = 0.0
        
        # Factor sentimiento
        if self.sentimiento.es_muy_negativo():
            base_prioridad += 0.4
        elif self.sentimiento.es_negativo():
            base_prioridad += 0.2
        
        # Factor emociones intensas
        emociones_intensas = len(self.obtener_emociones_intensas())
        if emociones_intensas > 0:
            base_prioridad += min(0.3, emociones_intensas * 0.1)
        
        # Factor puntos de dolor
        severidad_promedio = self.calcular_severidad_promedio_dolores()
        base_prioridad += severidad_promedio * 0.3
        
        # Aplicar confianza
        prioridad_final = base_prioridad * self.confianza_general
        
        return min(1.0, prioridad_final)
    
    # === Métodos de análisis estadístico ===
    
    def obtener_valencia_emocional(self) -> float:
        """
        Calcula valencia emocional combinada (-1.0 a 1.0)
        Combina sentimiento categórico con intensidades emocionales
        """
        # Base del sentimiento categórico
        valencia_base = self.sentimiento.obtener_valencia_numerica()
        
        if not self.emociones:
            return valencia_base
        
        # Ajustar con emociones granulares
        valencia_emociones = 0.0
        peso_total = 0.0
        
        for emocion in self.emociones:
            peso = emocion.intensidad * emocion.confianza
            if emocion.es_positiva():
                valencia_emociones += peso
            elif emocion.es_negativa():
                valencia_emociones -= peso
            # emociones neutras no afectan valencia
            peso_total += peso
        
        if peso_total == 0:
            return valencia_base
        
        valencia_emociones = valencia_emociones / peso_total
        
        # Combinar valencia base (70%) con emociones (30%)
        return (valencia_base * 0.7) + (valencia_emociones * 0.3)
    
    # === Métodos de serialización ===
    
    def to_dict(self) -> dict:
        """Convierte el análisis completo a diccionario"""
        return {
            'id': self.id,
            'indice_original': self.indice_original,
            'texto_original': self.texto_original,
            
            'analisis_categorico': {
                'sentimiento': self.sentimiento.to_dict() if self.sentimiento else None,
                'valencia_emocional': self.obtener_valencia_emocional()
            },
            
            'analisis_granular': {
                'emociones': [e.to_dict() for e in self.emociones],
                'temas': [t.to_dict() for t in self.temas],
                'puntos_dolor': [p.to_dict() for p in self.puntos_dolor]
            },
            
            'analisis_narrativo': {
                'resumen_ia': self.resumen_ia,
                'recomendaciones': self.recomendaciones
            },
            
            'metricas': {
                'es_critico': self.es_critico(),
                'requiere_atencion_inmediata': self.requiere_atencion_inmediata(),
                'prioridad': round(self.calcular_prioridad(), 3),
                'confianza_general': round(self.confianza_general, 3),
                'severidad_promedio_dolores': round(self.calcular_severidad_promedio_dolores(), 3)
            },
            
            'metadatos': {
                'fecha_analisis': self.fecha_analisis.isoformat(),
                'modelo_ia_utilizado': self.modelo_ia_utilizado,
                'tiempo_analisis_ms': self.tiempo_analisis_ms,
                'calificacion_nps': self.calificacion_nps,
                'calificacion_nota': self.calificacion_nota
            }
        }
    
    def obtener_resumen_ejecutivo(self) -> str:
        """Genera un resumen ejecutivo del análisis"""
        criticidad = "🚨 CRÍTICO" if self.es_critico() else "ℹ️ Normal"
        valencia = self.obtener_valencia_emocional()
        valencia_desc = "muy positiva" if valencia > 0.5 else "muy negativa" if valencia < -0.5 else "neutral"
        
        return f"""
{criticidad} - {self.sentimiento.categoria.value.upper()}
Valencia emocional: {valencia_desc} ({valencia:+.2f})
Emociones detectadas: {len(self.emociones)} | Temas: {len(self.temas)} | Dolores: {len(self.puntos_dolor)}
Prioridad: {self.calcular_prioridad():.1%} | Confianza: {self.confianza_general:.1%}
        """.strip()
    
    def __str__(self) -> str:
        return f"AnalisisComentario(id={self.id}, {self.sentimiento}, criticidad={self.es_critico()})"