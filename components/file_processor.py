"""
File Processing Component - Streamlit Native Caching
Handles Excel/CSV processing with automatic caching based on file content hash
"""

import streamlit as st
import pandas as pd
import hashlib
from typing import List, Dict, Tuple, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@st.cache_data(ttl=3600, show_spinner="Procesando archivo...")
def process_file_content(file_content: bytes, file_name: str) -> Tuple[List[str], Dict[str, Any]]:
    """
    Process uploaded Excel/CSV file with Streamlit native caching
    
    Cache Strategy:
    - TTL: 1 hour (reasonable for file reprocessing)
    - Key: Automatic based on file content hash + name
    - Benefit: Identical files load instantly
    
    Args:
        file_content: Raw file bytes
        file_name: Original file name
        
    Returns:
        Tuple of (comments_list, metadata_dict)
    """
    try:
        # Determine file type and process accordingly
        if file_name.lower().endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file_content, engine='openpyxl')
        elif file_name.lower().endswith('.csv'):
            # Try different encodings for CSV robustness
            try:
                df = pd.read_csv(file_content)
            except UnicodeDecodeError:
                df = pd.read_csv(file_content, encoding='latin-1')
        else:
            raise ValueError(f"Tipo de archivo no soportado: {file_name}")
        
        # Extract comments with smart column detection
        comments = extract_comments_from_dataframe(df)
        
        # Generate comprehensive metadata
        metadata = {
            'file_name': file_name,
            'total_rows': len(df),
            'valid_comments': len(comments),
            'columns': df.columns.tolist(),
            'file_size_bytes': len(file_content),
            'file_size_mb': len(file_content) / (1024 * 1024),
            'processed_at': datetime.now().isoformat(),
            'file_hash': hashlib.md5(file_content).hexdigest()[:8],
            'comment_avg_length': sum(len(c) for c in comments) / len(comments) if comments else 0
        }
        
        logger.info(f"📁 File processed: {len(comments)} comments from {file_name}")
        return comments, metadata
        
    except Exception as e:
        logger.error(f"❌ Error processing file {file_name}: {str(e)}")
        st.error(f"Error procesando archivo: {e}")
        return [], {
            'file_name': file_name,
            'error': str(e),
            'processed_at': datetime.now().isoformat()
        }


@st.cache_data(ttl=600)
def extract_comments_from_dataframe(df: pd.DataFrame) -> List[str]:
    """
    Extract comments from DataFrame with smart column detection and caching
    
    Cache Strategy:
    - TTL: 10 minutes (reasonable for column detection)
    - Handles various column naming patterns
    """
    possible_comment_columns = [
        'comentario', 'comentarios', 'comment', 'comments',
        'texto', 'text', 'mensaje', 'message',
        'opinion', 'feedback', 'review'
    ]
    
    comment_column = None
    
    # Smart column detection (case-insensitive)
    for col in df.columns:
        col_lower = col.lower().strip()
        if col_lower in possible_comment_columns:
            comment_column = col
            break
    
    # If no exact match, look for partial matches
    if not comment_column:
        for col in df.columns:
            col_lower = col.lower().strip()
            for pattern in ['coment', 'text', 'mensaje']:
                if pattern in col_lower:
                    comment_column = col
                    break
            if comment_column:
                break
    
    # Default to first text column if nothing found
    if not comment_column:
        text_columns = df.select_dtypes(include=['object']).columns
        if len(text_columns) > 0:
            comment_column = text_columns[0]
            logger.warning(f"⚠️ No comment column found, using: {comment_column}")
        else:
            logger.error("❌ No text columns found in file")
            return []
    
    # Extract and clean comments
    comments_series = df[comment_column].dropna()
    comments = []
    
    for comment in comments_series:
        comment_str = str(comment).strip()
        # Filter out very short or invalid comments
        if len(comment_str) >= 10 and comment_str.lower() not in ['n/a', 'none', 'null', '']:
            comments.append(comment_str)
    
    logger.info(f"📊 Extracted {len(comments)} valid comments from column '{comment_column}'")
    return comments


