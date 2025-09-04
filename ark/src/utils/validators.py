"""
Input Validation and Sanitization Module
Provides comprehensive validation for all user inputs to prevent security vulnerabilities
"""

import re
import html
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Union
import pandas as pd
import logging

# File type detection disabled to avoid dependency issues
HAS_MAGIC = False
magic = None

logger = logging.getLogger(__name__)

class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass

class InputValidator:
    """Comprehensive input validation and sanitization"""
    
    # File validation constants
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    ALLOWED_EXTENSIONS = {'.xlsx', '.csv', '.json', '.txt'}
    ALLOWED_MIME_TYPES = {
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'text/csv',
        'application/json',
        'text/plain'
    }
    
    # Text validation constants
    MAX_COMMENT_LENGTH = 5000
    MAX_COMMENTS_PER_BATCH = 1000
    MIN_COMMENT_LENGTH = 1
    
    # SQL injection patterns
    SQL_INJECTION_PATTERNS = [
        r'(\'|(\'\')|(\;)|\b(or|and)\b.*?(\=|like|\<|\>))',
        r'(union|select|insert|delete|update|drop|create|alter)',
        r'(\-\-|\#|\/\*|\*\/)',
        r'(script|javascript|vbscript|onload|onerror)',
        r'(xp_|sp_|exec|execute)'
    ]
    
    @staticmethod
    def validate_file_upload(uploaded_file) -> Tuple[bool, str]:
        """
        Validate uploaded file for security and format compliance
        
        Args:
            uploaded_file: Streamlit UploadedFile object
            
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        try:
            # Check file size
            if uploaded_file.size > InputValidator.MAX_FILE_SIZE:
                return False, f"File too large. Maximum size is {InputValidator.MAX_FILE_SIZE // (1024*1024)}MB"
            
            if uploaded_file.size == 0:
                return False, "File is empty"
            
            # Check file extension
            file_extension = Path(uploaded_file.name).suffix.lower()
            if file_extension not in InputValidator.ALLOWED_EXTENSIONS:
                return False, f"Unsupported file type. Allowed: {', '.join(InputValidator.ALLOWED_EXTENSIONS)}"
            
            # Check file content type (basic)
            if hasattr(uploaded_file, 'type') and uploaded_file.type:
                if uploaded_file.type not in InputValidator.ALLOWED_MIME_TYPES:
                    logger.warning(f"Suspicious MIME type: {uploaded_file.type}")
            
            # Check filename for suspicious content
            if not InputValidator._is_safe_filename(uploaded_file.name):
                return False, "Invalid filename. Use only letters, numbers, dots, hyphens, and underscores"
            
            return True, "Valid file"
            
        except Exception as e:
            logger.error(f"File validation error: {e}")
            return False, "File validation failed"
    
    @staticmethod
    def validate_comment_text(comment: str) -> Tuple[bool, str]:
        """
        Validate and sanitize comment text
        
        Args:
            comment: Raw comment text
            
        Returns:
            Tuple[bool, str]: (is_valid, sanitized_comment_or_error)
        """
        try:
            if not comment or not isinstance(comment, str):
                return False, "Comment must be a non-empty string"
            
            # Check length
            if len(comment) < InputValidator.MIN_COMMENT_LENGTH:
                return False, "Comment too short"
            
            if len(comment) > InputValidator.MAX_COMMENT_LENGTH:
                return False, f"Comment too long. Maximum {InputValidator.MAX_COMMENT_LENGTH} characters"
            
            # Check for SQL injection patterns
            for pattern in InputValidator.SQL_INJECTION_PATTERNS:
                if re.search(pattern, comment.lower()):
                    logger.warning(f"Potential SQL injection attempt blocked: {pattern}")
                    return False, "Comment contains potentially harmful content"
            
            # Sanitize HTML/script tags
            sanitized = html.escape(comment)
            
            # Remove potential script tags
            sanitized = re.sub(r'<script[^>]*>.*?</script>', '', sanitized, flags=re.IGNORECASE | re.DOTALL)
            
            # Remove excessive whitespace
            sanitized = re.sub(r'\s+', ' ', sanitized).strip()
            
            return True, sanitized
            
        except Exception as e:
            logger.error(f"Comment validation error: {e}")
            return False, "Comment validation failed"
    
    @staticmethod
    def validate_comment_batch(comments: List[str]) -> Tuple[bool, List[str], List[str]]:
        """
        Validate a batch of comments
        
        Args:
            comments: List of comment strings
            
        Returns:
            Tuple[bool, List[str], List[str]]: (all_valid, sanitized_comments, errors)
        """
        if not comments or len(comments) == 0:
            return False, [], ["No comments provided"]
        
        if len(comments) > InputValidator.MAX_COMMENTS_PER_BATCH:
            return False, [], [f"Too many comments. Maximum {InputValidator.MAX_COMMENTS_PER_BATCH} per batch"]
        
        sanitized_comments = []
        errors = []
        all_valid = True
        
        for i, comment in enumerate(comments):
            is_valid, result = InputValidator.validate_comment_text(comment)
            
            if is_valid:
                sanitized_comments.append(result)
            else:
                sanitized_comments.append("")  # Keep position but mark as invalid
                errors.append(f"Comment {i+1}: {result}")
                all_valid = False
        
        return all_valid, sanitized_comments, errors
    
    @staticmethod
    def validate_analysis_parameters(sample_size: int, total_comments: int) -> Tuple[bool, str]:
        """
        Validate analysis parameters
        
        Args:
            sample_size: Number of comments to analyze
            total_comments: Total available comments
            
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        if sample_size <= 0:
            return False, "Sample size must be positive"
        
        if sample_size > total_comments:
            return False, f"Sample size ({sample_size}) cannot exceed total comments ({total_comments})"
        
        if sample_size > InputValidator.MAX_COMMENTS_PER_BATCH:
            return False, f"Sample size too large. Maximum {InputValidator.MAX_COMMENTS_PER_BATCH} comments"
        
        return True, "Valid parameters"
    
    @staticmethod
    def sanitize_export_filename(filename: str) -> str:
        """
        Sanitize filename for export operations
        
        Args:
            filename: Proposed filename
            
        Returns:
            str: Sanitized filename
        """
        # Remove path separators and dangerous characters
        sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
        
        # Remove control characters
        sanitized = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', sanitized)
        
        # Limit length
        if len(sanitized) > 100:
            name, ext = Path(sanitized).stem, Path(sanitized).suffix
            sanitized = name[:95] + ext
        
        # Ensure it's not empty
        if not sanitized or sanitized.isspace():
            sanitized = "export_file"
        
        return sanitized
    
    @staticmethod
    def validate_dataframe_content(df: pd.DataFrame) -> Tuple[bool, str]:
        """
        Validate DataFrame content for suspicious data
        
        Args:
            df: Pandas DataFrame
            
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        try:
            # Check size limits
            if len(df) == 0:
                return False, "No data found in file"
            
            if len(df) > 20000:  # Updated limit per user requirement
                return False, "Dataset too large. Maximum 20,000 rows supported"
            
            # Check for suspicious column names
            suspicious_columns = ['password', 'token', 'secret', 'key', 'admin']
            for col in df.columns:
                if any(sus in col.lower() for sus in suspicious_columns):
                    logger.warning(f"Suspicious column name detected: {col}")
            
            # Validate text columns
            text_columns = df.select_dtypes(include=['object']).columns
            
            for col in text_columns[:3]:  # Check first 3 text columns
                sample_texts = df[col].dropna().head(10).astype(str)
                
                for text in sample_texts:
                    # Check for extremely long text (potential attack)
                    if len(text) > InputValidator.MAX_COMMENT_LENGTH * 2:
                        return False, f"Text in column '{col}' is suspiciously long"
                    
                    # Check for binary content
                    if any(ord(char) < 32 and char not in '\t\n\r' for char in text[:100]):
                        return False, f"Binary content detected in column '{col}'"
            
            return True, "Valid DataFrame content"
            
        except Exception as e:
            logger.error(f"DataFrame validation error: {e}")
            return False, "Content validation failed"
    
    @staticmethod
    def _is_safe_filename(filename: str) -> bool:
        """Check if filename is safe (no path traversal, etc.)"""
        # Check for path traversal
        if '..' in filename or '/' in filename or '\\' in filename:
            return False
        
        # Check for control characters
        if any(ord(char) < 32 for char in filename):
            return False
        
        # Check reasonable length
        if len(filename) > 255:
            return False
        
        # Check for dangerous patterns
        dangerous_patterns = ['con', 'prn', 'aux', 'nul', 'com1', 'lpt1']
        if Path(filename).stem.lower() in dangerous_patterns:
            return False
        
        return True

class SecurityLogger:
    """Centralized security event logging"""
    
    @staticmethod
    def log_validation_failure(event_type: str, details: str, user_info: str = "unknown"):
        """Log security validation failures"""
        logger.warning(f"SECURITY: {event_type} - {details} - User: {user_info}")
    
    @staticmethod
    def log_suspicious_activity(activity: str, details: str, user_info: str = "unknown"):
        """Log suspicious user activity"""
        logger.error(f"SECURITY ALERT: {activity} - {details} - User: {user_info}")

class Validators:
    """Simplified validator class for backward compatibility"""
    
    def __init__(self):
        self.validator = InputValidator()
    
    def validate_file_extension(self, filename: str) -> bool:
        """Validate file extension"""
        try:
            ext = Path(filename).suffix.lower()
            return ext in InputValidator.ALLOWED_EXTENSIONS
        except Exception as e:
            logger.error(f"Error validating file extension for '{filename}': {str(e)}")
            return False
    
    def validate_dataframe(self, df) -> bool:
        """Validate DataFrame"""
        if df is None or not isinstance(df, pd.DataFrame):
            return False
        return len(df) > 0
    
    def validate_comment(self, comment) -> bool:
        """Validate comment text"""
        if not comment or not isinstance(comment, str):
            return False
        return len(comment.strip()) > 0
    
    def validate_comment_content(self, comment: str) -> bool:
        """Validate comment content for security and appropriateness"""
        if not comment or not isinstance(comment, str):
            return False
        
        # Check basic length requirements
        if len(comment.strip()) == 0 or len(comment) > 10000:
            return False
        
        # Check for potential SQL injection patterns
        sql_patterns = [
            r'\bselect\b.*\bfrom\b',
            r'\binsert\b.*\binto\b',
            r'\bupdate\b.*\bset\b',
            r'\bdelete\b.*\bfrom\b',
            r'\bdrop\b.*\btable\b',
            r'\bunion\b.*\bselect\b',
            r';\s*--',
            r'/\*.*\*/'
        ]
        
        comment_lower = comment.lower()
        for pattern in sql_patterns:
            if re.search(pattern, comment_lower, re.IGNORECASE):
                logger.warning(f"Potential SQL injection detected: {pattern}")
                return False
        
        # Check for script injection patterns
        script_patterns = [
            r'<script[^>]*>',
            r'</script>',
            r'javascript:',
            r'on\w+\s*=',
            r'eval\s*\(',
            r'document\.',
            r'window\.',
            r'<iframe',
            r'<object',
            r'<embed'
        ]
        
        for pattern in script_patterns:
            if re.search(pattern, comment, re.IGNORECASE):
                logger.warning(f"Potential script injection detected: {pattern}")
                return False
        
        # Check for excessive repeated characters (spam detection)
        if len(set(comment.lower())) < 3 and len(comment) > 50:
            logger.warning("Potential spam detected: too few unique characters")
            return False
        
        # Check for excessive capitalization
        if len(comment) > 20:
            caps_ratio = sum(1 for c in comment if c.isupper()) / len(comment)
            if caps_ratio > 0.7:
                logger.warning("Excessive capitalization detected")
                # Don't reject, just log
        
        return True
    
    def validate_language_code(self, code: str) -> bool:
        """Validate ISO language code"""
        valid_codes = ['es', 'en', 'pt', 'fr', 'de', 'it', 'ru', 'ja', 'ko', 'zh']
        return code in valid_codes if code else False
    
    def validate_sentiment_label(self, label: str) -> bool:
        """Validate sentiment label"""
        if not label or not isinstance(label, str):
            return False
        valid = ['positive', 'negative', 'neutral', 'positivo', 'negativo']
        return label.lower() in valid
    
    def validate_nps_score(self, score) -> bool:
        """Validate NPS score (0-10)"""
        try:
            # Handle both int and float, convert to int for validation
            score_num = int(float(score)) if score is not None else None
            return score_num is not None and 0 <= score_num <= 10
        except (ValueError, TypeError, OverflowError) as e:
            logger.warning(f"Invalid NPS score format '{score}': {str(e)}")
            return False
    
    def validate_email(self, email: str) -> bool:
        """Validate email format"""
        if not email or not isinstance(email, str):
            return False
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def validate_date_format(self, date: str) -> bool:
        """Validate date in YYYY-MM-DD format"""
        if not date or not isinstance(date, str):
            return False
        pattern = r'^\d{4}-\d{2}-\d{2}$'
        if not re.match(pattern, date):
            return False
        try:
            from datetime import datetime
            datetime.strptime(date, '%Y-%m-%d')
            return True
        except ValueError as e:
            logger.warning(f"Invalid date format '{date}': {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error validating date '{date}': {str(e)}")
            return False
    
    def sanitize_input(self, text: str) -> str:
        """Sanitize input text"""
        if not text:
            return ""
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        # Remove extra spaces
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def validate_file_size(self, size, max_size_mb: int = 50) -> bool:
        """Validate file size"""
        if size is None or size < 0:
            return False
        max_size_bytes = max_size_mb * 1024 * 1024
        return 0 < size <= max_size_bytes
    
    def validate_column_names(self, df: pd.DataFrame) -> bool:
        """Validate DataFrame column names"""
        if not isinstance(df, pd.DataFrame):
            return False
        for col in df.columns:
            if not col or not isinstance(col, str) or col.strip() == '':
                return False
        return True
    
    def validate_percentage(self, value) -> bool:
        """Validate percentage value (0-100)"""
        try:
            num_value = float(value)
            return 0 <= num_value <= 100
        except (ValueError, TypeError) as e:
            logger.warning(f"Invalid percentage value '{value}': {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error validating percentage '{value}': {str(e)}")
            return False

# Example usage and testing
if __name__ == "__main__":
    # Test comment validation
    test_comments = [
        "El servicio es excelente",
        "SELECT * FROM users",  # SQL injection attempt
        "<script>alert('xss')</script>",  # XSS attempt
        "A" * 6000,  # Too long
        "",  # Empty
        "Comentario normal en español"
    ]
    
    print("Testing comment validation:")
    for i, comment in enumerate(test_comments):
        is_valid, result = InputValidator.validate_comment_text(comment)
        print(f"Comment {i+1}: {'VALID' if is_valid else 'INVALID'} - {result[:50]}...")
    
    # Test batch validation
    all_valid, sanitized, errors = InputValidator.validate_comment_batch(test_comments)
    print(f"\nBatch validation: {'PASS' if all_valid else 'FAIL'}")
    print(f"Errors: {len(errors)}")
    for error in errors:
        print(f"  - {error}")