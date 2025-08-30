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

# AI analysis detection
is_ai_analysis = results.get('ai_insights_enabled', False)
analysis_method = results.get('analysis_method', 'RULE_BASED_SIMPLE')

# Analysis method indicator  
if is_ai_analysis:
    st.markdown(
        ui.status_badge(
            icon="",
            text="Análisis con IA Completado",
            badge_type="positive"
        ),
        unsafe_allow_html=True
    )
else:
    st.markdown(
        ui.status_badge(
            icon="",
            text="Análisis Rápido Completado", 
            badge_type="neutral"
        ),
        unsafe_allow_html=True
    )

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

# AI-Enhanced Insights Section (NEW)
if is_ai_analysis:
    st.markdown(ui.section_divider(), unsafe_allow_html=True)
    st.markdown("### Insights de Inteligencia Artificial")
    
    insights = results.get('insights', {})
    
    # AI metrics display
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Customer Satisfaction Index
        satisfaction_index = insights.get('customer_satisfaction_index', 0)
        satisfaction_level = "Alto" if satisfaction_index > 70 else ("Medio" if satisfaction_index > 40 else "Bajo")
        st.metric(
            "Índice de Satisfacción", 
            f"{satisfaction_index}/100",
            delta=satisfaction_level
        )
    
    with col2:
        # Emotional Intensity  
        emotional_intensity = insights.get('emotional_intensity', 'medio')
        intensity_badge_type = "positive" if emotional_intensity in ['alto', 'muy_alto'] else "neutral"
        st.markdown(
            ui.status_badge(
                icon="",
                text=f"Intensidad: {emotional_intensity.title()}",
                badge_type=intensity_badge_type
            ),
            unsafe_allow_html=True
        )
    
    with col3:
        # Sentiment Stability
        sentiment_stability = insights.get('sentiment_stability', 'balanceado')
        stability_badge_type = "positive" if sentiment_stability == 'muy_balanceado' else ("negative" if 'polarizado' in sentiment_stability else "neutral")
        st.markdown(
            ui.status_badge(
                icon="",
                text=f"Estabilidad: {sentiment_stability.replace('_', ' ').title()}",
                badge_type=stability_badge_type
            ),
            unsafe_allow_html=True
        )
    
    # Priority Action Areas
    priority_areas = insights.get('priority_action_areas', [])
    if priority_areas:
        st.markdown("#### Áreas Prioritarias de Acción")
        for area in priority_areas[:4]:  # Show top 4
            area_display = area.replace('_', ' ').title().replace('Optimization', 'Optimización')
            st.info(f"• {area_display}")
    
    # Engagement Quality
    engagement_quality = insights.get('engagement_quality', 'básico')
    st.markdown(f"**Calidad de Engagement:** {engagement_quality.title()}")

# Modern section divider (PRESERVED)
st.markdown(ui.section_divider(), unsafe_allow_html=True)

# Detailed results with sophisticated visualization
st.markdown("### Análisis Detallado")

# Create charts (preserve sophisticated visualization)
import plotly.express as px

# Sentiment distribution pie chart with theme integration
if results.get('sentiment_percentages'):
    sentiment_data = results['sentiment_percentages']
    
    # Apply glassmorphism theme to chart
    chart_theme = theme.get_chart_theme(st.session_state.get('dark_mode', True))
    
    fig_sentiment = px.pie(
        values=list(sentiment_data.values()),
        names=list(sentiment_data.keys()),
        title="Distribución de Sentimientos"
    )
    fig_sentiment.update_layout(chart_theme['layout'])
    st.plotly_chart(fig_sentiment, use_container_width=True)

# Theme analysis with glassmorphism integration
if results.get('theme_counts'):
    theme_data = results['theme_counts']
    theme_df = pd.DataFrame(list(theme_data.items()), columns=['Tema', 'Frecuencia'])
    
    # Apply glassmorphism theme to chart
    chart_theme = theme.get_chart_theme(st.session_state.get('dark_mode', True))
    
    fig_themes = px.bar(
        theme_df,
        x='Tema', 
        y='Frecuencia',
        title="Temas Principales"
    )
    fig_themes.update_layout(chart_theme['layout'])
    st.plotly_chart(fig_themes, use_container_width=True)

