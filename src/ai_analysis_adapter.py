"""
AI Analysis Adapter - Interface between OpenAI API and existing data formats
This module converts OpenAI API responses to the exact format expected by the existing system,
ensuring zero breaking changes while adding AI capabilities.
"""

import pandas as pd
import numpy as np
from collections import Counter, defaultdict
import re
import logging
import time
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
import traceback
import os
from io import BytesIO

from src.sentiment_analysis.openai_analyzer import OpenAIAnalyzer
from src.enhanced_analysis import EnhancedAnalysis
from src.improved_analysis import ImprovedAnalysis

# Configure detailed logging for AI pipeline
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create AI pipeline specific logger
ai_logger = logging.getLogger("ai_pipeline")
ai_handler = logging.StreamHandler()
ai_formatter = logging.Formatter('[%(asctime)s] AI_PIPELINE - %(levelname)s - %(message)s')
ai_handler.setFormatter(ai_formatter)
ai_logger.addHandler(ai_handler)
ai_logger.setLevel(logging.DEBUG)

class AIAnalysisAdapter:
    """
    Adapter that provides AI-powered analysis while maintaining 
    compatibility with existing data formats and processing pipeline
    """
    
    def __init__(self):
        """Initialize the AI adapter with fallback analyzers"""
        self.openai_analyzer = None
        self.enhanced_analyzer = EnhancedAnalysis()  # Fallback
        self.improved_analyzer = ImprovedAnalysis()  # Fallback
        self.ai_available = False
        
        # Initialize OpenAI analyzer with comprehensive error handling
        try:
            ai_logger.info("Initializing OpenAI analyzer...")
            
            # Check for API key
            from src.config import Config
            config_instance = Config()
            api_key = config_instance.OPENAI_API_KEY
            
            if not api_key:
                ai_logger.error("OpenAI API key not found in environment variables")
                self.ai_available = False
                return
                
            ai_logger.debug(f"API key found: {'*' * 10}... (length: {len(api_key) if api_key else 0})")
            
            self.openai_analyzer = OpenAIAnalyzer(use_cache=True)
            self.ai_available = True
            ai_logger.info("✅ OpenAI analyzer initialized successfully")
            
        except ImportError as e:
            ai_logger.error(f"Failed to import OpenAI dependencies: {str(e)}")
            ai_logger.debug(f"Import error traceback: {traceback.format_exc()}")
            self.ai_available = False
        except Exception as e:
            ai_logger.error(f"OpenAI initialization failed: {str(e)}")
            ai_logger.debug(f"Initialization error traceback: {traceback.format_exc()}")
            self.ai_available = False
    
    def _read_and_validate_file(self, uploaded_file) -> pd.DataFrame:
        """Extract file reading logic to reduce nesting"""
        try:
            ai_logger.info(f"🚀 Reading file: {uploaded_file.name}")
            ai_logger.debug(f"File size: {uploaded_file.size} bytes")
            
            if uploaded_file.name.endswith('.csv'):
                return self._read_csv_file(uploaded_file)
            else:
                return self._read_excel_file(uploaded_file)
                
        except Exception as e:
            ai_logger.error(f"Failed to read file {uploaded_file.name}: {str(e)}")
            return None
    
    def _read_csv_file(self, uploaded_file) -> pd.DataFrame:
        """Read CSV file with proper handling and memory cleanup"""
        try:
            if hasattr(uploaded_file, 'read'):
                uploaded_file.seek(0)
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_csv(uploaded_file.content)
            
            # MICRO-FIX: Explicitly close file handle if possible
            if hasattr(uploaded_file, 'close'):
                uploaded_file.close()
            
            return df
        except Exception as e:
            # Clean up even on error
            if 'df' in locals():
                del df
            raise
    
    def _read_excel_file(self, uploaded_file) -> pd.DataFrame:
        """Read Excel file with proper handling and memory cleanup"""
        file_buffer = None
        file_content = None
        
        try:
            if hasattr(uploaded_file, 'read'):
                uploaded_file.seek(0)
                file_content = uploaded_file.read()
                file_buffer = BytesIO(file_content)
                df = pd.read_excel(file_buffer)
            else:
                df = pd.read_excel(uploaded_file.content)
            
            # MICRO-FIX: Explicit cleanup of file objects
            if file_buffer:
                file_buffer.close()
                del file_buffer
            
            if file_content:
                del file_content
            
            if hasattr(uploaded_file, 'close'):
                uploaded_file.close()
            
            return df
            
        except Exception as e:
            # Clean up on error
            if 'df' in locals():
                del df
            if file_buffer:
                file_buffer.close()
            if 'file_content' in locals():
                del file_content
            raise
    
    def _extract_analysis_data(self, df: pd.DataFrame) -> Dict:
        """Extract and prepare data for analysis to reduce main function complexity"""
        try:
            # Check for NPS and Nota columns
            has_nps = 'NPS' in df.columns
            has_nota = 'Nota' in df.columns
            nps_data = df['NPS'].tolist() if has_nps else []
            nota_data = df['Nota'].tolist() if has_nota else []
            
            # Find comment column
            comment_col = self._find_comment_column(df)
            if comment_col is None:
                ai_logger.error("No comment column found")
                return None
                
            # Extract and clean comments
            raw_comments = df[comment_col].dropna().tolist()
            if not raw_comments:
                ai_logger.error("No valid comments found")
                return None
                
            # Clean and process comments
            comments, comment_frequencies = self._clean_and_process_comments(raw_comments)
            
            return {
                'comments': comments,
                'comment_frequencies': comment_frequencies,
                'raw_comments': raw_comments,
                'nps_data': nps_data,
                'nota_data': nota_data,
                'has_nps': has_nps,
                'has_nota': has_nota
            }
            
        except Exception as e:
            ai_logger.error(f"Error extracting analysis data: {str(e)}")
            return None
    
    def _find_comment_column(self, df: pd.DataFrame) -> str:
        """Find the comment column in the dataframe"""
        comment_cols = ['comentario final', 'comment', 'comments', 'feedback', 'review', 'texto', 
                       'comentario', 'comentarios', 'respuesta', 'opinion', 'observacion']
        
        # Check explicit comment column names
        for col in df.columns:
            if any(name in col.lower() for name in comment_cols):
                return col
        
        # Fallback to first text column
        if len(df.columns) > 0:
            for col in df.columns:
                if df[col].dtype == 'object':
                    return col
        
        return None
    
    def _clean_and_process_comments(self, raw_comments: List[str]) -> Tuple[List[str], List[int]]:
        """Clean comments and calculate frequencies using existing functions"""
        # Import from correct locations (src.main is disabled)
        try:
            from src.utils.text_processing import clean_text
            from shared.business.analysis_engine import remove_duplicates_simple as remove_duplicates
        except ImportError:
            # Fallback implementations
            def clean_text(text):
                import re
                if not text or pd.isna(text):
                    return ""
                text = str(text).strip()
                text = re.sub(r'[^\w\s]', ' ', text)
                text = re.sub(r'\s+', ' ', text)
                return text.lower()
            
            def remove_duplicates(comments):
                seen = {}
                unique_comments = []
                frequencies = []
                
                for comment in comments:
                    if comment in seen:
                        seen[comment] += 1
                    else:
                        seen[comment] = 1
                        unique_comments.append(comment)
                
                frequencies = [seen[comment] for comment in unique_comments]
                return unique_comments, frequencies
        
        # Clean comments using existing function
        cleaned_comments = [clean_text(comment) for comment in raw_comments]
        
        # Get unique comments and frequencies using existing function
        unique_comments, comment_frequencies = remove_duplicates(cleaned_comments)
        
        ai_logger.info(f"Processed {len(raw_comments)} raw → {len(unique_comments)} unique comments")
        return unique_comments, comment_frequencies
    
    def _attempt_ai_analysis(self, comments: List[str], progress_bar=None) -> List[Dict]:
        """Attempt AI analysis with proper error handling"""
        if not self.ai_available or not self.openai_analyzer:
            ai_logger.info("OpenAI analyzer not available, skipping AI analysis")
            return None
            
        try:
            ai_logger.info(f"🤖 Attempting AI analysis of {len(comments)} unique comments")
            
            # Update progress
            if progress_bar:
                progress_bar.progress(0.3, "Iniciando análisis con IA...")
            
            # Perform AI analysis
            ai_results = self.openai_analyzer.analyze_batch(comments, progress_callback=progress_bar)
            
            if ai_results and len(ai_results) > 0:
                ai_logger.info(f"✅ AI analysis successful: {len(ai_results)} results")
                return ai_results
            else:
                ai_logger.warning("❌ AI analysis returned no results")
                return None
                
        except Exception as e:
            ai_logger.error(f"AI analysis failed: {str(e)}")
            ai_logger.debug(f"AI analysis error traceback: {traceback.format_exc()}")
            return None
    
    def _process_ai_results(self, ai_results: List[Dict], analysis_data: Dict, uploaded_file) -> Dict:
        """Process AI results into expected format"""
        return self._convert_ai_results_to_expected_format(
            ai_results, analysis_data['comments'], 
            analysis_data['comment_frequencies'], uploaded_file,
            analysis_data['raw_comments'], analysis_data['nps_data'],
            analysis_data['nota_data'], analysis_data['has_nps'], analysis_data['has_nota']
        )
    
    def _create_error_response(self, error_message: str) -> Dict:
        """Create standardized error response"""
        return {
            'analysis_results': [],
            'sentiments': [],
            'enhanced_results': [],
            'insights': {
                'total_comments': 0,
                'sentiment_percentages': {'positivo': 0, 'negativo': 0, 'neutral': 100},
                'avg_confidence': 0,
                'analysis_method': 'ERROR_FALLBACK'
            },
            'recommendations': [f'Error occurred during analysis: {error_message}'],
            'error': True,
            'error_message': error_message
        }

    def process_uploaded_file_with_ai(self, uploaded_file) -> Optional[Dict]:
        """
        Process uploaded file using AI analysis with fallback to rule-based analysis.
        Refactored to reduce deep nesting and improve maintainability.
        """
        start_time = time.time()
        analysis_type = "UNKNOWN"
        
        try:
            # Step 1: Read and validate file
            df = self._read_and_validate_file(uploaded_file)
            if df is None:
                return self._create_error_response("File reading failed")
            
            ai_logger.debug(f"File read successfully: {df.shape[0]} rows, {df.shape[1]} columns")
            
            # Step 2: Extract data and prepare for analysis
            analysis_data = self._extract_analysis_data(df)
            if not analysis_data:
                return self._create_error_response("No valid data found")
                
            ai_logger.info(f"📊 Preprocessed {len(analysis_data['raw_comments'])} raw → {len(analysis_data['comments'])} unique comments")
            
            # Step 3: Attempt AI analysis with fallback
            ai_results = self._attempt_ai_analysis(analysis_data['comments'])
            
            # Step 4: Process results based on AI success/failure
            if ai_results:
                ai_logger.info("✅ AI analysis successful - proceeding with format conversion")
                analysis_type = "AI_POWERED"
                result = self._process_ai_results(ai_results, analysis_data, uploaded_file)
                return result
            else:
                ai_logger.warning("❌ AI analysis failed - executing rule-based fallback")
                analysis_type = "RULE_BASED_FALLBACK"
                result = self._fallback_to_rule_based_analysis(
                    analysis_data['comments'], analysis_data['comment_frequencies'],
                    uploaded_file, analysis_data['raw_comments'], analysis_data['nps_data'],
                    analysis_data['nota_data'], analysis_data['has_nps'], analysis_data['has_nota']
                )
                return result
                
        except Exception as e:
            duration = time.time() - start_time
            ai_logger.error(f"💥 Analysis failed completely: {str(e)} | Duration: {duration:.2f}s")
            ai_logger.error(f"Error occurred at analysis_type: {analysis_type}")
            ai_logger.debug(f"Full error traceback: {traceback.format_exc()}")
            
            # Log diagnostic information
            try:
                ai_logger.debug(f"File name: {uploaded_file.name if hasattr(uploaded_file, 'name') else 'Unknown'}")
                ai_logger.debug(f"File size: {uploaded_file.size if hasattr(uploaded_file, 'size') else 'Unknown'}")
                ai_logger.debug(f"AI available: {self.ai_available}")
            except:
                pass
            
            return self._create_error_response(f"Critical analysis failure: {str(e)}")
        finally:
            duration = time.time() - start_time
            ai_logger.info(f"🏁 Analysis completed | Type: {analysis_type} | Duration: {duration:.2f}s")
    
    def _try_ai_analysis(self, comments: List[str]) -> Optional[List[Dict]]:
        """
        Attempt AI analysis with comprehensive error handling
        Returns None if AI analysis fails for any reason
        """
        try:
            ai_logger.info(f"📡 Calling OpenAI API for {len(comments)} comments...")
            start_time = time.time()
            
            # Validate input
            if not comments:
                ai_logger.error("No comments provided for AI analysis")
                return None
                
            valid_comments = [c for c in comments if c and c.strip()]
            if len(valid_comments) != len(comments):
                ai_logger.warning(f"Filtered {len(comments) - len(valid_comments)} empty/invalid comments")
            
            # Call OpenAI analyzer with timeout
            ai_logger.debug(f"Making API call with model: {self.openai_analyzer.model}")
            ai_results = self.openai_analyzer.analyze_comments_batch(valid_comments)
            
            duration = time.time() - start_time
            ai_logger.info(f"✅ OpenAI API successful | Duration: {duration:.2f}s | Results: {len(ai_results) if ai_results else 0}")
            
            # Validate results structure
            if not ai_results:
                ai_logger.error("OpenAI returned empty results")
                return None
                
            if len(ai_results) != len(valid_comments):
                ai_logger.error(f"Result count mismatch: got {len(ai_results)}, expected {len(valid_comments)}")
                return None
            
            # Enhanced validation - check ALL results, not just first 3
            required_fields = ['sentiment', 'confidence', 'themes', 'emotions']
            invalid_count = 0
            total_results = len(ai_results)
            
            for i, result in enumerate(ai_results):
                if not isinstance(result, dict):
                    ai_logger.error(f"Invalid result type at index {i}: {type(result)}")
                    invalid_count += 1
                    continue
                    
                missing_fields = [field for field in required_fields if field not in result or result[field] is None]
                if missing_fields:
                    ai_logger.warning(f"Result {i+1}/{total_results} missing fields: {missing_fields}")
                    invalid_count += 1
            
            # If >10% of results are invalid, force fallback to rule-based
            invalid_percentage = (invalid_count / total_results) * 100 if total_results > 0 else 100
            if invalid_percentage > 10:
                ai_logger.error(f"Too many invalid results: {invalid_count}/{total_results} ({invalid_percentage:.1f}%)")
                ai_logger.error("Forcing fallback to rule-based analysis")
                return None
            elif invalid_count > 0:
                ai_logger.warning(f"Found {invalid_count}/{total_results} invalid results, but continuing...")
            
            ai_logger.info(f"✅ AI results validation passed: {total_results - invalid_count}/{total_results} valid")
            ai_logger.debug(f"Sample result: {ai_results[0] if ai_results else 'None'}")
            return ai_results
            
        except ImportError as e:
            ai_logger.error(f"OpenAI import error: {str(e)}")
            return None
        except ConnectionError as e:
            ai_logger.error(f"OpenAI connection error: {str(e)}")
            return None
        except TimeoutError as e:
            ai_logger.error(f"OpenAI timeout error: {str(e)}")
            return None
        except Exception as e:
            ai_logger.error(f"OpenAI analysis failed: {str(e)}")
            ai_logger.debug(f"AI analysis error traceback: {traceback.format_exc()}")
            return None
    
    def _convert_ai_results_to_expected_format(self, ai_results: List[Dict], comments: List[str], 
                                            comment_frequencies: List[int], uploaded_file,
                                            raw_comments: List[str], nps_data: List, nota_data: List,
                                            has_nps: bool, has_nota: bool) -> Dict:
        """
        Convert OpenAI results to the exact format expected by the existing system
        """
        logger.info("[AI_PIPELINE] Converting AI results to expected format")
        
        # Convert AI sentiments to expected Spanish format
        sentiments = []
        for result in ai_results:
            ai_sentiment = result.get('sentiment', 'neutral')
            # Convert to Spanish format expected by existing system
            if ai_sentiment == 'positive':
                sentiments.append('positivo')
            elif ai_sentiment == 'negative':
                sentiments.append('negativo')
            else:
                sentiments.append('neutral')
        
        # Convert AI results to enhanced_results format
        enhanced_results = []
        churn_risks = []
        urgency_levels = []
        emotion_analysis = []
        competitor_mentions = []
        customer_segments = []
        
        for i, (comment, ai_result) in enumerate(zip(comments, ai_results)):
            # Convert AI emotions to expected format
            ai_emotions = ai_result.get('emotions', ['neutral'])
            emotions_formatted = {
                'intensity': self._calculate_emotion_intensity(ai_emotions, ai_result.get('confidence', 0.5)),
                'dominant': ai_emotions[0] if ai_emotions else 'neutral',
                'detected': ai_emotions
            }
            emotion_analysis.append(emotions_formatted)
            
            # Convert AI themes to extended_themes format
            ai_themes = ai_result.get('themes', [])
            extended_themes = self._convert_themes_to_extended_format(ai_themes)
            
            # Convert AI pain points to churn risk
            ai_pain_points = ai_result.get('pain_points', [])
            churn_risk = self._convert_pain_points_to_churn_risk(ai_pain_points, ai_result.get('confidence', 0.5))
            churn_risks.append(churn_risk)
            
            # Determine urgency from sentiment and pain points
            urgency = self._determine_urgency_from_ai(ai_result)
            urgency_levels.append(urgency)
            
            # Detect competitors (use existing logic as fallback, enhance with AI themes)
            competitors = self._detect_competitors_from_ai_themes(ai_themes)
            competitor_mentions.append(competitors)
            
            # Determine customer value (use AI confidence as proxy)
            customer_value = self._determine_customer_value_from_ai(ai_result)
            customer_segments.append(customer_value)
            
            # Create enhanced result in expected format
            enhanced_result = {
                'emotions': emotions_formatted,
                'extended_themes': extended_themes,
                'churn_risk': churn_risk,
                'competitors': competitors,
                'urgency': urgency,
                'customer_value': customer_value
            }
            enhanced_results.append(enhanced_result)
        
        # Create improved_results using AI data
        improved_results = []
        comment_quality = []
        service_issues = []
        
        for i, (comment, ai_result) in enumerate(zip(comments, ai_results)):
            # Convert AI analysis to quality assessment
            quality = self._convert_ai_to_quality_assessment(ai_result, comment)
            comment_quality.append(quality)
            
            # Convert AI themes to service issues
            issues = self._convert_ai_themes_to_service_issues(ai_result.get('themes', []), ai_result.get('pain_points', []))
            service_issues.append(issues)
            
            # Enhanced sentiment analysis
            nota = nota_data[i] if has_nota and i < len(nota_data) else None
            enhanced_sentiment = self._create_enhanced_sentiment_from_ai(ai_result, nota)
            
            improved_result = {
                'quality': quality,
                'themes': self._convert_ai_themes_to_improved_format(ai_result.get('themes', [])),
                'issues': issues,
                'enhanced_sentiment': enhanced_sentiment
            }
            improved_results.append(improved_result)
        
        # Calculate all statistics using converted data (identical to original logic)
        total = len(comments)
        sentiment_counts = Counter(sentiments)
        
        positive_pct = (sentiment_counts['positivo'] / total * 100) if total > 0 else 0
        neutral_pct = (sentiment_counts['neutral'] / total * 100) if total > 0 else 0
        negative_pct = (sentiment_counts['negativo'] / total * 100) if total > 0 else 0
        
        # Extract themes from AI results
        theme_counts, theme_examples = self._extract_themes_from_ai_results(ai_results, comments)
        
        # Calculate enhanced metrics
        high_churn_count = sum(1 for r in churn_risks if r['risk_level'] == 'high')
        medium_churn_count = sum(1 for r in churn_risks if r['risk_level'] == 'medium')
        
        urgency_distribution = Counter(urgency_levels)
        
        # Calculate NPS (inline logic to avoid dependency issues)
        if has_nps and nps_data:
            # Simple inline NPS calculation
            nps_scores = [score for score in nps_data[:len(comments)] if pd.notna(score)]
            if nps_scores:
                promoters = sum(1 for score in nps_scores if score >= 9)
                detractors = sum(1 for score in nps_scores if score <= 6)
                passives = sum(1 for score in nps_scores if 7 <= score <= 8)
                nps = ((promoters - detractors) / len(nps_scores)) * 100
            else:
                promoters = detractors = passives = nps = 0
        else:
            # Calculate NPS from AI-enhanced sentiment
            nps_scores = []
            for result in enhanced_results:
                intensity = result['emotions']['intensity']
                sentiment = sentiments[len(nps_scores)]  # Get corresponding sentiment
                nps_score = self.enhanced_analyzer.calculate_nps_from_sentiment(sentiment, intensity)
                nps_scores.append(nps_score)
            
            promoters = sum(1 for score in nps_scores if score >= 9)
            passives = sum(1 for score in nps_scores if 7 <= score < 9)
            detractors = sum(1 for score in nps_scores if score < 7)
            nps = ((promoters - detractors) / len(nps_scores)) * 100 if nps_scores else 0
        
        # Calculate other metrics using AI-enhanced data
        total_competitor_mentions = sum(len(comp) for comp in competitor_mentions)
        
        # Debug emotion analysis
        logger.debug(f"[AI_PIPELINE] Emotion analysis count: {len(emotion_analysis)}")
        if emotion_analysis:
            logger.debug(f"[AI_PIPELINE] Sample emotion: {emotion_analysis[0]}")
        
        dominant_emotions = Counter([ea['dominant'] for ea in emotion_analysis])
        avg_intensity = np.mean([ea['intensity'] for ea in emotion_analysis]) if emotion_analysis else 0
        
        logger.debug(f"[AI_PIPELINE] Dominant emotions: {dict(dominant_emotions)}")
        logger.debug(f"[AI_PIPELINE] Avg intensity: {avg_intensity}")
        
        # Calculate additional metrics
        avg_rating = np.mean([r for r in nota_data[:len(comments)] if pd.notna(r)]) if has_nota else 0
        
        # Generate satisfaction trend and alerts using AI data
        satisfaction_trend = self._generate_ai_satisfaction_trend(ai_results)
        alerts = self._generate_ai_alerts(urgency_distribution, total_competitor_mentions, total)
        
        # CSI analysis using AI insights
        csi_analysis = self._generate_ai_csi_analysis(ai_results)
        
        # Calculate file statistics
        file_size_kb = uploaded_file.size / 1024
        avg_length = np.mean([len(str(c)) for c in comments]) if comments else 0
        
        logger.info(f"[AI_PIPELINE] Format conversion completed | Sentiments: {dict(sentiment_counts)} | NPS: {nps:.1f}")
        
        # Return in EXACT same format as original process_uploaded_file()
        return {
            'total': total,
            'positive_pct': round(positive_pct, 1),
            'neutral_pct': round(neutral_pct, 1), 
            'negative_pct': round(negative_pct, 1),
            'positive_count': sentiment_counts['positivo'],
            'neutral_count': sentiment_counts['neutral'],
            'negative_count': sentiment_counts['negativo'],
            # Add sentiment_percentages format expected by UI
            'sentiment_percentages': {
                'positivo': round(positive_pct, 1),
                'negativo': round(negative_pct, 1),
                'neutral': round(neutral_pct, 1)
            },
            'theme_counts': theme_counts,
            'theme_examples': theme_examples,
            'file_size': round(file_size_kb, 1),
            'avg_length': round(avg_length),
            'comments': comments,
            'sentiments': sentiments,
            'comment_frequencies': comment_frequencies,
            'original_filename': uploaded_file.name,
            'analysis_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'raw_total': len(raw_comments),
            'duplicates_removed': len(raw_comments) - len(comments),
            'cleaning_applied': True,
            # Enhanced analysis results (AI-powered)
            'enhanced_results': enhanced_results,
            'churn_analysis': {
                'high_risk': high_churn_count,
                'medium_risk': medium_churn_count,
                'low_risk': total - high_churn_count - medium_churn_count,
                'details': churn_risks
            },
            'urgency_distribution': dict(urgency_distribution),
            'nps': {
                'score': round(nps, 1),
                'promoters': promoters,
                'detractors': detractors,
                'passives': passives,
                'has_real_nps': has_nps
            },
            'rating_data': {
                'average': round(avg_rating, 1) if avg_rating else 0,
                'has_ratings': has_nota,
                'ratings': nota_data[:len(comments)] if has_nota else []
            },
            'nps_categories': nps_data[:len(comments)] if has_nps else [],
            'competitor_analysis': {
                'total_mentions': total_competitor_mentions,
                'percentage': round((total_competitor_mentions / total * 100), 1) if total > 0 else 0,
                'details': competitor_mentions
            },
            'emotion_summary': {
                'distribution': dict(dominant_emotions),
                'avg_intensity': round(avg_intensity, 1)
            },
            'customer_segments': customer_segments,
            'satisfaction_trend': satisfaction_trend,
            'alerts': alerts,
            'improved_results': improved_results,
            'comment_quality_summary': Counter([q['quality'] for q in comment_quality]),
            'informative_comments': sum(1 for q in comment_quality if q['informative']),
            'service_issues_summary': Counter([i['severity'] for i in service_issues]),
            'csi_analysis': csi_analysis,
            'insights': self._generate_ai_insights(ai_results, has_nps, nps if has_nps else None),
            # Add AI-specific metadata
            'analysis_method': 'AI_POWERED',
            'ai_model_used': self.openai_analyzer.model if self.openai_analyzer else None,
            'ai_confidence_avg': np.mean([r.get('confidence', 0.5) for r in ai_results]) if ai_results else 0
        }
    
    def _fallback_to_rule_based_analysis(self, comments: List[str], comment_frequencies: List[int], 
                                       uploaded_file, raw_comments: List[str], nps_data: List, 
                                       nota_data: List, has_nps: bool, has_nota: bool) -> Dict:
        """
        Fallback to original rule-based analysis when AI fails
        """
        logger.info("[AI_PIPELINE] Executing rule-based fallback analysis")
        
        # Import and use original analysis function
        # Import from correct locations (src.main is disabled)
        try:
            from shared.business.analysis_engine import analyze_sentiment_simple, extract_themes_simple as extract_themes
        except ImportError:
            # Fallback implementations
            def analyze_sentiment_simple(text):
                if not text:
                    return 'neutral'
                text_lower = str(text).lower()
                positive_words = ['excelente', 'bueno', 'perfecto', 'satisfecho', 'genial']
                negative_words = ['malo', 'terrible', 'pésimo', 'frustrado', 'molesto']
                
                pos_count = sum(1 for word in positive_words if word in text_lower)
                neg_count = sum(1 for word in negative_words if word in text_lower)
                
                if pos_count > neg_count:
                    return 'positivo'
                elif neg_count > pos_count:
                    return 'negativo'
                else:
                    return 'neutral'
            
            def extract_themes(comments):
                themes = {'servicio': 0, 'precio': 0, 'velocidad': 0, 'calidad': 0}
                examples = {}
                for comment in comments:
                    comment_lower = str(comment).lower()
                    if any(word in comment_lower for word in ['servicio', 'atención']):
                        themes['servicio'] += 1
                return themes, examples
        
        # Perform rule-based analysis (identical to original)
        sentiments = [analyze_sentiment_simple(comment) for comment in comments]
        
        # Perform enhanced and improved analysis on each comment (identical to original)
        enhanced_results = []
        churn_risks = []
        urgency_levels = []
        emotion_analysis = []
        competitor_mentions = []
        customer_segments = []
        nps_scores = []
        improved_results = []
        comment_quality = []
        service_issues = []
        
        for i, comment in enumerate(comments):
            # Enhanced analysis (identical to original)
            analysis = self.enhanced_analyzer.full_analysis(comment)
            enhanced_results.append(analysis)
            
            # Extract key metrics (identical to original)
            churn_risks.append(analysis['churn_risk'])
            urgency_levels.append(analysis['urgency'])
            emotion_analysis.append(analysis['emotions'])
            competitor_mentions.append(analysis['competitors'])
            customer_segments.append(analysis['customer_value'])
            
            # Calculate NPS (identical to original)
            intensity = analysis['emotions']['intensity']
            nps_score = self.enhanced_analyzer.calculate_nps_from_sentiment(sentiments[i], intensity)
            nps_scores.append(nps_score)
            
            # Improved analysis (identical to original)
            quality = self.improved_analyzer.analyze_comment_quality(comment)
            comment_quality.append(quality)
            
            themes = self.improved_analyzer.detect_themes_improved(comment)
            issues = self.improved_analyzer.analyze_service_issues(comment)
            service_issues.append(issues)
            
            # Enhanced sentiment with rating if available (identical to original)
            nota = nota_data[i] if has_nota and i < len(nota_data) else None
            enhanced_sentiment = self.improved_analyzer.enhanced_sentiment_analysis(comment, nota)
            
            improved_results.append({
                'quality': quality,
                'themes': themes,
                'issues': issues,
                'enhanced_sentiment': enhanced_sentiment
            })
        
        # All remaining calculations identical to original process_uploaded_file()
        total = len(comments)
        sentiment_counts = Counter(sentiments)
        
        positive_pct = (sentiment_counts['positivo'] / total * 100) if total > 0 else 0
        neutral_pct = (sentiment_counts['neutral'] / total * 100) if total > 0 else 0
        negative_pct = (sentiment_counts['negativo'] / total * 100) if total > 0 else 0
        
        theme_counts, theme_examples = extract_themes(comments)
        
        # Calculate enhanced metrics
        high_churn_count = sum(1 for r in churn_risks if r['risk_level'] == 'high')
        medium_churn_count = sum(1 for r in churn_risks if r['risk_level'] == 'medium')
        
        urgency_distribution = Counter(urgency_levels)
        
        # Calculate NPS
        if has_nps and nps_data:
            # Simple inline NPS calculation (fallback version)
            nps_scores = [score for score in nps_data[:len(comments)] if pd.notna(score)]
            if nps_scores:
                promoters = sum(1 for score in nps_scores if score >= 9)
                detractors = sum(1 for score in nps_scores if score <= 6)
                passives = sum(1 for score in nps_scores if 7 <= score <= 8)
                nps = ((promoters - detractors) / len(nps_scores)) * 100
            else:
                promoters = detractors = passives = nps = 0
        else:
            promoters = sum(1 for score in nps_scores if score >= 9)
            passives = sum(1 for score in nps_scores if 7 <= score < 9)
            detractors = sum(1 for score in nps_scores if score < 7)
            nps = ((promoters - detractors) / len(nps_scores)) * 100 if nps_scores else 0
        
        # Calculate other metrics
        total_competitor_mentions = sum(len(comp) for comp in competitor_mentions)
        dominant_emotions = Counter([ea.get('dominant', 'neutral') for ea in emotion_analysis])
        avg_intensity = np.mean([ea.get('intensity', 1.0) for ea in emotion_analysis]) if emotion_analysis else 0
        avg_rating = np.mean([r for r in nota_data[:len(comments)] if pd.notna(r)]) if has_nota else 0
        
        # Generate satisfaction trend and alerts
        satisfaction_trend = {
            'trend': 'stable',
            'score': round(positive_pct - negative_pct, 1),
            'indicators': []
        }
        
        alerts = []
        if urgency_distribution.get('P0', 0) > 0:
            alerts.append({
                'severity': 'critical',
                'message': f'{urgency_distribution["P0"]} casos críticos sin servicio',
                'action': 'Respuesta técnica inmediata'
            })
        
        if total_competitor_mentions > total * 0.15:
            alerts.append({
                'severity': 'medium',
                'message': f'Competidores mencionados en {(total_competitor_mentions/total*100):.1f}% de comentarios',
                'action': 'Análisis competitivo requerido'
            })
        
        # CSI analysis
        csi_analysis = {
            'overall_score': round((positive_pct - negative_pct + 100) / 2, 1),
            'factors': {
                'sentiment_balance': round(positive_pct - negative_pct, 1),
                'engagement_level': round(avg_intensity, 1) if avg_intensity else 0
            }
        }
        
        # Calculate file statistics
        file_size_kb = uploaded_file.size / 1024
        avg_length = np.mean([len(str(c)) for c in comments]) if comments else 0
        
        # Return in exact same format but mark as rule-based fallback
        result = {
            'total': total,
            'positive_pct': round(positive_pct, 1),
            'neutral_pct': round(neutral_pct, 1),
            'negative_pct': round(negative_pct, 1),
            'positive_count': sentiment_counts['positivo'],
            'neutral_count': sentiment_counts['neutral'],
            'negative_count': sentiment_counts['negativo'],
            'theme_counts': theme_counts,
            'theme_examples': theme_examples,
            'file_size': round(file_size_kb, 1),
            'avg_length': round(avg_length),
            'comments': comments,
            'sentiments': sentiments,
            'comment_frequencies': comment_frequencies,
            'original_filename': uploaded_file.name,
            'analysis_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'raw_total': len(raw_comments),
            'duplicates_removed': len(raw_comments) - len(comments),
            'cleaning_applied': True,
            'enhanced_results': enhanced_results,
            'churn_analysis': {
                'high_risk': high_churn_count,
                'medium_risk': medium_churn_count,
                'low_risk': total - high_churn_count - medium_churn_count,
                'details': churn_risks
            },
            'urgency_distribution': dict(urgency_distribution),
            'nps': {
                'score': round(nps, 1),
                'promoters': promoters,
                'detractors': detractors,
                'passives': passives,
                'has_real_nps': has_nps
            },
            'rating_data': {
                'average': round(avg_rating, 1) if avg_rating else 0,
                'has_ratings': has_nota,
                'ratings': nota_data[:len(comments)] if has_nota else []
            },
            'nps_categories': nps_data[:len(comments)] if has_nps else [],
            'competitor_analysis': {
                'total_mentions': total_competitor_mentions,
                'percentage': round((total_competitor_mentions / total * 100), 1) if total > 0 else 0,
                'details': competitor_mentions
            },
            'emotion_summary': {
                'distribution': dict(dominant_emotions),
                'avg_intensity': round(avg_intensity, 1)
            },
            'customer_segments': customer_segments,
            'satisfaction_trend': satisfaction_trend,
            'alerts': alerts,
            'improved_results': improved_results,
            'comment_quality_summary': Counter([q['quality'] for q in comment_quality]),
            'informative_comments': sum(1 for q in comment_quality if q['informative']),
            'service_issues_summary': Counter([i['severity'] for i in service_issues]),
            'csi_analysis': csi_analysis,
            'insights': self.improved_analyzer.generate_insights({
                'nps': {'nps_score': nps} if has_nps else None,
                'service_issues': service_issues
            }),
            # Mark as fallback
            'analysis_method': 'RULE_BASED_FALLBACK',
            'ai_model_used': None,
            'ai_confidence_avg': 0
        }
        
        # CRITICAL MICRO-FIX: Clean up all accumulated lists before return
        try:
            del enhanced_results, churn_risks, urgency_levels, emotion_analysis
            del competitor_mentions, customer_segments, nps_scores, improved_results
            del comment_quality, service_issues, sentiments, comments
            del raw_comments, comment_frequencies
        except:
            pass  # Silent cleanup
        
        logger.info(f"[AI_PIPELINE] Rule-based fallback completed | Sentiments: {dict(sentiment_counts)}")
        return result
    
    # Helper methods for AI to existing format conversion
    def _calculate_emotion_intensity(self, ai_emotions: List[str], confidence: float) -> float:
        """Calculate emotion intensity from AI emotions and confidence"""
        intensity_map = {
            'frustración': 2.0, 'enojo': 2.5, 'ira': 2.5,
            'satisfacción': 1.8, 'alegría': 1.5, 'felicidad': 1.5,
            'preocupación': 1.2, 'inquietud': 1.0,
            'decepción': 1.8, 'tristeza': 1.5,
            'esperanza': 1.0, 'optimismo': 1.2,
            'neutral': 1.0
        }
        
        if not ai_emotions:
            return 1.0
            
        # Get intensity for dominant emotion
        dominant = ai_emotions[0].lower()
        base_intensity = intensity_map.get(dominant, 1.0)
        
        # Adjust by confidence
        return base_intensity * confidence
    
    def _convert_themes_to_extended_format(self, ai_themes: List[str]) -> Dict:
        """Convert AI themes to extended_themes format expected by existing system"""
        # Map AI themes to existing theme structure
        theme_mapping = {
            'precio': ['precio', 'costo', 'caro', 'barato'],
            'velocidad': ['lento', 'rápido', 'velocidad', 'conexion'],
            'calidad_servicio': ['servicio', 'calidad', 'atencion'],
            'soporte_tecnico': ['soporte', 'tecnico', 'ayuda', 'asistencia'],
            'cobertura': ['cobertura', 'señal', 'area'],
            'facturacion': ['factura', 'cobro', 'pago'],
        }
        
        detected_themes = {}
        for ai_theme in ai_themes:
            ai_theme_lower = ai_theme.lower()
            for existing_theme, keywords in theme_mapping.items():
                if any(keyword in ai_theme_lower for keyword in keywords):
                    if existing_theme not in detected_themes:
                        detected_themes[existing_theme] = {}
                    detected_themes[existing_theme][ai_theme] = True
        
        return detected_themes
    
    def _convert_pain_points_to_churn_risk(self, pain_points: List[str], confidence: float) -> Dict:
        """Convert AI pain points to churn risk assessment"""
        high_churn_indicators = ['cancelar', 'cambiar', 'competencia', 'dejar', 'horrible', 'pesimo']
        medium_churn_indicators = ['problema', 'lento', 'caro', 'mal servicio', 'no funciona']
        
        risk_score = 0
        risk_indicators = []
        
        for pain_point in pain_points:
            pain_lower = pain_point.lower()
            if any(indicator in pain_lower for indicator in high_churn_indicators):
                risk_score += 3
                risk_indicators.append(pain_point)
            elif any(indicator in pain_lower for indicator in medium_churn_indicators):
                risk_score += 2
                risk_indicators.append(pain_point)
        
        # Adjust by confidence
        risk_score = risk_score * confidence
        
        if risk_score >= 5:
            risk_level = 'high'
        elif risk_score >= 2:
            risk_level = 'medium'
        else:
            risk_level = 'low'
        
        return {
            'risk_level': risk_level,
            'score': min(risk_score, 10),
            'indicators': risk_indicators[:3],  # Top 3 indicators
            'factors': pain_points
        }
    
    def _determine_urgency_from_ai(self, ai_result: Dict) -> str:
        """Determine urgency level from AI analysis"""
        sentiment = ai_result.get('sentiment', 'neutral')
        pain_points = ai_result.get('pain_points', [])
        confidence = ai_result.get('confidence', 0.5)
        
        # Critical urgency indicators
        critical_indicators = ['sin servicio', 'no funciona', 'cortado', 'emergencia']
        high_indicators = ['muy lento', 'problema grave', 'urgente']
        
        urgency_score = 0
        
        if sentiment == 'negative' and confidence > 0.8:
            urgency_score += 2
        
        for pain_point in pain_points:
            pain_lower = pain_point.lower()
            if any(indicator in pain_lower for indicator in critical_indicators):
                urgency_score += 4
            elif any(indicator in pain_lower for indicator in high_indicators):
                urgency_score += 2
        
        if urgency_score >= 6:
            return 'P0'  # Critical
        elif urgency_score >= 4:
            return 'P1'  # High
        elif urgency_score >= 2:
            return 'P2'  # Medium
        else:
            return 'P3'  # Low
    
    def _detect_competitors_from_ai_themes(self, ai_themes: List[str]) -> List[str]:
        """Detect competitor mentions from AI themes"""
        competitors = ['tigo', 'claro', 'copaco', 'vox', 'telecel']
        detected = []
        
        for theme in ai_themes:
            theme_lower = theme.lower()
            for competitor in competitors:
                if competitor in theme_lower and competitor not in detected:
                    detected.append(competitor)
        
        return detected
    
    def _determine_customer_value_from_ai(self, ai_result: Dict) -> str:
        """Determine customer value segment from AI analysis"""
        confidence = ai_result.get('confidence', 0.5)
        themes = ai_result.get('themes', [])
        
        # High-value indicators
        high_value_themes = ['empresarial', 'corporativo', 'negocio', 'oficina']
        
        if any(theme.lower() in ' '.join(themes).lower() for theme in high_value_themes):
            return 'high_value'
        elif confidence > 0.8:  # Detailed, confident feedback suggests engaged customer
            return 'medium_value'
        else:
            return 'standard'
    
    def _convert_ai_to_quality_assessment(self, ai_result: Dict, comment: str) -> Dict:
        """Convert AI analysis to comment quality assessment"""
        confidence = ai_result.get('confidence', 0.5)
        themes = ai_result.get('themes', [])
        
        # Determine quality based on AI confidence and detail
        if confidence > 0.8 and len(themes) > 2:
            quality = 'high'
        elif confidence > 0.6 and len(themes) > 1:
            quality = 'medium'
        else:
            quality = 'low'
        
        return {
            'quality': quality,
            'informative': len(themes) > 1,
            'detail_level': 'high' if len(comment) > 100 else 'medium' if len(comment) > 50 else 'low',
            'confidence': confidence
        }
    
    def _convert_ai_themes_to_service_issues(self, themes: List[str], pain_points: List[str]) -> Dict:
        """Convert AI themes and pain points to service issues format"""
        severity_score = 0
        
        # High severity indicators
        high_severity = ['sin servicio', 'no funciona', 'cortado']
        medium_severity = ['lento', 'problema', 'falla']
        
        for pain_point in pain_points:
            pain_lower = pain_point.lower()
            if any(indicator in pain_lower for indicator in high_severity):
                severity_score += 3
            elif any(indicator in pain_lower for indicator in medium_severity):
                severity_score += 2
        
        if severity_score >= 5:
            severity = 'critical'
        elif severity_score >= 3:
            severity = 'high'
        elif severity_score >= 1:
            severity = 'medium'
        else:
            severity = 'low'
        
        return {
            'severity': severity,
            'categories': themes[:3],  # Top 3 themes
            'pain_points': pain_points[:3],  # Top 3 pain points
            'score': min(severity_score, 10)
        }
    
    def _create_enhanced_sentiment_from_ai(self, ai_result: Dict, nota: Optional[float]) -> Dict:
        """Create enhanced sentiment analysis from AI results"""
        ai_sentiment = ai_result.get('sentiment', 'neutral')
        confidence = ai_result.get('confidence', 0.5)
        
        # Convert to Spanish
        sentiment_es = 'positivo' if ai_sentiment == 'positive' else ('negativo' if ai_sentiment == 'negative' else 'neutral')
        
        return {
            'sentiment': sentiment_es,
            'confidence': confidence,
            'rating_alignment': nota is not None,
            'rating_value': nota,
            'ai_enhanced': True
        }
    
    def _convert_ai_themes_to_improved_format(self, ai_themes: List[str]) -> Dict:
        """Convert AI themes to improved analysis format"""
        return {theme: True for theme in ai_themes[:5]}  # Top 5 themes
    
    def _extract_themes_from_ai_results(self, ai_results: List[Dict], comments: List[str]) -> tuple:
        """Extract themes and examples from AI results"""
        theme_counts = defaultdict(int)
        theme_examples = defaultdict(list)
        
        for ai_result, comment in zip(ai_results, comments):
            themes = ai_result.get('themes', [])
            for theme in themes:
                theme_counts[theme] += 1
                if len(theme_examples[theme]) < 3:  # Keep top 3 examples
                    theme_examples[theme].append(comment[:100])  # First 100 characters
        
        return dict(theme_counts), dict(theme_examples)
    
    def _generate_ai_satisfaction_trend(self, ai_results: List[Dict]) -> Dict:
        """Generate satisfaction trend from AI results"""
        sentiments = [r.get('sentiment', 'neutral') for r in ai_results]
        confidences = [r.get('confidence', 0.5) for r in ai_results]
        
        positive_count = sum(1 for s in sentiments if s == 'positive')
        negative_count = sum(1 for s in sentiments if s == 'negative')
        avg_confidence = np.mean(confidences)
        
        score = ((positive_count - negative_count) / len(ai_results)) * 100
        
        if score > 20:
            trend = 'improving'
        elif score < -20:
            trend = 'declining'
        else:
            trend = 'stable'
        
        return {
            'trend': trend,
            'score': round(score, 1),
            'confidence': round(avg_confidence * 100, 1),
            'indicators': [f"AI confidence: {avg_confidence:.2f}"]
        }
    
    def _generate_ai_alerts(self, urgency_distribution: Counter, total_competitor_mentions: int, total: int) -> List[Dict]:
        """Generate alerts based on AI analysis"""
        alerts = []
        
        if urgency_distribution.get('P0', 0) > 0:
            alerts.append({
                'severity': 'critical',
                'message': f'{urgency_distribution["P0"]} casos críticos detectados por IA',
                'action': 'Respuesta técnica inmediata'
            })
        
        if total_competitor_mentions > total * 0.15:
            alerts.append({
                'severity': 'medium',
                'message': f'IA detectó competidores en {(total_competitor_mentions/total*100):.1f}% de comentarios',
                'action': 'Análisis competitivo requerido'
            })
        
        return alerts
    
    def _generate_ai_csi_analysis(self, ai_results: List[Dict]) -> Dict:
        """Generate CSI analysis from AI results"""
        sentiments = [r.get('sentiment', 'neutral') for r in ai_results]
        confidences = [r.get('confidence', 0.5) for r in ai_results]
        
        positive_count = sum(1 for s in sentiments if s == 'positive')
        negative_count = sum(1 for s in sentiments if s == 'negative')
        
        sentiment_balance = ((positive_count - negative_count) / len(ai_results)) * 100
        avg_confidence = np.mean(confidences) * 100
        
        overall_score = (sentiment_balance + 100) / 2  # Normalize to 0-100
        
        return {
            'overall_score': round(overall_score, 1),
            'factors': {
                'ai_sentiment_balance': round(sentiment_balance, 1),
                'ai_confidence_level': round(avg_confidence, 1),
                'data_quality': 'high' if avg_confidence > 70 else 'medium'
            },
            'ai_enhanced': True
        }
    
    def _generate_ai_insights(self, ai_results: List[Dict], has_nps: bool, nps_score: Optional[float]) -> Dict:
        """Generate insights from AI analysis results"""
        themes = []
        pain_points = []
        languages = []
        
        for result in ai_results:
            themes.extend(result.get('themes', []))
            pain_points.extend(result.get('pain_points', []))
            languages.append(result.get('language', 'es'))
        
        theme_counts = Counter(themes)
        pain_point_counts = Counter(pain_points)
        language_counts = Counter(languages)
        
        insights = {
            'top_themes': dict(theme_counts.most_common(5)),
            'main_pain_points': dict(pain_point_counts.most_common(5)),
            'language_distribution': dict(language_counts),
            'ai_powered': True,
            'analysis_quality': 'high'
        }
        
        if has_nps and nps_score is not None:
            insights['nps_correlation'] = {
                'nps_score': nps_score,
                'ai_enhanced': True
            }
        
        return insights
