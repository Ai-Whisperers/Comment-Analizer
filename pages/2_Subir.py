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
        
        # INTEGRATED ANALYSIS SECTION
        st.markdown("### Opciones de Análisis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Quick Analysis Button
            if st.button("Análisis Rápido", type="primary", use_container_width=True, key="quick_analysis"):
                # Enhanced progress feedback
                progress_steps = ["Validando archivo", "Extrayendo comentarios", "Análisis de sentimientos", "Generando reportes"]
                progress_placeholder = st.empty()
                
                with st.spinner("Procesando comentarios..."):
                    try:
                        from shared.business.file_processor import FileProcessor
                        processor = FileProcessor()
                        
                        # Step 1: Validating file
                        progress_placeholder.markdown(
                            ui.step_progress_indicator(progress_steps, 0),
                            unsafe_allow_html=True
                        )
                        
                        # Step 2: Extracting comments
                        progress_placeholder.markdown(
                            ui.step_progress_indicator(progress_steps, 1),
                            unsafe_allow_html=True
                        )
                        
                        # Step 3: Processing
                        progress_placeholder.markdown(
                            ui.step_progress_indicator(progress_steps, 2),
                            unsafe_allow_html=True
                        )
                        
                        # Process file using business logic
                        results = processor.process_uploaded_file(uploaded_file)
                        
                        # Step 4: Generating reports
                        progress_placeholder.markdown(
                            ui.step_progress_indicator(progress_steps, 3),
                            unsafe_allow_html=True
                        )
                        
                        if results:
                            st.session_state.analysis_results = results
                            st.session_state.analysis_type = "quick"
                            progress_placeholder.empty()
                            st.success("Análisis completado!")
                            st.rerun()
                        else:
                            progress_placeholder.empty()
                            st.error("Error procesando archivo")
                            
                    except Exception as e:
                        progress_placeholder.empty()
                        st.error(f"Error durante análisis: {str(e)}")
        
        with col2:
            # AI Analysis Button
            if st.button("Análisis con IA", type="secondary", use_container_width=True, key="ai_analysis"):
                # Enhanced AI progress feedback
                ai_steps = ["Preparando IA", "Análisis inteligente", "Extrayendo insights", "Generando recomendaciones"]
                ai_progress_placeholder = st.empty()
                
                with st.spinner("Procesando con inteligencia artificial..."):
                    try:
                        from shared.business.file_processor import FileProcessor
                        processor = FileProcessor()
                        
                        # AI processing steps
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
                            st.success("Análisis IA completado!")
                            st.rerun()
                        else:
                            ai_progress_placeholder.empty()
                            st.error("Error procesando archivo con IA")
                            
                    except Exception as e:
                        ai_progress_placeholder.empty()
                        st.error(f"Error durante análisis IA: {str(e)}")
    else:
        st.error(f"Error: {validation['error_message']}")

# INTEGRATED RESULTS SECTION
if 'analysis_results' in st.session_state:
    st.markdown(ui.section_divider(), unsafe_allow_html=True)
    st.markdown("### Resultados del Análisis")
    
    results = st.session_state.analysis_results
    is_ai_analysis = st.session_state.get('analysis_type') == 'ai'
    
    # Analysis method indicator
    if is_ai_analysis:
        st.markdown(
            ui.status_badge("", "Análisis con IA Completado", "positive"),
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            ui.status_badge("", "Análisis Rápido Completado", "neutral"),
            unsafe_allow_html=True
        )
    
    # Executive summary
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
    
    # Charts
    if results.get('sentiment_percentages'):
        import plotly.express as px
        import pandas as pd
        
        sentiment_data = results['sentiment_percentages']
        chart_theme = theme.get_chart_theme(st.session_state.get('dark_mode', True))
        
        fig_sentiment = px.pie(
            values=list(sentiment_data.values()),
            names=list(sentiment_data.keys()),
            title="Distribución de Sentimientos"
        )
        fig_sentiment.update_layout(chart_theme['layout'])
        st.plotly_chart(fig_sentiment, use_container_width=True)
    
    # Excel download
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
            
            # Summary sheet
            summary_data = [
                ['Total Comentarios', results.get('total', 0)],
                ['Positivos %', results.get('sentiment_percentages', {}).get('positivo', 0)],
                ['Negativos %', results.get('sentiment_percentages', {}).get('negativo', 0)],
                ['Neutrales %', results.get('sentiment_percentages', {}).get('neutral', 0)],
                ['Método', 'IA Avanzado' if is_ai_analysis else 'Análisis Rápido']
            ]
            summary_df = pd.DataFrame(summary_data, columns=['Métrica', 'Valor'])
            summary_df.to_excel(writer, sheet_name='Resumen', index=False)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        analysis_type = "IA" if is_ai_analysis else "rapido"
        filename = f"analisis_comentarios_{analysis_type}_{timestamp}.xlsx"
        
        st.download_button(
            label=f"Descargar Reporte {analysis_type.upper()}",
            data=output.getvalue(),
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
            key="download_excel"
        )
        
    except Exception as e:
        st.error(f"Error generando Excel: {e}")
    
    # Reset button
    if st.button("Nuevo Análisis", key="new_analysis", type="secondary"):
        if 'analysis_results' in st.session_state:
            del st.session_state.analysis_results
        if 'analysis_type' in st.session_state:
            del st.session_state.analysis_type
        st.rerun()

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