# Enhanced recommendations with AI differentiation
if is_ai_analysis:
    st.markdown("### Recomendaciones Estratégicas IA")
    recommendations = results.get('recommendations', [])
    
    for i, rec in enumerate(recommendations, 1):
        # Highlight strategic AI recommendations
        if any(indicator in rec for indicator in ['EXCELENCIA', 'CRÍTICO', 'INTENSIDAD', 'VELOCIDAD', 'PRECIO', 'SERVICIO']):
            st.warning(f"**{i}.** {rec}")  # Strategic recommendations in warning style
        else:
            st.info(f"{i}. {rec}")
            
    # Add AI analysis explanation
    with st.expander("ℹ️ Acerca de las Recomendaciones IA", expanded=False):
        st.markdown("""
        **Las recomendaciones estratégicas** están generadas por inteligencia artificial basándose en:
        - Patrones detectados en los comentarios
        - Análisis contextual de sentimientos
        - Métricas de satisfacción y engagement
        - Benchmarks de la industria de telecomunicaciones
        
        **Recomendaciones marcadas** requieren **acción prioritaria**.
        """)
else:
    st.markdown("### Recomendaciones")
    recommendations = results.get('recommendations', [])
    for i, rec in enumerate(recommendations, 1):
        st.info(f"{i}. {rec}")

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
        
        # Summary sheet with AI enhancement
        summary_data = [
            ['Total Comentarios', results.get('total', 0)],
            ['Positivos %', results.get('sentiment_percentages', {}).get('positivo', 0)],
            ['Negativos %', results.get('sentiment_percentages', {}).get('negativo', 0)],
            ['Neutrales %', results.get('sentiment_percentages', {}).get('neutral', 0)],
            ['Método de Análisis', results.get('analysis_method', 'RULE_BASED_SIMPLE')]
        ]
        
        # Add AI-specific metrics if available
        if is_ai_analysis:
            insights = results.get('insights', {})
            summary_data.extend([
                ['--- MÉTRICAS IA AVANZADAS ---', ''],
                ['Índice de Satisfacción (/100)', insights.get('customer_satisfaction_index', 0)],
                ['Intensidad Emocional', insights.get('emotional_intensity', 'medio')],
                ['Estabilidad de Sentimientos', insights.get('sentiment_stability', 'balanceado')],
                ['Calidad de Engagement', insights.get('engagement_quality', 'básico')]
            ])
        
        summary_df = pd.DataFrame(summary_data, columns=['Métrica', 'Valor'])
        summary_df.to_excel(writer, sheet_name='Resumen', index=False)
        
        # AI-specific sheet for enhanced analysis
        if is_ai_analysis:
            insights = results.get('insights', {})
            priority_areas = insights.get('priority_action_areas', [])
            
            ai_insights_df = pd.DataFrame([
                ['Customer Satisfaction Index', insights.get('customer_satisfaction_index', 0)],
                ['Emotional Intensity', insights.get('emotional_intensity', 'medio')],
                ['Sentiment Stability', insights.get('sentiment_stability', 'balanceado')],
                ['Engagement Quality', insights.get('engagement_quality', 'básico')],
                ['Top Priority Area', priority_areas[0] if priority_areas else 'N/A'],
                ['Priority Areas Count', len(priority_areas)]
            ], columns=['AI Metric', 'Value'])
            ai_insights_df.to_excel(writer, sheet_name='Insights IA', index=False)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    analysis_type = "IA" if is_ai_analysis else "rapido"
    filename = f"analisis_comentarios_{analysis_type}_{timestamp}.xlsx"
    
    # Enhanced download button with analysis type
    download_label = "📊 Descargar Reporte IA (3 hojas)" if is_ai_analysis else "📊 Descargar Reporte Básico (2 hojas)"
    
    st.download_button(
        label=download_label,
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