"""
UI Components - Sophisticated modern styling components
Extracted from original ui_styling.py to preserve professional UX
"""

class UIComponents:
    """Helper class for generating UI components with consistent modern styling"""
    
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
        """Generate floating particles HTML that won't block interactions"""
        return """
        <div class="particles-container" style="pointer-events: none !important; z-index: -999 !important;">
            <div class="particle" style="pointer-events: none;"></div>
            <div class="particle" style="pointer-events: none;"></div>
            <div class="particle" style="pointer-events: none;"></div>
        </div>
        """
    
    @staticmethod
    def glass_container(content: str) -> str:
        """Generate glass container HTML"""
        return f"""
        <div class="glass-card">
            {content}
        </div>
        """
    
    @staticmethod
    def status_badge(icon: str, text: str, badge_type: str = "neutral") -> str:
        """Generate status badge HTML with theme colors"""
        return f"""
        <div class="status-badge {badge_type}">
            <span class="badge-icon">{icon}</span>
            <span class="badge-text">{text}</span>
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
                margin-bottom: 0.5rem;
            ">{primary_text}</p>
            <p style="color: var(--text-muted); font-size: var(--size-sm);">
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
            border-radius: 1px;">
        </div>
        """
    
    @staticmethod
    def progress_indicator(progress: float, text: str = "") -> str:
        """Generate animated progress indicator"""
        return f"""
        <div class="progress-container" style="margin: 1rem 0;">
            <div class="progress-bar" style="
                width: 100%;
                height: 8px;
                background: var(--glass-bg);
                border-radius: 4px;
                overflow: hidden;
                position: relative;
            ">
                <div class="progress-fill" style="
                    width: {progress}%;
                    height: 100%;
                    background: linear-gradient(90deg, var(--primary), var(--secondary));
                    border-radius: 4px;
                    transition: width 0.3s ease;
                "></div>
            </div>
            {f'<p style="color: var(--text-secondary); font-size: var(--size-sm); margin-top: 0.5rem;">{text}</p>' if text else ''}
        </div>
        """
    
    @staticmethod
    def metric_card(title: str, value: str, trend: str = "", color: str = "primary") -> str:
        """Generate metric card with glass effect"""
        return f"""
        <div class="glass-card metric-card" style="
            text-align: center;
            padding: 1.5rem;
            transition: all 0.3s ease;
        ">
            <h3 style="color: var(--text-secondary); font-size: var(--size-sm); margin-bottom: 0.5rem;">
                {title}
            </h3>
            <p style="
                font-size: var(--size-2xl);
                font-weight: var(--weight-bold);
                color: var(--{color});
                margin-bottom: 0.25rem;
            ">{value}</p>
            {f'<p style="color: var(--text-muted); font-size: var(--size-xs);">{trend}</p>' if trend else ''}
        </div>
        """
    
    @staticmethod
    def alert_banner(message: str, alert_type: str = "info") -> str:
        """Generate alert banner with modern styling"""
        colors = {
            "info": "var(--secondary)",
            "success": "var(--positive)", 
            "warning": "var(--accent)",
            "error": "var(--negative)"
        }
        
        return f"""
        <div class="alert-banner {alert_type}" style="
            background: linear-gradient(135deg, 
                {colors.get(alert_type, colors['info'])}20,
                {colors.get(alert_type, colors['info'])}10);
            border-left: 4px solid {colors.get(alert_type, colors['info'])};
            padding: 1rem 1.5rem;
            border-radius: 8px;
            margin: 1rem 0;
        ">
            <p style="color: var(--text-primary); margin: 0;">{message}</p>
        </div>
        """