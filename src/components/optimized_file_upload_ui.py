"""
Optimized File Upload UI Components for Personal Paraguay Comments Analysis Platform
Features enhanced 2-column layout, compact metrics grid, and improved space utilization
"""

import streamlit as st
import pandas as pd
from pathlib import Path
from typing import Dict, Optional, Tuple

from src.theme import theme
from src.services.file_upload_service import FileUploadService
from src.services.session_manager import SessionManager
from src.data_processing.comment_reader import CommentReader
from src.utils.exceptions import ErrorHandler, FileProcessingError


class OptimizedFileUploadUI:
    """Optimized UI component with efficient space utilization"""

    def __init__(self):
        self.file_service = FileUploadService()
        self.session_manager = SessionManager()

    def render_upload_interface(self):
        """Render optimized 2-column layout interface"""
        # Progress tracker at the top
        self._render_progress_tracker()
        
        # Main 2-column layout for better space usage
        left_col, right_col = st.columns([1.2, 1], gap="medium")
        
        with left_col:
            self._render_left_column()
            
        with right_col:
            self._render_right_column()
            
        # Full-width data preview section below the columns
        if "uploaded_data" in st.session_state and st.session_state.uploaded_data is not None:
            st.markdown("---")
            self._render_full_width_preview()
            
    def _render_progress_tracker(self):
        """Render horizontal progress tracker"""
        steps = ["Upload", "Validate", "Preview", "Analyze"]
        current_step = st.session_state.get("upload_step", 0)
        
        # Create a compact progress bar
        progress_cols = st.columns(4)
        for idx, (col, step) in enumerate(zip(progress_cols, steps)):
            with col:
                if idx <= current_step:
                    st.markdown(f"""
                    <div style="text-align: center; padding: 8px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    border-radius: 8px; color: white; font-weight: 600;">
                        {idx + 1}. {step}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="text-align: center; padding: 8px; background: rgba(255,255,255,0.05); 
                    border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; color: #666;">
                        {idx + 1}. {step}
                    </div>
                    """, unsafe_allow_html=True)
        
        st.markdown("<hr style='margin: 16px 0;'>", unsafe_allow_html=True)

    def _render_left_column(self):
        """Render left column with upload and file info"""
        # Compact upload section
        with st.container():
            st.markdown("#### 📤 Upload Data")
            
            uploaded_file = st.file_uploader(
                "Choose file",
                type=["xlsx", "csv", "json", "txt"],
                help="Max 50MB • Excel, CSV, JSON, or Text",
                label_visibility="collapsed"
            )
            
            if uploaded_file:
                # Update progress
                if "upload_step" not in st.session_state:
                    st.session_state.upload_step = 1
                    
                self._handle_uploaded_file_compact(uploaded_file)
            else:
                # Sample dataset option in a compact format
                with st.expander("💡 No data? Try sample dataset"):
                    st.write("Load our Personal Paraguay telecommunications dataset for testing")
                    if st.button("Load Sample Data", use_container_width=True, type="primary"):
                        self._load_sample_dataset()

    def _render_right_column(self):
        """Render right column with real-time info and metrics"""
        if "uploaded_data" in st.session_state and st.session_state.uploaded_data is not None:
            # Show quality metrics only (preview moved to full width)
            self._render_compact_metrics()
        else:
            # Show helpful info when no data is uploaded
            self._render_upload_guide()

    def _handle_uploaded_file_compact(self, uploaded_file):
        """Handle file with compact validation display"""
        # Validate file
        is_valid, error_msg, metadata = self.file_service.validate_file_basic(uploaded_file)
        
        if not is_valid:
            st.error(f"❌ {error_msg}")
            return
            
        # Compact validation status in columns
        val_cols = st.columns(3)
        with val_cols[0]:
            st.success(f"✓ {metadata['extension'].upper()}")
        with val_cols[1]:
            st.success(f"✓ {metadata['size_mb']:.1f}MB")
        with val_cols[2]:
            st.info(f"~{metadata.get('rows_estimate', 'Unknown')} rows")
            
        # Process file
        with st.spinner("Processing..."):
            success, message, comments_df, processing_info = self.file_service.process_uploaded_file(uploaded_file)
            
            if not success:
                st.error(f"Processing failed: {message}")
                return
                
            # Update progress
            st.session_state.upload_step = 2
            
            # Handle Excel sheets if needed
            if processing_info.get("requires_sheet_selection", False):
                selected_sheet = st.selectbox(
                    "Select sheet:",
                    processing_info["sheets"],
                    index=0
                )
                if selected_sheet != processing_info.get("current_sheet"):
                    success, message, comments_df = self.file_service.process_excel_sheet(
                        processing_info["temp_path"], selected_sheet
                    )
                    
            # Store data and update UI
            data_info = self._create_data_info(comments_df)
            self.session_manager.store_uploaded_data(comments_df, data_info, processing_info)
            st.session_state.uploaded_data = comments_df
            st.session_state.upload_step = 3
            st.rerun()

    def _render_compact_metrics(self):
        """Render compact metrics in right column"""
        comments_df = st.session_state.uploaded_data
        
        # Compact metrics grid
        st.markdown("#### 📊 Dataset Metrics")
        metrics_container = st.container()
        with metrics_container:
            # 2x2 grid for metrics
            m1, m2 = st.columns(2)
            m3, m4 = st.columns(2)
            
            with m1:
                st.metric("Total Comments", f"{len(comments_df):,}")
            with m2:
                avg_len = int(comments_df['comment'].str.len().mean()) if 'comment' in comments_df.columns else 0
                st.metric("Avg Length", f"{avg_len} chars")
            with m3:
                quality_metrics = self.file_service.get_data_quality_metrics(comments_df)
                st.metric("Valid Entries", f"{quality_metrics['valid_entries']:,}")
            with m4:
                quality_pct = quality_metrics['quality_score']
                color = "🟢" if quality_pct >= 80 else "🟡" if quality_pct >= 60 else "🔴"
                st.metric("Quality", f"{color} {quality_pct}%")
    
    def _render_full_width_preview(self):
        """Render full-width data preview below the columns"""
        comments_df = st.session_state.uploaded_data
        
        # Full-width data preview section
        st.markdown("### 👀 Data Preview")
        
        # Control row with slider and action button
        control_col1, control_col2, control_col3 = st.columns([2, 1, 1])
        
        with control_col1:
            preview_rows = st.slider(
                "Number of rows to display:", 
                min_value=5, 
                max_value=min(100, len(comments_df)), 
                value=min(20, len(comments_df)),
                step=5,
                help="Adjust the number of rows shown in preview"
            )
        
        with control_col2:
            show_all_cols = st.checkbox("Show all columns", value=True, help="Toggle between all columns and essential columns only")
        
        with control_col3:
            if st.button(
                "🚀 Start Analysis", 
                type="primary", 
                use_container_width=True,
                help="Proceed to Analysis Dashboard"
            ):
                st.session_state.selected_page = "Analysis Dashboard"
                st.rerun()
        
        # Display the dataframe using full width
        if show_all_cols:
            display_df = comments_df.head(preview_rows)
        else:
            # Show only essential columns if they exist
            essential_cols = ['comment', 'date', 'category', 'source']
            available_cols = [col for col in essential_cols if col in comments_df.columns]
            if not available_cols:
                available_cols = comments_df.columns[:3]  # Show first 3 columns if no essential ones found
            display_df = comments_df[available_cols].head(preview_rows)
        
        # Use full container width for the dataframe
        st.dataframe(
            display_df, 
            use_container_width=True,
            height=min(preview_rows * 35 + 50, 600)  # Dynamic height based on rows
        )
        
        # Data info bar
        info_cols = st.columns(4)
        with info_cols[0]:
            st.info(f"📝 Showing {preview_rows} of {len(comments_df):,} total rows")
        with info_cols[1]:
            st.info(f"📊 {len(display_df.columns)} columns displayed")
        with info_cols[2]:
            null_count = comments_df.isnull().sum().sum()
            st.info(f"⚠️ {null_count:,} null values")
        with info_cols[3]:
            duplicates = comments_df.duplicated().sum()
            st.info(f"🔄 {duplicates:,} duplicate rows")

    def _render_upload_guide(self):
        """Render upload guide in right column when no data"""
        st.markdown("#### 📋 Quick Guide")
        
        # Compact format requirements
        with st.container():
            st.info("""
            **Supported Formats:**
            • Excel (.xlsx) - Multi-sheet support
            • CSV (.csv) - Comma-separated
            • JSON (.json) - Structured data
            • Text (.txt) - Line-by-line
            
            **Requirements:**
            • Max 50MB file size
            • Max 20,000 rows
            • UTF-8 encoding preferred
            """)
            
        # Tips section
        with st.expander("💡 Pro Tips", expanded=True):
            st.markdown("""
            • **Column naming**: Use 'comment' or 'text' for main content
            • **Date formats**: ISO 8601 (YYYY-MM-DD) recommended
            • **Categories**: Include if available for better analysis
            • **Clean data**: Remove special characters if possible
            """)

    def _create_data_info(self, comments_df: pd.DataFrame) -> Dict:
        """Create data info dictionary"""
        return {
            "total_comments": len(comments_df),
            "sources": ["uploaded_file"],
            "columns": list(comments_df.columns),
        }

    def _load_sample_dataset(self):
        """Load sample dataset"""
        try:
            dataset_path = Path("Personal_Paraguay_Fiber_To_The_Home_Customer_Comments_Dataset.xlsx")
            if dataset_path.exists():
                reader = CommentReader()
                comments_df = reader.read_file(dataset_path)
                data_info = reader.get_data_info()
                
                processing_info = {
                    "temp_path": str(dataset_path),
                    "file_extension": ".xlsx",
                    "is_excel": True,
                    "is_multi_sheet": False,
                    "requires_sheet_selection": False,
                }
                
                self.session_manager.store_uploaded_data(comments_df, data_info, processing_info)
                st.session_state.uploaded_data = comments_df
                st.session_state.upload_step = 3
                st.success("✅ Sample dataset loaded!")
                st.rerun()
            else:
                st.warning("Sample dataset not found")
        except Exception as e:
            ErrorHandler.handle_streamlit_error(e, "Failed to load dataset")