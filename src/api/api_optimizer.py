"""
API Usage Optimizer for Personal Paraguay Comments Analysis Platform
Implements intelligent batching, rate limiting, and cost optimization for API calls
"""

import time
import logging
import asyncio
import threading
from typing import List, Dict, Optional, Callable, Any
from collections import deque
from dataclasses import dataclass
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
import json

logger = logging.getLogger(__name__)


@dataclass
class APIBatch:
    """Represents a batch of API requests"""
    requests: List[Dict]
    priority: int = 1  # Higher number = higher priority
    created_at: datetime = None
    max_retries: int = 3
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


class APIRateLimiter:
    """
    Intelligent rate limiter that adapts to API response times and limits
    """
    
    def __init__(self, max_requests_per_minute: int = 60, adaptive: bool = True):
        """
        Initialize rate limiter
        
        Args:
            max_requests_per_minute: Base rate limit
            adaptive: Whether to adapt rate based on API performance
        """
        self.max_requests_per_minute = max_requests_per_minute
        self.adaptive = adaptive
        self.request_times = deque()
        self.last_request_time = 0
        self.current_rate = max_requests_per_minute
        self.consecutive_errors = 0
        self.lock = threading.Lock()
        
        # Adaptive parameters
        self.min_rate = max(1, max_requests_per_minute // 10)
        self.max_rate = max_requests_per_minute * 2
        self.backoff_factor = 0.7
        self.recovery_factor = 1.1
    
    def wait_if_needed(self) -> float:
        """
        Wait if necessary to respect rate limits
        
        Returns:
            Time waited in seconds
        """
        with self.lock:
            current_time = time.time()
            
            # Clean old request times (older than 1 minute)
            cutoff_time = current_time - 60
            while self.request_times and self.request_times[0] < cutoff_time:
                self.request_times.popleft()
            
            # Check if we need to wait
            if len(self.request_times) >= self.current_rate:
                # Calculate wait time
                oldest_request = self.request_times[0]
                wait_time = 60 - (current_time - oldest_request)
                
                if wait_time > 0:
                    logger.debug(f"Rate limiting: waiting {wait_time:.2f}s")
                    time.sleep(wait_time)
                    return wait_time
            
            # Record this request
            self.request_times.append(current_time)
            self.last_request_time = current_time
            return 0
    
    def record_success(self, response_time: float):
        """Record successful API call for adaptive rate adjustment"""
        if not self.adaptive:
            return
            
        with self.lock:
            self.consecutive_errors = 0
            
            # If response time is good and we haven't hit errors, increase rate
            if response_time < 2.0 and self.current_rate < self.max_rate:
                self.current_rate = min(
                    self.max_rate,
                    int(self.current_rate * self.recovery_factor)
                )
                logger.debug(f"Increased rate limit to {self.current_rate} requests/min")
    
    def record_error(self, error_type: str = "unknown"):
        """Record API error for adaptive rate adjustment"""
        if not self.adaptive:
            return
            
        with self.lock:
            self.consecutive_errors += 1
            
            # Reduce rate on repeated errors
            if self.consecutive_errors >= 3:
                self.current_rate = max(
                    self.min_rate,
                    int(self.current_rate * self.backoff_factor)
                )
                logger.warning(f"Reduced rate limit to {self.current_rate} requests/min due to errors")
                self.consecutive_errors = 0  # Reset counter


class APIBatchOptimizer:
    """
    Optimizes API batching based on content analysis and API performance
    """
    
    def __init__(self, min_batch_size: int = 5, max_batch_size: int = 25, 
                 target_tokens_per_batch: int = 3000):
        """
        Initialize batch optimizer
        
        Args:
            min_batch_size: Minimum items per batch
            max_batch_size: Maximum items per batch
            target_tokens_per_batch: Target token count per batch for cost optimization
        """
        self.min_batch_size = min_batch_size
        self.max_batch_size = max_batch_size
        self.target_tokens_per_batch = target_tokens_per_batch
        
    def estimate_tokens(self, text: str) -> int:
        """Estimate token count for text (rough approximation)"""
        # Rough estimate: 1 token ≈ 4 characters for English/Spanish
        return len(text) // 4
    
    def optimize_batches(self, items: List[str]) -> List[List[str]]:
        """
        Create optimally sized batches based on content
        
        Args:
            items: List of text items to batch
            
        Returns:
            List of optimized batches
        """
        if not items:
            return []
        
        batches = []
        current_batch = []
        current_tokens = 0
        
        for item in items:
            item_tokens = self.estimate_tokens(item)
            
            # Check if adding this item would exceed limits
            would_exceed_tokens = (current_tokens + item_tokens) > self.target_tokens_per_batch
            would_exceed_size = len(current_batch) >= self.max_batch_size
            
            # Start new batch if limits would be exceeded and current batch has minimum items
            if (would_exceed_tokens or would_exceed_size) and len(current_batch) >= self.min_batch_size:
                batches.append(current_batch)
                current_batch = []
                current_tokens = 0
            
            current_batch.append(item)
            current_tokens += item_tokens
        
        # Add remaining items as final batch
        if current_batch:
            batches.append(current_batch)
        
        logger.info(f"Optimized {len(items)} items into {len(batches)} batches")
        return batches


class APICallOptimizer:
    """
    Main API optimization coordinator that manages batching, rate limiting, and performance
    """
    
    def __init__(self, max_concurrent_requests: int = 3, enable_caching: bool = True):
        """
        Initialize API optimizer
        
        Args:
            max_concurrent_requests: Maximum concurrent API requests
            enable_caching: Whether to use caching for duplicate requests
        """
        self.rate_limiter = APIRateLimiter()
        self.batch_optimizer = APIBatchOptimizer()
        self.max_concurrent_requests = max_concurrent_requests
        self.enable_caching = enable_caching
        
        # Performance tracking
        self.total_requests = 0
        self.total_response_time = 0
        self.cache_hits = 0
        self.errors = 0
        
        # Simple cache for duplicate requests
        self.request_cache = {} if enable_caching else None
        
    def get_cache_key(self, prompt: str, model: str) -> str:
        """Generate cache key for request"""
        import hashlib
        content = f"{model}:{prompt}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def execute_optimized_batch(self, 
                               items: List[str],
                               api_function: Callable,
                               **api_kwargs) -> List[Dict]:
        """
        Execute API calls with full optimization
        
        Args:
            items: List of items to process
            api_function: API function to call for each batch
            **api_kwargs: Additional arguments for API function
            
        Returns:
            Combined results from all batches
        """
        # Optimize batches
        optimized_batches = self.batch_optimizer.optimize_batches(items)
        
        # Create API batches with priority
        api_batches = [
            APIBatch(
                requests=batch,
                priority=1,  # Can be adjusted based on business logic
                max_retries=3
            )
            for batch in optimized_batches
        ]
        
        # Execute batches with concurrency control
        return self._execute_batches_concurrently(api_batches, api_function, **api_kwargs)
    
    def _execute_batches_concurrently(self, 
                                    batches: List[APIBatch],
                                    api_function: Callable,
                                    **api_kwargs) -> List[Dict]:
        """Execute batches with controlled concurrency"""
        all_results = []
        
        with ThreadPoolExecutor(max_workers=self.max_concurrent_requests) as executor:
            # Submit all batches
            future_to_batch = {
                executor.submit(self._execute_single_batch, batch, api_function, **api_kwargs): batch
                for batch in batches
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_batch):
                batch = future_to_batch[future]
                try:
                    batch_results = future.result()
                    if batch_results:
                        all_results.extend(batch_results)
                except Exception as e:
                    logger.error(f"Batch execution failed: {e}")
                    self.errors += 1
                    # Continue with other batches
        
        return all_results
    
    def _execute_single_batch(self, 
                            batch: APIBatch,
                            api_function: Callable,
                            **api_kwargs) -> List[Dict]:
        """Execute a single batch with retries and rate limiting"""
        
        for attempt in range(batch.max_retries):
            try:
                # Rate limiting
                wait_time = self.rate_limiter.wait_if_needed()
                
                # Check cache first
                if self.enable_caching:
                    cache_key = self.get_cache_key(str(batch.requests), api_kwargs.get('model', 'default'))
                    if cache_key in self.request_cache:
                        self.cache_hits += 1
                        logger.debug(f"Cache hit for batch of {len(batch.requests)} items")
                        return self.request_cache[cache_key]
                
                # Execute API call
                start_time = time.time()
                results = api_function(batch.requests, **api_kwargs)
                response_time = time.time() - start_time
                
                # Record success
                self.total_requests += 1
                self.total_response_time += response_time
                self.rate_limiter.record_success(response_time)
                
                # Cache result
                if self.enable_caching and results:
                    self.request_cache[cache_key] = results
                
                logger.debug(f"Successfully processed batch of {len(batch.requests)} items in {response_time:.2f}s")
                return results
                
            except Exception as e:
                logger.warning(f"Batch attempt {attempt + 1}/{batch.max_retries} failed: {e}")
                self.rate_limiter.record_error(str(type(e)))
                
                if attempt < batch.max_retries - 1:
                    # Exponential backoff
                    delay = (2 ** attempt) * 1.0
                    time.sleep(delay)
                else:
                    logger.error(f"Batch failed after {batch.max_retries} attempts")
                    self.errors += 1
                    return []
        
        return []
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics"""
        avg_response_time = (
            self.total_response_time / self.total_requests 
            if self.total_requests > 0 else 0
        )
        
        cache_hit_rate = (
            self.cache_hits / (self.total_requests + self.cache_hits) * 100
            if (self.total_requests + self.cache_hits) > 0 else 0
        )
        
        return {
            "total_requests": self.total_requests,
            "average_response_time": avg_response_time,
            "cache_hits": self.cache_hits,
            "cache_hit_rate": cache_hit_rate,
            "errors": self.errors,
            "current_rate_limit": self.rate_limiter.current_rate,
            "estimated_cost_saved": self.cache_hits * 0.002  # Rough estimate
        }
    
    def clear_cache(self):
        """Clear the request cache"""
        if self.request_cache:
            self.request_cache.clear()
            logger.info("API cache cleared")


# Global optimizer instance with thread safety
import threading
_global_optimizer = None
_optimizer_lock = threading.Lock()


def get_global_api_optimizer() -> APICallOptimizer:
    """Get global API optimizer instance (thread-safe)"""
    global _global_optimizer
    if _global_optimizer is None:
        with _optimizer_lock:
            # Double-check locking pattern
            if _global_optimizer is None:
                _global_optimizer = APICallOptimizer()
    return _global_optimizer


def reset_global_optimizer():
    """Reset global optimizer (useful for testing)"""
    global _global_optimizer
    with _optimizer_lock:
        _global_optimizer = None


def optimize_api_usage(items: List[str], 
                      api_function: Callable,
                      **api_kwargs) -> List[Dict]:
    """
    Convenience function for optimized API usage
    
    Args:
        items: Items to process
        api_function: API function to call
        **api_kwargs: Additional API arguments
        
    Returns:
        Combined results
    """
    optimizer = get_global_api_optimizer()
    return optimizer.execute_optimized_batch(items, api_function, **api_kwargs)


# Cost optimization utilities

def estimate_api_cost(num_requests: int, 
                     avg_tokens_per_request: int = 1000,
                     model: str = "gpt-4o-mini") -> float:
    """
    Estimate API cost for requests
    
    Args:
        num_requests: Number of API requests
        avg_tokens_per_request: Average tokens per request
        model: Model being used
        
    Returns:
        Estimated cost in USD
    """
    # Rough pricing estimates (as of 2024)
    pricing = {
        "gpt-4o-mini": 0.000150,  # per 1K tokens input
        "gpt-4o": 0.003,          # per 1K tokens input
        "gpt-3.5-turbo": 0.0005,  # per 1K tokens input
    }
    
    cost_per_1k_tokens = pricing.get(model, 0.002)  # Default estimate
    total_tokens = num_requests * avg_tokens_per_request
    
    return (total_tokens / 1000) * cost_per_1k_tokens


def suggest_batch_size_for_budget(budget_usd: float,
                                 total_items: int,
                                 avg_tokens_per_item: int = 250,
                                 model: str = "gpt-4o-mini") -> Dict[str, Any]:
    """
    Suggest optimal batch configuration for given budget
    
    Args:
        budget_usd: Available budget in USD
        total_items: Total items to process
        avg_tokens_per_item: Average tokens per item
        model: Model to use
        
    Returns:
        Configuration suggestions
    """
    # Calculate max items we can afford
    cost_per_item = estimate_api_cost(1, avg_tokens_per_item, model)
    max_affordable_items = int(budget_usd / cost_per_item)
    
    # Suggest configuration
    if max_affordable_items >= total_items:
        return {
            "can_process_all": True,
            "suggested_batch_size": min(25, total_items),
            "estimated_cost": estimate_api_cost(total_items, avg_tokens_per_item, model),
            "items_to_process": total_items
        }
    else:
        return {
            "can_process_all": False,
            "suggested_batch_size": min(25, max_affordable_items),
            "estimated_cost": budget_usd,
            "items_to_process": max_affordable_items,
            "items_remaining": total_items - max_affordable_items,
            "suggestion": f"Process {max_affordable_items} items in batches of {min(25, max_affordable_items)}"
        }