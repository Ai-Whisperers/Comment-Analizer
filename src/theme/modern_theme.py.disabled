"""
Modern Professional Theme for Personal Paraguay Comments Analysis Platform
Implements contemporary flat design with proper visual hierarchy and accessibility
Based on comprehensive UX critique and modern design principles
"""

class ModernProfessionalTheme:
    """
    Modern professional theme addressing all visual hierarchy and UX issues
    Implements flat design, proper typography scale, and neutral color palette
    """
    
    # Modern neutral color palette with strategic accent colors
    COLORS = {
        # Neutral foundation (primary palette)
        'neutral_50': '#f8fafc',    # Background primary
        'neutral_100': '#f1f5f9',   # Background secondary  
        'neutral_200': '#e2e8f0',   # Border light
        'neutral_300': '#cbd5e1',   # Border medium
        'neutral_400': '#94a3b8',   # Text muted
        'neutral_500': '#64748b',   # Text secondary
        'neutral_600': '#475569',   # Text primary
        'neutral_700': '#334155',   # Text dark
        'neutral_800': '#1e293b',   # Sidebar/header text
        'neutral_900': '#0f172a',   # Maximum contrast
        
        # Strategic accent colors (minimal usage)
        'primary_500': '#3b82f6',   # Primary actions only
        'primary_600': '#2563eb',   # Primary hover
        'primary_700': '#1d4ed8',   # Primary active
        'primary_50': '#eff6ff',    # Primary background
        'primary_100': '#dbeafe',   # Primary background light
        
        # Semantic colors (status indicators)
        'success_500': '#22c55e',   # Success actions
        'success_50': '#f0fdf4',    # Success background
        'success_700': '#15803d',   # Success text
        
        'warning_500': '#f59e0b',   # Warning actions
        'warning_50': '#fffbeb',    # Warning background
        'warning_700': '#a16207',   # Warning text
        
        'error_500': '#ef4444',     # Error actions
        'error_50': '#fef2f2',      # Error background
        'error_700': '#b91c1c',     # Error text
        
        # Pure colors for extreme contrast
        'white': '#ffffff',
        'black': '#000000',
    }
    
    # Systematic typography scale (major third - 1.25)
    TYPOGRAPHY = {
        'font_family': '"Inter", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
        'font_family_mono': '"JetBrains Mono", "Fira Code", monospace',
        
        # Type scale (major third progression)
        'text_xs': '0.75rem',       # 12px - captions, fine print
        'text_sm': '0.875rem',      # 14px - secondary text
        'text_base': '1rem',        # 16px - body text
        'text_lg': '1.125rem',      # 18px - large body
        'text_xl': '1.25rem',       # 20px - small headings
        'text_2xl': '1.5rem',       # 24px - headings h3
        'text_3xl': '1.875rem',     # 30px - headings h2
        'text_4xl': '2.25rem',      # 36px - headings h1
        'text_5xl': '3rem',         # 48px - display
        
        # Font weights
        'font_normal': '400',
        'font_medium': '500',
        'font_semibold': '600',
        'font_bold': '700',
        
        # Line heights
        'leading_tight': '1.25',    # Headlines
        'leading_normal': '1.5',    # Body text
        'leading_relaxed': '1.625', # Paragraphs
        
        # Letter spacing
        'tracking_tight': '-0.025em',
        'tracking_normal': '0em',
        'tracking_wide': '0.025em',
    }
    
    # Consistent spacing system (base-8)
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
    
    # Minimal border radius system
    RADIUS = {
        'none': '0',
        'sm': '0.25rem',    # 4px - buttons, inputs
        'md': '0.375rem',   # 6px - cards
        'lg': '0.5rem',     # 8px - large components
        'full': '9999px',   # Pills only
    }
    
    # Subtle elevation system (maximum 2 levels)
    SHADOWS = {
        'none': 'none',
        'sm': '0 1px 2px 0 rgb(0 0 0 / 0.05)',           # Subtle
        'md': '0 4px 6px -1px rgb(0 0 0 / 0.1)',         # Interactive elements
        'lg': '0 10px 15px -3px rgb(0 0 0 / 0.1)',       # Elevated cards (rarely used)
    }
    
    @classmethod
    def get_main_css(cls) -> str:
        """Get the main CSS styling implementing modern flat design principles"""
        return f"""
        <style>
        /* Import modern fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
        
        /* === FOUNDATION === */
        .stApp {{
            font-family: {cls.TYPOGRAPHY['font_family']};
            color: {cls.COLORS['neutral_700']};
            background-color: {cls.COLORS['neutral_50']};
            line-height: {cls.TYPOGRAPHY['leading_normal']};
        }}
        
        /* === TYPOGRAPHY HIERARCHY === */
        h1 {{
            font-size: {cls.TYPOGRAPHY['text_4xl']};
            font-weight: {cls.TYPOGRAPHY['font_bold']};
            color: {cls.COLORS['neutral_900']};
            line-height: {cls.TYPOGRAPHY['leading_tight']};
            margin-bottom: {cls.SPACING['6']};
            letter-spacing: {cls.TYPOGRAPHY['tracking_tight']};
        }}
        
        h2 {{
            font-size: {cls.TYPOGRAPHY['text_3xl']};
            font-weight: {cls.TYPOGRAPHY['font_semibold']};
            color: {cls.COLORS['neutral_800']};
            line-height: {cls.TYPOGRAPHY['leading_tight']};
            margin-bottom: {cls.SPACING['4']};
        }}
        
        h3 {{
            font-size: {cls.TYPOGRAPHY['text_2xl']};
            font-weight: {cls.TYPOGRAPHY['font_semibold']};
            color: {cls.COLORS['neutral_800']};
            line-height: {cls.TYPOGRAPHY['leading_tight']};
            margin-bottom: {cls.SPACING['3']};
        }}
        
        h4 {{
            font-size: {cls.TYPOGRAPHY['text_xl']};
            font-weight: {cls.TYPOGRAPHY['font_medium']};
            color: {cls.COLORS['neutral_700']};
            margin-bottom: {cls.SPACING['2']};
        }}
        
        p {{
            font-size: {cls.TYPOGRAPHY['text_base']};
            color: {cls.COLORS['neutral_600']};
            line-height: {cls.TYPOGRAPHY['leading_relaxed']};
            margin-bottom: {cls.SPACING['4']};
        }}
        
        /* === FLAT HEADER (NO GRADIENT) === */
        .main-header {{
            background: {cls.COLORS['white']};
            border: 1px solid {cls.COLORS['neutral_200']};
            border-radius: {cls.RADIUS['lg']};
            padding: {cls.SPACING['8']};
            margin-bottom: {cls.SPACING['8']};
            box-shadow: {cls.SHADOWS['sm']};
        }}
        
        .main-header h1 {{
            color: {cls.COLORS['neutral_900']};
            margin: 0 0 {cls.SPACING['2']} 0;
            font-size: {cls.TYPOGRAPHY['text_4xl']};
            font-weight: {cls.TYPOGRAPHY['font_bold']};
        }}
        
        .main-header p {{
            color: {cls.COLORS['neutral_600']};
            margin: 0;
            font-size: {cls.TYPOGRAPHY['text_lg']};
            font-weight: {cls.TYPOGRAPHY['font_normal']};
        }}
        
        /* === CARD COMPONENTS (MINIMAL ELEVATION) === */
        .info-card {{
            background: {cls.COLORS['white']};
            border: 1px solid {cls.COLORS['neutral_200']};
            border-radius: {cls.RADIUS['md']};
            padding: {cls.SPACING['6']};
            margin-bottom: {cls.SPACING['4']};
            box-shadow: {cls.SHADOWS['sm']};
            transition: border-color 0.2s ease;
        }}
        
        .info-card:hover {{
            border-color: {cls.COLORS['neutral_300']};
        }}
        
        .info-card h3 {{
            color: {cls.COLORS['neutral_900']};
            margin: 0 0 {cls.SPACING['3']} 0;
            font-size: {cls.TYPOGRAPHY['text_xl']};
            font-weight: {cls.TYPOGRAPHY['font_semibold']};
        }}
        
        .info-card p {{
            color: {cls.COLORS['neutral_600']};
            margin: 0;
        }}
        
        /* === METRIC CARDS === */
        .metric-container {{
            background: {cls.COLORS['white']};
            border: 1px solid {cls.COLORS['neutral_200']};
            border-radius: {cls.RADIUS['md']};
            padding: {cls.SPACING['4']};
            box-shadow: {cls.SHADOWS['sm']};
        }}
        
        /* === UPLOAD SECTION (CLEAN DASHED BORDER) === */
        .upload-section {{
            background: {cls.COLORS['neutral_50']};
            border: 2px dashed {cls.COLORS['neutral_300']};
            border-radius: {cls.RADIUS['lg']};
            padding: {cls.SPACING['8']};
            text-align: center;
            transition: border-color 0.2s ease, background-color 0.2s ease;
        }}
        
        .upload-section:hover {{
            border-color: {cls.COLORS['primary_500']};
            background: {cls.COLORS['primary_50']};
        }}
        
        .upload-section h3 {{
            color: {cls.COLORS['neutral_800']};
            margin-bottom: {cls.SPACING['2']};
        }}
        
        .upload-section p {{
            color: {cls.COLORS['neutral_600']};
            margin-bottom: 0;
        }}
        
        /* === BUTTONS (ACTION-ORIENTED, NO GRADIENTS) === */
        .stButton > button {{
            background: {cls.COLORS['primary_500']};
            color: {cls.COLORS['white']};
            border: none;
            border-radius: {cls.RADIUS['sm']};
            padding: {cls.SPACING['3']} {cls.SPACING['5']};
            font-weight: {cls.TYPOGRAPHY['font_medium']};
            font-size: {cls.TYPOGRAPHY['text_sm']};
            letter-spacing: {cls.TYPOGRAPHY['tracking_wide']};
            transition: background-color 0.2s ease, box-shadow 0.2s ease;
            box-shadow: {cls.SHADOWS['sm']};
        }}
        
        .stButton > button:hover {{
            background: {cls.COLORS['primary_600']};
            box-shadow: {cls.SHADOWS['md']};
        }}
        
        .stButton > button:active {{
            background: {cls.COLORS['primary_700']};
            box-shadow: {cls.SHADOWS['sm']};
        }}
        
        /* === SIDEBAR (HIGH CONTRAST) === */
        [data-testid="stSidebar"] {{
            background-color: {cls.COLORS['neutral_800']};
            border-right: 1px solid {cls.COLORS['neutral_700']};
        }}
        
        [data-testid="stSidebar"] .stMarkdown h1,
        [data-testid="stSidebar"] .stMarkdown h2,
        [data-testid="stSidebar"] .stMarkdown h3 {{
            color: {cls.COLORS['white']} !important;
        }}
        
        [data-testid="stSidebar"] .stMarkdown p,
        [data-testid="stSidebar"] label {{
            color: {cls.COLORS['neutral_300']} !important;
        }}
        
        [data-testid="stSidebar"] .stSelectbox > div > div {{
            background-color: {cls.COLORS['neutral_700']};
            border: 1px solid {cls.COLORS['neutral_600']};
            color: {cls.COLORS['white']};
        }}
        
        /* === FORM ELEMENTS === */
        .stSelectbox > div > div,
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {{
            background-color: {cls.COLORS['white']};
            border: 1px solid {cls.COLORS['neutral_300']};
            border-radius: {cls.RADIUS['sm']};
            color: {cls.COLORS['neutral_900']};
            font-size: {cls.TYPOGRAPHY['text_base']};
        }}
        
        .stSelectbox > div > div:focus-within,
        .stTextInput > div > div:focus-within,
        .stTextArea > div > div:focus-within {{
            border-color: {cls.COLORS['primary_500']};
            box-shadow: 0 0 0 3px {cls.COLORS['primary_100']};
        }}
        
        /* === METRICS === */
        .stMetric {{
            background: {cls.COLORS['white']};
            border: 1px solid {cls.COLORS['neutral_200']};
            border-radius: {cls.RADIUS['md']};
            padding: {cls.SPACING['4']};
        }}
        
        .stMetric label {{
            color: {cls.COLORS['neutral_600']} !important;
            font-size: {cls.TYPOGRAPHY['text_sm']} !important;
            font-weight: {cls.TYPOGRAPHY['font_medium']} !important;
        }}
        
        .stMetric [data-testid="metric-value"] {{
            color: {cls.COLORS['neutral_900']} !important;
            font-size: {cls.TYPOGRAPHY['text_2xl']} !important;
            font-weight: {cls.TYPOGRAPHY['font_semibold']} !important;
        }}
        
        /* === ALERTS (SEMANTIC COLORS) === */
        .stAlert {{
            border-radius: {cls.RADIUS['md']};
            border: none;
            font-weight: {cls.TYPOGRAPHY['font_medium']};
        }}
        
        .stSuccess {{
            background-color: {cls.COLORS['success_50']};
            color: {cls.COLORS['success_700']};
        }}
        
        .stWarning {{
            background-color: {cls.COLORS['warning_50']};
            color: {cls.COLORS['warning_700']};
        }}
        
        .stError {{
            background-color: {cls.COLORS['error_50']};
            color: {cls.COLORS['error_700']};
        }}
        
        /* === DATA TABLES === */
        .stDataFrame {{
            border: 1px solid {cls.COLORS['neutral_200']};
            border-radius: {cls.RADIUS['md']};
            overflow: hidden;
        }}
        
        .stDataFrame th {{
            background-color: {cls.COLORS['neutral_100']} !important;
            color: {cls.COLORS['neutral_800']} !important;
            font-weight: {cls.TYPOGRAPHY['font_semibold']} !important;
            border-bottom: 1px solid {cls.COLORS['neutral_200']} !important;
        }}
        
        .stDataFrame td {{
            background-color: {cls.COLORS['white']} !important;
            color: {cls.COLORS['neutral_700']} !important;
            border-bottom: 1px solid {cls.COLORS['neutral_100']} !important;
        }}
        
        /* === FILE UPLOADER === */
        .stFileUploader {{
            background-color: {cls.COLORS['white']};
            border: 2px dashed {cls.COLORS['neutral_300']};
            border-radius: {cls.RADIUS['lg']};
            padding: {cls.SPACING['6']};
        }}
        
        .stFileUploader:hover {{
            border-color: {cls.COLORS['primary_500']};
            background-color: {cls.COLORS['primary_50']};
        }}
        
        .stFileUploader label,
        .stFileUploader span {{
            color: {cls.COLORS['neutral_700']} !important;
        }}
        
        /* === PROGRESS BARS === */
        .stProgress > div > div > div {{
            background: {cls.COLORS['primary_500']};
        }}
        
        /* === CODE BLOCKS === */
        .stCode {{
            background-color: {cls.COLORS['neutral_100']};
            border: 1px solid {cls.COLORS['neutral_200']};
            border-radius: {cls.RADIUS['sm']};
            color: {cls.COLORS['neutral_800']};
            font-family: {cls.TYPOGRAPHY['font_family_mono']};
        }}
        
        /* === TABS === */
        .stTabs [data-baseweb="tab-list"] {{
            gap: {cls.SPACING['1']};
            background-color: {cls.COLORS['neutral_100']};
            border-radius: {cls.RADIUS['md']};
            padding: {cls.SPACING['1']};
        }}
        
        .stTabs [data-baseweb="tab"] {{
            background-color: transparent;
            border-radius: {cls.RADIUS['sm']};
            color: {cls.COLORS['neutral_600']};
            font-weight: {cls.TYPOGRAPHY['font_medium']};
            padding: {cls.SPACING['2']} {cls.SPACING['4']};
        }}
        
        .stTabs [aria-selected="true"] {{
            background-color: {cls.COLORS['white']};
            color: {cls.COLORS['neutral_900']};
            box-shadow: {cls.SHADOWS['sm']};
        }}
        
        /* === EXPANDERS === */
        .streamlit-expanderHeader {{
            background-color: {cls.COLORS['neutral_100']};
            border: 1px solid {cls.COLORS['neutral_200']};
            border-radius: {cls.RADIUS['md']};
        }}
        
        /* === SCROLL BARS === */
        ::-webkit-scrollbar {{
            width: 6px;
            height: 6px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: {cls.COLORS['neutral_100']};
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: {cls.COLORS['neutral_400']};
            border-radius: 3px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: {cls.COLORS['neutral_500']};
        }}
        
        /* === UTILITY CLASSES === */
        .text-center {{ text-align: center; }}
        .text-left {{ text-align: left; }}
        .text-right {{ text-align: right; }}
        
        .font-medium {{ font-weight: {cls.TYPOGRAPHY['font_medium']}; }}
        .font-semibold {{ font-weight: {cls.TYPOGRAPHY['font_semibold']}; }}
        .font-bold {{ font-weight: {cls.TYPOGRAPHY['font_bold']}; }}
        
        .text-primary {{ color: {cls.COLORS['primary_500']}; }}
        .text-success {{ color: {cls.COLORS['success_500']}; }}
        .text-warning {{ color: {cls.COLORS['warning_500']}; }}
        .text-error {{ color: {cls.COLORS['error_500']}; }}
        
        .text-neutral-600 {{ color: {cls.COLORS['neutral_600']}; }}
        .text-neutral-700 {{ color: {cls.COLORS['neutral_700']}; }}
        .text-neutral-900 {{ color: {cls.COLORS['neutral_900']}; }}
        
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
        """
    
    @classmethod
    def get_component_html(cls, component_type: str, title: str, content: str, **kwargs) -> str:
        """Generate HTML for common UI components with modern flat design"""
        
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
                           color: {cls.COLORS['neutral_900']}; margin-bottom: {cls.SPACING['1']};">
                    {value}
                </div>
                <div style="font-size: {cls.TYPOGRAPHY['text_sm']}; color: {cls.COLORS['neutral_600']};">
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
            <div style="background: {cls.COLORS['success_50']}; border: 1px solid {cls.COLORS['success_500']}; 
                        border-radius: {cls.RADIUS['md']}; padding: {cls.SPACING['4']}; margin: {cls.SPACING['4']} 0;">
                <h4 style="color: {cls.COLORS['success_700']}; margin: 0 0 {cls.SPACING['2']} 0;">{title}</h4>
                <p style="color: {cls.COLORS['success_700']}; margin: 0;">{content}</p>
            </div>
            """
        
        elif component_type == "status_indicator":
            status_type = kwargs.get('status', 'info')
            colors_map = {
                'success': (cls.COLORS['success_50'], cls.COLORS['success_500']),
                'warning': (cls.COLORS['warning_50'], cls.COLORS['warning_500']),
                'error': (cls.COLORS['error_50'], cls.COLORS['error_500']),
                'info': (cls.COLORS['primary_50'], cls.COLORS['primary_500']),
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
            color = cls.COLORS['success_500']
            bg_color = cls.COLORS['success_50']
            status = "Excellent"
        elif score >= 70:
            color = cls.COLORS['warning_500']
            bg_color = cls.COLORS['warning_50']
            status = "Good"
        else:
            color = cls.COLORS['error_500']
            bg_color = cls.COLORS['error_50']
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

# Create modern theme instance
modern_theme = ModernProfessionalTheme()