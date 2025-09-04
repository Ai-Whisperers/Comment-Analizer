"""
Analizador de sentimientos basado en reglas - Fallback
"""
from typing import List, Dict, Set
import re
import logging

from ...domain.services.analizador_sentimientos import IAnalizadorSentimientos
from ...domain.value_objects.sentimiento import Sentimiento


logger = logging.getLogger(__name__)


class AnalizadorReglas(IAnalizadorSentimientos):
    """
    Implementación de análisis de sentimientos basado en reglas
    Usado como fallback cuando otros métodos no están disponibles
    """
    
    def __init__(self):
        self._inicializar_diccionarios()
    
    def analizar_sentimiento(self, texto: str) -> Sentimiento:
        """
        Analiza el sentimiento usando reglas predefinidas
        """
        if not texto or not texto.strip():
            return Sentimiento.crear_neutral(0.3, "reglas")
        
        texto_limpio = self._limpiar_texto(texto)
        
        # Contar palabras positivas y negativas
        puntuacion_positiva = self._calcular_puntuacion_positiva(texto_limpio)
        puntuacion_negativa = self._calcular_puntuacion_negativa(texto_limpio)
        
        # Aplicar modificadores
        puntuacion_negativa = self._aplicar_modificadores_intensidad(texto_limpio, puntuacion_negativa)
        
        # Determinar sentimiento
        diferencia = puntuacion_positiva - puntuacion_negativa
        total_palabras = len(texto_limpio.split())
        
        # Calcular confianza basada en la cantidad de indicadores encontrados
        total_indicadores = puntuacion_positiva + puntuacion_negativa
        confianza = min(0.9, 0.3 + (total_indicadores / max(total_palabras, 1)) * 2)
        
        if diferencia > 1:
            return Sentimiento.crear_positivo(confianza, "reglas")
        elif diferencia < -1:
            return Sentimiento.crear_negativo(confianza, "reglas")
        else:
            return Sentimiento.crear_neutral(max(confianza, 0.5), "reglas")
    
    def analizar_lote(self, textos: List[str]) -> List[Sentimiento]:
        """
        Analiza múltiples textos
        """
        return [self.analizar_sentimiento(texto) for texto in textos]
    
    def es_disponible(self) -> bool:
        """
        Este analizador siempre está disponible
        """
        return True
    
    def _inicializar_diccionarios(self):
        """
        Inicializa los diccionarios de palabras para análisis en español
        """
        self.palabras_positivas = {
            'excelente', 'genial', 'perfecto', 'increíble', 'fantástico',
            'bueno', 'buena', 'buenísimo', 'maravilloso', 'espectacular',
            'satisfecho', 'contento', 'feliz', 'alegre', 'encantado',
            'recomiendo', 'recomendaría', 'mejor', 'óptimo', 'ideal',
            'rápido', 'rápida', 'eficiente', 'eficaz', 'ágil',
            'amable', 'cordial', 'atento', 'servicial', 'profesional',
            'solución', 'solucionó', 'resolvió', 'ayuda', 'apoyo',
            'gracias', 'agradezco', 'agradecer'
        }
        
        self.palabras_negativas = {
            'malo', 'mala', 'terrible', 'pésimo', 'horrible',
            'desastre', 'frustrado', 'molesto', 'enojado', 'furioso',
            'lento', 'lenta', 'demora', 'tardó', 'esperar',
            'problema', 'problemas', 'falla', 'error', 'defecto',
            'no funciona', 'no sirve', 'no anda', 'cortado', 'caído',
            'difícil', 'complicado', 'imposible', 'inútil',
            'caro', 'costoso', 'expensive', 'cobro', 'cobran',
            'cancelar', 'cancelé', 'dejar', 'cambiar', 'competencia',
            'decepcionado', 'decepción', 'insatisfecho'
        }
        
        self.modificadores_intensidad = {
            'muy': 1.5,
            'súper': 1.5,
            'extremadamente': 2.0,
            'totalmente': 1.8,
            'completamente': 1.8,
            'absolutamente': 2.0,
            'demasiado': 1.5,
            'bastante': 1.3,
            'realmente': 1.4,
            'verdaderamente': 1.5
        }
        
        self.negadores = {
            'no', 'nunca', 'jamás', 'nada', 'nadie', 'ningún', 
            'ninguna', 'sin', 'ni'
        }
    
    def _limpiar_texto(self, texto: str) -> str:
        """
        Limpia y normaliza el texto para análisis
        """
        # Convertir a minúsculas
        texto = texto.lower()
        
        # Remover puntuación pero mantener espacios
        texto = re.sub(r'[^\w\s]', ' ', texto)
        
        # Normalizar espacios
        texto = re.sub(r'\s+', ' ', texto).strip()
        
        return texto
    
    def _calcular_puntuacion_positiva(self, texto: str) -> float:
        """
        Calcula la puntuación positiva del texto
        """
        palabras = texto.split()
        puntuacion = 0.0
        
        for i, palabra in enumerate(palabras):
            if palabra in self.palabras_positivas:
                peso = 1.0
                
                # Verificar modificadores de intensidad antes de la palabra
                if i > 0 and palabras[i-1] in self.modificadores_intensidad:
                    peso *= self.modificadores_intensidad[palabras[i-1]]
                
                # Verificar negadores
                negado = self._verificar_negacion(palabras, i)
                if negado:
                    peso *= -0.8  # Convertir en negativo pero con menos peso
                
                puntuacion += peso
        
        return max(0, puntuacion)  # No permitir puntuación negativa
    
    def _calcular_puntuacion_negativa(self, texto: str) -> float:
        """
        Calcula la puntuación negativa del texto
        """
        palabras = texto.split()
        puntuacion = 0.0
        
        for i, palabra in enumerate(palabras):
            if palabra in self.palabras_negativas:
                peso = 1.0
                
                # Verificar modificadores de intensidad
                if i > 0 and palabras[i-1] in self.modificadores_intensidad:
                    peso *= self.modificadores_intensidad[palabras[i-1]]
                
                # Verificar negadores (doble negación = positivo)
                negado = self._verificar_negacion(palabras, i)
                if negado:
                    peso *= -0.5  # Reduce el impacto negativo
                
                puntuacion += peso
        
        return max(0, puntuacion)
    
    def _aplicar_modificadores_intensidad(self, texto: str, puntuacion_base: float) -> float:
        """
        Aplica modificadores adicionales basados en patrones del texto
        """
        puntuacion = puntuacion_base
        
        # Signos de exclamación intensifican
        exclamaciones = texto.count('!')
        puntuacion *= (1 + exclamaciones * 0.2)
        
        # Palabras en mayúsculas (gritos) intensifican
        palabras_mayus = len([p for p in texto.split() if p.isupper() and len(p) > 2])
        puntuacion *= (1 + palabras_mayus * 0.3)
        
        # Repetición de letras (hoooola) intensifica
        repeticiones = len(re.findall(r'(.)\1{2,}', texto))
        puntuacion *= (1 + repeticiones * 0.15)
        
        return puntuacion
    
    def _verificar_negacion(self, palabras: List[str], indice_palabra: int) -> bool:
        """
        Verifica si una palabra está siendo negada
        """
        # Buscar negadores en las 3 palabras anteriores
        inicio = max(0, indice_palabra - 3)
        for i in range(inicio, indice_palabra):
            if palabras[i] in self.negadores:
                return True
        
        return False