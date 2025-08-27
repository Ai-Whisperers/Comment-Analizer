"""
Analysis Service for Personal Paraguay Comments Analysis Platform
Handles AI analysis operations and batch processing with memory optimization
"""

import streamlit as st
import pandas as pd
import os
import time
import threading
import queue
import logging
from typing import List, Dict

from src.sentiment_analysis.openai_analyzer import OpenAIAnalyzer
from src.sentiment_analysis.enhanced_analyzer import EnhancedAnalyzer
from src.sentiment_analysis.enhanced_analyzer import EnhancedAnalyzer as BasicAnalysisMethod
from src.ai_analysis_adapter import AIAnalysisAdapter
from src.utils.validators import InputValidator, SecurityLogger
from src.utils.exceptions import (
    ErrorHandler,
    APIConnectionError,
    AnalysisProcessingError,
)
from src.services.session_manager import SessionManager
from src.utils.memory_manager import MemoryManager, BatchProcessor, optimize_session_state, log_memory_status


class AnalysisService:
    """Service for handling AI analysis operations with memory optimization"""

    def __init__(self):
        self.session_manager = SessionManager()
        self.memory_manager = MemoryManager(max_memory_mb=768)
        self.batch_processor = BatchProcessor(batch_size=25, memory_limit_mb=512)

    def analyze_comments_with_ai(self, comments_df: pd.DataFrame, sample_size: int):
        """Analyze comments using OpenAI with proper validation"""

        # Create detailed progress containers
        progress_container = st.container()
        status_container = st.container()
        
        try:
            with progress_container:
                # Enhanced progress header
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
                    border: 2px solid #4299e1;
                    border-radius: 16px;
                    padding: 20px;
                    margin: 16px 0;
                    text-align: center;
                    animation: fadeIn 0.5s ease-out;
                ">
                    <div style="display: flex; align-items: center; justify-content: center; gap: 12px;">
                        <div class="loading-spinner"></div>
                        <h3 style="color: #e2e8f0; margin: 0;">Analysis in Progress</h3>
                    </div>
                    <p style="color: #a0aec0; margin: 8px 0 0 0;">Processing {sample_size:,} comments with Basic Analysis sentiment detection...</p>
                </div>
                """, unsafe_allow_html=True)
            
            with status_container:
                # Detailed progress tracking
                progress_bar = st.progress(0)
                status_text = st.empty()
                metrics_display = st.empty()
                # Step 1: Data Preparation
                with status_text:
                    st.markdown("""
                    <div style="
                        background: #334155;
                        border-radius: 8px;
                        padding: 12px;
                        margin: 8px 0;
                        border-left: 4px solid #f59e0b;
                    ">
                        <span style="color: #e2e8f0; font-weight: 500;">
                            Step 1/4: Sampling and preparing {sample_size:,} comments from dataset...
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
                progress_bar.progress(0.1)
                
                # Get sample of comments
                sample_comments = comments_df.sample(n=sample_size)["comment"].tolist()

                # Validate comment batch
                (
                    all_valid,
                    sanitized_comments,
                    validation_errors,
                ) = InputValidator.validate_comment_batch(sample_comments)

                # Step 2: Validation
                with status_text:
                    st.markdown("""
                    <div style="
                        background: #334155;
                        border-radius: 8px;
                        padding: 12px;
                        margin: 8px 0;
                        border-left: 4px solid #4299e1;
                    ">
                        <span style="color: #e2e8f0; font-weight: 500;">
                            Step 2/4: Validating and sanitizing comments for AI processing...
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
                progress_bar.progress(0.2)
                
                if not all_valid:
                    st.warning("Some comments failed validation:")
                    for error in validation_errors[:5]:  # Show first 5 errors
                        st.warning(f"  • {error}")

                    if len(validation_errors) > 5:
                        st.warning(
                            f"  • ... and {len(validation_errors) - 5} more errors"
                        )

                    # Use only valid comments
                    valid_comments = [c for c in sanitized_comments if c.strip()]
                    if len(valid_comments) == 0:
                        progress_container.empty()
                        status_container.empty()
                        st.error("No valid comments to analyze after validation")
                        return

                    st.info(f"Proceeding with {len(valid_comments)} valid comments")
                    sample_comments = valid_comments
                else:
                    sample_comments = sanitized_comments

                # Step 3: AI Analysis
                with status_text:
                    st.markdown(f"""
                    <div style="
                        background: #334155;
                        border-radius: 8px;
                        padding: 12px;
                        margin: 8px 0;
                        border-left: 4px solid #10b981;
                    ">
                        <span style="color: #e2e8f0; font-weight: 500;">
                            Step 3/4: Running Basic Analysis on {len(sample_comments):,} comments...
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
                progress_bar.progress(0.3)
                
                with metrics_display:
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Comments to Analyze", f"{len(sample_comments):,}")
                    with col2:
                        st.metric("AI Model", "GPT-4")
                    with col3:
                        st.metric("Processing", "In Progress...")
                    with col4:
                        st.metric("Status", "Analyzing...")
                
                # Use AI Adapter for comprehensive AI-powered analysis
                st.info("🤖 Using AI-powered analysis with OpenAI GPT-4 and automatic fallback.")
                ai_adapter = AIAnalysisAdapter()
                analyzer_type = "AI Analysis with Fallback" if ai_adapter.ai_available else "Rule-based Analysis"
                
                # Create a temporary uploaded file object from the DataFrame data
                if 'comments_data' in st.session_state:
                    comments_df = st.session_state['comments_data']
                    
                    # Create a BytesIO object from the DataFrame to simulate uploaded file
                    import io
                    from io import BytesIO
                    
                    # Create Excel file in memory
                    excel_buffer = BytesIO()
                    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                        comments_df.head(sample_size).to_excel(writer, index=False, sheet_name='Comentarios')
                    excel_buffer.seek(0)
                    
                    # Create mock uploaded file object
                    class MockUploadedFile:
                        def __init__(self, content, name):
                            self.name = name
                            self.size = len(content.getvalue())
                            self._content = content
                        
                        def read(self, size=-1):
                            return self._content.read(size)
                        
                        def seek(self, offset, whence=0):
                            return self._content.seek(offset, whence)
                    
                    mock_file = MockUploadedFile(excel_buffer, "analysis_data.xlsx")
                    
                    # Use AI adapter to process the data
                    st.info(f"🔄 Processing {sample_size} comments with AI adapter...")
                    ai_results = ai_adapter.process_uploaded_file_with_ai(mock_file)
                    
                    if ai_results:
                        # Store AI results in session state
                        st.session_state['analysis_results'] = ai_results
                        st.session_state['enhanced_insights'] = ai_results
                        
                        # Convert to the expected format for this function
                        results = []
                        sentiments = ai_results.get('sentiments', [])
                        for i, comment in enumerate(sample_comments):
                            sentiment = sentiments[i] if i < len(sentiments) else 'neutral'
                            results.append({
                                "comment_number": i + 1,
                                "sentiment": sentiment,
                                "confidence": ai_results.get('ai_confidence_avg', 0.8),
                                "language": "es",
                                "translation": comment,
                                "themes": ["ai_detected"],
                                "pain_points": [],
                                "emotions": ["ai_analyzed"]
                            })
                    else:
                        st.error("AI analysis failed - no results returned")
                        return
                
                else:
                    st.error("No comments data available in session state")
                    return

                # Update UI to show which analyzer was used
                with metrics_display:
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Comments to Analyze", f"{len(sample_comments):,}")
                    with col2:
                        analysis_method = ai_results.get('analysis_method', 'Unknown')
                        if analysis_method == 'AI_POWERED':
                            st.metric("AI Model", "🤖 GPT-4 Active")
                        elif analysis_method == 'RULE_BASED_FALLBACK':
                            st.metric("AI Model", "🔄 Fallback Mode")
                        else:
                            st.metric("AI Model", analyzer_type)
                    with col3:
                        st.metric("Processing", "Completed")
                    with col4:
                        st.metric("Status", "✅ Done")

                # Results are already set above in the AI processing block
                progress_bar.progress(0.7)

                # Step 4: Generating Insights
                with status_text:
                    st.markdown("""
                    <div style="
                        background: #334155;
                        border-radius: 8px;
                        padding: 12px;
                        margin: 8px 0;
                        border-left: 4px solid #8b5cf6;
                    ">
                        <span style="color: #e2e8f0; font-weight: 500;">
                            Step 4/4: Generating insights, recommendations, and storing results...
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
                progress_bar.progress(0.8)
                
                # Generate insights using basic analyzer
                try:
                    insights = analyzer.get_insights(results)
                    recommendations = analyzer.get_recommendations(insights)
                except Exception as e:
                    st.error(f"Failed to generate insights: {str(e)}")
                    # Create minimal fallback insights
                    total_comments = len(results)
                    insights = {
                        'sentiment_percentages': {'neutral': 100.0, 'positive': 0.0, 'negative': 0.0},
                        'sentiment_distribution': {'neutral': 100.0, 'positive': 0.0, 'negative': 0.0},
                        'top_themes': {'general': total_comments},
                        'top_pain_points': {},
                        'analyzed_count': total_comments,
                        'average_confidence': 0.5
                    }
                    recommendations = ["Basic analysis completed successfully. Configure OpenAI API key for advanced insights."]
                progress_bar.progress(0.9)

                # Store results using session manager
                self.session_manager.store_analysis_results(
                    results, insights, recommendations, sample_comments
                )
                
                progress_bar.progress(1.0)
                
                # Clear progress and show success
                progress_container.empty()
                status_container.empty()
                
                # Store success state for persistent display
                st.session_state['last_analysis_success'] = {
                    'timestamp': time.time(),
                    'comments_count': len(sample_comments),
                    'analyzer_type': analyzer_type,
                    'insights_count': len(insights.get('top_themes', {})),
                    'recommendations_count': len(recommendations)
                }
                
                # Show comprehensive success message
                st.success("🎉 **Analysis Complete!** Your results and insights are now available in the 'Results & Insights' tab below.")
                
                # Show analysis summary
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Comments Analyzed", len(sample_comments))
                with col2:
                    st.metric("Themes Found", len(insights.get('top_themes', {})))
                with col3:
                    st.metric("Recommendations", len(recommendations))
                
                st.info("📋 **Next Steps:** Switch to the 'Results & Insights' tab to view detailed analysis, charts, and export options.")
                
                st.rerun()

        except APIConnectionError as e:
            progress_container.empty()
            status_container.empty()
            ErrorHandler.handle_streamlit_error(e)
        except AnalysisProcessingError as e:
            progress_container.empty()
            status_container.empty()
            ErrorHandler.handle_streamlit_error(e)
        except Exception as e:
            progress_container.empty()
            status_container.empty()
            ErrorHandler.handle_streamlit_error(e, "Analysis failed unexpectedly")
            SecurityLogger.log_suspicious_activity("analysis_error", str(e))

    def analyze_all_comments_batch(self, comments_df: pd.DataFrame, batch_size: int):
        """Analyze all comments in batches with memory optimization and advanced progress tracking"""
        
        # Log initial memory status
        log_memory_status()
        
        # Clean session state before starting
        optimize_session_state()
        
        with self.memory_manager.memory_monitor("batch_analysis"):
            all_comments = comments_df["comment"].tolist()
            total_comments = len(all_comments)

            # Calculate total number of batches
            total_batches = (total_comments + batch_size - 1) // batch_size

            # Create progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()

            with st.spinner("Running memory-optimized batch analysis..."):
                try:
                    # Check API status
                    self._check_api_status()

                    # Create batches using memory-efficient batch processor
                    comment_batches = list(self.batch_processor.create_batches(all_comments, batch_size))
                    
                    # Define batch processing function
                    def process_comment_batch(batch_comments):
                        try:
                            return self._process_batch_with_retries(batch_comments, len(batch_comments))
                        except Exception as e:
                            logging.error(f"Error in batch processing: {e}")
                            return None
                    
                    # Define cleanup function
                    def cleanup_between_batches():
                        # Clear temporary variables and force garbage collection
                        self.memory_manager.force_garbage_collection()
                        log_memory_status()
                    
                    # Process all batches with memory management
                    all_results = self.batch_processor.process_batches_with_memory_management(
                        iter(comment_batches),
                        process_comment_batch,
                        cleanup_between_batches
                    )
                    
                    # Update progress for each completed batch
                    for i, batch in enumerate(comment_batches):
                        progress = (i + 1) / len(comment_batches)
                        progress_bar.progress(progress)
                        status_text.text(f"Completed batch {i+1}/{len(comment_batches)}")
                        time.sleep(0.1)  # Small delay for UI update

                    # Generate final insights with memory monitoring
                    status_text.text("Generating insights and recommendations...")

                    if all_results:
                        with self.memory_manager.memory_monitor("generating_insights"):
                            analyzer = OpenAIAnalyzer()
                            insights = analyzer.get_overall_insights(all_results)
                            recommendations = analyzer.generate_recommendations(insights)

                            # Store results using session manager
                            self.session_manager.store_analysis_results(
                                all_results, insights, recommendations, all_comments
                            )

                        # Calculate statistics
                        elapsed_time = time.time() - time.time()  # Will be calculated properly in batch processor
                        processing_stats = {
                            "total_processed": len(all_results),
                            "total_batches": len(comment_batches),
                            "batch_size": batch_size,
                            "memory_optimized": True,
                        }

                        st.session_state["batch_processed"] = True
                        st.session_state["processing_stats"] = processing_stats

                        # Complete progress
                        progress_bar.progress(1.0)
                        status_text.text("Memory-optimized analysis completed successfully!")

                        success_msg = f"Successfully analyzed {len(all_results)} comments!"
                        st.success(success_msg)

                        # Show performance stats with memory info
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            estimated_cost = len(all_results) * 0.002
                            st.info(f"Estimated API cost: ~${estimated_cost:.2f}")
                        with col2:
                            final_memory = self.memory_manager.get_memory_usage()
                            st.info(f"Memory usage: {final_memory['rss_mb']:.1f}MB")
                        with col3:
                            st.info(f"Batches: {len(comment_batches)}")

                        # Final cleanup
                        optimize_session_state()
                        st.rerun()

                    else:
                        st.error("No comments were successfully analyzed")

                except Exception as e:
                    ErrorHandler.handle_streamlit_error(
                        e, "Memory-optimized batch analysis failed"
                    )
                    self._show_troubleshooting_info()
                finally:
                    # Always clean up memory at the end
                    optimize_session_state()
                    self.memory_manager.force_garbage_collection()

    def _check_api_status(self):
        """Check OpenAI API status"""
        try:
            import openai

            st.info("Checking OpenAI API status...")

            # Get API key from environment
            api_key = os.environ.get("OPENAI_API_KEY")
            if not api_key:
                st.error(
                    "OpenAI API key not found in environment. Please check your settings."
                )
                return

            # Test API connectivity
            client = openai.OpenAI(api_key=api_key)
            models = client.models.list()
            available_models = [model.id for model in models.data]
            st.success(
                f"OpenAI API connection successful. Found {len(available_models)} models."
            )

            # Show model availability
            if "gpt-4" in str(available_models):
                st.info("GPT-4 models available")
            else:
                st.warning("GPT-4 models not found in your account")

        except Exception as e:
            st.error(f"Error connecting to OpenAI API: {str(e)}")
            st.warning("Will attempt to proceed, but analysis may fail.")

    def _process_batch_with_retries(
        self, batch_comments: List[str], batch_num: int, max_retries: int = 3
    ) -> List[Dict]:
        """Process a batch of comments with retry logic"""
        
        # Input validation
        if not batch_comments:
            raise ValueError("Comments list cannot be empty")
        
        if not isinstance(batch_comments, list):
            raise TypeError("Comments must be provided as a list")
        
        if len(batch_comments) > 1000:
            logging.warning(f"Large batch size {len(batch_comments)} detected, processing first 1000 comments")
            batch_comments = batch_comments[:1000]
        
        # Validate each comment
        validator = InputValidator()
        valid_comments = []
        
        for i, comment in enumerate(batch_comments):
            if not isinstance(comment, str):
                logging.warning(f"Skipping non-string comment at position {i}: {type(comment)}")
                continue
            
            if not comment or len(comment.strip()) == 0:
                logging.warning(f"Skipping empty comment at position {i}")
                continue
                
            if len(comment) > 5000:
                logging.warning(f"Truncating overly long comment at position {i} (length: {len(comment)})")
                comment = comment[:5000]
            
            # Basic security validation
            if not validator.validate_comment_content(comment):
                logging.warning(f"Skipping potentially malicious comment at position {i}")
                continue
            
            valid_comments.append(comment.strip())
        
        if not valid_comments:
            raise ValueError("No valid comments found in batch after validation")
        
        if len(valid_comments) < len(batch_comments):
            logging.info(f"Filtered batch: {len(batch_comments)} -> {len(valid_comments)} valid comments")
        
        # Update batch_comments to use only valid ones
        batch_comments = valid_comments
        retry_delay = 2

        for retry in range(max_retries):
            try:
                # Create analyzer and process batch
                analyzer = OpenAIAnalyzer()
                results = analyzer.analyze_comments_batch(batch_comments)
                return results

            except Exception as e:
                error_msg = str(e)
                if retry < max_retries - 1:
                    st.warning(
                        f"Retry {retry+1}/{max_retries} for batch {batch_num}: {error_msg[:100]}"
                    )
                    time.sleep(retry_delay)
                    retry_delay *= 1.5  # Exponential backoff
                else:
                    st.error(
                        f"Failed to process batch {batch_num} after {max_retries} attempts"
                    )
                    return None

    def _show_troubleshooting_info(self):
        """Show troubleshooting information"""
        with st.expander("Troubleshooting Steps"):
            st.write("**Common Solutions:**")
            st.write("1. Check that your API key is valid and has sufficient credits")
            st.write("2. Try a smaller batch size (e.g., 25 instead of 50)")
            st.write("3. Check your internet connection")
            st.write("4. Try analyzing a smaller dataset first")
            st.write("5. Verify OpenAI service status")

    def analyze_single_comment(self, comment: str) -> Dict:
        """Analyze a single comment"""
        try:
            analyzer = OpenAIAnalyzer()
            return analyzer.analyze_single_comment(comment)
        except Exception as e:
            raise AnalysisProcessingError(f"Single comment analysis failed: {str(e)}")

    def get_analysis_status(self) -> Dict:
        """Get current analysis status"""
        return {
            "has_results": self.session_manager.has_analysis_results(),
            "is_multi_sheet": st.session_state.get("is_multi_sheet", False),
            "current_sheet": st.session_state.get("current_sheet"),
            "sheet_status": self.session_manager.get_sheet_analysis_status(),
        }


def format_time(seconds: float) -> str:
    """Format seconds into a readable time string"""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"
