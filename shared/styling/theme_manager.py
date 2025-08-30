"""
Theme Manager - Extracted from original ui_styling.py
Preserves all modern styling and sophisticated theme systems
"""

from typing import Dict, Any


class ThemeManager:
    """Manages color themes and CSS generation for the application"""
    
    def __init__(self) -> None:
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
                'glass_border': 'rgba(139, 92, 246, 0.1)',
                'glass_border_hover': 'rgba(139, 92, 246, 0.15)',
                
                # Text colors with proper contrast
                'text_primary': '#F9FAFB',
                'text_secondary': '#D1D5DB',
                'text_muted': '#9CA3AF',
                'text_accent': '#C4B5FD',
            },
            
            'light': {
                # Light theme colors (complete professional theme)
                'primary': '#7C3AED',
                'primary_light': '#8B5CF6',
                'primary_dark': '#6D28D9',
                'primary_glow': '#A78BFA',
                
                'secondary': '#0891B2',
                'secondary_light': '#06B6D4',
                'secondary_dark': '#0E7490',
                'secondary_glow': '#22D3EE',
                
                'accent': '#D97706',
                'accent_light': '#F59E0B',
                
                'positive': '#059669',
                'positive_light': '#10B981',
                'negative': '#DC2626',
                'negative_light': '#EF4444',
                'neutral': '#4B5563',
                'neutral_light': '#6B7280',
                
                'bg_primary': '#FFFFFF',
                'bg_secondary': '#F9FAFB',
                'bg_tertiary': '#F3F4F6',
                'bg_gradient_start': '#FFFFFF',
                'bg_gradient_mid': '#F9FAFB',
                'bg_gradient_end': '#F3F4F6',
                
                'glass_bg': 'rgba(124, 58, 237, 0.03)',
                'glass_bg_hover': 'rgba(124, 58, 237, 0.06)',
                'glass_border': 'rgba(124, 58, 237, 0.1)',
                'glass_border_hover': 'rgba(124, 58, 237, 0.15)',
                
                'text_primary': '#111827',
                'text_secondary': '#374151',
                'text_muted': '#6B7280',
                'text_accent': '#7C3AED',
            }
        }
    
    def get_theme_colors(self, theme_name: str = 'dark') -> Dict[str, str]:
        """Get color system for specified theme"""
        return self.color_systems.get(theme_name, self.color_systems['dark'])
    
    def generate_css_variables(self, theme_name: str = 'dark') -> str:
        """Generate CSS custom properties for consistent theming"""
        colors = self.get_theme_colors(theme_name)
        
        css_vars = ":root {\n"
        for key, value in colors.items():
            css_vars += f"    --color-{key.replace('_', '-')}: {value};\n"
        
        # Typography system
        css_vars += """
        /* Typography Scale */
        --size-xs: 0.75rem;
        --size-sm: 0.875rem;
        --size-base: 1rem;
        --size-lg: 1.125rem;
        --size-xl: 1.25rem;
        --size-2xl: 1.5rem;
        --size-3xl: 1.875rem;
        
        /* Font Weights */
        --weight-light: 300;
        --weight-normal: 400;
        --weight-medium: 500;
        --weight-semibold: 600;
        --weight-bold: 700;
        """
        
        css_vars += "}\n"
        return css_vars
    
    def generate_base_styles(self) -> str:
        """Generate base typography and layout styles"""
        return """
        h1 { font-size: var(--size-3xl); font-weight: var(--weight-bold); }
        h2 { font-size: var(--size-2xl); font-weight: var(--weight-semibold); }
        h3 { font-size: var(--size-xl); font-weight: var(--weight-semibold); }
        h4 { font-size: var(--size-lg); font-weight: var(--weight-medium); }
        p { font-size: var(--size-base); font-weight: var(--weight-normal); }
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
        """