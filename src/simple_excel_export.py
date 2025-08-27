"""
Simple Excel Export - Just the essentials in 3 sheets
What users actually need, not a 16-sheet novel
"""

import pandas as pd
from io import BytesIO
import xlsxwriter
from datetime import datetime

class SimpleExcelExporter:
    """Export results to a simple 3-sheet Excel file"""
    
    def create_simple_excel(self, results):
        """
        Create a simple Excel with just 3 essential sheets:
        1. Summary - Key metrics and insights
        2. Details - Comment list with sentiments
        3. Charts - Visual representation
        """
        output = BytesIO()
        
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            workbook = writer.book
            
            # Define simple, clean formats
            formats = self._create_simple_formats(workbook)
            
            # Sheet 1: Executive Summary (1 page)
            self._create_summary_sheet(writer, workbook, formats, results)
            
            # Sheet 2: Comment Details
            self._create_details_sheet(writer, workbook, formats, results)
            
            # Sheet 3: Visual Dashboard
            self._create_dashboard_sheet(writer, workbook, formats, results)
            
        output.seek(0)
        return output.getvalue()
    
    def _create_simple_formats(self, workbook):
        """Create minimal, clean formats"""
        return {
            'title': workbook.add_format({
                'bold': True,
                'font_size': 16,
                'align': 'center',
                'valign': 'vcenter',
                'font_color': '#1a1a1a'
            }),
            'header': workbook.add_format({
                'bold': True,
                'font_size': 11,
                'bg_color': '#f0f0f0',
                'border': 1,
                'align': 'center',
                'valign': 'vcenter'
            }),
            'cell': workbook.add_format({
                'font_size': 10,
                'border': 1,
                'align': 'left',
                'valign': 'top',
                'text_wrap': True
            }),
            'number': workbook.add_format({
                'font_size': 10,
                'border': 1,
                'align': 'center',
                'num_format': '#,##0'
            }),
            'percent': workbook.add_format({
                'font_size': 10,
                'border': 1,
                'align': 'center',
                'num_format': '0.0%'
            }),
            'positive': workbook.add_format({
                'font_size': 10,
                'border': 1,
                'font_color': '#10b981',
                'bold': True,
                'align': 'center'
            }),
            'negative': workbook.add_format({
                'font_size': 10,
                'border': 1,
                'font_color': '#ef4444',
                'bold': True,
                'align': 'center'
            }),
            'neutral': workbook.add_format({
                'font_size': 10,
                'border': 1,
                'font_color': '#6b7280',
                'align': 'center'
            })
        }
    
    def _create_summary_sheet(self, writer, workbook, formats, results):
        """Create one-page executive summary"""
        worksheet = workbook.add_worksheet('Summary')
        
        # Set column widths
        worksheet.set_column('A:A', 30)
        worksheet.set_column('B:B', 20)
        
        row = 0
        
        # Title
        worksheet.merge_range(row, 0, row, 1, 'Comment Analysis Summary', formats['title'])
        row += 2
        
        # Key Metrics
        worksheet.write(row, 0, 'Analysis Date', formats['header'])
        worksheet.write(row, 1, results.get('analysis_date', datetime.now().strftime('%Y-%m-%d')), formats['cell'])
        row += 1
        
        worksheet.write(row, 0, 'File Analyzed', formats['header'])
        worksheet.write(row, 1, results.get('original_filename', 'N/A'), formats['cell'])
        row += 1
        
        worksheet.write(row, 0, 'Total Comments', formats['header'])
        worksheet.write(row, 1, results.get('total', 0), formats['number'])
        row += 2
        
        # Sentiment Breakdown
        worksheet.write(row, 0, 'SENTIMENT ANALYSIS', formats['header'])
        worksheet.write(row, 1, '', formats['header'])
        row += 1
        
        worksheet.write(row, 0, 'Positive', formats['cell'])
        positive_pct = results.get('positive_pct', 0) / 100
        worksheet.write(row, 1, positive_pct, formats['positive'])
        row += 1
        
        worksheet.write(row, 0, 'Neutral', formats['cell'])
        neutral_pct = results.get('neutral_pct', 0) / 100
        worksheet.write(row, 1, neutral_pct, formats['neutral'])
        row += 1
        
        worksheet.write(row, 0, 'Negative', formats['cell'])
        negative_pct = results.get('negative_pct', 0) / 100
        worksheet.write(row, 1, negative_pct, formats['negative'])
        row += 2
        
        # Top Issues (if available)
        if results.get('theme_counts'):
            worksheet.write(row, 0, 'TOP THEMES DETECTED', formats['header'])
            worksheet.write(row, 1, 'Count', formats['header'])
            row += 1
            
            themes = sorted(results['theme_counts'].items(), key=lambda x: x[1], reverse=True)[:5]
            for theme, count in themes:
                worksheet.write(row, 0, theme.replace('_', ' ').title(), formats['cell'])
                worksheet.write(row, 1, count, formats['number'])
                row += 1
        
        # Add a simple pie chart
        if results.get('total', 0) > 0:
            chart = workbook.add_chart({'type': 'pie'})
            chart.add_series({
                'categories': ['Summary', 6, 0, 8, 0],  # Sentiment labels
                'values': ['Summary', 6, 1, 8, 1],      # Sentiment percentages
                'name': 'Sentiment Distribution'
            })
            chart.set_title({'name': 'Sentiment Distribution'})
            chart.set_size({'width': 360, 'height': 280})
            worksheet.insert_chart('D2', chart)
    
    def _create_details_sheet(self, writer, workbook, formats, results):
        """Create detailed comments sheet"""
        if not results.get('comments'):
            return
        
        # Create DataFrame with comments and sentiments
        df_details = pd.DataFrame({
            'Comment': results.get('comments', [])[:500],  # Limit to 500 for performance
            'Sentiment': results.get('sentiments', [])[:500]
        })
        
        # Add sentiment coloring
        df_details.to_excel(writer, sheet_name='Details', index=False)
        
        worksheet = writer.sheets['Details']
        
        # Format headers
        for col_num, value in enumerate(df_details.columns.values):
            worksheet.write(0, col_num, value, formats['header'])
        
        # Format data rows with sentiment coloring
        for row_num, (comment, sentiment) in enumerate(zip(df_details['Comment'], df_details['Sentiment']), start=1):
            worksheet.write(row_num, 0, comment, formats['cell'])
            
            # Color-code sentiment
            if sentiment == 'positive':
                sentiment_format = formats['positive']
            elif sentiment == 'negative':
                sentiment_format = formats['negative']
            else:
                sentiment_format = formats['neutral']
            
            worksheet.write(row_num, 1, sentiment.title(), sentiment_format)
        
        # Set column widths
        worksheet.set_column('A:A', 80)  # Comments
        worksheet.set_column('B:B', 15)  # Sentiment
    
    def _create_dashboard_sheet(self, writer, workbook, formats, results):
        """Create visual dashboard sheet"""
        worksheet = workbook.add_worksheet('Dashboard')
        
        # Title
        worksheet.merge_range(0, 0, 0, 4, 'Visual Dashboard', formats['title'])
        
        # Create data table for chart
        data = [
            ['Metric', 'Value'],
            ['Positive', results.get('positive_count', 0)],
            ['Neutral', results.get('neutral_count', 0)],
            ['Negative', results.get('negative_count', 0)]
        ]
        
        for row_num, row_data in enumerate(data, start=2):
            for col_num, value in enumerate(row_data):
                if row_num == 2:
                    worksheet.write(row_num, col_num, value, formats['header'])
                else:
                    worksheet.write(row_num, col_num, value, formats['cell'] if col_num == 0 else formats['number'])
        
        # Add multiple charts
        # 1. Bar chart
        bar_chart = workbook.add_chart({'type': 'column'})
        bar_chart.add_series({
            'categories': ['Dashboard', 3, 0, 5, 0],
            'values': ['Dashboard', 3, 1, 5, 1],
            'name': 'Comment Count',
            'data_labels': {'value': True}
        })
        bar_chart.set_title({'name': 'Sentiment Distribution'})
        bar_chart.set_x_axis({'name': 'Sentiment'})
        bar_chart.set_y_axis({'name': 'Count'})
        bar_chart.set_size({'width': 480, 'height': 320})
        worksheet.insert_chart('D2', bar_chart)
        
        # 2. Pie chart
        pie_chart = workbook.add_chart({'type': 'pie'})
        pie_chart.add_series({
            'categories': ['Dashboard', 3, 0, 5, 0],
            'values': ['Dashboard', 3, 1, 5, 1],
            'name': 'Percentage Distribution',
            'data_labels': {'percentage': True}
        })
        pie_chart.set_title({'name': 'Sentiment Percentage'})
        pie_chart.set_size({'width': 480, 'height': 320})
        worksheet.insert_chart('D18', pie_chart)
        
        # Add key insights if available
        if results.get('insights'):
            row = 8
            worksheet.write(row, 0, 'KEY INSIGHTS', formats['header'])
            row += 1
            
            for i, insight in enumerate(results.get('insights', [])[:3], 1):
                insight_text = f"{i}. {insight.get('insight', '')}"
                worksheet.merge_range(row, 0, row, 3, insight_text, formats['cell'])
                row += 1
        
        # Hide gridlines for cleaner look
        worksheet.hide_gridlines(2)