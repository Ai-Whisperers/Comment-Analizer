"""
Robust API Client with Timeout and Connection Error Handling
Provides comprehensive timeout, retry, and connection management for all API calls
"""

import time
import logging
import asyncio
from typing import Any, Callable, Dict, Optional, List
from functools import wraps
import threading
import queue
from openai import OpenAI
from openai._exceptions import APITimeoutError, APIConnectionError, RateLimitError
import requests.exceptions

from src.config import Config
from src.utils.exceptions import (
    APIConnectionError as CustomAPIConnectionError,
    APITimeoutError as CustomAPITimeoutError, 
    APIRateLimitError,
    AnalysisProcessingError
)

logger = logging.getLogger(__name__)


class TimeoutConfig:
    """Configuration for API timeouts and retries"""
    
    # Connection timeouts (seconds)
    CONNECT_TIMEOUT = 10
    READ_TIMEOUT = 60
    TOTAL_TIMEOUT = 120
    
    # Retry configuration
    MAX_RETRIES = 5
    BASE_DELAY = 1
    MAX_DELAY = 60
    BACKOFF_FACTOR = 2
    
    # Rate limit handling
    RATE_LIMIT_DELAY = 60
    RATE_LIMIT_MAX_RETRIES = 3


class CircuitBreaker:
    """Circuit breaker pattern for API reliability"""
    
    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
        self._lock = threading.Lock()
    
    def call(self, func: Callable) -> Any:
        """Execute function with circuit breaker protection"""
        with self._lock:
            if self.state == "OPEN":
                if time.time() - self.last_failure_time > self.timeout:
                    self.state = "HALF_OPEN"
                    logger.info("Circuit breaker entering HALF_OPEN state")
                else:
                    raise CustomAPIConnectionError(
                        "Circuit breaker is OPEN - too many recent failures",
                        api_name="OpenAI API"
                    )
            
            try:
                result = func()
                if self.state == "HALF_OPEN":
                    self.state = "CLOSED"
                    self.failure_count = 0
                    logger.info("Circuit breaker reset to CLOSED state")
                return result
                
            except Exception as e:
                self.failure_count += 1
                self.last_failure_time = time.time()
                
                if self.failure_count >= self.failure_threshold:
                    self.state = "OPEN"
                    logger.warning(f"Circuit breaker opened after {self.failure_count} failures")
                
                raise e


