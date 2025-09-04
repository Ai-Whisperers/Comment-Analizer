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

# Import Clean Architecture components only
try:
    from src.shared.exceptions.archivo_exception import ArchivoException
    from src.shared.exceptions.ia_exception import IAException
    # CSS is handled in main app
        
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
    
    # IA Analysis (single button - pure IA app)
    if st.button("Analizar con Inteligencia Artificial", type="primary", use_container_width=True):
        _run_analysis(uploaded_file, "ai")

# Results section
if 'analysis_results' in st.session_state:
    st.markdown("---")
    st.markdown("### Resultados")
    
    results = st.session_state.analysis_results
    analysis_type = st.session_state.get('analysis_type', 'unknown')
    
    # IA Analysis status (pure IA app)
    st.success("Análisis con Inteligencia Artificial completado")
    
    # Show IA analysis results (pure IA format)
    if hasattr(results, 'es_exitoso') and results.es_exitoso():
        # IA Analysis metrics
        col1, col2, col3, col4 = st.columns(4)
        
        if hasattr(results, 'analisis_completo_ia') and results.analisis_completo_ia:
            # Pure IA maestro results
            analisis = results.analisis_completo_ia
            
            with col1:
                st.metric("Total Comentarios", results.total_comentarios)
            with col2:
                st.metric("Tiempo IA", f"{results.tiempo_total_segundos:.1f}s")
            with col3:
                # Get sentiment counts from IA analysis (correct field name)
                sentiments_ia = getattr(analisis, 'distribucion_sentimientos', {})
                positivos = sentiments_ia.get('POSITIVO', 0)
                st.metric("IA: Positivos", positivos)
            with col4:
                negativos = sentiments_ia.get('NEGATIVO', 0)
                st.metric("IA: Negativos", negativos)
        else:
            # Fallback metrics if IA structure incomplete
            with col1:
                st.metric("Total Comentarios", results.total_comentarios)
            with col2:
                st.metric("Estado", "Procesado")
            with col3:
                st.metric("Método", "IA Avanzada")
            with col4:
                st.metric("Calidad", "Máxima")
            
        # IA Insights (pure mechanical mapping from IA data)
        st.markdown("#### Insights de Inteligencia Artificial")
        
        if hasattr(results, 'analisis_completo_ia') and results.analisis_completo_ia:
            # Pure IA maestro results - mechanical display
            analisis = results.analisis_completo_ia
            
            # Temas detectados por IA (mechanical mapping)
            if hasattr(analisis, 'temas_mas_relevantes') and analisis.temas_mas_relevantes:
                st.markdown("**Temas principales detectados por IA:**")
                for tema, relevancia in list(analisis.temas_mas_relevantes.items())[:5]:
                    st.markdown(f"• **{tema}**: Relevancia {relevancia:.2f}")
            
            # Emociones detectadas por IA (mechanical mapping)
            if hasattr(analisis, 'emociones_predominantes') and analisis.emociones_predominantes:
                st.markdown("**Emociones identificadas por IA:**")
                for emocion, intensidad in list(analisis.emociones_predominantes.items())[:5]:
                    st.markdown(f"• **{emocion}**: Intensidad {intensidad:.1f}")
            
            # Resumen ejecutivo generado por IA
            if hasattr(analisis, 'resumen_ejecutivo') and analisis.resumen_ejecutivo:
                st.markdown("**Resumen Ejecutivo (Generado por IA):**")
                st.info(analisis.resumen_ejecutivo)
            
            # Recomendaciones de IA
            if hasattr(analisis, 'recomendaciones_principales') and analisis.recomendaciones_principales:
                st.markdown("**Recomendaciones de IA:**")
                for i, recomendacion in enumerate(analisis.recomendaciones_principales[:3], 1):
                    st.markdown(f"{i}. {recomendacion}")
            
            # Comentarios críticos identificados por IA
            if hasattr(results, 'comentarios_analizados') and results.comentarios_analizados:
                criticos_ia = [c for c in results.comentarios_analizados if hasattr(c, 'es_critico') and c.es_critico()]
                if criticos_ia:
                    with st.expander(f"{len(criticos_ia)} comentarios críticos detectados por IA"):
                        st.warning("Comentarios que requieren atención inmediata según análisis IA:")
                        for i, comentario in enumerate(criticos_ia[:5], 1):
                            st.warning(f"**{i}.** {comentario.texto_original}")
                            if hasattr(comentario, 'urgencia_detectada'):
                                st.caption(f"Urgencia IA: {comentario.urgencia_detectada}")
        else:
            st.info("Datos de análisis IA no disponibles en formato esperado")
        
        # Export IA results
        st.markdown("#### Exportar Análisis IA")
        if st.button("Generar Excel con Resultados IA", type="secondary"):
            excel_data = _create_simple_excel(results)
            st.download_button(
                "Descargar Excel", 
                excel_data,
                f"analisis_ia_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                "application/vnd.ms-excel"
            )
    else:
        st.error(f"Error en análisis IA: {results.mensaje if hasattr(results, 'mensaje') else 'Error desconocido'}")


