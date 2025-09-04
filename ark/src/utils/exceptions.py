"""
Custom Exception Classes for Personal Paraguay Fiber Comments Analysis
Provides specific exception types with user-friendly error messages
"""

import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class BaseAnalysisError(Exception):
    """Base exception class for all analysis errors"""
    
    def __init__(self, message: str, user_message: str = None, error_code: str = None):
        super().__init__(message)
        self.user_message = user_message or message
        self.error_code = error_code or "GENERAL_ERROR"
        
        # Log the technical error
        logger.error(f"[{self.error_code}] {message}")


class DataValidationError(BaseAnalysisError):
    """Raised when data validation fails"""
    
    def __init__(self, message: str, field: str = None):
        user_message = f"Data validation error: {message}"
        if field:
            user_message = f"Invalid data in field '{field}': {message}"
        
        super().__init__(
            message=message,
            user_message=user_message,
            error_code="DATA_VALIDATION_ERROR"
        )
        self.field = field


class FileProcessingError(BaseAnalysisError):
    """Raised when file processing fails"""
    
    def __init__(self, message: str, filename: str = None, file_type: str = None):
        if filename:
            user_message = f"Cannot process file '{filename}': {message}"
        else:
            user_message = f"File processing error: {message}"
            
        super().__init__(
            message=message,
            user_message=user_message,
            error_code="FILE_PROCESSING_ERROR"
        )
        self.filename = filename
        self.file_type = file_type


class APIConnectionError(BaseAnalysisError):
    """Raised when API connection fails"""
    
    def __init__(self, message: str, api_name: str = "External API"):
        user_message = f"Cannot connect to {api_name}. Please check your internet connection and API configuration."
        
        super().__init__(
            message=message,
            user_message=user_message,
            error_code="API_CONNECTION_ERROR"
        )
        self.api_name = api_name


class APIRateLimitError(BaseAnalysisError):
    """Raised when API rate limit is exceeded"""
    
    def __init__(self, message: str, retry_after: int = None):
        if retry_after:
            user_message = f"API rate limit exceeded. Please wait {retry_after} seconds before trying again."
        else:
            user_message = "API rate limit exceeded. Please wait a few minutes before trying again."
            
        super().__init__(
            message=message,
            user_message=user_message,
            error_code="API_RATE_LIMIT_ERROR"
        )
        self.retry_after = retry_after


class APITimeoutError(BaseAnalysisError):
    """Raised when API request times out"""
    
    def __init__(self, message: str, timeout_seconds: int = None):
        if timeout_seconds:
            user_message = f"Request timed out after {timeout_seconds} seconds. The service may be temporarily unavailable."
        else:
            user_message = "Request timed out. The service may be temporarily unavailable."
            
        super().__init__(
            message=message,
            user_message=user_message,
            error_code="API_TIMEOUT_ERROR"
        )
        self.timeout_seconds = timeout_seconds


class ConfigurationError(BaseAnalysisError):
    """Raised when configuration is invalid or missing"""
    
    def __init__(self, message: str, config_key: str = None):
        if config_key:
            user_message = f"Configuration error for '{config_key}': {message}"
        else:
            user_message = f"Configuration error: {message}"
            
        super().__init__(
            message=message,
            user_message=user_message,
            error_code="CONFIGURATION_ERROR"
        )
        self.config_key = config_key


class AnalysisProcessingError(BaseAnalysisError):
    """Raised when analysis processing fails"""
    
    def __init__(self, message: str, stage: str = None):
        if stage:
            user_message = f"Analysis failed during {stage}: {message}"
        else:
            user_message = f"Analysis processing error: {message}"
            
        super().__init__(
            message=message,
            user_message=user_message,
            error_code="ANALYSIS_PROCESSING_ERROR"
        )
        self.stage = stage


class CacheError(BaseAnalysisError):
    """Raised when cache operations fail"""
    
    def __init__(self, message: str, operation: str = None):
        if operation:
            user_message = f"Cache {operation} failed: {message}"
        else:
            user_message = f"Cache error: {message}"
            
        super().__init__(
            message=message,
            user_message=user_message,
            error_code="CACHE_ERROR"
        )
        self.operation = operation


class SecurityError(BaseAnalysisError):
    """Raised when security validation fails"""
    
    def __init__(self, message: str, violation_type: str = None):
        user_message = "Security validation failed. Please check your input and try again."
        
        super().__init__(
            message=message,
            user_message=user_message,
            error_code="SECURITY_ERROR"
        )
        self.violation_type = violation_type


