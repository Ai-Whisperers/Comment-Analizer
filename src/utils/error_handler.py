"""
Standardized Error Handling Module
FIX P1 #9: Consistent error handling patterns across the application
"""

import logging
import traceback
from typing import Optional, Dict, Any, Union, Callable
from datetime import datetime
from functools import wraps
import uuid

logger = logging.getLogger(__name__)


class AnalysisError:
    """Standardized error response structure"""
    
    def __init__(self, 
                 error_code: str,
                 error_message: str,
                 error_type: str = "UNKNOWN",
                 details: Optional[Dict[str, Any]] = None,
                 user_message: Optional[str] = None):
        """
        Create standardized error response
        
        Args:
            error_code: Unique error code (e.g., 'FILE_NOT_FOUND')
            error_message: Technical error message
            error_type: Category of error
            details: Additional error context
            user_message: User-friendly message in Spanish
        """
        self.error_code = error_code
        self.error_message = error_message
        self.error_type = error_type
        self.details = details or {}
        self.user_message = user_message or self._get_default_user_message(error_code)
        self.timestamp = datetime.now().isoformat()
        self.error_id = str(uuid.uuid4())[:8]
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            'error': True,
            'error_id': self.error_id,
            'error_code': self.error_code,
            'error_message': self.error_message,
            'error_type': self.error_type,
            'user_message': self.user_message,
            'details': self.details,
            'timestamp': self.timestamp
        }
        
    def _get_default_user_message(self, error_code: str) -> str:
        """Get default user-friendly message in Spanish"""
        messages = {
            'FILE_NOT_FOUND': 'No se encontró el archivo especificado',
            'INVALID_FORMAT': 'El formato del archivo no es válido',
            'NO_COMMENT_COLUMN': 'No se encontró columna de comentarios en el archivo',
            'API_ERROR': 'Error al conectar con el servicio de análisis',
            'MEMORY_ERROR': 'El archivo es demasiado grande para procesar',
            'VALIDATION_ERROR': 'Los datos no cumplen con el formato esperado',
            'PROCESSING_ERROR': 'Error al procesar los comentarios',
            'UNKNOWN': 'Ocurrió un error inesperado'
        }
        return messages.get(error_code, messages['UNKNOWN'])


class ErrorHandler:
    """Centralized error handling utilities"""
    
    @staticmethod
    def handle_error(exception: Exception, 
                    context: Optional[Dict[str, Any]] = None,
                    error_code: Optional[str] = None) -> AnalysisError:
        """
        Convert exception to standardized error response
        
        Args:
            exception: The exception to handle
            context: Additional context about where error occurred
            error_code: Override error code
            
        Returns:
            AnalysisError object
        """
        # Determine error code and type
        if error_code is None:
            error_code = ErrorHandler._get_error_code(exception)
        
        error_type = type(exception).__name__
        
        # Build error details
        details = {
            'exception_class': error_type,
            'traceback': traceback.format_exc() if logger.level <= logging.DEBUG else None
        }
        
        if context:
            details['context'] = context
            
        # Create error response
        error = AnalysisError(
            error_code=error_code,
            error_message=str(exception),
            error_type=error_type,
            details=details
        )
        
        # Log the error
        logger.error(f"Error {error.error_id}: {error_code} - {str(exception)}")
        if context:
            logger.debug(f"Error context: {context}")
            
        return error
        
    @staticmethod
    def _get_error_code(exception: Exception) -> str:
        """Map exception type to error code"""
        error_mapping = {
            FileNotFoundError: 'FILE_NOT_FOUND',
            ValueError: 'VALIDATION_ERROR',
            KeyError: 'MISSING_KEY',
            MemoryError: 'MEMORY_ERROR',
            TypeError: 'TYPE_ERROR',
            AttributeError: 'ATTRIBUTE_ERROR',
            ConnectionError: 'CONNECTION_ERROR',
            TimeoutError: 'TIMEOUT_ERROR'
        }
        
        for exc_type, code in error_mapping.items():
            if isinstance(exception, exc_type):
                return code
                
        return 'UNKNOWN'
        
    @staticmethod
    def safe_execute(func: Callable, 
                    *args, 
                    default=None,
                    context: Optional[Dict[str, Any]] = None,
                    **kwargs) -> Union[Any, AnalysisError]:
        """
        Execute function safely with error handling
        
        Args:
            func: Function to execute
            *args: Function arguments
            default: Default value to return on error
            context: Context for error reporting
            **kwargs: Function keyword arguments
            
        Returns:
            Function result or error/default
        """
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error = ErrorHandler.handle_error(e, context)
            
            if default is not None:
                logger.info(f"Returning default value after error: {error.error_code}")
                return default
            
            return error


