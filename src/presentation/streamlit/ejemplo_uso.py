"""
Ejemplo de uso del CSS Loader modular en Streamlit
Demuestra cómo integrar los estilos CSS modulares con componentes
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from css_loader import (
    load_css,
    load_component_css,
    glass_card,
    metric_card,
    section_header,
    with_css
)


def main():
    """Función principal de ejemplo"""
    # Configuración de página
    st.set_page_config(
        page_title="CSS Modular Demo",
        page_icon="🎨",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Cargar CSS principal
    load_css()
    
    # Header principal usando componente personalizado
    section_header(
        title="🎨 Demo CSS Modular",
        subtitle="Demostración de la arquitectura CSS modular para Streamlit"
    )
    
    # Métricas usando componentes glass
    st.markdown("## 📊 Métricas de Ejemplo")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        metric_card(
            title="Total Usuarios",
            value="12,345",
            change=15.3,
            icon="👥"
        )
    
    with col2:
        metric_card(
            title="Ingresos",
            value="$89,432",
            change=-2.4,
            icon="💰"
        )
    
    with col3:
        metric_card(
            title="Conversión",
            value="24.8%",
            change=8.1,
            icon="🎯"
        )
    
    with col4:
        metric_card(
            title="Satisfacción",
            value="4.7/5",
            change=0.2,
            icon="⭐"
        )
    
    # Sección de gráficos
    demo_charts_section()
    
    # Sección de formularios
    demo_forms_section()
    
    # Sección de componentes layout
    demo_layout_section()


@with_css("charts")
def demo_charts_section():
    """Demostración de componentes de gráficos"""
    section_header(
        title="📈 Visualizaciones",
        subtitle="Gráficos con estilos CSS modulares"
    )
    
    # Datos de ejemplo
    df = pd.DataFrame({
        'mes': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
        'ventas': [1200, 1900, 1600, 2100, 1800, 2400],
        'usuarios': [450, 680, 520, 780, 620, 850]
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig1 = px.line(df, x='mes', y='ventas', title="Tendencia de Ventas")
        fig1.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = px.bar(df, x='mes', y='usuarios', title="Usuarios por Mes")
        fig2.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        st.plotly_chart(fig2, use_container_width=True)


@with_css("forms")
def demo_forms_section():
    """Demostración de componentes de formularios"""
    section_header(
        title="📝 Formularios",
        subtitle="Inputs y controles con estilos modulares"
    )
    
    # Crear contenedor glass para el formulario
    glass_card_content = """
    <h3 class="text-gradient mb-4">Configuración de Análisis</h3>
    """
    
    with st.container():
        st.markdown(glass_card_content, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Nombre del Proyecto", placeholder="Ingresa el nombre...")
            
            analysis_type = st.selectbox(
                "Tipo de Análisis",
                ["Sentimientos", "Temas", "Completo"]
            )
            
            confidence = st.slider("Nivel de Confianza", 0.0, 1.0, 0.8)
        
        with col2:
            description = st.text_area(
                "Descripción", 
                placeholder="Describe tu análisis...",
                height=100
            )
            
            use_advanced = st.checkbox("Análisis Avanzado")
            
            if st.button("🚀 Iniciar Análisis", type="primary"):
                st.success("¡Análisis iniciado exitosamente!")


def demo_layout_section():
    """Demostración de componentes de layout"""
    section_header(
        title="🏗️ Layout Components",
        subtitle="Tarjetas, grids y estructuras"
    )
    
    # Grid de tarjetas
    st.markdown("""
    <div class="stats-grid">
        <div class="glass-card animate-fade-in">
            <h4 class="text-primary mb-2">📊 Analytics</h4>
            <p class="text-secondary">Panel de métricas y KPIs principales para seguimiento.</p>
            <div class="mt-4">
                <span class="text-success font-semibold">↗ +12.3%</span>
            </div>
        </div>
        
        <div class="glass-card animate-fade-in animate-delay-100">
            <h4 class="text-primary mb-2">🤖 IA Analysis</h4>
            <p class="text-secondary">Análisis inteligente de sentimientos y temas.</p>
            <div class="mt-4">
                <span class="text-info font-semibold">🔄 Procesando</span>
            </div>
        </div>
        
        <div class="glass-card animate-fade-in animate-delay-200">
            <h4 class="text-primary mb-2">📈 Reports</h4>
            <p class="text-secondary">Reportes detallados y exportación de datos.</p>
            <div class="mt-4">
                <span class="text-warning font-semibold">⏳ Pendiente</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Divider
    st.markdown('<hr class="divider-thick">', unsafe_allow_html=True)
    
    # Hero section
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">CSS Modular</h1>
        <p class="hero-subtitle">
            Arquitectura escalable y mantenible para aplicaciones Streamlit modernas
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="main-footer">
        <div class="footer-content">
            <p class="footer-text">
                Construido con 💜 usando arquitectura CSS modular
            </p>
            <div class="footer-links">
                <a href="#" class="footer-link">Documentación</a>
                <a href="#" class="footer-link">GitHub</a>
                <a href="#" class="footer-link">Soporte</a>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()