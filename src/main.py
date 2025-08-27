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


# Page config
st.set_page_config(
    page_title="Personal Paraguay — Análisis de Comentarios",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS styles
st.markdown("""
<style>
    .main { padding: 1rem; }
    .metric-card {
        background: linear-gradient(135deg, #1e2a3a 0%, #2d3748 100%);
        padding: 1rem; margin: 0.5rem; border-radius: 10px;
        border-left: 4px solid #4299e1; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .metric-value { font-size: 2rem; font-weight: bold; }
    .metric-label { color: #a0aec0; font-size: 0.875rem; margin-bottom: 0.25rem; }
    .progress-bar { width: 100%; height: 4px; background: #2d3748; border-radius: 2px; margin-top: 0.5rem; }
    .progress-fill { height: 100%; border-radius: 2px; transition: width 0.3s ease; }
</style>
""", unsafe_allow_html=True)

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

# Main UI
st.title("🔬 Análisis de Comentarios - Personal Paraguay")
st.markdown("*Análisis de sentimientos*")

# Upload section
uploaded_file = st.file_uploader(
    "📁 Subir archivo de comentarios",
    type=['csv', 'xlsx', 'xls'],
    help="Sube un archivo Excel o CSV con comentarios de clientes"
)

# Analysis button
if uploaded_file:
    st.info(f"📄 Archivo cargado: {uploaded_file.name}")
    
    if st.button("🚀 Analizar Comentarios", type="primary", use_container_width=True):
        with st.spinner("Procesando comentarios..."):
            results = process_file_simple(uploaded_file)
            if results:
                st.session_state.analysis_results = results
                st.success("✅ Análisis completado!")
                st.rerun()

# Results display
if st.session_state.analysis_results:
    results = st.session_state.analysis_results
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📊 Total", results['total'])
    with col2:
        st.metric("😊 Positivos", f"{results['positive_pct']}%", 
                 delta=f"{results['positive_count']} comentarios")
    with col3:
        st.metric("😐 Neutrales", f"{results['neutral_pct']}%",
                 delta=f"{results['neutral_count']} comentarios")
    with col4:
        st.metric("😞 Negativos", f"{results['negative_pct']}%",
                 delta=f"{results['negative_count']} comentarios")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Sentiment distribution bar chart
        fig_bar = go.Figure(data=[
            go.Bar(
                x=['Positivo', 'Neutral', 'Negativo'],
                y=[results['positive_count'], results['neutral_count'], results['negative_count']],
                marker_color=['#10b981', '#f59e0b', '#ef4444'],
                text=[f"{results['positive_pct']}%", f"{results['neutral_pct']}%", f"{results['negative_pct']}%"],
                textposition='auto'
            )
        ])
        fig_bar.update_layout(title="Distribución de Sentimientos", height=400)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        # Pie chart
        fig_pie = go.Figure(data=[go.Pie(
            labels=['Positivo', 'Neutral', 'Negativo'],
            values=[results['positive_count'], results['neutral_count'], results['negative_count']],
            marker_colors=['#10b981', '#f59e0b', '#ef4444']
        )])
        fig_pie.update_layout(title="Proporción de Sentimientos", height=400)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Themes section
    if any(count > 0 for count in results['theme_counts'].values()):
        st.subheader("📋 Temas Principales")
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
                            st.write(f"• {example}")
    
    # Data quality info
    st.subheader("📈 Información del Procesamiento")
    info_col1, info_col2, info_col3 = st.columns(3)
    
    with info_col1:
        st.metric("📄 Comentarios Originales", results['raw_total'])
    with info_col2:
        st.metric("🗑️ Duplicados Eliminados", results['duplicates_removed'])
    with info_col3:
        reduction = round((results['duplicates_removed'] / results['raw_total'] * 100), 1) if results['raw_total'] > 0 else 0
        st.metric("📉 Reducción", f"{reduction}%")
    
    # Download section
    st.subheader("📥 Descargar Resultados")
    
    try:
        excel_data = create_simple_excel(results)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"analisis_comentarios_{timestamp}.xlsx"
        
        st.download_button(
            label="📊 Descargar Reporte Excel",
            data=excel_data,
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
            help="Descargar reporte en formato Excel"
        )
    except Exception as e:
        st.error(f"Error creando Excel: {e}")

# Footer
st.markdown("---")
st.markdown("*Análisis de comentarios - Personal Paraguay*")