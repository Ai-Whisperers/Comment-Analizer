"""
Enhanced Dark Professional Theme - Response to Visual Critique
Implements improved contrast, visual hierarchy, and modern design patterns
"""

from .animations import get_animation_css
from .chart_themes import get_chart_css, get_dark_plotly_theme


class EnhancedDarkTheme:
    """
    Enhanced dark theme addressing visual critique issues:
    - Improved contrast and visual hierarchy
    - Better typography scaling
    - Distinct card layouts with shadows
    - Accent colors for CTAs
    - Proper spacing and padding
    """
    
    # Enhanced color palette with better contrast layers
    COLORS = {
        # Background hierarchy (distinct layers for visual separation)
        'bg_primary': '#0f1419',        # Deepest background
        'bg_secondary': '#1d273b',      # Card backgrounds (higher contrast)
        'bg_tertiary': '#222f3e',       # Elevated elements
        'bg_quaternary': '#2c3e50',     # Highest elevation
        'bg_elevated': '#34495e',       # Interactive elements
        
        # Surface colors for cards and containers
        'surface_primary': '#1e2a3a',   # Main card surface
        'surface_secondary': '#253344', # Nested card surface
        'surface_elevated': '#2d3e4f',  # Hover states
        'surface_hover': '#354a5f',     # Hover surface color
        
        # Text hierarchy (improved readability)
        'text_primary': '#ffffff',      # Primary headings
        'text_secondary': '#e2e8f0',    # Body text (higher contrast)
        'text_muted': '#a0aec0',        # Secondary text
        'text_disabled': '#718096',     # Disabled text
        'text_inverse': '#1a202c',      # Text on light backgrounds
        
        # Enhanced accent colors with warm tones
        'accent_primary': '#4299e1',    # Primary blue (CTAs)
        'accent_secondary': '#38b2ac',  # Teal (secondary actions)  
        'accent_tertiary': '#9f7aea',   # Purple (highlights)
        'accent_warm': '#f59e0b',       # Warm amber for highlights
        'accent_success': '#10b981',    # Warmer green for success
        'accent_warning': '#f59e0b',    # Warm amber for warnings
        'accent_danger': '#ef4444',     # Warm red for errors
        
        # Sentiment-based colors for analysis
        'sentiment_positive': '#10b981', # Warm green for positive sentiment
        'sentiment_neutral': '#6b7280',  # Neutral gray
        'sentiment_negative': '#ef4444', # Warm red for negative sentiment
        'sentiment_mixed': '#f59e0b',    # Warm amber for mixed sentiment
        
        # Interactive states
        'interactive_default': '#4299e1',
        'interactive_hover': '#3182ce',
        'interactive_active': '#2c5aa0',
        'interactive_disabled': '#4a5568',
        
        # Semantic colors (enhanced contrast)
        'success_50': '#f0fff4',
        'success_400': '#68d391',
        'success_500': '#48bb78',
        'success_600': '#38a169',
        'success_900': '#1a202c',
        
        'warning_50': '#fffbeb',
        'warning_400': '#f6ad55',
        'warning_500': '#ed8936',
        'warning_600': '#dd6b20',
        'warning_900': '#1a202c',
        
        'error_50': '#fed7d7',
        'error_400': '#fc8181',
        'error_500': '#e53e3e',
        'error_600': '#c53030',
        'error_900': '#1a202c',
        
        'info_50': '#ebf8ff',
        'info_400': '#63b3ed',
        'info_500': '#4299e1',
        'info_600': '#3182ce',
        'info_900': '#1a202c',
        
        # Border colors (improved visibility)
        'border_light': '#4a5568',
        'border_medium': '#718096',
        'border_strong': '#a0aec0',
        'border_accent': '#4299e1',
        
        # Shadow colors (enhanced depth)
        'shadow_sm': 'rgba(0, 0, 0, 0.4)',
        'shadow_md': 'rgba(0, 0, 0, 0.5)',
        'shadow_lg': 'rgba(0, 0, 0, 0.6)',
        'shadow_xl': 'rgba(0, 0, 0, 0.7)',
        
        # Data visualization colors
        'chart_blue': '#4299e1',
        'chart_green': '#48bb78',
        'chart_orange': '#ed8936',
        'chart_red': '#e53e3e',
        'chart_purple': '#9f7aea',
        'chart_teal': '#38b2ac',
    }
    
    # Enhanced typography scale (addressing readability critique)
    TYPOGRAPHY = {
        'font_family': '\"Inter\", -apple-system, BlinkMacSystemFont, \"Segoe UI\", Roboto, sans-serif',
        'font_family_mono': '\"JetBrains Mono\", \"Fira Code\", Consolas, monospace',
        
        # Enhanced hierarchical type scale with clear visual weight
        'text_xs': '0.75rem',       # 12px (captions, meta)
        'text_sm': '0.875rem',      # 14px (labels, help text)
        'text_base': '1rem',        # 16px (body text)
        'text_lg': '1.125rem',      # 18px (emphasized body)
        'text_xl': '1.25rem',       # 20px (small headings)
        'text_2xl': '1.5rem',       # 24px (section headings)
        'text_3xl': '1.875rem',     # 30px (page headings)
        'text_4xl': '2.25rem',      # 36px (main titles)
        'text_5xl': '3rem',         # 48px (hero titles)
        
        # Font weights
        'font_light': '300',
        'font_normal': '400',
        'font_medium': '500',
        'font_semibold': '600',
        'font_bold': '700',
        'font_extrabold': '800',
        
        # Line heights (improved readability)
        'leading_tight': '1.25',
        'leading_normal': '1.5',
        'leading_relaxed': '1.625',
        'leading_loose': '1.75',
        
        # Letter spacing
        'tracking_tight': '-0.025em',
        'tracking_normal': '0em',
        'tracking_wide': '0.025em',
        'tracking_wider': '0.05em',
    }
    
    # Compact spacing system (reduced excessive padding)
    SPACING = {
        '0': '0',           # 0px
        '0.5': '0.125rem',  # 2px
        '1': '0.25rem',     # 4px
        '1.5': '0.375rem',  # 6px
        '2': '0.5rem',      # 8px
        '3': '0.75rem',     # 12px
        '4': '1rem',        # 16px
        '5': '1.25rem',     # 20px
        '6': '1.5rem',      # 24px
        '8': '2rem',        # 32px
        '10': '2.5rem',     # 40px
        '12': '3rem',       # 48px
        '16': '4rem',       # 64px
        '20': '5rem',       # 80px
        '24': '6rem',       # 96px
    }
    
    # Enhanced border radius system
    RADIUS = {
        'none': '0',
        'sm': '0.375rem',   # 6px
        'md': '0.5rem',     # 8px
        'lg': '0.75rem',    # 12px
        'xl': '1rem',       # 16px
        '2xl': '1.5rem',    # 24px
        'full': '9999px',
    }
    
    # Enhanced shadow system
    SHADOWS = {
        'none': 'none',
        'sm': f'0 1px 3px 0 {COLORS["shadow_sm"]}, 0 1px 2px 0 {COLORS["shadow_sm"]}',
        'md': f'0 4px 6px -1px {COLORS["shadow_md"]}, 0 2px 4px -1px {COLORS["shadow_sm"]}',
        'lg': f'0 10px 15px -3px {COLORS["shadow_lg"]}, 0 4px 6px -2px {COLORS["shadow_md"]}',
        'xl': f'0 20px 25px -5px {COLORS["shadow_xl"]}, 0 10px 10px -5px {COLORS["shadow_lg"]}',
        'inner': f'inset 0 2px 4px 0 {COLORS["shadow_md"]}',
    }
    
    @classmethod
    def get_main_css(cls) -> str:
        """Get the enhanced CSS with improved visual hierarchy"""
        return f"""
        <style>
        /* === ENHANCED DARK THEME === */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
        
        /* === ROOT VARIABLES === */
        :root {{
            --font-family: {cls.TYPOGRAPHY['font_family']};
            --font-family-mono: {cls.TYPOGRAPHY['font_family_mono']};
            
            /* Colors */
            --bg-primary: {cls.COLORS['bg_primary']};
            --bg-secondary: {cls.COLORS['bg_secondary']};
            --surface-primary: {cls.COLORS['surface_primary']};
            --text-primary: {cls.COLORS['text_primary']};
            --text-secondary: {cls.COLORS['text_secondary']};
            --accent-primary: {cls.COLORS['accent_primary']};
            --border-medium: {cls.COLORS['border_medium']};
            
            /* Spacing */
            --spacing-2: {cls.SPACING['2']};
            --spacing-4: {cls.SPACING['4']};
            --spacing-6: {cls.SPACING['6']};
            --spacing-8: {cls.SPACING['8']};
            
            /* Shadows */
            --shadow-md: {cls.SHADOWS['md']};
            --shadow-lg: {cls.SHADOWS['lg']};
        }}
        
        /* === FOUNDATION === */
        .stApp {{
            font-family: var(--font-family);
            color: var(--text-primary);
            background: linear-gradient(135deg, {cls.COLORS['bg_primary']} 0%, #0a0e17 100%);
            line-height: {cls.TYPOGRAPHY['leading_normal']};
            font-size: {cls.TYPOGRAPHY['text_base']};
        }}
        
        /* Remove any white backgrounds */
        * {{
            background-color: transparent !important;
        }}
        
        /* Re-apply structured backgrounds */
        .stApp,
        [data-testid=\"stAppViewContainer\"],
        [data-testid=\"stHeader\"],
        [data-testid=\"stToolbar\"] {{
            background: linear-gradient(135deg, {cls.COLORS['bg_primary']} 0%, #0a0e17 100%) !important;
        }}
        
        /* === ENHANCED TYPOGRAPHY === */
        h1, h2, h3, h4, h5, h6 {{
            color: {cls.COLORS['text_primary']} !important;
            font-family: var(--font-family);
            font-weight: {cls.TYPOGRAPHY['font_semibold']};
            line-height: {cls.TYPOGRAPHY['leading_tight']};
            margin-bottom: var(--spacing-4);
        }}
        
        h1 {{
            font-size: {cls.TYPOGRAPHY['text_4xl']};
            font-weight: {cls.TYPOGRAPHY['font_bold']};
            letter-spacing: {cls.TYPOGRAPHY['tracking_tight']};
            margin-bottom: var(--spacing-8);
        }}
        
        h2 {{
            font-size: {cls.TYPOGRAPHY['text_3xl']};
            margin-bottom: var(--spacing-6);
        }}
        
        h3 {{
            font-size: {cls.TYPOGRAPHY['text_2xl']};
            margin-bottom: var(--spacing-4);
        }}
        
        h4 {{
            font-size: {cls.TYPOGRAPHY['text_xl']};
            margin-bottom: var(--spacing-4);
        }}
        
        p, div, span, label {{
            color: {cls.COLORS['text_secondary']} !important;
            font-size: {cls.TYPOGRAPHY['text_base']};
            line-height: {cls.TYPOGRAPHY['leading_relaxed']};
        }}
        
        /* === ENHANCED CARDS AND CONTAINERS === */
        .enhanced-card {{
            background: {cls.COLORS['surface_primary']} !important;
            border: 1px solid {cls.COLORS['border_light']};
            border-radius: {cls.RADIUS['lg']};
            padding: var(--spacing-8);
            margin-bottom: var(--spacing-6);
            box-shadow: var(--shadow-md);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        .enhanced-card:hover {{
            border-color: {cls.COLORS['border_accent']};
            box-shadow: var(--shadow-lg);
            transform: translateY(-2px);
        }}
        
        .elevated-card {{
            background: {cls.COLORS['surface_secondary']} !important;
            border: 1px solid {cls.COLORS['border_medium']};
            border-radius: {cls.RADIUS['xl']};
            padding: var(--spacing-8);
            box-shadow: var(--shadow-lg);
        }}
        
        /* === ENHANCED HEADER === */
        .main-header {{
            background: linear-gradient(135deg, {cls.COLORS['surface_primary']} 0%, {cls.COLORS['surface_secondary']} 100%) !important;
            border: 1px solid {cls.COLORS['border_medium']};
            border-radius: {cls.RADIUS['xl']};
            padding: var(--spacing-8);
            margin-bottom: var(--spacing-8);
            box-shadow: var(--shadow-lg);
            position: relative;
            overflow: hidden;
        }}
        
        .main-header::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, {cls.COLORS['accent_primary']}, {cls.COLORS['accent_secondary']}, {cls.COLORS['accent_tertiary']});
        }}
        
        .main-header h1 {{
            color: {cls.COLORS['text_primary']} !important;
            margin: 0 0 var(--spacing-2) 0;
            font-size: {cls.TYPOGRAPHY['text_4xl']};
        }}
        
        .main-header p {{
            color: {cls.COLORS['text_muted']} !important;
            margin: 0;
            font-size: {cls.TYPOGRAPHY['text_lg']};
        }}
        
        /* === ENHANCED BUTTONS (STRENGTHENED CTA STYLING) === */
        
        /* Primary CTA Buttons - Maximum Visual Impact */
        .stButton > button {{
            background: linear-gradient(135deg, {cls.COLORS['accent_primary']} 0%, {cls.COLORS['interactive_hover']} 100%) !important;
            color: {cls.COLORS['text_primary']} !important;
            border: none !important;
            border-radius: {cls.RADIUS['lg']} !important;
            padding: {cls.SPACING['5']} {cls.SPACING['8']} !important;
            font-weight: {cls.TYPOGRAPHY['font_bold']} !important;
            font-size: {cls.TYPOGRAPHY['text_lg']} !important;
            letter-spacing: {cls.TYPOGRAPHY['tracking_wide']} !important;
            line-height: {cls.TYPOGRAPHY['leading_tight']} !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 4px 14px rgba(66, 153, 225, 0.4), 0 2px 6px rgba(0, 0, 0, 0.1) !important;
            position: relative !important;
            overflow: hidden !important;
            cursor: pointer !important;
            min-height: 3.5rem !important;
            text-transform: none !important;
            width: 100% !important;
        }}
        
        /* Enhanced hover with dramatic glow effect */
        .stButton > button:hover {{
            background: linear-gradient(135deg, {cls.COLORS['interactive_hover']} 0%, {cls.COLORS['interactive_active']} 100%) !important;
            box-shadow: 0 8px 25px rgba(66, 153, 225, 0.5), 0 4px 12px rgba(0, 0, 0, 0.15) !important;
            transform: translateY(-3px) scale(1.03) !important;
        }}
        
        .stButton > button:active {{
            background: {cls.COLORS['interactive_active']} !important;
            transform: translateY(-1px) scale(1.01) !important;
            box-shadow: 0 4px 12px rgba(66, 153, 225, 0.4) !important;
        }}
        
        /* Focus state for accessibility */
        .stButton > button:focus {{
            outline: 3px solid rgba(66, 153, 225, 0.5) !important;
            outline-offset: 2px !important;
        }}
        
        /* Secondary button style - Enhanced */
        .secondary-button {{
            background: linear-gradient(135deg, {cls.COLORS['surface_secondary']} 0%, {cls.COLORS['surface_elevated']} 100%) !important;
            border: 2px solid {cls.COLORS['accent_primary']} !important;
            color: {cls.COLORS['text_primary']} !important;
            padding: {cls.SPACING['4']} {cls.SPACING['8']} !important;
            font-size: {cls.TYPOGRAPHY['text_lg']} !important;
            font-weight: {cls.TYPOGRAPHY['font_semibold']} !important;
            border-radius: {cls.RADIUS['lg']} !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
            min-height: 3.25rem !important;
        }}
        
        .secondary-button:hover {{
            background: linear-gradient(135deg, {cls.COLORS['accent_primary']} 0%, {cls.COLORS['interactive_hover']} 100%) !important;
            border-color: {cls.COLORS['interactive_hover']} !important;
            color: {cls.COLORS['text_primary']} !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(66, 153, 225, 0.3) !important;
        }}
        
        /* Danger/Warning buttons for critical actions */
        .danger-button {{
            background: linear-gradient(135deg, #e53e3e 0%, #c53030 100%) !important;
            color: {cls.COLORS['text_primary']} !important;
            border: none !important;
            padding: {cls.SPACING['4']} {cls.SPACING['8']} !important;
            font-size: {cls.TYPOGRAPHY['text_lg']} !important;
            font-weight: {cls.TYPOGRAPHY['font_bold']} !important;
            border-radius: {cls.RADIUS['lg']} !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 4px 12px rgba(229, 62, 62, 0.4) !important;
            min-height: 3.25rem !important;
        }}
        
        .danger-button:hover {{
            background: linear-gradient(135deg, #c53030 0%, #9c2626 100%) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(229, 62, 62, 0.5) !important;
        }}
        
        /* Success buttons for positive actions */
        .success-button {{
            background: linear-gradient(135deg, #38a169 0%, #2f855a 100%) !important;
            color: {cls.COLORS['text_primary']} !important;
            border: none !important;
            padding: {cls.SPACING['4']} {cls.SPACING['8']} !important;
            font-size: {cls.TYPOGRAPHY['text_lg']} !important;
            font-weight: {cls.TYPOGRAPHY['font_bold']} !important;
            border-radius: {cls.RADIUS['lg']} !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 4px 12px rgba(56, 161, 105, 0.4) !important;
            min-height: 3.25rem !important;
        }}
        
        .success-button:hover {{
            background: linear-gradient(135deg, #2f855a 0%, #276749 100%) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(56, 161, 105, 0.5) !important;
        }}
        
        /* Large CTA for hero sections */
        .large-cta-button {{
            padding: {cls.SPACING['6']} {cls.SPACING['12']} !important;
            font-size: {cls.TYPOGRAPHY['text_xl']} !important;
            font-weight: {cls.TYPOGRAPHY['font_extrabold']} !important;
            min-height: 4rem !important;
            border-radius: {cls.RADIUS['xl']} !important;
            box-shadow: 0 8px 25px rgba(66, 153, 225, 0.5), 0 4px 12px rgba(0, 0, 0, 0.15) !important;
        }}
        
        .large-cta-button:hover {{
            transform: translateY(-4px) scale(1.05) !important;
            box-shadow: 0 12px 35px rgba(66, 153, 225, 0.6), 0 6px 18px rgba(0, 0, 0, 0.2) !important;
        }}
        
        /* Compact button for inline actions */
        .compact-button {{
            padding: {cls.SPACING['2']} {cls.SPACING['4']} !important;
            font-size: {cls.TYPOGRAPHY['text_base']} !important;
            min-height: 2.5rem !important;
            border-radius: {cls.RADIUS['md']} !important;
        }}
        
        /* === ENHANCED STREAMLIT DROPDOWN MENU (FIXING CRITICAL ISSUES) === */
        
        /* Fix main dropdown menu overflow and clipping */
        [data-testid="stDropdown"], 
        [data-testid="stMainMenu"],
        [data-baseweb="popover"] {{
            position: relative !important;
            z-index: 999999 !important;
            overflow: visible !important;
        }}
        
        /* Fix dropdown menu container - Enhanced backgrounds and visibility */
        [data-baseweb="popover"] > div,
        [role="menu"],
        [role="listbox"],
        .stSelectbox > div > div,
        .stMultiSelect > div > div,
        [data-baseweb="select"] > div {{
            background: {cls.COLORS['surface_primary']} !important;
            border: 2px solid {cls.COLORS['border_medium']} !important;
            border-radius: {cls.RADIUS['lg']} !important;
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.3), 0 6px 15px rgba(0, 0, 0, 0.15) !important;
            overflow: hidden !important;
            min-width: 200px !important;
            max-width: 300px !important;
            padding: {cls.SPACING['2']} 0 !important;
            margin: 0 !important;
            backdrop-filter: blur(8px) !important;
        }}
        
        /* Ensure ALL dropdown content has proper background */
        [data-baseweb="popover"] *,
        [role="menu"] *,
        [role="listbox"] *,
        .stSelectbox *,
        .stMultiSelect * {{
            background-color: inherit !important;
        }}
        
        /* Fix redundant menu list nesting - target all ul elements */
        [role="menu"] ul,
        [role="listbox"] ul,
        [data-baseweb="popover"] ul {{
            list-style: none !important;
            margin: 0 !important;
            padding: 0 !important;
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }}
        
        /* Fix menu items with enhanced visibility and consistent alignment */
        [role="menuitem"],
        [role="option"],
        [data-baseweb="popover"] li,
        [role="menu"] li,
        [role="listbox"] li,
        .stSelectbox [role="option"],
        .stMultiSelect [role="option"] {{
            background: transparent !important;
            color: {cls.COLORS['text_primary']} !important;
            padding: {cls.SPACING['3']} {cls.SPACING['4']} !important;
            margin: 0 !important;
            border: none !important;
            border-radius: 0 !important;
            font-size: {cls.TYPOGRAPHY['text_lg']} !important;
            font-weight: {cls.TYPOGRAPHY['font_medium']} !important;
            line-height: {cls.TYPOGRAPHY['leading_normal']} !important;
            cursor: pointer !important;
            transition: all 0.2s ease !important;
            display: flex !important;
            align-items: center !important;
            justify-content: space-between !important;
            min-height: 44px !important;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1) !important;
        }}
        
        /* Enhanced hover and active states */
        [role="menuitem"]:hover,
        [role="option"]:hover,
        [data-baseweb="popover"] li:hover,
        [role="menu"] li:hover,
        [role="listbox"] li:hover {{
            background: linear-gradient(135deg, {cls.COLORS['surface_secondary']} 0%, {cls.COLORS['surface_elevated']} 100%) !important;
            color: {cls.COLORS['text_primary']} !important;
            border-left: 3px solid {cls.COLORS['accent_primary']} !important;
            padding-left: calc({cls.SPACING['4']} - 3px) !important;
        }}
        
        [role="menuitem"]:focus,
        [role="option"]:focus,
        [data-baseweb="popover"] li:focus {{
            outline: 2px solid {cls.COLORS['accent_primary']} !important;
            outline-offset: -2px !important;
            background: {cls.COLORS['surface_secondary']} !important;
        }}
        
        /* Fix keyboard shortcut styling and alignment */
        [role="menuitem"] kbd,
        [role="option"] kbd,
        [data-baseweb="popover"] kbd,
        .keyboard-shortcut {{
            background: {cls.COLORS['bg_tertiary']} !important;
            color: {cls.COLORS['text_muted']} !important;
            border: 1px solid {cls.COLORS['border_medium']} !important;
            border-radius: {cls.RADIUS['sm']} !important;
            padding: {cls.SPACING['1']} {cls.SPACING['2']} !important;
            font-family: {cls.TYPOGRAPHY['font_family_mono']} !important;
            font-size: {cls.TYPOGRAPHY['text_xs']} !important;
            font-weight: {cls.TYPOGRAPHY['font_medium']} !important;
            margin-left: auto !important;
            min-width: 20px !important;
            text-align: center !important;
        }}
        
        /* Fix divider spacing and visual impact */
        [role="menu"] hr,
        [role="listbox"] hr,
        [data-baseweb="popover"] hr {{
            border: none !important;
            height: 1px !important;
            background: {cls.COLORS['border_light']} !important;
            margin: {cls.SPACING['2']} {cls.SPACING['4']} !important;
            opacity: 0.6 !important;
        }}
        
        /* Fix menu section grouping */
        [role="menu"] .menu-section,
        [role="listbox"] .menu-section {{
            border-bottom: 1px solid {cls.COLORS['border_light']} !important;
            margin-bottom: {cls.SPACING['2']} !important;
            padding-bottom: {cls.SPACING['2']} !important;
        }}
        
        [role="menu"] .menu-section:last-child,
        [role="listbox"] .menu-section:last-child {{
            border-bottom: none !important;
            margin-bottom: 0 !important;
            padding-bottom: 0 !important;
        }}
        
        /* Remove any purple borders or artifacts */
        [data-baseweb="popover"] *,
        [role="menu"] *,
        [role="listbox"] * {{
            border-color: {cls.COLORS['border_medium']} !important;
        }}
        
        /* Fix dropdown trigger button styling */
        [data-testid="stMainMenu"] button,
        [data-testid="stMainMenuButton"] {{
            background: {cls.COLORS['surface_secondary']} !important;
            color: {cls.COLORS['text_secondary']} !important;
            border: 1px solid {cls.COLORS['border_medium']} !important;
            border-radius: {cls.RADIUS['md']} !important;
            padding: {cls.SPACING['2']} {cls.SPACING['3']} !important;
            transition: all 0.2s ease !important;
        }}
        
        [data-testid="stMainMenu"] button:hover,
        [data-testid="stMainMenuButton"]:hover {{
            background: {cls.COLORS['surface_elevated']} !important;
            color: {cls.COLORS['text_primary']} !important;
            border-color: {cls.COLORS['accent_primary']} !important;
        }}
        
        /* === REMOVE CLUTTER AND CLEAN INTERFACE === */
        
        /* Hide unnecessary Streamlit elements */
        .stDeployButton,
        #MainMenu::after,
        footer,
        header[data-testid="stHeader"],
        .css-1d391kg,
        .css-18e3th9 {{
            visibility: hidden !important;
            display: none !important;
        }}
        
        /* === ENHANCED VISUAL HIERARCHY === */
        
        /* Main page titles */
        h1, .main-title {{
            font-size: {cls.TYPOGRAPHY['text_4xl']} !important;
            font-weight: {cls.TYPOGRAPHY['font_extrabold']} !important;
            color: {cls.COLORS['text_primary']} !important;
            line-height: {cls.TYPOGRAPHY['leading_tight']} !important;
            margin-bottom: {cls.SPACING['4']} !important;
            letter-spacing: {cls.TYPOGRAPHY['tracking_tight']} !important;
        }}
        
        /* Section headings */
        h2, .section-title {{
            font-size: {cls.TYPOGRAPHY['text_2xl']} !important;
            font-weight: {cls.TYPOGRAPHY['font_bold']} !important;
            color: {cls.COLORS['text_primary']} !important;
            margin-bottom: {cls.SPACING['3']} !important;
            margin-top: {cls.SPACING['6']} !important;
        }}
        
        /* Subsection headings */
        h3, .subsection-title {{
            font-size: {cls.TYPOGRAPHY['text_xl']} !important;
            font-weight: {cls.TYPOGRAPHY['font_semibold']} !important;
            color: {cls.COLORS['text_secondary']} !important;
            margin-bottom: {cls.SPACING['2']} !important;
            margin-top: {cls.SPACING['4']} !important;
        }}
        
        /* Body text and content */
        p, .body-text {{
            font-size: {cls.TYPOGRAPHY['text_base']} !important;
            color: {cls.COLORS['text_secondary']} !important;
            line-height: {cls.TYPOGRAPHY['leading_normal']} !important;
            margin-bottom: {cls.SPACING['3']} !important;
        }}
        
        /* Small text and captions */
        .caption, .help-text {{
            font-size: {cls.TYPOGRAPHY['text_sm']} !important;
            color: {cls.COLORS['text_muted']} !important;
            line-height: {cls.TYPOGRAPHY['leading_normal']} !important;
        }}
        
        /* === COMPACT LAYOUT SYSTEM === */
        
        /* Reduce container padding for better space utilization */
        .main .block-container {{
            padding-top: {cls.SPACING['1']} !important;
            padding-bottom: {cls.SPACING['2']} !important;
            max-width: 100% !important;
            padding-left: {cls.SPACING['4']} !important;
            padding-right: {cls.SPACING['4']} !important;
        }}

        /* Compact element spacing */
        .element-container {{
            margin-bottom: calc({cls.SPACING['1']} / 2) !important;
        }}

        /* === COMPACT METRICS === */
        .stMetric {{
            background: transparent !important;
            border: 1px solid {cls.COLORS['border_light']} !important;
            border-radius: {cls.RADIUS['md']} !important;
            padding: {cls.SPACING['3']} !important;
            margin-bottom: {cls.SPACING['1']} !important;
            transition: all 0.2s ease !important;
        }}

        .stMetric:hover {{
            border-color: {cls.COLORS['accent_primary']} !important;
            transform: translateY(-1px) !important;
        }}

        .stMetric [data-testid="metric-label"] {{
            font-size: {cls.TYPOGRAPHY['text_xs']} !important;
            font-weight: {cls.TYPOGRAPHY['font_semibold']} !important;
            color: {cls.COLORS['text_muted']} !important;
            text-transform: uppercase !important;
            letter-spacing: 0.05em !important;
        }}

        .stMetric [data-testid="metric-value"] {{
            font-size: {cls.TYPOGRAPHY['text_xl']} !important;
            font-weight: {cls.TYPOGRAPHY['font_bold']} !important;
            color: {cls.COLORS['text_primary']} !important;
            margin-top: {cls.SPACING['1']} !important;
        }}

        /* === COMPACT TABLES === */
        .stDataFrame {{
            border-radius: {cls.RADIUS['md']} !important;
            overflow: hidden !important;
            margin: {cls.SPACING['2']} 0 !important;
        }}

        .stDataFrame table {{
            font-size: {cls.TYPOGRAPHY['text_sm']} !important;
        }}

        .stDataFrame th {{
            background: {cls.COLORS['surface_elevated']} !important;
            color: {cls.COLORS['text_primary']} !important;
            font-weight: {cls.TYPOGRAPHY['font_semibold']} !important;
            font-size: {cls.TYPOGRAPHY['text_xs']} !important;
            padding: {cls.SPACING['2']} !important;
            text-transform: uppercase !important;
            letter-spacing: 0.05em !important;
        }}

        .stDataFrame td {{
            padding: {cls.SPACING['2']} !important;
            border-bottom: 1px solid {cls.COLORS['border_light']} !important;
            vertical-align: top !important;
        }}

        /* === COMPACT FORMS === */
        .stSelectbox, .stSlider {{
            margin-bottom: {cls.SPACING['2']} !important;
        }}

        .stSelectbox label, .stSlider label {{
            font-size: {cls.TYPOGRAPHY['text_sm']} !important;
            font-weight: {cls.TYPOGRAPHY['font_medium']} !important;
            margin-bottom: {cls.SPACING['1']} !important;
        }}

        /* === SPACE OPTIMIZATION === */
        .stExpander {{
            margin-bottom: {cls.SPACING['1']} !important;
        }}

        .stExpander summary {{
            padding: {cls.SPACING['2']} {cls.SPACING['3']} !important;
            font-size: {cls.TYPOGRAPHY['text_sm']} !important;
        }}

        .stExpander details[open] > div {{
            padding: {cls.SPACING['2']} {cls.SPACING['3']} !important;
        }}

        /* Reduce button spacing */
        .stButton {{
            margin-bottom: {cls.SPACING['1']} !important;
        }}

        /* Compact alerts */
        .stAlert {{
            margin: {cls.SPACING['1']} 0 !important;
            padding: {cls.SPACING['2']} {cls.SPACING['3']} !important;
            font-size: {cls.TYPOGRAPHY['text_sm']} !important;
        }}
        
        /* Section dividers with minimal space */
        hr, .divider {{
            margin: {cls.SPACING['4']} 0 !important;
            border-color: {cls.COLORS['border_light']} !important;
            opacity: 0.3 !important;
        }}
        
        /* Hide GitHub ribbon and other promotional elements */
        .github-corner,
        .stAlert .css-1d391kg,
        [data-testid="stNotificationContentContainer"] {{
            display: none !important;
        }}
        
        /* Minimize spacing between elements for cleaner look */
        .element-container {{
            margin-bottom: {cls.SPACING['2']} !important;
        }}
        
        /* Clean up form elements */
        .stForm {{
            border: none !important;
            background: transparent !important;
        }}
        
        /* Remove unnecessary borders and outlines */
        .css-1d391kg,
        .css-k1vhr4 {{
            border: none !important;
            outline: none !important;
        }}
        
        /* === MODERNIZED SIDEBAR NAVIGATION === */
        .sidebar-navbar-vertical {{
            background: {cls.COLORS['surface_secondary']} !important;
            border-radius: {cls.RADIUS['xl']} !important;
            padding: {cls.SPACING['2']} !important;
            margin: {cls.SPACING['3']} 0 !important;
            border: 1px solid {cls.COLORS['border_medium']} !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
        }}
        
        /* Modern pill-shaped navigation buttons */
        .sidebar-navbar-vertical .stButton > button {{
            background: transparent !important;
            color: {cls.COLORS['text_muted']} !important;
            border: none !important;
            border-radius: {cls.RADIUS['full']} !important;
            padding: {cls.SPACING['2']} {cls.SPACING['4']} !important;
            font-size: {cls.TYPOGRAPHY['text_sm']} !important;
            font-weight: {cls.TYPOGRAPHY['font_medium']} !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            min-height: 2.75rem !important;
            margin-bottom: {cls.SPACING['1']} !important;
            width: 100% !important;
            text-align: center !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            position: relative !important;
        }}
        
        /* Active pill button with modern styling */
        .sidebar-navbar-vertical .stButton > button[class*="primary"] {{
            background: linear-gradient(135deg, {cls.COLORS['accent_primary']} 0%, {cls.COLORS['interactive_hover']} 100%) !important;
            color: {cls.COLORS['text_primary']} !important;
            font-weight: {cls.TYPOGRAPHY['font_bold']} !important;
            box-shadow: 0 4px 16px rgba(66, 153, 225, 0.4), 0 2px 4px rgba(0, 0, 0, 0.1) !important;
            transform: scale(1.02) !important;
        }}
        
        /* Enhanced hover states with subtle animations */
        .sidebar-navbar-vertical .stButton > button:hover {{
            background: {cls.COLORS['surface_elevated']} !important;
            color: {cls.COLORS['text_primary']} !important;
            transform: scale(1.01) !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
        }}
        
        /* Active button enhanced hover */
        .sidebar-navbar-vertical .stButton > button[class*="primary"]:hover {{
            background: linear-gradient(135deg, {cls.COLORS['interactive_hover']} 0%, {cls.COLORS['interactive_active']} 100%) !important;
            transform: scale(1.03) !important;
            box-shadow: 0 6px 20px rgba(66, 153, 225, 0.5), 0 4px 8px rgba(0, 0, 0, 0.15) !important;
        }}
        
        /* Active indicator dot */
        .sidebar-navbar-vertical .stButton > button[class*="primary"]::before {{
            content: '';
            position: absolute;
            left: {cls.SPACING['1']};
            top: 50%;
            transform: translateY(-50%);
            width: 4px;
            height: 4px;
            background: {cls.COLORS['text_primary']};
            border-radius: 50%;
            opacity: 0.8;
        }}
        
        /* Remove bottom margin from last button */
        .sidebar-navbar-vertical .stButton:last-child > button {{
            margin-bottom: 0 !important;
        }}
        
        /* === ENHANCED SIDEBAR (FIXED LAYOUT ISSUES) === */
        [data-testid=\"stSidebar\"] {{
            background: linear-gradient(180deg, {cls.COLORS['surface_primary']} 0%, {cls.COLORS['bg_secondary']} 100%) !important;
            border-right: 1px solid {cls.COLORS['border_medium']};
            backdrop-filter: blur(10px);
            width: 320px !important;
            min-width: 320px !important;
            overflow-y: auto !important;
            overflow-x: hidden !important;
        }}
        
        [data-testid=\"stSidebar\"] * {{
            background-color: transparent !important;
        }}
        
        /* === SIDEBAR CONTENT SECTIONS === */
        .sidebar-section {{
            background: {cls.COLORS['surface_secondary']} !important;
            border: 1px solid {cls.COLORS['border_light']};
            border-radius: {cls.RADIUS['lg']};
            padding: var(--spacing-6);
            margin-bottom: var(--spacing-6);
            box-shadow: var(--shadow-sm);
        }}
        
        .sidebar-header {{
            background: linear-gradient(135deg, {cls.COLORS['surface_primary']} 0%, {cls.COLORS['surface_secondary']} 100%) !important;
            border: 1px solid {cls.COLORS['border_medium']};
            border-radius: {cls.RADIUS['lg']};
            padding: var(--spacing-6);
            margin-bottom: var(--spacing-8);
            text-align: center;
        }}
        
        .sidebar-header h2 {{
            color: {cls.COLORS['text_primary']} !important;
            font-size: {cls.TYPOGRAPHY['text_2xl']} !important;
            font-weight: {cls.TYPOGRAPHY['font_bold']} !important;
            margin: 0 0 var(--spacing-2) 0 !important;
        }}
        
        .sidebar-header p {{
            color: {cls.COLORS['text_muted']} !important;
            font-size: {cls.TYPOGRAPHY['text_sm']} !important;
            margin: 0 !important;
        }}
        
        /* === FIXED DROPDOWN STYLING === */
        [data-testid=\"stSidebar\"] .stSelectbox {{
            margin-bottom: var(--spacing-6) !important;
            z-index: 9999 !important;
            position: relative !important;
        }}
        
        [data-testid=\"stSidebar\"] .stSelectbox label {{
            color: {cls.COLORS['text_primary']} !important;
            font-size: {cls.TYPOGRAPHY['text_base']} !important;
            font-weight: {cls.TYPOGRAPHY['font_semibold']} !important;
            margin-bottom: var(--spacing-3) !important;
            display: block !important;
        }}
        
        [data-testid=\"stSidebar\"] .stSelectbox > div > div {{
            background: {cls.COLORS['surface_elevated']} !important;
            border: 2px solid {cls.COLORS['border_light']} !important;
            border-radius: {cls.RADIUS['md']} !important;
            color: {cls.COLORS['text_primary']} !important;
            font-size: {cls.TYPOGRAPHY['text_base']} !important;
            padding: var(--spacing-3) var(--spacing-4) !important;
            min-height: 48px !important;
            z-index: 9999 !important;
            position: relative !important;
        }}
        
        [data-testid=\"stSidebar\"] .stSelectbox > div > div:focus-within {{
            border-color: {cls.COLORS['accent_primary']} !important;
            box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.2) !important;
        }}
        
        /* === DROPDOWN OPTIONS CONTAINER === */
        [data-testid=\"stSidebar\"] .stSelectbox [data-baseweb=\"select\"] > div {{
            z-index: 10000 !important;
            position: absolute !important;
            background: {cls.COLORS['surface_elevated']} !important;
            border: 2px solid {cls.COLORS['border_accent']} !important;
            border-radius: {cls.RADIUS['md']} !important;
            box-shadow: var(--shadow-xl) !important;
            margin-top: 4px !important;
            max-height: 200px !important;
            overflow-y: auto !important;
        }}
        
        /* === GLOBAL DROPDOWN POSITIONING FIX === */
        /* Ensure all dropdowns appear in their correct positions */
        .stSelectbox {{
            position: relative !important;
            z-index: 1 !important;
        }}
        
        .stSelectbox > div {{
            position: relative !important;
        }}
        
        /* Fix dropdown popover positioning */
        [data-baseweb=\"popover\"][data-placement] {{
            z-index: 9999 !important;
            position: absolute !important;
        }}
        
        /* Target dropdown list containers */
        .stSelectbox [data-baseweb=\"select\"] [role=\"listbox\"],
        .stSelectbox [data-baseweb=\"popover\"],
        [data-baseweb=\"select\"] > div[style*=\"position: absolute\"] {{
            z-index: 9999 !important;
            position: absolute !important;
            background: {cls.COLORS['surface_primary']} !important;
            border: 2px solid {cls.COLORS['border_accent']} !important;
            border-radius: {cls.RADIUS['md']} !important;
            box-shadow: var(--shadow-xl) !important;
            margin-top: 4px !important;
            max-height: 300px !important;
            overflow-y: auto !important;
            width: 100% !important;
            left: 0 !important;
            right: 0 !important;
        }}
        
        /* Dropdown option items */
        .stSelectbox [role=\"option\"] {{
            background: transparent !important;
            color: {cls.COLORS['text_primary']} !important;
            padding: var(--spacing-2) var(--spacing-3) !important;
            border: none !important;
            transition: background-color 0.2s ease !important;
        }}
        
        .stSelectbox [role=\"option\"]:hover,
        .stSelectbox [role=\"option\"]:focus {{
            background: {cls.COLORS['surface_hover']} !important;
            color: {cls.COLORS['text_primary']} !important;
        }}
        
        /* Prevent dropdown overflow in sidebar */
        [data-testid=\"stSidebar\"] {{
            overflow: visible !important;
        }}
        
        /* For sidebar dropdowns that might overflow */
        [data-testid=\"stSidebar\"] .stSelectbox [data-baseweb=\"popover\"] {{
            left: auto !important;
            right: -220px !important;
            width: 220px !important;
        }}
        
        /* Ensure main content dropdowns stay within their containers */
        .main .stSelectbox [data-baseweb=\"popover\"],
        .main .stSelectbox [role=\"listbox\"] {{
            left: 0 !important;
            right: auto !important;
            width: 100% !important;
        }}
        
        /* === SIDEBAR TEXT HIERARCHY === */
        [data-testid=\"stSidebar\"] .stMarkdown h1 {{
            color: {cls.COLORS['text_primary']} !important;
            font-size: {cls.TYPOGRAPHY['text_xl']} !important;
            font-weight: {cls.TYPOGRAPHY['font_bold']} !important;
            margin-bottom: var(--spacing-4) !important;
        }}
        
        [data-testid=\"stSidebar\"] .stMarkdown h2 {{
            color: {cls.COLORS['text_primary']} !important;
            font-size: {cls.TYPOGRAPHY['text_lg']} !important;
            font-weight: {cls.TYPOGRAPHY['font_semibold']} !important;
            margin-bottom: var(--spacing-3) !important;
        }}
        
        [data-testid=\"stSidebar\"] .stMarkdown h3 {{
            color: {cls.COLORS['text_secondary']} !important;
            font-size: {cls.TYPOGRAPHY['text_base']} !important;
            font-weight: {cls.TYPOGRAPHY['font_medium']} !important;
            margin-bottom: var(--spacing-2) !important;
        }}
        
        [data-testid=\"stSidebar\"] .stMarkdown p {{
            color: {cls.COLORS['text_muted']} !important;
            font-size: {cls.TYPOGRAPHY['text_sm']} !important;
            line-height: {cls.TYPOGRAPHY['leading_relaxed']} !important;
            margin-bottom: var(--spacing-3) !important;
        }}
        
        /* === SIDEBAR SCROLLBAR === */
        [data-testid=\"stSidebar\"]::-webkit-scrollbar {{
            width: 6px;
        }}
        
        [data-testid=\"stSidebar\"]::-webkit-scrollbar-track {{
            background: {cls.COLORS['bg_secondary']};
            border-radius: 3px;
        }}
        
        [data-testid=\"stSidebar\"]::-webkit-scrollbar-thumb {{
            background: {cls.COLORS['border_medium']};
            border-radius: 3px;
            transition: background 0.2s ease;
        }}
        
        [data-testid=\"stSidebar\"]::-webkit-scrollbar-thumb:hover {{
            background: {cls.COLORS['accent_primary']};
        }}
        
        /* === STATUS INDICATORS === */
        .status-indicator {{
            display: inline-flex;
            align-items: center;
            gap: var(--spacing-2);
            padding: var(--spacing-2) var(--spacing-3);
            border-radius: {cls.RADIUS['full']};
            font-size: {cls.TYPOGRAPHY['text_xs']};
            font-weight: {cls.TYPOGRAPHY['font_medium']};
            text-transform: uppercase;
            letter-spacing: {cls.TYPOGRAPHY['tracking_wide']};
        }}
        
        .status-indicator.success {{
            background: rgba(72, 187, 120, 0.2);
            color: {cls.COLORS['success_400']};
            border: 1px solid {cls.COLORS['success_500']};
        }}
        
        .status-indicator.warning {{
            background: rgba(237, 137, 54, 0.2);
            color: {cls.COLORS['warning_400']};
            border: 1px solid {cls.COLORS['warning_500']};
        }}
        
        .status-indicator.error {{
            background: rgba(229, 62, 62, 0.2);
            color: {cls.COLORS['error_400']};
            border: 1px solid {cls.COLORS['error_500']};
        }}
        
        /* === NAVIGATION ICONS === */
        .nav-icon {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 24px;
            height: 24px;
            border-radius: {cls.RADIUS['sm']};
            background: {cls.COLORS['accent_primary']};
            color: {cls.COLORS['text_primary']};
            font-size: 14px;
            margin-right: var(--spacing-3);
        }}
        
        /* === DIVIDERS === */
        .sidebar-divider {{
            height: 1px;
            background: linear-gradient(90deg, transparent, {cls.COLORS['border_light']}, transparent);
            margin: var(--spacing-6) 0;
        }}
        
        /* === ENHANCED RADIO BUTTONS (NAVIGATION) === */
        [data-testid=\"stSidebar\"] .stRadio {{
            background: transparent !important;
        }}
        
        [data-testid=\"stSidebar\"] .stRadio > div {{
            background: transparent !important;
            gap: var(--spacing-2) !important;
        }}
        
        [data-testid=\"stSidebar\"] .stRadio label {{
            background: {cls.COLORS['surface_secondary']} !important;
            border: 2px solid {cls.COLORS['border_light']};
            border-radius: {cls.RADIUS['lg']};
            padding: var(--spacing-4) var(--spacing-6);
            margin-bottom: var(--spacing-3);
            color: {cls.COLORS['text_secondary']} !important;
            font-size: {cls.TYPOGRAPHY['text_base']} !important;
            font-weight: {cls.TYPOGRAPHY['font_medium']} !important;
            cursor: pointer;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex !important;
            align-items: center;
            width: 100%;
            box-sizing: border-box;
        }}
        
        [data-testid=\"stSidebar\"] .stRadio label:hover {{
            background: {cls.COLORS['surface_elevated']} !important;
            border-color: {cls.COLORS['border_accent']};
            color: {cls.COLORS['text_primary']} !important;
            transform: translateY(-1px);
            box-shadow: var(--shadow-md);
        }}
        
        [data-testid=\"stSidebar\"] .stRadio label[data-checked=\"true\"] {{
            background: linear-gradient(135deg, {cls.COLORS['accent_primary']} 0%, {cls.COLORS['interactive_hover']} 100%) !important;
            border-color: {cls.COLORS['accent_primary']};
            color: {cls.COLORS['text_primary']} !important;
            font-weight: {cls.TYPOGRAPHY['font_semibold']} !important;
            box-shadow: var(--shadow-lg);
        }}
        
        [data-testid=\"stSidebar\"] .stRadio input[type=\"radio\"] {{
            display: none !important;
        }}
        
        /* === RADIO BUTTON ICONS === */
        [data-testid=\"stSidebar\"] .stRadio label::before {{
            content: '';
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: {cls.COLORS['border_medium']};
            margin-right: var(--spacing-3);
            transition: all 0.2s ease;
        }}
        
        [data-testid=\"stSidebar\"] .stRadio label:hover::before {{
            background: {cls.COLORS['accent_primary']};
        }}
        
        [data-testid=\"stSidebar\"] .stRadio label[data-checked=\"true\"]::before {{
            background: {cls.COLORS['text_primary']};
            box-shadow: 0 0 6px rgba(255, 255, 255, 0.3);
        }}
        
        /* === ENHANCED FORM ELEMENTS === */
        .stSelectbox > div > div,
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {{
            background: {cls.COLORS['surface_secondary']} !important;
            border: 2px solid {cls.COLORS['border_light']} !important;
            border-radius: {cls.RADIUS['md']};
            color: {cls.COLORS['text_primary']} !important;
            font-size: {cls.TYPOGRAPHY['text_base']};
            padding: var(--spacing-4);
            transition: all 0.2s ease;
        }}
        
        .stSelectbox > div > div:focus-within,
        .stTextInput > div > div:focus-within,
        .stTextArea > div > div:focus-within {{
            border-color: {cls.COLORS['accent_primary']} !important;
            box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.1) !important;
            background: {cls.COLORS['surface_elevated']} !important;
        }}
        
        /* === ENHANCED METRICS === */
        .stMetric {{
            background: {cls.COLORS['surface_primary']} !important;
            border: 1px solid {cls.COLORS['border_light']};
            border-radius: {cls.RADIUS['lg']};
            padding: var(--spacing-6);
            box-shadow: var(--shadow-sm);
            transition: all 0.2s ease;
        }}
        
        .stMetric:hover {{
            box-shadow: var(--shadow-md);
            transform: translateY(-2px);
        }}
        
        .stMetric label {{
            color: {cls.COLORS['text_muted']} !important;
            font-size: {cls.TYPOGRAPHY['text_sm']} !important;
            font-weight: {cls.TYPOGRAPHY['font_semibold']} !important;
            text-transform: uppercase;
            letter-spacing: {cls.TYPOGRAPHY['tracking_wider']};
        }}
        
        .stMetric [data-testid=\"metric-value\"] {{
            color: {cls.COLORS['text_primary']} !important;
            font-size: {cls.TYPOGRAPHY['text_3xl']} !important;
            font-weight: {cls.TYPOGRAPHY['font_bold']} !important;
        }}
        
        /* === ENHANCED ALERTS === */
        .stAlert {{
            border-radius: {cls.RADIUS['lg']};
            border: none;
            font-weight: {cls.TYPOGRAPHY['font_medium']};
            font-size: {cls.TYPOGRAPHY['text_base']};
            padding: var(--spacing-4) var(--spacing-6);
        }}
        
        .stSuccess {{
            background: linear-gradient(135deg, {cls.COLORS['bg_secondary']} 0%, rgba(16, 185, 129, 0.1) 100%) !important;
            color: {cls.COLORS['accent_success']} !important;
            border-left: 4px solid {cls.COLORS['accent_success']};
        }}
        
        .stWarning {{
            background: linear-gradient(135deg, {cls.COLORS['bg_secondary']} 0%, rgba(245, 158, 11, 0.1) 100%) !important;
            color: {cls.COLORS['accent_warning']} !important;
            border-left: 4px solid {cls.COLORS['accent_warning']};
        }}
        
        .stError {{
            background: linear-gradient(135deg, {cls.COLORS['bg_secondary']} 0%, rgba(239, 68, 68, 0.1) 100%) !important;
            color: {cls.COLORS['accent_danger']} !important;
            border-left: 4px solid {cls.COLORS['accent_danger']};
        }}
        
        .stInfo {{
            background: linear-gradient(135deg, {cls.COLORS['info_900']} 0%, rgba(66, 153, 225, 0.1) 100%) !important;
            color: {cls.COLORS['info_400']} !important;
            border-left: 4px solid {cls.COLORS['info_500']};
        }}
        
        /* === ENHANCED DATA TABLES === */
        .stDataFrame {{
            background: {cls.COLORS['surface_primary']} !important;
            border: 1px solid {cls.COLORS['border_light']};
            border-radius: {cls.RADIUS['lg']};
            overflow: hidden;
            box-shadow: var(--shadow-md);
        }}
        
        .stDataFrame th {{
            background: linear-gradient(135deg, {cls.COLORS['surface_secondary']} 0%, {cls.COLORS['bg_tertiary']} 100%) !important;
            color: {cls.COLORS['text_primary']} !important;
            font-weight: {cls.TYPOGRAPHY['font_bold']} !important;
            font-size: {cls.TYPOGRAPHY['text_base']} !important;
            text-transform: uppercase;
            letter-spacing: {cls.TYPOGRAPHY['tracking_wide']};
            padding: var(--spacing-4) var(--spacing-6) !important;
            border-bottom: 2px solid {cls.COLORS['accent_primary']} !important;
        }}
        
        .stDataFrame td {{
            background: {cls.COLORS['surface_primary']} !important;
            color: {cls.COLORS['text_secondary']} !important;
            font-size: {cls.TYPOGRAPHY['text_base']} !important;
            padding: var(--spacing-4) var(--spacing-6) !important;
            border-bottom: 1px solid {cls.COLORS['border_light']} !important;
            transition: background-color 0.2s ease;
        }}
        
        .stDataFrame tr:hover td {{
            background: {cls.COLORS['surface_elevated']} !important;
            color: {cls.COLORS['text_primary']} !important;
        }}
        
        /* === PROGRESS BARS === */
        .stProgress {{
            background: {cls.COLORS['surface_secondary']} !important;
            border-radius: {cls.RADIUS['full']};
            overflow: hidden;
            box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.3);
            height: 12px;
        }}
        
        .stProgress > div > div > div {{
            background: linear-gradient(45deg, {cls.COLORS['accent_primary']}, {cls.COLORS['accent_secondary']}) !important;
            border-radius: {cls.RADIUS['full']};
        }}
        
        /* === TABS === */
        .stTabs [data-baseweb=\"tab-list\"] {{
            gap: var(--spacing-2);
            background: {cls.COLORS['surface_secondary']} !important;
            border-radius: {cls.RADIUS['lg']};
            padding: var(--spacing-2);
        }}
        
        .stTabs [data-baseweb=\"tab\"] {{
            background: transparent !important;
            border-radius: {cls.RADIUS['md']};
            color: {cls.COLORS['text_muted']} !important;
            font-weight: {cls.TYPOGRAPHY['font_semibold']};
            font-size: {cls.TYPOGRAPHY['text_base']};
            padding: var(--spacing-3) var(--spacing-6);
            transition: all 0.2s ease;
        }}
        
        .stTabs [aria-selected=\"true\"] {{
            background: {cls.COLORS['accent_primary']} !important;
            color: {cls.COLORS['text_primary']} !important;
            box-shadow: var(--shadow-sm);
        }}
        
        /* === SENTIMENT-BASED STYLING === */
        .sentiment-positive {{
            color: {cls.COLORS['sentiment_positive']} !important;
            border-left: 3px solid {cls.COLORS['sentiment_positive']} !important;
            background: linear-gradient(135deg, {cls.COLORS['bg_secondary']} 0%, rgba(16, 185, 129, 0.05) 100%) !important;
        }}
        
        .sentiment-negative {{
            color: {cls.COLORS['sentiment_negative']} !important;
            border-left: 3px solid {cls.COLORS['sentiment_negative']} !important;
            background: linear-gradient(135deg, {cls.COLORS['bg_secondary']} 0%, rgba(239, 68, 68, 0.05) 100%) !important;
        }}
        
        .sentiment-neutral {{
            color: {cls.COLORS['sentiment_neutral']} !important;
            border-left: 3px solid {cls.COLORS['sentiment_neutral']} !important;
            background: linear-gradient(135deg, {cls.COLORS['bg_secondary']} 0%, rgba(107, 114, 128, 0.05) 100%) !important;
        }}
        
        .sentiment-mixed {{
            color: {cls.COLORS['sentiment_mixed']} !important;
            border-left: 3px solid {cls.COLORS['sentiment_mixed']} !important;
            background: linear-gradient(135deg, {cls.COLORS['bg_secondary']} 0%, rgba(245, 158, 11, 0.05) 100%) !important;
        }}
        
        /* Sentiment badges */
        .sentiment-badge {{
            display: inline-flex;
            align-items: center;
            padding: {cls.SPACING['1']} {cls.SPACING['2']};
            border-radius: 9999px;
            font-size: {cls.TYPOGRAPHY['text_xs']};
            font-weight: {cls.TYPOGRAPHY['font_semibold']};
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        .sentiment-badge.positive {{
            background: rgba(16, 185, 129, 0.2) !important;
            color: {cls.COLORS['sentiment_positive']} !important;
            border: 1px solid {cls.COLORS['sentiment_positive']};
        }}
        
        .sentiment-badge.negative {{
            background: rgba(239, 68, 68, 0.2) !important;
            color: {cls.COLORS['sentiment_negative']} !important;
            border: 1px solid {cls.COLORS['sentiment_negative']};
        }}
        
        .sentiment-badge.neutral {{
            background: rgba(107, 114, 128, 0.2) !important;
            color: {cls.COLORS['sentiment_neutral']} !important;
            border: 1px solid {cls.COLORS['sentiment_neutral']};
        }}
        
        .sentiment-badge.mixed {{
            background: rgba(245, 158, 11, 0.2) !important;
            color: {cls.COLORS['sentiment_mixed']} !important;
            border: 1px solid {cls.COLORS['sentiment_mixed']};
        }}
        
        /* === WARM ACCENT HIGHLIGHTS === */
        .warm-highlight {{
            background: linear-gradient(135deg, {cls.COLORS['accent_warm']} 0%, rgba(245, 158, 11, 0.8) 100%) !important;
            color: {cls.COLORS['text_primary']} !important;
            padding: {cls.SPACING['1']} {cls.SPACING['2']} !important;
            border-radius: {cls.RADIUS['sm']} !important;
            font-weight: {cls.TYPOGRAPHY['font_semibold']} !important;
        }}
        
        .warm-border {{
            border: 2px solid {cls.COLORS['accent_warm']} !important;
            box-shadow: 0 0 0 1px rgba(245, 158, 11, 0.2) !important;
        }}
        
        /* === RESPONSIVE DESIGN === */
        @media (max-width: 768px) {{
            .main-header {{
                padding: var(--spacing-6);
            }}
            
            .main-header h1 {{
                font-size: {cls.TYPOGRAPHY['text_3xl']};
            }}
            
            .enhanced-card {{
                padding: var(--spacing-6);
                margin-bottom: var(--spacing-4);
            }}
        }}
        
        /* === UTILITY CLASSES === */
        .text-center {{ text-align: center; }}
        .text-left {{ text-align: left; }}
        .text-right {{ text-align: right; }}
        
        .font-medium {{ font-weight: {cls.TYPOGRAPHY['font_medium']}; }}
        .font-semibold {{ font-weight: {cls.TYPOGRAPHY['font_semibold']}; }}
        .font-bold {{ font-weight: {cls.TYPOGRAPHY['font_bold']}; }}
        
        .text-accent {{ color: {cls.COLORS['accent_primary']} !important; }}
        .text-success {{ color: {cls.COLORS['success_400']} !important; }}
        .text-warning {{ color: {cls.COLORS['warning_400']} !important; }}
        .text-error {{ color: {cls.COLORS['error_400']} !important; }}
        
        .bg-surface {{ background: {cls.COLORS['surface_primary']} !important; }}
        .bg-elevated {{ background: {cls.COLORS['surface_elevated']} !important; }}
        
        .border-accent {{ border-color: {cls.COLORS['accent_primary']} !important; }}
        .shadow-enhanced {{ box-shadow: var(--shadow-lg); }}
        </style>
        """ + get_animation_css() + get_chart_css()
    
    @classmethod
    def get_component_html(cls, component_type: str, title: str, content: str, **kwargs) -> str:
        """Generate enhanced HTML components with improved styling"""
        
        if component_type == "header":
            subtitle = kwargs.get('subtitle', '')
            return f"""
            <div class="main-header">
                <h1>{title}</h1>
                <p>{content}</p>
                {f'<p style="font-size: {cls.TYPOGRAPHY["text_sm"]}; color: {cls.COLORS["text_muted"]}; margin-top: {cls.SPACING["2"]};">{subtitle}</p>' if subtitle else ''}
            </div>
            """
        
        elif component_type == "enhanced_card":
            icon = kwargs.get('icon', '')
            return f"""
            <div class="enhanced-card">
                <h3 style="display: flex; align-items: center; gap: {cls.SPACING['3']};">
                    {icon} {title}
                </h3>
                <div>{content}</div>
            </div>
            """
        
        elif component_type == "elevated_card":
            return f"""
            <div class="elevated-card">
                <h4>{title}</h4>
                <div>{content}</div>
            </div>
            """
        
        elif component_type == "cta_button":
            action = kwargs.get('action', 'primary')
            size = kwargs.get('size', 'normal')
            
            # Define button classes and styling based on action type
            button_classes = {
                'primary': '',  # Default Streamlit button styling applies
                'secondary': 'secondary-button',
                'danger': 'danger-button',
                'success': 'success-button',
                'large': 'large-cta-button',
                'compact': 'compact-button'
            }
            
            # Get appropriate class
            classes = button_classes.get(action, '')
            if size == 'large':
                classes += ' large-cta-button'
            elif size == 'compact':
                classes += ' compact-button'
            
            # Define background colors for each action
            bg_colors = {
                'primary': f"linear-gradient(135deg, {cls.COLORS['accent_primary']} 0%, {cls.COLORS['interactive_hover']} 100%)",
                'secondary': f"linear-gradient(135deg, {cls.COLORS['surface_secondary']} 0%, {cls.COLORS['surface_elevated']} 100%)",
                'danger': "linear-gradient(135deg, #e53e3e 0%, #c53030 100%)",
                'success': "linear-gradient(135deg, #38a169 0%, #2f855a 100%)",
                'large': f"linear-gradient(135deg, {cls.COLORS['accent_primary']} 0%, {cls.COLORS['interactive_hover']} 100%)",
                'compact': f"linear-gradient(135deg, {cls.COLORS['accent_primary']} 0%, {cls.COLORS['interactive_hover']} 100%)"
            }
            
            background = bg_colors.get(action, bg_colors['primary'])
            
            # Determine font size based on action type
            font_sizes = {
                'large': cls.TYPOGRAPHY['text_xl'],
                'compact': cls.TYPOGRAPHY['text_base'],
                'normal': cls.TYPOGRAPHY['text_lg']
            }
            font_size = font_sizes.get(size, font_sizes['normal'])
            
            # Determine padding based on size
            paddings = {
                'large': f"{cls.SPACING['6']} {cls.SPACING['12']}",
                'compact': f"{cls.SPACING['2']} {cls.SPACING['4']}",
                'normal': f"{cls.SPACING['5']} {cls.SPACING['8']}"
            }
            padding = paddings.get(size, paddings['normal'])
            
            return f"""

            </div>
            """
        
        elif component_type == "status_card":
            status = kwargs.get('status', 'info')
            color_map = {
                'success': cls.COLORS['success_400'],
                'warning': cls.COLORS['warning_400'],
                'error': cls.COLORS['error_400'],
                'info': cls.COLORS['info_400']
            }
            bg_map = {
                'success': f"linear-gradient(135deg, {cls.COLORS['success_900']} 0%, rgba(72, 187, 120, 0.1) 100%)",
                'warning': f"linear-gradient(135deg, {cls.COLORS['warning_900']} 0%, rgba(237, 137, 54, 0.1) 100%)",
                'error': f"linear-gradient(135deg, {cls.COLORS['error_900']} 0%, rgba(229, 62, 62, 0.1) 100%)",
                'info': f"linear-gradient(135deg, {cls.COLORS['info_900']} 0%, rgba(66, 153, 225, 0.1) 100%)"
            }
            
            return f"""
            <div style="
                background: {bg_map.get(status, bg_map['info'])};
                border-left: 4px solid {color_map.get(status, color_map['info'])};
                border-radius: {cls.RADIUS['lg']};
                padding: {cls.SPACING['4']} {cls.SPACING['6']};
                margin: {cls.SPACING['4']} 0;
            ">
                <h4 style="color: {color_map.get(status, color_map['info'])}; margin: 0 0 {cls.SPACING['2']} 0;">{title}</h4>
                <p style="color: {color_map.get(status, color_map['info'])}; margin: 0;">{content}</p>
            </div>
            """
        
        else:
            return f"""
            <div class="enhanced-card">
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
        
        return f"""<div style="background: {bg_color}; border: 1px solid {color}; border-radius: {cls.RADIUS['md']}; padding: {cls.SPACING['4']}; text-align: center;">
    <div style="font-size: {cls.TYPOGRAPHY['text_3xl']}; font-weight: {cls.TYPOGRAPHY['font_bold']}; color: {color}; margin-bottom: {cls.SPACING['1']};">
        {score:.0f}%
    </div>
    <div style="font-size: {cls.TYPOGRAPHY['text_sm']}; color: {color}; text-transform: uppercase;">
        Data Quality: {status}
    </div>
</div>"""


# Create enhanced theme instance
enhanced_dark_theme = EnhancedDarkTheme()