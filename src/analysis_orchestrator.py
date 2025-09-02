"""
Analysis Orchestrator - Main coordination responsibilities
Extracted from AIAnalysisAdapter for orchestration logic
"""

import time
import logging
import traceback
from typing import Dict, Optional, Any

logger = logging.getLogger(__name__)


class AnalysisOrchestrator:
    """
    Orchestrates the complete AI analysis pipeline
    Coordinates between data processing, AI interface, and result conversion
    """
    
    def __init__(self):
        # Initialize component dependencies
        from src.ai_data_processor import AIDataProcessor
        from src.ai_interface import AIInterface  
        from src.result_converter import ResultConverter
        
        self.data_processor = AIDataProcessor()
        self.ai_interface = AIInterface()
        self.result_converter = ResultConverter()
        
        # Analysis metadata
        self.ai_available = self.ai_interface.ai_available
        
        logger.info(f"Analysis Orchestrator initialized - AI Available: {self.ai_available}")
    
    def process_uploaded_file_with_ai(self, uploaded_file) -> Optional[Dict]:
        """
        Main orchestration method - coordinates complete analysis pipeline
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            Complete analysis results or None if failed
        """
        start_time = time.time()
        analysis_type = "UNKNOWN"
        
        try:
            logger.info(f"🚀 Starting analysis orchestration for: {uploaded_file.name}")
            
            # STEP 1: Data Processing
            logger.info("📊 Step 1: Processing uploaded file...")
            df = self.data_processor.read_and_validate_file(uploaded_file)
            analysis_data = self.data_processor.extract_analysis_data(df)
            
            logger.info(f"📊 Preprocessed {analysis_data['total_rows']} raw → {len(analysis_data['comments'])} unique comments")
            
            # STEP 2: AI Analysis (if available)
            if self.ai_available:
                logger.info("🤖 Step 2: Attempting AI analysis...")
                analysis_type = "AI_POWERED"
                
                ai_results = self.ai_interface.analyze_comments(analysis_data['comments'])
                
                if ai_results and len(ai_results) > 0:
                    logger.info("✅ AI analysis successful - proceeding with format conversion")
                    
                    # STEP 3: Result Conversion
                    logger.info("🔄 Step 3: Converting results to expected format...")
                    result = self.result_converter.convert_ai_results_to_expected_format(
                        ai_results, analysis_data, uploaded_file
                    )
                    
                    duration = time.time() - start_time
                    logger.info(f"🏁 Analysis completed successfully | Type: {analysis_type} | Duration: {duration:.2f}s")
                    
                    return result
                else:
                    logger.warning("❌ AI analysis failed - executing rule-based fallback")
                    analysis_type = "RULE_BASED_FALLBACK"
                    return self._execute_fallback_analysis(analysis_data, uploaded_file)
            else:
                logger.info("⚡ AI not available - executing rule-based analysis")
                analysis_type = "RULE_BASED"
                return self._execute_fallback_analysis(analysis_data, uploaded_file)
                
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"💥 Analysis failed completely: {str(e)} | Duration: {duration:.2f}s")
            logger.error(f"Error occurred at analysis_type: {analysis_type}")
            logger.debug(f"Full error traceback: {traceback.format_exc()}")
            
            # Log diagnostic information (with proper error handling)
            try:
                logger.debug(f"File name: {uploaded_file.name if hasattr(uploaded_file, 'name') else 'Unknown'}")
                logger.debug(f"File size: {uploaded_file.size if hasattr(uploaded_file, 'size') else 'Unknown'}")
                logger.debug(f"AI available: {self.ai_available}")
            except Exception as debug_error:
                logger.warning(f"Failed to log debug info: {debug_error}")
                # Continue execution - debug logging failure is not critical
            
            return self._create_error_response(f"Critical analysis failure: {str(e)}")
        finally:
            duration = time.time() - start_time
            logger.info(f"🏁 Analysis completed | Type: {analysis_type} | Duration: {duration:.2f}s")
    
    def _execute_fallback_analysis(self, analysis_data: Dict, uploaded_file) -> Dict[str, Any]:
        """Execute rule-based analysis as fallback"""
        try:
            logger.info("[ORCHESTRATOR] Executing rule-based fallback analysis")
            
            # Import analysis engine for fallback
            from shared.business.analysis_engine import (
                analyze_sentiment_simple, extract_themes_simple,
                calculate_sentiment_percentages, generate_insights_summary,
                create_recommendations
            )
            
            comments = analysis_data['comments']
            
            # Basic sentiment analysis
            sentiments = [analyze_sentiment_simple(comment) for comment in comments]
            
            # Extract themes
            theme_counts, theme_examples = extract_themes_simple(comments)
            
            # Calculate statistics
            sentiment_percentages = calculate_sentiment_percentages(sentiments)
            
            # Generate fallback result structure
            return {
                'total': len(comments),
                'comments': comments,
                'sentiments': sentiments,
                'sentiment_percentages': sentiment_percentages,
                'theme_counts': theme_counts,
                'theme_examples': theme_examples,
                'original_filename': uploaded_file.name,
                'analysis_method': 'RULE_BASED_FALLBACK',
                'insights': generate_insights_summary({'sentiments': sentiments, 'sentiment_percentages': sentiment_percentages}, enhanced_ai=False),
                'recommendations': create_recommendations({'sentiments': sentiments, 'sentiment_percentages': sentiment_percentages}, enhanced_ai=False)
            }
            
        except Exception as e:
            logger.error(f"Fallback analysis failed: {str(e)}")
            return self._create_error_response(f"All analysis methods failed: {str(e)}")
    
    def _create_error_response(self, error_message: str) -> Dict[str, Any]:
        """Create standardized error response"""
        return {
            'error': True,
            'error_message': error_message,
            'total': 0,
            'sentiments': [],
            'sentiment_percentages': {'positivo': 0, 'negativo': 0, 'neutral': 0},
            'insights': {'total_comments': 0, 'analysis_method': 'ERROR'},
            'recommendations': ['Error en análisis - revise archivo y configuración']
        }
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        return {
            'ai_available': self.ai_available,
            'ai_stats': self.ai_interface.get_analyzer_stats() if self.ai_available else {},
            'orchestrator_status': 'operational',
            'components': {
                'data_processor': 'operational',
                'ai_interface': 'operational' if self.ai_available else 'limited',
                'result_converter': 'operational'
            }
        }