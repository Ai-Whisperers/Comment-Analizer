"""
Página Principal - Clean Architecture
Simple landing page usando solo src/
"""

import streamlit as st
import sys
from pathlib import Path

# Add src to path
current_dir = Path(__file__).parent.parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

# Load enhanced CSS for glassmorphism effects
try:
    from src.presentation.streamlit.enhanced_css_loader import ensure_css_loaded, inject_page_css
    ensure_css_loaded()
    inject_page_css('main')  # Add main page specific styles
    CSS_LOADED = True
except ImportError:
    # CSS will be loaded from main app
    CSS_LOADED = False

# Page content with styling support
st.title("Personal Paraguay - Análisis de Comentarios")

st.markdown("""
## Plataforma de Análisis con Inteligencia Artificial

Esta aplicación utiliza **Inteligencia Artificial avanzada** para analizar comentarios de clientes:
- **GPT-4 de OpenAI** para análisis comprehensivo
- **Análisis emocional granular** con intensidades
- **Detección automática de temas** y puntos de dolor
- **Clean Architecture** con principios SOLID
""")

# System status
st.markdown("---")
st.markdown("### Estado del Sistema")

# Check sistema IA puro status
if 'caso_uso_maestro' in st.session_state and st.session_state.caso_uso_maestro:
    st.success("✅ Sistema IA Maestro: Activo y Funcional")
    
    # IA system metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Estado IA", "🤖 GPT-4 Listo")
    
    with col2:
        # Check if we have analysis results in memory
        total_analizados = 0
        if 'analysis_results' in st.session_state:
            resultado = st.session_state.analysis_results
            if hasattr(resultado, 'total_comentarios'):
                total_analizados = resultado.total_comentarios
        st.metric("Comentarios Analizados", total_analizados)
    
    with col3:
        st.metric("Versión", "3.0.0 IA-Pure")
        
    # Show IA capabilities
    if st.session_state.get('app_info'):
        info = st.session_state.app_info
        if info.get('configuracion_actual', {}).get('openai_configurado'):
            st.info("🧠 Sistema configurado para análisis IA avanzado con GPT-4")
        
elif 'contenedor' in st.session_state:
    st.warning("⚠️ Sistema IA en inicialización...")
    st.info("Verificando configuración de OpenAI...")
else:
    st.error("❌ Sistema IA no inicializado")
    st.error("Recarga la página o verifica configuración de API key")

# Instructions
st.markdown("---")
st.markdown("### ¿Cómo usar?")

st.markdown("""
1. **Ve a la página 'Subir'** usando la barra lateral
2. **Carga tu archivo** Excel (.xlsx, .xls) o CSV con comentarios
3. **Presiona 'Analizar con Inteligencia Artificial'** 
4. **La IA procesará** todos los comentarios en una sola llamada
5. **Revisa los insights** generados automáticamente
6. **Exporta el reporte** completo a Excel
""")

# Technical details
with st.expander("Detalles Técnicos"):
    st.markdown("""
    **Arquitectura:** Clean Architecture + SOLID + Domain-Driven Design  
    **Capas:** Domain → Application → Infrastructure  
    **Análisis:** Hybrid (IA + Rules)  
    **Idiomas:** Español, Guaraní, Inglés  
    **Formatos:** Excel, CSV  
    **Exportación:** Excel, Resumen texto
    """)

st.markdown("---")
st.markdown("*Powered by Clean Architecture | Personal Paraguay 2024*")