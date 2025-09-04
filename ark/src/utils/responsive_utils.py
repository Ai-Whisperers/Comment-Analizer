"""
Responsive Design Utilities for Personal Paraguay Comments Analysis Platform
Provides responsive column layouts and screen size detection
"""

import streamlit as st
from typing import List, Tuple, Optional, Union
import pandas as pd


class ResponsiveUI:
    """Utility class for responsive design patterns"""
    
    @staticmethod
    def get_column_config(screen_type: str, layout_type: str) -> Union[List[float], int]:
        """
        Get responsive column configuration based on screen type and layout
        
        Args:
            screen_type: 'mobile', 'tablet', or 'desktop'
            layout_type: 'metrics', 'form', 'data', 'sidebar_main', etc.
            
        Returns:
            Column configuration for st.columns()
        """
        configs = {
            'metrics': {
                'mobile': 1,  # Single column
                'tablet': 2,  # 2 columns
                'desktop': 4  # 4 columns
            },
            'form': {
                'mobile': 1,
                'tablet': [1.5, 1],
                'desktop': [2, 1]
            },
            'data': {
                'mobile': 1,
                'tablet': 1,
                'desktop': [3, 1]  # Main content + sidebar
            },
            'sidebar_main': {
                'mobile': 1,
                'tablet': [1, 2],
                'desktop': [1, 3]
            },
            'two_column': {
                'mobile': 1,
                'tablet': 2,
                'desktop': 2
            },
            'three_column': {
                'mobile': 1,
                'tablet': 2,
                'desktop': 3
            }
        }
        
        return configs.get(layout_type, {}).get(screen_type, 1)
    
    @staticmethod
    def estimate_screen_size() -> str:
        """
        Estimate screen size based on Streamlit's container width
        Note: This is an approximation since Streamlit doesn't provide viewport info
        
        Returns:
            'mobile', 'tablet', or 'desktop'
        """
        # Use session state to track container width if available
        if 'container_width' in st.session_state:
            width = st.session_state.container_width
            if width < 768:
                return 'mobile'
            elif width < 1024:
                return 'tablet'
            else:
                return 'desktop'
        
        # Default to desktop if no width info available
        return 'desktop'
    
    @staticmethod
    def responsive_columns(layout_type: str, gap: str = "medium") -> List:
        """
        Create responsive columns based on estimated screen size
        
        Args:
            layout_type: Type of layout ('metrics', 'form', 'data', etc.)
            gap: Gap between columns ('small', 'medium', 'large')
            
        Returns:
            List of column objects from st.columns()
        """
        screen = ResponsiveUI.estimate_screen_size()
        config = ResponsiveUI.get_column_config(screen, layout_type)
        
        if isinstance(config, int):
            if config == 1:
                # Return single column as list for consistency
                return [st.container()]
            else:
                return st.columns(config, gap=gap)
        else:
            return st.columns(config, gap=gap)
    
    @staticmethod
    def responsive_dataframe(
        df: pd.DataFrame,
        max_rows_mobile: int = 10,
        max_rows_tablet: int = 15,
        max_rows_desktop: int = 20,
        height_mobile: int = 300,
        height_tablet: int = 400,
        height_desktop: int = 500
    ):
        """
        Display a dataframe with responsive height and row count
        
        Args:
            df: DataFrame to display
            max_rows_*: Maximum rows to show per screen size
            height_*: Container height per screen size
        """
        screen = ResponsiveUI.estimate_screen_size()
        
        if screen == 'mobile':
            max_rows = max_rows_mobile
            height = height_mobile
        elif screen == 'tablet':
            max_rows = max_rows_tablet
            height = height_tablet
        else:
            max_rows = max_rows_desktop
            height = height_desktop
        
        # Display with responsive settings
        st.dataframe(
            df.head(max_rows),
            use_container_width=True,
            height=height
        )
    
    @staticmethod
    def responsive_metrics(metrics: List[Tuple[str, any, Optional[str]]]):
        """
        Display metrics in a responsive grid
        
        Args:
            metrics: List of tuples (label, value, delta/help)
        """
        cols = ResponsiveUI.responsive_columns('metrics')
        
        # Distribute metrics across available columns
        for idx, (label, value, extra) in enumerate(metrics):
            col_idx = idx % len(cols)
            with cols[col_idx]:
                if extra and isinstance(extra, str) and extra.startswith('+') or extra.startswith('-'):
                    st.metric(label, value, delta=extra)
                else:
                    st.metric(label, value, help=extra)
    
    @staticmethod
    def responsive_container_style() -> str:
        """
        Get responsive CSS for containers
        
        Returns:
            CSS string for responsive containers
        """
        return """
        <style>
        /* Mobile First Responsive Design */
        @media (max-width: 640px) {
            /* Mobile styles */
            .stColumns > div {
                flex: 0 0 100% !important;
                max-width: 100% !important;
            }
            
            .stMetric {
                padding: 0.5rem !important;
            }
            
            .stDataFrame {
                font-size: 0.8rem !important;
            }
            
            h1 { font-size: 1.5rem !important; }
            h2 { font-size: 1.25rem !important; }
            h3 { font-size: 1.1rem !important; }
            
            .stButton > button {
                width: 100% !important;
                padding: 0.75rem !important;
            }
        }
        
        @media (min-width: 641px) and (max-width: 1024px) {
            /* Tablet styles */
            .stColumns.two-col > div {
                flex: 0 0 50% !important;
                max-width: 50% !important;
            }
            
            .stMetric {
                padding: 0.75rem !important;
            }
        }
        
        @media (min-width: 1025px) {
            /* Desktop styles */
            .stColumns > div {
                flex: auto !important;
            }
        }
        
        /* Responsive tables */
        .dataframe {
            overflow-x: auto !important;
            -webkit-overflow-scrolling: touch;
        }
        
        /* Responsive charts */
        .plotly-graph-div {
            width: 100% !important;
        }
        
        /* Better mobile spacing */
        @media (max-width: 640px) {
            .main .block-container {
                padding: 1rem 0.5rem !important;
                max-width: 100% !important;
            }
            
            .stTabs [data-baseweb="tab-list"] {
                gap: 0.25rem !important;
                overflow-x: auto !important;
            }
            
            .stTabs [data-baseweb="tab"] {
                padding: 0.5rem !important;
                font-size: 0.9rem !important;
            }
        }
        </style>
        """
    
    @staticmethod
    def apply_responsive_theme():
        """Apply responsive theme to the entire app"""
        st.markdown(ResponsiveUI.responsive_container_style(), unsafe_allow_html=True)


