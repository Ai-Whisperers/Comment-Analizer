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
        
        return {
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
    """Create Excel report with analysis results"""
    output = BytesIO()
    
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        # Sheet 1: Summary
        summary_data = {
            'Métrica': ['Total Comentarios', 'Positivos', 'Neutrales', 'Negativos', 'Duplicados Eliminados'],
            'Valor': [results['total'], f"{results['positive_pct']}%", f"{results['neutral_pct']}%", 
                     f"{results['negative_pct']}%", results['duplicates_removed']],
            'Cantidad': [results['total'], results['positive_count'], results['neutral_count'],
                        results['negative_count'], results['duplicates_removed']]
        }
        pd.DataFrame(summary_data).to_excel(writer, sheet_name='Resumen', index=False)
        
        # Sheet 2: Comments with sentiment
        comments_data = {
            'Comentario': results['comments'][:500],
            'Sentimiento': results['sentiments'][:500],
            'Frecuencia': [results['comment_frequencies'].get(c, 1) for c in results['comments'][:500]]
        }
        pd.DataFrame(comments_data).to_excel(writer, sheet_name='Comentarios', index=False)
        
        # Sheet 3: Themes
        if results['theme_counts']:
            themes_data = {
                'Tema': list(results['theme_counts'].keys()),
                'Cantidad': list(results['theme_counts'].values())
            }
            pd.DataFrame(themes_data).to_excel(writer, sheet_name='Temas', index=False)
    
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