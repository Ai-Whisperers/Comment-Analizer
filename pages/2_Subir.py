"""
Página Subir - Clean Architecture
Simple upload and analysis page using only src/
"""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd
from datetime import datetime

# Add src to path
current_dir = Path(__file__).parent.parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

# Load CSS and import Clean Architecture components
try:
    from src.shared.exceptions.archivo_exception import ArchivoException
    from src.shared.exceptions.ia_exception import IAException
    from src.presentation.streamlit.css_loader import load_component_css, glass_card, metric_card
    
    # Load CSS if available
    if st.session_state.get('css_loaded', False):
        load_component_css('complete')
        
except ImportError as e:
    st.error(f"Error importando Clean Architecture: {str(e)}")

st.title("Subir y Analizar Comentarios")

st.markdown("""
Sube tu archivo Excel o CSV con comentarios de clientes para análisis automático.
""")

# File upload
st.markdown("### Cargar Archivo")

uploaded_file = st.file_uploader(
    "Selecciona tu archivo",
    type=['xlsx', 'xls', 'csv'],
    help="Formatos soportados: Excel (.xlsx, .xls) y CSV"
)

if uploaded_file:
    # Basic file validation
    file_size_mb = uploaded_file.size / (1024 * 1024)
    
    if file_size_mb > 5:
        st.error("Archivo muy grande. Máximo 5MB.")
        st.stop()
    
    st.success(f"Archivo válido: {uploaded_file.name} ({file_size_mb:.1f}MB)")
    
    # File preview
    with st.expander("Vista previa", expanded=True):
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file, nrows=5)
            else:
                df = pd.read_excel(uploaded_file, nrows=5)
            
            st.dataframe(df)
            st.info(f"Mostrando primeras 5 filas de {len(df.columns)} columnas")
            
        except Exception as e:
            st.warning(f"No se pudo generar vista previa: {str(e)}")
    
    # Analysis section
    st.markdown("### Análisis")
    
    # Check if system is ready
    if 'analizador_app' not in st.session_state:
        st.error("Sistema no inicializado. Recarga la página.")
        st.stop()
    
    # Analysis buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Análisis con IA", type="primary", use_container_width=True):
            _run_analysis(uploaded_file, "ai")
    
    with col2:
        if st.button("Análisis con Reglas", type="secondary", use_container_width=True):
            _run_analysis(uploaded_file, "rules")

# Results section
if 'analysis_results' in st.session_state:
    st.markdown("---")
    st.markdown("### Resultados")
    
    results = st.session_state.analysis_results
    analysis_type = st.session_state.get('analysis_type', 'unknown')
    
    # Status badge
    if analysis_type == "maestro_ia":
        st.success("Análisis maestro IA completado")
    elif 'ai' in analysis_type:
        st.success("Análisis con IA completado")
    else:
        st.info("Análisis con reglas completado")
    
    # Show results - handle both standard and maestro formats
    if hasattr(results, 'es_exitoso'):
        if results.es_exitoso():
            # Executive summary - handle different result types
            col1, col2, col3, col4 = st.columns(4)
            
            # Maestro system has different structure
            if analysis_type == "maestro_ia" and hasattr(results, 'analisis_completo_ia'):
                analisis = results.analisis_completo_ia
                with col1:
                    st.metric("Total", results.total_comentarios)
                with col2:
                    st.metric("Tiempo", f"{results.tiempo_total_segundos:.1f}s")
                with col3:
                    st.metric("Método", "Maestro IA")
                with col4:
                    st.metric("Estado", "Avanzado")
            else:
                # Standard system
                with col1:
                    st.metric("Total", results.total_comentarios)
                
                with col2:
                    stats = results.estadisticas_sentimientos
                    positivos = stats.get('positivos', 0) if stats else 0
                    st.metric("Positivos", positivos)
                
                with col3:
                    negativos = stats.get('negativos', 0) if stats else 0
                    st.metric("Negativos", negativos)
                
                with col4:
                    criticos = getattr(results, 'comentarios_criticos', 0)
                    st.metric("Críticos", criticos)
            
            # Main insights - handle different formats
            st.markdown("#### Temas Principales")
            
            if analysis_type == "maestro_ia" and hasattr(results, 'analisis_completo_ia'):
                # Maestro system format
                analisis = results.analisis_completo_ia
                if hasattr(analisis, 'temas_frecuencias') and analisis.temas_frecuencias:
                    for tema, freq in list(analisis.temas_frecuencias.items())[:5]:
                        st.markdown(f"• **{tema}**: {freq} menciones")
                else:
                    st.info("No hay datos de temas disponibles en análisis maestro")
            elif hasattr(results, 'temas_principales') and results.temas_principales:
                # Standard system format
                for tema, freq in list(results.temas_principales.items())[:5]:
                    st.markdown(f"• **{tema}**: {freq} menciones")
            else:
                st.info("No hay temas detectados")
            
            # Critical comments - handle different formats
            criticos_count = getattr(results, 'comentarios_criticos', 0)
            if criticos_count > 0:
                with st.expander(f"{criticos_count} comentarios críticos"):
                    try:
                        criticos = st.session_state.analizador_app.obtener_comentarios_criticos()
                        for i, comentario in enumerate(criticos[:5], 1):
                            st.warning(f"**{i}.** {comentario.texto}")
                            if comentario.urgencia:
                                st.caption(f"Acción: {comentario.urgencia.accion_recomendada()}")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            
            # Export
            st.markdown("#### Exportar")
            if st.button("Generar Excel", type="secondary"):
                excel_data = _create_simple_excel(results)
                st.download_button(
                    "Descargar Excel", 
                    excel_data,
                    f"analisis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    "application/vnd.ms-excel"
                )
        else:
            st.error(f"Error en análisis: {results.mensaje}")
    else:
        st.error("Formato de resultados no reconocido")


