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

# Import Clean Architecture components + CSS utilities
try:
    from src.shared.exceptions.archivo_exception import ArchivoException
    from src.shared.exceptions.ia_exception import IAException
    
    # Try to import CSS utilities for enhanced styling
    try:
        from src.presentation.streamlit.css_loader import glass_card, metric_card
        CSS_UTILS_AVAILABLE = True
    except ImportError:
        CSS_UTILS_AVAILABLE = False
        
except ImportError as e:
    st.error(f"Error importando Clean Architecture: {str(e)}")
    CSS_UTILS_AVAILABLE = False

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
    
    # Enhanced file preview with glassmorphism if available
    with st.expander("👀 Vista Previa del Archivo", expanded=True):
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file, nrows=5)
                df_full = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file, nrows=5)
                df_full = pd.read_excel(uploaded_file)
            
            # File stats with enhanced display
            col_stats1, col_stats2, col_stats3 = st.columns(3)
            with col_stats1:
                st.metric("📊 Total Filas", len(df_full))
            with col_stats2:
                st.metric("📋 Columnas", len(df_full.columns))
            with col_stats3:
                # Detect comment column
                comment_cols = ['comentario', 'comment', 'comentarios', 'feedback', 'review']
                comment_col = None
                for col in df_full.columns:
                    if any(cc in col.lower() for cc in comment_cols):
                        comment_col = col
                        break
                st.metric("💬 Comentarios", len(df_full[comment_col].dropna()) if comment_col else "No detectados")
            
            # Data preview
            st.markdown("**Primeras 5 filas:**")
            st.dataframe(df, use_container_width=True)
            
            # Column analysis
            if comment_col:
                st.success(f"✅ Columna de comentarios detectada: **{comment_col}**")
            else:
                st.warning("⚠️ No se detectó columna de comentarios clara")
                
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
            # Pure IA maestro results - use REAL DTO structure
            analisis = results.analisis_completo_ia
            
            with col1:
                st.metric("Total Comentarios", analisis.total_comentarios)
            with col2:
                st.metric("Tiempo IA", f"{analisis.tiempo_analisis:.1f}s")
            with col3:
                # Use real field names from AnalisisCompletoIA
                sentiments = analisis.distribucion_sentimientos
                positivos = sentiments.get('POSITIVO', 0)
                st.metric("Positivos", positivos)
            with col4:
                negativos = sentiments.get('NEGATIVO', 0) 
                st.metric("Negativos", negativos)
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
            
        # IA Insights (pure mechanical mapping using REAL DTO structure)
        st.markdown("#### Insights de Inteligencia Artificial")
        
        if hasattr(results, 'analisis_completo_ia') and results.analisis_completo_ia:
            analisis = results.analisis_completo_ia
            
            # Display IA executive summary first
            st.markdown("**Resumen Ejecutivo (Generado por IA):**")
            st.info(analisis.resumen_ejecutivo)
            
            # IA metrics in columns
            col_ia1, col_ia2 = st.columns(2)
            
            with col_ia1:
                st.markdown("**📊 Métricas IA:**")
                st.metric("Confianza General", f"{analisis.confianza_general:.1f}%")
                st.metric("Modelo Utilizado", analisis.modelo_utilizado)
                st.metric("Tokens Utilizados", f"{analisis.tokens_utilizados:,}")
            
            with col_ia2:
                st.markdown("**🎯 Análisis:**")
                st.metric("Tendencia General", analisis.tendencia_general.title())
                
                # Count critical comments from individual analysis
                if hasattr(results, 'comentarios_analizados') and results.comentarios_analizados:
                    criticos = len([c for c in results.comentarios_analizados if hasattr(c, 'es_critico') and c.es_critico()])
                    st.metric("Comentarios Críticos", criticos)
            
            # Themes from IA (using real structure)
            if analisis.temas_mas_relevantes:
                st.markdown("**🏷️ Temas Principales (IA):**")
                for tema, relevancia in list(analisis.temas_mas_relevantes.items())[:5]:
                    st.markdown(f"• **{tema}**: {relevancia:.1f} relevancia")
            
            # Emotions from IA (using real structure)
            if analisis.emociones_predominantes:
                st.markdown("**😊 Emociones Predominantes (IA):**")
                for emocion, intensidad in list(analisis.emociones_predominantes.items())[:5]:
                    st.markdown(f"• **{emocion}**: {intensidad:.1f} intensidad")
            
            # Pain points from IA
            if analisis.dolores_mas_severos:
                st.markdown("**⚠️ Puntos de Dolor Más Severos (IA):**")
                for dolor, severidad in list(analisis.dolores_mas_severos.items())[:3]:
                    st.markdown(f"• **{dolor}**: {severidad:.1f} severidad")
            
            # IA Recommendations
            if analisis.recomendaciones_principales:
                st.markdown("**💡 Recomendaciones de IA:**")
                for i, recomendacion in enumerate(analisis.recomendaciones_principales[:3], 1):
                    st.markdown(f"{i}. {recomendacion}")
            
            # Critical comments detected by IA (using real data structure)
            if hasattr(results, 'comentarios_analizados') and results.comentarios_analizados:
                criticos_ia = [c for c in results.comentarios_analizados 
                              if hasattr(c, 'es_critico') and c.es_critico()]
                
                if criticos_ia:
                    with st.expander(f"🚨 {len(criticos_ia)} comentarios críticos (IA)"):
                        st.warning("Comentarios que requieren atención inmediata según análisis IA:")
                        for i, comentario in enumerate(criticos_ia[:5], 1):
                            st.warning(f"**{i}.** {comentario.texto_original}")
                            
                            # Show IA-detected urgency and recommendations
                            if hasattr(comentario, 'puntos_dolor') and comentario.puntos_dolor:
                                dolores_texto = ", ".join([p.descripcion for p in comentario.puntos_dolor[:2]])
                                st.caption(f"🎯 Puntos de dolor IA: {dolores_texto}")
                            
                            if hasattr(comentario, 'recomendaciones') and comentario.recomendaciones:
                                st.caption(f"💡 Recomendación IA: {comentario.recomendaciones[0]}")
        else:
            st.info("Análisis IA completado - formato de datos simplificado")
        
        # Export IA results
        st.markdown("#### Exportar Análisis IA")
        if st.button("Generar Excel Profesional IA", type="secondary"):
            excel_data = _create_professional_excel(results)
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


