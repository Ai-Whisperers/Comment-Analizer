"""
Analizador maestro que hace análisis completo con una sola llamada a IA
"""
import openai
import json
import time
import asyncio
from typing import List, Dict, Any
from datetime import datetime
import logging

from ...application.dtos.analisis_completo_ia import AnalisisCompletoIA
from ...shared.exceptions.ia_exception import IAException

# HIGH-004 FIX: Import retry strategy for error recovery
try:
    from .retry_strategy import DEFAULT_RETRY, OpenAIRetryWrapper
    RETRY_AVAILABLE = True
except ImportError:
    RETRY_AVAILABLE = False

# POLISH-002 FIX: Import constants to eliminate magic numbers
try:
    from .ai_engine_constants import AIEngineConstants
    CONSTANTS_AVAILABLE = True
except ImportError:
    CONSTANTS_AVAILABLE = False

# PROGRESS TRACKING: Import real-time progress tracker
try:
    from .ai_progress_tracker import create_progress_tracker, track_step, reset_progress_tracker
    PROGRESS_TRACKING_AVAILABLE = True
except ImportError:
    PROGRESS_TRACKING_AVAILABLE = False


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
                 temperatura: float = 0.0, cache_ttl: int = 3600, max_tokens: int = 8000,
                 ai_configuration=None):
        self.client = openai.OpenAI(api_key=api_key)
        self.modelo = modelo
        self.usar_cache = usar_cache
        self.max_tokens_limit = max_tokens
        
        # PHASE 2: Store centralized AI configuration if provided
        self.ai_configuration = ai_configuration
        
        # FUNCTIONAL FIX: Initialize _cache_ttl_seconds for all cases (logging needs it)
        if ai_configuration:
            self._cache_ttl_seconds = ai_configuration.cache_ttl_seconds
        elif CONSTANTS_AVAILABLE:
            self._cache_ttl_seconds = cache_ttl or AIEngineConstants.DEFAULT_CACHE_TTL
        else:
            self._cache_ttl_seconds = cache_ttl or 3600
        
        # Cache con límites para prevenir memory leaks
        if usar_cache:
            from collections import OrderedDict
            self._cache = OrderedDict()
            
            # PHASE 2: Use centralized configuration for cache size
            if ai_configuration:
                self._cache_max_size = ai_configuration.cache_max_size
            elif CONSTANTS_AVAILABLE:
                self._cache_max_size = AIEngineConstants.DEFAULT_CACHE_SIZE
            else:
                self._cache_max_size = 50  # Fallback
                
            self._cache_timestamps = {}  # Track cuando se creó cada entry
        else:
            self._cache = None
            
        self.disponible = self._verificar_disponibilidad()
        
        # PHASE 2: Use centralized configuration for deterministic settings
        if ai_configuration:
            self.temperatura = ai_configuration.temperature
            self.seed = ai_configuration.seed
        else:
            # Fallback to parameter and constants
            self.temperatura = temperatura
            if CONSTANTS_AVAILABLE:
                self.seed = AIEngineConstants.FIXED_SEED
            else:
                self.seed = 12345  # Fallback
        
        # HIGH-004 FIX: Initialize retry strategy for error recovery
        if RETRY_AVAILABLE:
            self.retry_wrapper = OpenAIRetryWrapper(DEFAULT_RETRY)
            retry_info = "enabled"
        else:
            self.retry_wrapper = None
            retry_info = "disabled"
        
        # PHASE 1 FIX: Validate deterministic configuration for intelligent retry decisions
        self._is_deterministic = self._validate_deterministic_config()
        
        logger.info(f"🤖 AnalizadorMaestroIA inicializado - Modelo: {modelo}, Cache: {self._cache_max_size if usar_cache else 'disabled'}, TTL: {self._cache_ttl_seconds}s, Retry: {retry_info}, Determinista: {self._is_deterministic}")
    
    def _calcular_tokens_dinamicos(self, num_comentarios: int) -> int:
        """
        Calcula max_tokens dinámicamente basado en número de comentarios
        
        Fórmula optimizada:
        - Base: 1200 tokens para estructura JSON
        - Por comentario: 80 tokens promedio  
        - Buffer: 10% extra para variabilidad
        - Límite por modelo: gpt-4o-mini=16384, gpt-4=128000
        """
        
        # POLISH-002 FIX: Use constants for safety limits and calculations
        if CONSTANTS_AVAILABLE:
            safety_limit = AIEngineConstants.SAFETY_COMMENT_LIMIT
            tokens_base = AIEngineConstants.BASE_TOKENS_JSON_STRUCTURE
            tokens_por_comentario = AIEngineConstants.TOKENS_PER_COMMENT
            buffer_percentage = AIEngineConstants.TOKEN_BUFFER_PERCENTAGE
        else:
            # Fallback values
            safety_limit = 20
            tokens_base = 1200
            tokens_por_comentario = 80  
            buffer_percentage = 1.10
        
        # ULTIMATE SAFETY NET: Force safe comment count regardless of input
        if num_comentarios > safety_limit:
            logger.error(f"🚨 ULTIMATE SAFETY: Token calculation received {num_comentarios} comentarios, forcing to {safety_limit}")
            num_comentarios = safety_limit
            
        # Cálculo básico con constantes
        tokens_calculados = tokens_base + (num_comentarios * tokens_por_comentario)
        
        # Buffer configurable para variabilidad
        tokens_con_buffer = int(tokens_calculados * buffer_percentage)
        
        # POLISH-002 FIX: Use constants for model limits  
        if CONSTANTS_AVAILABLE:
            limite_modelo = AIEngineConstants.get_model_token_limit(self.modelo)
        else:
            # Fallback model limits
            limites_por_modelo = {
                'gpt-4o-mini': 16384,
                'gpt-4o': 16384,
                'gpt-4': 128000,
                'gpt-4-turbo': 128000
            }
            limite_modelo = limites_por_modelo.get(self.modelo, 16384)
        
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
            
        # Safety check 3: FASE 3 OPTIMIZED - Increased production limit for better performance
        PRODUCTION_SAFE_LIMIT = 12000  # FASE 3: Increased from 8K to 12K for larger batches
        if tokens_finales > PRODUCTION_SAFE_LIMIT:
            logger.error(f"🚨 PRODUCTION SAFETY: Forzando tokens de {tokens_finales:,} a límite producción {PRODUCTION_SAFE_LIMIT:,}")
            tokens_finales = PRODUCTION_SAFE_LIMIT
        
        logger.info(f"📊 Tokens finales: {num_comentarios} comentarios → {tokens_finales:,} tokens (modelo: {self.modelo}, límites: modelo={limite_modelo:,}, config={self.max_tokens_limit:,})")
        
        # Warning si llegamos al límite
        if tokens_finales >= tokens_maximos:
            logger.warning(f"⚠️ Archivo muy grande: {num_comentarios} comentarios requieren tokens máximos ({tokens_maximos:,}) para modelo {self.modelo}")
        
        return tokens_finales
    
    def _validate_deterministic_config(self) -> bool:
        """
        PHASE 1 FIX: Validate if current configuration is deterministic
        
        Returns:
            bool: True if configuration is deterministic (temperature=0.0 and fixed seed)
        """
        try:
            is_temp_deterministic = abs(self.temperatura) < 0.001  # Temperature near 0.0
            has_fixed_seed = self.seed is not None and self.seed > 0
            
            deterministic = is_temp_deterministic and has_fixed_seed
            
            if deterministic:
                logger.info(f"🔒 Configuración determinista detectada: temp={self.temperatura}, seed={self.seed}")
                logger.info("⚠️ Reintentos producirán resultados idénticos - se aplicará skip inteligente")
            else:
                logger.info(f"🎲 Configuración no-determinista: temp={self.temperatura}, seed={self.seed}")
                
            return deterministic
            
        except Exception as e:
            logger.warning(f"⚠️ Error validando configuración determinista: {e}")
            return False
    
    def is_deterministic(self) -> bool:
        """
        Returns True if the analyzer is configured for deterministic results
        """
        return getattr(self, '_is_deterministic', False)
    
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
        
        # CRITICAL FIX: Cleanup expired cache entries to prevent memory leak
        if self.usar_cache:
            self._cleanup_expired_cache()
        
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
        
        # FASE 5 OPTIMIZATION: Adaptive safety nets based on file size and configuration
        
        # SAFETY NET 1: Adaptive maximum based on file size and token limits
        if tokens_disponibles >= 12000:  # 12K+ tokens available
            ADAPTIVE_MAX_COMMENTS = min(60, max_comentarios_teorico)  # Up to 60 for large token limits
        elif tokens_disponibles >= 8000:   # 8K+ tokens available  
            ADAPTIVE_MAX_COMMENTS = min(40, max_comentarios_teorico)  # Up to 40 for medium token limits
        else:  # Limited tokens
            ADAPTIVE_MAX_COMMENTS = min(25, max_comentarios_teorico)  # Conservative for small token limits
            
        if len(comentarios_raw) > ADAPTIVE_MAX_COMMENTS:
            logger.warning(f"🚨 ADAPTIVE SAFETY: {len(comentarios_raw)} comentarios > {ADAPTIVE_MAX_COMMENTS} (tokens={tokens_disponibles:,}), limitando")
            comentarios_raw = comentarios_raw[:ADAPTIVE_MAX_COMMENTS]
            
        # SAFETY NET 2: Model-specific limits (unchanged but more permissive due to FASE 3)
        if len(comentarios_raw) > max_comentarios_teorico:
            logger.warning(f"🚨 MODEL LIMIT: {len(comentarios_raw)} comentarios > {max_comentarios_teorico}, limitando para {self.modelo}")
            comentarios_raw = comentarios_raw[:max_comentarios_teorico]
        
        inicio_tiempo = time.time()
        
        # PROGRESS TRACKING: Initialize real-time progress tracker
        if PROGRESS_TRACKING_AVAILABLE:
            tracker = create_progress_tracker(len(comentarios_raw))
        
        logger.info(f"🔍 Iniciando análisis maestro de {len(comentarios_raw)} comentarios (limitado para {self.modelo})")
        
        try:
            # STEP 1: Cache operations (3% of total time)
            with track_step('cache_check') if PROGRESS_TRACKING_AVAILABLE else track_step('cache_check'):
                cache_key = self._generar_cache_key(comentarios_raw)
                
                # Verificar cache (con TTL y LRU)
                if self.usar_cache and self._verificar_cache_valido(cache_key):
                    logger.info("💾 Resultado obtenido desde cache")
                    # Move to end (LRU)
                    self._cache.move_to_end(cache_key)
                    return self._cache[cache_key]
            
            # STEP 2: Prompt generation (10% of total time)
            with track_step('prompt_generation') if PROGRESS_TRACKING_AVAILABLE else track_step('prompt_generation'):
                prompt_completo = self._generar_prompt_maestro(comentarios_raw)
            
            # STEP 3: OpenAI API call (75% of total time - LONGEST STEP)
            with track_step('openai_api_call') if PROGRESS_TRACKING_AVAILABLE else track_step('openai_api_call'):
                respuesta_raw = self._hacer_llamada_api_maestra(prompt_completo, len(comentarios_raw))
            
            # STEP 4: Response processing and emotion extraction (10% of total time)  
            with track_step('response_processing') if PROGRESS_TRACKING_AVAILABLE else track_step('response_processing'):
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
      "i": 1,
      "sent": "pos|neu|neg",
      "conf": 0.85,
      "tema": "vel|pre|ser|cob|fac",
      "emo": "sat|fru|eno|neu",
      "urg": "b|m|a|c"
    }}
  ],
  "stats": {{"pos": 0, "neu": 0, "neg": 0, "tema_top": "vel", "urg": 0}}
}}

