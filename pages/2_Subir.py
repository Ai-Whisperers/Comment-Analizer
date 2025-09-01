"""
Upload Page - Simplified architecture with modern styling preserved
Clean button implementation without deep nesting
"""

import sys
import streamlit as st
from pathlib import Path

# Add shared modules to path
current_dir = Path(__file__).parent.parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from shared.styling.theme_manager_full import ThemeManager, UIComponents
from shared.business.file_processor import FileProcessor
import pandas as pd
import plotly.express as px
from datetime import datetime
from io import BytesIO

# Import memory monitoring functions
try:
    from shared.utils.memory_monitor import get_memory_status, optimize_memory, format_memory_display
    MEMORY_MONITORING_AVAILABLE = True
except ImportError:
    MEMORY_MONITORING_AVAILABLE = False

# Initialize styling and components (PRESERVE MODERN UX)
if 'theme_manager' not in st.session_state:
    st.session_state.theme_manager = ThemeManager()
    st.session_state.ui = UIComponents()

theme = st.session_state.theme_manager
ui = st.session_state.ui

# Apply modular glassmorphism Web3 styling (proper separation of concerns)
from shared.styling.modular_css import initialize_modular_styles
initialize_modular_styles(dark_mode=st.session_state.get('dark_mode', True))

# Modern animated header (PRESERVED SOPHISTICATION)
st.markdown(
    ui.animated_header(
        title="Análisis de Comentarios",
        subtitle="Personal Paraguay | Cargar Archivo"
    ),
    unsafe_allow_html=True
)

# Floating particles effect (PRESERVED)
st.markdown(ui.floating_particles(), unsafe_allow_html=True)

# SIMPLE BUTTON ARCHITECTURE (FIX FOR RELIABILITY)
st.markdown("### Cargar Archivo")

# File upload with modern styling
uploaded_file = st.file_uploader(
    "Cargar archivo Excel o CSV",
    type=['xlsx', 'xls', 'csv'],
    help="Sube un archivo Excel (.xlsx, .xls) o CSV con comentarios de clientes"
)