def _run_analysis(uploaded_file, analysis_type):
    """Run analysis using clean architecture (maestro system if available)"""
    with st.spinner(f"Procesando con {'IA' if analysis_type == 'ai' else 'reglas'}..."):
        try:
            # Try maestro system first if available
            if 'caso_uso_maestro' in st.session_state and st.session_state.caso_uso_maestro and analysis_type == 'ai':
                try:
                    from src.application.use_cases.analizar_excel_maestro_caso_uso import ComandoAnalisisExcelMaestro
                    
                    comando = ComandoAnalisisExcelMaestro(
                        archivo_cargado=uploaded_file,
                        nombre_archivo=uploaded_file.name,
                        limpiar_repositorio=True
                    )
                    
                    resultado = st.session_state.caso_uso_maestro.ejecutar(comando)
                    
                    if resultado.es_exitoso():
                        st.session_state.analysis_results = resultado
                        st.session_state.analysis_type = "maestro_ia"
                        st.success("Análisis maestro IA completado!")
                        st.balloons()
                        st.rerun()
                        return
                        
                except Exception as maestro_error:
                    st.warning(f"Maestro IA falló, usando sistema estándar: {maestro_error}")
            
            # Standard system fallback
            app = st.session_state.analizador_app
            
            resultado = app.analizar_archivo(
                archivo_cargado=uploaded_file,
                nombre_archivo=uploaded_file.name,
                incluir_analisis_avanzado=True,
                limpiar_datos_anteriores=True
            )
            
            if resultado.es_exitoso():
                st.session_state.analysis_results = resultado
                st.session_state.analysis_type = f"clean_architecture_{analysis_type}"
                st.success("Análisis completado!")
                st.balloons()
                st.rerun()
            else:
                st.error(f"Error: {resultado.mensaje}")
                
        except ArchivoException as e:
            st.error(f"Error de archivo: {str(e)}")
        except IAException as e:
            st.error(f"Error de IA: {str(e)}")
        except Exception as e:
            st.error(f"Error inesperado: {str(e)}")


def _create_simple_excel(resultado):
    """Create simple Excel export"""
    import io
    from openpyxl import Workbook
    
    wb = Workbook()
    ws = wb.active
    ws.title = "Análisis"
    
    # Header
    ws['A1'] = "Personal Paraguay - Análisis de Comentarios"
    ws['A2'] = f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    ws['A3'] = "Método: Clean Architecture"
    
    # Summary
    ws['A5'] = "RESUMEN"
    ws['A6'] = f"Total: {resultado.total_comentarios}"
    ws['A7'] = f"Críticos: {resultado.comentarios_criticos}"
    
    # Sentiments
    stats = resultado.estadisticas_sentimientos
    ws['A9'] = "SENTIMIENTOS"
    ws['A10'] = f"Positivos: {stats.get('positivos', 0)}"
    ws['A11'] = f"Negativos: {stats.get('negativos', 0)}"
    ws['A12'] = f"Neutrales: {stats.get('neutrales', 0)}"
    
    # Themes
    ws['A14'] = "TEMAS PRINCIPALES"
    row = 15
    for tema, freq in resultado.temas_principales.items():
        ws[f'A{row}'] = f"{tema}: {freq}"
        row += 1
    
    # Save
    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return buffer.getvalue()