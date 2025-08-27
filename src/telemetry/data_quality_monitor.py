"""
Data Quality Monitoring and Telemetry
Tracks data quality issues and provides insights for improvement
"""

import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path
import threading

logger = logging.getLogger(__name__)

class DataQualityMonitor:
    """Monitor and track data quality issues across the application"""
    
    def __init__(self, log_dir: Optional[Path] = None):
        """
        Initialize data quality monitor
        
        Args:
            log_dir: Directory to store quality logs (optional)
        """
        self.log_dir = log_dir or Path(__file__).parent.parent.parent / 'logs' / 'data_quality'
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # In-memory metrics
        self.metrics = {
            'session_start': datetime.now().isoformat(),
            'files_processed': 0,
            'total_errors': 0,
            'key_errors': {},
            'empty_results': 0,
            'validation_failures': [],
            'performance_metrics': [],
            'data_quality_scores': []
        }
        
        # Thread-safe lock
        self._lock = threading.Lock()
        
        # Log file for current session
        self.session_file = self.log_dir / f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    def track_key_error(self, key: str, context: str = "unknown"):
        """
        Track missing dictionary keys
        
        Args:
            key: The missing key
            context: Where the error occurred
        """
        with self._lock:
            if key not in self.metrics['key_errors']:
                self.metrics['key_errors'][key] = {
                    'count': 0,
                    'contexts': []
                }
            
            self.metrics['key_errors'][key]['count'] += 1
            if context not in self.metrics['key_errors'][key]['contexts']:
                self.metrics['key_errors'][key]['contexts'].append(context)
            
            self.metrics['total_errors'] += 1
            logger.info(f"Tracked KeyError: '{key}' in {context}")
    
    def track_file_processing(self, filename: str, result_stats: Dict[str, Any]):
        """
        Track file processing statistics
        
        Args:
            filename: Name of processed file
            result_stats: Statistics about the processing result
        """
        with self._lock:
            self.metrics['files_processed'] += 1
            
            processing_record = {
                'timestamp': datetime.now().isoformat(),
                'filename': filename,
                'total_comments': result_stats.get('total', 0),
                'raw_comments': result_stats.get('raw_total', 0),
                'duplicates_removed': result_stats.get('duplicates_removed', 0),
                'has_ai_analysis': result_stats.get('analysis_method') == 'AI_ENHANCED',
                'processing_time': result_stats.get('processing_time', 0)
            }
            
            self.metrics['performance_metrics'].append(processing_record)
            
            # Track empty results
            if result_stats.get('total', 0) == 0:
                self.metrics['empty_results'] += 1
            
            logger.info(f"Tracked file processing: {filename} with {result_stats.get('total', 0)} comments")
    
    def track_validation_failure(self, issues: List[str], context: str = "unknown"):
        """
        Track validation failures
        
        Args:
            issues: List of validation issues
            context: Where the validation failed
        """
        with self._lock:
            failure_record = {
                'timestamp': datetime.now().isoformat(),
                'context': context,
                'issues': issues,
                'issue_count': len(issues)
            }
            
            self.metrics['validation_failures'].append(failure_record)
            self.metrics['total_errors'] += len(issues)
            
            logger.warning(f"Validation failure in {context}: {len(issues)} issues")
    
    def track_data_quality_score(self, score: float, context: str = "analysis"):
        """
        Track data quality scores
        
        Args:
            score: Quality score (0-100)
            context: Context of the score
        """
        with self._lock:
            score_record = {
                'timestamp': datetime.now().isoformat(),
                'score': score,
                'context': context
            }
            
            self.metrics['data_quality_scores'].append(score_record)
            logger.info(f"Data quality score for {context}: {score}%")
    
    def get_current_metrics(self) -> Dict[str, Any]:
        """Get current metrics snapshot"""
        with self._lock:
            return self.metrics.copy()
    
    def get_health_report(self) -> Dict[str, Any]:
        """
        Generate health report with recommendations
        
        Returns:
            Dictionary with health metrics and recommendations
        """
        with self._lock:
            # Calculate averages
            avg_quality = 0
            if self.metrics['data_quality_scores']:
                avg_quality = sum(s['score'] for s in self.metrics['data_quality_scores']) / len(self.metrics['data_quality_scores'])
            
            # Identify top issues
            top_key_errors = sorted(
                self.metrics['key_errors'].items(),
                key=lambda x: x[1]['count'],
                reverse=True
            )[:5]
            
            # Generate recommendations
            recommendations = []
            
            if avg_quality < 70:
                recommendations.append("Data quality is below acceptable threshold. Review validation rules.")
            
            if self.metrics['empty_results'] > 0:
                recommendations.append(f"Found {self.metrics['empty_results']} empty results. Check data preprocessing.")
            
            if top_key_errors:
                most_common_key = top_key_errors[0][0]
                recommendations.append(f"Most common missing key: '{most_common_key}'. Consider adding default handling.")
            
            if self.metrics['total_errors'] > self.metrics['files_processed'] * 5:
                recommendations.append("High error rate detected. Review error handling patterns.")
            
            return {
                'session_duration': (datetime.now() - datetime.fromisoformat(self.metrics['session_start'])).total_seconds(),
                'files_processed': self.metrics['files_processed'],
                'total_errors': self.metrics['total_errors'],
                'average_quality_score': round(avg_quality, 1),
                'empty_results_count': self.metrics['empty_results'],
                'top_missing_keys': dict(top_key_errors),
                'health_status': self._determine_health_status(avg_quality),
                'recommendations': recommendations
            }
    
    def _determine_health_status(self, avg_quality: float) -> str:
        """Determine overall health status"""
        if avg_quality >= 90:
            return "EXCELLENT"
        elif avg_quality >= 75:
            return "GOOD"
        elif avg_quality >= 60:
            return "FAIR"
        elif avg_quality >= 40:
            return "POOR"
        else:
            return "CRITICAL"
    
    def save_session_metrics(self):
        """Save current session metrics to file"""
        with self._lock:
            try:
                with open(self.session_file, 'w', encoding='utf-8') as f:
                    json.dump(self.metrics, f, indent=2, ensure_ascii=False)
                logger.info(f"Session metrics saved to {self.session_file}")
            except Exception as e:
                logger.error(f"Failed to save session metrics: {e}")
    
    def get_summary_statistics(self) -> str:
        """
        Get formatted summary statistics
        
        Returns:
            Formatted string with key statistics
        """
        report = self.get_health_report()
        
        summary = f"""
╔═══════════════════════════════════════════════════╗
║           DATA QUALITY MONITORING REPORT           ║
╠═══════════════════════════════════════════════════╣
║ Session Duration: {report['session_duration']:.1f}s
║ Files Processed: {report['files_processed']}
║ Total Errors: {report['total_errors']}
║ Average Quality: {report['average_quality_score']}%
║ Health Status: {report['health_status']}
╠═══════════════════════════════════════════════════╣
║ TOP ISSUES:
"""
        
        for key, data in list(report['top_missing_keys'].items())[:3]:
            summary += f"║   • '{key}': {data['count']} occurrences\n"
        
        if report['recommendations']:
            summary += "╠═══════════════════════════════════════════════════╣\n"
            summary += "║ RECOMMENDATIONS:\n"
            for rec in report['recommendations']:
                summary += f"║   → {rec}\n"
        
        summary += "╚═══════════════════════════════════════════════════╝"
        
        return summary
    
    def __del__(self):
        """Save metrics on cleanup"""
        try:
            self.save_session_metrics()
        except:
            pass  # Silently fail on cleanup


# Global monitor instance
_monitor = None

def get_monitor() -> DataQualityMonitor:
    """Get or create global monitor instance"""
    global _monitor
    if _monitor is None:
        _monitor = DataQualityMonitor()
    return _monitor

def track_quality_issue(issue_type: str, details: Any, context: str = "unknown"):
    """
    Convenience function to track quality issues
    
    Args:
        issue_type: Type of issue (key_error, validation, etc.)
        details: Issue details
        context: Where the issue occurred
    """
    monitor = get_monitor()
    
    if issue_type == "key_error":
        monitor.track_key_error(details, context)
    elif issue_type == "validation":
        monitor.track_validation_failure(details, context)
    elif issue_type == "quality_score":
        monitor.track_data_quality_score(details, context)
    else:
        logger.warning(f"Unknown issue type: {issue_type}")

def get_quality_report() -> str:
    """Get formatted quality report"""
    monitor = get_monitor()
    return monitor.get_summary_statistics()