class ResourceLimitError(BaseAnalysisError):
    """Raised when resource limits are exceeded"""
    
    def __init__(self, message: str, resource_type: str = None, limit_value: Any = None):
        if resource_type and limit_value:
            user_message = f"Resource limit exceeded for {resource_type}: maximum {limit_value} allowed."
        elif resource_type:
            user_message = f"Resource limit exceeded for {resource_type}."
        else:
            user_message = "Resource limit exceeded. Please reduce the size of your request."
            
        super().__init__(
            message=message,
            user_message=user_message,
            error_code="RESOURCE_LIMIT_ERROR"
        )
        self.resource_type = resource_type
        self.limit_value = limit_value


class ErrorHandler:
    """Centralized error handling utility"""
    
    @staticmethod
    def handle_streamlit_error(error: Exception, default_message: str = "An unexpected error occurred"):
        """Handle errors in Streamlit context with user-friendly messages"""
        import streamlit as st
        
        if isinstance(error, BaseAnalysisError):
            st.error(error.user_message)
            
            # Show details in expander for debugging
            if hasattr(error, 'error_code'):
                with st.expander("Technical Details"):
                    st.code(f"Error Code: {error.error_code}")
                    st.code(f"Message: {str(error)}")
        else:
            # Handle unexpected errors
            st.error(default_message)
            logger.error(f"Unexpected error: {str(error)}", exc_info=True)
            
            with st.expander("Error Details"):
                st.code(f"Error Type: {type(error).__name__}")
                st.code(f"Message: {str(error)}")
    
    @staticmethod
    def wrap_api_errors(func):
        """Decorator to wrap API calls and convert common errors"""
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ConnectionError as e:
                raise APIConnectionError(f"Connection failed: {str(e)}")
            except TimeoutError as e:
                raise APITimeoutError(f"Request timed out: {str(e)}")
            except Exception as e:
                # Check for rate limit indicators in error message
                error_str = str(e).lower()
                if "rate limit" in error_str or "429" in error_str:
                    raise APIRateLimitError(f"Rate limit exceeded: {str(e)}")
                elif "timeout" in error_str:
                    raise APITimeoutError(f"Request timed out: {str(e)}")
                elif "connection" in error_str or "network" in error_str:
                    raise APIConnectionError(f"Connection error: {str(e)}")
                else:
                    raise AnalysisProcessingError(f"API call failed: {str(e)}")
        
        return wrapper
    
    @staticmethod
    def get_user_friendly_message(error: Exception) -> str:
        """Get user-friendly message for any error"""
        if isinstance(error, BaseAnalysisError):
            return error.user_message
        
        # Map common error types to user-friendly messages
        error_mappings = {
            "FileNotFoundError": "The specified file was not found. Please check the file path.",
            "PermissionError": "Permission denied. Please check file permissions.",
            "ValueError": "Invalid value provided. Please check your input.",
            "KeyError": "Required information is missing. Please check your configuration.",
            "ConnectionError": "Network connection failed. Please check your internet connection.",
            "TimeoutError": "Operation timed out. Please try again.",
        }
        
        error_type = type(error).__name__
        return error_mappings.get(error_type, "An unexpected error occurred. Please try again.")


# Convenience functions for common error scenarios
def raise_if_invalid_file(filepath: str, allowed_extensions: list = None):
    """Raise FileProcessingError if file is invalid"""
    import os
    from pathlib import Path
    
    if not os.path.exists(filepath):
        raise FileProcessingError(f"File not found: {filepath}", filename=os.path.basename(filepath))
    
    if allowed_extensions:
        file_ext = Path(filepath).suffix.lower()
        if file_ext not in allowed_extensions:
            raise FileProcessingError(
                f"Unsupported file type '{file_ext}'. Allowed: {', '.join(allowed_extensions)}", 
                filename=os.path.basename(filepath),
                file_type=file_ext
            )


def raise_if_empty_data(data, data_name: str = "data"):
    """Raise DataValidationError if data is empty"""
    if not data or (hasattr(data, '__len__') and len(data) == 0):
        raise DataValidationError(f"{data_name} cannot be empty")


def raise_if_missing_config(config_value, config_name: str):
    """Raise ConfigurationError if config value is missing"""
    if not config_value:
        raise ConfigurationError(f"Missing required configuration: {config_name}", config_key=config_name)