# ENHANCED FILE UPLOAD WITH PREVIEW
if uploaded_file:
    # File validation display
    processor = FileProcessor()
    validation = processor.validate_file(uploaded_file)
    
    if validation['valid']:
        st.success(f"Archivo válido: {uploaded_file.name} ({validation['file_size_mb']:.1f}MB)")
        
        # Enhanced file preview with statistics
        try:
            import pandas as pd
            import io
            
            # Read file for preview
            if uploaded_file.name.endswith('.csv'):
                df_preview = pd.read_csv(uploaded_file, nrows=5)
                df_full = pd.read_csv(uploaded_file)
            else:
                df_preview = pd.read_excel(uploaded_file, nrows=5)
                df_full = pd.read_excel(uploaded_file)
            
            # Display file preview header with stats
            st.markdown(
                ui.file_preview_header(
                    filename=uploaded_file.name,
                    filesize=f"{validation['file_size_mb']:.1f}MB",
                    rows=len(df_full),
                    columns=len(df_full.columns)
                ),
                unsafe_allow_html=True
            )
            
            # Show data preview
            with st.expander("Vista previa de datos (primeras 5 filas)", expanded=True):
                st.dataframe(df_preview, use_container_width=True)
                
                # Column analysis
                col_info = []
                for col in df_full.columns:
                    col_type = "Comentarios" if any(keyword in col.lower() for keyword in ['comment', 'comentario', 'feedback']) else "Numérica" if df_full[col].dtype in ['int64', 'float64'] else "Texto"
                    col_info.append(f"**{col}**: {col_type}")
                
                st.info("**Columnas detectadas:** " + " | ".join(col_info))
            
        except Exception as e:
            st.warning(f"No se pudo generar vista previa: {str(e)}")
        
        # INTELLIGENT ANALYSIS SECTION (IA Primary)
        st.markdown("### Análisis Inteligente")
        
        # Check API key availability
        import os
        api_key_available = bool(os.getenv('OPENAI_API_KEY'))
        
        if api_key_available:
            # AI Analysis as primary option
            if st.button("Iniciar Análisis con IA", type="primary", use_container_width=True, key="ai_analysis"):
                # Enhanced AI progress feedback
                ai_steps = ["Preparando IA", "Análisis inteligente", "Extrayendo insights", "Generando recomendaciones"]
                ai_progress_placeholder = st.empty()
                
                with st.spinner("Procesando con inteligencia artificial..."):
                    try:
                        from shared.business.file_processor import FileProcessor
                        processor = FileProcessor()
                        
                        # AI processing steps with detailed feedback
                        for i, step in enumerate(ai_steps):
                            ai_progress_placeholder.markdown(
                                ui.step_progress_indicator(ai_steps, i),
                                unsafe_allow_html=True
                            )
                        
                        # Process file using AI-enhanced business logic
                        results = processor.process_uploaded_file(uploaded_file, use_ai_insights=True)
                        
                        if results:
                            st.session_state.analysis_results = results
                            st.session_state.analysis_type = "ai"
                            ai_progress_placeholder.empty()
                            st.success("Análisis IA completado con insights avanzados!")
                            st.rerun()
                        else:
                            ai_progress_placeholder.empty()
                            st.error("Error procesando archivo con IA")
                            
                    except Exception as e:
                        ai_progress_placeholder.empty()
                        st.error(f"Error durante análisis IA: {str(e)}")
        else:
            # Fallback to quick analysis if no API key
            st.warning("API key no disponible - usando análisis rápido como alternativa")
            
            if st.button("Análisis Rápido (Fallback)", type="secondary", use_container_width=True, key="fallback_analysis"):
                progress_steps = ["Validando archivo", "Extrayendo comentarios", "Análisis básico", "Generando reportes"]
                progress_placeholder = st.empty()
                
                with st.spinner("Procesando comentarios (modo básico)..."):
                    try:
                        from shared.business.file_processor import FileProcessor
                        processor = FileProcessor()
                        
                        # Basic processing steps
                        for i, step in enumerate(progress_steps):
                            progress_placeholder.markdown(
                                ui.step_progress_indicator(progress_steps, i),
                                unsafe_allow_html=True
                            )
                        
                        # Process file using basic logic
                        results = processor.process_uploaded_file(uploaded_file, use_ai_insights=False)
                        
                        if results:
                            st.session_state.analysis_results = results
                            st.session_state.analysis_type = "quick"
                            progress_placeholder.empty()
                            st.info("Análisis básico completado. Para insights avanzados, configure API key.")
                            st.rerun()
                        else:
                            progress_placeholder.empty()
                            st.error("Error procesando archivo")
                            
                    except Exception as e:
                        progress_placeholder.empty()
                        st.error(f"Error durante análisis: {str(e)}")
    else:
        st.error(f"Error: {validation['error_message']}")

