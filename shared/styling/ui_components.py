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
    def status_badge(icon: str, text: str, badge_type: str = "neutral", aria_label: str = "") -> str:
        """Generate accessible status badge HTML with theme colors"""
        aria_description = aria_label or f"Estado: {text}"
        return f"""
        <div class="status-badge {badge_type}" 
             role="status" 
             aria-live="polite" 
             aria-label="{aria_description}"
             tabindex="0">
            <span class="badge-icon" aria-hidden="true">{icon}</span>
            <span class="badge-text">{text}</span>
            <span class="sr-only">{aria_description}</span>
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
    def file_preview_header(filename: str, filesize: str, rows: int, columns: int) -> str:
        """Generate accessible file preview header with stats"""
        aria_label = f"Vista previa del archivo {filename}: {rows} filas, {columns} columnas, tamaño {filesize}"
        return f"""
        <div class="file-preview" 
             role="region" 
             aria-label="{aria_label}"
             tabindex="0">
            <div class="file-preview-header">
                <div class="file-preview-title">Vista Previa del Archivo</div>
                <div class="file-preview-info">{filename}</div>
            </div>
            <div class="file-preview-stats" role="group" aria-label="Estadísticas del archivo">
                <div class="file-stat" role="figure" aria-label="Tamaño del archivo: {filesize}">
                    <div class="file-stat-value">{filesize}</div>
                    <div class="file-stat-label">Tamaño</div>
                </div>
                <div class="file-stat" role="figure" aria-label="Número de filas: {rows}">
                    <div class="file-stat-value">{rows}</div>
                    <div class="file-stat-label">Filas</div>
                </div>
                <div class="file-stat" role="figure" aria-label="Número de columnas: {columns}">
                    <div class="file-stat-value">{columns}</div>
                    <div class="file-stat-label">Columnas</div>
                </div>
            </div>
            <div class="sr-only">{aria_label}</div>
        </div>
        """
    
    @staticmethod
    def progress_indicator(progress: float, text: str = "") -> str:
        """Generate accessible progress indicator with glassmorphism styling"""
        aria_label = f"Progreso del análisis: {progress}% completado"
        return f"""
        <div class="progress-indicator" 
             role="progressbar" 
             aria-valuenow="{progress}" 
             aria-valuemin="0" 
             aria-valuemax="100"
             aria-label="{aria_label}"
             tabindex="0">
            <div class="progress-bar-container">
                <div class="progress-bar-fill" style="width: {progress}%;"></div>
            </div>
            {f'<div class="progress-text">{text}</div>' if text else ''}
            <div class="sr-only">{aria_label}</div>
        </div>
        """
    
    @staticmethod
    def step_progress_indicator(steps: list, current_step: int) -> str:
        """Generate accessible step-based progress indicator"""
        steps_html = ""
        for i, step in enumerate(steps):
            status_class = "completed" if i < current_step else ("active" if i == current_step else "")
            aria_current = 'aria-current="step"' if i == current_step else ''
            steps_html += f'<div class="progress-step {status_class}" {aria_current}>{step}</div>'
        
        progress_percent = (current_step / len(steps)) * 100 if steps else 0
        aria_label = f"Progreso por pasos: paso {current_step + 1} de {len(steps)}, {progress_percent:.0f}% completado"
        
        return f"""
        <div class="progress-indicator" 
             role="progressbar" 
             aria-valuenow="{current_step}" 
             aria-valuemin="0" 
             aria-valuemax="{len(steps) - 1}"
             aria-label="{aria_label}"
             tabindex="0">
            <div class="progress-steps" role="group" aria-label="Pasos del proceso">
                {steps_html}
            </div>
            <div class="sr-only">{aria_label}</div>
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