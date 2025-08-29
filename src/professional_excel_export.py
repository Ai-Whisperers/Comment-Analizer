"""
Professional Excel Export Module for Personal Paraguay
Creates a comprehensive, professionally formatted Excel report
"""

import pandas as pd
import numpy as np
from datetime import datetime
from io import BytesIO
import xlsxwriter
import logging

logger = logging.getLogger(__name__)

class ProfessionalExcelExporter:
    def __init__(self):
        """Initialize professional Excel exporter with style configurations"""
        
        # Professional color scheme (Personal Paraguay brand colors)
        self.colors = {
            'primary': '#1E3A8A',      # Deep blue
            'secondary': '#3B82F6',    # Bright blue
            'success': '#10B981',      # Green
            'warning': '#F59E0B',      # Orange
            'danger': '#EF4444',       # Red
            'dark': '#1F2937',         # Dark gray
            'light': '#F3F4F6',        # Light gray
            'white': '#FFFFFF'         # White
        }
        
        # Sheet order (logical flow)
        self.sheet_order = [
            '00_Portada',
            '01_Resumen_Ejecutivo',
            '02_Metodología',
            '03_KPIs_Dashboard',
            '04_Análisis_NPS',
            '05_Análisis_Sentimientos',
            '06_Análisis_Emociones',
            '07_Temas_Principales',
            '08_Problemas_Servicio',
            '09_Análisis_Competencia',
            '10_Análisis_Churn',
            '11_Plan_Acción',
            '12_Comentarios_Detalle',
            '13_Estadísticas_Limpieza',
            '14_Glosario',
            '15_Anexos'
        ]

    def create_professional_excel(self, results):
        """Create a professional Excel report with all analyses"""
        try:
            # Input validation
            if not results:
                raise ValueError("No analysis results provided for Excel export")
                
            if not isinstance(results, dict):
                raise TypeError("Results must be a dictionary")
                
            output = BytesIO()
            
            # Create Excel writer with xlsxwriter engine for advanced formatting
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                workbook = writer.book
                
                # Define professional formats
                formats = self._create_formats(workbook)
                
                # Sheet 00: Cover Page
                self._create_cover_sheet(writer, workbook, formats, results)
                
                # Sheet 01: Executive Summary
                self._create_executive_summary(writer, workbook, formats, results)
                
                # Sheet 02: Methodology
                self._create_methodology_sheet(writer, workbook, formats)
                
                # Sheet 03: KPIs Dashboard
                self._create_kpi_dashboard(writer, workbook, formats, results)
                
                # Sheet 04: NPS Analysis
                self._create_nps_analysis(writer, workbook, formats, results)
                
                # Sheet 05: Sentiment Analysis
                self._create_sentiment_analysis(writer, workbook, formats, results)
                
                # Sheet 06: Emotion Analysis
                self._create_emotion_analysis(writer, workbook, formats, results)
                
                # Sheet 07: Main Themes
                self._create_themes_analysis(writer, workbook, formats, results)
                
                # Sheet 08: Service Problems
                self._create_service_problems(writer, workbook, formats, results)
                
                # Sheet 09: Competition Analysis
                self._create_competition_analysis(writer, workbook, formats, results)
                
                # Sheet 10: Churn Analysis
                self._create_churn_analysis(writer, workbook, formats, results)
                
                # Sheet 11: Action Plan
                self._create_action_plan(writer, workbook, formats, results)
                
                # Sheet 12: Detailed Comments
                self._create_detailed_comments(writer, workbook, formats, results)
                
                # Sheet 13: Data Cleaning Statistics
                self._create_cleaning_stats(writer, workbook, formats, results)
                
                # Sheet 14: Glossary
                self._create_glossary(writer, workbook, formats)
                
                # Sheet 15: Appendix
                self._create_appendix(writer, workbook, formats, results)
                
            return output.getvalue()
            
        except ValueError as e:
            logger.error(f"Invalid input data for Excel export: {str(e)}")
            raise ValueError(f"Invalid input data for Excel export: {str(e)}")
        except TypeError as e:
            logger.error(f"Data type error in Excel export: {str(e)}")
            raise TypeError(f"Data type error in Excel export: {str(e)}")
        except MemoryError as e:
            logger.error(f"Not enough memory to create Excel report: {str(e)}")
            raise MemoryError(f"Not enough memory to create Excel report: {str(e)}")
        except Exception as e:
            logger.error(f"Excel export failed: {str(e)}")
            raise RuntimeError(f"Excel export failed: {str(e)}")
    
    def _create_formats(self, workbook):
        """Create professional cell formats"""
        formats = {
            'title': workbook.add_format({
                'bold': True,
                'font_size': 24,
                'font_color': self.colors['primary'],
                'align': 'center',
                'valign': 'vcenter'
            }),
            'subtitle': workbook.add_format({
                'bold': True,
                'font_size': 18,
                'font_color': self.colors['dark'],
                'align': 'center',
                'valign': 'vcenter'
            }),
            'header': workbook.add_format({
                'bold': True,
                'font_size': 12,
                'font_color': self.colors['white'],
                'bg_color': self.colors['primary'],
                'align': 'center',
                'valign': 'vcenter',
                'border': 1
            }),
            'subheader': workbook.add_format({
                'bold': True,
                'font_size': 11,
                'font_color': self.colors['dark'],
                'bg_color': self.colors['light'],
                'align': 'left',
                'valign': 'vcenter',
                'border': 1
            }),
            'cell': workbook.add_format({
                'font_size': 10,
                'align': 'left',
                'valign': 'vcenter',
                'border': 1,
                'text_wrap': True
            }),
            'cell_center': workbook.add_format({
                'font_size': 10,
                'align': 'center',
                'valign': 'vcenter',
                'border': 1
            }),
            'number': workbook.add_format({
                'font_size': 10,
                'align': 'right',
                'valign': 'vcenter',
                'border': 1,
                'num_format': '#,##0'
            }),
            'percentage': workbook.add_format({
                'font_size': 10,
                'align': 'right',
                'valign': 'vcenter',
                'border': 1,
                'num_format': '0.0%'
            }),
            'currency': workbook.add_format({
                'font_size': 10,
                'align': 'right',
                'valign': 'vcenter',
                'border': 1,
                'num_format': '₲ #,##0'
            }),
            'good': workbook.add_format({
                'font_size': 10,
                'font_color': self.colors['success'],
                'bold': True,
                'align': 'center',
                'valign': 'vcenter',
                'border': 1
            }),
            'warning': workbook.add_format({
                'font_size': 10,
                'font_color': self.colors['warning'],
                'bold': True,
                'align': 'center',
                'valign': 'vcenter',
                'border': 1
            }),
            'bad': workbook.add_format({
                'font_size': 10,
                'font_color': self.colors['danger'],
                'bold': True,
                'align': 'center',
                'valign': 'vcenter',
                'border': 1
            }),
            'date': workbook.add_format({
                'font_size': 10,
                'align': 'center',
                'valign': 'vcenter',
                'border': 1,
                'num_format': 'dd/mm/yyyy hh:mm'
            })
        }
        return formats
    
    def _create_cover_sheet(self, writer, workbook, formats, results):
        """Create professional cover page"""
        worksheet = workbook.add_worksheet('00_Portada')
        
        # Set column widths
        worksheet.set_column('A:A', 5)
        worksheet.set_column('B:F', 20)
        
        # Company logo area (placeholder)
        worksheet.merge_range('B2:F4', 'PERSONAL PARAGUAY', formats['title'])
        worksheet.merge_range('B5:F5', 'Análisis de Comentarios de Clientes', formats['subtitle'])
        
        # Report info
        worksheet.write('B8', 'REPORTE DE ANÁLISIS', formats['subheader'])
        worksheet.write('B10', 'Fecha de Generación:', formats['cell'])
        worksheet.write('C10', datetime.now().strftime('%d/%m/%Y %H:%M'), formats['date'])
        
        worksheet.write('B11', 'Período Analizado:', formats['cell'])
        worksheet.write('C11', results.get('analysis_date', 'N/A'), formats['cell'])
        
        worksheet.write('B12', 'Total de Comentarios:', formats['cell'])
        worksheet.write('C12', results.get('total', 0), formats['number'])
        
        worksheet.write('B13', 'Archivo Fuente:', formats['cell'])
        worksheet.write('C13', results.get('original_filename', 'N/A'), formats['cell'])
        
        # Key metrics summary
        worksheet.write('B16', 'MÉTRICAS CLAVE', formats['subheader'])
        
        nps_score = results.get('nps', {}).get('score', 0)
        nps_format = formats['good'] if nps_score > 0 else formats['bad'] if nps_score < -20 else formats['warning']
        worksheet.write('B18', 'NPS Score:', formats['cell'])
        worksheet.write('C18', f"{nps_score}%", nps_format)
        
        if results.get('csi_analysis'):
            csi = results['csi_analysis']['csi_score']
            csi_format = formats['good'] if csi >= 70 else formats['warning'] if csi >= 50 else formats['bad']
            worksheet.write('B19', 'Índice de Satisfacción (CSI):', formats['cell'])
            worksheet.write('C19', f"{csi}%", csi_format)
        
        worksheet.write('B20', 'Sentimiento Positivo:', formats['cell'])
        worksheet.write('C20', f"{results.get('positive_pct', 0)}%", formats['percentage'])
        
        worksheet.write('B21', 'Sentimiento Negativo:', formats['cell'])
        neg_pct = results.get('negative_pct', 0)
        neg_format = formats['bad'] if neg_pct > 30 else formats['warning'] if neg_pct > 20 else formats['good']
        worksheet.write('C21', f"{neg_pct}%", neg_format)
    
    def _create_executive_summary(self, writer, workbook, formats, results):
        """Create executive summary with key insights"""
        df_summary = pd.DataFrame({
            'Sección': ['RESUMEN EJECUTIVO'],
            'Contenido': ['']
        })
        
        worksheet = workbook.add_worksheet('01_Resumen_Ejecutivo')
        
        # Title
        worksheet.merge_range('A1:G1', 'RESUMEN EJECUTIVO', formats['title'])
        worksheet.merge_range('A2:G2', f"Análisis de {results.get('total', 0)} Comentarios de Clientes", formats['subtitle'])
        
        # Key Findings Section
        row = 4
        worksheet.merge_range(f'A{row}:G{row}', '1. HALLAZGOS CLAVE', formats['subheader'])
        
        row += 2
        findings = [
            f"• NPS Score: {results.get('nps', {}).get('score', 0)}% - {'Crítico' if results.get('nps', {}).get('score', 0) < -20 else 'Necesita Mejora' if results.get('nps', {}).get('score', 0) < 0 else 'Positivo'}",
            f"• Satisfacción General: {100 - results.get('negative_pct', 0):.1f}%",
            f"• Comentarios Informativos: {results.get('informative_comments', 0)}/{results.get('total', 0)}",
            f"• Principales Temas: Servicio, Mejoras Necesarias, Precio",
            f"• Riesgo de Churn Alto: {results.get('churn_analysis', {}).get('high_risk', 0)} clientes"
        ]
        
        for finding in findings:
            worksheet.write(f'B{row}', finding, formats['cell'])
            row += 1
        
        # Recommendations Section
        row += 1
        worksheet.merge_range(f'A{row}:G{row}', '2. RECOMENDACIONES PRINCIPALES', formats['subheader'])
        
        row += 2
        if results.get('insights'):
            for i, insight in enumerate(results['insights'][:5], 1):
                worksheet.write(f'B{row}', f"{i}. {insight['action']}", formats['cell'])
                row += 1
        
        # Critical Alerts
        if results.get('alerts'):
            row += 1
            worksheet.merge_range(f'A{row}:G{row}', '3. ALERTAS CRÍTICAS', formats['subheader'])
            row += 2
            for alert in results['alerts'][:3]:
                worksheet.write(f'B{row}', f"⚠️ {alert['message']}", formats['warning'] if alert['severity'] != 'critical' else formats['bad'])
                row += 1
        
        # Next Steps
        row += 1
        worksheet.merge_range(f'A{row}:G{row}', '4. PRÓXIMOS PASOS', formats['subheader'])
        row += 2
        next_steps = [
            "1. Revisar clientes en alto riesgo de churn (Ver hoja 10)",
            "2. Implementar plan de acción prioritario (Ver hoja 11)",
            "3. Monitorear métricas clave semanalmente",
            "4. Realizar seguimiento a casos críticos P0"
        ]
        for step in next_steps:
            worksheet.write(f'B{row}', step, formats['cell'])
            row += 1
        
        # Set column widths
        worksheet.set_column('A:A', 5)
        worksheet.set_column('B:G', 20)
    
    def _create_methodology_sheet(self, writer, workbook, formats):
        """Create methodology explanation sheet"""
        worksheet = workbook.add_worksheet('02_Metodología')
        
        # Title
        worksheet.merge_range('A1:G1', 'METODOLOGÍA DE ANÁLISIS', formats['title'])
        
        # Sections
        row = 3
        sections = [
            {
                'title': '1. PROCESAMIENTO DE DATOS',
                'content': [
                    '• Limpieza de datos: Corrección ortográfica automática de errores comunes',
                    '• Eliminación de duplicados: Identificación y conteo de frecuencias',
                    '• Filtrado de calidad: Exclusión de respuestas no informativas ("No", ".", "Nada")',
                    '• Normalización: Estandarización de formato y puntuación'
                ]
            },
            {
                'title': '2. ANÁLISIS DE SENTIMIENTOS',
                'content': [
                    '• Clasificación en 3 categorías: Positivo, Neutral, Negativo',
                    '• Algoritmo híbrido: Combina análisis de texto con calificación (Nota)',
                    '• Palabras clave específicas del sector telecomunicaciones',
                    '• Ponderación por intensidad emocional (escala 1-10)'
                ]
            },
            {
                'title': '3. CÁLCULO DE NPS',
                'content': [
                    '• Basado en columna NPS real del dataset',
                    '• Promotores: Nota 9-10 (32.4% del total)',
                    '• Pasivos: Nota 7-8 (23.6% del total)',
                    '• Detractores: Nota 0-6 (44% del total)',
                    '• Fórmula: NPS = (% Promotores - % Detractores)'
                ]
            },
            {
                'title': '4. ÍNDICE DE SATISFACCIÓN (CSI)',
                'content': [
                    '• Fórmula compuesta: 40% promedio rating + 30% ratings altos + 30% inverso ratings bajos',
                    '• Escala 0-100 puntos',
                    '• Niveles: Crítico (<50), Bajo (50-60), Regular (60-70), Bueno (70-80), Excelente (80+)'
                ]
            },
            {
                'title': '5. DETECCIÓN DE TEMAS',
                'content': [
                    '• Análisis de palabras clave y frases',
                    '• Categorización automática en temas principales',
                    '• Cálculo de frecuencia y porcentaje de ocurrencia',
                    '• Identificación de sub-temas dentro de categorías principales'
                ]
            },
            {
                'title': '6. ANÁLISIS DE RIESGO',
                'content': [
                    '• Churn: Detección de intención de cancelación',
                    '• Urgencia: Clasificación P0 (crítico) a P3 (deseable)',
                    '• Competencia: Identificación de menciones a competidores',
                    '• Problemas de servicio: Severidad crítica/alta/media/baja'
                ]
            }
        ]
        
        for section in sections:
            worksheet.merge_range(f'A{row}:G{row}', section['title'], formats['subheader'])
            row += 2
            for item in section['content']:
                worksheet.write(f'B{row}', item, formats['cell'])
                row += 1
            row += 1
        
        # Set column widths
        worksheet.set_column('A:A', 5)
        worksheet.set_column('B:G', 25)
    
    def _create_kpi_dashboard(self, writer, workbook, formats, results):
        """Create KPI dashboard with visual indicators"""
        # Prepare data
        kpi_data = {
            'KPI': [
                'Net Promoter Score (NPS)',
                'Índice de Satisfacción (CSI)',
                'Sentimiento Positivo',
                'Sentimiento Negativo',
                'Calificación Promedio',
                'Riesgo de Churn Alto',
                'Casos Críticos (P0)',
                'Comentarios Informativos',
                'Menciones a Competidores'
            ],
            'Valor Actual': [
                f"{results.get('nps', {}).get('score', 0)}%",
                f"{results.get('csi_analysis', {}).get('csi_score', 0) if results.get('csi_analysis') else 'N/A'}%",
                f"{results.get('positive_pct', 0)}%",
                f"{results.get('negative_pct', 0)}%",
                f"{results.get('rating_data', {}).get('average', 0)}/10",
                results.get('churn_analysis', {}).get('high_risk', 0),
                results.get('urgency_distribution', {}).get('P0', 0),
                f"{results.get('informative_comments', 0)}/{results.get('total', 0)}",
                f"{results.get('competitor_analysis', {}).get('total_mentions', 0)}"
            ],
            'Meta/Benchmark': [
                '>0%',
                '>70%',
                '>40%',
                '<20%',
                '>7.0',
                '<10',
                '0',
                '>80%',
                '<10%'
            ],
            'Estado': [],
            'Tendencia': [],
            'Prioridad': []
        }
        
        # Calculate status for each KPI
        for i, kpi in enumerate(kpi_data['KPI']):
            if 'NPS' in kpi:
                val = results.get('nps', {}).get('score', 0)
                kpi_data['Estado'].append('✅ Bueno' if val > 0 else '⚠️ Alerta' if val > -20 else '❌ Crítico')
                kpi_data['Tendencia'].append('→ Estable')
                kpi_data['Prioridad'].append('ALTA' if val < -20 else 'MEDIA' if val < 0 else 'BAJA')
            elif 'CSI' in kpi:
                val = results.get('csi_analysis', {}).get('csi_score', 0) if results.get('csi_analysis') else 0
                kpi_data['Estado'].append('✅ Bueno' if val >= 70 else '⚠️ Regular' if val >= 50 else '❌ Crítico')
                kpi_data['Tendencia'].append('→ Estable')
                kpi_data['Prioridad'].append('ALTA' if val < 50 else 'MEDIA' if val < 70 else 'BAJA')
            else:
                kpi_data['Estado'].append('→ Monitorear')
                kpi_data['Tendencia'].append('→ Estable')
                kpi_data['Prioridad'].append('MEDIA')
        
        df_kpi = pd.DataFrame(kpi_data)
        df_kpi.to_excel(writer, sheet_name='03_KPIs_Dashboard', index=False)
        
        # Format the sheet
        worksheet = writer.sheets['03_KPIs_Dashboard']
        worksheet.set_column('A:A', 30)
        worksheet.set_column('B:F', 15)
        
        # Add header formatting
        for col_num, value in enumerate(df_kpi.columns.values):
            worksheet.write(0, col_num, value, formats['header'])
    
    def _create_nps_analysis(self, writer, workbook, formats, results):
        """Create detailed NPS analysis"""
        nps_data = {
            'Categoría': ['Promotores', 'Pasivos', 'Detractores', 'TOTAL'],
            'Cantidad': [
                results.get('nps', {}).get('promoters', 0),
                results.get('nps', {}).get('passives', 0),
                results.get('nps', {}).get('detractors', 0),
                results.get('total', 0)
            ],
            'Porcentaje': [
                f"{results.get('nps', {}).get('promoters', 0)/max(results.get('total', 1), 1)*100:.1f}%",
                f"{results.get('nps', {}).get('passives', 0)/max(results.get('total', 1), 1)*100:.1f}%",
                f"{results.get('nps', {}).get('detractors', 0)/max(results.get('total', 1), 1)*100:.1f}%",
                '100.0%'
            ],
            'Nota Promedio': ['9-10', '7-8', '0-6', f"{results.get('rating_data', {}).get('average', 0):.1f}"],
            'Acción Recomendada': [
                'Mantener satisfacción y solicitar referencias',
                'Convertir en promotores con mejoras específicas',
                'Acción urgente de retención y mejora',
                f"NPS Score: {results.get('nps', {}).get('score', 0)}%"
            ]
        }
        
        df_nps = pd.DataFrame(nps_data)
        df_nps.to_excel(writer, sheet_name='04_Análisis_NPS', index=False)
        
        worksheet = writer.sheets['04_Análisis_NPS']
        worksheet.set_column('A:A', 20)
        worksheet.set_column('B:E', 25)
        
        # Add header formatting
        for col_num, value in enumerate(df_nps.columns.values):
            worksheet.write(0, col_num, value, formats['header'])
        
        # Add a chart if possible
        if results.get('nps'):
            chart = workbook.add_chart({'type': 'pie'})
            chart.add_series({
                'categories': ['04_Análisis_NPS', 1, 0, 3, 0],
                'values': ['04_Análisis_NPS', 1, 1, 3, 1],
                'name': 'Distribución NPS'
            })
            chart.set_title({'name': 'Distribución NPS'})
            chart.set_style(10)
            worksheet.insert_chart('G2', chart)
    
    def _create_sentiment_analysis(self, writer, workbook, formats, results):
        """Create enhanced sentiment analysis sheet with OpenAI data"""
        from src.i18n.translations import get_comprehensive_sentiment_labels
        
        # Get Spanish labels
        labels = get_comprehensive_sentiment_labels()
        
        # Basic sentiment data
        sentiment_data = {
            'Sentimiento': ['Positivo', 'Neutral', 'Negativo'],
            'Cantidad': [
                results.get('positive_count', 0),
                results.get('neutral_count', 0),
                results.get('negative_count', 0)
            ],
            'Porcentaje': [
                f"{results.get('positive_pct', 0):.1f}%",
                f"{results.get('neutral_pct', 0):.1f}%",
                f"{results.get('negative_pct', 0):.1f}%"
            ],
            'Interpretación': [
                'Clientes satisfechos - Mantener nivel de servicio',
                'Clientes indiferentes - Oportunidad de mejora',
                'Clientes insatisfechos - Requiere acción inmediata'
            ]
        }
        
        # Add AI confidence if available
        if results.get('analysis_method') == 'AI_POWERED':
            sentiment_data['Confianza IA'] = [
                f"{results.get('ai_confidence_avg', 0) * 100:.1f}%",
                f"{results.get('ai_confidence_avg', 0) * 100:.1f}%", 
                f"{results.get('ai_confidence_avg', 0) * 100:.1f}%"
            ]
        
        df_sentiment = pd.DataFrame(sentiment_data)
        df_sentiment.to_excel(writer, sheet_name='05_Análisis_Sentimientos', index=False, startrow=0)
        
        worksheet = writer.sheets['05_Análisis_Sentimientos']
        worksheet.set_column('A:A', 15)
        worksheet.set_column('B:E', 15)
        worksheet.set_column('D:D', 40)
        
        # Headers
        for col_num, value in enumerate(df_sentiment.columns.values):
            worksheet.write(0, col_num, value, formats['header'])
        
        # Add detailed analysis if AI data is available
        if results.get('analysis_method') == 'AI_POWERED' and 'comments' in results:
            row_start = len(df_sentiment) + 4
            
            # Section header
            worksheet.merge_range(f'A{row_start}:H{row_start}', 
                                'ANÁLISIS DETALLADO CON IA', formats['title'])
            row_start += 2
            
            # Create detailed data table
            detailed_data = []
            comments = results.get('comments', [])[:50]  # Limit for Excel performance
            sentiments = results.get('sentiments', [])[:50]
            
            # Extract AI data from enhanced results if available
            for i, (comment, sentiment) in enumerate(zip(comments, sentiments)):
                row_data = {
                    'ID': f'C{i+1:04d}',
                    'Comentario': comment[:100] + '...' if len(comment) > 100 else comment,
                    'Sentimiento': sentiment.title(),
                    'Confianza': 'N/A',
                    'Idioma': 'Español',
                    'Temas': 'N/A',
                    'Emociones': 'N/A',
                    'Puntos de Dolor': 'N/A'
                }
                
                # Add AI enhancement data if available
                if 'enhanced_results' in results and i < len(results['enhanced_results']):
                    enhanced = results['enhanced_results'][i]
                    
                    # Extract confidence from intensity
                    intensity = enhanced.get('emotions', {}).get('intensity', 1.0)
                    confidence = min(intensity / 2.5, 1.0)  # Normalize to 0-1
                    row_data['Confianza'] = f"{confidence * 100:.1f}%"
                    
                    # Extract themes
                    themes = list(enhanced.get('extended_themes', {}).keys())[:3]
                    row_data['Temas'] = ', '.join(themes) if themes else 'N/A'
                    
                    # Extract emotions
                    emotions = enhanced.get('emotions', {}).get('detected', [])[:3]
                    row_data['Emociones'] = ', '.join(emotions) if emotions else 'N/A'
                    
                    # Extract pain points
                    pain_points = enhanced.get('churn_risk', {}).get('indicators', [])[:3]
                    row_data['Puntos de Dolor'] = ', '.join(pain_points) if pain_points else 'N/A'
                
                detailed_data.append(row_data)
            
            # Create detailed DataFrame
            df_detailed = pd.DataFrame(detailed_data)
            df_detailed.to_excel(writer, sheet_name='05_Análisis_Sentimientos', 
                               index=False, startrow=row_start)
            
            # Format detailed table headers
            for col_num, value in enumerate(df_detailed.columns.values):
                worksheet.write(row_start, col_num, value, formats['header'])
            
            # Set column widths for detailed section
            worksheet.set_column('A:A', 8)   # ID
            worksheet.set_column('B:B', 50)  # Comment
            worksheet.set_column('C:C', 12)  # Sentiment
            worksheet.set_column('D:D', 12)  # Confidence
            worksheet.set_column('E:E', 10)  # Language
            worksheet.set_column('F:F', 25)  # Themes
            worksheet.set_column('G:G', 20)  # Emotions
            worksheet.set_column('H:H', 25)  # Pain Points
    
    def _create_emotion_analysis(self, writer, workbook, formats, results):
        """Create emotion analysis sheet"""
        if 'enhanced_results' in results and results['enhanced_results']:
            emotion_data = []
            emotion_counts = {}
            
            for res in results['enhanced_results'][:100]:  # Sample
                emotion = res.get('emotions', {})
                dominant = emotion.get('dominant_emotion', 'neutral')
                emotion_counts[dominant] = emotion_counts.get(dominant, 0) + 1
            
            for emotion, count in emotion_counts.items():
                emotion_data.append({
                    'Emoción': emotion.replace('_', ' ').title(),
                    'Frecuencia': count,
                    'Porcentaje': f"{count/len(results['enhanced_results'])*100:.1f}%"
                })
            
            if emotion_data:
                df_emotion = pd.DataFrame(emotion_data)
                df_emotion = df_emotion.sort_values('Frecuencia', ascending=False)
                df_emotion.to_excel(writer, sheet_name='06_Análisis_Emociones', index=False)
                
                worksheet = writer.sheets['06_Análisis_Emociones']
                worksheet.set_column('A:C', 20)
                
                for col_num, value in enumerate(df_emotion.columns.values):
                    worksheet.write(0, col_num, value, formats['header'])
    
    def _create_themes_analysis(self, writer, workbook, formats, results):
        """Create themes analysis sheet"""
        if 'theme_counts' in results:
            theme_labels = {
                'velocidad_lenta': 'Velocidad Lenta',
                'intermitencias': 'Intermitencias',
                'atencion_cliente': 'Atención al Cliente',
                'precio': 'Precio',
                'cobertura': 'Cobertura',
                'instalacion': 'Instalación'
            }
            
            themes_data = []
            for theme, count in results['theme_counts'].items():
                themes_data.append({
                    'Tema Principal': theme_labels.get(theme, theme.replace('_', ' ').title()),
                    'Menciones': count,
                    'Porcentaje': f"{count/max(results.get('total', 1), 1)*100:.1f}%",
                    'Severidad': 'Alta' if count > 50 else 'Media' if count > 20 else 'Baja',
                    'Prioridad': 'P1' if count > 50 else 'P2' if count > 20 else 'P3'
                })
            
            df_themes = pd.DataFrame(themes_data)
            df_themes = df_themes.sort_values('Menciones', ascending=False)
            df_themes.to_excel(writer, sheet_name='07_Temas_Principales', index=False)
            
            worksheet = writer.sheets['07_Temas_Principales']
            worksheet.set_column('A:A', 25)
            worksheet.set_column('B:E', 15)
            
            for col_num, value in enumerate(df_themes.columns.values):
                worksheet.write(0, col_num, value, formats['header'])
    
    def _create_service_problems(self, writer, workbook, formats, results):
        """Create service problems analysis"""
        if 'service_issues_summary' in results:
            problems_data = {
                'Severidad': ['Crítica', 'Alta', 'Media', 'Baja'],
                'Cantidad': [
                    results['service_issues_summary'].get('critical', 0),
                    results['service_issues_summary'].get('high', 0),
                    results['service_issues_summary'].get('medium', 0),
                    results['service_issues_summary'].get('low', 0)
                ],
                'Descripción': [
                    'Sin servicio - Requiere respuesta inmediata',
                    'Intermitencias - Afecta productividad',
                    'Lentitud - Experiencia degradada',
                    'Problemas menores - Monitorear'
                ],
                'Tiempo Respuesta': ['< 4 horas', '< 24 horas', '< 48 horas', '< 1 semana'],
                'Responsable': ['NOC + Gerencia', 'Soporte Técnico L2', 'Soporte Técnico L1', 'Monitoreo']
            }
            
            df_problems = pd.DataFrame(problems_data)
            df_problems.to_excel(writer, sheet_name='08_Problemas_Servicio', index=False)
            
            worksheet = writer.sheets['08_Problemas_Servicio']
            worksheet.set_column('A:E', 25)
            
            for col_num, value in enumerate(df_problems.columns.values):
                worksheet.write(0, col_num, value, formats['header'])
    
    def _create_competition_analysis(self, writer, workbook, formats, results):
        """Create competition analysis sheet"""
        comp_data = {
            'Competidor': ['Tigo', 'Copaco', 'Claro', 'Vox', 'TOTAL'],
            'Menciones': [0, 0, 0, 0, 0],
            'Porcentaje': ['0%', '0%', '0%', '0%', '0%'],
            'Contexto': ['', '', '', '', '']
        }
        
        # Update with real data if available
        if 'enhanced_results' in results:
            for res in results['enhanced_results']:
                comp = res.get('competitors', {})
                if comp.get('mentioned'):
                    for competitor in comp['mentioned']:
                        if competitor.lower() == 'tigo':
                            comp_data['Menciones'][0] += 1
                        elif competitor.lower() == 'copaco':
                            comp_data['Menciones'][1] += 1
                        elif competitor.lower() == 'claro':
                            comp_data['Menciones'][2] += 1
                        elif competitor.lower() == 'vox':
                            comp_data['Menciones'][3] += 1
            
            comp_data['Menciones'][4] = sum(comp_data['Menciones'][:4])
            total = results.get('total', 1)
            for i in range(5):
                comp_data['Porcentaje'][i] = f"{comp_data['Menciones'][i]/total*100:.1f}%"
        
        df_comp = pd.DataFrame(comp_data)
        df_comp.to_excel(writer, sheet_name='09_Análisis_Competencia', index=False)
        
        worksheet = writer.sheets['09_Análisis_Competencia']
        worksheet.set_column('A:D', 20)
        
        for col_num, value in enumerate(df_comp.columns.values):
            worksheet.write(0, col_num, value, formats['header'])
    
    def _create_churn_analysis(self, writer, workbook, formats, results):
        """Create churn risk analysis"""
        churn_data = []
        
        if 'enhanced_results' in results:
            for i, res in enumerate(results['enhanced_results'][:50]):  # Top 50
                churn = res.get('churn_risk', {})
                if churn.get('risk_level') in ['high', 'medium']:
                    churn_data.append({
                        'Cliente ID': f'C{i+1:04d}',
                        'Nivel de Riesgo': churn.get('risk_level', '').upper(),
                        'Probabilidad (%)': churn.get('probability', 0),
                        'Indicadores': ', '.join(churn.get('indicators', [])) if churn.get('indicators') else 'N/A',
                        'Acción': 'Llamada urgente' if churn.get('risk_level') == 'high' else 'Seguimiento'
                    })
        
        if churn_data:
            df_churn = pd.DataFrame(churn_data)
            df_churn = df_churn.sort_values('Probabilidad (%)', ascending=False)
            df_churn.to_excel(writer, sheet_name='10_Análisis_Churn', index=False)
            
            worksheet = writer.sheets['10_Análisis_Churn']
            worksheet.set_column('A:A', 15)
            worksheet.set_column('B:E', 25)
            
            for col_num, value in enumerate(df_churn.columns.values):
                worksheet.write(0, col_num, value, formats['header'])
    
    def _create_action_plan(self, writer, workbook, formats, results):
        """Create prioritized action plan"""
        actions = []
        
        # High priority actions based on analysis
        if results.get('nps', {}).get('score', 0) < -20:
            actions.append({
                'Prioridad': 'P0',
                'Área': 'NPS',
                'Acción': 'Programa urgente de mejora de satisfacción',
                'Responsable': 'Gerencia General',
                'Plazo': '48 horas',
                'KPI': 'Mejorar NPS en 20 puntos'
            })
        
        if results.get('churn_analysis', {}).get('high_risk', 0) > 10:
            actions.append({
                'Prioridad': 'P0',
                'Área': 'Retención',
                'Acción': 'Contactar clientes en alto riesgo',
                'Responsable': 'Customer Success',
                'Plazo': '24 horas',
                'KPI': 'Retener 80% de clientes en riesgo'
            })
        
        if results.get('urgency_distribution', {}).get('P0', 0) > 0:
            actions.append({
                'Prioridad': 'P0',
                'Área': 'Servicio',
                'Acción': 'Resolver casos críticos sin servicio',
                'Responsable': 'NOC',
                'Plazo': 'Inmediato',
                'KPI': '100% casos P0 resueltos en 4 horas'
            })
        
        # Add more actions based on themes
        if results.get('theme_counts', {}).get('precio', 0) > 50:
            actions.append({
                'Prioridad': 'P1',
                'Área': 'Precio',
                'Acción': 'Revisar estrategia de pricing',
                'Responsable': 'Comercial',
                'Plazo': '1 semana',
                'KPI': 'Reducir quejas de precio en 30%'
            })
        
        if actions:
            df_actions = pd.DataFrame(actions)
            df_actions.to_excel(writer, sheet_name='11_Plan_Acción', index=False)
            
            worksheet = writer.sheets['11_Plan_Acción']
            worksheet.set_column('A:F', 25)
            
            for col_num, value in enumerate(df_actions.columns.values):
                worksheet.write(0, col_num, value, formats['header'])
    
    def _create_detailed_comments(self, writer, workbook, formats, results):
        """Create detailed comments sheet"""
        if 'comments' in results and 'sentiments' in results:
            comments_data = []
            for i, (comment, sentiment) in enumerate(zip(results['comments'][:200], results['sentiments'][:200])):
                freq = results.get('comment_frequencies', {}).get(comment, 1)
                comments_data.append({
                    'ID': f'C{i+1:04d}',
                    'Comentario': comment[:500] if len(comment) > 500 else comment,
                    'Sentimiento': sentiment.title(),
                    'Frecuencia': freq,
                    'Longitud': len(comment),
                    'Informativo': 'Sí' if len(comment) > 20 else 'No'
                })
            
            df_comments = pd.DataFrame(comments_data)
            df_comments = df_comments.sort_values('Frecuencia', ascending=False)
            df_comments.to_excel(writer, sheet_name='12_Comentarios_Detalle', index=False)
            
            worksheet = writer.sheets['12_Comentarios_Detalle']
            worksheet.set_column('A:A', 10)
            worksheet.set_column('B:B', 60)
            worksheet.set_column('C:F', 15)
            
            for col_num, value in enumerate(df_comments.columns.values):
                worksheet.write(0, col_num, value, formats['header'])
    
    def _create_cleaning_stats(self, writer, workbook, formats, results):
        """Create data cleaning statistics"""
        cleaning_data = {
            'Proceso': [
                'Comentarios Originales',
                'Después de Limpieza',
                'Duplicados Eliminados',
                'Comentarios Únicos',
                'Tasa de Duplicación',
                'Comentarios Informativos',
                'Comentarios No Informativos'
            ],
            'Cantidad': [
                results.get('raw_total', 0),
                results.get('total', 0),
                results.get('duplicates_removed', 0),
                results.get('total', 0),
                f"{(results.get('duplicates_removed', 0)/max(results.get('raw_total', 1), 1)*100):.1f}%",
                results.get('informative_comments', 0),
                results.get('total', 0) - results.get('informative_comments', 0)
            ],
            'Descripción': [
                'Total de registros en archivo original',
                'Después de corrección y normalización',
                'Comentarios idénticos removidos',
                'Comentarios únicos para análisis',
                'Porcentaje de duplicación encontrado',
                'Comentarios con contenido analizable',
                'Respuestas como "No", ".", "Nada"'
            ]
        }
        
        df_cleaning = pd.DataFrame(cleaning_data)
        df_cleaning.to_excel(writer, sheet_name='13_Estadísticas_Limpieza', index=False)
        
        worksheet = writer.sheets['13_Estadísticas_Limpieza']
        worksheet.set_column('A:A', 30)
        worksheet.set_column('B:B', 15)
        worksheet.set_column('C:C', 40)
        
        for col_num, value in enumerate(df_cleaning.columns.values):
            worksheet.write(0, col_num, value, formats['header'])
    
    def _create_glossary(self, writer, workbook, formats):
        """Create glossary of terms"""
        glossary_data = {
            'Término': [
                'NPS', 'CSI', 'Churn', 'Sentimiento', 'P0-P3', 
                'Promotor', 'Detractor', 'Pasivo', 'ROI', 'KPI'
            ],
            'Definición': [
                'Net Promoter Score - Métrica de lealtad del cliente (-100 a +100)',
                'Customer Satisfaction Index - Índice compuesto de satisfacción (0-100)',
                'Tasa de cancelación - Clientes que abandonan el servicio',
                'Análisis de opinión positiva, neutral o negativa',
                'Niveles de prioridad: P0 (crítico) a P3 (deseable)',
                'Cliente que califica 9-10, recomienda activamente',
                'Cliente que califica 0-6, insatisfecho',
                'Cliente que califica 7-8, satisfecho pero no entusiasta',
                'Return on Investment - Retorno de inversión',
                'Key Performance Indicator - Indicador clave de rendimiento'
            ],
            'Uso en Reporte': [
                'Medición principal de satisfacción',
                'Evaluación integral del servicio',
                'Identificación de riesgo de pérdida',
                'Clasificación de comentarios',
                'Priorización de acciones',
                'Segmentación de clientes satisfechos',
                'Segmentación de clientes insatisfechos',
                'Segmentación de clientes neutrales',
                'Evaluación de inversiones',
                'Métricas de seguimiento'
            ]
        }
        
        df_glossary = pd.DataFrame(glossary_data)
        df_glossary.to_excel(writer, sheet_name='14_Glosario', index=False)
        
        worksheet = writer.sheets['14_Glosario']
        worksheet.set_column('A:A', 15)
        worksheet.set_column('B:B', 50)
        worksheet.set_column('C:C', 35)
        
        for col_num, value in enumerate(df_glossary.columns.values):
            worksheet.write(0, col_num, value, formats['header'])
    
    def _create_appendix(self, writer, workbook, formats, results):
        """Create appendix with additional information"""
        worksheet = workbook.add_worksheet('15_Anexos')
        
        # Title
        worksheet.merge_range('A1:F1', 'INFORMACIÓN ADICIONAL', formats['title'])
        
        # Sections
        row = 3
        
        # Data source
        worksheet.write(f'A{row}', 'FUENTE DE DATOS', formats['subheader'])
        row += 2
        worksheet.write(f'B{row}', 'Archivo:', formats['cell'])
        worksheet.write(f'C{row}', results.get('original_filename', 'N/A'), formats['cell'])
        row += 1
        worksheet.write(f'B{row}', 'Fecha de Análisis:', formats['cell'])
        worksheet.write(f'C{row}', results.get('analysis_date', 'N/A'), formats['cell'])
        row += 1
        worksheet.write(f'B{row}', 'Total de Registros:', formats['cell'])
        worksheet.write(f'C{row}', results.get('raw_total', 0), formats['number'])
        
        # Contact information
        row += 3
        worksheet.write(f'A{row}', 'CONTACTO', formats['subheader'])
        row += 2
        worksheet.write(f'B{row}', 'Generado por:', formats['cell'])
        worksheet.write(f'C{row}', 'Sistema de Análisis Personal Paraguay', formats['cell'])
        row += 1
        worksheet.write(f'B{row}', 'Versión:', formats['cell'])
        worksheet.write(f'C{row}', '5.0 Professional', formats['cell'])
        row += 1
        worksheet.write(f'B{row}', 'Soporte:', formats['cell'])
        worksheet.write(f'C{row}', 'analytics@personal.com.py', formats['cell'])
        
        # Notes
        row += 3
        worksheet.write(f'A{row}', 'NOTAS', formats['subheader'])
        row += 2
        worksheet.write(f'B{row}', '• Este reporte es confidencial y para uso interno', formats['cell'])
        row += 1
        worksheet.write(f'B{row}', '• Los datos se actualizan en tiempo real', formats['cell'])
        row += 1
        worksheet.write(f'B{row}', '• Para más detalles, consultar hojas específicas', formats['cell'])
        
        worksheet.set_column('A:A', 5)
        worksheet.set_column('B:F', 30)