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

# Page content
st.title("Personal Paraguay - Análisis de Comentarios")

st.markdown("""
## Bienvenido a la Plataforma de Análisis

Esta aplicación utiliza **Clean Architecture** para analizar comentarios de clientes con:
- **Análisis con IA** usando OpenAI GPT-4
- **Análisis por Reglas** como respaldo robusto
- **Arquitectura Limpia** con principios SOLID
""")

# System status
st.markdown("---")
st.markdown("### Estado del Sistema")

if 'analizador_app' in st.session_state:
    try:
        info = st.session_state.analizador_app.obtener_info_sistema()
        st.success(f"Sistema activo: {info.get('version', 'v2.0.0')}")
        
        stats = st.session_state.analizador_app.obtener_estadisticas_repositorio()
        config_stats = stats.get('configuracion', {})
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("OpenAI", "Configurado" if config_stats.get('openai_configurado') else "Sin configurar")
        
        with col2:
            st.metric("Comentarios", stats.get('total', 0))
            
    except Exception as e:
        st.error(f"Error obteniendo estado: {str(e)}")
else:
    st.warning("Sistema no inicializado")

# Instructions
st.markdown("---")
st.markdown("### ¿Cómo usar?")

st.markdown("""
1. **Ve a la página 'Subir'** usando la barra lateral
2. **Carga tu archivo** Excel (.xlsx, .xls) o CSV
3. **Elige el tipo de análisis:**
   - **Con IA**: Análisis avanzado con GPT-4
   - **Con Reglas**: Análisis robusto sin conexión
4. **Revisa los resultados** y exporta si necesitas
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