# ENHANCED AI RESULTS SECTION WITH DETAILED INSIGHTS
if 'analysis_results' in st.session_state:
    st.markdown(ui.section_divider(), unsafe_allow_html=True)
    st.markdown("### Resultados del Análisis Inteligente")
    
    results = st.session_state.analysis_results
    is_ai_analysis = st.session_state.get('analysis_type') == 'ai'
    
    # Analysis method indicator
    if is_ai_analysis:
        st.markdown(
            ui.status_badge("", "Análisis con IA Completado - Insights Avanzados", "positive"),
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            ui.status_badge("", "Análisis Rápido Completado (Fallback)", "neutral"),
            unsafe_allow_html=True
        )
    
    # Executive summary with 4-column layout
    st.markdown("#### Resumen Ejecutivo")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(
            ui.status_badge("", f"{results.get('total', 0)} Comentarios", "neutral"),
            unsafe_allow_html=True
        )
    
    with col2:
        positive_pct = results.get('sentiment_percentages', {}).get('positivo', 0)
        st.markdown(
            ui.status_badge("", f"{positive_pct}% Positivos", "positive"),
            unsafe_allow_html=True
        )
    
    with col3:
        negative_pct = results.get('sentiment_percentages', {}).get('negativo', 0)
        st.markdown(
            ui.status_badge("", f"{negative_pct}% Negativos", "negative"),
            unsafe_allow_html=True
        )
    
    with col4:
        neutral_pct = results.get('sentiment_percentages', {}).get('neutral', 0)
        st.markdown(
            ui.status_badge("", f"{neutral_pct}% Neutrales", "neutral"),
            unsafe_allow_html=True
        )
    
    # AI-Enhanced Insights Section (Detailed for IA analysis)
    if is_ai_analysis:
        st.markdown(ui.section_divider(), unsafe_allow_html=True)
        st.markdown("#### Insights de Inteligencia Artificial")
        
        insights = results.get('insights', {})
        
        # AI metrics display (3-column layout)
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
            st.markdown("##### Áreas Prioritarias de Acción")
            for area in priority_areas[:4]:  # Show top 4
                area_display = area.replace('_', ' ').title().replace('Optimization', 'Optimización')
                st.info(f"• {area_display}")
        
        # Engagement Quality
        engagement_quality = insights.get('engagement_quality', 'básico')
        st.markdown(f"**Calidad de Engagement:** {engagement_quality.title()}")
        
        # Emotion Analysis Section (if available)
        if results.get('emotion_summary'):
            st.markdown("##### Análisis Emocional Detallado")
            
            emotion_summary = results['emotion_summary']
            emotion_distribution = emotion_summary.get('distribution', {})
            avg_intensity = emotion_summary.get('avg_intensity', 0)
            
            # Emotion intensity metric
            col_intensity1, col_intensity2 = st.columns(2)
            with col_intensity1:
                st.metric("Intensidad Emocional Promedio", f"{avg_intensity}/10")
            with col_intensity2:
                intensity_level = "Alta" if avg_intensity > 7 else ("Media" if avg_intensity > 4 else "Baja")
                st.markdown(
                    ui.status_badge(
                        icon="",
                        text=f"Nivel: {intensity_level}",
                        badge_type="positive" if avg_intensity > 7 else ("neutral" if avg_intensity > 4 else "negative")
                    ),
                    unsafe_allow_html=True
                )
            
            # Emotion distribution chart
            if emotion_distribution:
                chart_theme = theme.get_chart_theme(st.session_state.get('dark_mode', True))
                
                emotion_df = pd.DataFrame(list(emotion_distribution.items()), columns=['Emoción', 'Frecuencia'])
                emotion_df = emotion_df.sort_values('Frecuencia', ascending=False).head(10)  # Top 10 emotions
                
                fig_emotions = px.bar(
                    emotion_df,
                    x='Emoción',
                    y='Frecuencia', 
                    title="Distribución de Emociones Específicas (Top 10)"
                )
                fig_emotions.update_layout(chart_theme['layout'])
                st.plotly_chart(fig_emotions, use_container_width=True)
    
    # Detailed sentiment analysis charts
    if results.get('sentiment_percentages'):
        import plotly.express as px
        import pandas as pd
        
        sentiment_data = results['sentiment_percentages']
        chart_theme = theme.get_chart_theme(st.session_state.get('dark_mode', True))
        
        # Sentiment pie chart
        fig_sentiment = px.pie(
            values=list(sentiment_data.values()),
            names=list(sentiment_data.keys()),
            title="Distribución de Sentimientos"
        )
        fig_sentiment.update_layout(chart_theme['layout'])
        st.plotly_chart(fig_sentiment, use_container_width=True)
    
    # Theme analysis chart
    if results.get('theme_counts'):
        theme_data = results['theme_counts']
        theme_df = pd.DataFrame(list(theme_data.items()), columns=['Tema', 'Frecuencia'])
        theme_df = theme_df.sort_values('Frecuencia', ascending=False)
        
        chart_theme = theme.get_chart_theme(st.session_state.get('dark_mode', True))
        
        fig_themes = px.bar(
            theme_df,
            x='Tema', 
            y='Frecuencia',
            title="Temas Principales Identificados"
        )
        fig_themes.update_layout(chart_theme['layout'])
        st.plotly_chart(fig_themes, use_container_width=True)
    
    # AI Strategic Recommendations (if IA analysis)
    if is_ai_analysis:
        st.markdown("#### Recomendaciones Estratégicas IA")
        recommendations = results.get('recommendations', [])
        
        for i, rec in enumerate(recommendations, 1):
            # Highlight strategic AI recommendations
            if any(indicator in rec for indicator in ['EXCELENCIA', 'CRÍTICO', 'INTENSIDAD', 'VELOCIDAD', 'PRECIO', 'SERVICIO']):
                st.warning(f"**{i}.** {rec}")  # Strategic recommendations in warning style
            else:
                st.info(f"{i}. {rec}")
                
        # Add AI analysis explanation
        with st.expander("Acerca de las Recomendaciones IA", expanded=False):
            st.markdown("""
            **Las recomendaciones estratégicas** están generadas por inteligencia artificial basándose en:
            - Patrones detectados en los comentarios
            - Análisis contextual de sentimientos
            - Métricas de satisfacción y engagement
            - Benchmarks de la industria
            
            **Recomendaciones marcadas** requieren **acción prioritaria**.
            """)
    else:
        # Basic recommendations for fallback
        st.markdown("#### Recomendaciones Básicas")
        recommendations = results.get('recommendations', [])
        for i, rec in enumerate(recommendations, 1):
            st.info(f"{i}. {rec}")
    
    # Enhanced Excel download with AI-specific content
    from datetime import datetime
    from io import BytesIO
    
    try:
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
                ['Método de Análisis', 'IA Avanzado' if is_ai_analysis else 'Análisis Rápido']
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
            
            # AI-specific sheets for enhanced analysis
            if is_ai_analysis:
                insights = results.get('insights', {})
                priority_areas = insights.get('priority_action_areas', [])
                
                # AI Insights sheet
                ai_insights_df = pd.DataFrame([
                    ['Customer Satisfaction Index', insights.get('customer_satisfaction_index', 0)],
                    ['Emotional Intensity', insights.get('emotional_intensity', 'medio')],
                    ['Sentiment Stability', insights.get('sentiment_stability', 'balanceado')],
                    ['Engagement Quality', insights.get('engagement_quality', 'básico')],
                    ['Top Priority Area', priority_areas[0] if priority_areas else 'N/A'],
                    ['Priority Areas Count', len(priority_areas)]
                ], columns=['AI Metric', 'Value'])
                ai_insights_df.to_excel(writer, sheet_name='Insights IA', index=False)
                
                # Emotion Analysis sheet (if emotion data is available)
                if results.get('emotion_summary'):
                    emotion_summary = results['emotion_summary']
                    emotion_distribution = emotion_summary.get('distribution', {})
                    avg_intensity = emotion_summary.get('avg_intensity', 0)
                    
                    if emotion_distribution:
                        emotion_data = []
                        for emotion, count in emotion_distribution.items():
                            emotion_data.append([emotion.title(), count])
                        
                        emotion_df = pd.DataFrame(emotion_data, columns=['Emoción', 'Frecuencia'])
                        emotion_df = emotion_df.sort_values('Frecuencia', ascending=False)
                        
                        # Add summary row
                        summary_row = pd.DataFrame([
                            ['--- RESUMEN EMOCIONAL ---', ''],
                            ['Total Emociones Detectadas', len(emotion_distribution)],
                            ['Intensidad Promedio (/10)', avg_intensity],
                            ['Emoción Dominante', emotion_df.iloc[0]['Emoción'] if len(emotion_df) > 0 else 'N/A']
                        ], columns=['Emoción', 'Frecuencia'])
                        
                        final_emotion_df = pd.concat([emotion_df, summary_row], ignore_index=True)
                        final_emotion_df.to_excel(writer, sheet_name='Emociones Detalladas', index=False)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        analysis_type = "IA" if is_ai_analysis else "rapido"
        filename = f"analisis_comentarios_{analysis_type}_{timestamp}.xlsx"
        
        # Enhanced download button with analysis type
        emotion_sheets = " + Emociones" if (is_ai_analysis and results.get('emotion_summary')) else ""
        sheet_count = "4 hojas" if (is_ai_analysis and results.get('emotion_summary')) else ("3 hojas" if is_ai_analysis else "2 hojas")
        download_label = f"Descargar Reporte IA ({sheet_count}){emotion_sheets}" if is_ai_analysis else "Descargar Reporte Básico (2 hojas)"
        
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
    
    # Reset button for new analysis
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Nuevo Análisis", key="new_analysis", type="secondary", use_container_width=True):
            # Clear analysis results
            for key in ['analysis_results', 'analysis_type', 'uploaded_file']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    
    with col2:
        if st.button("Limpiar Memoria", key="cleanup_memory_results", type="secondary", use_container_width=True):
            # Memory optimization after analysis
            if MEMORY_MONITORING_AVAILABLE:
                if optimize_memory():
                    st.success("Memoria limpiada")
                    st.rerun()
                else:
                    st.error("Error limpiando memoria")

