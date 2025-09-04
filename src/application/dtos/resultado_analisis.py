"""
DTO para resultado de análisis
"""
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from datetime import datetime
from ...domain.entities.comentario import Comentario


@dataclass
class ResultadoAnalisis:
    """
    DTO que encapsula el resultado completo de un análisis de comentarios
    """
    exito: bool
    mensaje: str
    total_comentarios: int
    estadisticas_sentimientos: Dict[str, Any]
    comentarios_criticos: int
    temas_principales: Dict[str, int]
    comentarios_alta_calidad: int
    fecha_analisis: datetime
    nombre_archivo: Optional[str] = None
    metodos_utilizados: Optional[Dict[str, Any]] = None
    comentarios: Optional[List[Comentario]] = None
    
    def obtener_resumen(self) -> str:
        """
        Obtiene un resumen textual del análisis
        """
        if not self.exito:
            return f"❌ Error: {self.mensaje}"
        
        resumen = f"""
✅ Análisis completado exitosamente
📊 Total comentarios: {self.total_comentarios}
📈 Sentimientos: {self.estadisticas_sentimientos.get('positivos', 0)} positivos, {self.estadisticas_sentimientos.get('negativos', 0)} negativos
🚨 Comentarios críticos: {self.comentarios_criticos}
⭐ Alta calidad: {self.comentarios_alta_calidad}
🏷️ Temas principales: {len(self.temas_principales)}
"""
        return resumen.strip()
    
    def es_exitoso(self) -> bool:
        """Verifica si el análisis fue exitoso"""
        return self.exito
    
    def requiere_atencion_inmediata(self) -> bool:
        """Determina si hay comentarios que requieren atención inmediata"""
        return self.comentarios_criticos > 0