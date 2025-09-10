"""
Chart Generation Component - Streamlit Native Caching
All visualization functions cached for instant regeneration
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)


@st.cache_data(ttl=600, show_spinner="Generando gráficos...")
def create_analysis_dashboard(analysis_data: Dict[str, Any]) -> Dict[str, go.Figure]:
    """
    Create complete analysis dashboard with single Streamlit cache operation
    
    Cache Strategy:
    - TTL: 10 minutes (charts don't change frequently)
    - Single cache operation for all charts (more efficient)
    - Automatic invalidation when analysis data changes
    
    Replaces: 7 individual chart functions with manual regeneration
    Benefits: Instant chart display for same analysis data
    """
    if not analysis_data:
        logger.warning("⚠️ No analysis data provided for dashboard")
        return {}
    
    logger.info("📊 Creating cached analysis dashboard")
    
    charts = {}
    
    try:
        # Extract data with fallbacks for different result formats
        sentiments = analysis_data.get('distribution', {}).get('sentiments', {})
        
        # Generate all charts in single cached operation
        charts['sentiment_chart'] = create_sentiment_pie(sentiments)
        
        # Additional charts based on available data
        if 'emotions' in analysis_data:
            charts['emotion_chart'] = create_emotion_donut(analysis_data['emotions'])
        
        if 'themes' in analysis_data:
            charts['theme_chart'] = create_theme_bar(analysis_data['themes'])
            
        # Metrics gauges
        charts['metrics_gauge'] = create_metrics_dashboard(analysis_data)
        
        logger.info(f"✅ Dashboard created with {len(charts)} charts")
        return charts
        
    except Exception as e:
        logger.error(f"❌ Error creating dashboard: {str(e)}")
        return {'error_chart': create_error_chart(str(e))}


@st.cache_data(ttl=600)
def create_sentiment_pie(sentiment_data: Dict[str, int]) -> go.Figure:
    """
    Cached sentiment pie chart generation
    Optimized colors and styling for Streamlit theme integration
    """
    if not sentiment_data:
        return create_empty_chart("Sin datos de sentimientos")
    
    # Normalize keys for different data formats
    positive = sentiment_data.get('positivo', sentiment_data.get('positive', 0))
    neutral = sentiment_data.get('neutral', 0)  
    negative = sentiment_data.get('negativo', sentiment_data.get('negative', 0))
    
    if positive + neutral + negative == 0:
        return create_empty_chart("Sin análisis de sentimientos")
    
    # Create pie chart with optimized styling
    fig = go.Figure(data=[go.Pie(
        labels=['Positivo', 'Neutral', 'Negativo'],
        values=[positive, neutral, negative],
        hole=0.4,
        marker=dict(
            colors=['#10B981', '#6B7280', '#EF4444'],  # Green, Gray, Red
            line=dict(color='rgba(255,255,255,0.2)', width=2)
        )
    )])
    
    fig.update_layout(
        title="📊 Distribución de Sentimientos",
        font=dict(family="Arial, sans-serif", size=12),
        showlegend=True,
        height=400,
        margin=dict(t=40, b=20, l=20, r=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig


@st.cache_data(ttl=600)
def create_emotion_donut(emotion_data: Dict[str, float]) -> go.Figure:
    """Cached emotion donut chart with glassmorphism styling"""
    if not emotion_data:
        return create_empty_chart("Sin datos de emociones")
    
    # Sort emotions by intensity
    sorted_emotions = sorted(emotion_data.items(), key=lambda x: x[1], reverse=True)
    top_emotions = sorted_emotions[:8]  # Show top 8 emotions
    
    labels, values = zip(*top_emotions) if top_emotions else ([], [])
    
    # Emotion color mapping
    emotion_colors = {
        'alegría': '#FFD700',
        'satisfacción': '#32CD32', 
        'frustración': '#FF6B6B',
        'enojo': '#DC143C',
        'confusión': '#8A2BE2',
        'decepción': '#FF8C00',
        'preocupación': '#4682B4',
        'neutral': '#708090'
    }
    
    colors = [emotion_colors.get(emotion, '#708090') for emotion in labels]
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.6,
        marker=dict(colors=colors, line=dict(color='rgba(255,255,255,0.3)', width=2))
    )])
    
    fig.update_layout(
        title="😊 Emociones Predominantes",
        height=400,
        font=dict(family="Arial, sans-serif", size=12),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig


@st.cache_data(ttl=600)  
def create_theme_bar(theme_data: Dict[str, float]) -> go.Figure:
    """Cached theme bar chart with professional styling"""
    if not theme_data:
        return create_empty_chart("Sin datos de temas")
    
    # Sort themes by relevance
    sorted_themes = sorted(theme_data.items(), key=lambda x: x[1], reverse=True)
    themes, relevance = zip(*sorted_themes) if sorted_themes else ([], [])
    
    fig = go.Figure(data=[go.Bar(
        x=list(themes),
        y=list(relevance),
        marker=dict(
            color=list(relevance),
            colorscale='Viridis',
            line=dict(color='rgba(255,255,255,0.3)', width=1)
        ),
        text=[f"{val:.1f}" for val in relevance],
        textposition='auto'
    )])
    
    fig.update_layout(
        title="🎯 Temas Más Relevantes",
        xaxis_title="Temas",
        yaxis_title="Relevancia",
        height=400,
        font=dict(family="Arial, sans-serif", size=12),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig


@st.cache_data(ttl=300)
def create_metrics_dashboard(analysis_data: Dict[str, Any]) -> go.Figure:
    """
    Create metrics gauge dashboard with caching
    Shorter TTL since metrics are lightweight and may update more frequently
    """
    metadata = analysis_data.get('metadata', {})
    summary = analysis_data.get('summary', {})
    
    # Create multi-gauge dashboard
    fig = make_subplots(
        rows=2, cols=2,
        specs=[[{"type": "indicator"}, {"type": "indicator"}],
               [{"type": "indicator"}, {"type": "indicator"}]],
        subplot_titles=("Confianza General", "Lotes Procesados", 
                       "Eficiencia", "Performance")
    )
    
    # Confidence gauge
    confidence = summary.get('confidence', 0.5) * 100
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=confidence,
        title={'text': "Confianza %"},
        gauge={'axis': {'range': [None, 100]},
               'bar': {'color': "darkgreen"},
               'steps': [{'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 80], 'color': "yellow"},
                        {'range': [80, 100], 'color': "green"}]},
        domain={'x': [0, 0.5], 'y': [0.5, 1]}
    ), row=1, col=1)
    
    # Batches processed gauge  
    total_batches = metadata.get('total_batches_processed', 0)
    fig.add_trace(go.Indicator(
        mode="number",
        value=total_batches,
        title={'text': "Lotes"},
        domain={'x': [0.5, 1], 'y': [0.5, 1]}
    ), row=1, col=2)
    
    # Efficiency gauge (comments per batch)
    total_comments = summary.get('total_comments', 0)
    efficiency = total_comments / total_batches if total_batches > 0 else 0
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=efficiency,
        title={'text': "Comentarios/Lote"},
        gauge={'axis': {'range': [0, 100]},
               'bar': {'color': "blue"}},
        domain={'x': [0, 0.5], 'y': [0, 0.5]}
    ), row=2, col=1)
    
    # Performance indicator (synthetic metric)
    cache_enabled = metadata.get('cache_enabled', False)
    processing_method = metadata.get('processing_method', 'unknown')
    performance_score = 85 if cache_enabled and 'optimized' in processing_method else 60
    
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=performance_score,
        title={'text': "Performance Score"},
        gauge={'axis': {'range': [0, 100]},
               'bar': {'color': "purple"}},
        domain={'x': [0.5, 1], 'y': [0, 0.5]}
    ), row=2, col=2)
    
    fig.update_layout(
        title="📈 Métricas de Análisis",
        height=500,
        font=dict(family="Arial, sans-serif", size=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig


def create_empty_chart(message: str) -> go.Figure:
    """Create empty chart with message for missing data"""
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        xref="paper", yref="paper",
        x=0.5, y=0.5, 
        xanchor='center', yanchor='middle',
        font=dict(size=16, color="gray")
    )
    fig.update_layout(
        title="📊 Gráfico No Disponible",
        height=300,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig


def create_error_chart(error_message: str) -> go.Figure:
    """Create error chart for failed chart generation"""
    fig = go.Figure()
    fig.add_annotation(
        text=f"❌ Error generando gráfico:\n{error_message}",
        xref="paper", yref="paper",
        x=0.5, y=0.5,
        xanchor='center', yanchor='middle', 
        font=dict(size=14, color="red")
    )
    fig.update_layout(
        title="❌ Error en Visualización",
        height=300,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig


@st.cache_data(ttl=1800)
def prepare_chart_data_optimized(raw_analysis: Dict[str, Any]) -> Dict[str, Any]:
    """
    Prepare analysis data for chart consumption with Streamlit caching
    
    Cache Strategy:
    - TTL: 30 minutes (data preparation is expensive)  
    - Transforms raw AI results into chart-ready format
    - Cached separately for flexibility in chart generation
    """
    if not raw_analysis:
        return {}
    
    chart_data = {
        'sentiments': {},
        'emotions': {},
        'themes': {},
        'metrics': {}
    }
    
    # Extract sentiment distribution
    if 'distribution' in raw_analysis:
        sentiments = raw_analysis['distribution'].get('sentiments', {})
        chart_data['sentiments'] = sentiments
    
    # Extract emotion data from individual comments
    comments = raw_analysis.get('comments', [])
    emotion_counts = {}
    theme_counts = {}
    
    for comment in comments:
        # Aggregate emotions
        emotion = comment.get('emotion', 'neutral')
        emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        # Aggregate themes  
        theme = comment.get('theme', 'unknown')
        theme_counts[theme] = theme_counts.get(theme, 0) + 1
    
    chart_data['emotions'] = emotion_counts
    chart_data['themes'] = theme_counts
    
    # Prepare metrics
    chart_data['metrics'] = {
        'total_comments': len(comments),
        'avg_confidence': sum(c.get('confidence', 0.5) for c in comments) / len(comments) if comments else 0.5,
        'processing_metadata': raw_analysis.get('metadata', {})
    }
    
    logger.info(f"📊 Chart data prepared for {len(comments)} comments")
    return chart_data