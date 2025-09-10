"""
Intelligent Retry Strategy for AI Model Calls
PHASE 3: Smart retry decisions based on model configuration and failure analysis
"""
import logging
import time
from typing import Dict, Any, Optional, Callable, Tuple
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class RetryDecision(Enum):
    """Possible retry decisions"""
    SKIP_RETRY = "skip_retry"
    RETRY_WITH_VARIATION = "retry_with_variation"
    RETRY_STANDARD = "retry_standard"
    ABORT_RETRIES = "abort_retries"


@dataclass
class RetryContext:
    """Context information for retry decisions"""
    attempt_number: int
    previous_result: Optional[Dict[str, Any]]
    error: Optional[Exception]
    is_deterministic: bool
    original_temperature: float
    model_name: str
    batch_size: int
    failure_reason: str = ""
    confidence_score: float = 0.0


@dataclass
class RetryResult:
    """Result of retry analysis"""
    decision: RetryDecision
    new_temperature: Optional[float] = None
    delay_seconds: float = 0.5
    reason: str = ""
    should_continue: bool = True


class IntelligentRetryStrategy:
    """
    PHASE 3: Intelligent retry strategy that makes smart decisions about when and how to retry
    
    Key Features:
    - Detects deterministic configurations and skips useless retries
    - Applies micro-variations for deterministic models when beneficial
    - Analyzes failure patterns to decide optimal retry strategy
    - Provides transparent logging of all decisions
    """
    
    def __init__(self, ai_configuration=None):
        self.ai_configuration = ai_configuration
        self.retry_history: Dict[str, list] = {}
        
        # Configuration from centralized config or defaults
        if ai_configuration:
            self.max_retries = ai_configuration.batch_retry_count
            self.base_delay = ai_configuration.batch_retry_base_delay
            self.temperature_increment = ai_configuration.retry_temperature_increment
            self.max_retry_temperature = ai_configuration.max_retry_temperature
            self.intelligent_retry_enabled = ai_configuration.intelligent_retry_enabled
            self.deterministic_skip_enabled = ai_configuration.deterministic_skip_retry
        else:
            # Fallback configuration
            self.max_retries = 2
            self.base_delay = 0.5
            self.temperature_increment = 0.1
            self.max_retry_temperature = 0.3
            self.intelligent_retry_enabled = True
            self.deterministic_skip_enabled = True
        
        logger.info(f"🧠 IntelligentRetryStrategy initialized - "
                   f"max_retries={self.max_retries}, "
                   f"intelligent={self.intelligent_retry_enabled}, "
                   f"deterministic_skip={self.deterministic_skip_enabled}")
    
    def should_retry(self, context: RetryContext) -> RetryResult:
        """
        Main decision method - determines if and how to retry
        
        Args:
            context: RetryContext with all relevant information
            
        Returns:
            RetryResult with decision and parameters
        """
        try:
            # Basic validation
            if context.attempt_number >= self.max_retries:
                return RetryResult(
                    decision=RetryDecision.ABORT_RETRIES,
                    reason=f"Maximum retries ({self.max_retries}) reached",
                    should_continue=False
                )
            
            if not self.intelligent_retry_enabled:
                return self._standard_retry_decision(context)
            
            # Analyze failure type
            failure_analysis = self._analyze_failure(context)
            
            # Make intelligent decision based on failure analysis
            if failure_analysis["is_confidence_failure"]:
                return self._handle_confidence_failure(context, failure_analysis)
            elif failure_analysis["is_api_error"]:
                return self._handle_api_error(context, failure_analysis)
            elif failure_analysis["is_deterministic_repeat"]:
                return self._handle_deterministic_repeat(context)
            else:
                return self._standard_retry_decision(context)
                
        except Exception as e:
            logger.error(f"❌ Error in retry strategy: {e}")
            return RetryResult(
                decision=RetryDecision.ABORT_RETRIES,
                reason=f"Error in retry analysis: {str(e)}",
                should_continue=False
            )
    
    def _analyze_failure(self, context: RetryContext) -> Dict[str, Any]:
        """Analyze the type of failure to determine best retry strategy"""
        analysis = {
            "is_confidence_failure": False,
            "is_api_error": False,
            "is_deterministic_repeat": False,
            "confidence_too_low": False,
            "identical_result": False
        }
        
        # Check if it's a confidence-related failure
        if context.previous_result and context.confidence_score > 0:
            if self.ai_configuration:
                threshold = self.ai_configuration.get_effective_confidence_threshold(context.batch_size, context.model_name)
            else:
                threshold = 0.5
            
            if context.confidence_score < threshold:
                analysis["is_confidence_failure"] = True
                analysis["confidence_too_low"] = True
                
                # Check if this is a deterministic configuration
                if context.is_deterministic and abs(context.original_temperature) < 0.001:
                    analysis["is_deterministic_repeat"] = True
        
        # Check for API errors
        if context.error:
            analysis["is_api_error"] = True
        
        # Check for identical results (deterministic repeat)
        if context.is_deterministic and not context.error:
            batch_key = f"{context.model_name}_{context.batch_size}"
            if batch_key in self.retry_history:
                previous_attempts = self.retry_history[batch_key]
                if len(previous_attempts) > 0:
                    # Simple check for identical confidence scores
                    last_confidence = previous_attempts[-1].get("confidence", 0)
                    if abs(last_confidence - context.confidence_score) < 0.01:
                        analysis["identical_result"] = True
                        analysis["is_deterministic_repeat"] = True
        
        return analysis
    
    def _handle_confidence_failure(self, context: RetryContext, analysis: Dict) -> RetryResult:
        """Handle failures due to low confidence scores"""
        
        # If deterministic and we've seen this before, consider skipping or adding variation
        if analysis["is_deterministic_repeat"]:
            if self.deterministic_skip_enabled and self.temperature_increment <= 0:
                return RetryResult(
                    decision=RetryDecision.SKIP_RETRY,
                    reason=f"Deterministic config (temp={context.original_temperature:.3f}) will produce identical low confidence ({context.confidence_score:.3f})",
                    should_continue=False
                )
            else:
                # Add temperature variation to break deterministic pattern
                new_temp = min(
                    context.original_temperature + (context.attempt_number * self.temperature_increment),
                    self.max_retry_temperature
                )
                
                return RetryResult(
                    decision=RetryDecision.RETRY_WITH_VARIATION,
                    new_temperature=new_temp,
                    delay_seconds=self.base_delay + (context.attempt_number * 0.3),
                    reason=f"Adding temperature variation ({new_temp:.3f}) to break deterministic low confidence pattern",
                    should_continue=True
                )
        else:
            # Non-deterministic confidence failure - standard retry
            return RetryResult(
                decision=RetryDecision.RETRY_STANDARD,
                delay_seconds=self.base_delay + (context.attempt_number * 0.3),
                reason=f"Confidence failure ({context.confidence_score:.3f}) - standard retry",
                should_continue=True
            )
    
    def _handle_api_error(self, context: RetryContext, analysis: Dict) -> RetryResult:
        """Handle API-related errors"""
        # For API errors, always retry with exponential backoff
        delay = self.base_delay * (2 ** context.attempt_number)
        
        return RetryResult(
            decision=RetryDecision.RETRY_STANDARD,
            delay_seconds=min(delay, 10.0),  # Cap at 10 seconds
            reason=f"API error retry with exponential backoff ({delay:.1f}s)",
            should_continue=True
        )
    
    def _handle_deterministic_repeat(self, context: RetryContext) -> RetryResult:
        """Handle deterministic configurations that will produce identical results"""
        
        if self.deterministic_skip_enabled:
            return RetryResult(
                decision=RetryDecision.SKIP_RETRY,
                reason=f"Deterministic configuration detected - identical results expected",
                should_continue=False
            )
        else:
            # Add slight temperature variation
            new_temp = min(
                context.original_temperature + (context.attempt_number * self.temperature_increment),
                self.max_retry_temperature
            )
            
            return RetryResult(
                decision=RetryDecision.RETRY_WITH_VARIATION,
                new_temperature=new_temp,
                delay_seconds=self.base_delay,
                reason=f"Deterministic config - adding temperature variation ({new_temp:.3f})",
                should_continue=True
            )
    
    def _standard_retry_decision(self, context: RetryContext) -> RetryResult:
        """Standard retry decision for when intelligent retry is disabled"""
        delay = self.base_delay + (context.attempt_number * 0.3)
        
        return RetryResult(
            decision=RetryDecision.RETRY_STANDARD,
            delay_seconds=delay,
            reason=f"Standard retry {context.attempt_number + 1}/{self.max_retries}",
            should_continue=True
        )
    
    def record_attempt(self, context: RetryContext, result: Any):
        """Record retry attempt for future analysis"""
        batch_key = f"{context.model_name}_{context.batch_size}"
        
        if batch_key not in self.retry_history:
            self.retry_history[batch_key] = []
        
        attempt_record = {
            "attempt": context.attempt_number,
            "confidence": context.confidence_score,
            "temperature": context.original_temperature,
            "success": result is not None and getattr(result, 'es_exitoso', lambda: False)(),
            "timestamp": time.time()
        }
        
        self.retry_history[batch_key].append(attempt_record)
        
        # Keep only last 10 attempts per batch type
        if len(self.retry_history[batch_key]) > 10:
            self.retry_history[batch_key] = self.retry_history[batch_key][-10:]
    
    def get_retry_statistics(self) -> Dict[str, Any]:
        """Get statistics about retry patterns"""
        if not self.retry_history:
            return {"total_batches": 0, "total_attempts": 0}
        
        total_attempts = sum(len(attempts) for attempts in self.retry_history.values())
        successful_batches = sum(
            1 for attempts in self.retry_history.values()
            if any(attempt["success"] for attempt in attempts)
        )
        
        return {
            "total_batches": len(self.retry_history),
            "total_attempts": total_attempts,
            "successful_batches": successful_batches,
            "average_attempts_per_batch": total_attempts / len(self.retry_history) if self.retry_history else 0,
            "success_rate": successful_batches / len(self.retry_history) if self.retry_history else 0
        }
    
    def clear_history(self):
        """Clear retry history"""
        self.retry_history.clear()
        logger.info("🧹 Retry history cleared")