REGLAS: JSON válido, campos abreviados, analizar EXACTAMENTE {len(comentarios)} comentarios (numerados 1-{len(comentarios)}). 
NO agregar comentarios extra. RETORNAR exactamente {len(comentarios)} items en array "comentarios".
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
            
            # HIGH-004 FIX: Use retry wrapper for robust API calls  
            if self.retry_wrapper:
                response = self.retry_wrapper.wrap_chat_completion(
                    client=self.client,
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
            else:
                # Fallback to direct API call without retry (maintains existing behavior)
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
            
            # BATCH FIX: Validar y corregir discrepancias de conteo
            expected_count = len(comentarios_originales)
            received_count = len(comentarios_analizados)
            
            if received_count != expected_count:
                logger.warning(f"⚠️ Discrepancia: esperados {expected_count}, recibidos {received_count}")
                
                if received_count > expected_count:
                    # AI devolvió más comentarios de los esperados - truncar al límite
                    logger.info(f"🔧 Truncando {received_count} → {expected_count} comentarios")
                    comentarios_analizados = comentarios_analizados[:expected_count]
                elif received_count < expected_count:
                    # AI devolvió menos comentarios - reportar pero continuar
                    logger.warning(f"⚠️ AI analizó solo {received_count}/{expected_count} comentarios")
                    # Continuar con los comentarios que sí fueron analizados
            
            # Calcular confianza general desde nueva estructura abreviada
            confianzas_sentimientos = [
                c.get('conf', 0.5) 
                for c in comentarios_analizados
            ]
            confianza_general = sum(confianzas_sentimientos) / len(confianzas_sentimientos) if confianzas_sentimientos else 0.5
            
            # Adaptar distribución de sentimientos desde stats abreviado
            # Ensure we use consistent field names for charts
            distribucion_sentimientos = {
                'positivo': stats.get('pos', 0),
                'neutral': stats.get('neu', 0), 
                'negativo': stats.get('neg', 0),
                # Also include abbreviated versions for direct chart access
                'pos': stats.get('pos', 0),
                'neu': stats.get('neu', 0),
                'neg': stats.get('neg', 0)
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
                emociones_predominantes=self._extract_emotions_from_comments(comentarios_analizados)
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
            self._cache_timestamps.clear()  # ✅ FIXED: Clear timestamps too
            logger.info("🧹 Cache de analizador maestro limpiado")
    
    def _cleanup_expired_cache(self) -> None:
        """
        CRITICAL FIX: Background cleanup of expired cache entries to prevent memory leak
        Addresses CRITICAL-001: Memory leak in cache timestamps dictionary
        """
        if not self._cache or not self.usar_cache:
            return
        
        import time
        current_time = time.time()
        expired_keys = []
        
        # Identify expired keys
        for key, timestamp in self._cache_timestamps.items():
            if current_time - timestamp > self._cache_ttl_seconds:
                expired_keys.append(key)
        
        # Remove expired entries from both dictionaries
        removed_count = 0
        for key in expired_keys:
            if key in self._cache:
                del self._cache[key]
                removed_count += 1
            if key in self._cache_timestamps:
                del self._cache_timestamps[key]
        
        if removed_count > 0:
            logger.info(f"🧹 Cleaned {removed_count} expired cache entries (memory leak prevention)")
        
        # Additional safety: if timestamps dict grows larger than cache, clean it
        if len(self._cache_timestamps) > len(self._cache):
            # Remove timestamps that don't have corresponding cache entries
            orphaned_keys = set(self._cache_timestamps.keys()) - set(self._cache.keys())
            for key in list(orphaned_keys):  # Convert to list to avoid dict changing during iteration
                if key in self._cache_timestamps:
                    del self._cache_timestamps[key]
            if orphaned_keys:
                logger.debug(f"🧹 Cleaned {len(orphaned_keys)} orphaned timestamp entries")
    
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
    
    def _extract_emotions_from_comments(self, comentarios_analizados: List[Dict]) -> Dict[str, float]:
        """Extract and aggregate emotions from individual comment analysis"""
        emotion_counts = {}
        
        for comentario in comentarios_analizados:
            if isinstance(comentario, dict):
                # Handle abbreviated emotion format: 'emo' field
                emo = comentario.get('emo', comentario.get('emocion_principal', 'neutral'))
                
                # Map abbreviated emotions to full names
                emotion_mapping = {
                    'sat': 'satisfaccion',
                    'fru': 'frustracion', 
                    'eno': 'enojo',
                    'neu': 'neutral',
                    'ale': 'alegria',
                    'pre': 'preocupacion',
                    'dec': 'decepcion'
                }
                
                emotion_name = emotion_mapping.get(emo, emo)
                emotion_counts[emotion_name] = emotion_counts.get(emotion_name, 0) + 1
        
        # Convert counts to intensities (normalize by total)
        total_comments = len(comentarios_analizados)
        emotion_intensities = {}
        
        for emotion, count in emotion_counts.items():
            intensity = count / total_comments if total_comments > 0 else 0
            emotion_intensities[emotion] = round(intensity, 2)
            
        return emotion_intensities
    
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
    
    async def analizar_batch_async(self, comentarios_batch: List[str]) -> AnalisisCompletoIA:
        """
        OPTIMIZATION: Async version of batch analysis for concurrent I/O
        Streamlit-safe: No threading, uses AsyncIO in main thread only
        """
        if not self.disponible:
            raise IAException("El analizador maestro IA no está disponible")
        
        if not comentarios_batch:
            raise IAException("No hay comentarios para analizar")
        
        # Create async client if not exists
        if not hasattr(self, '_async_client'):
            self._async_client = openai.AsyncOpenAI(api_key=self.api_key)
        
        try:
            num_comentarios = len(comentarios_batch)
            logger.info(f"🔍 [ASYNC] Iniciando análisis maestro de {num_comentarios} comentarios")
            
            # Prepare prompt (reuse existing logic)
            prompt = self._crear_prompt_maestro(comentarios_batch)
            
            # Async API call
            response = await self._async_client.chat.completions.create(
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
                temperature=self.temperatura,
                seed=self.seed,
                max_tokens=self._calcular_tokens_dinamicos(num_comentarios),
                response_format={"type": "json_object"}
            )
            
            # Parse response (reuse existing logic)
            return self._parsear_respuesta_maestro(response, comentarios_batch)
            
        except Exception as e:
            logger.error(f"❌ [ASYNC] Error en análisis maestro: {str(e)}")
            raise IAException(f"Error en análisis maestro async: {str(e)}")
    
    async def analizar_batches_concurrent(self, batches: List[List[str]]) -> List[AnalisisCompletoIA]:
        """
        OPTIMIZATION: Process multiple batches concurrently using AsyncIO
        Streamlit-safe: Main thread only, no custom threads
        Expected: 30-50% additional performance improvement
        """
        logger.info(f"⚡ [ASYNC] Starting concurrent I/O processing of {len(batches)} batches")
        
        # Semaphore to respect OpenAI rate limits
        semaphore = asyncio.Semaphore(3)  # Max 3 concurrent calls
        
        async def process_single_batch_with_semaphore(batch_index, batch):
            async with semaphore:
                try:
                    logger.info(f"🔄 [ASYNC] Processing batch {batch_index + 1}/{len(batches)}")
                    result = await self.analizar_batch_async(batch)
                    logger.info(f"✅ [ASYNC] Batch {batch_index + 1} completed: confidence={result.confianza_general:.2f}")
                    return ('success', batch_index + 1, result)
                except Exception as e:
                    logger.error(f"❌ [ASYNC] Batch {batch_index + 1} failed: {str(e)}")
                    return ('error', batch_index + 1, str(e))
        
        # Create tasks for all batches
        tasks = [
            process_single_batch_with_semaphore(i, batch) 
            for i, batch in enumerate(batches)
        ]
        
        # Execute concurrently and wait for all to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        successful_results = []
        failed_batches = []
        
        for result in results:
            if isinstance(result, Exception):
                logger.error(f"❌ [ASYNC] Task exception: {result}")
                failed_batches.append(result)
            else:
                status, batch_num, data = result
                if status == 'success':
                    successful_results.append(data)
                else:
                    failed_batches.append((batch_num, data))
        
        logger.info(f"📊 [ASYNC] Completed: {len(successful_results)} successful, {len(failed_batches)} failed")
        return successful_results