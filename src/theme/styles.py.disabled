"""
Professional Theme and Styling Module for Personal Paraguay Comments Analysis Platform
Centralized CSS styling and theme management for consistent UI across all pages
"""

class ProfessionalTheme:
    """
    Professional theme configuration for the Personal Paraguay Comments Analysis Platform
    Provides consistent styling, colors, and layout components
    """
    
    # Enhanced color palette
    COLORS = {
        # Primary brand colors - Updated for richer gradients
        'primary_dark': '#1a365d',      # Deeper blue
        'primary_medium': '#2563eb',    # Vibrant blue  
        'primary_light': '#60a5fa',     # Light blue
        'primary_ultra_light': '#dbeafe', # Ultra light blue
        'accent': '#7c3aed',            # Purple accent
        
        # Text colors - Enhanced for better contrast
        'text_primary': '#0a0e17',      # Almost black for maximum readability
        'text_secondary': '#293241',    # Darker gray
        'text_muted': '#4b5563',        # Medium gray (darker than before)
        'text_light': '#6b7280',        # Light gray (darker than before)
        'text_on_dark': '#ffffff',      # Pure white for dark backgrounds
        
        # Background colors - Soft non-white tones for better readability
        'bg_primary': '#f8f9fa',        # Very light gray instead of white
        'bg_secondary': '#f0f2f5',      # Light gray
        'bg_tertiary': '#e9ecef',       # Medium light gray
        'bg_highlight': '#e6f0f9',      # Soft blue tint
        'bg_card': '#f2f4f6',           # Card background with slight tint
        
        # Status colors - More vibrant
        'success': '#10b981',          # Emerald green
        'success_bg': '#d1fae5',       # Light green
        'success_text': '#065f46',     # Dark green
        'warning': '#f59e0b',          # Amber
        'warning_bg': '#fef3c7',       # Light amber
        'error': '#ef4444',            # Red
        'error_bg': '#fee2e2',         # Light red
        'info': '#3b82f6',             # Blue
        'info_bg': '#dbeafe',          # Light blue
        
        # Border and shadow - Enhanced depth
        'border_light': '#e5e7eb',     # Light border
        'border_medium': '#d1d5db',    # Medium border
        'border_focus': '#93c5fd',     # Focus border (light blue)
        'shadow_light': 'rgba(0, 0, 0, 0.05)',
        'shadow_medium': 'rgba(0, 0, 0, 0.08)',
        'shadow_large': 'rgba(0, 0, 0, 0.12)',
        'shadow_colored': 'rgba(37, 99, 235, 0.15)', # Blue-tinted shadow
        'glass_effect': 'rgba(255, 255, 255, 0.8)',  # For glassmorphism
    }
    
    # Typography - Enhanced with modern font pairing
    TYPOGRAPHY = {
        'font_family': '"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
        'font_family_heading': '"Outfit", "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
        'font_size_xxl': '3rem',        # Page titles
        'font_size_xl': '2.25rem',      # Section headers
        'font_size_lg': '1.5rem',       # Subsections
        'font_size_md': '1.125rem',     # Normal text
        'font_size_sm': '0.9375rem',    # Secondary text
        'font_size_xs': '0.8125rem',    # Auxiliary text
        'font_weight_light': '300',
        'font_weight_normal': '400',
        'font_weight_medium': '500',
        'font_weight_semibold': '600',
        'font_weight_bold': '700',
        'line_height_tight': '1.2',     # For headings
        'line_height_normal': '1.5',    # For body text
        'line_height_relaxed': '1.75',  # For paragraphs
        'letter_spacing_tight': '-0.01em',  # For headings
        'letter_spacing_wide': '0.01em'     # For buttons/small text
    }
    
    # Spacing and dimensions - More precise scale
    SPACING = {
        'xxs': '0.125rem',     # 2px
        'xs': '0.25rem',       # 4px
        'sm': '0.5rem',        # 8px
        'md': '1rem',          # 16px
        'lg': '1.5rem',        # 24px
        'xl': '2rem',          # 32px
        'xxl': '3rem',         # 48px
        '3xl': '4rem',         # 64px
        '4xl': '6rem',         # 96px
        'border_radius_xs': '4px',      # Small elements
        'border_radius_sm': '8px',      # Buttons, inputs
        'border_radius': '12px',        # Cards, sections
        'border_radius_lg': '16px',     # Large elements
        'border_radius_xl': '24px',     # Featured sections
        'border_radius_full': '9999px'  # Pills, badges
    }
    
    @classmethod
    def get_main_css(cls) -> str:
        """Get the main CSS styling for the application"""
        return f"""
        <style>
        /* Import enhanced fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700&display=swap');
        
        /* Global styling improvements - Updated background color */
        .stApp {{
            font-family: {cls.TYPOGRAPHY['font_family']};
            color: {cls.COLORS['text_primary']};
            line-height: {cls.TYPOGRAPHY['line_height_normal']};
            background-color: {cls.COLORS['bg_primary']};
        }}
        
        /* Add smooth scrolling and better focus styles */
        html {{
            scroll-behavior: smooth;
        }}
        
        :focus {{
            outline: 2px solid {cls.COLORS['border_focus']};
            outline-offset: 2px;
            transition: outline-offset 0.2s ease;
        }}
        
        /* Main header component - Enhanced with modern gradient and glassmorphism */
        .main-header {{
            background: linear-gradient(135deg, {cls.COLORS['primary_dark']} 0%, {cls.COLORS['primary_medium']} 60%, {cls.COLORS['accent']} 100%);
            padding: {cls.SPACING['lg']} {cls.SPACING['xl']};
            border-radius: {cls.SPACING['border_radius_lg']};
            margin-bottom: {cls.SPACING['xl']};
            box-shadow: 0 8px 20px {cls.COLORS['shadow_colored']}, 0 4px 6px {cls.COLORS['shadow_medium']};
            position: relative;
            overflow: hidden;
        }}
        
        /* Add subtle pattern overlay */
        .main-header:before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-image: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M11 18c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm48 25c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm-43-7c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm63 31c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM34 90c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm56-76c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM12 86c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm28-65c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm23-11c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-6 60c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm29 22c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zM32 63c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm57-13c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-9-21c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM60 91c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM35 41c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM12 60c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2z' fill='%23ffffff' fill-opacity='0.05' fill-rule='evenodd'/%3E%3C/svg%3E");
            opacity: 0.2;
        }}
        
        .main-header h1 {{
            color: {cls.COLORS['text_on_dark']};
            margin: 0;
            font-weight: {cls.TYPOGRAPHY['font_weight_semibold']};
            font-size: {cls.TYPOGRAPHY['font_size_xxl']};
            font-family: {cls.TYPOGRAPHY['font_family_heading']};
            letter-spacing: {cls.TYPOGRAPHY['letter_spacing_tight']};
            line-height: {cls.TYPOGRAPHY['line_height_tight']};
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);
            position: relative;
        }}
        
        .main-header p {{
            color: {cls.COLORS['text_on_dark']};
            margin: {cls.SPACING['sm']} 0 0 0;
            font-size: {cls.TYPOGRAPHY['font_size_md']};
            font-weight: {cls.TYPOGRAPHY['font_weight_normal']};
            opacity: 0.9;
            max-width: 600px;
            position: relative;
        }}
        
        /* Card components - Enhanced with modern styling */
        .info-card {{
            background: {cls.COLORS['bg_card']};
            padding: {cls.SPACING['lg']} {cls.SPACING['xl']};
            border-radius: {cls.SPACING['border_radius']};
            box-shadow: 0 4px 15px {cls.COLORS['shadow_light']}, 0 1px 3px {cls.COLORS['shadow_light']};
            margin-bottom: {cls.SPACING['lg']};
            border-top: 4px solid {cls.COLORS['primary_medium']};
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            position: relative;
        }}
        
        .info-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px {cls.COLORS['shadow_medium']}, 0 2px 4px {cls.COLORS['shadow_light']};
        }}
        
        /* Add subtle pattern to cards */
        .info-card::after {{
            content: '';
            position: absolute;
            top: 0;
            right: 0;
            width: 100px;
            height: 100px;
            background-image: url("data:image/svg+xml,%3Csvg width='52' height='26' viewBox='0 0 52 26' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%233b82f6' fill-opacity='0.05'%3E%3Cpath d='M10 10c0-2.21-1.79-4-4-4-3.314 0-6-2.686-6-6h2c0 2.21 1.79 4 4 4 3.314 0 6 2.686 6 6 0 2.21 1.79 4 4 4 3.314 0 6 2.686 6 6 0 2.21 1.79 4 4 4v2c-3.314 0-6-2.686-6-6 0-2.21-1.79-4-4-4-3.314 0-6-2.686-6-6zm25.464-1.95l8.486 8.486-1.414 1.414-8.486-8.486 1.414-1.414z' /%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
            opacity: 0.7;
            pointer-events: none;
        }}
        
        .metric-container {{
            background: {cls.COLORS['bg_card']};
            padding: {cls.SPACING['lg']} {cls.SPACING['lg']};
            border-radius: {cls.SPACING['border_radius_lg']};
            border-left: 4px solid {cls.COLORS['primary_medium']};
            box-shadow: 0 4px 12px {cls.COLORS['shadow_light']}, 0 1px 3px {cls.COLORS['shadow_light']};
            margin-bottom: {cls.SPACING['md']};
            transition: transform 0.2s ease;
        }}
        
        .metric-container:hover {{
            transform: translateY(-1px);
        }}
        
        /* Upload section styling - Enhanced with animation */
        .upload-section {{
            background: {cls.COLORS['bg_secondary']};
            padding: {cls.SPACING['xl']};
            border-radius: {cls.SPACING['border_radius_lg']};
            border: 2px dashed {cls.COLORS['primary_medium']};
            margin: {cls.SPACING['md']} 0;
            text-align: center;
            transition: all 0.2s ease;
            position: relative;
        }}
        
        .upload-section:hover {{
            border-color: {cls.COLORS['primary_dark']};
            background: {cls.COLORS['bg_highlight']};
        }}
        
        /* Add animated upload icon */
        .upload-section::before {{
            content: '⬆️';
            font-size: 1.5rem;
            display: block;
            margin-bottom: {cls.SPACING['md']};
            opacity: 0.7;
            animation: pulse 2s infinite ease-in-out;
        }}
        
        @keyframes pulse {{
            0% {{ transform: translateY(0); }}
            50% {{ transform: translateY(-5px); }}
            100% {{ transform: translateY(0); }}
        }}
        
        /* Status indicators */
        .status-indicator {{
            display: inline-flex;
            align-items: center;
            gap: {cls.SPACING['sm']};
            padding: {cls.SPACING['sm']} {cls.SPACING['md']};
            border-radius: 20px;
            font-weight: {cls.TYPOGRAPHY['font_weight_medium']};
            font-size: {cls.TYPOGRAPHY['font_size_sm']};
        }}
        
        .status-healthy {{
            background: {cls.COLORS['success_bg']};
            color: {cls.COLORS['success']};
        }}
        
        .status-warning {{
            background: {cls.COLORS['warning_bg']};
            color: {cls.COLORS['warning']};
        }}
        
        .status-error {{
            background: {cls.COLORS['error_bg']};
            color: {cls.COLORS['error']};
        }}
        
        /* Navigation styling */
        .navigation-card {{
            background: {cls.COLORS['bg_tertiary']};
            padding: {cls.SPACING['md']};
            border-radius: {cls.SPACING['border_radius_sm']};
            margin-top: {cls.SPACING['md']};
        }}
        
        /* Sidebar enhancements */
        .sidebar-header {{
            text-align: center;
            padding: {cls.SPACING['md']} 0;
        }}
        
        .sidebar-header h2 {{
            color: {cls.COLORS['primary_dark']};
            margin-bottom: {cls.SPACING['sm']};
            font-weight: {cls.TYPOGRAPHY['font_weight_semibold']};
        }}
        
        .sidebar-header p {{
            color: {cls.COLORS['text_muted']};
            font-size: {cls.TYPOGRAPHY['font_size_sm']};
            margin: 0;
        }}
        
        /* Form element improvements - Added darker backgrounds */
        .stSelectbox > div > div {{
            background-color: {cls.COLORS['bg_tertiary']};
            border: 1px solid {cls.COLORS['border_medium']};
            border-radius: {cls.SPACING['border_radius_sm']};
        }}
        
        .stTextInput > div > div > input {{
            background-color: {cls.COLORS['bg_tertiary']};
            border: 1px solid {cls.COLORS['border_medium']};
            border-radius: {cls.SPACING['border_radius_sm']};
            color: {cls.COLORS['text_primary']};
        }}
        
        .stTextArea > div > div > textarea {{
            background-color: {cls.COLORS['bg_tertiary']};
            border: 1px solid {cls.COLORS['border_medium']};
            border-radius: {cls.SPACING['border_radius_sm']};
            color: {cls.COLORS['text_primary']};
        }}
        
        /* Metric styling - Improved contrast */
        .stMetric {{
            background: {cls.COLORS['bg_tertiary']};
            padding: {cls.SPACING['md']};
            border-radius: {cls.SPACING['border_radius_sm']};
            box-shadow: 0 1px 3px {cls.COLORS['shadow_medium']};
        }}
        
        /* Ensure metric text is visible */
        .stMetric p, .stMetric label {{
            color: {cls.COLORS['text_primary']} !important;
            font-weight: {cls.TYPOGRAPHY['font_weight_medium']};
        }}
        
        /* Button improvements - Modern design with hover effects */
        .stButton > button {{
            background: linear-gradient(135deg, {cls.COLORS['primary_medium']} 0%, {cls.COLORS['primary_dark']} 100%);
            color: {cls.COLORS['bg_primary']};
            border: none;
            border-radius: {cls.SPACING['border_radius_full']};
            font-weight: {cls.TYPOGRAPHY['font_weight_medium']};
            padding: {cls.SPACING['sm']} {cls.SPACING['xl']};
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
            box-shadow: 0 2px 5px {cls.COLORS['shadow_light']};
            letter-spacing: {cls.TYPOGRAPHY['letter_spacing_wide']};
            position: relative;
            overflow: hidden;
        }}
        
        .stButton > button:hover {{
            box-shadow: 0 5px 15px {cls.COLORS['shadow_colored']};
            transform: translateY(-2px);
            background: linear-gradient(135deg, {cls.COLORS['primary_dark']} 0%, {cls.COLORS['accent']} 100%);
        }}
        
        /* Add subtle ripple effect */
        .stButton > button::after {{
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 5px;
            height: 5px;
            background: rgba(255, 255, 255, 0.5);
            opacity: 0;
            border-radius: 100%;
            transform: scale(1, 1) translate(-50%);
            transform-origin: 50% 50%;
        }}
        
        .stButton > button:focus::after {{
            animation: ripple 1s ease-out;
        }}
        
        @keyframes ripple {{
            0% {{ transform: scale(0, 0); opacity: 0.5; }}
            100% {{ transform: scale(20, 20); opacity: 0; }}
        }}
        
        /* Success/Warning/Error message styling - Enhanced */
        .stAlert {{
            border-radius: {cls.SPACING['border_radius_sm']};
            border: none;
            font-weight: {cls.TYPOGRAPHY['font_weight_medium']};
        }}
        
        /* Fix alert text visibility */
        .stAlert div[data-testid="stMarkdownContainer"] p {{
            color: inherit !important;
            font-weight: {cls.TYPOGRAPHY['font_weight_medium']};
        }}
        
        /* Data frame styling - Improved contrast */
        .stDataFrame {{
            border-radius: {cls.SPACING['border_radius_sm']};
            border: 1px solid {cls.COLORS['border_medium']};
        }}
        
        /* Improve data table contrast */
        .stDataFrame th {{
            background-color: {cls.COLORS['bg_tertiary']} !important;
            color: {cls.COLORS['text_primary']} !important;
            font-weight: {cls.TYPOGRAPHY['font_weight_semibold']} !important;
        }}
        
        .stDataFrame td {{
            background-color: {cls.COLORS['bg_primary']} !important;
            color: {cls.COLORS['text_primary']} !important;
        }}
        
        /* Progress bar styling */
        .stProgress > div > div > div {{
            background: linear-gradient(90deg, {cls.COLORS['primary_medium']} 0%, {cls.COLORS['primary_light']} 100%);
        }}
        
        /* Expander styling */
        .streamlit-expanderHeader {{
            background-color: {cls.COLORS['bg_secondary']};
            border-radius: {cls.SPACING['border_radius_sm']};
        }}
        
        /* Chart improvements */
        .stPlotlyChart {{
            border-radius: {cls.SPACING['border_radius_sm']};
            box-shadow: 0 1px 3px {cls.COLORS['shadow_light']};
        }}
        
        /* Typography improvements */
        h1, h2, h3, h4, h5, h6 {{
            font-family: {cls.TYPOGRAPHY['font_family']};
            color: {cls.COLORS['text_primary']};
            font-weight: {cls.TYPOGRAPHY['font_weight_semibold']};
        }}
        
        p {{
            font-family: {cls.TYPOGRAPHY['font_family']};
            line-height: {cls.TYPOGRAPHY['line_height_normal']};
            color: {cls.COLORS['text_secondary']};
        }}
        
        /* Code block styling - Darkened for better readability */
        .stCode {{
            background-color: {cls.COLORS['bg_tertiary']};
            border: 1px solid {cls.COLORS['border_medium']};
            border-radius: {cls.SPACING['border_radius_sm']};
            color: {cls.COLORS['text_primary']};
        }}
        
        /* Tab styling - Enhanced contrast */
        .stTabs [data-baseweb="tab-list"] {{
            gap: {cls.SPACING['sm']};
        }}
        
        .stTabs [data-baseweb="tab"] {{
            background-color: {cls.COLORS['bg_tertiary']};
            border-radius: {cls.SPACING['border_radius_sm']};
            color: {cls.COLORS['text_primary']};
            font-weight: {cls.TYPOGRAPHY['font_weight_medium']};
        }}
        
        .stTabs [aria-selected="true"] {{
            background-color: {cls.COLORS['primary_dark']};
            color: #ffffff;
        }}
        
        /* Loading spinner improvements */
        .stSpinner {{
            color: {cls.COLORS['primary_medium']};
        }}
        
                 /* Sidebar improvements - Darker background */
         .css-1d391kg {{
             background-color: {cls.COLORS['bg_tertiary']};
         }}
         
         /* Fix sidebar text visibility */
         [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] .stSelectbox label {{
             color: {cls.COLORS['text_primary']} !important;
         }}
        
        /* File uploader styling - Improved contrast */
        .stFileUploader {{
            background-color: {cls.COLORS['bg_tertiary']};
            border: 2px dashed {cls.COLORS['primary_medium']};
            border-radius: {cls.SPACING['border_radius']};
            padding: {cls.SPACING['lg']};
        }}
        
        /* Ensure all file uploader text is visible */
        .stFileUploader label, .stFileUploader span {{
            color: {cls.COLORS['text_primary']} !important;
        }}
        
        /* Custom utility classes */
        .text-center {{
            text-align: center;
        }}
        
        .text-left {{
            text-align: left;
        }}
        
        .text-right {{
            text-align: right;
        }}
        
        .font-weight-bold {{
            font-weight: {cls.TYPOGRAPHY['font_weight_bold']};
        }}
        
        .font-weight-medium {{
            font-weight: {cls.TYPOGRAPHY['font_weight_medium']};
        }}
        
        .text-primary {{
            color: {cls.COLORS['primary_medium']};
        }}
        
        .text-success {{
            color: {cls.COLORS['success']};
        }}
        
        .text-warning {{
            color: {cls.COLORS['warning']};
        }}
        
        .text-error {{
            color: {cls.COLORS['error']};
        }}
        
        .bg-gradient {{
            background: linear-gradient(90deg, {cls.COLORS['primary_dark']} 0%, {cls.COLORS['primary_medium']} 50%, {cls.COLORS['primary_light']} 100%);
        }}
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: {cls.COLORS['bg_secondary']};
            border-radius: 4px;
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: {cls.COLORS['primary_light']};
            border-radius: 4px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: {cls.COLORS['primary_medium']};
        }}
        
        /* Add loading animations */
        .stSpinner > div {{
            border-top-color: {cls.COLORS['primary_medium']} !important;
            animation-duration: 1.2s !important;
        }}
        
        /* Fade-in animations */
        .main-header, .info-card, .metric-container, .upload-section {{
            animation: fadeIn 0.5s ease-out;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        /* Mobile responsiveness - Enhanced */
        @media (max-width: 768px) {{
            .main-header {{
                padding: {cls.SPACING['md']};
            }}
            
            .main-header h1 {{
                font-size: {cls.TYPOGRAPHY['font_size_lg']};
            }}
            
            .info-card {{
                padding: {cls.SPACING['md']};
            }}
            
            .upload-section {{
                padding: {cls.SPACING['md']};
            }}
            
            /* Stack columns on mobile */
            .st-emotion-cache-1r6slb0 > .st-emotion-cache-16txtl3 {{
                flex-direction: column !important;
            }}
            
            /* Full-width elements on mobile */
            .st-emotion-cache-1r6slb0 > .st-emotion-cache-16txtl3 > .st-emotion-cache-1wmy9hl {{
                width: 100% !important;
            }}
        }}
        </style>
        """
    
    @classmethod
    def get_component_html(cls, component_type: str, title: str, content: str, **kwargs) -> str:
        """Generate HTML for common UI components"""
        
        if component_type == "header":
            return f"""
            <div class="main-header">
                <h1>{title}</h1>
                <p>{content}</p>
            </div>
            """
        
        elif component_type == "info_card":
            icon = kwargs.get('icon', '')
            return f"""
            <div class="info-card">
                <h3 style="color: {cls.COLORS['primary_dark']}; margin-bottom: {cls.SPACING['md']};">
                    {icon} {title}
                </h3>
                <div style="color: {cls.COLORS['text_secondary']}; line-height: {cls.TYPOGRAPHY['line_height_normal']};">
                    {content}
                </div>
            </div>
            """
        
        elif component_type == "metric_card":
            value = kwargs.get('value', '')
            subtitle = kwargs.get('subtitle', '')
            return f"""
            <div class="metric-container">
                <h3 style="color: {cls.COLORS['primary_medium']}; margin: 0; font-size: 2rem;">{value}</h3>
                <p style="color: {cls.COLORS['text_muted']}; margin: 0;">{subtitle}</p>
            </div>
            """
        
        elif component_type == "status_indicator":
            status_type = kwargs.get('status', 'info')  # healthy, warning, error, info
            return f"""
            <div class="status-indicator status-{status_type}">
                {title}: {content}
            </div>
            """
        
        elif component_type == "upload_section":
            return f"""
            <div class="upload-section">
                <h3 style="color: {cls.COLORS['text_primary']}; margin-bottom: {cls.SPACING['md']};">{title}</h3>
                <p style="color: {cls.COLORS['text_muted']}; margin-bottom: {cls.SPACING['lg']};">
                    {content}
                </p>
            </div>
            """
        
        elif component_type == "navigation_desc":
            return f"""
            <div class="navigation-card">
                <p style="margin: 0; color: {cls.COLORS['text_muted']}; font-size: {cls.TYPOGRAPHY['font_size_xs']};">
                    {content}
                </p>
            </div>
            """
        
        elif component_type == "sidebar_header":
            icon = kwargs.get('icon', '')
            subtitle = kwargs.get('subtitle', '')
            return f"""
            <div class="sidebar-header">
                <h2>{icon} {title}</h2>
                <p>{subtitle}</p>
            </div>
            """
        
        elif component_type == "success_alert":
            return f"""
            <div style="background: {cls.COLORS['success_bg']}; border: 1px solid {cls.COLORS['success']}; 
                        border-radius: {cls.SPACING['border_radius_sm']}; padding: {cls.SPACING['md']}; margin: {cls.SPACING['md']} 0;">
                <h3 style="color: {cls.COLORS['success']}; margin: 0;">{title}</h3>
                <p style="color: {cls.COLORS['success_text']}; margin: {cls.SPACING['sm']} 0 0 0;">
                    {content}
                </p>
            </div>
            """
        
        else:
            # Default card
            return f"""
            <div class="info-card">
                <h3>{title}</h3>
                <p>{content}</p>
            </div>
            """
    
    @classmethod
    def get_quality_score_html(cls, score: float) -> str:
        """Generate HTML for data quality score display"""
        if score >= 90:
            color = cls.COLORS['success']
            status = "Excellent"
        elif score >= 70:
            color = cls.COLORS['warning'] 
            status = "Good"
        else:
            color = cls.COLORS['error']
            status = "Needs Review"
        
        return f"""
        <div style="text-align: center; padding: {cls.SPACING['md']};">
            <h2 style="color: {color}; margin: 0;">{score:.0f}%</h2>
            <p style="color: {color}; margin: {cls.SPACING['sm']} 0; font-weight: {cls.TYPOGRAPHY['font_weight_semibold']};">
                Data Quality: {status}
            </p>
        </div>
        """

# Theme instance for easy import
theme = ProfessionalTheme()