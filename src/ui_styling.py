"""
UI Styling Module for Comment Analyzer
Centralized styling system with coherent Web3 design
"""

from typing import Dict, Any


class ThemeManager:
    """Manages color themes and CSS generation for the application"""
    
    def __init__(self):
        # Coherent Web3 color system with consistent saturation and brightness
        self.color_systems = {
            'dark': {
                # Primary gradient spectrum
                'primary': '#8B5CF6',        # Main violet
                'primary_light': '#A78BFA',  # Lighter violet
                'primary_dark': '#7C3AED',   # Darker violet
                'primary_glow': '#B794F6',   # Glow effect violet
                
                # Secondary gradient spectrum  
                'secondary': '#06B6D4',       # Cyan
                'secondary_light': '#22D3EE', # Light cyan
                'secondary_dark': '#0891B2',  # Dark cyan
                'secondary_glow': '#67E8F9',  # Glow cyan
                
                # Accent colors for special elements
                'accent': '#F59E0B',          # Amber
                'accent_light': '#FCD34D',    # Light amber
                
                # Semantic colors
                'positive': '#10B981',        # Emerald
                'positive_light': '#34D399',
                'negative': '#EF4444',        # Red
                'negative_light': '#F87171',
                'neutral': '#6B7280',         # Gray
                'neutral_light': '#9CA3AF',
                
                # Background gradient system
                'bg_primary': '#0A0A0F',      # Deep black
                'bg_secondary': '#12111A',    # Slightly lighter
                'bg_tertiary': '#1A1825',     # Card background
                'bg_gradient_start': '#0F0E13',
                'bg_gradient_mid': '#1A1825', 
                'bg_gradient_end': '#16151F',
                
                # Glass effects with consistent opacity
                'glass_bg': 'rgba(139, 92, 246, 0.03)',
                'glass_bg_hover': 'rgba(139, 92, 246, 0.06)',
                'glass_border': 'rgba(139, 92, 246, 0.15)',
                'glass_border_hover': 'rgba(139, 92, 246, 0.25)',
                'glass_blur': '16px',
                
                # Text hierarchy
                'text_primary': '#FFFFFF',
                'text_secondary': '#E5E7EB',
                'text_tertiary': '#9CA3AF',
                'text_muted': '#6B7280'
            },
            'light': {
                # Primary gradient spectrum
                'primary': '#8B5CF6',
                'primary_light': '#A78BFA',
                'primary_dark': '#7C3AED',
                'primary_glow': '#B794F6',
                
                # Secondary gradient spectrum
                'secondary': '#06B6D4',
                'secondary_light': '#22D3EE',
                'secondary_dark': '#0891B2',
                'secondary_glow': '#67E8F9',
                
                # Accent colors
                'accent': '#F59E0B',
                'accent_light': '#FCD34D',
                
                # Semantic colors
                'positive': '#10B981',
                'positive_light': '#34D399',
                'negative': '#EF4444',
                'negative_light': '#F87171',
                'neutral': '#6B7280',
                'neutral_light': '#9CA3AF',
                
                # Background gradient system
                'bg_primary': '#FFFFFF',
                'bg_secondary': '#FAFAFA',
                'bg_tertiary': '#F3F4F6',
                'bg_gradient_start': '#FAFAFA',
                'bg_gradient_mid': '#F3E8FF',
                'bg_gradient_end': '#E0F2FE',
                
                # Glass effects
                'glass_bg': 'rgba(255, 255, 255, 0.6)',
                'glass_bg_hover': 'rgba(255, 255, 255, 0.8)',
                'glass_border': 'rgba(139, 92, 246, 0.2)',
                'glass_border_hover': 'rgba(139, 92, 246, 0.3)',
                'glass_blur': '12px',
                
                # Text hierarchy
                'text_primary': '#111827',
                'text_secondary': '#374151',
                'text_tertiary': '#6B7280',
                'text_muted': '#9CA3AF'
            }
        }
        
        # Consistent animation timing system
        self.animations = {
            'duration_fast': '0.2s',
            'duration_normal': '0.3s',
            'duration_slow': '0.5s',
            'duration_ambient': '20s',
            'easing_default': 'cubic-bezier(0.4, 0, 0.2, 1)',
            'easing_bounce': 'cubic-bezier(0.68, -0.55, 0.265, 1.55)'
        }
        
        # Typography scale (Major Third - 1.25 ratio)
        self.typography = {
            'size_xs': '0.75rem',    # 12px
            'size_sm': '0.875rem',   # 14px
            'size_base': '1rem',     # 16px
            'size_lg': '1.25rem',    # 20px
            'size_xl': '1.5rem',     # 24px
            'size_2xl': '1.875rem',  # 30px
            'size_3xl': '2.25rem',   # 36px
            'size_4xl': '3rem',      # 48px
            'weight_light': '300',
            'weight_normal': '400',
            'weight_medium': '500',
            'weight_semibold': '600',
            'weight_bold': '700'
        }
        
        # Elevation system for consistent shadows
        self.elevation = {
            'sm': '0 2px 8px rgba(139, 92, 246, 0.08)',
            'md': '0 8px 24px rgba(139, 92, 246, 0.12)',
            'lg': '0 16px 40px rgba(139, 92, 246, 0.16)',
            'xl': '0 24px 56px rgba(139, 92, 246, 0.20)'
        }
    
    def get_theme(self, dark_mode: bool) -> Dict[str, str]:
        """Get theme colors based on mode"""
        return self.color_systems['dark' if dark_mode else 'light']
    
    def generate_css_variables(self, theme: Dict[str, str]) -> str:
        """Generate CSS custom properties"""
        variables = []
        
        # Add theme colors
        for key, value in theme.items():
            css_key = key.replace('_', '-')
            variables.append(f"--{css_key}: {value};")
        
        # Add animation variables
        for key, value in self.animations.items():
            css_key = key.replace('_', '-')
            variables.append(f"--{css_key}: {value};")
        
        # Add typography variables
        for key, value in self.typography.items():
            css_key = key.replace('_', '-')
            variables.append(f"--{css_key}: {value};")
        
        # Add elevation variables
        for key, value in self.elevation.items():
            variables.append(f"--elevation-{key}: {value};")
        
        return "\n".join(variables)
    
    def generate_base_styles(self, theme: Dict[str, str]) -> str:
        """Generate base application styles with coherent design"""
        return f"""
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        :root {{
            {self.generate_css_variables(theme)}
        }}
        
        * {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            transition: color var(--duration-normal) var(--easing-default),
                        background-color var(--duration-normal) var(--easing-default),
                        border-color var(--duration-normal) var(--easing-default);
        }}
        
        .stApp {{
            background: linear-gradient(135deg, 
                var(--bg-gradient-start) 0%, 
                var(--bg-gradient-mid) 50%, 
                var(--bg-gradient-end) 100%);
            background-attachment: fixed;
            color: var(--text-primary);
        }}
        
        /* Typography hierarchy */
        h1 {{ font-size: var(--size-3xl); font-weight: var(--weight-bold); }}
        h2 {{ font-size: var(--size-2xl); font-weight: var(--weight-semibold); }}
        h3 {{ font-size: var(--size-xl); font-weight: var(--weight-semibold); }}
        h4 {{ font-size: var(--size-lg); font-weight: var(--weight-medium); }}
        p {{ font-size: var(--size-base); font-weight: var(--weight-normal); }}
        """
    
    def generate_animations(self) -> str:
        """Generate consistent CSS animations"""
        return """
        @keyframes gradientShift {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes shimmer {
            0% { background-position: -200% center; }
            100% { background-position: 200% center; }
        }
        
        @keyframes pulse {
            0%, 100% { 
                opacity: 1;
                transform: scale(1);
            }
            50% { 
                opacity: 0.9;
                transform: scale(1.02);
            }
        }
        
        @keyframes glow {
            0%, 100% { 
                box-shadow: 0 0 20px rgba(139, 92, 246, 0.3),
                            0 0 40px rgba(139, 92, 246, 0.2);
            }
            50% { 
                box-shadow: 0 0 30px rgba(139, 92, 246, 0.4),
                            0 0 60px rgba(139, 92, 246, 0.3);
            }
        }
        
        @keyframes float {
            0% {
                transform: translateY(0) translateX(0) scale(1);
                opacity: 0.5;
            }
            33% {
                transform: translateY(-30px) translateX(20px) scale(1.1);
                opacity: 0.8;
            }
            66% {
                transform: translateY(-20px) translateX(-20px) scale(0.9);
                opacity: 0.6;
            }
            100% {
                transform: translateY(0) translateX(0) scale(1);
                opacity: 0.5;
            }
        }
        
        /* Apply animations with consistent timing */
        .animate-fade-in { 
            animation: fadeInUp var(--duration-slow) var(--easing-default) forwards;
            opacity: 0;
        }
        
        .animate-shimmer {
            animation: shimmer 3s linear infinite;
        }
        
        .animate-pulse {
            animation: pulse 2s var(--easing-default) infinite;
        }
        
        .animate-glow {
            animation: glow 3s var(--easing-default) infinite;
        }
        
        .animate-float {
            animation: float 6s var(--easing-default) infinite;
        }
        """
    
    def generate_glass_effects(self) -> str:
        """Generate consistent glassmorphism styles"""
        return """
        /* Base glass effect */
        .glass {
            backdrop-filter: blur(var(--glass-blur));
            -webkit-backdrop-filter: blur(var(--glass-blur));
            background: var(--glass-bg);
            border: 1px solid var(--glass-border);
            border-radius: 16px;
            transition: all var(--duration-normal) var(--easing-default);
        }
        
        .glass:hover {
            background: var(--glass-bg-hover);
            border-color: var(--glass-border-hover);
            transform: translateY(-2px);
            box-shadow: var(--elevation-md);
        }
        
        /* Glass card variant */
        .glass-card {
            backdrop-filter: blur(var(--glass-blur));
            -webkit-backdrop-filter: blur(var(--glass-blur));
            background: var(--glass-bg);
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            padding: 1.5rem;
            box-shadow: var(--elevation-sm);
            transition: all var(--duration-normal) var(--easing-default);
        }
        
        .glass-card:hover {
            background: var(--glass-bg-hover);
            border-color: var(--glass-border-hover);
            transform: translateY(-4px);
            box-shadow: var(--elevation-lg);
        }
        
        /* Glass button */
        .glass-button {
            backdrop-filter: blur(var(--glass-blur));
            background: linear-gradient(135deg, var(--glass-bg), var(--glass-bg-hover));
            border: 1px solid var(--glass-border);
            border-radius: 12px;
            padding: 0.75rem 1.5rem;
            transition: all var(--duration-fast) var(--easing-default);
            position: relative;
            overflow: hidden;
        }
        
        .glass-button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, 
                transparent, 
                rgba(255, 255, 255, 0.1), 
                transparent);
            transition: left var(--duration-slow);
        }
        
        .glass-button:hover::before {
            left: 100%;
        }
        """
    
    def generate_component_styles(self) -> str:
        """Generate coherent component styles"""
        return """
        /* Headers with consistent gradient */
        h1, h2, h3 {
            background: linear-gradient(135deg, 
                var(--primary) 0%, 
                var(--secondary) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: var(--weight-semibold);
            letter-spacing: -0.02em;
            line-height: 1.2;
        }
        
        /* Buttons with Web3 style */
        .stButton > button {
            background: linear-gradient(135deg, 
                var(--primary) 0%, 
                var(--primary-dark) 100%);
            color: white;
            font-weight: var(--weight-medium);
            font-size: var(--size-base);
            padding: 0.75rem 2rem;
            border: none;
            border-radius: 12px;
            box-shadow: var(--elevation-sm);
            transition: all var(--duration-normal) var(--easing-default);
            position: relative;
            overflow: hidden;
        }
        
        .stButton > button::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, 
                transparent, 
                rgba(255, 255, 255, 0.2), 
                transparent);
            transform: translateX(-100%);
            transition: transform var(--duration-slow);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: var(--elevation-md);
        }
        
        .stButton > button:hover::after {
            transform: translateX(100%);
        }
        
        /* File uploader with glass effect */
        [data-testid="stFileUploader"] {
            background: var(--glass-bg);
            border: 2px dashed var(--glass-border);
            border-radius: 20px;
            padding: 2rem;
            transition: all var(--duration-normal) var(--easing-default);
            position: relative;
        }
        
        [data-testid="stFileUploader"]::before {
            content: '';
            position: absolute;
            inset: -2px;
            border-radius: 20px;
            padding: 2px;
            background: linear-gradient(135deg, 
                var(--primary), 
                var(--secondary));
            -webkit-mask: linear-gradient(#fff 0 0) content-box, 
                         linear-gradient(#fff 0 0);
            -webkit-mask-composite: xor;
            mask-composite: exclude;
            opacity: 0;
            transition: opacity var(--duration-normal);
        }
        
        [data-testid="stFileUploader"]:hover {
            background: var(--glass-bg-hover);
        }
        
        [data-testid="stFileUploader"]:hover::before {
            opacity: 1;
        }
        
        /* Fix for file uploader browse button */
        [data-testid="stFileUploader"] button {
            z-index: 10 !important;
            position: relative !important;
            pointer-events: auto !important;
            cursor: pointer !important;
            background: var(--primary) !important;
            color: white !important;
        }
        
        /* Ensure dropzone is clickable */
        [data-testid="stFileUploadDropzone"] {
            position: relative !important;
            z-index: 5 !important;
            pointer-events: auto !important;
        }
        
        /* Fix for upload button hover */
        [data-testid="stFileUploader"] button:hover {
            background: var(--primary-dark) !important;
            transform: scale(1.05);
            transition: all 0.2s;
        }
        
        /* Ensure file input is accessible */
        [data-testid="stFileUploader"] input[type="file"] {
            position: absolute !important;
            opacity: 0 !important;
            pointer-events: auto !important;
            z-index: 15 !important;
            cursor: pointer !important;
        }
        
        /* Metrics with coherent styling */
        [data-testid="metric-container"] {
            background: var(--glass-bg);
            border: 1px solid var(--glass-border);
            border-radius: 16px;
            padding: 1.5rem;
            box-shadow: var(--elevation-sm);
            transition: all var(--duration-normal) var(--easing-default);
            animation: fadeInUp var(--duration-slow) var(--easing-default) forwards;
            opacity: 0;
        }
        
        [data-testid="metric-container"]:nth-child(1) { animation-delay: 0.1s; }
        [data-testid="metric-container"]:nth-child(2) { animation-delay: 0.2s; }
        [data-testid="metric-container"]:nth-child(3) { animation-delay: 0.3s; }
        [data-testid="metric-container"]:nth-child(4) { animation-delay: 0.4s; }
        
        [data-testid="metric-container"]:hover {
            transform: translateY(-4px);
            box-shadow: var(--elevation-md);
            border-color: var(--glass-border-hover);
        }
        
        /* Sidebar with glass effect */
        section[data-testid="stSidebar"] {
            background: var(--bg-tertiary);
            backdrop-filter: blur(20px);
            border-right: 1px solid var(--glass-border);
        }
        
        section[data-testid="stSidebar"] .stButton > button {
            width: 100%;
            background: var(--glass-bg);
            color: var(--text-primary);
        }
        
        section[data-testid="stSidebar"] .stButton > button:hover {
            background: var(--glass-bg-hover);
        }
        
        /* Expanders with coherent style */
        .streamlit-expanderHeader {
            background: var(--glass-bg);
            border-radius: 12px;
            padding: 0.75rem 1rem;
            transition: all var(--duration-normal) var(--easing-default);
            border: 1px solid var(--glass-border);
        }
        
        .streamlit-expanderHeader:hover {
            background: var(--glass-bg-hover);
            border-color: var(--glass-border-hover);
        }
        
        /* Charts with glass container */
        .js-plotly-plot {
            border-radius: 16px;
            overflow: hidden;
            box-shadow: var(--elevation-sm);
            background: var(--glass-bg);
            padding: 1rem;
            animation: fadeInUp var(--duration-slow) var(--easing-default);
        }
        """
    
    def generate_metric_card_styles(self) -> str:
        """Generate coherent metric card styles"""
        return """
        .metric-card-enhanced {
            background: var(--glass-bg);
            backdrop-filter: blur(var(--glass-blur));
            border-radius: 20px;
            padding: 1.5rem;
            text-align: center;
            border: 1px solid var(--glass-border);
            box-shadow: var(--elevation-sm);
            transition: all var(--duration-normal) var(--easing-default);
            animation: fadeInUp var(--duration-slow) var(--easing-default);
            position: relative;
            overflow: hidden;
        }
        
        .metric-card-enhanced::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, 
                var(--primary), 
                var(--secondary));
            transform: scaleX(0);
            transition: transform var(--duration-normal) var(--easing-default);
        }
        
        .metric-card-enhanced:hover {
            transform: translateY(-8px);
            box-shadow: var(--elevation-lg);
            border-color: var(--glass-border-hover);
        }
        
        .metric-card-enhanced:hover::before {
            transform: scaleX(1);
        }
        
        /* Semantic color variants */
        .metric-card-enhanced.positive {
            background: linear-gradient(135deg, 
                rgba(16, 185, 129, 0.05), 
                rgba(16, 185, 129, 0.02));
            border-color: rgba(16, 185, 129, 0.3);
        }
        
        .metric-card-enhanced.positive:hover {
            background: linear-gradient(135deg, 
                rgba(16, 185, 129, 0.08), 
                rgba(16, 185, 129, 0.04));
            border-color: rgba(16, 185, 129, 0.5);
        }
        
        .metric-card-enhanced.negative {
            background: linear-gradient(135deg, 
                rgba(239, 68, 68, 0.05), 
                rgba(239, 68, 68, 0.02));
            border-color: rgba(239, 68, 68, 0.3);
        }
        
        .metric-card-enhanced.negative:hover {
            background: linear-gradient(135deg, 
                rgba(239, 68, 68, 0.08), 
                rgba(239, 68, 68, 0.04));
            border-color: rgba(239, 68, 68, 0.5);
        }
        
        .metric-card-enhanced.neutral {
            background: linear-gradient(135deg, 
                rgba(107, 114, 128, 0.05), 
                rgba(107, 114, 128, 0.02));
            border-color: rgba(107, 114, 128, 0.3);
        }
        
        .metric-card-enhanced.neutral:hover {
            background: linear-gradient(135deg, 
                rgba(107, 114, 128, 0.08), 
                rgba(107, 114, 128, 0.04));
            border-color: rgba(107, 114, 128, 0.5);
        }
        
        /* Metric components */
        .metric-icon {
            font-size: var(--size-3xl);
            margin-bottom: 0.5rem;
            opacity: 0.8;
            transition: all var(--duration-normal) var(--easing-default);
        }
        
        .metric-card-enhanced:hover .metric-icon {
            transform: scale(1.1);
            opacity: 1;
        }
        
        .metric-title {
            font-size: var(--size-sm);
            color: var(--text-tertiary);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-weight: var(--weight-medium);
            margin-bottom: 0.5rem;
        }
        
        .metric-value-large {
            font-size: var(--size-2xl);
            font-weight: var(--weight-bold);
            margin: 0.5rem 0;
            background: linear-gradient(135deg, 
                var(--primary), 
                var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .metric-delta {
            font-size: var(--size-sm);
            color: var(--text-tertiary);
            font-weight: var(--weight-normal);
        }
        """
    
    def generate_particle_styles(self) -> str:
        """Generate consistent particle animation styles"""
        return """
        .particles-container {
            position: fixed;
            width: 100%;
            height: 100%;
            overflow: hidden;
            z-index: -1;
            pointer-events: none;
            opacity: 0.6;
        }
        
        .particle {
            position: absolute;
            width: 3px;
            height: 3px;
            background: var(--primary-glow);
            border-radius: 50%;
            filter: blur(1px);
            animation: float var(--duration-ambient) infinite;
        }
        
        .particle:nth-child(2n) {
            background: var(--secondary-glow);
            width: 2px;
            height: 2px;
        }
        
        .particle:nth-child(3n) {
            background: var(--accent-light);
            width: 4px;
            height: 4px;
        }
        
        /* Staggered animation delays for natural movement */
        .particle:nth-child(1) { 
            left: 10%; 
            animation-duration: 18s;
            animation-delay: 0s;
        }
        .particle:nth-child(2) { 
            left: 25%; 
            animation-duration: 22s;
            animation-delay: 3s;
        }
        .particle:nth-child(3) { 
            left: 40%; 
            animation-duration: 20s;
            animation-delay: 1s;
        }
        .particle:nth-child(4) { 
            left: 60%; 
            animation-duration: 24s;
            animation-delay: 4s;
        }
        .particle:nth-child(5) { 
            left: 75%; 
            animation-duration: 19s;
            animation-delay: 2s;
        }
        .particle:nth-child(6) { 
            left: 90%; 
            animation-duration: 21s;
            animation-delay: 5s;
        }
        """
    
    def generate_special_effects(self) -> str:
        """Generate special Web3 effects"""
        return """
        /* Gradient borders */
        .gradient-border {
            position: relative;
            background: var(--bg-tertiary);
            border-radius: 16px;
            padding: 1px;
        }
        
        .gradient-border::before {
            content: '';
            position: absolute;
            inset: 0;
            border-radius: 16px;
            padding: 1px;
            background: linear-gradient(135deg, 
                var(--primary), 
                var(--secondary),
                var(--accent));
            -webkit-mask: linear-gradient(#fff 0 0) content-box, 
                         linear-gradient(#fff 0 0);
            -webkit-mask-composite: xor;
            mask-composite: exclude;
        }
        
        /* Animated gradient text */
        .gradient-text-animated {
            background: linear-gradient(90deg, 
                var(--primary) 0%, 
                var(--secondary) 25%, 
                var(--primary) 50%, 
                var(--secondary) 75%, 
                var(--primary) 100%);
            background-size: 200% auto;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: shimmer 3s linear infinite;
        }
        
        /* Neon glow effect */
        .neon-glow {
            text-shadow: 
                0 0 10px var(--primary-glow),
                0 0 20px var(--primary-glow),
                0 0 30px var(--primary),
                0 0 40px var(--primary);
            animation: pulse 2s var(--easing-default) infinite;
        }
        
        /* Holographic effect */
        .holographic {
            background: linear-gradient(135deg, 
                var(--primary), 
                var(--secondary), 
                var(--accent), 
                var(--primary));
            background-size: 200% 200%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: gradientShift var(--duration-ambient) ease infinite;
        }
        """
    
    def get_complete_css(self, dark_mode: bool) -> str:
        """Get complete CSS for the application"""
        theme = self.get_theme(dark_mode)
        
        css_parts = [
            self.generate_base_styles(theme),
            self.generate_animations(),
            self.generate_glass_effects(),
            self.generate_component_styles(),
            self.generate_metric_card_styles(),
            self.generate_particle_styles(),
            self.generate_special_effects()
        ]
        
        return '\n'.join(css_parts)


