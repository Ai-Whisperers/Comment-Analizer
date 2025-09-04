"""
Home Page - Manual introductorio para usuarios sin conocimientos técnicos
Landing page profesional con guía paso a paso
"""

import sys
import streamlit as st
from pathlib import Path

# Add shared modules to path
current_dir = Path(__file__).parent.parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from shared.styling.theme_manager_full import ThemeManager, UIComponents

# Initialize styling (PRESERVE MODERN UX)
if 'theme_manager' not in st.session_state:
    st.session_state.theme_manager = ThemeManager()
    st.session_state.ui = UIComponents()

theme = st.session_state.theme_manager
ui = st.session_state.ui

# Apply modular glassmorphism Web3 styling
from shared.styling.modular_css import initialize_modular_styles
initialize_modular_styles(dark_mode=st.session_state.get('dark_mode', True))

# Hero Header
st.markdown(
    ui.animated_header(
        title="Analizador de Comentarios",
        subtitle="Personal Paraguay | Plataforma de Análisis Inteligente"
    ),
    unsafe_allow_html=True
)

# Floating particles effect
st.markdown(ui.floating_particles(), unsafe_allow_html=True)

# Introduction Section
st.markdown("## Bienvenido a su Plataforma de Análisis")

st.markdown("""
Esta aplicación le permite **analizar comentarios de clientes** de manera profesional y obtener **insights valiosos** 
para mejorar su negocio. No necesita conocimientos técnicos - todo está diseñado para ser **fácil de usar**.
""")

# Section divider
st.markdown(ui.section_divider(), unsafe_allow_html=True)

# How it works section
st.markdown("## ¿Cómo Funciona?")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        ui.glass_container("""
        <div style="text-align: center; padding: 1rem;">
            <h4 style="color: var(--primary-purple); margin-bottom: 1rem;">Paso 1: Subir Datos</h4>
            <p>Suba su archivo Excel o CSV con comentarios de clientes. 
            La aplicación acepta archivos hasta 1.5MB con máximo 200 comentarios.</p>
        </div>
        """),
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        ui.glass_container("""
        <div style="text-align: center; padding: 1rem;">
            <h4 style="color: var(--secondary-cyan); margin-bottom: 1rem;">Paso 2: Analizar</h4>
            <p>Elija entre Análisis Rápido (resultados inmediatos) o 
            Análisis con IA (insights avanzados y recomendaciones estratégicas).</p>
        </div>
        """),
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        ui.glass_container("""
        <div style="text-align: center; padding: 1rem;">
            <h4 style="color: var(--accent-amber); margin-bottom: 1rem;">Paso 3: Resultados</h4>
            <p>Obtenga reportes profesionales con gráficos, métricas ejecutivas 
            y recomendaciones. Descargue todo en Excel.</p>
        </div>
        """),
        unsafe_allow_html=True
    )

# Section divider
st.markdown(ui.section_divider(), unsafe_allow_html=True)

# What you can analyze section
st.markdown("## ¿Qué Puede Analizar?")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Tipos de Datos Soportados")
    st.markdown("""
    **Formatos de Archivo:**
    - Archivos Excel (.xlsx, .xls)
    - Archivos CSV (.csv)
    
    **Contenido Requerido:**
    - Una columna con comentarios de clientes
    - Opcionalmente: calificaciones NPS, notas numéricas
    
    **Ejemplos de Comentarios:**
    - "El servicio de internet es muy lento"
    - "Excelente atención al cliente, muy satisfecho"
    - "Los precios son muy altos para el servicio"
    """)

with col2:
    st.markdown("### Resultados que Obtendrá")
    st.markdown("""
    **Análisis Automático:**
    - Distribución de sentimientos (Positivo/Neutral/Negativo)
    - Temas principales mencionados
    - Métricas de satisfacción del cliente
    
    **Con Inteligencia Artificial:**
    - Análisis emocional detallado
    - Recomendaciones estratégicas específicas
    - Áreas prioritarias de mejora
    - Índice de satisfacción avanzado
    
    **Reportes Profesionales:**
    - Gráficos ejecutivos listos para presentar
    - Exportación a Excel con múltiples hojas
    - Resumen ejecutivo con insights clave
    """)

# Section divider
st.markdown(ui.section_divider(), unsafe_allow_html=True)

# Quick start section
st.markdown("## Inicio Rápido")

st.markdown("""
### Para Comenzar Inmediatamente:

**1. Prepare su Archivo**
   - Abra Excel o Google Sheets
   - Asegúrese de tener una columna con comentarios de clientes
   - Guarde como archivo Excel (.xlsx) o CSV
   - Verifique que el archivo sea menor a 1.5MB

**2. Use la Aplicación**
   - Vaya a la sección "Subir" en el menú lateral
   - Seleccione su archivo y verifique la vista previa
   - Haga clic en "Procesar Archivo"
   - Elija "Análisis Rápido" para resultados inmediatos

**3. Analice los Resultados**
   - Revise el resumen ejecutivo con métricas clave
   - Explore los gráficos de distribución de sentimientos
   - Descargue el reporte completo en Excel
   - Use las recomendaciones para mejorar su servicio
""")

