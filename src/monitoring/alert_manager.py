"""
Alert Manager - Real monitoring with actual notifications
Sends alerts via console and log files (webhook ready)
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import threading
import time

logger = logging.getLogger(__name__)

class AlertManager:
    """Manages real-time alerts and notifications"""
    
    def __init__(self, alert_log_dir: Optional[Path] = None):
        self.alert_log_dir = alert_log_dir or Path(__file__).parent.parent.parent / 'logs' / 'alerts'
        self.alert_log_dir.mkdir(parents=True, exist_ok=True)
        
        # Alert thresholds
        self.thresholds = {
            'error_rate': 0.1,  # 10% error rate
            'processing_time': 30,  # 30 seconds
            'memory_usage_mb': 500,  # 500MB
            'failed_analyses': 3,  # 3 consecutive failures
        }
        
        # Alert state tracking
        self.alert_state = {
            'consecutive_failures': 0,
            'last_alert_time': None,
            'alert_cooldown_seconds': 300,  # 5 minute cooldown
        }
        
        self._lock = threading.Lock()
        
    def check_and_alert(self, metric_type: str, value: float, context: Dict[str, Any] = None):
        """Check metric against threshold and send alert if needed"""
        with self._lock:
            threshold = self.thresholds.get(metric_type)
            if threshold and value > threshold:
                self._send_alert(metric_type, value, threshold, context)
    
    def track_analysis_failure(self, error: str, file_name: str = "unknown"):
        """Track analysis failures and alert on consecutive failures"""
        with self._lock:
            self.alert_state['consecutive_failures'] += 1
            
            if self.alert_state['consecutive_failures'] >= self.thresholds['failed_analyses']:
                self._send_alert(
                    'consecutive_failures',
                    self.alert_state['consecutive_failures'],
                    self.thresholds['failed_analyses'],
                    {'error': error, 'file': file_name}
                )
                # Reset counter after alert
                self.alert_state['consecutive_failures'] = 0
    
    def track_analysis_success(self):
        """Reset failure counter on success"""
        with self._lock:
            self.alert_state['consecutive_failures'] = 0
    
    def _send_alert(self, alert_type: str, value: float, threshold: float, context: Dict[str, Any] = None):
        """Send alert through available channels"""
        
        # Check cooldown
        now = datetime.now()
        if self.alert_state['last_alert_time']:
            time_since_last = (now - self.alert_state['last_alert_time']).seconds
            if time_since_last < self.alert_state['alert_cooldown_seconds']:
                return  # Skip alert due to cooldown
        
        alert_data = {
            'timestamp': now.isoformat(),
            'alert_type': alert_type,
            'severity': self._get_severity(alert_type, value, threshold),
            'value': value,
            'threshold': threshold,
            'message': self._format_alert_message(alert_type, value, threshold),
            'context': context or {}
        }
        
        # Log to file (always)
        self._log_alert(alert_data)
        
        # Console notification (visible in logs)
        self._console_alert(alert_data)
        
        # Webhook placeholder (uncomment and configure for production)
        # self._send_webhook_alert(alert_data)
        
        self.alert_state['last_alert_time'] = now
    
    def _get_severity(self, alert_type: str, value: float, threshold: float) -> str:
        """Determine alert severity"""
        ratio = value / threshold if threshold > 0 else 999
        
        if ratio > 3:
            return 'CRITICAL'
        elif ratio > 2:
            return 'HIGH'
        elif ratio > 1.5:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def _format_alert_message(self, alert_type: str, value: float, threshold: float) -> str:
        """Format human-readable alert message"""
        messages = {
            'error_rate': f'Error rate {value:.1%} exceeds threshold {threshold:.1%}',
            'processing_time': f'Processing took {value:.1f}s, exceeding {threshold}s limit',
            'memory_usage_mb': f'Memory usage {value:.0f}MB exceeds {threshold:.0f}MB limit',
            'consecutive_failures': f'{int(value)} consecutive analysis failures detected',
        }
        return messages.get(alert_type, f'{alert_type}: {value} > {threshold}')
    
    def _log_alert(self, alert_data: Dict[str, Any]):
        """Log alert to file"""
        alert_file = self.alert_log_dir / f"alerts_{datetime.now().strftime('%Y%m%d')}.jsonl"
        
        try:
            with open(alert_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(alert_data, ensure_ascii=False) + '\n')
        except Exception as e:
            logger.error(f"Failed to log alert: {e}")
    
    def _console_alert(self, alert_data: Dict[str, Any]):
        """Send alert to console/logs"""
        severity = alert_data['severity']
        message = alert_data['message']
        
        alert_text = f"""
╔═══════════════════════════════════════════════════════╗
║                    SYSTEM ALERT                       ║
╠═══════════════════════════════════════════════════════╣
║ Severity: {severity:<10} Time: {datetime.now().strftime('%H:%M:%S')}
║ {message:<50}
╚═══════════════════════════════════════════════════════╝
"""
        
        if severity in ['CRITICAL', 'HIGH']:
            logger.error(alert_text)
        else:
            logger.warning(alert_text)
        
        # Also print for immediate visibility
        print(alert_text)
    
    def _send_webhook_alert(self, alert_data: Dict[str, Any]):
        """Send alert to webhook (configure for production)"""
        # Example webhook integration (uncomment and configure)
        """
        import requests
        
        webhook_url = "YOUR_WEBHOOK_URL"  # Slack, Discord, Teams, etc.
        
        try:
            payload = {
                'text': f"🚨 {alert_data['severity']} Alert: {alert_data['message']}",
                'attachments': [{
                    'color': 'danger' if alert_data['severity'] == 'CRITICAL' else 'warning',
                    'fields': [
                        {'title': 'Type', 'value': alert_data['alert_type'], 'short': True},
                        {'title': 'Value', 'value': str(alert_data['value']), 'short': True},
                    ]
                }]
            }
            
            response = requests.post(webhook_url, json=payload, timeout=5)
            response.raise_for_status()
        except Exception as e:
            logger.error(f"Failed to send webhook alert: {e}")
        """
        pass
    
    def get_alert_summary(self) -> Dict[str, Any]:
        """Get summary of recent alerts"""
        today = datetime.now().strftime('%Y%m%d')
        alert_file = self.alert_log_dir / f"alerts_{today}.jsonl"
        
        alerts = []
        if alert_file.exists():
            try:
                with open(alert_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip():
                            alerts.append(json.loads(line))
            except Exception as e:
                logger.error(f"Failed to read alerts: {e}")
        
        return {
            'total_alerts_today': len(alerts),
            'critical_alerts': sum(1 for a in alerts if a.get('severity') == 'CRITICAL'),
            'recent_alerts': alerts[-5:] if alerts else [],
            'alert_types': list(set(a.get('alert_type') for a in alerts))
        }


# Global alert manager instance
_alert_manager = None

def get_alert_manager() -> AlertManager:
    """Get or create global alert manager"""
    global _alert_manager
    if _alert_manager is None:
        _alert_manager = AlertManager()
    return _alert_manager

def send_alert(metric_type: str, value: float, context: Dict[str, Any] = None):
    """Convenience function to send alerts"""
    manager = get_alert_manager()
    manager.check_and_alert(metric_type, value, context)