def _create_professional_excel(resultado):
    """Create comprehensive Excel export from IA analysis using real DTO structure"""
    import io
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment
    
    wb = Workbook()
    ws = wb.active
    ws.title = "Análisis IA Completo"
    
    # Styling
    header_font = Font(bold=True, size=14)
    section_font = Font(bold=True, size=12)
    
    # Header section
    ws['A1'] = "Personal Paraguay - Análisis con Inteligencia Artificial"
    ws['A1'].font = header_font
    ws['A2'] = f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    ws['A3'] = "Método: AnalizadorMaestroIA + GPT-4"
    
    if hasattr(resultado, 'analisis_completo_ia') and resultado.analisis_completo_ia:
        analisis = resultado.analisis_completo_ia
        
        # Executive Summary
        ws['A5'] = "RESUMEN EJECUTIVO IA"
        ws['A5'].font = section_font
        ws['A6'] = f"Total comentarios analizados: {analisis.total_comentarios}"
        ws['A7'] = f"Tendencia general: {analisis.tendencia_general}"
        ws['A8'] = f"Confianza del análisis: {analisis.confianza_general:.1f}%"
        ws['A9'] = f"Modelo IA utilizado: {analisis.modelo_utilizado}"
        ws['A10'] = f"Tiempo de procesamiento: {analisis.tiempo_analisis:.1f}s"
        ws['A11'] = f"Tokens consumidos: {analisis.tokens_utilizados:,}"
        
        # IA Narrative Summary
        ws['A13'] = "ANÁLISIS NARRATIVO IA"
        ws['A13'].font = section_font
        ws.merge_cells('A14:E14')
        ws['A14'] = analisis.resumen_ejecutivo
        ws['A14'].alignment = Alignment(wrap_text=True)
        
        # Sentiment distribution
        ws['A16'] = "DISTRIBUCIÓN DE SENTIMIENTOS"
        ws['A16'].font = section_font
        row = 17
        for sentimiento, cantidad in analisis.distribucion_sentimientos.items():
            ws[f'A{row}'] = sentimiento
            ws[f'B{row}'] = cantidad
            ws[f'C{row}'] = f"{(cantidad/analisis.total_comentarios)*100:.1f}%"
            row += 1
        
        # Top themes with relevance
        ws[f'A{row + 1}'] = "TEMAS MÁS RELEVANTES"
        ws[f'A{row + 1}'].font = section_font
        row += 2
        for tema, relevancia in list(analisis.temas_mas_relevantes.items())[:8]:
            ws[f'A{row}'] = tema
            ws[f'B{row}'] = f"{relevancia:.2f}"
            ws[f'C{row}'] = "Alta" if relevancia > 0.7 else "Media" if relevancia > 0.4 else "Baja"
            row += 1
        
        # Emotions with intensities
        ws[f'A{row + 1}'] = "EMOCIONES PREDOMINANTES"
        ws[f'A{row + 1}'].font = section_font  
        row += 2
        for emocion, intensidad in list(analisis.emociones_predominantes.items())[:6]:
            ws[f'A{row}'] = emocion
            ws[f'B{row}'] = f"{intensidad:.1f}"
            ws[f'C{row}'] = "Intensa" if intensidad > 7 else "Moderada" if intensidad > 4 else "Leve"
            row += 1
        
        # Pain points with severity
        if analisis.dolores_mas_severos:
            ws[f'A{row + 1}'] = "PUNTOS DE DOLOR CRÍTICOS"
            ws[f'A{row + 1}'].font = section_font
            row += 2
            for dolor, severidad in list(analisis.dolores_mas_severos.items())[:5]:
                ws[f'A{row}'] = dolor
                ws[f'B{row}'] = f"{severidad:.1f}"
                ws[f'C{row}'] = "Crítico" if severidad > 8 else "Alto" if severidad > 6 else "Medio"
                row += 1
        
        # IA Recommendations
        ws[f'A{row + 1}'] = "RECOMENDACIONES ACCIONABLES IA"
        ws[f'A{row + 1}'].font = section_font
        row += 2
        for i, recomendacion in enumerate(analisis.recomendaciones_principales, 1):
            ws[f'A{row}'] = f"Recomendación {i}"
            ws.merge_cells(f'B{row}:E{row}')
            ws[f'B{row}'] = recomendacion
            ws[f'B{row}'].alignment = Alignment(wrap_text=True)
            row += 1
            
    else:
        # Fallback structure
        ws['A5'] = "DATOS LIMITADOS DISPONIBLES"
        ws['A6'] = f"Total comentarios: {getattr(resultado, 'total_comentarios', 0)}"
    
    # Adjust column widths
    ws.column_dimensions['A'].width = 25
    ws.column_dimensions['B'].width = 15
    ws.column_dimensions['C'].width = 15
    ws.column_dimensions['D'].width = 15
    ws.column_dimensions['E'].width = 30
    
    # Save to bytes
    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return buffer.getvalue()