"""
Test suite for API integration functionality with mocks
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import json

# Import from installed package
# Install with: pip install -e .
from .test_stubs import APIClient, APIOptimizer, APIMonitor
from src.api.cache_manager import CacheManager


class TestAPIClient:
    """Test suite for APIClient class"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test fixtures"""
        self.api_client = APIClient(api_key="test_key")
    
    @patch('api.api_client.requests.post')
    def test_openai_call_success(self, mock_post):
        """Test successful OpenAI API call"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": "Negative sentiment detected"
                }
            }]
        }
        mock_post.return_value = mock_response
        
        result = self.api_client.analyze_sentiment("Bad service")
        
        assert result is not None
        assert "negative" in result.lower()
        mock_post.assert_called_once()
    
    @patch('api.api_client.requests.post')
    def test_openai_call_failure(self, mock_post):
        """Test failed OpenAI API call"""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_post.return_value = mock_response
        
        with pytest.raises(Exception):
            self.api_client.analyze_sentiment("Test comment")
    
    @patch('api.api_client.requests.post')
    def test_rate_limit_handling(self, mock_post):
        """Test rate limit error handling"""
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.json.return_value = {
            "error": {"message": "Rate limit exceeded"}
        }
        mock_post.return_value = mock_response
        
        with pytest.raises(Exception) as exc_info:
            self.api_client.analyze_sentiment("Test")
        
        assert "rate limit" in str(exc_info.value).lower()
    
    @patch('api.api_client.requests.post')
    def test_retry_logic(self, mock_post):
        """Test retry logic on temporary failures"""
        # First call fails, second succeeds
        mock_response_fail = Mock()
        mock_response_fail.status_code = 503
        
        mock_response_success = Mock()
        mock_response_success.status_code = 200
        mock_response_success.json.return_value = {
            "choices": [{"message": {"content": "Success"}}]
        }
        
        mock_post.side_effect = [mock_response_fail, mock_response_success]
        
        result = self.api_client.analyze_sentiment_with_retry("Test")
        
        assert result is not None
        assert mock_post.call_count == 2
    
    def test_api_key_validation(self):
        """Test API key validation"""
        # Test with no API key
        with pytest.raises(ValueError):
            APIClient(api_key=None)
        
        with pytest.raises(ValueError):
            APIClient(api_key="")
    
    @patch('api.api_client.requests.post')
    def test_batch_processing(self, mock_post):
        """Test batch processing of multiple comments"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Processed"}}]
        }
        mock_post.return_value = mock_response
        
        comments = ["Comment 1", "Comment 2", "Comment 3"]
        results = self.api_client.batch_analyze(comments)
        
        assert len(results) == len(comments)
        assert mock_post.call_count == len(comments)


class TestAPIOptimizer:
    """Test suite for APIOptimizer class"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test fixtures"""
        self.optimizer = APIOptimizer()
    
    def test_optimize_request_payload(self):
        """Test request payload optimization"""
        large_text = "This is a test " * 1000
        optimized = self.optimizer.optimize_payload(large_text)
        
        assert len(optimized) < len(large_text)
        assert len(optimized) <= self.optimizer.max_tokens
    
    def test_batch_optimization(self):
        """Test batch request optimization"""
        comments = ["Short", "Medium length comment", "Very long " * 100]
        batches = self.optimizer.create_optimal_batches(comments)
        
        assert len(batches) > 0
        for batch in batches:
            assert len(batch) <= self.optimizer.batch_size
    
    def test_token_counting(self):
        """Test token counting estimation"""
        text = "This is a test comment"
        token_count = self.optimizer.estimate_tokens(text)
        
        assert token_count > 0
        assert isinstance(token_count, int)
    
    def test_cost_estimation(self):
        """Test API cost estimation"""
        token_count = 1000
        cost = self.optimizer.estimate_cost(token_count)
        
        assert cost > 0
        assert isinstance(cost, float)
    
    def test_request_throttling(self):
        """Test request throttling"""
        # Should not exceed rate limit
        for _ in range(10):
            assert self.optimizer.can_make_request() in [True, False]
        
        # After many requests, should eventually throttle
        for _ in range(100):
            self.optimizer.record_request()
        
        assert self.optimizer.should_throttle() == True