def create_intelligent_retry_strategy(ai_configuration=None) -> IntelligentRetryStrategy:
    """Factory function to create an intelligent retry strategy"""
    return IntelligentRetryStrategy(ai_configuration)


def create_retry_context(attempt_number: int, previous_result: Any, error: Exception = None,
                        is_deterministic: bool = True, original_temperature: float = 0.0,
                        model_name: str = "unknown", batch_size: int = 20) -> RetryContext:
    """Helper function to create retry context"""
    
    confidence_score = 0.0
    failure_reason = ""
    
    if previous_result:
        if hasattr(previous_result, 'confianza_general'):
            confidence_score = previous_result.confianza_general
        elif hasattr(previous_result, 'es_exitoso'):
            confidence_score = 0.3 if not previous_result.es_exitoso() else 0.8
        
        if hasattr(previous_result, 'es_exitoso') and not previous_result.es_exitoso():
            failure_reason = "Validation failure"
    
    if error:
        failure_reason = f"API Error: {str(error)}"
    
    return RetryContext(
        attempt_number=attempt_number,
        previous_result=previous_result,
        error=error,
        is_deterministic=is_deterministic,
        original_temperature=original_temperature,
        model_name=model_name,
        batch_size=batch_size,
        failure_reason=failure_reason,
        confidence_score=confidence_score
    )