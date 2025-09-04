"""
Implementación del analizador de sentimientos usando OpenAI
"""
import openai
import json
import time
from typing import List, Optional
import logging

from ...domain.services.analizador_sentimientos import IAnalizadorSentimientos
from ...domain.value_objects.sentimiento import Sentimiento
from ...shared.exceptions.ia_exception import IAException


logger = logging.getLogger(__name__)


class AnalizadorOpenAI(IAnalizadorSentimientos):
    """
    Implementación del analizador de sentimientos usando la API de OpenAI
    """
    
    def __init__(self, api_key: str, modelo: str = "gpt-4", usar_cache: bool = True):
        self.client = openai.OpenAI(api_key=api_key)
        self.modelo = modelo
        self.usar_cache = usar_cache
        self._cache = {} if usar_cache else None
        self.disponible = self._verificar_disponibilidad()
    
    def analizar_sentimiento(self, texto: str) -> Sentimiento:
        """
        Analiza el sentimiento de un texto individual
        """
        if not self.disponible:
            raise IAException("El analizador OpenAI no está disponible")
        
        # Verificar cache
        if self.usar_cache and texto in self._cache:
            return self._cache[texto]
        
        try:
            resultado = self._hacer_llamada_api([texto])
            if resultado:
                sentimiento = self._parsear_resultado_sentimiento(resultado[0])
                
                # Guardar en cache
                if self.usar_cache:
                    self._cache[texto] = sentimiento
                
                return sentimiento
            else:
                raise IAException("No se recibió resultado de la API")
                
        except Exception as e:
            logger.error(f"Error analizando sentimiento: {str(e)}")
            raise IAException(f"Error en análisis: {str(e)}")
    
    def analizar_lote(self, textos: List[str]) -> List[Sentimiento]:
        """
        Analiza el sentimiento de múltiples textos de manera eficiente
        """
        if not self.disponible:
            raise IAException("El analizador OpenAI no está disponible")
        
        if not textos:
            return []
        
        sentimientos = []
        textos_pendientes = []
        indices_pendientes = []
        
        # Verificar cache para cada texto
        for i, texto in enumerate(textos):
            if self.usar_cache and texto in self._cache:
                sentimientos.append(self._cache[texto])
            else:
                sentimientos.append(None)  # Placeholder
                textos_pendientes.append(texto)
                indices_pendientes.append(i)
        
        # Procesar textos no cacheados
        if textos_pendientes:
            try:
                resultados = self._hacer_llamada_api_lote(textos_pendientes)
                
                for i, resultado in enumerate(resultados):
                    sentimiento = self._parsear_resultado_sentimiento(resultado)
                    indice_original = indices_pendientes[i]
                    texto_original = textos_pendientes[i]
                    
                    sentimientos[indice_original] = sentimiento
                    
                    # Guardar en cache
                    if self.usar_cache:
                        self._cache[texto_original] = sentimiento
                        
            except Exception as e:
                logger.error(f"Error en análisis por lotes: {str(e)}")
                # Fallback: llenar con sentimientos neutrales
                for i in indices_pendientes:
                    if sentimientos[i] is None:
                        sentimientos[i] = Sentimiento.crear_neutral(0.3, "openai_error")
        
        return sentimientos
    
    def es_disponible(self) -> bool:
        """
        Verifica si el analizador está disponible
        """
        return self.disponible
    
    def _verificar_disponibilidad(self) -> bool:
        """
        Verifica la disponibilidad de la API
        """
        try:
            # Hacer una llamada de prueba simple
            response = self.client.chat.completions.create(
                model=self.modelo,
                messages=[{"role": "user", "content": "test"}],
                max_tokens=5
            )
            return True
        except Exception as e:
            logger.warning(f"OpenAI no disponible: {str(e)}")
            return False
    
    def _hacer_llamada_api(self, textos: List[str]) -> List[dict]:
        """
        Hace una llamada a la API para analizar textos
        """
        prompt = self._generar_prompt(textos)
        
        try:
            response = self.client.chat.completions.create(
                model=self.modelo,
                messages=[
                    {"role": "system", "content": "Eres un experto analizador de sentimientos para comentarios de clientes de telecomunicaciones en español."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.3
            )
            
            content = response.choices[0].message.content
            return self._parsear_respuesta_api(content)
            
        except Exception as e:
            logger.error(f"Error en llamada API: {str(e)}")
            raise IAException(f"Error comunicándose con OpenAI: {str(e)}")
    
    def _hacer_llamada_api_lote(self, textos: List[str]) -> List[dict]:
        """
        Procesa múltiples textos en lotes para optimizar llamadas API
        """
        TAMAÑO_LOTE = 20  # Procesar de a 20 comentarios
        todos_los_resultados = []
        
        for i in range(0, len(textos), TAMAÑO_LOTE):
            lote = textos[i:i+TAMAÑO_LOTE]
            resultados_lote = self._hacer_llamada_api(lote)
            todos_los_resultados.extend(resultados_lote)
            
            # Pausa entre lotes para evitar rate limiting
            if i + TAMAÑO_LOTE < len(textos):
                time.sleep(1)
        
        return todos_los_resultados
    
    def _generar_prompt(self, textos: List[str]) -> str:
        """
        Genera el prompt para la API
        """
        textos_numerados = '\n'.join([f"{i+1}. {texto}" for i, texto in enumerate(textos)])
        
        return f"""
Analiza el sentimiento de estos comentarios de clientes de telecomunicaciones y responde en formato JSON válido:

{textos_numerados}

Para cada comentario, proporciona:
- sentiment: "positive", "negative", o "neutral"
- confidence: número entre 0.0 y 1.0
- themes: lista de temas principales (máximo 5)
- pain_points: lista de puntos de dolor mencionados
- emotions: lista de emociones detectadas

Formato de respuesta (JSON array):
[
  {{
    "sentiment": "positive",
    "confidence": 0.85,
    "themes": ["velocidad", "servicio"],
    "pain_points": [],
    "emotions": ["satisfacción"]
  }}
]
"""
    
    def _parsear_respuesta_api(self, content: str) -> List[dict]:
        """
        Parsea la respuesta JSON de la API
        """
        try:
            # Limpiar la respuesta
            content = content.strip()
            if content.startswith('```json'):
                content = content[7:]
            if content.endswith('```'):
                content = content[:-3]
            
            # Parsear JSON
            resultados = json.loads(content)
            
            if isinstance(resultados, list):
                return resultados
            else:
                return [resultados]
                
        except json.JSONDecodeError as e:
            logger.error(f"Error parseando JSON: {str(e)}, Content: {content}")
            raise IAException(f"Respuesta inválida de la API: {str(e)}")
    
    def _parsear_resultado_sentimiento(self, resultado: dict) -> Sentimiento:
        """
        Convierte el resultado de la API en un objeto Sentimiento
        """
        try:
            sentiment_str = resultado.get('sentiment', 'neutral').lower()
            confidence = float(resultado.get('confidence', 0.5))
            
            if sentiment_str == 'positive':
                return Sentimiento.crear_positivo(confidence, "openai")
            elif sentiment_str == 'negative':
                return Sentimiento.crear_negativo(confidence, "openai")
            else:
                return Sentimiento.crear_neutral(confidence, "openai")
                
        except (ValueError, KeyError) as e:
            logger.warning(f"Error parseando resultado: {str(e)}")
            return Sentimiento.crear_neutral(0.3, "openai_error")