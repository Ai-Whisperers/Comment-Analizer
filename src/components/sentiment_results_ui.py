"""
Sentiment Results UI Component with Spanish translations and OpenAI variables
Enhanced component for displaying comprehensive sentiment analysis results
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Optional, Any
from src.i18n.translations import t, translate_sentiment_data, get_comprehensive_sentiment_labels
import numpy as np

class SentimentResultsUI:
    """Enhanced UI component for sentiment analysis results with Spanish labels"""
    
    def __init__(self):
        """Initialize the sentiment results UI component"""
        self.labels = get_comprehensive_sentiment_labels()
        
        # Spanish color mapping for sentiments
        self.sentiment_colors = {
            'positivo': '#10B981',    # Green
            'positive': '#10B981',
            'neutral': '#F59E0B',     # Amber/Yellow  
            'negativo': '#EF4444',    # Red
            'negative': '#EF4444'
        }
        
        # AI confidence color scale
        self.confidence_colors = {
            'high': '#10B981',      # Green (>80%)
            'medium': '#F59E0B',    # Yellow (60-80%)
            'low': '#EF4444'        # Red (<60%)
        }
    
    def render_comprehensive_results(self, results: Dict[str, Any]):
        """
        Render comprehensive sentiment analysis results with Spanish labels
        
        Args:
            results: Analysis results dictionary from AI adapter or fallback
        """
        if not results:
            st.warning("⚠️ No hay resultados de análisis disponibles")
            return
        
        # Render header with analysis method indicator
        self._render_analysis_header(results)
        
        # Main sentiment overview
        self._render_sentiment_overview(results)
        
        # AI-enhanced details if available
        if results.get('analysis_method') == 'AI_POWERED':
            self._render_ai_enhanced_section(results)
        
        # Detailed sentiment breakdown
        self._render_detailed_breakdown(results)
        
        # Export options
        self._render_export_options(results)
    
    def _render_analysis_header(self, results: Dict[str, Any]):
        """Render header with analysis method and quality indicators"""
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown("## 📊 Análisis de Sentimientos")
            
        with col2:
            # Analysis method indicator
            method = results.get('analysis_method', 'UNKNOWN')
            if method == 'AI_POWERED':
                st.success("🤖 Con IA")
                model = results.get('ai_model_used', 'N/A')
                st.caption(f"Modelo: {model}")
            elif method == 'RULE_BASED_FALLBACK':
                st.info("📋 Basado en Reglas")
            else:
                st.warning("❓ Método Desconocido")
        
        with col3:
            # AI confidence if available
            if results.get('analysis_method') == 'AI_POWERED':
                ai_confidence = results.get('ai_confidence_avg', 0)
                confidence_pct = ai_confidence * 100
                
                if confidence_pct >= 80:
                    st.success(f"🎯 Confianza: {confidence_pct:.1f}%")
                elif confidence_pct >= 60:
                    st.warning(f"⚡ Confianza: {confidence_pct:.1f}%")
                else:
                    st.error(f"⚠️ Confianza: {confidence_pct:.1f}%")
        
        st.markdown("---")
    
    def _render_sentiment_overview(self, results: Dict[str, Any]):
        """Render main sentiment overview with Spanish labels"""
        # Main metrics
        col1, col2, col3, col4 = st.columns(4)
        
        total = results.get('total', 0)
        positive_count = results.get('positive_count', 0)
        neutral_count = results.get('neutral_count', 0)
        negative_count = results.get('negative_count', 0)
        
        positive_pct = results.get('positive_pct', 0)
        neutral_pct = results.get('neutral_pct', 0)
        negative_pct = results.get('negative_pct', 0)
        
        with col1:
            st.metric(
                label="Total de Comentarios",
                value=total,
                help="Número total de comentarios analizados"
            )
        
        with col2:
            st.metric(
                label="Positivos",
                value=f"{positive_count} ({positive_pct:.1f}%)",
                delta=f"+{positive_pct:.1f}%",
                delta_color="normal" if positive_pct > 0 else "off"
            )
        
        with col3:
            st.metric(
                label="Neutrales", 
                value=f"{neutral_count} ({neutral_pct:.1f}%)",
                help="Comentarios sin sentimiento claro"
            )
        
        with col4:
            st.metric(
                label="Negativos",
                value=f"{negative_count} ({negative_pct:.1f}%)",
                delta=f"-{negative_pct:.1f}%",
                delta_color="inverse" if negative_pct > 0 else "off"
            )
        
        # Visualizations
        self._render_sentiment_charts(results)
    
    def _render_sentiment_charts(self, results: Dict[str, Any]):
        """Render sentiment analysis charts with Spanish labels"""
        col1, col2 = st.columns(2)
        
        # Data for charts
        sentiments = ['Positivo', 'Neutral', 'Negativo']
        counts = [
            results.get('positive_count', 0),
            results.get('neutral_count', 0), 
            results.get('negative_count', 0)
        ]
        percentages = [
            results.get('positive_pct', 0),
            results.get('neutral_pct', 0),
            results.get('negative_pct', 0)
        ]
        colors = [self.sentiment_colors['positivo'], self.sentiment_colors['neutral'], self.sentiment_colors['negativo']]
        
        with col1:
            # Bar chart
            fig_bar = go.Figure(data=[
                go.Bar(
                    x=sentiments,
                    y=counts,
                    marker_color=colors,
                    text=[f"{pct:.1f}%" for pct in percentages],
                    textposition='auto',
                    hovertemplate='<b>%{x}</b><br>Cantidad: %{y}<br>Porcentaje: %{text}<extra></extra>'
                )
            ])
            fig_bar.update_layout(
                title="Distribución de Sentimientos",
                xaxis_title="Tipo de Sentimiento",
                yaxis_title="Cantidad de Comentarios",
                height=400,
                showlegend=False
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        
        with col2:
            # Pie chart  
            fig_pie = go.Figure(data=[go.Pie(
                labels=sentiments,
                values=counts,
                marker_colors=colors,
                hovertemplate='<b>%{label}</b><br>Cantidad: %{value}<br>Porcentaje: %{percent}<extra></extra>'
            )])
            fig_pie.update_layout(
                title="Proporción de Sentimientos",
                height=400
            )
            st.plotly_chart(fig_pie, use_container_width=True)
    
    def _render_ai_enhanced_section(self, results: Dict[str, Any]):
        """Render AI-enhanced analysis section"""
        st.markdown("### 🤖 Análisis Mejorado con IA")
        
        # Create tabs for different AI insights
        tab1, tab2, tab3, tab4 = st.tabs(["Temas", "Emociones", "Puntos de Dolor", "Calidad"])
        
        with tab1:
            self._render_themes_analysis(results)
        
        with tab2:
            self._render_emotions_analysis(results)
        
        with tab3:
            self._render_pain_points_analysis(results)
        
        with tab4:
            self._render_quality_analysis(results)
    
    def _render_themes_analysis(self, results: Dict[str, Any]):
        """Render themes analysis with Spanish labels"""
        theme_counts = results.get('theme_counts', {})
        
        if not theme_counts:
            st.info("📝 No se encontraron temas específicos")
            return
        
        # Convert themes to Spanish and sort by frequency
        spanish_themes = {}
        for theme, count in theme_counts.items():
            spanish_theme = t(theme, theme.replace('_', ' ').title())
            spanish_themes[spanish_theme] = count
        
        # Display top themes
        sorted_themes = sorted(spanish_themes.items(), key=lambda x: x[1], reverse=True)[:10]
        
        if sorted_themes:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Temas Más Mencionados:**")
                for theme, count in sorted_themes[:5]:
                    percentage = (count / results.get('total', 1)) * 100
                    st.markdown(f"• **{theme}**: {count} menciones ({percentage:.1f}%)")
            
            with col2:
                # Themes chart
                themes, counts = zip(*sorted_themes) if sorted_themes else ([], [])
                fig_themes = px.bar(
                    x=list(counts)[:5], 
                    y=list(themes)[:5],
                    orientation='h',
                    title="Top 5 Temas",
                    labels={'x': 'Frecuencia', 'y': 'Tema'}
                )
                fig_themes.update_layout(height=300)
                st.plotly_chart(fig_themes, use_container_width=True)
    
    def _render_emotions_analysis(self, results: Dict[str, Any]):
        """Render emotions analysis with Spanish labels"""
        emotion_summary = results.get('emotion_summary', {})
        
        if not emotion_summary:
            st.info("😐 No hay datos de análisis emocional disponibles")
            return
        
        emotion_dist = emotion_summary.get('distribution', {})
        avg_intensity = emotion_summary.get('avg_intensity', 0)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(
                label="Intensidad Emocional Promedio",
                value=f"{avg_intensity:.1f}/5.0",
                help="Intensidad promedio de las emociones detectadas"
            )
            
            st.markdown("**Emociones Detectadas:**")
            for emotion, count in sorted(emotion_dist.items(), key=lambda x: x[1], reverse=True):
                spanish_emotion = t(emotion, emotion.title())
                percentage = (count / sum(emotion_dist.values())) * 100
                st.markdown(f"• **{spanish_emotion}**: {count} ({percentage:.1f}%)")
        
        with col2:
            if emotion_dist:
                # Emotions pie chart
                emotions = [t(em, em.title()) for em in emotion_dist.keys()]
                counts = list(emotion_dist.values())
                
                fig_emotions = px.pie(
                    values=counts,
                    names=emotions,
                    title="Distribución de Emociones"
                )
                st.plotly_chart(fig_emotions, use_container_width=True)
    
    def _render_pain_points_analysis(self, results: Dict[str, Any]):
        """Render pain points analysis"""
        churn_analysis = results.get('churn_analysis', {})
        
        if not churn_analysis:
            st.info("⚠️ No hay análisis de puntos de dolor disponible")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Riesgo de Cancelación:**")
            high_risk = churn_analysis.get('high_risk', 0)
            medium_risk = churn_analysis.get('medium_risk', 0)
            low_risk = churn_analysis.get('low_risk', 0)
            
            st.error(f"🔴 Alto Riesgo: {high_risk} clientes")
            st.warning(f"🟡 Riesgo Medio: {medium_risk} clientes")
            st.success(f"🟢 Bajo Riesgo: {low_risk} clientes")
        
        with col2:
            # Risk distribution chart
            risk_data = {
                'Nivel de Riesgo': ['Alto', 'Medio', 'Bajo'],
                'Cantidad': [high_risk, medium_risk, low_risk]
            }
            df_risk = pd.DataFrame(risk_data)
            
            if df_risk['Cantidad'].sum() > 0:
                fig_risk = px.bar(
                    df_risk, 
                    x='Nivel de Riesgo', 
                    y='Cantidad',
                    color='Nivel de Riesgo',
                    color_discrete_map={
                        'Alto': '#EF4444',
                        'Medio': '#F59E0B', 
                        'Bajo': '#10B981'
                    },
                    title="Distribución de Riesgo de Cancelación"
                )
                st.plotly_chart(fig_risk, use_container_width=True)
    
    def _render_quality_analysis(self, results: Dict[str, Any]):
        """Render comment quality analysis"""
        quality_summary = results.get('comment_quality_summary', {})
        informative_count = results.get('informative_comments', 0)
        total = results.get('total', 1)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(
                label="Comentarios Informativos",
                value=f"{informative_count}/{total}",
                delta=f"{(informative_count/total)*100:.1f}%",
                help="Comentarios que proporcionan información útil"
            )
            
            if quality_summary:
                st.markdown("**Distribución de Calidad:**")
                for quality, count in quality_summary.items():
                    spanish_quality = t(f"{quality}_quality", quality.title())
                    percentage = (count / total) * 100
                    st.markdown(f"• **{spanish_quality}**: {count} ({percentage:.1f}%)")
        
        with col2:
            if quality_summary:
                # Quality distribution chart
                qualities = [t(f"{q}_quality", q.title()) for q in quality_summary.keys()]
                counts = list(quality_summary.values())
                
                fig_quality = px.pie(
                    values=counts,
                    names=qualities,
                    title="Distribución de Calidad de Comentarios"
                )
                st.plotly_chart(fig_quality, use_container_width=True)
    
    def _render_detailed_breakdown(self, results: Dict[str, Any]):
        """Render detailed comment breakdown table"""
        if not results.get('comments') or not results.get('sentiments'):
            return
        
        st.markdown("### 📋 Desglose Detallado de Comentarios")
        
        # Prepare data for table
        comments = results.get('comments', [])[:100]  # Limit for performance
        sentiments = results.get('sentiments', [])[:100]
        
        table_data = []
        for i, (comment, sentiment) in enumerate(zip(comments, sentiments)):
            # Translate sentiment to Spanish
            sentiment_es = t(sentiment, sentiment.title())
            
            row = {
                'ID': f'C{i+1:04d}',
                'Comentario': comment[:100] + '...' if len(comment) > 100 else comment,
                'Sentimiento': sentiment_es,
                'Longitud': len(comment)
            }
            
            # Add AI data if available
            if results.get('analysis_method') == 'AI_POWERED':
                enhanced_results = results.get('enhanced_results', [])
                if i < len(enhanced_results):
                    enhanced = enhanced_results[i]
                    
                    # Extract themes
                    themes = list(enhanced.get('extended_themes', {}).keys())[:2]
                    row['Temas'] = ', '.join([t(theme, theme.replace('_', ' ').title()) for theme in themes]) if themes else 'N/A'
                    
                    # Extract emotions
                    emotions = enhanced.get('emotions', {}).get('detected', [])[:2]
                    row['Emociones'] = ', '.join([t(emotion, emotion.title()) for emotion in emotions]) if emotions else 'N/A'
            
            table_data.append(row)
        
        # Display table
        df_table = pd.DataFrame(table_data)
        
        # Color-code sentiments
        def color_sentiment(val):
            if val == 'Positivo':
                return 'background-color: rgba(16, 185, 129, 0.1)'
            elif val == 'Negativo':
                return 'background-color: rgba(239, 68, 68, 0.1)'
            else:
                return 'background-color: rgba(245, 158, 11, 0.1)'
        
        styled_df = df_table.style.applymap(color_sentiment, subset=['Sentimiento'])
        st.dataframe(styled_df, use_container_width=True, height=400)
    
    def _render_export_options(self, results: Dict[str, Any]):
        """Render export options with Spanish labels"""
        st.markdown("### 📥 Opciones de Exportación")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 Excel Completo", use_container_width=True):
                # Trigger professional Excel export
                st.session_state['export_type'] = 'professional'
                st.success("✅ Generando Excel profesional...")
        
        with col2:
            if st.button("📋 Excel Simple", use_container_width=True):
                # Trigger simple Excel export
                st.session_state['export_type'] = 'simple'
                st.success("✅ Generando Excel simple...")
        
        with col3:
            if st.button("📄 Reporte PDF", use_container_width=True):
                st.info("🚧 Próximamente disponible")
    
    def render_ai_confidence_indicator(self, confidence: float) -> str:
        """
        Render AI confidence indicator with appropriate styling
        
        Args:
            confidence: Confidence score (0.0 to 1.0)
            
        Returns:
            HTML string with styled confidence indicator
        """
        confidence_pct = confidence * 100
        
        if confidence_pct >= 80:
            color = self.confidence_colors['high']
            icon = "🎯"
            level = "Alta"
        elif confidence_pct >= 60:
            color = self.confidence_colors['medium']
            icon = "⚡"
            level = "Media"
        else:
            color = self.confidence_colors['low']
            icon = "⚠️"
            level = "Baja"
        
        return f"""
        <div style="
            display: inline-flex;
            align-items: center;
            background-color: {color}20;
            color: {color};
            padding: 4px 8px;
            border-radius: 16px;
            font-size: 12px;
            font-weight: bold;
        ">
            {icon} {level} ({confidence_pct:.1f}%)
        </div>
        """


# Global instance for easy access
sentiment_ui = SentimentResultsUI()

def render_sentiment_results(results: Dict[str, Any]):
    """Convenience function to render sentiment results"""
    return sentiment_ui.render_comprehensive_results(results)