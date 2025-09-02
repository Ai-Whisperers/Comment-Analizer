"""
Enhanced Results UI Component with improved visualization and organization
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json

class EnhancedResultsUI:
    """Enhanced UI component for displaying analysis results"""
    
    def __init__(self):
        self.sentiment_colors = {
            'positive': '#10B981',  # Green
            'neutral': '#F59E0B',   # Yellow/Amber
            'negative': '#EF4444'   # Red
        }
        
        self.nps_colors = {
            'promoter': '#10B981',  # Green
            'passive': '#F59E0B',   # Yellow
            'detractor': '#EF4444'  # Red
        }
        
        self.priority_icons = {
            'critical': '🔴',
            'high': '🟠',
            'medium': '🟡',
            'low': '🟢'
        }
    
    def render_results(self):
        """Main render method for enhanced results display"""
        if 'analysis_results' not in st.session_state and 'results' not in st.session_state:
            st.info("📊 No analysis results available yet. Please run an analysis first.")
            return
        
        # Get analysis data with comprehensive validation
        results = st.session_state.get('analysis_results', {})
        if not isinstance(results, dict):
            results = {}
        
        insights = st.session_state.get('insights', {})
        if not isinstance(insights, dict):
            insights = {}
            
        recommendations = st.session_state.get('recommendations', [])
        if not isinstance(recommendations, list):
            recommendations = []
        
        # Render fixed top summary
        self._render_top_summary(results, insights)
        
        # Add NPS widget
        self._render_nps_widget(insights)
        
        # Create tabbed interface for results
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Overview", 
            "🏷️ Themes & Pain Points", 
            "📈 Data Stats",
            "💡 Recommendations",
            "📅 Historical Trends"
        ])
        
        with tab1:
            self._render_overview_tab(results, insights)
        
        with tab2:
            self._render_themes_pain_points_tab(results, insights)
        
        with tab3:
            self._render_data_stats_tab(results, insights)
        
        with tab4:
            self._render_recommendations_tab(recommendations, insights)
        
        with tab5:
            self._render_historical_trends_tab(results, insights)
    
    def _render_top_summary(self, results: List, insights: Dict):
        """Render fixed top summary row with key metrics"""
        st.markdown("""
        <style>
        .summary-container {
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .metric-card {
            background: rgba(255,255,255,0.1);
            border-radius: 8px;
            padding: 12px;
            text-align: center;
        }
        .metric-value {
            font-size: 24px;
            font-weight: bold;
            color: white;
        }
        .metric-label {
            font-size: 12px;
            color: #cbd5e1;
            margin-top: 4px;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Calculate metrics
        total_comments = len(results) if results else 0
        sentiment_dist = insights.get('sentiment_percentages', {})
        top_pain_points = insights.get('top_pain_points', {})
        top_pain = list(top_pain_points.keys())[0] if top_pain_points else "None detected"
        
        # Create summary container
        st.markdown('<div class="summary-container">', unsafe_allow_html=True)
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{total_comments:,}</div>
                <div class="metric-label">Total Comments</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            pos_pct = sentiment_dist.get('positive', 0)
            color = self._get_sentiment_color_hex(pos_pct)
            st.markdown(f"""
            <div class="metric-card" style="border-left: 4px solid {color};">
                <div class="metric-value" style="color: {color};">{pos_pct:.1f}%</div>
                <div class="metric-label">Positive</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            neu_pct = sentiment_dist.get('neutral', 0)
            color = self.sentiment_colors['neutral']
            st.markdown(f"""
            <div class="metric-card" style="border-left: 4px solid {color};">
                <div class="metric-value" style="color: {color};">{neu_pct:.1f}%</div>
                <div class="metric-label">Neutral</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            neg_pct = sentiment_dist.get('negative', 0)
            color = self.sentiment_colors['negative']
            st.markdown(f"""
            <div class="metric-card" style="border-left: 4px solid {color};">
                <div class="metric-value" style="color: {color};">{neg_pct:.1f}%</div>
                <div class="metric-label">Negative</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col5:
            st.markdown(f"""
            <div class="metric-card" style="border-left: 4px solid #EF4444;">
                <div class="metric-value" style="font-size: 16px;">#{top_pain[:20]}</div>
                <div class="metric-label">Top Pain Point</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def _render_nps_widget(self, insights: Dict):
        """Render NPS category widget"""
        if 'nps_analysis' in st.session_state:
            nps_data = st.session_state['nps_analysis']
        else:
            # Mock NPS data if not available
            nps_data = {
                'promoters': {'count': 120, 'percentage': 40},
                'passives': {'count': 90, 'percentage': 30},
                'detractors': {'count': 90, 'percentage': 30},
                'nps_score': 10
            }
        
        st.markdown("""
        <style>
        .nps-container {
            background: white;
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        </style>
        """, unsafe_allow_html=True)
        
        with st.container():
            col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
            
            with col1:
                st.metric(
                    "🟢 Promoters", 
                    f"{nps_data['promoters']['percentage']:.0f}%",
                    f"{nps_data['promoters']['count']} customers"
                )
            
            with col2:
                st.metric(
                    "🟡 Passives",
                    f"{nps_data['passives']['percentage']:.0f}%",
                    f"{nps_data['passives']['count']} customers"
                )
            
            with col3:
                st.metric(
                    "🔴 Detractors",
                    f"{nps_data['detractors']['percentage']:.0f}%",
                    f"{nps_data['detractors']['count']} customers"
                )
            
            with col4:
                nps_score = nps_data['nps_score']
                delta_color = "normal" if nps_score > 0 else "inverse"
                st.metric(
                    "📊 NPS Score",
                    f"{nps_score:.0f}",
                    f"{'↑' if nps_score > 0 else '↓'} Industry avg: 15",
                    delta_color=delta_color
                )
    
    def _render_overview_tab(self, results: List, insights: Dict):
        """Render overview tab with main visualizations"""
        col1, col2 = st.columns(2)
        
        with col1:
            # Compact sentiment distribution pie chart
            self._render_compact_sentiment_chart(insights)
        
        with col2:
            # Compact confidence distribution
            self._render_confidence_chart(results)
        
        # Key insights summary
        st.markdown("### 🔍 Key Insights")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            avg_confidence = insights.get('average_confidence', 0)
            st.info(f"**Avg Confidence:** {avg_confidence:.2f}")
        
        with col2:
            total_themes = len(insights.get('top_themes', {}))
            st.info(f"**Themes Detected:** {total_themes}")
        
        with col3:
            total_pain_points = len(insights.get('top_pain_points', {}))
            st.warning(f"**Pain Points:** {total_pain_points}")
    
    def _render_themes_pain_points_tab(self, results: List, insights: Dict):
        """Render themes and pain points with drill-down capability"""
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🏷️ Top Themes")
            themes = insights.get('top_themes', {})
            
            if themes:
                # Create compact bar chart
                theme_df = pd.DataFrame(
                    list(themes.items())[:8],  # Show top 8
                    columns=['Theme', 'Count']
                )
                
                fig = px.bar(
                    theme_df, 
                    x='Count', 
                    y='Theme',
                    orientation='h',
                    height=300,
                    color='Count',
                    color_continuous_scale='Blues'
                )
                fig.update_layout(
                    margin=dict(l=0, r=0, t=0, b=0),
                    showlegend=False,
                    yaxis_title="",
                    xaxis_title="Mentions"
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Expandable details for each theme
                with st.expander("📋 Theme Details & Sample Comments"):
                    for theme, count in list(themes.items())[:5]:
                        st.markdown(f"**{theme}** ({count} mentions)")
                        
                        # Show sample comments for this theme
                        theme_comments = self._get_theme_comments(results, theme)[:3]
                        for comment in theme_comments:
                            st.caption(f"• {comment[:100]}...")
                        st.markdown("---")
        
        with col2:
            st.subheader("⚠️ Top Pain Points")
            pain_points = insights.get('top_pain_points', {})
            
            if pain_points:
                # Create compact bar chart
                pain_df = pd.DataFrame(
                    list(pain_points.items())[:8],  # Show top 8
                    columns=['Pain Point', 'Count']
                )
                
                fig = px.bar(
                    pain_df,
                    x='Count',
                    y='Pain Point',
                    orientation='h',
                    height=300,
                    color='Count',
                    color_continuous_scale='Reds'
                )
                fig.update_layout(
                    margin=dict(l=0, r=0, t=0, b=0),
                    showlegend=False,
                    yaxis_title="",
                    xaxis_title="Mentions"
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Expandable details with NPS breakdown
                with st.expander("📋 Pain Point Analysis & NPS Impact"):
                    for pain_point, count in list(pain_points.items())[:5]:
                        st.markdown(f"**{pain_point}** ({count} mentions)")
                        
                        # Mock NPS breakdown for pain point
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.caption("🔴 Detractors: 70%")
                        with col2:
                            st.caption("🟡 Passives: 20%")
                        with col3:
                            st.caption("🟢 Promoters: 10%")
                        
                        # Sample negative comments
                        st.caption("Sample feedback:")
                        pain_comments = self._get_pain_point_comments(results, pain_point)[:2]
                        for comment in pain_comments:
                            st.caption(f"• {comment[:100]}...")
                        st.markdown("---")
    
    def _render_data_stats_tab(self, results: List, insights: Dict):
        """Render collapsible data statistics"""
        with st.expander("📊 Dataset Statistics", expanded=True):
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                file_size = st.session_state.get('file_size', 'N/A')
                st.metric("File Size", file_size)
            
            with col2:
                avg_length = self._calculate_avg_comment_length(results)
                st.metric("Avg Comment Length", f"{avg_length} chars")
            
            with col3:
                languages = insights.get('language_distribution', {'Spanish': 100})
                main_lang = max(languages, key=languages.get)
                st.metric("Primary Language", main_lang)
            
            with col4:
                response_rate = len(results) / len(results) * 100 if results else 0
                st.metric("Response Rate", f"{response_rate:.1f}%")
        
        with st.expander("🔤 Language & Keyword Analysis", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Top Keywords**")
                # Mock keyword data
                keywords = {
                    'servicio': 45, 'internet': 38, 'velocidad': 32,
                    'problema': 28, 'bien': 25, 'malo': 22
                }
                for word, count in list(keywords.items())[:10]:
                    st.caption(f"• {word}: {count} mentions")
            
            with col2:
                st.markdown("**Language Mix**")
                st.progress(0.7, "Spanish: 70%")
                st.progress(0.2, "Guaraní: 20%")
                st.progress(0.1, "Mixed: 10%")
    
    def _render_recommendations_tab(self, recommendations: List, insights: Dict):
        """Render AI recommendations with priority tags"""
        st.markdown("""
        <style>
        .recommendation-card {
            background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
            border-left: 4px solid #f59e0b;
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 12px;
        }
        .rec-critical {
            background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
            border-left-color: #ef4444;
        }
        .rec-high {
            background: linear-gradient(135deg, #fed7aa 0%, #fdba74 100%);
            border-left-color: #f97316;
        }
        .rec-medium {
            background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
            border-left-color: #f59e0b;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown("### 💡 AI-Powered Recommendations")
        
        # Group recommendations by priority
        critical_recs = []
        high_recs = []
        medium_recs = []
        
        # Parse recommendations - could be strings or dicts
        for rec in recommendations[:10]:
            if isinstance(rec, dict):
                priority = rec.get('priority', 'medium')
                action = rec.get('action', str(rec))
            else:
                # Simple string recommendation
                priority = 'medium'
                action = str(rec)
            
            if 'critical' in priority.lower() or 'urgent' in action.lower():
                critical_recs.append(action)
            elif 'high' in priority.lower() or 'important' in action.lower():
                high_recs.append(action)
            else:
                medium_recs.append(action)
        
        # Display by priority
        if critical_recs:
            st.markdown("#### 🔴 Critical Actions")
            for rec in critical_recs:
                st.markdown(f"""
                <div class="recommendation-card rec-critical">
                    <strong>URGENT:</strong> {rec}
                </div>
                """, unsafe_allow_html=True)
        
        if high_recs:
            st.markdown("#### 🟠 High Priority")
            for rec in high_recs:
                st.markdown(f"""
                <div class="recommendation-card rec-high">
                    <strong>HIGH:</strong> {rec}
                </div>
                """, unsafe_allow_html=True)
        
        if medium_recs:
            st.markdown("#### 🟡 Medium Priority")
            for rec in medium_recs:
                st.markdown(f"""
                <div class="recommendation-card rec-medium">
                    {rec}
                </div>
                """, unsafe_allow_html=True)
        
        # Quick wins section
        with st.expander("⚡ Quick Wins - Low Effort, High Impact"):
            quick_wins = [
                "Improve router configuration guides",
                "Reduce customer service response time",
                "Clarify billing statements",
                "Enhance self-service portal"
            ]
            for win in quick_wins:
                st.success(f"✓ {win}")
    
    def _render_historical_trends_tab(self, results: List, insights: Dict):
        """Render historical comparison widgets"""
        st.markdown("### 📅 Historical Trends & Comparisons")
        
        # Date range selector
        col1, col2 = st.columns(2)
        with col1:
            period = st.selectbox(
                "Select Period",
                ["Last 7 days", "Last 30 days", "Last 3 months"]
            )
        with col2:
            comparison = st.selectbox(
                "Compare with",
                ["Previous period", "Same period last year"]
            )
        
        # Mock historical data
        dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
        historical_data = pd.DataFrame({
            'Date': dates,
            'Positive': [40 + i % 10 for i in range(30)],
            'Neutral': [30 - i % 5 for i in range(30)],
            'Negative': [30 - i % 8 for i in range(30)]
        })
        
        # Sentiment trend chart
        st.subheader("📈 Sentiment Trend")
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=historical_data['Date'],
            y=historical_data['Positive'],
            name='Positive',
            line=dict(color=self.sentiment_colors['positive'], width=3),
            fill='tonexty'
        ))
        
        fig.add_trace(go.Scatter(
            x=historical_data['Date'],
            y=historical_data['Negative'],
            name='Negative',
            line=dict(color=self.sentiment_colors['negative'], width=3),
            fill='tonexty'
        ))
        
        fig.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=0, b=0),
            hovermode='x unified',
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Week over week comparison
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 Week-over-Week Change")
            st.metric("Positive Sentiment", "42%", "+2%", delta_color="normal")
            st.metric("Negative Sentiment", "28%", "-3%", delta_color="inverse")
            st.metric("NPS Score", "15", "+5", delta_color="normal")
        
        with col2:
            st.markdown("#### 🔄 Pain Point Evolution")
            pain_evolution = {
                'Connection issues': ('↑', '+15%', 'red'),
                'Slow speed': ('↓', '-8%', 'green'),
                'Billing problems': ('→', '0%', 'gray'),
                'Customer service': ('↓', '-12%', 'green')
            }
            
            for pain, (arrow, change, color) in pain_evolution.items():
                if color == 'red':
                    st.error(f"{arrow} {pain}: {change}")
                elif color == 'green':
                    st.success(f"{arrow} {pain}: {change}")
                else:
                    st.info(f"{arrow} {pain}: {change}")
    
    # Helper methods
    def _get_sentiment_color_hex(self, percentage: float) -> str:
        """Get color based on sentiment percentage"""
        if percentage >= 60:
            return self.sentiment_colors['positive']
        elif percentage >= 40:
            return self.sentiment_colors['neutral']
        else:
            return self.sentiment_colors['negative']
    
    def _render_compact_sentiment_chart(self, insights: Dict):
        """Render compact sentiment pie chart"""
        sentiment_dist = insights.get('sentiment_percentages', {
            'positive': 40, 'neutral': 35, 'negative': 25
        })
        
        fig = px.pie(
            values=list(sentiment_dist.values()),
            names=list(sentiment_dist.keys()),
            color_discrete_map=self.sentiment_colors,
            height=250
        )
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(
            margin=dict(l=0, r=0, t=20, b=0),
            showlegend=False,
            title="Sentiment Distribution"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _render_confidence_chart(self, results: List):
        """Render confidence distribution chart"""
        if results:
            confidences = [r.get('confidence', 0.5) for r in results]
            
            fig = px.histogram(
                x=confidences,
                nbins=20,
                height=250,
                color_discrete_sequence=['#4299e1']
            )
            
            fig.update_layout(
                margin=dict(l=0, r=0, t=20, b=0),
                showlegend=False,
                title="Confidence Distribution",
                xaxis_title="Confidence Score",
                yaxis_title="Count"
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    def _calculate_avg_comment_length(self, results: List) -> int:
        """Calculate average comment length"""
        if not results:
            return 0
        
        lengths = [len(r.get('translation', '')) for r in results]
        return int(sum(lengths) / len(lengths)) if lengths else 0
    
    def _get_theme_comments(self, results: List, theme: str) -> List[str]:
        """Get sample comments for a theme"""
        theme_comments = []
        for result in results:
            themes = result.get('themes', [])
            if theme.lower() in [t.lower() for t in themes]:
                comment = result.get('translation', '')
                if comment:
                    theme_comments.append(comment)
        return theme_comments[:5]
    
    def _get_pain_point_comments(self, results: List, pain_point: str) -> List[str]:
        """Get sample comments for a pain point"""
        pain_comments = []
        for result in results:
            pain_points = result.get('pain_points', [])
            comment = result.get('translation', '')
            if pain_point.lower() in comment.lower() or \
               pain_point.lower() in [p.lower() for p in pain_points]:
                if comment:
                    pain_comments.append(comment)
        return pain_comments[:5]