"""
UI Styling Module for Comment Analyzer
Centralized styling system with clean CSS generation
"""

from typing import Dict, Any


class ThemeManager:
    """Manages color themes and CSS generation for the application"""
    
    def __init__(self):
        self.color_systems = {
            'dark': {
                'primary': '#8B5CF6',
                'primary_light': '#A78BFA',
                'primary_dark': '#7C3AED',
                'secondary': '#06B6D4',
                'secondary_light': '#22D3EE',
                'accent': '#F59E0B',
                'positive': '#10B981',
                'negative': '#EF4444',
                'neutral': '#6B7280',
                'bg_start': '#0F0E13',
                'bg_mid': '#1A1825',
                'bg_end': '#16151F',
                'glass_bg': 'rgba(139, 92, 246, 0.05)',
                'glass_border': 'rgba(139, 92, 246, 0.2)',
                'text_primary': '#F3F4F6',
                'text_secondary': '#9CA3AF'
            },
            'light': {
                'primary': '#8B5CF6',
                'primary_light': '#A78BFA',
                'primary_dark': '#7C3AED',
                'secondary': '#06B6D4',
                'secondary_light': '#22D3EE',
                'accent': '#F59E0B',
                'positive': '#10B981',
                'negative': '#EF4444',
                'neutral': '#6B7280',
                'bg_start': '#FAFAFA',
                'bg_mid': '#F3E8FF',
                'bg_end': '#E0F2FE',
                'glass_bg': 'rgba(255, 255, 255, 0.7)',
                'glass_border': 'rgba(139, 92, 246, 0.3)',
                'text_primary': '#1F2937',
                'text_secondary': '#6B7280'
            }
        }
    
    def get_theme(self, dark_mode: bool) -> Dict[str, str]:
        """Get theme colors based on mode"""
        return self.color_systems['dark' if dark_mode else 'light']
    
    def generate_css_variables(self, theme: Dict[str, str]) -> str:
        """Generate CSS custom properties"""
        variables = []
        for key, value in theme.items():
            css_key = key.replace('_', '-')
            variables.append(f"--{css_key}: {value};")
        return "\n".join(variables)
    
    def generate_base_styles(self, theme: Dict[str, str]) -> str:
        """Generate base application styles"""
        return f"""
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        :root {{
            {self.generate_css_variables(theme)}
        }}
        
        * {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }}
        
        .stApp {{
            background: linear-gradient(135deg, var(--bg-start) 0%, var(--bg-mid) 50%, var(--bg-end) 100%);
        }}
        """
    
    def generate_animations(self) -> str:
        """Generate CSS animations"""
        return """
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }
        
        @keyframes shimmer {
            to { background-position: 200% center; }
        }
        
        @keyframes glow {
            0%, 100% { 
                filter: brightness(1) drop-shadow(0 0 3px var(--primary-alpha-40)); 
            }
            50% { 
                filter: brightness(1.1) drop-shadow(0 0 8px var(--primary-alpha-60)); 
            }
        }
        
        @keyframes float {
            0% {
                transform: translateY(100vh) scale(0);
                opacity: 0;
            }
            10% {
                opacity: 0.5;
            }
            90% {
                opacity: 0.5;
            }
            100% {
                transform: translateY(-100vh) scale(1.5);
                opacity: 0;
            }
        }
        
        @keyframes slideInRight {
            from {
                transform: translateX(-100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        """
    
    def generate_glass_effects(self) -> str:
        """Generate glassmorphism styles"""
        return """
        .glass-card {
            backdrop-filter: blur(12px);
            background: var(--glass-bg);
            border: 1px solid var(--glass-border);
            border-radius: 16px;
            box-shadow: 0 8px 32px 0 rgba(139, 92, 246, 0.15);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .glass-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 40px 0 rgba(139, 92, 246, 0.25);
            border-color: var(--primary-light);
            background: rgba(139, 92, 246, 0.08);
        }
        """
    
    def generate_component_styles(self) -> str:
        """Generate component-specific styles"""
        return """
        /* Section headers */
        .section-title {
            margin-top: 0;
            margin-bottom: 1rem;
            color: var(--text-primary);
        }
        
        .upload-section {
            padding: 2rem;
            margin: 2rem 0;
        }
        
        .results-header {
            margin: 2rem 0;
            text-align: center;
        }
        
        .gradient-text {
            background: linear-gradient(90deg, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2rem;
            margin-bottom: 2rem;
        }
        
        /* Headers */
        h1, h2, h3 {
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 600;
            animation: glow 4s ease-in-out infinite;
        }
        
        /* Buttons */
        .stButton > button {
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
            color: white;
            font-weight: 600;
            letter-spacing: 0.025em;
            padding: 0.75rem 2rem;
            border: none;
            border-radius: 12px;
            position: relative;
            overflow: hidden;
            transition: all 0.3s;
        }
        
        .stButton > button::before {
            content: "";
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
            transition: left 0.6s;
        }
        
        .stButton > button:hover::before {
            left: 100%;
        }
        
        .stButton > button:hover {
            transform: scale(1.02);
            box-shadow: 0 10px 30px rgba(139, 92, 246, 0.4);
            background: linear-gradient(135deg, var(--primary-light) 0%, var(--primary) 100%);
        }
        
        /* File Uploader */
        [data-testid="stFileUploader"] {
            background: var(--glass-bg);
            border: 2px dashed var(--glass-border);
            border-radius: 20px;
            padding: 2rem;
            transition: all 0.3s;
        }
        
        [data-testid="stFileUploader"]:hover {
            border-color: var(--primary);
            background: rgba(139, 92, 246, 0.08);
            box-shadow: 0 0 30px rgba(139, 92, 246, 0.3);
        }
        
        /* Metrics */
        [data-testid="metric-container"] {
            background: var(--glass-bg);
            border: 1px solid var(--glass-border);
            border-radius: 16px;
            padding: 1.5rem;
            position: relative;
            animation: fadeInUp 0.5s ease-out;
            animation-fill-mode: both;
        }
        
        [data-testid="metric-container"]:nth-child(1) { animation-delay: 0.1s; }
        [data-testid="metric-container"]:nth-child(2) { animation-delay: 0.2s; }
        [data-testid="metric-container"]:nth-child(3) { animation-delay: 0.3s; }
        [data-testid="metric-container"]:nth-child(4) { animation-delay: 0.4s; }
        
        /* Sidebar */
        section[data-testid="stSidebar"] {
            background: rgba(15, 15, 35, 0.7);
            backdrop-filter: blur(20px);
            border-right: 1px solid var(--glass-border);
        }
        
        /* Expanders */
        .streamlit-expanderHeader {
            background: var(--glass-bg);
            border-radius: 12px;
            transition: all 0.3s;
        }
        
        .streamlit-expanderHeader:hover {
            background: rgba(139, 92, 246, 0.15);
        }
        
        /* Alerts */
        .stAlert {
            backdrop-filter: blur(10px);
            background: var(--glass-bg);
            border-left: 4px solid;
            animation: slideInRight 0.5s ease-out;
        }
        
        /* Charts */
        .js-plotly-plot {
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 8px 32px rgba(139, 92, 246, 0.2);
            animation: fadeIn 1s ease-out;
        }
        
        /* Animated background */
        .main::before {
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(-45deg, var(--bg-start), var(--bg-mid), var(--bg-end), rgba(139, 92, 246, 0.1));
            background-size: 400% 400%;
            animation: gradientShift 20s ease infinite;
            z-index: -1;
        }
        """
    
    def generate_metric_card_styles(self) -> str:
        """Generate metric card specific styles"""
        return """
        .metric-card-enhanced {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 1.5rem;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            animation: slideUp 0.6s ease-out;
        }
        
        .metric-card-enhanced:hover {
            transform: translateY(-10px) scale(1.02);
            box-shadow: 0 20px 40px rgba(139, 92, 246, 0.3);
        }
        
        .metric-card-enhanced.positive {
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(16, 185, 129, 0.1));
            border-color: rgba(16, 185, 129, 0.5);
        }
        
        .metric-card-enhanced.neutral {
            background: linear-gradient(135deg, rgba(107, 114, 128, 0.2), rgba(107, 114, 128, 0.1));
            border-color: rgba(107, 114, 128, 0.5);
        }
        
        .metric-card-enhanced.negative {
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.2), rgba(239, 68, 68, 0.1));
            border-color: rgba(239, 68, 68, 0.5);
        }
        
        .metric-icon {
            font-size: 3rem;
            margin-bottom: 0.5rem;
            animation: bounce 2s infinite;
            font-weight: 300;
            opacity: 0.8;
        }
        
        .metric-title {
            font-size: 0.9rem;
            opacity: 0.7;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .metric-value-large {
            font-size: 2.5rem;
            font-weight: 700;
            margin: 0.5rem 0;
            background: linear-gradient(90deg, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .metric-delta {
            font-size: 0.9rem;
            opacity: 0.6;
        }
        """
    
    def generate_particle_styles(self) -> str:
        """Generate particle animation styles"""
        return """
        .particles-container {
            position: fixed;
            width: 100%;
            height: 100%;
            overflow: hidden;
            z-index: -1;
            pointer-events: none;
        }
        
        .particle {
            position: absolute;
            width: 4px;
            height: 4px;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            border-radius: 50%;
            animation: float 20s infinite;
            opacity: 0.5;
        }
        
        .particle:nth-child(1) {
            left: 10%;
            animation-duration: 15s;
            animation-delay: 0s;
        }
        
        .particle:nth-child(2) {
            left: 30%;
            animation-duration: 20s;
            animation-delay: 2s;
        }
        
        .particle:nth-child(3) {
            left: 50%;
            animation-duration: 18s;
            animation-delay: 4s;
        }
        
        .particle:nth-child(4) {
            left: 70%;
            animation-duration: 22s;
            animation-delay: 6s;
        }
        
        .particle:nth-child(5) {
            left: 90%;
            animation-duration: 16s;
            animation-delay: 8s;
        }
        """
    
    def get_complete_css(self, dark_mode: bool) -> str:
        """Get complete CSS for the application"""
        theme = self.get_theme(dark_mode)
        
        # Add computed alpha values for easier use
        theme['primary-alpha-40'] = theme['primary'] + '66'  # 40% opacity in hex
        theme['primary-alpha-60'] = theme['primary'] + '99'  # 60% opacity in hex
        
        css_parts = [
            self.generate_base_styles(theme),
            self.generate_animations(),
            self.generate_glass_effects(),
            self.generate_component_styles(),
            self.generate_metric_card_styles(),
            self.generate_particle_styles()
        ]
        
        return '\n'.join(css_parts)