class UIComponents:
    """Helper class for generating UI components with consistent styling"""
    
    @staticmethod
    def animated_header(title: str, subtitle: str = "") -> str:
        """Generate animated header HTML with Web3 style"""
        return f"""
        <div class="animate-fade-in" style="text-align: center; padding: 3rem 0;">
            <h1 class="gradient-text-animated" style="font-size: var(--size-4xl); margin-bottom: 1rem;">
                {title}
            </h1>
            {f'<p style="color: var(--text-secondary); font-size: var(--size-lg);">{subtitle}</p>' if subtitle else ''}
        </div>
        """
    
    @staticmethod
    def floating_particles() -> str:
        """Generate floating particles HTML"""
        return """
        <div class="particles-container">
            <div class="particle"></div>
            <div class="particle"></div>
            <div class="particle"></div>
            <div class="particle"></div>
            <div class="particle"></div>
            <div class="particle"></div>
        </div>
        """
    
    @staticmethod
    def metric_card(icon: str, title: str, value: str, delta: str = "", card_type: str = "") -> str:
        """Generate metric card HTML with coherent styling"""
        class_name = f"metric-card-enhanced {card_type}" if card_type else "metric-card-enhanced"
        return f"""
        <div class="{class_name}">
            <div class="metric-icon">{icon}</div>
            <div class="metric-title">{title}</div>
            <div class="metric-value-large">{value}</div>
            {f'<div class="metric-delta">{delta}</div>' if delta else ''}
        </div>
        """
    
    @staticmethod
    def glass_container(content: str, style: str = "") -> str:
        """Generate glass container HTML"""
        return f"""
        <div class="glass-card" style="{style}">
            {content}
        </div>
        """
    
    @staticmethod
    def upload_section() -> str:
        """Generate upload section with glass container"""
        return """
        <div class="glass-card" style="margin: 2rem 0; padding: 2rem;">
            <h3 class="gradient-text-animated" style="margin-bottom: 1.5rem;">Upload Data</h3>
        </div>
        """
    
    @staticmethod
    def results_header() -> str:
        """Generate results section header"""
        return """
        <div class="animate-fade-in" style="text-align: center; margin: 3rem 0;">
            <h2 class="holographic" style="font-size: var(--size-3xl);">
                Sentiment Analysis Results
            </h2>
        </div>
        """
    
    @staticmethod
    def gradient_footer(primary_text: str, secondary_text: str) -> str:
        """Generate gradient footer HTML"""
        return f"""
        <div class="glass-card animate-fade-in" style="margin-top: 4rem; padding: 2rem; text-align: center;">
            <p class="gradient-text-animated" style="
                font-weight: var(--weight-semibold);
                font-size: var(--size-lg);
                margin: 0 0 0.5rem 0;
            ">{primary_text}</p>
            <p style="color: var(--text-tertiary); font-size: var(--size-base); margin: 0;">
                {secondary_text}
            </p>
        </div>
        """
    
    @staticmethod
    def section_divider() -> str:
        """Generate a section divider with gradient"""
        return """
        <div style="margin: 2rem 0; height: 2px; background: linear-gradient(90deg, 
            transparent, 
            var(--primary), 
            var(--secondary), 
            transparent);
            opacity: 0.5;">
        </div>
        """
    
    @staticmethod
    def loading_spinner() -> str:
        """Generate loading spinner with Web3 style"""
        return """
        <div style="display: flex; justify-content: center; align-items: center; padding: 2rem;">
            <div class="animate-pulse" style="
                width: 60px;
                height: 60px;
                border: 3px solid var(--glass-border);
                border-top-color: var(--primary);
                border-radius: 50%;
                animation: spin 1s linear infinite;
            "></div>
        </div>
        <style>
            @keyframes spin {
                to { transform: rotate(360deg); }
            }
        </style>
        """


def inject_styles(dark_mode: bool) -> str:
    """Main function to inject all styles into the app"""
    theme_manager = ThemeManager()
    css = theme_manager.get_complete_css(dark_mode)
    
    # Add any additional runtime styles
    additional_css = """
    /* Ensure smooth transitions on theme change */
    * {
        transition-duration: 0.3s !important;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-tertiary);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, var(--primary-light), var(--secondary-light));
    }
    """
    
    return f"<style>{css}{additional_css}</style>"