# Modern section divider (PRESERVED)
st.markdown(ui.section_divider(), unsafe_allow_html=True)

# File requirements with modern styling
st.markdown("### Requisitos del Archivo")

with st.expander("Información de formato", expanded=False):
    st.markdown("""
    **Formatos soportados:**
    - Excel (.xlsx, .xls)
    - CSV (.csv)
    
    **Límites para Streamlit Cloud:**
    - Tamaño máximo: 1.5MB
    - Comentarios máximos: 200
    
    **Columnas requeridas:**
    - Una columna con comentarios (puede llamarse: comentario, comment, feedback, etc.)
    - Columnas opcionales: NPS, Nota
    """)

# Modern gradient footer (PRESERVED)
st.markdown(
    ui.gradient_footer(
        primary_text="Cargar Archivo | Analizador de Comentarios",
        secondary_text="Impulsado por Análisis Avanzados"
    ),
    unsafe_allow_html=True
)

# Memory monitoring in sidebar (PRESERVED FUNCTIONALITY)
with st.sidebar:
    st.markdown("### Estado del Sistema")
    
    try:
        if MEMORY_MONITORING_AVAILABLE:
            memory_status = get_memory_status()
            
            if memory_status['available']:
                label, value, delta = format_memory_display(memory_status)
                
                st.metric(label, value, delta)
                
                # Show recommendation for high memory usage
                if memory_status['status'] != 'Normal':
                    st.warning(memory_status['recommendation'])
                    
                    # Memory cleanup button for high usage
                    if memory_status['status'] == 'Alto':
                        if st.button("Limpiar Memoria", key="memory_cleanup_upload", type="secondary"):
                            if optimize_memory():
                                st.success("Memoria optimizada")
                                st.rerun()
                            else:
                                st.error("Error en optimización")
                
                # Environment info
                st.caption(f"Entorno: {memory_status['environment']}")
            else:
                st.info(memory_status['error'])
        else:
            st.info("Monitoreo de memoria no disponible")
    except Exception as e:
        st.info(f"Error en monitoreo: {str(e)}")
    
    # Navigation
    st.markdown("---")
    st.markdown("### Navegación")
    if st.button("Ver Resultados", disabled=('analysis_results' not in st.session_state)):
        st.switch_page("pages/results.py")