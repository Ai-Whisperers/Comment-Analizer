"""
Retry Strategy for AI API calls
HIGH-004 FIX: Intelligent retry logic with exponential backoff for OpenAI API
"""
import time
import random
import logging
from typing import Optional, Callable, TypeVar, Any
from functools import wraps
import openai

from ...shared.exceptions.ia_exception import IAException

T = TypeVar('T')
logger = logging.getLogger(__name__)


class RetryStrategy:
    """
    HIGH-004 FIX: Intelligent retry mechanism with exponential backoff
    Handles transient failures in OpenAI API calls gracefully
    """
    
    def __init__(self, max_retries: int = 3, base_delay: float = 1.0, max_delay: float = 60.0, 
                 jitter: bool = True):
        """
        Initialize retry strategy
        
        Args:
            max_retries: Maximum number of retry attempts
            base_delay: Base delay in seconds for exponential backoff
            max_delay: Maximum delay in seconds to cap exponential growth
            jitter: Add random jitter to prevent thundering herd
        """
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.jitter = jitter
        logger.debug(f"🔄 RetryStrategy initialized: {max_retries} retries, {base_delay}s base delay")
    
    def __call__(self, func: Callable[..., T]) -> Callable[..., T]:
        """
        Decorator that applies retry logic to a function
        
        Args:
            func: Function to apply retry logic to
            
        Returns:
            Decorated function with retry capability
        """
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            last_exception = None
            
            for attempt in range(self.max_retries + 1):
                try:
                    # Call the original function
                    return func(*args, **kwargs)
                    
                except openai.RateLimitError as e:
                    last_exception = e
                    if attempt == self.max_retries:
                        break
                    
                    # Rate limit errors should always be retried with exponential backoff
                    delay = self._calculate_delay(attempt)
                    logger.warning(f"⏳ Rate limit hit, retrying in {delay:.2f}s (attempt {attempt + 1}/{self.max_retries + 1})")
                    time.sleep(delay)
                    
                except openai.APIConnectionError as e:
                    last_exception = e
                    if attempt == self.max_retries:
                        break
                    
                    # Connection errors might be transient, retry with shorter delay
                    delay = self._calculate_delay(attempt, factor=0.5)
                    logger.warning(f"🌐 Connection error, retrying in {delay:.2f}s: {str(e)}")
                    time.sleep(delay)
                    
                except openai.InternalServerError as e:
                    last_exception = e
                    if attempt == self.max_retries:
                        break
                    
                    # Server errors might be transient
                    delay = self._calculate_delay(attempt)
                    logger.warning(f"🔧 Server error, retrying in {delay:.2f}s: {str(e)}")
                    time.sleep(delay)
                    
                except openai.AuthenticationError as e:
                    # Authentication errors should not be retried
                    logger.error(f"🔐 Authentication error - not retrying: {str(e)}")
                    raise IAException("Authentication failed - check API key", "OpenAI", str(e))
                    
                except openai.BadRequestError as e:
                    # Bad request errors should not be retried
                    logger.error(f"❌ Bad request error - not retrying: {str(e)}")
                    raise IAException("Bad request to OpenAI API", "OpenAI", str(e))
                    
                except Exception as e:
                    # Unknown errors - try once more then fail
                    if attempt < self.max_retries:
                        last_exception = e
                        delay = self.base_delay
                        logger.warning(f"❓ Unknown error, retrying once in {delay}s: {str(e)}")
                        time.sleep(delay)
                    else:
                        raise
            
            # All retries exhausted
            error_msg = f"Max retries ({self.max_retries}) exhausted"
            if last_exception:
                error_msg += f": {str(last_exception)}"
            raise IAException(error_msg, "OpenAI", str(last_exception))
        
        return wrapper
    
    def _calculate_delay(self, attempt: int, factor: float = 1.0) -> float:
        """
        Calculate delay for exponential backoff with optional jitter
        
        Args:
            attempt: Current attempt number (0-based)
            factor: Multiplier for delay calculation
            
        Returns:
            float: Delay in seconds
        """
        # Exponential backoff: base_delay * (2 ^ attempt)
        delay = self.base_delay * (2 ** attempt) * factor
        
        # Cap at max_delay
        delay = min(delay, self.max_delay)
        
        # Add jitter to prevent thundering herd problem
        if self.jitter:
            jitter_amount = random.uniform(0, 0.1 * delay)
            delay += jitter_amount
        
        return delay
    
    def retry_with_backoff(self, func: Callable[..., T], *args, **kwargs) -> T:
        """
        Manually apply retry logic to a function call
        
        Args:
            func: Function to call with retry
            *args: Function arguments
            **kwargs: Function keyword arguments
            
        Returns:
            Function result
        """
        decorated_func = self(func)
        return decorated_func(*args, **kwargs)


class OpenAIRetryWrapper:
    """
    HIGH-004 FIX: Specialized retry wrapper for OpenAI operations
    Provides intelligent error categorization and recovery
    """
    
    def __init__(self, retry_strategy: RetryStrategy):
        """
        Initialize with retry strategy
        
        Args:
            retry_strategy: RetryStrategy instance to use
        """
        self.retry_strategy = retry_strategy
        logger.debug("🔄 OpenAIRetryWrapper initialized")
    
    def wrap_chat_completion(self, client: openai.OpenAI, **kwargs) -> Any:
        """
        Wrap OpenAI chat completion with intelligent retry
        
        Args:
            client: OpenAI client instance
            **kwargs: Arguments for chat completion
            
        Returns:
            Chat completion response
        """
        @self.retry_strategy
        def _make_completion():
            return client.chat.completions.create(**kwargs)
        
        return _make_completion()
    
    def wrap_api_call(self, api_func: Callable, *args, **kwargs) -> Any:
        """
        Generic wrapper for any OpenAI API call
        
        Args:
            api_func: OpenAI API function to call
            *args: Function arguments
            **kwargs: Function keyword arguments
            
        Returns:
            API response
        """
        @self.retry_strategy  
        def _make_api_call():
            return api_func(*args, **kwargs)
        
        return _make_api_call()


# Default retry configurations for different scenarios
DEFAULT_RETRY = RetryStrategy(max_retries=3, base_delay=1.0, max_delay=30.0)
AGGRESSIVE_RETRY = RetryStrategy(max_retries=5, base_delay=0.5, max_delay=60.0)
CONSERVATIVE_RETRY = RetryStrategy(max_retries=2, base_delay=2.0, max_delay=15.0)

# Global wrapper instances
default_retry_wrapper = OpenAIRetryWrapper(DEFAULT_RETRY)
aggressive_retry_wrapper = OpenAIRetryWrapper(AGGRESSIVE_RETRY)
conservative_retry_wrapper = OpenAIRetryWrapper(CONSERVATIVE_RETRY)