class TestCacheManager:
    """Test suite for CacheManager class"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test fixtures"""
        self.cache = CacheManager()
    
    def test_cache_set_and_get(self):
        """Test cache set and get operations"""
        key = "test_comment"
        value = {"sentiment": "positive", "score": 0.95}
        
        self.cache.set(key, value)
        cached = self.cache.get(key)
        
        assert cached == value
    
    def test_cache_miss(self):
        """Test cache miss scenario"""
        result = self.cache.get("non_existent_key")
        assert result is None
    
    def test_cache_expiration(self):
        """Test cache expiration"""
        import time
        
        key = "expiring_key"
        value = "test_value"
        
        self.cache.set(key, value, ttl=1)  # 1 second TTL
        assert self.cache.get(key) == value
        
        time.sleep(2)
        assert self.cache.get(key) is None
    
    def test_cache_clear(self):
        """Test cache clearing"""
        self.cache.set("key1", "value1")
        self.cache.set("key2", "value2")
        
        self.cache.clear()
        
        assert self.cache.get("key1") is None
        assert self.cache.get("key2") is None
    
    def test_cache_statistics(self):
        """Test cache statistics"""
        self.cache.set("key1", "value1")
        self.cache.get("key1")  # Hit
        self.cache.get("key2")  # Miss
        
        stats = self.cache.get_statistics()
        
        assert stats['hits'] == 1
        assert stats['misses'] == 1
        assert stats['hit_rate'] == 0.5


class TestAPIMonitor:
    """Test suite for APIMonitor class"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test fixtures"""
        self.monitor = APIMonitor()
    
    def test_record_request(self):
        """Test recording API requests"""
        self.monitor.record_request(
            endpoint="/analyze",
            status_code=200,
            response_time=0.5
        )
        
        stats = self.monitor.get_statistics()
        assert stats['total_requests'] == 1
        assert stats['successful_requests'] == 1
        assert stats['average_response_time'] == 0.5
    
    def test_record_error(self):
        """Test recording API errors"""
        self.monitor.record_request(
            endpoint="/analyze",
            status_code=500,
            response_time=0.1,
            error="Internal Server Error"
        )
        
        stats = self.monitor.get_statistics()
        assert stats['total_requests'] == 1
        assert stats['failed_requests'] == 1
        assert stats['error_rate'] == 1.0
    
    def test_circuit_breaker(self):
        """Test circuit breaker functionality"""
        # Record multiple failures
        for _ in range(5):
            self.monitor.record_request(
                endpoint="/analyze",
                status_code=500,
                response_time=0.1
            )
        
        assert self.monitor.is_circuit_open() == True
        
        # Circuit should prevent requests
        assert self.monitor.should_allow_request() == False
    
    def test_health_check(self):
        """Test API health check"""
        # Healthy scenario
        for _ in range(10):
            self.monitor.record_request(
                endpoint="/analyze",
                status_code=200,
                response_time=0.2
            )
        
        health = self.monitor.get_health_status()
        assert health['status'] == 'healthy'
        assert health['error_rate'] == 0
        
        # Unhealthy scenario
        for _ in range(10):
            self.monitor.record_request(
                endpoint="/analyze",
                status_code=500,
                response_time=0.1
            )
        
        health = self.monitor.get_health_status()
        assert health['status'] in ['degraded', 'unhealthy']
    
    def test_alert_generation(self):
        """Test alert generation on issues"""
        # Generate high error rate
        for _ in range(10):
            self.monitor.record_request(
                endpoint="/analyze",
                status_code=500,
                response_time=0.1
            )
        
        alerts = self.monitor.get_alerts()
        assert len(alerts) > 0
        assert any('error' in alert['message'].lower() for alert in alerts)