"""
AI Data Processor - File reading and validation responsibilities
Extracted from AIAnalysisAdapter to improve maintainability
"""

import pandas as pd
import logging
from io import BytesIO
from typing import Dict, List, Optional, Any
from pathlib import Path

logger = logging.getLogger(__name__)


class AIDataProcessor:
    """
    Handles file reading, validation, and data extraction
    Separated from main AI adapter for better maintainability
    """
    
    def __init__(self):
        # Import configuration
        from src.config import Config
        self.config = Config()
        
    def read_and_validate_file(self, uploaded_file) -> pd.DataFrame:
        """Read and validate uploaded file with proper error handling"""
        try:
            # Log file information
            logger.info(f"🚀 Reading file: {uploaded_file.name}")
            logger.debug(f"File size: {getattr(uploaded_file, 'size', 'unknown')} bytes")
            
            # Determine file type and read accordingly
            if uploaded_file.name.lower().endswith('.csv'):
                return self._read_csv_file(uploaded_file)
            else:
                return self._read_excel_file(uploaded_file)
                
        except Exception as e:
            logger.error(f"Failed to read file {uploaded_file.name}: {str(e)}")
            raise
    
    def _read_csv_file(self, uploaded_file) -> pd.DataFrame:
        """Read CSV file with proper encoding handling"""
        try:
            if hasattr(uploaded_file, 'read'):
                uploaded_file.seek(0)
                # Try UTF-8 first, fallback to latin-1 for problematic files
                try:
                    df = pd.read_csv(uploaded_file, encoding='utf-8')
                except UnicodeDecodeError:
                    uploaded_file.seek(0)
                    df = pd.read_csv(uploaded_file, encoding='latin-1')
            else:
                df = pd.read_csv(uploaded_file.content, encoding='utf-8')
            
            logger.debug(f"CSV file read successfully: {df.shape[0]} rows, {df.shape[1]} columns")
            return df
            
        except Exception as e:
            logger.error(f"Failed to read CSV file: {str(e)}")
            raise
    
    def _read_excel_file(self, uploaded_file) -> pd.DataFrame:
        """Read Excel file with proper memory management using context managers"""
        try:
            if hasattr(uploaded_file, 'read'):
                # Reset file pointer to beginning
                uploaded_file.seek(0)
                
                # Use context manager for automatic resource cleanup
                with BytesIO(uploaded_file.read()) as file_buffer:
                    df = pd.read_excel(file_buffer)
                    logger.debug(f"Excel file read successfully: {df.shape[0]} rows, {df.shape[1]} columns")
                    return df
            else:
                # Handle file content directly with context manager
                with BytesIO(uploaded_file.content) as file_buffer:
                    df = pd.read_excel(file_buffer)
                    logger.debug(f"Excel file read successfully: {df.shape[0]} rows, {df.shape[1]} columns")
                    return df
                    
        except Exception as e:
            # Context managers automatically handle cleanup even on exceptions
            logger.error(f"Failed to read Excel file: {str(e)}")
            raise
    
    def extract_analysis_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Extract and prepare data for analysis"""
        try:
            # Find comment column
            comment_col = self._find_comment_column(df)
            if not comment_col:
                raise ValueError("No comment column found in file")
            
            # Extract comments with string conversion (FIX: ensure all are strings)
            raw_comments = df[comment_col].dropna().astype(str).tolist()
            if not raw_comments:
                raise ValueError("No valid comments found in file")
            
            # Extract additional data if available
            nps_data = self._extract_nps_data(df)
            nota_data = self._extract_nota_data(df)
            
            return {
                'comments': raw_comments,
                'comment_column': comment_col,
                'nps_data': nps_data,
                'nota_data': nota_data,
                'total_rows': len(df),
                'has_nps': len(nps_data) > 0,
                'has_nota': len(nota_data) > 0
            }
            
        except Exception as e:
            logger.error(f"Failed to extract analysis data: {str(e)}")
            raise
    
    def _find_comment_column(self, df: pd.DataFrame) -> Optional[str]:
        """Find the column that contains comments"""
        comment_keywords = [
            'comentario', 'comment', 'feedback', 'review', 'opinion',
            'observacion', 'nota', 'mensaje', 'texto'
        ]
        
        for col in df.columns:
            col_lower = str(col).lower()
            if any(keyword in col_lower for keyword in comment_keywords):
                return col
        
        # Fallback: use first text column
        for col in df.columns:
            if df[col].dtype == 'object':
                return col
        
        return None
    
    def _extract_nps_data(self, df: pd.DataFrame) -> List[Any]:
        """Extract NPS data if available"""
        nps_keywords = ['nps', 'recomendacion', 'recomienda', 'satisfaction']
        
        for col in df.columns:
            col_lower = str(col).lower()
            if any(keyword in col_lower for keyword in nps_keywords):
                return df[col].tolist()
        
        return []
    
    def _extract_nota_data(self, df: pd.DataFrame) -> List[Any]:
        """Extract rating/nota data if available"""
        nota_keywords = ['nota', 'rating', 'calificacion', 'puntuacion', 'score']
        
        for col in df.columns:
            col_lower = str(col).lower()
            if any(keyword in col_lower for keyword in nota_keywords):
                return df[col].tolist()
        
        return []