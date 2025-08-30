"""
Results Page - Sophisticated results display with modern styling preserved
Professional visualization without architectural complexity
"""

import sys
from pathlib import Path
from datetime import datetime
from io import BytesIO

# Add shared modules to path
current_dir = Path(__file__).parent.parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

import streamlit as st
import pandas as pd
from shared.styling.theme_manager_full import ThemeManager, UIComponents

# Initialize styling (PRESERVE MODERN UX)
if 'theme_manager' not in st.session_state:
    st.session_state.theme_manager = ThemeManager()
    st.session_state.ui = UIComponents()

theme = st.session_state.theme_manager
ui = st.session_state.ui

# Apply sophisticated styling (EXACT SAME AS ORIGINAL)
dark_theme = theme.get_theme(st.session_state.get('dark_mode', True))
st.markdown(f"<style>{theme.generate_css_variables(dark_theme)}</style>", unsafe_allow_html=True)
st.markdown(f"<style>{theme.generate_base_styles(dark_theme)}</style>", unsafe_allow_html=True)
st.markdown(f"<style>{theme.generate_animations()}</style>", unsafe_allow_html=True)

# Modern header (PRESERVED SOPHISTICATION)
st.markdown(
    ui.animated_header(
        title="Resultados del Análisis",
        subtitle="Personal Paraguay | Análisis Avanzado"
    ),
    unsafe_allow_html=True
)

# Check if results exist
if 'analysis_results' not in st.session_state:
    st.error("No hay resultados disponibles. Por favor, realiza un análisis primero.")
    if st.button("Ir a Cargar Archivo", key="goto_upload"):
        st.switch_page("pages/upload.py")
    st.stop()

results = st.session_state.analysis_results

# SOPHISTICATED RESULTS DISPLAY (PRESERVED FROM ORIGINAL)
st.markdown("### Resumen Ejecutivo")

# Modern metrics display with glass effects
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        ui.status_badge(
            icon="",
            text=f"{results.get('total', 0)} Comentarios",
            badge_type="neutral"
        ),
        unsafe_allow_html=True
    )

with col2:
    positive_pct = results.get('sentiment_percentages', {}).get('positivo', 0)
    st.markdown(
        ui.status_badge(
            icon="", 
            text=f"{positive_pct}% Positivos",
            badge_type="positive"
        ),
        unsafe_allow_html=True
    )

with col3:
    negative_pct = results.get('sentiment_percentages', {}).get('negativo', 0)
    st.markdown(
        ui.status_badge(
            icon="",
            text=f"{negative_pct}% Negativos", 
            badge_type="negative"
        ),
        unsafe_allow_html=True
    )

with col4:
    neutral_pct = results.get('sentiment_percentages', {}).get('neutral', 0)
    st.markdown(
        ui.status_badge(
            icon="",
            text=f"{neutral_pct}% Neutrales",
            badge_type="neutral"
        ),
        unsafe_allow_html=True
    )

# Modern section divider (PRESERVED)
st.markdown(ui.section_divider(), unsafe_allow_html=True)

# Detailed results with sophisticated visualization
st.markdown("### Análisis Detallado")

# Create charts (preserve sophisticated visualization)
import plotly.express as px

# Sentiment distribution pie chart
if results.get('sentiment_percentages'):
    sentiment_data = results['sentiment_percentages']
    fig_sentiment = px.pie(
        values=list(sentiment_data.values()),
        names=list(sentiment_data.keys()),
        title="Distribución de Sentimientos"
    )
    st.plotly_chart(fig_sentiment, use_container_width=True)

# Theme analysis
if results.get('theme_counts'):
    theme_data = results['theme_counts']
    theme_df = pd.DataFrame(list(theme_data.items()), columns=['Tema', 'Frecuencia'])
    
    fig_themes = px.bar(
        theme_df,
        x='Tema', 
        y='Frecuencia',
        title="Temas Principales"
    )
    st.plotly_chart(fig_themes, use_container_width=True)

# Recommendations with modern styling
st.markdown("### Recomendaciones")

recommendations = results.get('recommendations', [])
for i, rec in enumerate(recommendations, 1):
    st.info(f"{i}. {rec}")  # Use simple Streamlit info instead of non-existent alert_banner

# SIMPLE DOWNLOAD SECTION (NO COMPLEX NESTING)
st.markdown("### Descargar Resultados")

# Generate Excel report (preserve functionality)
try:
    # Simple Excel generation
    output = BytesIO()
    
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        # Results sheet
        results_df = pd.DataFrame({
            'Comentario': results.get('comments', []),
            'Sentimiento': results.get('sentiments', [])
        })
        results_df.to_excel(writer, sheet_name='Resultados', index=False)
        
        # Summary sheet
        summary_df = pd.DataFrame([
            ['Total Comentarios', results.get('total', 0)],
            ['Positivos %', results.get('sentiment_percentages', {}).get('positivo', 0)],
            ['Negativos %', results.get('sentiment_percentages', {}).get('negativo', 0)],
            ['Neutrales %', results.get('sentiment_percentages', {}).get('neutral', 0)]
        ], columns=['Métrica', 'Valor'])
        summary_df.to_excel(writer, sheet_name='Resumen', index=False)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"analisis_comentarios_{timestamp}.xlsx"
    
    # SIMPLE DOWNLOAD BUTTON (NO NESTING)
    st.download_button(
        label="Descargar Reporte Excel",
        data=output.getvalue(),
        file_name=filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
        key="download_excel"
    )
    
except Exception as e:
    st.error(f"Error generando Excel: {e}")

# SIMPLE NAVIGATION (NO COMPLEX STRUCTURE)
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Nueva Carga", key="new_upload_from_results"):
        # Clear results and go to upload
        if 'analysis_results' in st.session_state:
            del st.session_state.analysis_results
        if 'uploaded_file' in st.session_state:
            del st.session_state.uploaded_file
        st.switch_page("pages/upload.py")

with col2:
    if st.button("Procesar Nuevo", key="reprocess"):
        st.switch_page("pages/analyze.py")

with col3:
    if st.button("Limpiar Memoria", key="cleanup_memory"):
        # Simple cleanup without complex nesting
        if 'analysis_results' in st.session_state:
            del st.session_state.analysis_results
        st.success("Memoria limpiada")
        st.rerun()

# Modern footer (PRESERVED)
st.markdown(
    ui.gradient_footer(
        primary_text="Panel de Resultados | Analizador de Comentarios",
        secondary_text="Plataforma de Análisis Profesional"
    ),
    unsafe_allow_html=True
)