def _run_analysis(uploaded_file, analysis_type):
    """Run pure IA analysis using maestro system only"""
    with st.spinner("Procesando con Inteligencia Artificial..."):
        try:
            # Pure IA analysis - no fallbacks
            if 'caso_uso_maestro' not in st.session_state or not st.session_state.caso_uso_maestro:
                st.error("Sistema IA no está disponible. Verifica configuración de OpenAI API key.")
                return
                
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
                st.success("Análisis IA completado!")
                st.balloons()
                st.rerun()
            else:
                st.error(f"Error en análisis IA: {resultado.mensaje}")
                
        except ArchivoException as e:
            st.error(f"Error procesando archivo: {str(e)}")
        except IAException as e:
            st.error(f"Error de servicio IA: {str(e)}")
            st.info("Verifica que tu OpenAI API key esté configurada correctamente.")
        except Exception as e:
            st.error(f"Error inesperado: {str(e)}")
            st.error("Este es un error no manejado. Por favor contacta soporte técnico.")


def _create_simple_excel(resultado):
    """Create Excel export from pure IA analysis (mechanical mapping)"""
    import io
    from openpyxl import Workbook
    
    wb = Workbook()
    ws = wb.active
    ws.title = "Análisis IA"
    
    # Header
    ws['A1'] = "Personal Paraguay - Análisis con Inteligencia Artificial"
    ws['A2'] = f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    ws['A3'] = "Método: AnalizadorMaestroIA + GPT-4"
    
    # IA Analysis Summary
    if hasattr(resultado, 'analisis_completo_ia') and resultado.analisis_completo_ia:
        analisis = resultado.analisis_completo_ia
        
        ws['A5'] = "ANÁLISIS IA - RESUMEN EJECUTIVO"
        ws['A6'] = f"Total comentarios: {analisis.total_comentarios}"
        ws['A7'] = f"Tendencia general: {analisis.tendencia_general}"
        ws['A8'] = f"Confianza IA: {analisis.confianza_general:.2f}"
        ws['A9'] = f"Modelo utilizado: {analisis.modelo_utilizado}"
        ws['A10'] = f"Tiempo análisis: {analisis.tiempo_analisis:.1f}s"
        
        # IA Executive Summary
        ws['A12'] = "RESUMEN EJECUTIVO (GENERADO POR IA)"
        ws['A13'] = analisis.resumen_ejecutivo
        
        # Sentimientos (from IA)
        ws['A15'] = "DISTRIBUCIÓN SENTIMIENTOS (IA)"
        row = 16
        for sentimiento, cantidad in analisis.distribucion_sentimientos.items():
            ws[f'A{row}'] = f"{sentimiento}: {cantidad}"
            row += 1
        
        # Temas relevantes (from IA)
        ws[f'A{row + 1}'] = "TEMAS MÁS RELEVANTES (IA)"
        row += 2
        for tema, relevancia in analisis.temas_mas_relevantes.items():
            ws[f'A{row}'] = f"{tema}: {relevancia:.2f} relevancia"
            row += 1
        
        # Emociones (from IA)
        ws[f'A{row + 1}'] = "EMOCIONES PREDOMINANTES (IA)"
        row += 2
        for emocion, intensidad in analisis.emociones_predominantes.items():
            ws[f'A{row}'] = f"{emocion}: {intensidad:.1f} intensidad"
            row += 1
        
        # Recomendaciones (from IA)
        ws[f'A{row + 1}'] = "RECOMENDACIONES PRINCIPALES (IA)"
        row += 2
        for i, recomendacion in enumerate(analisis.recomendaciones_principales, 1):
            ws[f'A{row}'] = f"{i}. {recomendacion}"
            row += 1
    else:
        # Fallback if AnalisisCompletoIA not available
        ws['A5'] = "ANÁLISIS ESTÁNDAR"
        ws['A6'] = f"Total: {getattr(resultado, 'total_comentarios', 0)}"
    
    # Save
    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return buffer.getvalue()