class RobustAPIClient:
    """Robust API client with comprehensive error handling"""
    
    def __init__(self, api_key: str):
        if not api_key:
            raise CustomAPIConnectionError("API key is required", api_name="OpenAI API")
        
        self.client = OpenAI(
            api_key=api_key,
            timeout=TimeoutConfig.TOTAL_TIMEOUT
        )
        self.circuit_breaker = CircuitBreaker()
        self.request_queue = queue.Queue()
        self.stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "timeout_errors": 0,
            "connection_errors": 0,
            "rate_limit_errors": 0
        }
    
    def _execute_with_timeout(self, func: Callable, timeout: int) -> Any:
        """Execute function with custom timeout using threading"""
        result_queue = queue.Queue()
        exception_queue = queue.Queue()
        
        def target():
            try:
                result = func()
                result_queue.put(result)
            except Exception as e:
                exception_queue.put(e)
        
        thread = threading.Thread(target=target)
        thread.daemon = True
        thread.start()
        thread.join(timeout)
        
        if thread.is_alive():
            # Thread is still running, timeout occurred
            logger.warning(f"Operation timed out after {timeout} seconds")
            raise CustomAPITimeoutError(
                f"API call timed out after {timeout} seconds",
                timeout_seconds=timeout
            )
        
        # Check for exceptions
        if not exception_queue.empty():
            raise exception_queue.get()
        
        # Check for results
        if not result_queue.empty():
            return result_queue.get()
        
        raise AnalysisProcessingError("No result returned from API call")
    
    def _handle_api_error(self, error: Exception) -> Exception:
        """Convert API errors to custom exceptions"""
        error_str = str(error).lower()
        
        if isinstance(error, APITimeoutError) or "timeout" in error_str:
            self.stats["timeout_errors"] += 1
            return CustomAPITimeoutError(f"OpenAI API timeout: {str(error)}")
        
        elif isinstance(error, APIConnectionError) or "connection" in error_str:
            self.stats["connection_errors"] += 1
            return CustomAPIConnectionError(f"OpenAI API connection error: {str(error)}", api_name="OpenAI API")
        
        elif isinstance(error, RateLimitError) or "rate_limit" in error_str or "429" in error_str:
            self.stats["rate_limit_errors"] += 1
            return APIRateLimitError(f"OpenAI API rate limit: {str(error)}")
        
        else:
            return AnalysisProcessingError(f"OpenAI API error: {str(error)}")
    
    def _retry_with_backoff(self, func: Callable, max_retries: int = None) -> Any:
        """Execute function with exponential backoff retry logic"""
        max_retries = max_retries or TimeoutConfig.MAX_RETRIES
        delay = TimeoutConfig.BASE_DELAY
        
        for attempt in range(max_retries):
            try:
                self.stats["total_requests"] += 1
                result = self.circuit_breaker.call(func)
                self.stats["successful_requests"] += 1
                return result
                
            except APIRateLimitError as e:
                self.stats["failed_requests"] += 1
                if attempt < max_retries - 1:
                    wait_time = TimeoutConfig.RATE_LIMIT_DELAY
                    logger.warning(f"Rate limit hit, waiting {wait_time}s before retry {attempt + 1}/{max_retries}")
                    time.sleep(wait_time)
                    continue
                raise e
            
            except (CustomAPITimeoutError, CustomAPIConnectionError) as e:
                self.stats["failed_requests"] += 1
                if attempt < max_retries - 1:
                    wait_time = min(delay * (TimeoutConfig.BACKOFF_FACTOR ** attempt), TimeoutConfig.MAX_DELAY)
                    logger.warning(f"API error on attempt {attempt + 1}/{max_retries}: {str(e)}")
                    logger.info(f"Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                raise e
            
            except Exception as e:
                self.stats["failed_requests"] += 1
                converted_error = self._handle_api_error(e)
                
                if isinstance(converted_error, (CustomAPITimeoutError, CustomAPIConnectionError, APIRateLimitError)):
                    if attempt < max_retries - 1:
                        wait_time = min(delay * (TimeoutConfig.BACKOFF_FACTOR ** attempt), TimeoutConfig.MAX_DELAY)
                        logger.warning(f"Retryable error on attempt {attempt + 1}/{max_retries}: {str(e)}")
                        logger.info(f"Retrying in {wait_time}s...")
                        time.sleep(wait_time)
                        continue
                
                raise converted_error
        
        raise AnalysisProcessingError(f"Failed after {max_retries} attempts")
    
    def chat_completion(self, messages: List[Dict], model: str = "gpt-4o-mini", **kwargs) -> Any:
        """Create chat completion with robust error handling"""
        
        def make_request():
            return self._execute_with_timeout(
                lambda: self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    timeout=TimeoutConfig.READ_TIMEOUT,
                    **kwargs
                ),
                timeout=TimeoutConfig.TOTAL_TIMEOUT
            )
        
        return self._retry_with_backoff(make_request)
    
    def get_stats(self) -> Dict:
        """Get API client statistics"""
        total = self.stats["total_requests"]
        if total == 0:
            success_rate = 0
        else:
            success_rate = (self.stats["successful_requests"] / total) * 100
        
        return {
            **self.stats,
            "success_rate_percent": round(success_rate, 2),
            "circuit_breaker_state": self.circuit_breaker.state,
            "failure_count": self.circuit_breaker.failure_count
        }


