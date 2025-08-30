"""
File Processor - Core file processing logic without UI dependencies
Extracted from main.py to enable reuse across pages
"""

import pandas as pd
import logging
from typing import Dict, List, Tuple, Optional
from .analysis_engine import (
    analyze_sentiment_simple, clean_text_simple, 
    remove_duplicates_simple, extract_themes_simple,
    calculate_sentiment_percentages, generate_insights_summary,
    create_recommendations
)

logger = logging.getLogger(__name__)


class FileProcessor:
    """Handles file processing operations without UI dependencies"""
    
    def __init__(self):
        self.MAX_FILE_SIZE_MB = 1.5  # Conservative limit for Streamlit Cloud
        self.MAX_COMMENTS = 200      # Conservative limit for stability
    
    def validate_file(self, uploaded_file) -> Dict[str, any]:
        """Validate uploaded file and return validation results"""
        validation = {
            'valid': False,
            'file_size_mb': 0,
            'file_type': '',
            'error_message': None
        }
        
        try:
            # Check file exists and has content
            if not uploaded_file or not hasattr(uploaded_file, 'name'):
                validation['error_message'] = "No se proporcionó archivo válido"
                return validation
            
            # Check file size
            if hasattr(uploaded_file, 'size'):
                file_size_mb = uploaded_file.size / (1024 * 1024)
                validation['file_size_mb'] = file_size_mb
                
                if file_size_mb > self.MAX_FILE_SIZE_MB:
                    validation['error_message'] = f"Archivo demasiado grande: {file_size_mb:.1f}MB > {self.MAX_FILE_SIZE_MB}MB"
                    return validation
            
            # Check file type
            file_extension = uploaded_file.name.lower().split('.')[-1]
            validation['file_type'] = file_extension
            
            if file_extension not in ['xlsx', 'xls', 'csv']:
                validation['error_message'] = f"Formato no soportado: .{file_extension}"
                return validation
            
            validation['valid'] = True
            return validation
            
        except Exception as e:
            validation['error_message'] = f"Error validando archivo: {str(e)}"
            return validation
    
    def read_file_data(self, uploaded_file) -> Optional[pd.DataFrame]:
        """Read file data without UI dependencies"""
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file, encoding='utf-8', on_bad_lines='skip')
            else:
                # Try multiple Excel engines
                try:
                    df = pd.read_excel(uploaded_file, engine='openpyxl')
                except:
                    uploaded_file.seek(0)
                    df = pd.read_excel(uploaded_file, engine=None)
            
            return df
            
        except UnicodeDecodeError:
            # Try latin-1 encoding as fallback
            if uploaded_file.name.endswith('.csv'):
                uploaded_file.seek(0)
                df = pd.read_csv(uploaded_file, encoding='latin-1', on_bad_lines='skip')
                return df
            else:
                raise Exception("Error de codificación en archivo Excel")
                
        except Exception as e:
            logger.error(f"Error reading file: {e}")
            raise
    
    def find_comment_column(self, df: pd.DataFrame) -> Optional[str]:
        """Find the comment column in the dataframe"""
        comment_keywords = [
            'comentario final', 'comentario', 'comentarios', 'comment', 'comments',
            'feedback', 'review', 'texto', 'respuesta', 'opinion', 'observacion'
        ]
        
        # Check for exact keyword matches first
        for col in df.columns:
            col_lower = str(col).lower().strip()
            for keyword in comment_keywords:
                if keyword in col_lower:
                    return col
        
        # Fallback to first text column
        for col in df.columns:
            if df[col].dtype == 'object':
                return col
        
        return None
    
    def extract_comments(self, df: pd.DataFrame, comment_col: str) -> List[str]:
        """Extract and clean comments from dataframe"""
        try:
            # Get raw comments
            raw_comments = df[comment_col].dropna().tolist()
            
            if not raw_comments:
                raise Exception("No se encontraron comentarios válidos")
            
            # Apply size limits for stability
            if len(raw_comments) > self.MAX_COMMENTS:
                raw_comments = raw_comments[:self.MAX_COMMENTS]
            
            # Clean comments
            cleaned_comments = [clean_text_simple(comment) for comment in raw_comments]
            
            # Remove duplicates
            unique_comments, frequencies = remove_duplicates_simple(cleaned_comments)
            
            return {
                'raw_comments': raw_comments,
                'cleaned_comments': cleaned_comments,
                'unique_comments': unique_comments,
                'comment_frequencies': frequencies
            }
            
        except Exception as e:
            logger.error(f"Error extracting comments: {e}")
            raise
    
    def analyze_comments(self, comment_data: Dict, use_ai_insights: bool = False) -> Dict:
        """Perform sentiment analysis on comment data"""
        try:
            unique_comments = comment_data['unique_comments']
            comment_frequencies = comment_data['comment_frequencies']
            
            # Analyze sentiments
            sentiments = [analyze_sentiment_simple(comment) for comment in unique_comments]
            
            # Extract themes
            theme_counts, theme_examples = extract_themes_simple(unique_comments)
            
            # Calculate statistics
            sentiment_percentages = calculate_sentiment_percentages(sentiments)
            
            # Generate results with analysis method indicator
            analysis_method = 'AI_ENHANCED' if use_ai_insights else 'RULE_BASED_SIMPLE'
            
            results = {
                'total': len(unique_comments),
                'comments': unique_comments,
                'sentiments': sentiments,
                'comment_frequencies': comment_frequencies,
                'sentiment_percentages': sentiment_percentages,
                'positive_count': sentiments.count('positivo'),
                'neutral_count': sentiments.count('neutral'), 
                'negative_count': sentiments.count('negativo'),
                'theme_counts': theme_counts,
                'theme_examples': theme_examples,
                'raw_total': len(comment_data['raw_comments']),
                'duplicates_removed': len(comment_data['raw_comments']) - len(unique_comments),
                'cleaning_applied': True,
                'analysis_method': analysis_method,
                'ai_insights_enabled': use_ai_insights
            }
            
            # Add insights and recommendations (enhanced with AI if requested)
            results['insights'] = generate_insights_summary(results, enhanced_ai=use_ai_insights)
            results['recommendations'] = create_recommendations(results, enhanced_ai=use_ai_insights)
            
            return results
            
        except Exception as e:
            logger.error(f"Error analyzing comments: {e}")
            raise
    
    def process_uploaded_file(self, uploaded_file, use_ai_insights: bool = False) -> Optional[Dict]:
        """Complete file processing pipeline"""
        try:
            # Validate file
            validation = self.validate_file(uploaded_file)
            if not validation['valid']:
                raise Exception(validation['error_message'])
            
            # Read data
            df = self.read_file_data(uploaded_file)
            if df is None or df.empty:
                raise Exception("No se pudieron leer datos del archivo")
            
            # Find comment column
            comment_col = self.find_comment_column(df)
            if not comment_col:
                raise Exception("No se encontró columna de comentarios")
            
            # Extract comments
            comment_data = self.extract_comments(df, comment_col)
            
            # Analyze comments with AI enhancement if requested
            results = self.analyze_comments(comment_data, use_ai_insights)
            
            # Add file metadata
            results.update({
                'original_filename': uploaded_file.name,
                'file_size': validation['file_size_mb'],
                'file_type': validation['file_type']
            })
            
            return results
            
        except Exception as e:
            logger.error(f"Error processing file: {e}")
            raise