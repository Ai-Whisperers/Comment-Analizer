"""
DTO para el resultado completo del análisis de IA
"""
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from datetime import datetime


@dataclass
class AnalisisCompletoIA:
    """
    DTO que encapsula el resultado completo del análisis maestro de IA
    
    Este es el resultado directo de la llamada única a OpenAI
    que reemplaza múltiples análisis fragmentados.
    """
    # Análisis general del lote
    total_comentarios: int
    tendencia_general: str           # "positiva", "neutral", "negativa"
    resumen_ejecutivo: str          # análisis narrativo de la IA
    recomendaciones_principales: List[str]  # sugerencias de acción
    
    # Análisis individuales por comentario
    comentarios_analizados: List[Dict[str, Any]]
    
    # Metadatos del análisis
    confianza_general: float        # confianza promedio del análisis
    tiempo_analisis: float          # tiempo que tomó el análisis
    tokens_utilizados: int          # tokens consumidos en la API
    modelo_utilizado: str          # modelo de IA utilizado
    fecha_analisis: datetime
    
    # Estadísticas agregadas calculadas por IA
    distribucion_sentimientos: Dict[str, int]  # conteos por categoría
    temas_mas_relevantes: Dict[str, float]     # temas con relevancia promedio
    dolores_mas_severos: Dict[str, float]      # puntos de dolor con severidad promedio
    emociones_predominantes: Dict[str, float]  # emociones con intensidad promedio
    
    def es_exitoso(self) -> bool:
        """Verifica si el análisis fue exitoso"""
        # CRITICAL FIX: Import constants to eliminate hardcoding
        try:
            from ...infrastructure.external_services.ai_engine_constants import AIEngineConstants
            umbral_confianza = AIEngineConstants.MIN_CONFIDENCE_THRESHOLD
        except ImportError:
            # Fallback for backwards compatibility
            umbral_confianza = 0.5
        
        # CRITICAL FIX: Use >= instead of > for correct threshold validation
        return (self.comentarios_analizados and 
                len(self.comentarios_analizados) == self.total_comentarios and
                self.confianza_general >= umbral_confianza)
    
    def obtener_comentario_analizado(self, indice: int) -> Optional[Dict[str, Any]]:
        """Obtiene el análisis de un comentario específico por índice"""
        if 0 <= indice < len(self.comentarios_analizados):
            return self.comentarios_analizados[indice]
        return None
    
    def obtener_comentarios_criticos(self) -> List[Dict[str, Any]]:
        """Obtiene comentarios que requieren atención crítica"""
        criticos = []
        for comentario in self.comentarios_analizados:
            # Verificar si tiene sentimiento muy negativo o puntos de dolor severos
            sentimiento = comentario.get('sentimiento', {})
            puntos_dolor = comentario.get('puntos_dolor', [])
            
            es_muy_negativo = (sentimiento.get('categoria') == 'negativo' and 
                             sentimiento.get('confianza', 0) >= 0.8)
            
            tiene_dolor_severo = any(dolor.get('severidad', 0) >= 0.7 for dolor in puntos_dolor)
            
            if es_muy_negativo or tiene_dolor_severo:
                criticos.append(comentario)
        
        return criticos
    
    def calcular_nps_estimado(self) -> int:
        """
        Calcula un NPS estimado basado en la distribución de sentimientos
        Retorna valor entre -100 y 100
        """
        positivos = self.distribucion_sentimientos.get('positivo', 0)
        neutrales = self.distribucion_sentimientos.get('neutral', 0) 
        negativos = self.distribucion_sentimientos.get('negativo', 0)
        
        if self.total_comentarios == 0:
            return 0
        
        # NPS = % Promotores - % Detractores
        # Consideramos positivos como promotores, negativos como detractores
        pct_promotores = (positivos / self.total_comentarios) * 100
        pct_detractores = (negativos / self.total_comentarios) * 100
        
        return int(pct_promotores - pct_detractores)
    
    def obtener_resumen_ejecutivo_completo(self) -> str:
        """Obtiene un resumen completo del análisis"""
        nps_estimado = self.calcular_nps_estimado()
        criticos = len(self.obtener_comentarios_criticos())
        
        return f"""
{self.resumen_ejecutivo}

MÉTRICAS CLAVE:
📊 Comentarios analizados: {self.total_comentarios}
📈 Tendencia general: {self.tendencia_general}
🎯 NPS estimado: {nps_estimado}
🚨 Comentarios críticos: {criticos}
⚡ Confianza general: {self.confianza_general:.1%}

DISTRIBUCIÓN SENTIMIENTOS:
• Positivos: {self.distribucion_sentimientos.get('positivo', 0)}
• Neutrales: {self.distribucion_sentimientos.get('neutral', 0)}  
• Negativos: {self.distribucion_sentimientos.get('negativo', 0)}
        """.strip()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el análisis completo a diccionario"""
        return {
            'analisis_general': {
                'total_comentarios': self.total_comentarios,
                'tendencia_general': self.tendencia_general,
                'resumen_ejecutivo': self.resumen_ejecutivo,
                'recomendaciones_principales': self.recomendaciones_principales,
                'confianza_general': self.confianza_general,
                'nps_estimado': self.calcular_nps_estimado()
            },
            'comentarios': self.comentarios_analizados,
            'estadisticas': {
                'distribucion_sentimientos': self.distribucion_sentimientos,
                'temas_mas_relevantes': self.temas_mas_relevantes,
                'dolores_mas_severos': self.dolores_mas_severos,
                'emociones_predominantes': self.emociones_predominantes
            },
            'metadatos': {
                'tiempo_analisis': self.tiempo_analisis,
                'tokens_utilizados': self.tokens_utilizados,
                'modelo_utilizado': self.modelo_utilizado,
                'fecha_analisis': self.fecha_analisis.isoformat(),
                'comentarios_criticos': len(self.obtener_comentarios_criticos())
            }
        }