"""
AI Interface - OpenAI communication responsibilities
Extracted from AIAnalysisAdapter for focused AI interaction
"""

import logging
from typing import List, Dict, Optional, Any, Callable
from src.sentiment_analysis.openai_analyzer import OpenAIAnalyzer

logger = logging.getLogger(__name__)


class AIInterface:
    """
    Handles all OpenAI API communication and analysis
    Focused responsibility for AI interaction
    """
    
    def __init__(self):
        self.openai_analyzer = None
        self.ai_available = False
        
        # Initialize OpenAI analyzer
        try:
            logger.info("Initializing OpenAI analyzer...")
            
            # Check for API key
            from src.config import Config
            config_instance = Config()
            api_key = config_instance.OPENAI_API_KEY
            
            if not api_key:
                logger.error("OpenAI API key not found in environment variables")
                self.ai_available = False
                return
                
            logger.debug(f"API key found: {'*' * 10}... (length: {len(api_key) if api_key else 0})")
            
            self.openai_analyzer = OpenAIAnalyzer(use_cache=True)
            self.ai_available = True
            logger.info("✅ OpenAI analyzer initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI: {str(e)}")
            self.ai_available = False
    
    def analyze_comments(self, comments: List[str], progress_callback: Optional[Callable] = None) -> Optional[List[Dict]]:
        """
        Perform AI analysis on list of comments
        
        Args:
            comments: List of comment strings to analyze
            progress_callback: Optional progress callback function
            
        Returns:
            List of AI analysis results or None if failed
        """
        if not self.ai_available or not self.openai_analyzer:
            logger.warning("AI not available for analysis")
            return None
        
        try:
            logger.info(f"🤖 Attempting AI analysis of {len(comments)} comments")
            
            # Update progress
            if progress_callback:
                progress_callback(0.3, "Iniciando análisis con IA...")
            
            # Perform AI analysis using OpenAI analyzer
            ai_results = self.openai_analyzer.analyze_batch(comments, progress_callback=progress_callback)
            
            if ai_results and len(ai_results) > 0:
                logger.info(f"✅ AI analysis successful: {len(ai_results)} results")
                return ai_results
            else:
                logger.warning("❌ AI analysis returned no results")
                return None
                
        except Exception as e:
            logger.error(f"AI analysis failed: {str(e)}")
            return None
    
    def get_analyzer_stats(self) -> Dict[str, Any]:
        """Get performance and usage statistics from AI analyzer"""
        if not self.ai_available or not self.openai_analyzer:
            return {"ai_available": False}
        
        try:
            stats = {
                "ai_available": True,
                "cache_stats": self.openai_analyzer.get_cache_stats(),
                "api_health": self.openai_analyzer.get_api_health_status(),
                "performance_stats": self.openai_analyzer.get_api_performance_stats()
            }
            return stats
            
        except Exception as e:
            logger.error(f"Failed to get analyzer stats: {str(e)}")
            return {"ai_available": True, "stats_error": str(e)}
    
    def test_connection(self) -> Dict[str, Any]:
        """Test AI connection and return status"""
        if not self.ai_available or not self.openai_analyzer:
            return {
                "status": "unavailable",
                "ai_available": False,
                "error": "AI analyzer not initialized"
            }
        
        try:
            return self.openai_analyzer.test_connection()
        except Exception as e:
            logger.error(f"AI connection test failed: {str(e)}")
            return {
                "status": "error",
                "ai_available": False,
                "error": str(e)
            }