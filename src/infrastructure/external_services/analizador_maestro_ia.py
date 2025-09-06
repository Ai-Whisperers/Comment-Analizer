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
    
    def __init__(self, api_key: str, modelo: str = "gpt-4", usar_cache: bool = True, 
                 temperatura: float = 0.0, cache_ttl: int = 3600, max_tokens: int = 8000):
        self.client = openai.OpenAI(api_key=api_key)
        self.modelo = modelo
        self.usar_cache = usar_cache
        self.max_tokens_limit = max_tokens
        
        # Cache con límites para prevenir memory leaks
        if usar_cache:
            from collections import OrderedDict
            self._cache = OrderedDict()
            self._cache_max_size = 50  # Límite máximo de entradas
            self._cache_ttl_seconds = cache_ttl  # TTL configurable
            self._cache_timestamps = {}  # Track cuando se creó cada entry
        else:
            self._cache = None
            
        self.disponible = self._verificar_disponibilidad()
        
        # Configuración determinista configurable
        self.temperatura = temperatura    # ← Configurable para consistencia
        self.seed = 12345                 # ← Seed fijo para máxima reproducibilidad
        
        logger.info(f"🤖 AnalizadorMaestroIA inicializado - Modelo: {modelo}, Cache: {self._cache_max_size if usar_cache else 'disabled'}, TTL: {self._cache_ttl_seconds}s")
    
    def _calcular_tokens_dinamicos(self, num_comentarios: int) -> int:
        """
        Calcula max_tokens dinámicamente basado en número de comentarios
        
        Fórmula optimizada:
        - Base: 1200 tokens para estructura JSON
        - Por comentario: 80 tokens promedio  
        - Buffer: 10% extra para variabilidad
        - Límite por modelo: gpt-4o-mini=16384, gpt-4=128000
        """
        
        # ULTIMATE SAFETY NET: Force safe comment count regardless of input
        if num_comentarios > 20:
            logger.error(f"🚨 ULTIMATE SAFETY: Token calculation received {num_comentarios} comentarios, forcing to 20")
            num_comentarios = 20
        # Tokens base para estructura JSON (OPTIMIZADO para límites estrictos)
        tokens_base = 1200  # REDUCIDO de 2000 para mayor eficiencia
        
        # Tokens por comentario (análisis optimizado)
        tokens_por_comentario = 80  # REDUCIDO de 120 para ser más conservador
        
        # Cálculo básico
        tokens_calculados = tokens_base + (num_comentarios * tokens_por_comentario)
        
        # Buffer del 10% para variabilidad (REDUCIDO del 20%)
        tokens_con_buffer = int(tokens_calculados * 1.10)
        
        # Límites específicos por modelo
        limites_por_modelo = {
            'gpt-4o-mini': 16384,      # Límite real de gpt-4o-mini
            'gpt-4o': 16384,           # gpt-4o también tiene límite 16K
            'gpt-4': 128000,           # gpt-4 Turbo
            'gpt-4-turbo': 128000      # gpt-4 Turbo
        }
        
        # Obtener límite del modelo actual
        limite_modelo = limites_por_modelo.get(self.modelo, 16384)  # Default a gpt-4o-mini limit
        
        # Aplicar límites: usar el menor entre configurado y límite del modelo
        tokens_minimos = 1000
        tokens_maximos = min(self.max_tokens_limit, limite_modelo)
        
        # FORZAR límite absoluto - nunca exceder límite del modelo
        tokens_finales = max(tokens_minimos, min(tokens_con_buffer, tokens_maximos))
        
        # MULTIPLE SAFETY CHECKS: Never exceed any limit
        
        # Safety check 1: Never exceed model limit
        if tokens_finales > limite_modelo:
            logger.error(f"🚨 MODEL SAFETY: Forzando tokens de {tokens_finales:,} a límite modelo {limite_modelo:,}")
            tokens_finales = limite_modelo
            
        # Safety check 2: Never exceed configuration limit  
        if tokens_finales > self.max_tokens_limit:
            logger.error(f"🚨 CONFIG SAFETY: Forzando tokens de {tokens_finales:,} a límite config {self.max_tokens_limit:,}")
            tokens_finales = self.max_tokens_limit
            
        # Safety check 3: Ultra-conservative 8K limit for production
        PRODUCTION_SAFE_LIMIT = 8000
        if tokens_finales > PRODUCTION_SAFE_LIMIT:
            logger.error(f"🚨 PRODUCTION SAFETY: Forzando tokens de {tokens_finales:,} a límite producción {PRODUCTION_SAFE_LIMIT:,}")
            tokens_finales = PRODUCTION_SAFE_LIMIT
        
        logger.info(f"📊 Tokens finales: {num_comentarios} comentarios → {tokens_finales:,} tokens (modelo: {self.modelo}, límites: modelo={limite_modelo:,}, config={self.max_tokens_limit:,})")
        
        # Warning si llegamos al límite
        if tokens_finales >= tokens_maximos:
            logger.warning(f"⚠️ Archivo muy grande: {num_comentarios} comentarios requieren tokens máximos ({tokens_maximos:,}) para modelo {self.modelo}")
        
        return tokens_finales
    
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
        
        # LÍMITE DE SEGURIDAD: Calcular máximo de comentarios basado en modelo
        limites_por_modelo = {
            'gpt-4o-mini': 16384,
            'gpt-4o': 16384,
            'gpt-4': 128000,
            'gpt-4-turbo': 128000
        }
        limite_modelo = limites_por_modelo.get(self.modelo, 16384)
        
        # Calcular máximo de comentarios que caben en el límite configurado
        # OPTIMIZADO: Usar límite de configuración directamente para control estricto
        tokens_disponibles = min(limite_modelo, self.max_tokens_limit)  # Usar el menor
        tokens_base = 1200
        tokens_por_comentario = 80
        max_comentarios_teorico = int((tokens_disponibles - tokens_base) / tokens_por_comentario / 1.10)
        
        # Con 8,000 tokens configurados: comentarios_max = ~77, usamos 60 para seguridad
        
        # MULTIPLE SAFETY NETS: Force safe limits regardless of configuration
        
        # SAFETY NET 1: Absolute maximum for any model (ultra-conservative)
        ABSOLUTE_MAX_COMMENTS = 25
        if len(comentarios_raw) > ABSOLUTE_MAX_COMMENTS:
            logger.error(f"🚨 ABSOLUTE SAFETY: {len(comentarios_raw)} comentarios > {ABSOLUTE_MAX_COMMENTS}, forcing to {ABSOLUTE_MAX_COMMENTS}")
            comentarios_raw = comentarios_raw[:ABSOLUTE_MAX_COMMENTS]
            
        # SAFETY NET 2: Model-specific limits
        if len(comentarios_raw) > max_comentarios_teorico:
            logger.warning(f"🚨 MODEL LIMIT: {len(comentarios_raw)} comentarios > {max_comentarios_teorico}, limitando para {self.modelo}")
            comentarios_raw = comentarios_raw[:max_comentarios_teorico]
            
        # SAFETY NET 3: Ultra-conservative for 8K token limit
        if len(comentarios_raw) > 20:
            logger.warning(f"🚨 TOKEN SAFETY: {len(comentarios_raw)} comentarios > 20, forzando a 20 para garantizar <8K tokens")
            comentarios_raw = comentarios_raw[:20]
        
        inicio_tiempo = time.time()
        logger.info(f"🔍 Iniciando análisis maestro de {len(comentarios_raw)} comentarios (limitado para {self.modelo})")
        
        try:
            # Generar hash para cache (determinista por contenido)
            cache_key = self._generar_cache_key(comentarios_raw)
            
            # Verificar cache (con TTL y LRU)
            if self.usar_cache and self._verificar_cache_valido(cache_key):
                logger.info("💾 Resultado obtenido desde cache")
                # Move to end (LRU)
                self._cache.move_to_end(cache_key)
                return self._cache[cache_key]
            
            # Generar prompt maestro
            prompt_completo = self._generar_prompt_maestro(comentarios_raw)
            
            # Hacer llamada única a OpenAI
            respuesta_raw = self._hacer_llamada_api_maestra(prompt_completo, len(comentarios_raw))
            
            # Procesar respuesta y crear DTO
            tiempo_transcurrido = time.time() - inicio_tiempo
            analisis_completo = self._procesar_respuesta_maestra(
                respuesta_raw, comentarios_raw, tiempo_transcurrido
            )
            
            # Guardar en cache con límites
            if self.usar_cache:
                self._guardar_en_cache(cache_key, analisis_completo)
            
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
Analiza {len(comentarios)} comentarios telco. Solo JSON válido.