class ResponsiveCards:
    """Create responsive card layouts"""
    
    @staticmethod
    def metric_card(title: str, value: any, subtitle: str = "", color: str = "#667eea"):
        """Create a responsive metric card"""
        return f"""
        <div class="responsive-metric-card" style="
            background: linear-gradient(135deg, {color}20 0%, {color}10 100%);
            border: 1px solid {color}40;
            border-radius: 12px;
            padding: 1rem;
            height: 100%;
            transition: transform 0.2s;
        ">
            <h4 style="margin: 0 0 0.5rem 0; color: {color}; font-size: 0.9rem;">
                {title}
            </h4>
            <div style="font-size: 1.8rem; font-weight: bold; margin: 0.25rem 0;">
                {value}
            </div>
            {f'<div style="font-size: 0.8rem; color: #888;">{subtitle}</div>' if subtitle else ''}
        </div>
        """
    
    @staticmethod
    def info_card(title: str, content: str, icon: str = "ℹ️"):
        """Create a responsive info card"""
        return f"""
        <div class="responsive-info-card" style="
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            padding: 1rem;
            margin: 0.5rem 0;
        ">
            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                <span style="font-size: 1.2rem; margin-right: 0.5rem;">{icon}</span>
                <h4 style="margin: 0; font-size: 1rem;">{title}</h4>
            </div>
            <div style="font-size: 0.9rem; color: #ccc; line-height: 1.5;">
                {content}
            </div>
        </div>
        """
    
    @staticmethod
    def progress_card(title: str, progress: float, color: str = "#667eea"):
        """Create a responsive progress card"""
        return f"""
        <div class="responsive-progress-card" style="
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            padding: 1rem;
            margin: 0.5rem 0;
        ">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span style="font-weight: 600;">{title}</span>
                <span style="color: {color};">{progress:.1f}%</span>
            </div>
            <div style="background: rgba(255, 255, 255, 0.1); border-radius: 4px; height: 8px; overflow: hidden;">
                <div style="
                    background: linear-gradient(90deg, {color} 0%, {color}80 100%);
                    height: 100%;
                    width: {progress}%;
                    transition: width 0.3s;
                    border-radius: 4px;
                "></div>
            </div>
        </div>
        """