class ConnectionHealthChecker:
    """Monitor API connection health"""
    
    def __init__(self, api_client: RobustAPIClient):
        self.api_client = api_client
        self.last_health_check = None
        self.is_healthy = True
    
    def check_health(self) -> bool:
        """Perform health check with minimal API call"""
        try:
            # Make a minimal API call to test connectivity
            response = self.api_client.chat_completion(
                messages=[{"role": "user", "content": "ping"}],
                max_tokens=1,
                temperature=0
            )
            
            self.is_healthy = True
            self.last_health_check = time.time()
            logger.info("API health check passed")
            return True
            
        except Exception as e:
            self.is_healthy = False
            self.last_health_check = time.time()
            logger.warning(f"API health check failed: {str(e)}")
            return False
    
    def get_health_status(self) -> Dict:
        """Get current health status"""
        return {
            "is_healthy": self.is_healthy,
            "last_check": self.last_health_check,
            "time_since_check": time.time() - self.last_health_check if self.last_health_check else None
        }


def timeout_handler(timeout_seconds: int = TimeoutConfig.TOTAL_TIMEOUT):
    """Decorator for adding timeout to any function"""
    # Input validation for timeout_seconds
    if not isinstance(timeout_seconds, (int, float)):
        raise TypeError("timeout_seconds must be a number")
    
    if timeout_seconds <= 0:
        raise ValueError("timeout_seconds must be positive")
    
    if timeout_seconds < 1:
        logger.warning(f"Very short timeout ({timeout_seconds}s) may cause frequent timeouts")
    elif timeout_seconds > 3600:  # 1 hour
        logger.warning(f"Very long timeout ({timeout_seconds}s) may cause hanging")
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result_queue = queue.Queue()
            exception_queue = queue.Queue()
            
            def target():
                try:
                    result = func(*args, **kwargs)
                    result_queue.put(result)
                except Exception as e:
                    exception_queue.put(e)
            
            thread = threading.Thread(target=target)
            thread.daemon = True
            thread.start()
            thread.join(timeout_seconds)
            
            if thread.is_alive():
                raise CustomAPITimeoutError(
                    f"Function {func.__name__} timed out after {timeout_seconds} seconds",
                    timeout_seconds=timeout_seconds
                )
            
            if not exception_queue.empty():
                raise exception_queue.get()
            
            if not result_queue.empty():
                return result_queue.get()
            
            raise AnalysisProcessingError(f"No result from {func.__name__}")
        
        return wrapper
    return decorator


# Convenience function to create API client
def create_robust_client(api_key: str = None) -> RobustAPIClient:
    """Create a robust API client with default configuration"""
    api_key = api_key or Config.OPENAI_API_KEY
    return RobustAPIClient(api_key)


# Testing and monitoring utilities
class APIMonitor:
    """Monitor API performance and reliability"""
    
    def __init__(self):
        self.metrics = {
            "response_times": [],
            "error_counts": {},
            "hourly_requests": {},
            "daily_costs": {}
        }
    
    def log_request(self, duration: float, success: bool, error_type: str = None):
        """Log API request metrics"""
        self.metrics["response_times"].append(duration)
        
        if not success and error_type:
            self.metrics["error_counts"][error_type] = self.metrics["error_counts"].get(error_type, 0) + 1
        
        # Keep only last 1000 response times
        if len(self.metrics["response_times"]) > 1000:
            self.metrics["response_times"] = self.metrics["response_times"][-1000:]
    
    def get_performance_summary(self) -> Dict:
        """Get performance metrics summary"""
        if not self.metrics["response_times"]:
            return {"status": "No data available"}
        
        response_times = self.metrics["response_times"]
        return {
            "avg_response_time": sum(response_times) / len(response_times),
            "max_response_time": max(response_times),
            "min_response_time": min(response_times),
            "total_errors": sum(self.metrics["error_counts"].values()),
            "error_breakdown": dict(self.metrics["error_counts"]),
            "total_requests": len(response_times)
        }


# Global instances with thread safety
import threading
_api_monitor = APIMonitor()
_robust_client = None
_client_lock = threading.Lock()


def get_global_client() -> RobustAPIClient:
    """Get global robust API client instance (thread-safe)"""
    global _robust_client
    if _robust_client is None:
        with _client_lock:
            # Double-check locking pattern
            if _robust_client is None:
                _robust_client = create_robust_client()
    return _robust_client


def reset_global_client():
    """Reset global client (useful for testing)"""
    global _robust_client
    with _client_lock:
        _robust_client = None


def get_api_monitor() -> APIMonitor:
    """Get global API monitor instance"""
    return _api_monitor