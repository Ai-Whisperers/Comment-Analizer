"""
Export Manager Module
Handles exporting analysis results to various formats (PDF, Excel, CSV)
"""

import pandas as pd
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import io
import base64
from src.config import Config

class ExportManager:
    """Class to handle exporting analysis results"""
    
    def __init__(self):
        self.output_path = Path(Config.OUTPUTS_PATH)
        self.output_path.mkdir(exist_ok=True, parents=True)
        
        # Create subdirectories
        (self.output_path / "reports").mkdir(exist_ok=True)
        (self.output_path / "exports").mkdir(exist_ok=True)
        (self.output_path / "visualizations").mkdir(exist_ok=True)
    
    def export_to_excel(self, 
                       analysis_results: List[Dict], 
                       insights: Dict, 
                       recommendations: List[str],
                       original_comments: List[str] = None) -> str:
        """Export analysis results to Excel file"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"personal_paraguay_analysis_{timestamp}.xlsx"
        filepath = self.output_path / "exports" / filename
        
        with pd.ExcelWriter(filepath, engine='xlsxwriter') as writer:
            
            # Main results sheet
            if analysis_results:
                results_df = pd.DataFrame(analysis_results)
                if original_comments and len(original_comments) == len(results_df):
                    results_df['original_comment'] = original_comments
                results_df.to_excel(writer, sheet_name='Analysis_Results', index=False)
            
            # Insights summary sheet
            insights_data = []
            insights_data.append(['Total Comments', insights.get('total_comments', 0)])
            insights_data.append(['Average Confidence', insights.get('avg_confidence', 0)])
            insights_data.append(['Guarani Percentage', f"{insights.get('guarani_percentage', 0)}%"])
            
            # Sentiment distribution
            sentiment_dist = insights.get('sentiment_percentages', {})
            for sentiment, percentage in sentiment_dist.items():
                insights_data.append([f'Sentiment: {sentiment.title()}', f"{percentage}%"])
            
            insights_df = pd.DataFrame(insights_data, columns=['Metric', 'Value'])
            insights_df.to_excel(writer, sheet_name='Summary', index=False)
            
            # Top themes sheet
            themes = insights.get('top_themes', {})
            if themes:
                themes_df = pd.DataFrame(list(themes.items()), columns=['Theme', 'Count'])
                themes_df.to_excel(writer, sheet_name='Top_Themes', index=False)
            
            # Pain points sheet
            pain_points = insights.get('top_pain_points', {})
            if pain_points:
                pain_points_df = pd.DataFrame(list(pain_points.items()), 
                                             columns=['Pain_Point', 'Count'])
                pain_points_df.to_excel(writer, sheet_name='Pain_Points', index=False)
            
            # Recommendations sheet
            if recommendations:
                rec_df = pd.DataFrame(recommendations, columns=['Recommendation'])
                rec_df.to_excel(writer, sheet_name='Recommendations', index=False)
        
        return str(filepath)
    
    def export_to_csv(self, analysis_results: List[Dict], original_comments: List[str] = None) -> str:
        """Export detailed results to CSV"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"personal_paraguay_detailed_{timestamp}.csv"
        filepath = self.output_path / "exports" / filename
        
        if analysis_results:
            results_df = pd.DataFrame(analysis_results)
            if original_comments and len(original_comments) == len(results_df):
                results_df['original_comment'] = original_comments
            results_df.to_csv(filepath, index=False, encoding='utf-8')
        
        return str(filepath)
    
    def create_summary_report(self, 
                             insights: Dict, 
                             recommendations: List[str],
                             analysis_date: str = None) -> str:
        """Create a text-based summary report"""
        
        if not analysis_date:
            analysis_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"personal_paraguay_summary_{timestamp}.txt"
        filepath = self.output_path / "reports" / filename
        
        report_content = f"""
PERSONAL PARAGUAY - CUSTOMER COMMENTS ANALYSIS REPORT
Generated: {analysis_date}

EXECUTIVE SUMMARY
==================
Total Comments Analyzed: {insights.get('total_comments', 0)}
Analysis Confidence: {insights.get('avg_confidence', 0):.2f}
Guarani Content: {insights.get('guarani_percentage', 0)}%

SENTIMENT DISTRIBUTION
=====================
"""
        
        sentiment_dist = insights.get('sentiment_percentages', {})
        for sentiment, percentage in sentiment_dist.items():
            report_content += f"{sentiment.title()}: {percentage}%\n"
        
        report_content += "\nTOP THEMES\n=========\n"
        themes = insights.get('top_themes', {})
        for i, (theme, count) in enumerate(themes.items(), 1):
            report_content += f"{i}. {theme}: {count} mentions\n"
        
        report_content += "\nTOP PAIN POINTS\n==============\n"
        pain_points = insights.get('top_pain_points', {})
        for i, (pain_point, count) in enumerate(pain_points.items(), 1):
            report_content += f"{i}. {pain_point}: {count} mentions\n"
        
        report_content += "\nRECOMMENDATIONS\n==============\n"
        for i, recommendation in enumerate(recommendations, 1):
            report_content += f"{i}. {recommendation}\n"
        
        report_content += "\nLANGUAGE DISTRIBUTION\n===================\n"
        lang_dist = insights.get('language_distribution', {})
        for language, count in lang_dist.items():
            lang_name = {'es': 'Spanish', 'gn': 'Guarani', 'mixed': 'Mixed'}.get(language, language)
            report_content += f"{lang_name}: {count} comments\n"
        
        report_content += f"\n\nReport generated by Personal Paraguay Fiber Comments Analysis System"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        return str(filepath)
    
    def export_insights_json(self, insights: Dict, recommendations: List[str]) -> str:
        """Export insights and recommendations as JSON"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"personal_paraguay_insights_{timestamp}.json"
        filepath = self.output_path / "exports" / filename
        
        export_data = {
            "analysis_date": datetime.now().isoformat(),
            "insights": insights,
            "recommendations": recommendations,
            "export_info": {
                "system": "Personal Paraguay Fiber Comments Analysis",
                "version": "1.0",
                "export_format": "JSON"
            }
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        return str(filepath)
    
    def get_download_link(self, filepath: str, link_text: str = "Download") -> str:
        """Generate download link for Streamlit"""
        
        try:
            with open(filepath, 'rb') as f:
                file_data = f.read()
            
            b64_data = base64.b64encode(file_data).decode()
            file_extension = Path(filepath).suffix.lower()
            
            # Set MIME type based on extension
            mime_types = {
                '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                '.csv': 'text/csv',
                '.txt': 'text/plain',
                '.json': 'application/json'
            }
            
            mime_type = mime_types.get(file_extension, 'application/octet-stream')
            filename = Path(filepath).name
            
            download_link = f'<a href="data:{mime_type};base64,{b64_data}" download="{filename}">{link_text}</a>'
            return download_link
            
        except Exception as e:
            return f"Error creating download link: {str(e)}"
    
    def cleanup_old_files(self, days_old: int = 7):
        """Clean up export files older than specified days"""
        
        cutoff_date = datetime.now().timestamp() - (days_old * 24 * 60 * 60)
        
        for directory in [self.output_path / "exports", self.output_path / "reports"]:
            if directory.exists():
                for file_path in directory.glob("*"):
                    if file_path.is_file() and file_path.stat().st_mtime < cutoff_date:
                        try:
                            file_path.unlink()
                        except Exception:
                            pass  # Ignore cleanup errors

# Example usage
if __name__ == "__main__":
    # Test export functionality
    sample_results = [
        {
            "sentiment": "positive",
            "confidence": 0.95,
            "language": "es",
            "themes": ["velocidad", "calidad"],
            "pain_points": []
        },
        {
            "sentiment": "negative", 
            "confidence": 0.85,
            "language": "es",
            "themes": ["instalacion"],
            "pain_points": ["demora"]
        }
    ]
    
    sample_insights = {
        "total_comments": 2,
        "sentiment_percentages": {"positive": 50, "negative": 50},
        "top_themes": {"velocidad": 1, "instalacion": 1},
        "top_pain_points": {"demora": 1},
        "avg_confidence": 0.90,
        "guarani_percentage": 0
    }
    
    sample_recommendations = [
        "Mejorar tiempos de instalacion",
        "Mantener calidad de velocidad"
    ]
    
    exporter = ExportManager()
    
    # Test exports
    excel_file = exporter.export_to_excel(sample_results, sample_insights, sample_recommendations)
    csv_file = exporter.export_to_csv(sample_results)
    summary_file = exporter.create_summary_report(sample_insights, sample_recommendations)
    json_file = exporter.export_insights_json(sample_insights, sample_recommendations)
    
    print(f"Excel exported to: {excel_file}")
    print(f"CSV exported to: {csv_file}")
    print(f"Summary exported to: {summary_file}")
    print(f"JSON exported to: {json_file}")