@st.cache_data(ttl=300)
def generate_file_preview(comments: List[str], metadata: Dict[str, Any], max_preview: int = 5) -> str:
    """
    Generate file preview with caching for UI display
    
    Cache Strategy:
    - TTL: 5 minutes (UI preview data)
    - Short TTL since preview is lightweight
    """
    if not comments:
        return "📄 **Vista previa:** No se encontraron comentarios válidos"
    
    preview_count = min(len(comments), max_preview)
    preview_comments = []
    
    for i in range(preview_count):
        comment = comments[i]
        # Truncate long comments for preview
        display_comment = comment[:150] + "..." if len(comment) > 150 else comment
        preview_comments.append(f"{i+1}. {display_comment}")
    
    preview_text = f"""
📄 **Vista previa del archivo:**

**📊 Estadísticas:**
- Total comentarios válidos: {len(comments)}
- Promedio de caracteres: {metadata.get('comment_avg_length', 0):.0f}
- Archivo: {metadata.get('file_name', 'Desconocido')}

**📝 Primeros {preview_count} comentarios:**
{chr(10).join(preview_comments)}
"""

    if len(comments) > max_preview:
        preview_text += f"\n\n*... y {len(comments) - max_preview} comentarios más*"
    
    return preview_text


@st.cache_data(ttl=3600)
def validate_file_structure(df: pd.DataFrame, file_name: str) -> Dict[str, Any]:
    """
    Validate file structure with comprehensive caching
    
    Cache Strategy:
    - TTL: 1 hour (structure validation rarely changes)
    - Comprehensive validation for user feedback
    """
    validation_result = {
        'is_valid': True,
        'issues': [],
        'warnings': [],
        'recommendations': [],
        'column_analysis': {}
    }
    
    # Check basic structure
    if len(df) == 0:
        validation_result['is_valid'] = False
        validation_result['issues'].append("Archivo vacío")
        return validation_result
    
    # Analyze columns
    text_columns = df.select_dtypes(include=['object']).columns.tolist()
    numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
    
    validation_result['column_analysis'] = {
        'total_columns': len(df.columns),
        'text_columns': text_columns,
        'numeric_columns': numeric_columns,
        'total_rows': len(df)
    }
    
    # Check for comment-like columns
    comment_patterns = ['coment', 'text', 'mensaje', 'opinion', 'feedback']
    potential_comment_columns = []
    
    for col in text_columns:
        col_lower = col.lower()
        for pattern in comment_patterns:
            if pattern in col_lower:
                potential_comment_columns.append(col)
                break
    
    if not potential_comment_columns:
        validation_result['warnings'].append(
            "No se detectaron columnas de comentarios obvias. "
            "Se usará la primera columna de texto disponible."
        )
    
    # Check data quality
    if len(df) > 2000:
        validation_result['warnings'].append(
            f"Archivo grande ({len(df)} filas). "
            "Consider processing in smaller files for better performance."
        )
    
    # Recommendations
    if len(text_columns) > 1:
        validation_result['recommendations'].append(
            "Múltiples columnas de texto detectadas. "
            f"Se usará: {potential_comment_columns[0] if potential_comment_columns else text_columns[0]}"
        )
    
    return validation_result


@st.cache_data(ttl=1800)
def calculate_processing_estimate(num_comments: int, batch_size: int = 50) -> Dict[str, float]:
    """
    Calculate processing time estimates with caching
    
    Cache Strategy:
    - TTL: 30 minutes (estimates don't change frequently)
    - Based on optimized performance parameters
    """
    num_batches = (num_comments + batch_size - 1) // batch_size
    
    # Optimized timing estimates (after performance improvements)
    processing_per_batch = 3.0  # Average AI processing time per batch
    pause_per_batch = 0.2       # Minimal rate limiting pause
    overhead = 2.0              # File processing + UI overhead
    
    total_processing_time = (num_batches * processing_per_batch) + \
                           ((num_batches - 1) * pause_per_batch) + \
                           overhead
    
    return {
        'estimated_total_seconds': total_processing_time,
        'estimated_minutes': total_processing_time / 60,
        'num_batches': num_batches,
        'batch_size': batch_size,
        'processing_per_batch': processing_per_batch
    }