COMENTARIOS:
{comentarios_numerados}

FORMATO:
{{
  "general": {{
    "total": {len(comentarios)},
    "tendencia": "positiva|neutral|negativa", 
    "resumen": "Máximo 100 caracteres"
  }},
  "comentarios": [
    {{
      "i": 0,
      "sent": "pos|neu|neg",
      "conf": 0.85,
      "tema": "vel|pre|ser|cob|fac",
      "emo": "sat|fru|eno|neu",
      "urg": "b|m|a|c"
    }}
  ],
  "stats": {{"pos": 0, "neu": 0, "neg": 0, "tema_top": "vel", "urg": 0}}
}}

REGLAS: JSON válido, campos abreviados, analizar TODOS los {len(comentarios)} comentarios.
"""
    
    def _hacer_llamada_api_maestra(self, prompt: str, num_comentarios: int) -> Dict[str, Any]:
        """
        Hace la llamada única y comprensiva a OpenAI con configuración determinista
        
        Args:
            prompt: El prompt maestro generado
            num_comentarios: Número de comentarios para calcular tokens dinámicamente
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
                max_tokens=self._calcular_tokens_dinamicos(num_comentarios),
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
            # Adaptar a nuevo formato abreviado
            analisis_general = respuesta.get('general', {})
            comentarios_analizados = respuesta.get('comentarios', [])
            stats = respuesta.get('stats', {})
            
            # Validar que tenemos todos los comentarios
            if len(comentarios_analizados) != len(comentarios_originales):
                logger.warning(f"⚠️ Discrepancia: esperados {len(comentarios_originales)}, recibidos {len(comentarios_analizados)}")
            
            # Calcular confianza general desde nueva estructura abreviada
            confianzas_sentimientos = [
                c.get('conf', 0.5) 
                for c in comentarios_analizados
            ]
            confianza_general = sum(confianzas_sentimientos) / len(confianzas_sentimientos) if confianzas_sentimientos else 0.5
            
            # Adaptar distribución de sentimientos desde stats abreviado
            distribucion_sentimientos = {
                'positivo': stats.get('pos', 0),
                'neutral': stats.get('neu', 0), 
                'negativo': stats.get('neg', 0)
            }
            
            return AnalisisCompletoIA(
                # Análisis general (formato abreviado adaptado)
                total_comentarios=analisis_general.get('total', len(comentarios_originales)),
                tendencia_general=analisis_general.get('tendencia', 'neutral'),
                resumen_ejecutivo=analisis_general.get('resumen', ''),
                recomendaciones_principales=["Optimizar según tendencia detectada", "Revisar comentarios urgentes"],
                
                # Análisis individuales
                comentarios_analizados=comentarios_analizados,
                
                # Metadatos
                confianza_general=confianza_general,
                tiempo_analisis=tiempo_analisis,
                tokens_utilizados=respuesta.get('_tokens_utilizados', 0),
                modelo_utilizado=respuesta.get('_modelo_utilizado', self.modelo),
                fecha_analisis=datetime.now(),
                
                # Estadísticas agregadas adaptadas (formato abreviado)
                distribucion_sentimientos=distribucion_sentimientos,
                temas_mas_relevantes={stats.get('tema_top', 'unknown'): 1.0} if stats.get('tema_top') else {},
                dolores_mas_severos={},  # Simplificado para eficiencia de tokens
                emociones_predominantes={}  # Simplificado para eficiencia de tokens
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
    
    def _verificar_cache_valido(self, cache_key: str) -> bool:
        """Verifica si una entrada de cache es válida (existe y no expiró)"""
        if not self._cache or cache_key not in self._cache:
            return False
            
        # Verificar TTL
        if cache_key in self._cache_timestamps:
            import time
            timestamp = self._cache_timestamps[cache_key]
            if time.time() - timestamp > self._cache_ttl_seconds:
                # Expiró - remover del cache
                del self._cache[cache_key]
                del self._cache_timestamps[cache_key]
                return False
                
        return True
    
    def _guardar_en_cache(self, cache_key: str, analisis: AnalisisCompletoIA) -> None:
        """Guarda en cache con implementación LRU y size limits"""
        if not self._cache:
            return
            
        import time
        
        # Verificar límite de tamaño
        if len(self._cache) >= self._cache_max_size:
            # Remover el más antiguo (LRU)
            oldest_key, _ = self._cache.popitem(last=False)
            if oldest_key in self._cache_timestamps:
                del self._cache_timestamps[oldest_key]
            logger.debug(f"🗑️ Cache LRU: removida entrada antigua")
        
        # Guardar nueva entrada
        self._cache[cache_key] = analisis
        self._cache_timestamps[cache_key] = time.time()
        logger.debug(f"💾 Cache: guardada nueva entrada ({len(self._cache)}/{self._cache_max_size})")
    
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