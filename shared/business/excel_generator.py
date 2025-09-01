"""
Professional Excel Report Generator with Enhanced UX
Generates formatted Excel reports with proper styling and visualizations
"""

import pandas as pd
from datetime import datetime
from io import BytesIO
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class ProfessionalExcelGenerator:
    """
    Generates professional Excel reports with enhanced formatting and UX
    Optimized for executive presentation and business analysis
    """
    
    def __init__(self):
        self.brand_colors = {
            'primary': '#8B5CF6',      # Purple
            'secondary': '#06B6D4',    # Cyan  
            'accent': '#F59E0B',       # Amber
            'success': '#10B981',      # Green
            'warning': '#F59E0B',      # Amber
            'error': '#EF4444',        # Red
            'text': '#1F2937',         # Dark gray
            'background': '#F8FAFC'    # Light gray
        }
    
    def generate_enhanced_report(self, results: Dict[str, Any], is_ai_analysis: bool = False) -> BytesIO:
        """
        Generate enhanced Excel report with professional formatting
        
        Args:
            results: Analysis results dictionary
            is_ai_analysis: Whether this is an AI analysis (True) or fallback (False)
            
        Returns:
            BytesIO: Excel file buffer ready for download
        """
        output = BytesIO()
        
        try:
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                workbook = writer.book
                
                # Define professional formats
                formats = self._create_excel_formats(workbook)
                
                # 1. Executive Dashboard (Always first)
                self._create_executive_dashboard(writer, results, is_ai_analysis, formats)
                
                # 2. Detailed Results
                self._create_detailed_results(writer, results, formats)
                
                # 3. Sentiment Analysis
                self._create_sentiment_analysis(writer, results, formats)
                
                if is_ai_analysis:
                    # 4. AI Insights (Only for AI analysis)
                    self._create_ai_insights_sheet(writer, results, formats)
                    
                    # 5. Strategic Recommendations
                    self._create_strategic_recommendations(writer, results, formats)
                    
                    # 6. Emotional Analysis (if available)
                    if results.get('emotion_summary'):
                        self._create_emotional_analysis(writer, results, formats)
                
                # 7. Data Dictionary (Always last)
                self._create_data_dictionary(writer, is_ai_analysis, formats)
            
            output.seek(0)
            return output
            
        except Exception as e:
            logger.error(f"Error generating Excel report: {e}")
            raise
    
    def _create_excel_formats(self, workbook):
        """Create professional Excel formatting styles"""
        return {
            'title': workbook.add_format({
                'bold': True,
                'font_size': 16,
                'font_color': self.brand_colors['primary'],
                'align': 'center',
                'valign': 'vcenter',
                'bg_color': self.brand_colors['background'],
                'border': 1
            }),
            'header': workbook.add_format({
                'bold': True,
                'font_size': 12,
                'font_color': 'white',
                'align': 'center',
                'valign': 'vcenter',
                'bg_color': self.brand_colors['primary'],
                'border': 1
            }),
            'subheader': workbook.add_format({
                'bold': True,
                'font_size': 11,
                'font_color': self.brand_colors['text'],
                'bg_color': '#E5E7EB',
                'border': 1
            }),
            'metric_value': workbook.add_format({
                'bold': True,
                'font_size': 14,
                'font_color': self.brand_colors['primary'],
                'align': 'center',
                'valign': 'vcenter',
                'border': 1
            }),
            'metric_label': workbook.add_format({
                'font_size': 10,
                'font_color': self.brand_colors['text'],
                'align': 'center',
                'valign': 'vcenter',
                'bg_color': '#F3F4F6',
                'border': 1
            }),
            'positive': workbook.add_format({
                'font_color': self.brand_colors['success'],
                'bold': True,
                'border': 1
            }),
            'negative': workbook.add_format({
                'font_color': self.brand_colors['error'],
                'bold': True,
                'border': 1
            }),
            'neutral': workbook.add_format({
                'font_color': self.brand_colors['text'],
                'border': 1
            }),
            'percentage': workbook.add_format({
                'num_format': '0.0%',
                'align': 'center',
                'border': 1
            }),
            'currency': workbook.add_format({
                'num_format': '$#,##0',
                'align': 'right',
                'border': 1
            }),
            'date': workbook.add_format({
                'num_format': 'dd/mm/yyyy hh:mm',
                'align': 'center',
                'border': 1
            }),
            'error': workbook.add_format({
                'font_color': self.brand_colors['error'],
                'bold': True,
                'bg_color': '#FEE2E2',
                'border': 1
            }),
            'warning': workbook.add_format({
                'font_color': self.brand_colors['warning'],
                'bold': True,
                'bg_color': '#FEF3C7',
                'border': 1
            })
        }
    
    def _create_executive_dashboard(self, writer, results: Dict, is_ai_analysis: bool, formats: Dict):
        """Create executive dashboard with key metrics"""
        
        # Executive summary data
        dashboard_data = [
            ['PERSONAL PARAGUAY - ANÁLISIS DE COMENTARIOS', ''],
            ['', ''],
            ['Fecha del Análisis', datetime.now().strftime("%d/%m/%Y %H:%M")],
            ['Tipo de Análisis', 'Inteligencia Artificial Avanzada' if is_ai_analysis else 'Análisis Rápido'],
            ['', ''],
            ['MÉTRICAS PRINCIPALES', ''],
            ['Total de Comentarios Analizados', results.get('total', 0)],
            ['Comentarios Positivos', f"{results.get('sentiment_percentages', {}).get('positivo', 0)}%"],
            ['Comentarios Negativos', f"{results.get('sentiment_percentages', {}).get('negativo', 0)}%"],
            ['Comentarios Neutrales', f"{results.get('sentiment_percentages', {}).get('neutral', 0)}%"]
        ]
        
        # Add AI-specific metrics
        if is_ai_analysis:
            insights = results.get('insights', {})
            dashboard_data.extend([
                ['', ''],
                ['INSIGHTS DE INTELIGENCIA ARTIFICIAL', ''],
                ['Índice de Satisfacción del Cliente', f"{insights.get('customer_satisfaction_index', 0)}/100"],
                ['Intensidad Emocional', insights.get('emotional_intensity', 'medio').title()],
                ['Estabilidad de Sentimientos', insights.get('sentiment_stability', 'balanceado').replace('_', ' ').title()],
                ['Calidad de Engagement', insights.get('engagement_quality', 'básico').title()],
                ['', ''],
                ['RECOMENDACIÓN PRINCIPAL', ''],
                ['Acción Prioritaria', results.get('recommendations', ['Mantener calidad actual'])[0] if results.get('recommendations') else 'Mantener calidad actual']
            ])
        
        dashboard_df = pd.DataFrame(dashboard_data, columns=['Métrica', 'Valor'])
        dashboard_df.to_excel(writer, sheet_name='Dashboard Ejecutivo', index=False)
        
        # Apply formatting
        worksheet = writer.sheets['Dashboard Ejecutivo']
        worksheet.write('A1', 'PERSONAL PARAGUAY - ANÁLISIS DE COMENTARIOS', formats['title'])
        worksheet.merge_range('A1:B1', 'PERSONAL PARAGUAY - ANÁLISIS DE COMENTARIOS', formats['title'])
        
        # Auto-adjust column widths
        worksheet.set_column('A:A', 30)
        worksheet.set_column('B:B', 25)
        
        # Format sections
        worksheet.write('A6', 'MÉTRICAS PRINCIPALES', formats['header'])
        worksheet.write('B6', '', formats['header'])
        
        if is_ai_analysis:
            worksheet.write('A12', 'INSIGHTS DE INTELIGENCIA ARTIFICIAL', formats['header'])
            worksheet.write('B12', '', formats['header'])
    
    def _create_detailed_results(self, writer, results: Dict, formats: Dict):
        """Create detailed results sheet with comment analysis"""
        
        comments = results.get('comments', [])
        sentiments = results.get('sentiments', [])
        
        # Create detailed dataframe
        detailed_data = []
        for i, (comment, sentiment) in enumerate(zip(comments, sentiments), 1):
            detailed_data.append({
                'ID': i,
                'Comentario': comment,
                'Sentimiento': sentiment.title(),
                'Longitud': len(comment) if comment else 0,
                'Palabras': len(comment.split()) if comment else 0
            })
        
        detailed_df = pd.DataFrame(detailed_data)
        detailed_df.to_excel(writer, sheet_name='Análisis Detallado', index=False)
        
        # Apply formatting
        worksheet = writer.sheets['Análisis Detallado']
        
        # Header formatting
        for col_num, header in enumerate(detailed_df.columns):
            worksheet.write(0, col_num, header, formats['header'])
        
        # Auto-adjust columns
        worksheet.set_column('A:A', 8)   # ID
        worksheet.set_column('B:B', 50)  # Comentario
        worksheet.set_column('C:C', 15)  # Sentimiento
        worksheet.set_column('D:D', 12)  # Longitud
        worksheet.set_column('E:E', 12)  # Palabras
        
        # Apply conditional formatting for sentiments
        worksheet.conditional_format('C2:C1000', {
            'type': 'text',
            'criteria': 'containing',
            'value': 'Positivo',
            'format': formats['positive']
        })
        
        worksheet.conditional_format('C2:C1000', {
            'type': 'text', 
            'criteria': 'containing',
            'value': 'Negativo',
            'format': formats['negative']
        })
    
    def _create_sentiment_analysis(self, writer, results: Dict, formats: Dict):
        """Create sentiment analysis summary sheet"""
        
        sentiment_data = results.get('sentiment_percentages', {})
        
        # Sentiment summary
        sentiment_summary = [
            ['DISTRIBUCIÓN DE SENTIMIENTOS', ''],
            ['', ''],
            ['Sentimiento', 'Porcentaje', 'Interpretación'],
            ['Positivo', f"{sentiment_data.get('positivo', 0)}%", 'Clientes satisfechos'],
            ['Negativo', f"{sentiment_data.get('negativo', 0)}%", 'Clientes insatisfechos'],
            ['Neutral', f"{sentiment_data.get('neutral', 0)}%", 'Comentarios informativos']
        ]
        
        # Add theme analysis if available
        theme_counts = results.get('theme_counts', {})
        if theme_counts:
            sentiment_summary.extend([
                ['', ''],
                ['TEMAS PRINCIPALES', ''],
                ['', ''],
                ['Tema', 'Frecuencia', 'Relevancia']
            ])
            
            # Sort themes by frequency
            sorted_themes = sorted(theme_counts.items(), key=lambda x: x[1], reverse=True)
            for theme, count in sorted_themes[:10]:  # Top 10 themes
                relevance = "Alta" if count > 5 else ("Media" if count > 2 else "Baja")
                sentiment_summary.append([theme.title(), count, relevance])
        
        sentiment_df = pd.DataFrame(sentiment_summary)
        sentiment_df.to_excel(writer, sheet_name='Análisis de Sentimientos', index=False, header=False)
        
        # Apply formatting
        worksheet = writer.sheets['Análisis de Sentimientos']
        worksheet.write('A1', 'DISTRIBUCIÓN DE SENTIMIENTOS', formats['title'])
        worksheet.merge_range('A1:C1', 'DISTRIBUCIÓN DE SENTIMIENTOS', formats['title'])
        
        # Format headers
        worksheet.write('A3', 'Sentimiento', formats['header'])
        worksheet.write('B3', 'Porcentaje', formats['header'])
        worksheet.write('C3', 'Interpretación', formats['header'])
        
        # Auto-adjust columns
        worksheet.set_column('A:A', 15)
        worksheet.set_column('B:B', 12)
        worksheet.set_column('C:C', 25)
    
    def _create_ai_insights_sheet(self, writer, results: Dict, formats: Dict):
        """Create AI-specific insights sheet"""
        
        insights = results.get('insights', {})
        
        ai_data = [
            ['INSIGHTS DE INTELIGENCIA ARTIFICIAL', ''],
            ['', ''],
            ['MÉTRICAS AVANZADAS', ''],
            ['Índice de Satisfacción del Cliente', f"{insights.get('customer_satisfaction_index', 0)}/100"],
            ['Intensidad Emocional', insights.get('emotional_intensity', 'medio').title()],
            ['Estabilidad de Sentimientos', insights.get('sentiment_stability', 'balanceado').replace('_', ' ').title()],
            ['Calidad de Engagement', insights.get('engagement_quality', 'básico').title()],
            ['', ''],
            ['ÁREAS PRIORITARIAS DE ACCIÓN', ''],
            ['', '']
        ]
        
        # Add priority areas
        priority_areas = insights.get('priority_action_areas', [])
        for i, area in enumerate(priority_areas[:5], 1):  # Top 5 areas
            area_display = area.replace('_', ' ').title()
            ai_data.append([f"{i}. {area_display}", "Requiere atención"])
        
        # Add confidence metrics if available
        if insights.get('confidence_score'):
            ai_data.extend([
                ['', ''],
                ['MÉTRICAS DE CONFIANZA', ''],
                ['Score de Confianza IA', f"{insights.get('confidence_score', 0):.1f}%"],
                ['Calidad de Datos', insights.get('data_quality', 'buena').title()]
            ])
        
        ai_df = pd.DataFrame(ai_data, columns=['Métrica IA', 'Valor'])
        ai_df.to_excel(writer, sheet_name='Insights IA Avanzados', index=False)
        
        # Apply formatting
        worksheet = writer.sheets['Insights IA Avanzados']
        worksheet.write('A1', 'INSIGHTS DE INTELIGENCIA ARTIFICIAL', formats['title'])
        worksheet.merge_range('A1:B1', 'INSIGHTS DE INTELIGENCIA ARTIFICIAL', formats['title'])
        
        # Format sections
        worksheet.write('A3', 'MÉTRICAS AVANZADAS', formats['header'])
        worksheet.write('A9', 'ÁREAS PRIORITARIAS DE ACCIÓN', formats['header'])
        
        # Auto-adjust columns
        worksheet.set_column('A:A', 35)
        worksheet.set_column('B:B', 20)
    
    def _create_strategic_recommendations(self, writer, results: Dict, formats: Dict):
        """Create strategic recommendations sheet"""
        
        recommendations = results.get('recommendations', [])
        
        rec_data = [
            ['RECOMENDACIONES ESTRATÉGICAS', ''],
            ['', ''],
            ['Prioridad', 'Recomendación', 'Tipo', 'Impacto Esperado']
        ]
        
        # Categorize recommendations
        for i, rec in enumerate(recommendations, 1):
            # Determine priority and type based on keywords
            if any(keyword in rec for keyword in ['CRÍTICO', 'EXCELENCIA']):
                priority = "Alta"
                rec_type = "Estratégica"
                impact = "Alto"
            elif any(keyword in rec for keyword in ['INTENSIDAD', 'VELOCIDAD', 'PRECIO', 'SERVICIO']):
                priority = "Media"
                rec_type = "Operacional"
                impact = "Medio"
            else:
                priority = "Baja"
                rec_type = "Mantenimiento"
                impact = "Bajo"
            
            rec_data.append([priority, rec, rec_type, impact])
        
        rec_df = pd.DataFrame(rec_data)
        rec_df.to_excel(writer, sheet_name='Recomendaciones Estratégicas', index=False, header=False)
        
        # Apply formatting
        worksheet = writer.sheets['Recomendaciones Estratégicas']
        worksheet.write('A1', 'RECOMENDACIONES ESTRATÉGICAS', formats['title'])
        worksheet.merge_range('A1:D1', 'RECOMENDACIONES ESTRATÉGICAS', formats['title'])
        
        # Header formatting
        for col, header in enumerate(['Prioridad', 'Recomendación', 'Tipo', 'Impacto Esperado']):
            worksheet.write(2, col, header, formats['header'])
        
        # Auto-adjust columns
        worksheet.set_column('A:A', 12)  # Prioridad
        worksheet.set_column('B:B', 60)  # Recomendación
        worksheet.set_column('C:C', 15)  # Tipo
        worksheet.set_column('D:D', 15)  # Impacto
        
        # Conditional formatting for priorities
        worksheet.conditional_format('A4:A100', {
            'type': 'text',
            'criteria': 'containing',
            'value': 'Alta',
            'format': formats['error']
        })
        
        worksheet.conditional_format('A4:A100', {
            'type': 'text',
            'criteria': 'containing', 
            'value': 'Media',
            'format': formats['warning']
        })
    
    def _create_emotional_analysis(self, writer, results: Dict, formats: Dict):
        """Create emotional analysis sheet (AI only)"""
        
        emotion_summary = results.get('emotion_summary', {})
        emotion_distribution = emotion_summary.get('distribution', {})
        avg_intensity = emotion_summary.get('avg_intensity', 0)
        
        emotion_data = [
            ['ANÁLISIS EMOCIONAL DETALLADO', ''],
            ['', ''],
            ['RESUMEN EMOCIONAL', ''],
            ['Intensidad Promedio', f"{avg_intensity}/10"],
            ['Total Emociones Detectadas', len(emotion_distribution)],
            ['', ''],
            ['DISTRIBUCIÓN DE EMOCIONES', ''],
            ['', ''],
            ['Emoción', 'Frecuencia', 'Porcentaje', 'Interpretación']
        ]
        
        # Sort emotions by frequency
        if emotion_distribution:
            total_emotions = sum(emotion_distribution.values())
            sorted_emotions = sorted(emotion_distribution.items(), key=lambda x: x[1], reverse=True)
            
            for emotion, count in sorted_emotions:
                percentage = (count / total_emotions * 100) if total_emotions > 0 else 0
                
                # Emotion interpretation
                if emotion.lower() in ['alegría', 'satisfacción', 'gratitud']:
                    interpretation = "Emoción positiva"
                elif emotion.lower() in ['enojo', 'frustración', 'decepción']:
                    interpretation = "Emoción negativa"
                else:
                    interpretation = "Emoción neutral"
                
                emotion_data.append([emotion.title(), count, f"{percentage:.1f}%", interpretation])
        
        emotion_df = pd.DataFrame(emotion_data)
        emotion_df.to_excel(writer, sheet_name='Análisis Emocional', index=False, header=False)
        
        # Apply formatting
        worksheet = writer.sheets['Análisis Emocional']
        worksheet.write('A1', 'ANÁLISIS EMOCIONAL DETALLADO', formats['title'])
        worksheet.merge_range('A1:D1', 'ANÁLISIS EMOCIONAL DETALLADO', formats['title'])
        
        # Format headers
        for col, header in enumerate(['Emoción', 'Frecuencia', 'Porcentaje', 'Interpretación']):
            worksheet.write(8, col, header, formats['header'])
        
        # Auto-adjust columns
        worksheet.set_column('A:A', 20)  # Emoción
        worksheet.set_column('B:B', 12)  # Frecuencia
        worksheet.set_column('C:C', 12)  # Porcentaje
        worksheet.set_column('D:D', 20)  # Interpretación
    
    def _create_data_dictionary(self, writer, is_ai_analysis: bool, formats: Dict):
        """Create data dictionary explaining all metrics"""
        
        dictionary_data = [
            ['DICCIONARIO DE DATOS', ''],
            ['', ''],
            ['Término', 'Definición'],
            ['Sentimiento Positivo', 'Comentarios que expresan satisfacción, agrado o evaluación favorable'],
            ['Sentimiento Negativo', 'Comentarios que expresan insatisfacción, quejas o evaluación desfavorable'],
            ['Sentimiento Neutral', 'Comentarios informativos sin carga emocional clara'],
            ['', '']
        ]
        
        if is_ai_analysis:
            dictionary_data.extend([
                ['MÉTRICAS DE INTELIGENCIA ARTIFICIAL', ''],
                ['Índice de Satisfacción', 'Puntuación 0-100 basada en análisis contextual de comentarios'],
                ['Intensidad Emocional', 'Nivel de carga emocional en los comentarios (Bajo/Medio/Alto)'],
                ['Estabilidad de Sentimientos', 'Consistencia en la polaridad de sentimientos'],
                ['Calidad de Engagement', 'Nivel de interacción y profundidad en comentarios'],
                ['Áreas Prioritarias', 'Aspectos del negocio que requieren atención inmediata'],
                ['Análisis Emocional', 'Detección de emociones específicas más allá de sentimientos básicos'],
                ['', '']
            ])
        
        dictionary_data.extend([
            ['METODOLOGÍA', ''],
            ['Tipo de Análisis', 'IA Avanzada con OpenAI GPT' if is_ai_analysis else 'Análisis de Reglas Básicas'],
            ['Fecha de Procesamiento', datetime.now().strftime("%d/%m/%Y")],
            ['Plataforma', 'Personal Paraguay Comment Analyzer'],
            ['Versión', '2.0 - Análisis Inteligente Integrado']
        ])
        
        dict_df = pd.DataFrame(dictionary_data, columns=['Término', 'Definición'])
        dict_df.to_excel(writer, sheet_name='Diccionario de Datos', index=False)
        
        # Apply formatting
        worksheet = writer.sheets['Diccionario de Datos']
        worksheet.write('A1', 'DICCIONARIO DE DATOS', formats['title'])
        worksheet.merge_range('A1:B1', 'DICCIONARIO DE DATOS', formats['title'])
        
        # Format headers
        worksheet.write('A3', 'Término', formats['header'])
        worksheet.write('B3', 'Definición', formats['header'])
        
        # Auto-adjust columns
        worksheet.set_column('A:A', 25)  # Término
        worksheet.set_column('B:B', 60)  # Definición
    


# Convenience function for easy integration
def generate_professional_excel(results: Dict[str, Any], is_ai_analysis: bool = False) -> BytesIO:
    """
    Generate professional Excel report with enhanced UX
    
    Args:
        results: Analysis results dictionary
        is_ai_analysis: Whether this is an AI analysis
        
    Returns:
        BytesIO: Excel file buffer ready for download
    """
    generator = ProfessionalExcelGenerator()
    return generator.generate_enhanced_report(results, is_ai_analysis)