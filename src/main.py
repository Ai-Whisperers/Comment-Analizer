"""
Comment Analyzer - Personal Paraguay
Sentiment analysis for customer feedback
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
from datetime import datetime
import numpy as np
from collections import Counter
import re
from io import BytesIO
from src.ai_overseer import apply_ai_oversight
from src.ui_styling import inject_styles, UIComponents, ThemeManager


# Page config
st.set_page_config(
    page_title="Personal Paraguay — Análisis de Comentarios",
    page_icon="P",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize theme state
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True  # Default to dark mode for web3 aesthetics

# Initialize UI components helper
ui = UIComponents()
theme_manager = ThemeManager()

# Theme toggle in sidebar
with st.sidebar:
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("◐", key="theme_toggle", help="Toggle Dark/Light Mode"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()
    with col2:
        st.markdown(f"**{'Dark' if st.session_state.dark_mode else 'Light'} Mode**")
    st.markdown("---")

# Inject all styles
st.markdown(inject_styles(st.session_state.dark_mode), unsafe_allow_html=True)

# Color system is now handled by ui_styling module

# Get current theme colors from theme manager
theme = theme_manager.get_theme(st.session_state.dark_mode)

# All CSS is now handled by the ui_styling module
# Old CSS blocks have been completely removed

@st.cache_data
def analyze_sentiment_simple(text):
    """Analyze sentiment of text"""
    if pd.isna(text) or text == "":
        return "neutral"
    
    text = str(text).lower()
    
    # Spanish sentiment words
    positive_words = [
        'excelente', 'bueno', 'buena', 'mejor', 'satisfecho', 'contento',
        'rápido', 'rápida', 'eficiente', 'funciona', 'bien', 'perfecto',
        'recomiendo', 'feliz', 'increíble', 'fantástico', 'genial'
    ]
    
    negative_words = [
        'malo', 'mala', 'pésimo', 'pesimo', 'terrible', 'horrible',
        'lento', 'lenta', 'no funciona', 'problema', 'problemas',
        'error', 'falla', 'deficiente', 'caro', 'costoso', 'demora'
    ]
    
    # Count positive and negative indicators
    pos_count = sum(word in text for word in positive_words)
    neg_count = sum(word in text for word in negative_words)
    
    if pos_count > neg_count:
        return "positivo"
    elif neg_count > pos_count:
        return "negativo"
    else:
        return "neutral"

def clean_text_simple(text):
    """Clean and normalize text"""
    if pd.isna(text) or text == "":
        return text
    
    text = str(text).strip()
    
    # Basic corrections for common typos
    corrections = {
        'pesimo': 'pésimo', 'lentp': 'lento', 'servico': 'servicio',
        'internert': 'internet', 'intenet': 'internet', 'señaal': 'señal',
        'exelente': 'excelente', 'buenno': 'bueno', 'no funcona': 'no funciona'
    }
    
    for wrong, correct in corrections.items():
        text = text.replace(wrong, correct)
    
    return text.strip()

def remove_duplicates_simple(comments):
    """Remove duplicate comments"""
    if not comments:
        return [], {}
    
    # Remove exact duplicates and very short comments
    seen = set()
    unique_comments = []
    frequencies = {}
    
    for comment in comments:
        clean = str(comment).lower().strip()
        if len(clean.split()) >= 3 and clean not in seen:  # At least 3 words
            seen.add(clean)
            unique_comments.append(comment)
            frequencies[comment] = 1
        elif clean in seen:
            # Count frequency of duplicates
            for uc in unique_comments:
                if str(uc).lower().strip() == clean:
                    frequencies[uc] = frequencies.get(uc, 1) + 1
                    break
    
    return unique_comments, frequencies

def extract_themes_simple(texts):
    """Extract themes from comments"""
    themes = {
        'velocidad': ['lento', 'lenta', 'velocidad', 'demora', 'tarda'],
        'interrupciones': ['cae', 'corta', 'corte', 'intermitencia', 'interrumpe'],
        'servicio': ['atención', 'servicio', 'cliente', 'soporte', 'ayuda'],
        'precio': ['caro', 'precio', 'costoso', 'tarifa', 'factura'],
        'cobertura': ['cobertura', 'señal', 'zona', 'área', 'alcance'],
        'instalacion': ['instalación', 'técnico', 'visita', 'demora']
    }
    
    theme_counts = {theme: 0 for theme in themes}
    theme_examples = {theme: [] for theme in themes}
    
    for text in texts:
        if pd.isna(text):
            continue
        text_lower = str(text).lower()
        for theme, keywords in themes.items():
            if any(keyword in text_lower for keyword in keywords):
                theme_counts[theme] += 1
                if len(theme_examples[theme]) < 3:
                    theme_examples[theme].append(text[:100])
    
    return theme_counts, theme_examples

def process_file_simple(uploaded_file):
    """Process uploaded file and extract comments"""
    try:
        # Read file
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        # Find comment column
        comment_cols = ['comentario final', 'comment', 'comments', 'feedback', 'texto', 'comentario']
        comment_col = None
        
        for col in df.columns:
            if any(name in col.lower() for name in comment_cols):
                comment_col = col
                break
        
        if comment_col is None:
            # Use first text column
            for col in df.columns:
                if df[col].dtype == 'object':
                    comment_col = col
                    break
        
        if comment_col is None:
            st.error("No se encontró columna de comentarios")
            return None
        
        # Extract and clean comments
        raw_comments = df[comment_col].dropna().tolist()
        if not raw_comments:
            st.error("No se encontraron comentarios válidos")
            return None
        
        # Clean text
        cleaned_comments = [clean_text_simple(comment) for comment in raw_comments]
        
        # Remove duplicates
        unique_comments, comment_frequencies = remove_duplicates_simple(cleaned_comments)
        
        # Analyze sentiment
        sentiments = [analyze_sentiment_simple(comment) for comment in unique_comments]
        
        # Count sentiments
        sentiment_counts = Counter(sentiments)
        total = len(unique_comments)
        
        positive_count = sentiment_counts.get('positivo', 0)
        neutral_count = sentiment_counts.get('neutral', 0)
        negative_count = sentiment_counts.get('negativo', 0)
        
        # Calculate percentages
        positive_pct = round((positive_count / total * 100), 1) if total > 0 else 0
        neutral_pct = round((neutral_count / total * 100), 1) if total > 0 else 0
        negative_pct = round((negative_count / total * 100), 1) if total > 0 else 0
        
        # Extract themes
        theme_counts, theme_examples = extract_themes_simple(unique_comments)
        
        # File statistics
        file_size_kb = uploaded_file.size / 1024 if hasattr(uploaded_file, 'size') else 0
        avg_length = np.mean([len(comment) for comment in unique_comments]) if unique_comments else 0
        
        results = {
            'total': total,
            'raw_total': len(raw_comments),
            'duplicates_removed': len(raw_comments) - len(unique_comments),
            'positive_count': positive_count,
            'neutral_count': neutral_count,
            'negative_count': negative_count,
            'positive_pct': positive_pct,
            'neutral_pct': neutral_pct,
            'negative_pct': negative_pct,
            'comments': unique_comments,
            'sentiments': sentiments,
            'comment_frequencies': comment_frequencies,
            'theme_counts': theme_counts,
            'theme_examples': theme_examples,
            'original_filename': uploaded_file.name,
            'analysis_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'file_size': file_size_kb,
            'avg_length': avg_length,
            'analysis_method': 'SIMPLE_RULE_BASED'
        }
        
        # Apply AI Oversight for quality validation
        try:
            enhanced_results = apply_ai_oversight(results, strict=False, language='es')
            
            # Show AI validation status
            if 'overseer_validation' in enhanced_results:
                validation = enhanced_results['overseer_validation']
                if validation.get('ai_enhanced'):
                    st.info(f"Validación IA aplicada - Confianza: {validation.get('confidence', 0):.1%}")
                else:
                    st.info("Validación basada en reglas aplicada")
            
            return enhanced_results
        except Exception as ai_error:
            st.warning(f"Validación IA no disponible: {str(ai_error)}")
            # Return original results if AI oversight fails
            return results
        
    except Exception as e:
        st.error(f"Error procesando archivo: {str(e)}")
        return None

def create_simple_excel(results):
    """Create enhanced Excel report with complete analysis results and formatting"""
    output = BytesIO()
    
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        workbook = writer.book
        
        # Define formats for better visualization
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'center',
            'fg_color': '#8B5CF6',
            'font_color': 'white',
            'border': 1
        })
        
        positive_format = workbook.add_format({
            'fg_color': '#E6F7ED',
            'font_color': '#10B981',
            'border': 1
        })
        
        negative_format = workbook.add_format({
            'fg_color': '#FEE2E2',
            'font_color': '#EF4444',
            'border': 1
        })
        
        neutral_format = workbook.add_format({
            'fg_color': '#F3F4F6',
            'font_color': '#6B7280',
            'border': 1
        })
        
        # Sheet 1: Executive Summary (NEW)
        exec_summary = {
            'KPI': [
                'Total Comentarios Analizados',
                'Satisfacción Neta (Positivos - Negativos)',
                'Temas Críticos Detectados',
                'Calidad del Análisis',
                'Comentarios Únicos',
                'Tasa de Duplicación'
            ],
            'Valor': [
                results['total'],
                f"{results['positive_pct'] - results['negative_pct']:.1f}%",
                sum(1 for v in results.get('theme_counts', {}).values() if v > 5),
                f"{results.get('overseer_validation', {}).get('quality_score', 0):.0%}",
                results['total'],
                f"{(results.get('duplicates_removed', 0) / results.get('raw_total', results.get('total', 1)) * 100) if results.get('raw_total', results.get('total', 1)) > 0 else 0:.1f}%"
            ],
            'Interpretación': [
                'Volumen total de feedback procesado',
                'Diferencia entre sentimientos positivos y negativos',
                'Número de temas con más de 5 menciones',
                'Confianza en el análisis realizado',
                'Comentarios después de eliminar duplicados',
                'Porcentaje de comentarios duplicados encontrados'
            ]
        }
        df_exec = pd.DataFrame(exec_summary)
        df_exec.to_excel(writer, sheet_name='Resumen Ejecutivo', index=False)
        worksheet_exec = writer.sheets['Resumen Ejecutivo']
        
        # Format executive summary headers
        for col_num, value in enumerate(df_exec.columns.values):
            worksheet_exec.write(0, col_num, value, header_format)
        
        # Auto-adjust column widths
        worksheet_exec.set_column('A:A', 40)
        worksheet_exec.set_column('B:B', 25)
        worksheet_exec.set_column('C:C', 50)
        
        # Sheet 2: Original Summary (Enhanced)
        summary_data = {
            'Métrica': ['Total Comentarios', 'Positivos', 'Neutrales', 'Negativos', 'Duplicados Eliminados'],
            'Valor': [results['total'], f"{results['positive_pct']}%", f"{results['neutral_pct']}%", 
                     f"{results['negative_pct']}%", results['duplicates_removed']],
            'Cantidad': [results['total'], results['positive_count'], results['neutral_count'],
                        results['negative_count'], results['duplicates_removed']]
        }
        df_summary = pd.DataFrame(summary_data)
        df_summary.to_excel(writer, sheet_name='Resumen', index=False)
        worksheet_summary = writer.sheets['Resumen']
        
        # Format summary headers
        for col_num, value in enumerate(df_summary.columns.values):
            worksheet_summary.write(0, col_num, value, header_format)
        
        # Sheet 3: ALL Comments with enhanced data (NO LIMIT)
        comments_data = {
            'Comentario': results['comments'],  # ALL comments, no [:500] limit
            'Sentimiento': results['sentiments'],
            'Frecuencia': [results['comment_frequencies'].get(c, 1) for c in results['comments']],
            'Requiere Acción': ['Sí' if s == 'negativo' else 'No' for s in results['sentiments']],
            'Prioridad': ['Alta' if s == 'negativo' else 'Media' if s == 'neutral' else 'Baja' 
                         for s in results['sentiments']]
        }
        df_comments = pd.DataFrame(comments_data)
        df_comments.to_excel(writer, sheet_name='Comentarios Completos', index=False)
        worksheet_comments = writer.sheets['Comentarios Completos']
        
        # Format comments headers
        for col_num, value in enumerate(df_comments.columns.values):
            worksheet_comments.write(0, col_num, value, header_format)
        
        # Auto-adjust column width for comments
        worksheet_comments.set_column('A:A', 60)
        worksheet_comments.set_column('B:E', 15)
        
        # Sheet 4: Themes with more details
        if results.get('theme_counts'):
            themes_data = {
                'Tema': list(results['theme_counts'].keys()),
                'Cantidad': list(results['theme_counts'].values()),
                'Porcentaje': [f"{(v/results['total']*100):.1f}%" if results['total'] > 0 else "0%" 
                              for v in results['theme_counts'].values()],
                'Impacto': ['Alto' if v > 10 else 'Medio' if v > 5 else 'Bajo' 
                           for v in results['theme_counts'].values()]
            }
            df_themes = pd.DataFrame(themes_data)
            df_themes.to_excel(writer, sheet_name='Análisis de Temas', index=False)
            worksheet_themes = writer.sheets['Análisis de Temas']
            
            # Format themes headers
            for col_num, value in enumerate(df_themes.columns.values):
                worksheet_themes.write(0, col_num, value, header_format)
        
        # Sheet 5: Pain Points Matrix (NEW)
        pain_points_data = {
            'Punto de Dolor': [
                'Velocidad/Lentitud',
                'Interrupciones del Servicio',
                'Atención al Cliente',
                'Precios Altos',
                'Problemas de Cobertura',
                'Demoras en Instalación'
            ],
            'Frecuencia': [
                results.get('theme_counts', {}).get('velocidad', 0),
                results.get('theme_counts', {}).get('interrupciones', 0),
                results.get('theme_counts', {}).get('servicio', 0),
                results.get('theme_counts', {}).get('precio', 0),
                results.get('theme_counts', {}).get('cobertura', 0),
                results.get('theme_counts', {}).get('instalacion', 0)
            ]
        }
        
        # Calculate impact scores based on frequency and sentiment correlation
        pain_points_data['Impacto en Negocio'] = [
            'CRÍTICO' if freq > 10 else 'ALTO' if freq > 5 else 'MEDIO' if freq > 0 else 'BAJO'
            for freq in pain_points_data['Frecuencia']
        ]
        
        pain_points_data['Prioridad'] = [
            1 if imp == 'CRÍTICO' else 2 if imp == 'ALTO' else 3 if imp == 'MEDIO' else 4
            for imp in pain_points_data['Impacto en Negocio']
        ]
        
        pain_points_data['Acción Recomendada'] = [
            'Intervención inmediata requerida' if freq > 10 else
            'Revisar y mejorar proceso' if freq > 5 else
            'Monitorear tendencia' if freq > 0 else
            'Sin acciones requeridas'
            for freq in pain_points_data['Frecuencia']
        ]
        
        df_pain = pd.DataFrame(pain_points_data)
        df_pain = df_pain.sort_values('Prioridad')  # Sort by priority
        df_pain.to_excel(writer, sheet_name='Matriz de Puntos Críticos', index=False)
        worksheet_pain = writer.sheets['Matriz de Puntos Críticos']
        
        # Format pain points headers
        for col_num, value in enumerate(df_pain.columns.values):
            worksheet_pain.write(0, col_num, value, header_format)
        
        # Apply conditional formatting for impact column
        worksheet_pain.conditional_format('C2:C7', {
            'type': 'cell',
            'criteria': 'equal to',
            'value': '"CRÍTICO"',
            'format': negative_format
        })
        
        worksheet_pain.conditional_format('C2:C7', {
            'type': 'cell',
            'criteria': 'equal to',
            'value': '"ALTO"',
            'format': workbook.add_format({'fg_color': '#FEF3C7', 'font_color': '#F59E0B'})
        })
        
        # Auto-adjust columns
        worksheet_pain.set_column('A:A', 25)
        worksheet_pain.set_column('B:B', 12)
        worksheet_pain.set_column('C:C', 18)
        worksheet_pain.set_column('D:D', 10)
        worksheet_pain.set_column('E:E', 35)
        
        # Sheet 6: AI Insights (if available)
        if 'overseer_validation' in results:
            ai_data = {
                'Métrica de Calidad': [
                    'Validación Aplicada',
                    'Confianza del Análisis',
                    'Calidad General',
                    'Mejorado con IA',
                    'Fecha de Análisis'
                ],
                'Valor': [
                    'Sí' if results['overseer_validation'].get('validated') else 'No',
                    f"{results['overseer_validation'].get('confidence', 0):.0%}",
                    f"{results['overseer_validation'].get('quality_score', 0):.0%}",
                    'Sí' if results['overseer_validation'].get('ai_enhanced') else 'No',
                    results['overseer_validation'].get('timestamp', 'N/A')
                ]
            }
            df_ai = pd.DataFrame(ai_data)
            df_ai.to_excel(writer, sheet_name='Validación IA', index=False)
            worksheet_ai = writer.sheets['Validación IA']
            
            # Format AI insights headers
            for col_num, value in enumerate(df_ai.columns.values):
                worksheet_ai.write(0, col_num, value, header_format)
            
            worksheet_ai.set_column('A:A', 25)
            worksheet_ai.set_column('B:B', 30)
        
        # Sheet 7: Sentiment Analysis Chart Data
        chart_data = {
            'Sentimiento': ['Positivo', 'Neutral', 'Negativo'],
            'Cantidad': [results['positive_count'], results['neutral_count'], results['negative_count']],
            'Porcentaje': [results['positive_pct'], results['neutral_pct'], results['negative_pct']]
        }
        df_chart = pd.DataFrame(chart_data)
        df_chart.to_excel(writer, sheet_name='Datos para Gráficos', index=False)
        worksheet_chart = writer.sheets['Datos para Gráficos']
        
        # Create a pie chart
        pie_chart = workbook.add_chart({'type': 'pie'})
        pie_chart.add_series({
            'name': 'Distribución de Sentimientos',
            'categories': ['Datos para Gráficos', 1, 0, 3, 0],
            'values': ['Datos para Gráficos', 1, 1, 3, 1],
            'points': [
                {'fill': {'color': '#10B981'}},  # Green for positive
                {'fill': {'color': '#6B7280'}},  # Gray for neutral
                {'fill': {'color': '#EF4444'}},  # Red for negative
            ],
        })
        pie_chart.set_title({'name': 'Distribución de Sentimientos'})
        pie_chart.set_size({'width': 380, 'height': 280})
        worksheet_chart.insert_chart('E2', pie_chart)
        
        # Create a column chart for themes
        if results.get('theme_counts'):
            col_chart = workbook.add_chart({'type': 'column'})
            col_chart.add_series({
                'name': 'Frecuencia de Temas',
                'categories': ['Análisis de Temas', 1, 0, len(results['theme_counts']), 0],
                'values': ['Análisis de Temas', 1, 1, len(results['theme_counts']), 1],
                'fill': {'color': '#8B5CF6'},
            })
            col_chart.set_title({'name': 'Temas Principales Detectados'})
            col_chart.set_x_axis({'name': 'Tema'})
            col_chart.set_y_axis({'name': 'Frecuencia'})
            col_chart.set_size({'width': 480, 'height': 320})
            worksheet_themes.insert_chart('F2', col_chart)
    
    output.seek(0)
    return output.getvalue()

# Initialize session state
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None

# Web3 Animated Header using clean UI component
st.markdown(
    ui.animated_header(
        title="Análisis de Comentarios",
        subtitle="Personal Paraguay | Sentiment Analysis Platform"
    ),
    unsafe_allow_html=True
)

# Add floating particles effect
st.markdown(ui.floating_particles(), unsafe_allow_html=True)

# Upload section with glass container
st.markdown(ui.upload_section(), unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "",
    type=['csv', 'xlsx', 'xls'],
    help="Drag and drop or click to upload Excel/CSV files",
    label_visibility="collapsed"
)

# Analysis button
if uploaded_file:
    # Add section divider
    st.markdown(ui.section_divider(), unsafe_allow_html=True)
    st.info(f"Archivo cargado: {uploaded_file.name}")
    
    # Animated analyze button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Analizar Comentarios", type="primary", use_container_width=True):
            with st.spinner("Procesando comentarios..."):
                results = process_file_simple(uploaded_file)
                if results:
                    st.session_state.analysis_results = results
                    st.success("Análisis completado!")
                    # Add success animation
                    st.balloons()
                    st.rerun()

# Results display
if st.session_state.analysis_results:
    results = st.session_state.analysis_results
    
    # Display AI Oversight Report if available
    if 'oversight_report' in results:
        with st.expander("Reporte de Validación IA", expanded=False):
            st.text(results['oversight_report'])
    
    # Display quality metrics if available
    if 'overseer_validation' in results:
        validation_data = results['overseer_validation']
        quality_score = validation_data.get('quality_score', 0)
        
        # Show quality badge
        if quality_score >= 0.8:
            st.success(f"Calidad de Análisis: {quality_score:.1%} - Excelente")
        elif quality_score >= 0.6:
            st.warning(f"Calidad de Análisis: {quality_score:.1%} - Mejorable")
        else:
            st.error(f"Calidad de Análisis: {quality_score:.1%} - Requiere Revisión")
    
    # Add section divider before results
    st.markdown(ui.section_divider(), unsafe_allow_html=True)
    
    # Enhanced metrics header
    st.markdown(ui.results_header(), unsafe_allow_html=True)
    
    # Summary metrics with animations
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(
            ui.metric_card(icon="▣", title="Total", value=str(results['total'])),
            unsafe_allow_html=True
        )
        
    with col2:
        st.markdown(
            ui.metric_card(
                icon="+",
                title="Positivos",
                value=f"{results['positive_pct']}%",
                delta=f"{results['positive_count']} comentarios",
                card_type="positive"
            ),
            unsafe_allow_html=True
        )
        
    with col3:
        st.markdown(
            ui.metric_card(
                icon="=",
                title="Neutrales",
                value=f"{results['neutral_pct']}%",
                delta=f"{results['neutral_count']} comentarios",
                card_type="neutral"
            ),
            unsafe_allow_html=True
        )
        
    with col4:
        st.markdown(
            ui.metric_card(
                icon="-",
                title="Negativos",
                value=f"{results['negative_pct']}%",
                delta=f"{results['negative_count']} comentarios",
                card_type="negative"
            ),
            unsafe_allow_html=True
        )
    
    # All metric card CSS is now in ui_styling module
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Sentiment distribution bar chart
        fig_bar = go.Figure(data=[
            go.Bar(
                x=['Positivo', 'Neutral', 'Negativo'],
                y=[results['positive_count'], results['neutral_count'], results['negative_count']],
                marker_color=[theme['positive'], theme['neutral'], theme['negative']],
                text=[f"{results['positive_pct']}%", f"{results['neutral_pct']}%", f"{results['negative_pct']}%"],
                textposition='auto'
            )
        ])
        fig_bar.update_layout(
            title="Distribución de Sentimientos",
            height=400,
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            font=dict(color='#a0aec0'),
            showlegend=False,
            margin=dict(l=0, r=0, t=40, b=0)
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        # Pie chart
        fig_pie = go.Figure(data=[go.Pie(
            labels=['Positivo', 'Neutral', 'Negativo'],
            values=[results['positive_count'], results['neutral_count'], results['negative_count']],
            marker_colors=[theme['positive'], theme['neutral'], theme['negative']]
        )])
        fig_pie.update_layout(
            title="Proporción de Sentimientos",
            height=400,
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            font=dict(color='#a0aec0'),
            margin=dict(l=0, r=0, t=40, b=0)
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Themes section
    if any(count > 0 for count in results['theme_counts'].values()):
        st.subheader("Temas Principales")
        theme_col1, theme_col2 = st.columns(2)
        
        with theme_col1:
            for i, (theme, count) in enumerate(results['theme_counts'].items()):
                if count > 0:
                    st.metric(theme.replace('_', ' ').title(), count)
        
        with theme_col2:
            # Theme examples
            for theme, examples in results['theme_examples'].items():
                if examples:
                    with st.expander(f"Ejemplos: {theme.replace('_', ' ').title()}"):
                        for example in examples:
                            st.write(f"- {example}")
    
    # Data quality info
    st.subheader("Información del Procesamiento")
    info_col1, info_col2, info_col3 = st.columns(3)
    
    with info_col1:
        st.metric("Comentarios Originales", results['raw_total'])
    with info_col2:
        st.metric("Duplicados Eliminados", results['duplicates_removed'])
    with info_col3:
        reduction = round((results['duplicates_removed'] / results['raw_total'] * 100), 1) if results['raw_total'] > 0 else 0
        st.metric("Reducción", f"{reduction}%")
    
    # Download section
    st.subheader("Descargar Resultados")
    
    try:
        excel_data = create_simple_excel(results)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"analisis_comentarios_{timestamp}.xlsx"
        
        st.download_button(
            label="Descargar Reporte Excel",
            data=excel_data,
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
            help="Descargar reporte en formato Excel"
        )
    except Exception as e:
        st.error(f"Error creando Excel: {e}")

# Enhanced footer using clean UI component
st.markdown(
    ui.gradient_footer(
        primary_text="Análisis de Comentarios | Personal Paraguay",
        secondary_text="Powered by Advanced Analytics"
    ),
    unsafe_allow_html=True
)