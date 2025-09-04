"""
Analizador maestro que hace análisis completo con una sola llamada a IA
"""
import openai
import json
import time
from typing import List, Dict, Any
from datetime import datetime
import logging

from ...application.dtos.analisis_completo_ia import AnalisisCompletoIA
from ...shared.exceptions.ia_exception import IAException


logger = logging.getLogger(__name__)


class AnalizadorMaestroIA:
    """
    Analizador maestro que reemplaza múltiples analizadores fragmentados
    
    Hace UNA sola llamada comprensiva a OpenAI que analiza:
    - Sentimientos categóricos (determinista)
    - Emociones granulares (con intensidades variables)
    - Temas principales (con relevancia variable) 
    - Puntos de dolor (con severidad variable)
    - Análisis narrativo completo (variable - como ChatGPT real)
    """
    
    def __init__(self, api_key: str, modelo: str = "gpt-4", usar_cache: bool = True):
        self.client = openai.OpenAI(api_key=api_key)
        self.modelo = modelo
        self.usar_cache = usar_cache
        self._cache = {} if usar_cache else None
        self.disponible = self._verificar_disponibilidad()
        
        # Configuración determinista 
        self.temperatura = 0.0    # ← DETERMINISTA para consistencia
        self.seed = 12345         # ← Seed fijo para máxima reproducibilidad
        
        logger.info(f"🤖 AnalizadorMaestroIA inicializado - Modelo: {modelo}, Determinista: temp={self.temperatura}, seed={self.seed}")
    
    def analizar_excel_completo(self, comentarios_raw: List[str]) -> AnalisisCompletoIA:
        """
        Análisis maestro: UNA sola llamada que reemplaza todo el pipeline fragmentado
        
        Args:
            comentarios_raw: Lista de comentarios como strings
            
        Returns:
            AnalisisCompletoIA con el resultado completo
        """
        if not self.disponible:
            raise IAException("El analizador maestro IA no está disponible")
        
        if not comentarios_raw:
            raise IAException("No hay comentarios para analizar")
        
        inicio_tiempo = time.time()
        logger.info(f"🔍 Iniciando análisis maestro de {len(comentarios_raw)} comentarios")
        
        try:
            # Generar hash para cache (determinista por contenido)
            cache_key = self._generar_cache_key(comentarios_raw)
            
            # Verificar cache
            if self.usar_cache and cache_key in self._cache:
                logger.info("💾 Resultado obtenido desde cache")
                return self._cache[cache_key]
            
            # Generar prompt maestro
            prompt_completo = self._generar_prompt_maestro(comentarios_raw)
            
            # Hacer llamada única a OpenAI
            respuesta_raw = self._hacer_llamada_api_maestra(prompt_completo)
            
            # Procesar respuesta y crear DTO
            tiempo_transcurrido = time.time() - inicio_tiempo
            analisis_completo = self._procesar_respuesta_maestra(
                respuesta_raw, comentarios_raw, tiempo_transcurrido
            )
            
            # Guardar en cache
            if self.usar_cache:
                self._cache[cache_key] = analisis_completo
            
            logger.info(f"✅ Análisis maestro completado en {tiempo_transcurrido:.2f}s")
            return analisis_completo
            
        except Exception as e:
            logger.error(f"❌ Error en análisis maestro: {str(e)}")
            raise IAException(f"Error en análisis maestro: {str(e)}")
    
    def _generar_prompt_maestro(self, comentarios: List[str]) -> str:
        """
        Genera el prompt maestro que solicita análisis completo de una sola vez
        """
        comentarios_numerados = '\n'.join([
            f"{i+1}. {comentario[:500]}..." if len(comentario) > 500 else f"{i+1}. {comentario}"
            for i, comentario in enumerate(comentarios)
        ])
        
        return f"""
Eres un experto analista de experiencia del cliente en telecomunicaciones. Analiza estos {len(comentarios)} comentarios y proporciona un análisis completo y estructurado.

COMENTARIOS A ANALIZAR:
{comentarios_numerados}

RESPUESTA REQUERIDA (JSON estricto):
{{
  "analisis_general": {{
    "total_comentarios": {len(comentarios)},
    "tendencia_general": "positiva|neutral|negativa",
    "resumen_ejecutivo": "Tu análisis narrativo completo de las tendencias, patrones y insights principales",
    "recomendaciones_principales": [
      "Recomendación específica 1",
      "Recomendación específica 2", 
      "Recomendación específica 3"
    ]
  }},
  "comentarios": [
    {{
      "indice": 0,
      "sentimiento": {{
        "categoria": "positivo|neutral|negativo",
        "confianza": 0.85
      }},
      "emociones": [
        {{
          "tipo": "satisfaccion|frustracion|enojo|alegria|decepcion|preocupacion|etc",
          "intensidad": 0.7,
          "confianza": 0.8,
          "contexto": "parte específica del comentario donde se detecta"
        }}
      ],
      "temas": [
        {{
          "categoria": "velocidad|precio|servicio_cliente|cobertura|etc",
          "relevancia": 0.9,
          "confianza": 0.8,
          "contexto_especifico": "parte del comentario relevante"
        }}
      ],
      "puntos_dolor": [
        {{
          "tipo": "velocidad_lenta|cobros_incorrectos|mal_servicio_cliente|etc",
          "severidad": 0.8,
          "confianza": 0.9,
          "nivel_impacto": "critico|alto|moderado|bajo",
          "contexto_especifico": "descripción específica del problema"
        }}
      ],
      "resumen": "Análisis específico de este comentario individual"
    }}
  ],
  "estadisticas_agregadas": {{
    "distribucion_sentimientos": {{"positivo": 0, "neutral": 0, "negativo": 0}},
    "temas_mas_relevantes": {{"velocidad": 0.8, "precio": 0.6}},
    "dolores_mas_severos": {{"velocidad_lenta": 0.7, "cobros_incorrectos": 0.5}},
    "emociones_predominantes": {{"frustracion": 0.6, "satisfaccion": 0.4}}
  }}
}}

INSTRUCCIONES CRÍTICAS:
1. CONSISTENCIA: sentimiento.confianza debe ser consistente para textos similares
2. VARIABILIDAD CONTROLADA: emociones.intensidad, temas.relevancia, puntos_dolor.severidad PUEDEN variar para expresar matices
3. NARRATIVA NATURAL: resumen_ejecutivo y recomendaciones deben ser naturales y únicos
4. JSON VÁLIDO: Respuesta debe ser JSON válido sin texto adicional
5. TODOS LOS COMENTARIOS: Incluir análisis de todos los {len(comentarios)} comentarios en el array
6. TELECOMUNICACIONES: Enfocarse en temas específicos del sector (velocidad, cobertura, planes, servicio técnico, etc.)
"""
    
    def _hacer_llamada_api_maestra(self, prompt: str) -> Dict[str, Any]:
        """
        Hace la llamada única y comprensiva a OpenAI con configuración determinista
        """
        try:
            logger.debug(f"🚀 Enviando prompt maestro (temp={self.temperatura}, seed={self.seed})")
            
            response = self.client.chat.completions.create(
                model=self.modelo,
                messages=[
                    {
                        "role": "system", 
                        "content": "Eres un experto analista de experiencia del cliente especializado en telecomunicaciones. Responde SOLO con JSON válido, sin texto adicional."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=self.temperatura,  # ← DETERMINISTA
                seed=self.seed,                # ← REPRODUCIBLE
                max_tokens=4000,
                response_format={"type": "json_object"}  # ← Forzar JSON válido
            )
            
            content = response.choices[0].message.content
            tokens_utilizados = response.usage.total_tokens if response.usage else 0
            
            logger.debug(f"📊 Tokens utilizados: {tokens_utilizados}")
            
            # Parsear JSON de respuesta
            resultado = json.loads(content)
            resultado['_tokens_utilizados'] = tokens_utilizados
            resultado['_modelo_utilizado'] = self.modelo
            
            return resultado
            
        except json.JSONDecodeError as e:
            logger.error(f"❌ Error parseando JSON: {str(e)}")
            logger.error(f"Contenido recibido: {content[:500]}...")
            raise IAException(f"Respuesta JSON inválida de OpenAI: {str(e)}")
            
        except Exception as e:
            logger.error(f"❌ Error en llamada API: {str(e)}")
            raise IAException(f"Error comunicándose con OpenAI: {str(e)}")
    
    def _procesar_respuesta_maestra(self, respuesta: Dict[str, Any], 
                                   comentarios_originales: List[str], 
                                   tiempo_analisis: float) -> AnalisisCompletoIA:
        """
        Procesa la respuesta JSON de OpenAI y crea el DTO estructurado
        """
        try:
            analisis_general = respuesta.get('analisis_general', {})
            comentarios_analizados = respuesta.get('comentarios', [])
            estadisticas = respuesta.get('estadisticas_agregadas', {})
            
            # Validar que tenemos todos los comentarios
            if len(comentarios_analizados) != len(comentarios_originales):
                logger.warning(f"⚠️ Discrepancia: esperados {len(comentarios_originales)}, recibidos {len(comentarios_analizados)}")
            
            # Calcular confianza general
            confianzas_sentimientos = [
                c.get('sentimiento', {}).get('confianza', 0.5) 
                for c in comentarios_analizados
            ]
            confianza_general = sum(confianzas_sentimientos) / len(confianzas_sentimientos) if confianzas_sentimientos else 0.5
            
            return AnalisisCompletoIA(
                # Análisis general
                total_comentarios=analisis_general.get('total_comentarios', len(comentarios_originales)),
                tendencia_general=analisis_general.get('tendencia_general', 'neutral'),
                resumen_ejecutivo=analisis_general.get('resumen_ejecutivo', ''),
                recomendaciones_principales=analisis_general.get('recomendaciones_principales', []),
                
                # Análisis individuales
                comentarios_analizados=comentarios_analizados,
                
                # Metadatos
                confianza_general=confianza_general,
                tiempo_analisis=tiempo_analisis,
                tokens_utilizados=respuesta.get('_tokens_utilizados', 0),
                modelo_utilizado=respuesta.get('_modelo_utilizado', self.modelo),
                fecha_analisis=datetime.now(),
                
                # Estadísticas agregadas
                distribucion_sentimientos=estadisticas.get('distribucion_sentimientos', {}),
                temas_mas_relevantes=estadisticas.get('temas_mas_relevantes', {}),
                dolores_mas_severos=estadisticas.get('dolores_mas_severos', {}),
                emociones_predominantes=estadisticas.get('emociones_predominantes', {})
            )
            
        except Exception as e:
            logger.error(f"❌ Error procesando respuesta: {str(e)}")
            raise IAException(f"Error procesando respuesta de IA: {str(e)}")
    
    def _generar_cache_key(self, comentarios: List[str]) -> str:
        """Genera clave de cache determinista basada en el contenido"""
        import hashlib
        
        # Crear hash de todos los comentarios concatenados
        contenido_completo = "|".join(sorted(comentarios))  # Sort para determinismo
        hash_contenido = hashlib.md5(contenido_completo.encode()).hexdigest()
        
        # Incluir configuración en la clave
        config_key = f"{self.modelo}_{self.temperatura}_{self.seed}"
        return f"{config_key}_{hash_contenido}"
    
    def _verificar_disponibilidad(self) -> bool:
        """Verifica la disponibilidad de la API"""
        try:
            response = self.client.chat.completions.create(
                model=self.modelo,
                messages=[{"role": "user", "content": "test"}],
                max_tokens=5,
                temperature=0.0
            )
            logger.info("✅ API OpenAI disponible")
            return True
        except Exception as e:
            logger.warning(f"⚠️ OpenAI no disponible: {str(e)}")
            return False
    
    def es_disponible(self) -> bool:
        """Verifica si el analizador está disponible"""
        return self.disponible
    
    def limpiar_cache(self) -> None:
        """Limpia el cache de análisis"""
        if self._cache:
            self._cache.clear()
            logger.info("🧹 Cache de analizador maestro limpiado")
    
    def obtener_estadisticas_cache(self) -> Dict[str, Any]:
        """Obtiene estadísticas del cache"""
        if not self._cache:
            return {"cache_habilitado": False}
        
        return {
            "cache_habilitado": True,
            "entradas_cache": len(self._cache),
            "temperatura": self.temperatura,
            "seed": self.seed,
            "modelo": self.modelo
        }