class UIComponents:
    """Helper class for generating UI components with consistent styling"""
    
    @staticmethod
    def animated_header(title: str, subtitle: str = "") -> str:
        """Generate animated header HTML"""
        return f"""
        <div style="text-align: center; padding: 2rem 0;">
            <h1 class="animated-title">{title}</h1>
            {f'<p class="animated-subtitle">{subtitle}</p>' if subtitle else ''}
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
        </div>
        """
    
    @staticmethod
    def metric_card(icon: str, title: str, value: str, delta: str = "", card_type: str = "") -> str:
        """Generate metric card HTML"""
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
        <div class="glass-card upload-section">
            <h3 class="section-title">Upload Data</h3>
        </div>
        """
    
    @staticmethod
    def results_header() -> str:
        """Generate results section header"""
        return """
        <div class="results-header">
            <h2 class="gradient-text">Sentiment Analysis Results</h2>
        </div>
        """
    
    @staticmethod
    def gradient_footer(primary_text: str, secondary_text: str) -> str:
        """Generate gradient footer HTML"""
        return f"""
        <div class="glass-card" style="margin-top: 4rem; padding: 2rem; text-align: center;">
            <p style="
                background: linear-gradient(90deg, var(--primary), var(--secondary));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-weight: 600;
                font-size: 1.1rem;
                margin: 0 0 0.5rem 0;
            ">{primary_text}</p>
            <p style="color: var(--text-secondary); font-size: 0.9rem; margin: 0;">
                {secondary_text}
            </p>
        </div>
        """


def inject_styles(dark_mode: bool) -> str:
    """Main function to inject all styles into the app"""
    theme_manager = ThemeManager()
    css = theme_manager.get_complete_css(dark_mode)
    
    # Add special styles for animated title
    additional_css = """
    .animated-title {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 50%, var(--primary) 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shimmer 3s linear infinite;
        margin: 0 0 1rem 0;
    }
    
    .animated-subtitle {
        font-size: 1.2rem;
        opacity: 0.8;
        animation: fadeIn 1s ease-out;
        color: var(--text-primary);
        margin: 0;
    }
    """
    
    return f"<style>{css}{additional_css}</style>"