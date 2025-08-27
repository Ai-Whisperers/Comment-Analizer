"""
Result Dictionary Schema Validation
Ensures data consistency and catches missing fields early
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class ResultSchemaValidator:
    """Validates analysis result dictionaries against expected schema"""
    
    # Define required and optional fields with their types and defaults
    SCHEMA = {
        'required': {
            'total': (int, 0),
            'comments': (list, []),
            'sentiments': (list, []),
            'analysis_date': (str, datetime.now().strftime('%Y-%m-%d')),
            'original_filename': (str, 'unknown.xlsx'),
        },
        'optional': {
            'raw_total': (int, 0),
            'duplicates_removed': (int, 0),
            'comment_frequencies': (dict, {}),
            'theme_counts': (dict, {}),
            'theme_examples': (dict, {}),
            'positive_count': (int, 0),
            'neutral_count': (int, 0),
            'negative_count': (int, 0),
            'positive_pct': (float, 0.0),
            'neutral_pct': (float, 0.0),
            'negative_pct': (float, 0.0),
            'file_size': (int, 0),
            'avg_length': (float, 0.0),
            'enhanced_results': (list, []),
            'insights': (list, []),
            'alerts': (list, []),
            'satisfaction_trend': (dict, {}),
            'nps': (dict, {}),
            'churn_analysis': (dict, {}),
            'urgency_distribution': (dict, {}),
            'competitor_analysis': (dict, {}),
            'service_issues_summary': (dict, {}),
            'rating_data': (dict, {}),
            'csi_analysis': (dict, {}),
            'analysis_method': (str, 'RULE_BASED'),
        }
    }
    
    def __init__(self, enable_telemetry: bool = True):
        """Initialize validator with optional telemetry"""
        self.enable_telemetry = enable_telemetry
        self.validation_stats = {
            'total_validations': 0,
            'missing_required': {},
            'missing_optional': {},
            'type_mismatches': {},
            'fields_fixed': 0
        }
    
    def validate_and_fix(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and fix result dictionary
        
        Args:
            results: Dictionary to validate
            
        Returns:
            Fixed dictionary with all required fields
        """
        self.validation_stats['total_validations'] += 1
        fixed_results = results.copy()
        
        # Check and fix required fields
        for field, (expected_type, default) in self.SCHEMA['required'].items():
            if field not in fixed_results:
                self._log_missing_field(field, 'required')
                fixed_results[field] = default
                self.validation_stats['fields_fixed'] += 1
            elif not isinstance(fixed_results[field], expected_type):
                self._log_type_mismatch(field, type(fixed_results[field]), expected_type)
                fixed_results[field] = default
                self.validation_stats['fields_fixed'] += 1
        
        # Check and fix optional fields if accessed
        for field, (expected_type, default) in self.SCHEMA['optional'].items():
            if field not in fixed_results:
                self._log_missing_field(field, 'optional')
                fixed_results[field] = default
                self.validation_stats['fields_fixed'] += 1
            elif not isinstance(fixed_results[field], expected_type):
                self._log_type_mismatch(field, type(fixed_results[field]), expected_type)
                fixed_results[field] = default
                self.validation_stats['fields_fixed'] += 1
        
        # Ensure list lengths match
        self._ensure_list_consistency(fixed_results)
        
        return fixed_results
    
    def _ensure_list_consistency(self, results: Dict[str, Any]):
        """Ensure comments and sentiments lists have same length"""
        comments_len = len(results.get('comments', []))
        sentiments_len = len(results.get('sentiments', []))
        
        if comments_len != sentiments_len:
            logger.warning(f"List length mismatch: comments={comments_len}, sentiments={sentiments_len}")
            if comments_len > sentiments_len:
                # Pad sentiments with 'neutral'
                results['sentiments'].extend(['neutral'] * (comments_len - sentiments_len))
            elif sentiments_len > comments_len:
                # Trim sentiments
                results['sentiments'] = results['sentiments'][:comments_len]
    
    def _log_missing_field(self, field: str, field_type: str):
        """Log missing field for telemetry"""
        if self.enable_telemetry:
            key = f'missing_{field_type}'
            if field not in self.validation_stats[key]:
                self.validation_stats[key][field] = 0
            self.validation_stats[key][field] += 1
            logger.debug(f"Missing {field_type} field: {field}")
    
    def _log_type_mismatch(self, field: str, actual_type: type, expected_type: type):
        """Log type mismatch for telemetry"""
        if self.enable_telemetry:
            if field not in self.validation_stats['type_mismatches']:
                self.validation_stats['type_mismatches'][field] = []
            self.validation_stats['type_mismatches'][field].append({
                'actual': str(actual_type),
                'expected': str(expected_type)
            })
            logger.warning(f"Type mismatch for {field}: expected {expected_type}, got {actual_type}")
    
    def get_validation_report(self) -> Dict[str, Any]:
        """Get telemetry report on validation issues"""
        return {
            'total_validations': self.validation_stats['total_validations'],
            'fields_fixed': self.validation_stats['fields_fixed'],
            'missing_required_fields': self.validation_stats['missing_required'],
            'missing_optional_fields': self.validation_stats['missing_optional'],
            'type_mismatches': self.validation_stats['type_mismatches'],
            'health_score': self._calculate_health_score()
        }
    
    def _calculate_health_score(self) -> float:
        """Calculate data quality health score (0-100)"""
        if self.validation_stats['total_validations'] == 0:
            return 100.0
        
        # Penalize for missing required fields more than optional
        required_penalty = sum(self.validation_stats['missing_required'].values()) * 10
        optional_penalty = sum(self.validation_stats['missing_optional'].values()) * 2
        type_penalty = len(self.validation_stats['type_mismatches']) * 5
        
        total_penalty = required_penalty + optional_penalty + type_penalty
        avg_penalty = total_penalty / max(self.validation_stats['total_validations'], 1)
        
        health_score = max(0, 100 - avg_penalty)
        return round(health_score, 1)
    
    def validate_only(self, results: Dict[str, Any]) -> List[str]:
        """
        Validate without fixing, return list of issues
        
        Args:
            results: Dictionary to validate
            
        Returns:
            List of validation issues
        """
        issues = []
        
        # Check required fields
        for field in self.SCHEMA['required']:
            if field not in results:
                issues.append(f"Missing required field: {field}")
            elif not isinstance(results[field], self.SCHEMA['required'][field][0]):
                issues.append(f"Type mismatch for {field}: expected {self.SCHEMA['required'][field][0].__name__}")
        
        # Check list consistency
        comments_len = len(results.get('comments', []))
        sentiments_len = len(results.get('sentiments', []))
        if comments_len != sentiments_len:
            issues.append(f"List length mismatch: comments={comments_len}, sentiments={sentiments_len}")
        
        return issues


# Global validator instance
_validator = None

def get_validator() -> ResultSchemaValidator:
    """Get or create global validator instance"""
    global _validator
    if _validator is None:
        _validator = ResultSchemaValidator(enable_telemetry=True)
    return _validator

def validate_results(results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convenience function to validate and fix results
    
    Args:
        results: Dictionary to validate
        
    Returns:
        Fixed dictionary with all required fields
    """
    validator = get_validator()
    return validator.validate_and_fix(results)