"""
Dark Professional Theme for Personal Paraguay Comments Analysis Platform
Implements dark theme with no white backgrounds - only white text on dark backgrounds
Maintains excellent readability and professional appearance with smooth animations
"""

from .animations import get_animation_css
from .chart_themes import get_chart_css, get_dark_plotly_theme

class DarkProfessionalTheme:
    """
    Dark professional theme with no white backgrounds
    Specifically designed per user requirement: "only white text is allowed"
    """
    
    # Dark color palette - no white backgrounds anywhere
    COLORS = {
        # Dark background hierarchy (darkest to lighter)
        'bg_primary': '#0f172a',      # Primary dark background
        'bg_secondary': '#1e293b',    # Secondary dark background
        'bg_tertiary': '#334155',     # Tertiary dark background
        'bg_elevated': '#475569',     # Elevated components
        'bg_card': '#1e293b',         # Card backgrounds
        'bg_input': '#334155',        # Input field backgrounds
        
        # Text colors (white to gray on dark backgrounds)
        'text_primary': '#ffffff',    # Pure white text
        'text_secondary': '#f1f5f9',  # Near-white text
        'text_muted': '#cbd5e1',      # Muted text
        'text_disabled': '#94a3b8',   # Disabled text
        
        # Accent colors for interactive elements
        'primary_400': '#60a5fa',     # Primary accent (light blue)
        'primary_500': '#3b82f6',     # Primary buttons
        'primary_600': '#2563eb',     # Primary hover
        'primary_700': '#1d4ed8',     # Primary active
        'primary_900': '#1e3a8a',     # Primary dark
        
        # Semantic colors (dark theme variants)
        'success_400': '#4ade80',     # Success green
        'success_600': '#16a34a',     # Success dark
        'success_900': '#14532d',     # Success background
        
        'warning_400': '#fbbf24',     # Warning amber
        'warning_600': '#d97706',     # Warning dark
        'warning_900': '#451a03',     # Warning background
        
        'error_400': '#f87171',       # Error red
        'error_600': '#dc2626',       # Error dark
        'error_900': '#450a0a',       # Error background
        
        'info_400': '#38bdf8',        # Info blue
        'info_600': '#0284c7',       # Info dark
        'info_900': '#0c4a6e',       # Info background
        
        # Border and outline colors
        'border_light': '#475569',    # Light borders
        'border_medium': '#64748b',   # Medium borders
        'border_focus': '#60a5fa',    # Focus borders
        
        # Shadow colors for depth
        'shadow_sm': 'rgba(0, 0, 0, 0.3)',
        'shadow_md': 'rgba(0, 0, 0, 0.4)',
        'shadow_lg': 'rgba(0, 0, 0, 0.5)',
    }
    
    # Typography (same as modern theme but optimized for dark backgrounds)
    TYPOGRAPHY = {
        'font_family': '"Inter", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
        'font_family_mono': '"JetBrains Mono", "Fira Code", monospace',
        
        # Type scale
        'text_xs': '0.75rem',
        'text_sm': '0.875rem',
        'text_base': '1rem',
        'text_lg': '1.125rem',
        'text_xl': '1.25rem',
        'text_2xl': '1.5rem',
        'text_3xl': '1.875rem',
        'text_4xl': '2.25rem',
        'text_5xl': '3rem',
        
        # Font weights
        'font_normal': '400',
        'font_medium': '500',
        'font_semibold': '600',
        'font_bold': '700',
        
        # Line heights
        'leading_tight': '1.25',
        'leading_normal': '1.5',
        'leading_relaxed': '1.625',
        
        # Letter spacing
        'tracking_tight': '-0.025em',
        'tracking_normal': '0em',
        'tracking_wide': '0.025em',
    }
    
    # Spacing system (base-8)
    SPACING = {
        '1': '0.25rem',   # 4px
        '2': '0.5rem',    # 8px
        '3': '0.75rem',   # 12px
        '4': '1rem',      # 16px
        '5': '1.25rem',   # 20px
        '6': '1.5rem',    # 24px
        '8': '2rem',      # 32px
        '10': '2.5rem',   # 40px
        '12': '3rem',     # 48px
        '16': '4rem',     # 64px
        '20': '5rem',     # 80px
    }
    
    # Border radius system
    RADIUS = {
        'none': '0',
        'sm': '0.25rem',
        'md': '0.375rem',
        'lg': '0.5rem',
        'full': '9999px',
    }
    
    # Shadow system (enhanced for dark theme)
    SHADOWS = {
        'none': 'none',
        'sm': f'0 1px 2px 0 {COLORS["shadow_sm"]}',
        'md': f'0 4px 6px -1px {COLORS["shadow_md"]}',
        'lg': f'0 10px 15px -3px {COLORS["shadow_lg"]}',
    }
    
    @classmethod
    def get_main_css(cls) -> str:
        """Get the main CSS styling for dark theme"""
        return f"""
        <style>
        /* Import modern fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
        
        /* === DARK FOUNDATION === */
        .stApp {{
            font-family: {cls.TYPOGRAPHY['font_family']};
            color: {cls.COLORS['text_primary']};
            background-color: {cls.COLORS['bg_primary']};
            line-height: {cls.TYPOGRAPHY['leading_normal']};
        }}
        
        /* Remove any white backgrounds */
        * {{
            background-color: transparent !important;
        }}
        
        /* Re-apply dark backgrounds where needed */
        .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stHeader"],
        [data-testid="stToolbar"] {{
            background-color: {cls.COLORS['bg_primary']} !important;
        }}
        
        /* === TYPOGRAPHY HIERARCHY (WHITE TEXT) === */
        h1, h2, h3, h4, h5, h6 {{
            color: {cls.COLORS['text_primary']} !important;
            font-family: {cls.TYPOGRAPHY['font_family']};
            font-weight: {cls.TYPOGRAPHY['font_semibold']};
            line-height: {cls.TYPOGRAPHY['leading_tight']};
        }}
        
        h1 {{
            font-size: {cls.TYPOGRAPHY['text_4xl']};
            margin-bottom: {cls.SPACING['6']};
            letter-spacing: {cls.TYPOGRAPHY['tracking_tight']};
        }}
        
        h2 {{
            font-size: {cls.TYPOGRAPHY['text_3xl']};
            margin-bottom: {cls.SPACING['4']};
        }}
        
        h3 {{
            font-size: {cls.TYPOGRAPHY['text_2xl']};
            margin-bottom: {cls.SPACING['3']};
        }}
        
        h4 {{
            font-size: {cls.TYPOGRAPHY['text_xl']};
            margin-bottom: {cls.SPACING['2']};
        }}
        
        p, div, span {{
            color: {cls.COLORS['text_secondary']} !important;
            font-size: {cls.TYPOGRAPHY['text_base']};
            line-height: {cls.TYPOGRAPHY['leading_relaxed']};
        }}
        
        /* === DARK HEADER === */
        .main-header {{
            background: {cls.COLORS['bg_secondary']};
            border: 1px solid {cls.COLORS['border_light']};
            border-radius: {cls.RADIUS['lg']};
            padding: {cls.SPACING['8']};
            margin-bottom: {cls.SPACING['8']};
            box-shadow: {cls.SHADOWS['md']};
        }}
        
        .main-header h1 {{
            color: {cls.COLORS['text_primary']} !important;
            margin: 0 0 {cls.SPACING['2']} 0;
        }}
        
        .main-header p {{
            color: {cls.COLORS['text_muted']} !important;
            margin: 0;
            font-size: {cls.TYPOGRAPHY['text_lg']};
        }}
        
        /* === DARK CARDS === */
        .info-card {{
            background: {cls.COLORS['bg_card']} !important;
            border: 1px solid {cls.COLORS['border_light']};
            border-radius: {cls.RADIUS['md']};
            padding: {cls.SPACING['6']};
            margin-bottom: {cls.SPACING['4']};
            box-shadow: {cls.SHADOWS['sm']};
            transition: border-color 0.2s ease, box-shadow 0.2s ease;
        }}
        
        .info-card:hover {{
            border-color: {cls.COLORS['primary_400']};
            box-shadow: {cls.SHADOWS['md']};
        }}
        
        .info-card h3 {{
            color: {cls.COLORS['text_primary']} !important;
            margin: 0 0 {cls.SPACING['3']} 0;
        }}
        
        .info-card p, .info-card div {{
            color: {cls.COLORS['text_muted']} !important;
        }}
        
        /* === METRIC CARDS === */
        .metric-container {{
            background: {cls.COLORS['bg_card']} !important;
            border: 1px solid {cls.COLORS['border_light']};
            border-radius: {cls.RADIUS['md']};
            padding: {cls.SPACING['4']};
            box-shadow: {cls.SHADOWS['sm']};
        }}
        
        /* === UPLOAD SECTION === */
        .upload-section {{
            background: {cls.COLORS['bg_secondary']} !important;
            border: 2px dashed {cls.COLORS['border_medium']};
            border-radius: {cls.RADIUS['lg']};
            padding: {cls.SPACING['8']};
            text-align: center;
            transition: border-color 0.2s ease, background-color 0.2s ease;
        }}
        
        .upload-section:hover {{
            border-color: {cls.COLORS['primary_400']};
            background: {cls.COLORS['bg_tertiary']} !important;
        }}
        
        .upload-section h3 {{
            color: {cls.COLORS['text_primary']} !important;
        }}
        
        .upload-section p {{
            color: {cls.COLORS['text_muted']} !important;
        }}
        
        /* === DARK BUTTONS === */
        .stButton > button {{
            background: {cls.COLORS['primary_500']} !important;
            color: {cls.COLORS['text_primary']} !important;
            border: none;
            border-radius: {cls.RADIUS['sm']};
            padding: {cls.SPACING['3']} {cls.SPACING['5']};
            font-weight: {cls.TYPOGRAPHY['font_medium']};
            font-size: {cls.TYPOGRAPHY['text_sm']};
            letter-spacing: {cls.TYPOGRAPHY['tracking_wide']};
            transition: all 0.2s ease;
            box-shadow: {cls.SHADOWS['sm']};
        }}
        
        .stButton > button:hover {{
            background: {cls.COLORS['primary_600']} !important;
            box-shadow: {cls.SHADOWS['md']};
            transform: translateY(-1px);
        }}
        
        .stButton > button:active {{
            background: {cls.COLORS['primary_700']} !important;
            transform: translateY(0);
        }}
        
        /* === DARK SIDEBAR === */
        [data-testid="stSidebar"] {{
            background-color: {cls.COLORS['bg_secondary']} !important;
            border-right: 1px solid {cls.COLORS['border_light']};
        }}
        
        [data-testid="stSidebar"] * {{
            background-color: transparent !important;
        }}
        
        [data-testid="stSidebar"] .stMarkdown h1,
        [data-testid="stSidebar"] .stMarkdown h2,
        [data-testid="stSidebar"] .stMarkdown h3 {{
            color: {cls.COLORS['text_primary']} !important;
        }}
        
        [data-testid="stSidebar"] .stMarkdown p,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] .stSelectbox label {{
            color: {cls.COLORS['text_muted']} !important;
        }}
        
        [data-testid="stSidebar"] .stSelectbox > div > div {{
            background-color: {cls.COLORS['bg_input']} !important;
            border: 1px solid {cls.COLORS['border_light']};
            color: {cls.COLORS['text_primary']} !important;
        }}
        
        /* === FORM ELEMENTS === */
        .stSelectbox > div > div,
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {{
            background-color: {cls.COLORS['bg_input']} !important;
            border: 1px solid {cls.COLORS['border_light']} !important;
            border-radius: {cls.RADIUS['sm']};
            color: {cls.COLORS['text_primary']} !important;
        }}
        
        .stSelectbox > div > div:focus-within,
        .stTextInput > div > div:focus-within,
        .stTextArea > div > div:focus-within {{
            border-color: {cls.COLORS['primary_400']} !important;
            box-shadow: 0 0 0 3px {cls.COLORS['primary_900']} !important;
        }}
        
        /* === METRICS === */
        .stMetric {{
            background: {cls.COLORS['bg_card']} !important;
            border: 1px solid {cls.COLORS['border_light']};
            border-radius: {cls.RADIUS['md']};
            padding: {cls.SPACING['4']};
        }}
        
        .stMetric label {{
            color: {cls.COLORS['text_muted']} !important;
            font-size: {cls.TYPOGRAPHY['text_sm']} !important;
            font-weight: {cls.TYPOGRAPHY['font_medium']} !important;
        }}
        
        .stMetric [data-testid="metric-value"] {{
            color: {cls.COLORS['text_primary']} !important;
            font-size: {cls.TYPOGRAPHY['text_2xl']} !important;
            font-weight: {cls.TYPOGRAPHY['font_semibold']} !important;
        }}
        
        /* === ALERTS === */
        .stAlert {{
            border-radius: {cls.RADIUS['md']};
            border: none;
            font-weight: {cls.TYPOGRAPHY['font_medium']};
        }}
        
        .stSuccess {{
            background-color: {cls.COLORS['success_900']} !important;
            color: {cls.COLORS['success_400']} !important;
            border: 1px solid {cls.COLORS['success_600']};
        }}
        
        .stWarning {{
            background-color: {cls.COLORS['warning_900']} !important;
            color: {cls.COLORS['warning_400']} !important;
            border: 1px solid {cls.COLORS['warning_600']};
        }}
        
        .stError {{
            background-color: {cls.COLORS['error_900']} !important;
            color: {cls.COLORS['error_400']} !important;
            border: 1px solid {cls.COLORS['error_600']};
        }}
        
        .stInfo {{
            background-color: {cls.COLORS['info_900']} !important;
            color: {cls.COLORS['info_400']} !important;
            border: 1px solid {cls.COLORS['info_600']};
        }}
        
        /* === DATA TABLES === */
        .stDataFrame {{
            background: {cls.COLORS['bg_card']} !important;
            border: 1px solid {cls.COLORS['border_light']};
            border-radius: {cls.RADIUS['md']};
            overflow: hidden;
        }}
        
        .stDataFrame th {{
            background-color: {cls.COLORS['bg_tertiary']} !important;
            color: {cls.COLORS['text_primary']} !important;
            font-weight: {cls.TYPOGRAPHY['font_semibold']} !important;
            border-bottom: 1px solid {cls.COLORS['border_light']} !important;
        }}
        
        .stDataFrame td {{
            background-color: {cls.COLORS['bg_card']} !important;
            color: {cls.COLORS['text_secondary']} !important;
            border-bottom: 1px solid {cls.COLORS['border_light']} !important;
        }}
        
        /* === FILE UPLOADER === */
        .stFileUploader {{
            background-color: {cls.COLORS['bg_secondary']} !important;
            border: 2px dashed {cls.COLORS['border_medium']};
            border-radius: {cls.RADIUS['lg']};
            padding: {cls.SPACING['6']};
        }}
        
        .stFileUploader:hover {{
            border-color: {cls.COLORS['primary_400']};
            background-color: {cls.COLORS['bg_tertiary']} !important;
        }}
        
        .stFileUploader label,
        .stFileUploader span {{
            color: {cls.COLORS['text_muted']} !important;
        }}
        
        /* === PROGRESS BARS === */
        .stProgress > div > div > div {{
            background: {cls.COLORS['primary_500']} !important;
        }}
        
        .stProgress > div > div {{
            background: {cls.COLORS['bg_tertiary']} !important;
        }}
        
        /* === CODE BLOCKS === */
        .stCode {{
            background-color: {cls.COLORS['bg_tertiary']} !important;
            border: 1px solid {cls.COLORS['border_light']};
            border-radius: {cls.RADIUS['sm']};
            color: {cls.COLORS['text_primary']} !important;
            font-family: {cls.TYPOGRAPHY['font_family_mono']};
        }}
        
        /* === TABS === */
        .stTabs [data-baseweb="tab-list"] {{
            gap: {cls.SPACING['1']};
            background-color: {cls.COLORS['bg_tertiary']} !important;
            border-radius: {cls.RADIUS['md']};
            padding: {cls.SPACING['1']};
        }}
        
        .stTabs [data-baseweb="tab"] {{
            background-color: transparent !important;
            border-radius: {cls.RADIUS['sm']};
            color: {cls.COLORS['text_muted']} !important;
            font-weight: {cls.TYPOGRAPHY['font_medium']};
            padding: {cls.SPACING['2']} {cls.SPACING['4']};
        }}
        
        .stTabs [aria-selected="true"] {{
            background-color: {cls.COLORS['bg_card']} !important;
            color: {cls.COLORS['text_primary']} !important;
            box-shadow: {cls.SHADOWS['sm']};
        }}
        
        /* === EXPANDERS === */
        .streamlit-expanderHeader {{
            background-color: {cls.COLORS['bg_tertiary']} !important;
            border: 1px solid {cls.COLORS['border_light']};
            border-radius: {cls.RADIUS['md']};
            color: {cls.COLORS['text_primary']} !important;
        }}
        
        .streamlit-expanderContent {{
            background-color: {cls.COLORS['bg_card']} !important;
            border: 1px solid {cls.COLORS['border_light']};
            color: {cls.COLORS['text_secondary']} !important;
        }}
        
        /* === SCROLL BARS === */
        ::-webkit-scrollbar {{
            width: 6px;
            height: 6px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: {cls.COLORS['bg_tertiary']};
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: {cls.COLORS['border_medium']};
            border-radius: 3px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: {cls.COLORS['primary_400']};
        }}
        
        /* === LOADING STATES === */
        .stSpinner {{
            color: {cls.COLORS['primary_400']} !important;
        }}
        
        /* === SMOOTH ANIMATIONS === */
        * {{
            transition: background-color 0.2s ease, border-color 0.2s ease, color 0.2s ease;
        }}
        
        /* === UTILITY CLASSES === */
        .text-center {{ text-align: center; }}
        .text-left {{ text-align: left; }}
        .text-right {{ text-align: right; }}
        
        .font-medium {{ font-weight: {cls.TYPOGRAPHY['font_medium']}; }}
        .font-semibold {{ font-weight: {cls.TYPOGRAPHY['font_semibold']}; }}
        .font-bold {{ font-weight: {cls.TYPOGRAPHY['font_bold']}; }}
        
        .text-primary {{ color: {cls.COLORS['primary_400']} !important; }}
        .text-success {{ color: {cls.COLORS['success_400']} !important; }}
        .text-warning {{ color: {cls.COLORS['warning_400']} !important; }}
        .text-error {{ color: {cls.COLORS['error_400']} !important; }}
        
        .text-white {{ color: {cls.COLORS['text_primary']} !important; }}
        .text-muted {{ color: {cls.COLORS['text_muted']} !important; }}
        
        /* === RESPONSIVE DESIGN === */
        @media (max-width: 768px) {{
            .main-header {{
                padding: {cls.SPACING['6']};
            }}
            
            .main-header h1 {{
                font-size: {cls.TYPOGRAPHY['text_3xl']};
            }}
            
            .info-card {{
                padding: {cls.SPACING['4']};
            }}
            
            .upload-section {{
                padding: {cls.SPACING['6']};
            }}
        }}
        </style>
        """ + get_animation_css() + get_chart_css()
    
    @classmethod
    def get_component_html(cls, component_type: str, title: str, content: str, **kwargs) -> str:
        """Generate HTML for common UI components with dark theme"""
        
        if component_type == "header":
            return f"""
            <div class="main-header">
                <h1>{title}</h1>
                <p>{content}</p>
            </div>
            """
        
        elif component_type == "info_card":
            return f"""
            <div class="info-card">
                <h3>{title}</h3>
                <div>{content}</div>
            </div>
            """
        
        elif component_type == "metric_card":
            value = kwargs.get('value', '')
            subtitle = kwargs.get('subtitle', '')
            return f"""
            <div class="metric-container">
                <div style="font-size: {cls.TYPOGRAPHY['text_3xl']}; font-weight: {cls.TYPOGRAPHY['font_bold']}; 
                           color: {cls.COLORS['text_primary']}; margin-bottom: {cls.SPACING['1']};">
                    {value}
                </div>
                <div style="font-size: {cls.TYPOGRAPHY['text_sm']}; color: {cls.COLORS['text_muted']};">
                    {subtitle}
                </div>
            </div>
            """
        
        elif component_type == "upload_section":
            return f"""
            <div class="upload-section">
                <h3>{title}</h3>
                <p>{content}</p>
            </div>
            """
        
        elif component_type == "success_alert":
            return f"""
            <div style="background: {cls.COLORS['success_900']}; border: 1px solid {cls.COLORS['success_600']}; 
                        border-radius: {cls.RADIUS['md']}; padding: {cls.SPACING['4']}; margin: {cls.SPACING['4']} 0;">
                <h4 style="color: {cls.COLORS['success_400']}; margin: 0 0 {cls.SPACING['2']} 0;">{title}</h4>
                <p style="color: {cls.COLORS['success_400']}; margin: 0;">{content}</p>
            </div>
            """
        
        elif component_type == "status_indicator":
            status_type = kwargs.get('status', 'info')
            colors_map = {
                'success': (cls.COLORS['success_900'], cls.COLORS['success_400']),
                'warning': (cls.COLORS['warning_900'], cls.COLORS['warning_400']),
                'error': (cls.COLORS['error_900'], cls.COLORS['error_400']),
                'info': (cls.COLORS['info_900'], cls.COLORS['info_400']),
            }
            bg_color, text_color = colors_map.get(status_type, colors_map['info'])
            
            return f"""
            <div style="display: inline-flex; align-items: center; gap: {cls.SPACING['2']}; 
                        background: {bg_color}; color: {text_color}; padding: {cls.SPACING['2']} {cls.SPACING['3']}; 
                        border-radius: {cls.RADIUS['full']}; font-size: {cls.TYPOGRAPHY['text_sm']}; 
                        font-weight: {cls.TYPOGRAPHY['font_medium']};">
                {title}: {content}
            </div>
            """
        
        elif component_type == "sidebar_header":
            icon = kwargs.get('icon', '')
            subtitle = kwargs.get('subtitle', '')
            return f"""
            <div style="text-align: center; padding: {cls.SPACING['4']} 0; border-bottom: 1px solid {cls.COLORS['border_light']}; margin-bottom: {cls.SPACING['4']};">
                <h2 style="color: {cls.COLORS['text_primary']}; margin-bottom: {cls.SPACING['2']}; font-weight: {cls.TYPOGRAPHY['font_semibold']};">
                    {icon} {title}
                </h2>
                <p style="color: {cls.COLORS['text_muted']}; font-size: {cls.TYPOGRAPHY['text_sm']}; margin: 0;">
                    {subtitle}
                </p>
            </div>
            """
        
        else:
            return f"""
            <div class="info-card">
                <h3>{title}</h3>
                <div>{content}</div>
            </div>
            """
    
    @classmethod
    def get_quality_score_html(cls, score: float) -> str:
        """Generate HTML for data quality score display"""
        if score >= 90:
            color = cls.COLORS['success_400']
            bg_color = cls.COLORS['success_900']
            status = "Excellent"
        elif score >= 70:
            color = cls.COLORS['warning_400']
            bg_color = cls.COLORS['warning_900']
            status = "Good"
        else:
            color = cls.COLORS['error_400']
            bg_color = cls.COLORS['error_900']
            status = "Needs Review"
        
        return f"""
        <div style="background: {bg_color}; border: 1px solid {color}; border-radius: {cls.RADIUS['md']}; 
                    padding: {cls.SPACING['4']}; text-align: center;">
            <div style="font-size: {cls.TYPOGRAPHY['text_3xl']}; font-weight: {cls.TYPOGRAPHY['font_bold']}; 
                       color: {color}; margin-bottom: {cls.SPACING['1']};">
                {score:.0f}%
            </div>
            <div style="font-size: {cls.TYPOGRAPHY['text_sm']}; color: {color}; font-weight: {cls.TYPOGRAPHY['font_medium']};">
                Data Quality: {status}
            </div>
        </div>
        """
    
    @classmethod
    def get_plotly_theme(cls) -> dict:
        """Get Plotly theme configuration for dark mode charts"""
        return get_dark_plotly_theme()

# Create dark theme instance
dark_theme = DarkProfessionalTheme()