"""
OpenAI-based Sentiment Analysis and Language Processing Module
Handles all AI tasks including sentiment analysis, language detection, and translation using OpenAI API
with optimized batching and rate limiting
"""

import pandas as pd
import json
import logging
from typing import List, Dict, Optional, Tuple, Any
from openai import OpenAI
from src.config import Config
from src.api.cache_manager import CacheManager
from src.api.api_client import RobustAPIClient, get_global_client, get_api_monitor, timeout_handler
from src.api.api_optimizer import get_global_api_optimizer, optimize_api_usage, estimate_api_cost
from src.data_processing.language_detector import LanguageDetector
from src.utils.exceptions import (
    APIConnectionError, APITimeoutError, APIRateLimitError,
    AnalysisProcessingError, ErrorHandler
)
import time
import re

# Set up logging
logging.basicConfig(level=getattr(logging, Config.LOG_LEVEL))
logger = logging.getLogger(__name__)

class OpenAIAnalyzer:
    """Class to handle all AI analysis using OpenAI API"""
    
    def __init__(self, use_cache: bool = True):
        config_instance = Config()
        if not config_instance.OPENAI_API_KEY:
            raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY in environment variables.")
        
        # Use robust API client with timeout and retry handling
        self.robust_client = get_global_client()
        self.api_monitor = get_api_monitor()
        self.api_optimizer = get_global_api_optimizer()
        self.model = "gpt-4o-mini"  # Using cost-effective model
        self.use_cache = use_cache
        self.cache_manager = CacheManager() if use_cache else None
        self.api_calls_saved = 0  # Track cache hits
        self.language_detector = LanguageDetector()  # Initialize language detector
        
    def analyze_comments_batch(self, comments: List[str]) -> List[Dict]:
        """
        Analyze a batch of comments for sentiment, language, and key themes
        
        Args:
            comments: List of comment strings to analyze
            
        Returns:
            List of analysis results for each comment
        """
        # Check cache first if enabled
        if self.use_cache and self.cache_manager:
            cached_results = self.cache_manager.get_cached_analysis(comments, "sentiment")
            if cached_results and len(cached_results) == len(comments):
                self.api_calls_saved += 1
                logger.info(f"Using cached results for {len(comments)} comments")
                return cached_results
        
        results = []
        
        # Pre-detect languages for all comments to optimize API usage
        logger.info(f"Pre-detecting languages for {len(comments)} comments")
        language_info = []
        spanish_only = True  # Track if batch contains only Spanish for optimization
        
        for comment in comments:
            if not comment or not comment.strip():
                language_info.append({"language": "unknown", "confidence": 0.5})
                continue
                
            # Use our lightweight language detector
            lang_result = self.language_detector.detect_language(comment)
            language_info.append({
                "language": lang_result["language"], 
                "confidence": lang_result["confidence"]
            })
            
            # Check if we have non-Spanish content
            if lang_result["language"] != "es":
                spanish_only = False
        
        # Count by language
        language_counts = {}
        for info in language_info:
            lang = info["language"]
            language_counts[lang] = language_counts.get(lang, 0) + 1
        
        logger.info(f"Pre-detected language distribution: {language_counts}")
        
        # Use API optimizer for intelligent batching and rate limiting
        try:
            results = optimize_api_usage(
                items=comments,
                api_function=self._analyze_optimized_batch,
                language_info=language_info,
                model=self.model
            )
            
            # Cache the results if caching is enabled
            if self.use_cache and self.cache_manager and results:
                self.cache_manager.cache_analysis_result(comments, results, "sentiment")
                logger.info(f"Cached analysis results for {len(comments)} comments")
            
            return results
            
        except Exception as e:
            logger.error(f"Optimized batch analysis failed: {e}")
            # Fallback to traditional processing
            return self._analyze_comments_fallback(comments, language_info)
    
    def _analyze_optimized_batch(self, batch_comments: List[str], **kwargs) -> List[Dict]:
        """
        Process a batch of comments using optimized API calls
        This method is called by the API optimizer
        """
        language_info = kwargs.get('language_info', [])
        
        # Create language info if not provided
        if not language_info or len(language_info) != len(batch_comments):
            language_info = []
            for comment in batch_comments:
                if not comment or not comment.strip():
                    language_info.append({"language": "unknown", "confidence": 0.5})
                else:
                    lang_result = self.language_detector.detect_language(comment)
                    language_info.append({
                        "language": lang_result["language"], 
                        "confidence": lang_result["confidence"]
                    })
        
        # Enhance batch with language context for API
        enhanced_batch = []
        for i, comment in enumerate(batch_comments):
            if not comment or not comment.strip():
                enhanced_batch.append(comment)
                continue
                
            lang = language_info[i]["language"]
            # Only add language hint for non-Spanish or mixed to help the API
            if lang in ["gn", "mixed"]:
                enhanced_batch.append(f"{comment} [pre-detected language: {lang}]")
            else:
                enhanced_batch.append(comment)
        
        try:
            # Use existing batch analysis method
            batch_results = self._analyze_batch_openai(enhanced_batch)
            
            # Enhance results with pre-detected language info
            for i, result in enumerate(batch_results):
                if i < len(language_info):
                    result["pre_detected_language"] = language_info[i]["language"]
                    result["language_confidence"] = language_info[i]["confidence"]
                    
                    # If our confidence is high, override the API's language detection
                    if language_info[i]["confidence"] > 0.8:
                        result["language"] = language_info[i]["language"]
            
            return batch_results
            
        except Exception as e:
            logger.error(f"Error in optimized batch processing: {e}")
            # Return default results for failed batch
            return [self._get_default_result_with_language(comment, language_info[i] if i < len(language_info) else None) 
                   for i, comment in enumerate(batch_comments)]
    
    def _analyze_comments_fallback(self, comments: List[str], language_info: List[Dict]) -> List[Dict]:
        """
        Fallback method for when optimized processing fails
        Uses traditional batch processing with manual rate limiting
        """
        results = []
        
        # Process in smaller batches for fallback
        batch_size = min(25, len(comments))  # Smaller batches for stability
        for i in range(0, len(comments), batch_size):
            batch = comments[i:i+batch_size]
            batch_langs = language_info[i:i+batch_size]
            
            try:
                batch_results = self._analyze_optimized_batch(batch, language_info=batch_langs)
                results.extend(batch_results)
                
                # Manual rate limiting for fallback
                if i + batch_size < len(comments):
                    time.sleep(2.0)  # More conservative delay
                
            except Exception as e:
                logger.error(f"Error processing fallback batch {i//batch_size + 1}: {str(e)}")
                # Add default results for failed batch
                for j, comment in enumerate(batch):
                    lang_info = batch_langs[j] if j < len(batch_langs) else None
                    default_result = self._get_default_result_with_language(comment, lang_info)
                    results.append(default_result)
        
        return results
    
    def _get_default_result_with_language(self, comment: str, lang_info: Optional[Dict] = None) -> Dict:
        """Get default result with language information"""
        default_result = self._get_default_result(comment)
        
        if lang_info:
            default_result["pre_detected_language"] = lang_info["language"]
            default_result["language_confidence"] = lang_info["confidence"]
            if lang_info["language"] != "unknown":
                default_result["language"] = lang_info["language"]
        
        return default_result
    
    def _analyze_batch_openai(self, comments: List[str]) -> List[Dict]:
        """Analyze a small batch of comments using OpenAI with retry logic"""
        
        # Create numbered comments for the prompt
        numbered_comments = []
        for i, comment in enumerate(comments, 1):
            numbered_comments.append(f"{i}. {comment}")
        
        comments_text = "\n".join(numbered_comments)
        
        prompt = f"""
You are analyzing {len(comments)} customer comments about telecommunications/fiber internet services in Paraguay.

YOUR TASK: For EACH numbered comment, analyze and extract the following information:
1. Sentiment: ONLY "positive", "negative", or "neutral" - be consistent
2. Confidence: Value between 0.0-1.0 showing your confidence in the sentiment classification
3. Language: ONLY "es" (Spanish), "gn" (Guarani), or "mixed" - no other values
4. Translation: If Guarani or mixed, provide Spanish translation; if Spanish, copy original
5. Key themes: Array of main topics (maximum 3 short terms)
6. Pain points: Array of specific problems mentioned (can be empty)
7. Emotions: Array of primary emotions detected

IMPORTANT: Some comments include pre-detected language information. Use this information to guide your analysis.
When a comment has [pre-detected language: gn] or [pre-detected language: mixed], focus extra attention on proper translation.

Comments to analyze:
{comments_text}

VERY IMPORTANT INSTRUCTIONS:
- Always respond with a valid JSON array 
- Include EXACTLY {len(comments)} objects in your JSON response
- Maintain the EXACT same order as the input comments
- Be concise in themes/pain points (1-3 words each)
- Never leave any field empty/null - use empty arrays [] where appropriate
- Keep translations and themes short and to the point
- Maintain consistent format across ALL comments

Required JSON format (one object for each comment):
[
  {{
    "comment_number": 1,
    "sentiment": "negative",
    "confidence": 0.85,
    "language": "es",
    "translation": "El servicio es muy lento",
    "themes": ["velocidad", "calidad_servicio"],
    "pain_points": ["conexión lenta"],
    "emotions": ["frustración"]
  }},
  {{
    "comment_number": 2,
    "sentiment": "positive",
    "confidence": 0.92,
    "language": "es",
    "translation": "Excelente servicio y rápido",
    "themes": ["calidad_servicio", "velocidad"],
    "pain_points": [],
    "emotions": ["satisfacción"]
  }},
  ... (continue for each comment)
]

Return ONLY the JSON array with no additional text or explanation.
"""

        # Use robust API client with automatic timeout and retry handling
        try:
            start_time = time.time()
            
            # Calculate dynamic max_tokens based on batch size
            # Estimate: ~150 tokens per comment response + 500 buffer
            estimated_response_tokens = len(comments) * 150 + 500
            max_tokens = min(8000, max(4000, estimated_response_tokens))
            logger.debug(f"Using max_tokens={max_tokens} for {len(comments)} comments")
            
            # Make robust API call
            response = self.robust_client.chat_completion(
                messages=[
                    {"role": "system", "content": "You are an expert in telecommunications customer sentiment analysis for Paraguay. Respond only with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                model=self.model,
                temperature=0.1,
                max_tokens=max_tokens
            )
            
            # Log performance metrics
            duration = time.time() - start_time
            self.api_monitor.log_request(duration, True)
            
            response_text = response.choices[0].message.content
            
            # Log response for debugging
            logger.debug(f"OpenAI raw response ({len(response_text)} chars): {response_text[:1000]}...")
            
            # Dynamic token limit warning based on calculated max_tokens
            # Use 85% of max_tokens as warning threshold (conservative)
            warning_threshold = int(max_tokens * 0.85 * 4)  # ~4 chars per token
            if len(response_text) >= warning_threshold:
                logger.warning(f"Response near token limit - may be truncated (response: {len(response_text)} chars, threshold: {warning_threshold}, max_tokens: {max_tokens})")
            
            # Robust JSON parsing - try direct parsing first
            try:
                # Try direct JSON parsing (most reliable)
                results = json.loads(response_text.strip())
                logger.debug(f"Direct JSON parsing successful: {len(results)} results")
            except json.JSONDecodeError:
                # Fallback to regex extraction for responses with extra text
                logger.debug("Direct JSON parsing failed, trying regex extraction...")
                json_match = re.search(r'(\[[\s\S]*\])', response_text)
                if json_match:
                    clean_json = json_match.group(1)
                    try:
                        results = json.loads(clean_json)
                        logger.debug(f"Regex JSON parsing successful: {len(results)} results")
                    except json.JSONDecodeError as e:
                        logger.error(f"Invalid JSON after regex extraction: {str(e)}")
                        logger.error(f"Extracted JSON: {clean_json[:500]}...")
                        raise AnalysisProcessingError(f"JSON parsing failed: {str(e)}")
                else:
                    logger.error(f"No JSON array found in response: {response_text[:500]}...")
                    raise AnalysisProcessingError("No valid JSON array found in API response")
            
            # Validate results structure
            if not isinstance(results, list):
                logger.error(f"Expected JSON array, got: {type(results)}")
                raise AnalysisProcessingError("API response is not a JSON array")
            
            # Validate and fill missing results
            while len(results) < len(comments):
                missing_idx = len(results)
                logger.warning(f"Missing result for comment {missing_idx + 1}, adding default")
                results.append(self._get_default_result(comments[missing_idx]))
                
            return results[:len(comments)]  # Ensure exact match
                
        except (APIConnectionError, APITimeoutError, APIRateLimitError) as e:
            # Log specific API errors
            error_type = type(e).__name__
            self.api_monitor.log_request(0, False, error_type)
            logger.error(f"API error during comment analysis: {str(e)}")
            # Return default results for failed batches instead of crashing
            logger.warning(f"Returning default results for {len(comments)} comments due to API error")
            return [self._get_default_result(comment) for comment in comments]
            
        except Exception as e:
            # Log unexpected errors
            self.api_monitor.log_request(0, False, "UnexpectedError")
            logger.error(f"Unexpected error during comment analysis: {str(e)}")
            # Return default results for failed batches instead of crashing
            logger.warning(f"Returning default results for {len(comments)} comments due to unexpected error")
            return [self._get_default_result(comment) for comment in comments]
    
    def _get_default_result(self, comment: str) -> Dict:
        """Get dynamic analysis result for failed cases (no more fixed values)"""
        # Use basic rule-based analysis instead of fixed values
        from shared.business.analysis_engine import analyze_sentiment_simple, extract_themes_simple
        
        # Dynamic sentiment instead of always 'neutral'
        dynamic_sentiment = analyze_sentiment_simple(comment) if comment else 'neutral'
        
        # Dynamic themes instead of always 'sin_clasificar'
        if comment and comment.strip():
            theme_result = extract_themes_simple([comment])
            dynamic_themes = list(theme_result[0].keys()) if theme_result and theme_result[0] else []
            if not dynamic_themes:
                # Content-based theme detection as fallback
                comment_lower = comment.lower()
                if any(word in comment_lower for word in ['internet', 'fibra', 'conexion']):
                    dynamic_themes = ['conectividad']
                elif any(word in comment_lower for word in ['servicio', 'atencion']):
                    dynamic_themes = ['servicio']
                else:
                    dynamic_themes = ['comentario_general']
        else:
            dynamic_themes = ['sin_datos']
        
        # Dynamic confidence based on comment length and specificity
        confidence = 0.3  # minimum
        if comment and len(comment.split()) > 5:
            confidence += 0.2
        if comment and any(word in comment.lower() for word in ['muy', 'excelente', 'pésimo', 'problema']):
            confidence += 0.2
        confidence = min(0.8, confidence)  # cap at 0.8 for fallback
        
        # Dynamic emotions based on content
        dynamic_emotions = ['neutral']
        if comment:
            comment_lower = comment.lower()
            if any(word in comment_lower for word in ['excelente', 'bueno', 'bien']):
                dynamic_emotions = ['satisfacción']
            elif any(word in comment_lower for word in ['malo', 'problema', 'lento']):
                dynamic_emotions = ['frustración']
            elif any(word in comment_lower for word in ['rápido', 'eficiente']):
                dynamic_emotions = ['alegría']
        
        return {
            "comment_number": 0,
            "sentiment": dynamic_sentiment,
            "confidence": confidence,
            "language": "es",
            "translation": comment,
            "themes": dynamic_themes,
            "pain_points": self._extract_pain_points_dynamic(comment),
            "emotions": dynamic_emotions
        }
    
    def _extract_pain_points_dynamic(self, comment: str) -> List[str]:
        """Extract pain points dynamically from comment"""
        if not comment:
            return []
        
        pain_points = []
        comment_lower = comment.lower()
        
        if any(word in comment_lower for word in ['lento', 'demora']):
            pain_points.append('velocidad_baja')
        if any(word in comment_lower for word in ['se corta', 'desconecta']):
            pain_points.append('conexión_inestable')
        if any(word in comment_lower for word in ['caro', 'precio']):
            pain_points.append('precio_alto')
        if any(word in comment_lower for word in ['soporte', 'atencion']):
            pain_points.append('soporte_deficiente')
        
        return pain_points
    
    def analyze_batch(self, comments: List[str], progress_callback=None) -> List[Dict]:
        """
        Alias for analyze_comments_batch for compatibility with AI adapter
        """
        return self.analyze_comments_batch(comments)
    
    def analyze_single_comment(self, comment: str) -> Dict:
        """Analyze a single comment"""
        results = self.analyze_comments_batch([comment])
        return results[0] if results else self._get_default_result(comment)
    
    def get_overall_insights(self, analysis_results: List[Dict]) -> Dict:
        """Generate overall insights from all analyzed comments"""
        
        # Aggregate data
        sentiments = [r['sentiment'] for r in analysis_results]
        themes = []
        pain_points = []
        languages = [r['language'] for r in analysis_results]
        
        for result in analysis_results:
            themes.extend(result.get('themes', []))
            pain_points.extend(result.get('pain_points', []))
        
        # Count frequencies
        sentiment_counts = pd.Series(sentiments).value_counts().to_dict()
        theme_counts = pd.Series(themes).value_counts().head(10).to_dict()
        pain_point_counts = pd.Series(pain_points).value_counts().head(10).to_dict()
        language_counts = pd.Series(languages).value_counts().to_dict()
        
        # Calculate percentages
        total = len(analysis_results)
        sentiment_percentages = {k: round((v/total)*100, 1) for k, v in sentiment_counts.items()}
        
        return {
            "total_comments": total,
            "sentiment_distribution": sentiment_counts,
            "sentiment_percentages": sentiment_percentages,
            "top_themes": theme_counts,
            "top_pain_points": pain_point_counts,
            "language_distribution": language_counts,
            "avg_confidence": round(sum(r.get('confidence', 0.5) for r in analysis_results) / total, 2),
            "guarani_percentage": round((language_counts.get('gn', 0) + language_counts.get('mixed', 0)) / total * 100, 1)
        }
    
    def generate_recommendations(self, insights: Dict) -> List[str]:
        """Generate business recommendations based on analysis insights"""
        
        recommendations = []
        
        # Sentiment-based recommendations
        negative_pct = insights['sentiment_percentages'].get('negative', 0)
        if negative_pct > 30:
            recommendations.append(f"Alta prioridad: {negative_pct}% de comentarios negativos - requiere acción inmediata")
        elif negative_pct > 15:
            recommendations.append(f"Atención: {negative_pct}% de comentarios negativos - monitorear tendencias")
        
        # Theme-based recommendations
        top_themes = list(insights['top_themes'].keys())[:3]
        if top_themes:
            recommendations.append(f"Enfocar mejoras en: {', '.join(top_themes)}")
        
        # Pain point recommendations
        top_pain_points = list(insights['top_pain_points'].keys())[:3]
        if top_pain_points:
            recommendations.append(f"Resolver problemas principales: {', '.join(top_pain_points)}")
        
        # Language recommendations
        guarani_pct = insights.get('guarani_percentage', 0)
        if guarani_pct > 5:
            recommendations.append(f"Considerar soporte en guaraní: {guarani_pct}% de comentarios en guaraní/mixto")
        
        # Confidence recommendations
        avg_confidence = insights.get('avg_confidence', 0)
        if avg_confidence < 0.7:
            recommendations.append("Revisar manualmente comentarios con baja confianza de clasificación")
        
        return recommendations
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics and performance metrics"""
        if not self.use_cache or not self.cache_manager:
            return {"caching": "disabled"}
        
        cache_stats = self.cache_manager.get_cache_stats()
        cache_stats["api_calls_saved_this_session"] = self.api_calls_saved
        
        return cache_stats
    
    def get_api_health_status(self) -> Dict:
        """Get current API connection health status"""
        try:
            client_stats = self.robust_client.get_stats()
            monitor_stats = self.api_monitor.get_performance_summary()
            
            return {
                "connection_health": {
                    "circuit_breaker_state": client_stats.get("circuit_breaker_state", "UNKNOWN"),
                    "success_rate": client_stats.get("success_rate_percent", 0),
                    "total_requests": client_stats.get("total_requests", 0),
                    "recent_failures": client_stats.get("failure_count", 0)
                },
                "performance_metrics": monitor_stats,
                "api_calls_saved": self.api_calls_saved,
                "cache_enabled": self.use_cache
            }
        except Exception as e:
            logger.error(f"Error getting API health status: {str(e)}")
            return {"error": str(e)}
    
    @timeout_handler(timeout_seconds=30)
    def test_connection(self) -> Dict:
        """Test API connection with minimal request"""
        try:
            start_time = time.time()
            
            response = self.robust_client.chat_completion(
                messages=[{"role": "user", "content": "test"}],
                model=self.model,
                max_tokens=1,
                temperature=0
            )
            
            duration = time.time() - start_time
            
            return {
                "status": "healthy",
                "response_time_ms": round(duration * 1000, 2),
                "api_available": True,
                "test_timestamp": time.time()
            }
            
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "api_available": False,
                "test_timestamp": time.time()
            }
    
    def clear_cache(self) -> bool:
        """Clear the analysis cache"""
        if not self.use_cache or not self.cache_manager:
            return False
        
        return self.cache_manager.clear_cache()
    
    def cleanup_cache(self) -> int:
        """Clean up expired cache entries"""
        if not self.use_cache or not self.cache_manager:
            return 0
        
        return self.cache_manager.cleanup_expired_cache()
    
    def get_api_performance_stats(self) -> Dict[str, Any]:
        """
        Get comprehensive API performance and optimization statistics
        
        Returns:
            Dictionary containing performance metrics and optimization info
        """
        optimizer_stats = self.api_optimizer.get_performance_stats()
        
        # Add analyzer-specific stats
        stats = {
            "api_optimizer": optimizer_stats,
            "cache_hits_saved": self.api_calls_saved,
            "cache_enabled": self.use_cache,
            "model_used": self.model,
            "estimated_total_cost": optimizer_stats.get("total_requests", 0) * 0.002,
            "cost_saved_from_cache": optimizer_stats.get("estimated_cost_saved", 0),
        }
        
        # Add API monitor stats if available
        if hasattr(self.api_monitor, 'get_performance_metrics'):
            monitor_stats = self.api_monitor.get_performance_metrics()
            stats["api_monitor"] = monitor_stats
        
        return stats
    
    def optimize_for_budget(self, total_comments: int, budget_usd: float) -> Dict[str, Any]:
        """
        Suggest optimal processing configuration for given budget
        
        Args:
            total_comments: Total number of comments to process
            budget_usd: Available budget in USD
            
        Returns:
            Optimization suggestions
        """
        from api.api_optimizer import suggest_batch_size_for_budget
        
        avg_tokens_per_comment = 250  # Conservative estimate
        
        suggestions = suggest_batch_size_for_budget(
            budget_usd=budget_usd,
            total_items=total_comments,
            avg_tokens_per_item=avg_tokens_per_comment,
            model=self.model
        )
        
        # Add analyzer-specific recommendations
        if suggestions["can_process_all"]:
            suggestions["recommendation"] = (
                f"Budget allows processing all {total_comments} comments. "
                f"Use batch size of {suggestions['suggested_batch_size']} for optimal performance."
            )
        else:
            suggestions["recommendation"] = (
                f"Budget allows processing {suggestions['items_to_process']} of {total_comments} comments. "
                f"Consider increasing budget by ${budget_usd * 0.5:.2f} to process 50% more comments."
            )
        
        return suggestions

# Example usage and testing
if __name__ == "__main__":
    # Test with sample comments
    sample_comments = [
        "El servicio de fibra es excelente, muy rápido",
        "Tengo problemas con la conexión, se corta mucho",
        "El precio está bien pero la instalación demoró mucho"
    ]
    
    try:
        analyzer = OpenAIAnalyzer()
        results = analyzer.analyze_comments_batch(sample_comments)
        
        print("Analysis Results:")
        for i, result in enumerate(results):
            print(f"\nComment {i+1}: {sample_comments[i]}")
            print(f"Sentiment: {result['sentiment']} (confidence: {result['confidence']})")
            print(f"Language: {result['language']}")
            print(f"Themes: {result['themes']}")
            
        insights = analyzer.get_overall_insights(results)
        print("\nOverall Insights:")
        print(json.dumps(insights, indent=2, ensure_ascii=False))
        
        recommendations = analyzer.generate_recommendations(insights)
        print("\nRecommendations:")
        for rec in recommendations:
            print(f"- {rec}")
            
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure to set OPENAI_API_KEY environment variable")