# Section divider
st.markdown(ui.section_divider(), unsafe_allow_html=True)

# Benefits section
st.markdown("## Beneficios Principales")

benefits_col1, benefits_col2 = st.columns(2)

with benefits_col1:
    st.markdown(
        ui.status_badge("", "Ahorro de Tiempo", "positive"),
        unsafe_allow_html=True
    )
    st.markdown("Analice cientos de comentarios en minutos en lugar de horas")
    
    st.markdown(
        ui.status_badge("", "Insights Profesionales", "positive"),
        unsafe_allow_html=True
    )
    st.markdown("Obtenga análisis que normalmente requieren expertos en datos")

with benefits_col2:
    st.markdown(
        ui.status_badge("", "Reportes Ejecutivos", "positive"),
        unsafe_allow_html=True
    )
    st.markdown("Genere presentaciones profesionales automáticamente")
    
    st.markdown(
        ui.status_badge("", "Recomendaciones IA", "positive"),
        unsafe_allow_html=True
    )
    st.markdown("Reciba sugerencias estratégicas basadas en inteligencia artificial")

# Section divider
st.markdown(ui.section_divider(), unsafe_allow_html=True)

# Example use cases
st.markdown("## Casos de Uso Típicos")

with st.expander("Telecomunicaciones y Servicios", expanded=False):
    st.markdown("""
    **Ideal para analizar:**
    - Comentarios sobre calidad de internet
    - Feedback de atención al cliente
    - Quejas sobre precios y servicios
    - Sugerencias de mejora de clientes
    
    **Resultados típicos:**
    - Identificación de problemas de velocidad en zonas específicas
    - Análisis de satisfacción con atención al cliente
    - Evaluación de percepción de precios
    - Recomendaciones para mejorar servicios
    """)

with st.expander("Retail y Comercio", expanded=False):
    st.markdown("""
    **Ideal para analizar:**
    - Reviews de productos
    - Comentarios de experiencia de compra
    - Feedback sobre servicio al cliente
    - Sugerencias sobre productos
    
    **Resultados típicos:**
    - Productos más valorados y criticados
    - Aspectos de servicio a mejorar
    - Tendencias en preferencias de clientes
    - Oportunidades de nuevos productos
    """)

with st.expander("Servicios Profesionales", expanded=False):
    st.markdown("""
    **Ideal para analizar:**
    - Evaluaciones de servicios profesionales
    - Feedback de consultoría
    - Comentarios sobre procesos
    - Testimonios de clientes
    
    **Resultados típicos:**
    - Fortalezas del servicio profesional
    - Áreas de mejora en procesos
    - Nivel de satisfacción general
    - Recomendaciones para crecimiento
    """)

# Section divider
st.markdown(ui.section_divider(), unsafe_allow_html=True)

# Getting started call to action
st.markdown("## ¿Listo para Comenzar?")

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    if st.button("Comenzar Análisis", type="primary", width='stretch', key="start_analysis"):
        st.switch_page("pages/2_Subir.py")

st.markdown("""
<div style="text-align: center; margin-top: 2rem; color: var(--text-tertiary);">
<p><strong>¿Necesita ayuda?</strong> Cada paso tiene instrucciones claras y la aplicación le guiará durante todo el proceso.</p>
</div>
""", unsafe_allow_html=True)

# Section divider
st.markdown(ui.section_divider(), unsafe_allow_html=True)

# Technical information (optional expandable)
with st.expander("Información Técnica (Opcional)", expanded=False):
    st.markdown("""
    ### Especificaciones Técnicas
    
    **Límites de Archivo:**
    - Tamaño máximo: 1.5MB (optimizado para Streamlit Cloud)
    - Comentarios máximos: 200 por análisis
    - Formatos: Excel (.xlsx, .xls), CSV (.csv)
    
    **Análisis Disponibles:**
    - **Análisis Rápido**: Procesamiento local con reglas predefinidas
    - **Análisis con IA**: Procesamiento con OpenAI GPT para insights avanzados
    
    **Seguridad y Privacidad:**
    - Sus datos se procesan de forma segura
    - No se almacenan comentarios después del análisis
    - Cumple con estándares de privacidad de datos
    
    **Compatibilidad:**
    - Funciona en cualquier navegador moderno
    - Optimizado para dispositivos móviles
    - Interfaz responsive para tablets y escritorio
    """)

# Footer
st.markdown(
    ui.gradient_footer(
        primary_text="Página Principal | Analizador de Comentarios",
        secondary_text="Plataforma Profesional para Análisis de Feedback"
    ),
    unsafe_allow_html=True
)