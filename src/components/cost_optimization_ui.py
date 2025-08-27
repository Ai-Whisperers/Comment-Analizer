"""
Cost Optimization UI Components for Personal Paraguay Comments Analysis Platform
Handles UI rendering for cost analysis and optimization functionality
"""

import streamlit as st
import pandas as pd
import time
from collections import Counter
from typing import Dict, List, Optional

from src.theme import theme
from src.services.session_manager import SessionManager


class CostOptimizationUI:
    """UI component for cost optimization and efficiency analysis"""

    def __init__(self):
        self.session_manager = SessionManager()

    def render_cost_optimization(self):
        """Render the complete cost optimization interface"""
        st.header("Cost Optimization & Efficiency")
        
        # Check if data is loaded
        if not self.session_manager.has_data_loaded():
            st.warning("No data loaded. Please upload data first in the 'Data Upload' section.")
            return
        
        current_data = self.session_manager.get_current_data()
        comments_df = current_data["comments_data"]
        
        self._render_cost_analysis_overview(comments_df)
        self._render_optimization_settings()
        self._render_duplicate_analysis(comments_df)
        self._render_efficiency_monitoring()
        self._render_batch_optimization()
        self._render_api_usage_tracking()

    def _render_cost_analysis_overview(self, comments_df: pd.DataFrame):
        """Render cost analysis overview section"""
        st.subheader("Cost Analysis")
        
        total_comments = len(comments_df)
        standard_cost = total_comments * 0.002  # Standard cost at $0.002 per comment
        
        # Analyze duplicates
        duplicate_analysis = self._analyze_duplicates(comments_df)
        
        # Display cost metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Standard API Cost", f"${standard_cost:.2f}")
            st.caption(f"Based on {total_comments} comments at $0.002 each")
            
        with col2:
            optimized_cost = standard_cost - duplicate_analysis['duplicate_savings']
            st.metric("Optimized Cost", f"${optimized_cost:.2f}", 
                     delta=f"-${duplicate_analysis['duplicate_savings']:.2f}")
            st.caption("After removing duplicates and pre-filtering")
            
        with col3:
            savings_pct = (duplicate_analysis['duplicate_savings'] / standard_cost) * 100 if standard_cost > 0 else 0
            st.metric("Potential Savings", f"{savings_pct:.1f}%")
            st.caption(f"Found {duplicate_analysis['total_duplicates']} duplicate comments")

    def _analyze_duplicates(self, comments_df: pd.DataFrame) -> Dict:
        """Analyze duplicate comments for cost optimization"""
        if 'duplicate_analysis' not in st.session_state:
            with st.spinner("Analyzing for duplicates..."):
                # Create hashable representation of comments
                comments_list = comments_df['comment'].str.strip().str.lower().tolist()
                comment_counts = Counter(comments_list)
                
                # Find duplicates
                duplicates = {comment: count for comment, count in comment_counts.items() if count > 1}
                total_duplicates = sum(count - 1 for count in duplicates.values())
                
                # Calculate savings
                duplicate_savings = total_duplicates * 0.002
                total_comments = len(comments_df)
                
                # Store in session
                st.session_state['duplicate_analysis'] = {
                    'total_duplicates': total_duplicates,
                    'duplicate_pct': (total_duplicates / max(1, total_comments)) * 100,
                    'duplicate_savings': duplicate_savings,
                    'duplicates': duplicates
                }
        
        return st.session_state['duplicate_analysis']

    def _render_optimization_settings(self):
        """Render optimization settings section"""
        st.markdown("---")
        st.subheader("Optimization Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            self._render_duplicate_handling_options()
        
        with col2:
            self._render_prefiltering_options()

    def _render_duplicate_handling_options(self):
        """Render duplicate handling options"""
        st.write("**Duplicate Handling**")
        dedup_option = st.radio(
            "How to handle duplicates:",
            ["Process duplicates only once", "Process all comments (no deduplication)"],
            index=0,
            key="dedup_option"
        )
        
        duplicate_analysis = st.session_state.get('duplicate_analysis', {})
        
        # Calculate impact
        if dedup_option == "Process duplicates only once":
            savings = duplicate_analysis.get('duplicate_savings', 0)
            st.success(f"Saves ${savings:.2f}")
        else:
            st.info("No cost savings from deduplication")
        
        # Store preference
        st.session_state['use_deduplication'] = (dedup_option == "Process duplicates only once")

    def _render_prefiltering_options(self):
        """Render pre-filtering options"""
        st.write("**Pre-filtering Options**")
        
        use_prefiltering = st.checkbox("Enable pre-filtering for simple sentiment", value=True, key="use_prefiltering")
        use_language_detection = st.checkbox("Use lightweight language detection before API calls", value=True, key="use_language_detection")
        use_caching = st.checkbox("Cache API results for repeated analyses", value=True, key="use_caching")
        
        if use_language_detection:
            st.success("Reduces API costs by pre-identifying language and adding context")
            self._render_language_detection_test()

    def _render_language_detection_test(self):
        """Render language detection testing section"""
        if self.session_manager.has_data_loaded():
            with st.expander("Test Language Detection"):
                current_data = self.session_manager.get_current_data()
                comments_df = current_data["comments_data"]
                
                sample_size = min(10, len(comments_df))
                samples = comments_df.sample(n=sample_size)
                
                st.caption(f"Testing language detection on {sample_size} random comments")
                
                # Simple language detection simulation
                for idx, row in samples.iterrows():
                    comment = row['comment']
                    # Simple heuristic for demonstration
                    is_spanish = any(word in comment.lower() for word in ['de', 'la', 'el', 'en', 'con', 'por'])
                    language = "Spanish" if is_spanish else "Guarani"
                    confidence = 0.8 if is_spanish else 0.6
                    
                    st.write(f"**{language}** ({confidence:.1%}): _{comment[:50]}..._")

    def _render_duplicate_analysis(self, comments_df: pd.DataFrame):
        """Render detailed duplicate analysis section"""
        st.markdown("---")
        st.subheader("Duplicate Analysis Details")
        
        duplicate_analysis = st.session_state.get('duplicate_analysis', {})
        
        if duplicate_analysis and duplicate_analysis.get('duplicates'):
            # Show top duplicates
            duplicates = duplicate_analysis['duplicates']
            top_duplicates = sorted(duplicates.items(), key=lambda x: x[1], reverse=True)[:10]
            
            if top_duplicates:
                st.write("**Top 10 Most Frequent Duplicate Comments:**")
                
                duplicate_data = []
                for comment, count in top_duplicates:
                    savings = (count - 1) * 0.002
                    duplicate_data.append({
                        "Comment Preview": comment[:50] + "..." if len(comment) > 50 else comment,
                        "Occurrences": count,
                        "Potential Savings": f"${savings:.3f}"
                    })
                
                duplicate_df = pd.DataFrame(duplicate_data)
                st.dataframe(duplicate_df, use_container_width=True)
                
                # Export duplicate analysis
                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("Remove Duplicates for Analysis", key="remove_duplicates"):
                        self._remove_duplicates_from_dataset(comments_df)
                
                with col2:
                    if st.button("Export Duplicate Report", key="export_duplicates"):
                        self._export_duplicate_report(duplicate_analysis)
        else:
            st.info("No duplicate comments found in the dataset.")

    def _render_efficiency_monitoring(self):
        """Render efficiency monitoring section"""
        st.markdown("---")
        st.subheader("Efficiency Monitoring")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**API Usage Tracking**")
            
            # Get session stats
            total_api_calls = st.session_state.get('total_api_calls', 0)
            cached_responses = st.session_state.get('cached_responses', 0)
            total_cost = total_api_calls * 0.002
            saved_cost = cached_responses * 0.002
            
            st.metric("Total API Calls", total_api_calls)
            st.metric("Cached Responses", cached_responses)
            st.metric("Total Cost", f"${total_cost:.3f}")
            st.metric("Saved via Cache", f"${saved_cost:.3f}")
        
        with col2:
            st.write("**Performance Metrics**")
            
            avg_response_time = st.session_state.get('avg_response_time', 0)
            success_rate = st.session_state.get('api_success_rate', 100)
            
            st.metric("Avg Response Time", f"{avg_response_time:.2f}s")
            st.metric("Success Rate", f"{success_rate:.1f}%")
            
            # Reset tracking button
            if st.button("Reset Tracking", key="reset_tracking"):
                tracking_keys = ['total_api_calls', 'cached_responses', 'avg_response_time', 'api_success_rate']
                for key in tracking_keys:
                    if key in st.session_state:
                        del st.session_state[key]
                st.success("Tracking data reset!")
                st.rerun()

    def _render_batch_optimization(self):
        """Render batch optimization section"""
        st.markdown("---")
        st.subheader("Batch Processing Optimization")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Batch Size Configuration**")
            
            # Calculate optimal batch size
            if self.session_manager.has_data_loaded():
                current_data = self.session_manager.get_current_data()
                total_comments = len(current_data["comments_data"])
                
                # Recommend batch size based on dataset size
                if total_comments <= 100:
                    recommended_batch = 25
                elif total_comments <= 1000:
                    recommended_batch = 50
                else:
                    recommended_batch = 100
                
                st.info(f"Recommended batch size for {total_comments} comments: **{recommended_batch}**")
                
                batch_size = st.slider(
                    "Batch size for processing:",
                    min_value=10,
                    max_value=200,
                    value=recommended_batch,
                    step=10,
                    key="batch_size_optimization"
                )
                
                # Calculate processing estimates
                estimated_batches = (total_comments + batch_size - 1) // batch_size
                estimated_time = estimated_batches * 3  # Assume 3 seconds per batch
                estimated_cost = total_comments * 0.002
                
                st.write(f"**Estimates:**")
                st.write(f"- Batches: {estimated_batches}")
                st.write(f"- Time: ~{estimated_time // 60}m {estimated_time % 60}s")
                st.write(f"- Cost: ${estimated_cost:.2f}")
        
        with col2:
            st.write("**Processing Strategy**")
            
            strategy = st.selectbox(
                "Processing strategy:",
                ["Conservative (slower, more reliable)", "Balanced (recommended)", "Aggressive (faster, higher risk)"],
                index=1,
                key="processing_strategy"
            )
            
            if strategy == "Conservative (slower, more reliable)":
                st.info("• Smaller batches\n• Longer delays between requests\n• Higher retry limits")
            elif strategy == "Balanced (recommended)":
                st.success("• Standard batch sizes\n• Normal request intervals\n• Standard retry logic")
            else:
                st.warning("• Larger batches\n• Minimal delays\n• Limited retries\n• May hit rate limits")

    def _render_api_usage_tracking(self):
        """Render API usage tracking section"""
        st.markdown("---")
        st.subheader("API Usage Tracking")
        
        # Usage history
        if 'api_usage_history' not in st.session_state:
            st.session_state['api_usage_history'] = []
        
        usage_history = st.session_state['api_usage_history']
        
        if usage_history:
            # Convert to DataFrame for display
            usage_df = pd.DataFrame(usage_history)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Recent API Usage**")
                st.dataframe(usage_df.tail(10), use_container_width=True)
            
            with col2:
                st.write("**Usage Summary**")
                total_calls = len(usage_history)
                total_cost = sum(usage_df.get('cost', [0]))
                avg_response = usage_df.get('response_time', [0])
                avg_response_time = sum(avg_response) / len(avg_response) if avg_response else 0
                
                st.metric("Total API Calls", total_calls)
                st.metric("Total Cost", f"${total_cost:.3f}")
                st.metric("Avg Response Time", f"{avg_response_time:.2f}s")
                
                # Export usage data
                if st.button("Export Usage Data", key="export_usage"):
                    self._export_usage_data(usage_df)
        else:
            st.info("No API usage data recorded yet. Start analyzing comments to track usage.")

    def _remove_duplicates_from_dataset(self, comments_df: pd.DataFrame):
        """Remove duplicates from the current dataset"""
        original_count = len(comments_df)
        deduplicated_df = comments_df.drop_duplicates(subset=['comment'])
        new_count = len(deduplicated_df)
        removed_count = original_count - new_count
        
        # Update session state
        current_data = self.session_manager.get_current_data()
        current_data["comments_data"] = deduplicated_df
        
        # Update data info
        data_info = current_data["data_info"]
        data_info["total_comments"] = new_count
        
        # Store updated data
        self.session_manager.store_uploaded_data(
            deduplicated_df, 
            data_info, 
            current_data.get("processing_info", {})
        )
        
        st.success(f"Removed {removed_count} duplicate comments. Dataset now has {new_count} unique comments.")
        st.rerun()

    def _export_duplicate_report(self, duplicate_analysis: Dict):
        """Export duplicate analysis report"""
        try:
            # Create report data
            report_data = {
                "summary": duplicate_analysis,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "recommendations": [
                    "Enable deduplication to save API costs",
                    "Review top duplicates for data quality issues",
                    "Consider implementing input validation to prevent duplicates"
                ]
            }
            
            # Convert to JSON for download
            import json
            report_json = json.dumps(report_data, indent=2)
            
            st.download_button(
                label="Download Duplicate Analysis Report",
                data=report_json,
                file_name=f"duplicate_analysis_{int(time.time())}.json",
                mime="application/json"
            )
            
            st.success("Duplicate analysis report ready for download!")
            
        except Exception as e:
            st.error(f"Failed to export duplicate report: {str(e)}")

    def _export_usage_data(self, usage_df: pd.DataFrame):
        """Export API usage data"""
        try:
            csv_data = usage_df.to_csv(index=False)
            
            st.download_button(
                label="Download Usage Data CSV",
                data=csv_data,
                file_name=f"api_usage_{int(time.time())}.csv",
                mime="text/csv"
            )
            
            st.success("Usage data ready for download!")
            
        except Exception as e:
            st.error(f"Failed to export usage data: {str(e)}")

    def get_optimization_summary(self) -> Dict:
        """Get optimization summary for display"""
        duplicate_analysis = st.session_state.get('duplicate_analysis', {})
        
        return {
            "duplicate_savings": duplicate_analysis.get('duplicate_savings', 0),
            "total_duplicates": duplicate_analysis.get('total_duplicates', 0),
            "use_deduplication": st.session_state.get('use_deduplication', True),
            "use_caching": st.session_state.get('use_caching', True),
            "batch_size": st.session_state.get('batch_size_optimization', 50),
            "total_api_calls": st.session_state.get('total_api_calls', 0),
            "cached_responses": st.session_state.get('cached_responses', 0),
        }