def with_error_handling(error_code: Optional[str] = None,
                        default=None,
                        log_level=logging.ERROR):
    """
    Decorator for consistent error handling
    
    Args:
        error_code: Override error code
        default: Default return value on error
        log_level: Logging level for errors
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                context = {
                    'function': func.__name__,
                    'module': func.__module__
                }
                
                error = ErrorHandler.handle_error(e, context, error_code)
                
                if log_level:
                    logger.log(log_level, f"Error in {func.__name__}: {error.to_dict()}")
                    
                if default is not None:
                    return default
                    
                # Return error dict for functions expecting dict returns
                if 'dict' in str(func.__annotations__.get('return', '')):
                    return error.to_dict()
                    
                # Re-raise for other cases
                raise
                
        return wrapper
    return decorator


class ResultOrError:
    """
    Container for function results that may be either success or error
    Provides consistent interface for checking and accessing results
    """
    
    def __init__(self, value: Any, is_error: bool = False):
        self._value = value
        self._is_error = is_error
        
    @property
    def is_success(self) -> bool:
        """Check if result is successful"""
        return not self._is_error
        
    @property
    def is_error(self) -> bool:
        """Check if result is an error"""
        return self._is_error
        
    @property
    def value(self) -> Any:
        """Get the value (result or error)"""
        return self._value
        
    def get_or_raise(self) -> Any:
        """Get value or raise exception if error"""
        if self._is_error:
            if isinstance(self._value, AnalysisError):
                raise RuntimeError(self._value.error_message)
            raise RuntimeError(str(self._value))
        return self._value
        
    def get_or_default(self, default: Any) -> Any:
        """Get value or return default if error"""
        return default if self._is_error else self._value
        
    @classmethod
    def success(cls, value: Any) -> 'ResultOrError':
        """Create success result"""
        return cls(value, is_error=False)
        
    @classmethod
    def error(cls, error: Union[Exception, AnalysisError, str]) -> 'ResultOrError':
        """Create error result"""
        if isinstance(error, str):
            error = AnalysisError('ERROR', error)
        elif isinstance(error, Exception):
            error = ErrorHandler.handle_error(error)
        return cls(error, is_error=True)


# Global error codes for consistency
class ErrorCodes:
    """Centralized error codes"""
    
    # File errors
    FILE_NOT_FOUND = 'FILE_NOT_FOUND'
    FILE_TOO_LARGE = 'FILE_TOO_LARGE'
    INVALID_FORMAT = 'INVALID_FORMAT'
    
    # Data errors
    NO_DATA = 'NO_DATA'
    NO_COMMENT_COLUMN = 'NO_COMMENT_COLUMN'
    INVALID_DATA = 'INVALID_DATA'
    
    # API errors
    API_CONNECTION = 'API_CONNECTION'
    API_TIMEOUT = 'API_TIMEOUT'
    API_RATE_LIMIT = 'API_RATE_LIMIT'
    API_INVALID_RESPONSE = 'API_INVALID_RESPONSE'
    
    # Processing errors
    PROCESSING_FAILED = 'PROCESSING_FAILED'
    ANALYSIS_FAILED = 'ANALYSIS_FAILED'
    MEMORY_ERROR = 'MEMORY_ERROR'
    
    # Validation errors
    VALIDATION_FAILED = 'VALIDATION_FAILED'
    MISSING_REQUIRED = 'MISSING_REQUIRED'
    TYPE_ERROR = 'TYPE_ERROR'
    
    # System errors
    SYSTEM_ERROR = 'SYSTEM_ERROR'
    UNKNOWN = 'UNKNOWN'