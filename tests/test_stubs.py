"""
Test stubs for missing or renamed classes
"""

class APIClient:
    """Stub APIClient for testing"""
    def __init__(self, api_key="test"):
        self.api_key = api_key
        self.max_tokens = 4000
        self.batch_size = 10
    
    def analyze_sentiment(self, text):
        return "negative" if "bad" in text.lower() else "positive"
    
    def analyze_sentiment_with_retry(self, text):
        return self.analyze_sentiment(text)
    
    def batch_analyze(self, texts):
        return [self.analyze_sentiment(t) for t in texts]


class APIOptimizer:
    """Stub APIOptimizer for testing"""
    def __init__(self):
        self.max_tokens = 4000
        self.batch_size = 10
    
    def optimize_payload(self, text):
        return text[:self.max_tokens]
    
    def create_optimal_batches(self, items):
        batches = []
        for i in range(0, len(items), self.batch_size):
            batches.append(items[i:i + self.batch_size])
        return batches
    
    def estimate_tokens(self, text):
        return len(text) // 4
    
    def estimate_cost(self, tokens):
        return tokens * 0.00001
    
    def can_make_request(self):
        return True
    
    def record_request(self):
        pass
    
    def should_throttle(self):
        return False


class APIMonitor:
    """Stub APIMonitor for testing"""
    def __init__(self):
        self.requests = []
        self.errors = []
    
    def record_request(self, endpoint, status_code, response_time, error=None):
        self.requests.append({
            'endpoint': endpoint,
            'status_code': status_code,
            'response_time': response_time,
            'error': error
        })
        if status_code >= 400:
            self.errors.append(error)
    
    def get_statistics(self):
        total = len(self.requests)
        successful = sum(1 for r in self.requests if r['status_code'] < 400)
        failed = total - successful
        avg_time = sum(r['response_time'] for r in self.requests) / max(total, 1)
        
        return {
            'total_requests': total,
            'successful_requests': successful,
            'failed_requests': failed,
            'average_response_time': avg_time,
            'error_rate': failed / max(total, 1)
        }
    
    def is_circuit_open(self):
        recent_errors = sum(1 for r in self.requests[-5:] if r.get('status_code', 200) >= 500)
        return recent_errors >= 5
    
    def should_allow_request(self):
        return not self.is_circuit_open()
    
    def get_health_status(self):
        stats = self.get_statistics()
        error_rate = stats['error_rate']
        
        if error_rate == 0:
            status = 'healthy'
        elif error_rate < 0.5:
            status = 'degraded'
        else:
            status = 'unhealthy'
        
        return {
            'status': status,
            'error_rate': error_rate
        }
    
    def get_alerts(self):
        alerts = []
        stats = self.get_statistics()
        
        if stats['error_rate'] > 0.5:
            alerts.append({
                'severity': 'high',
                'message': 'High error rate detected'
            })
        
        return alerts


class CommentReader:
    """Stub CommentReader for testing"""
    def __init__(self):
        pass
    
    def read_file(self, filepath):
        import pandas as pd
        if filepath.endswith('.csv'):
            return pd.read_csv(filepath)
        return pd.read_excel(filepath)
    
    def detect_comment_column(self, df):
        for col in df.columns:
            if 'comment' in col.lower() or 'feedback' in col.lower():
                return col
        return df.columns[0] if len(df.columns) > 0 else None
    
    def clean_comments(self, comments):
        cleaned = []
        for c in comments:
            if c is None:
                cleaned.append("")
            else:
                cleaned.append(str(c).strip())
        return cleaned
    
    def remove_duplicates(self, comments):
        from collections import Counter
        lower_comments = [str(c).lower() for c in comments]
        counts = Counter(lower_comments)
        seen = set()
        unique = []
        
        for c in comments:
            lower = str(c).lower()
            if lower not in seen:
                seen.add(lower)
                unique.append(c)
        
        return unique, dict(counts)
    
    def extract_metadata(self, df):
        return {
            'total_rows': len(df),
            'columns': list(df.columns),
            'has_nps': 'NPS' in df.columns,
            'has_ratings': 'Nota' in df.columns or 'Rating' in df.columns
        }


class LanguageDetector:
    """Stub LanguageDetector for testing"""
    def __init__(self):
        pass
    
    def detect(self, text):
        if not text or not str(text).strip():
            return 'unknown'
        
        text_lower = str(text).lower()
        spanish_words = ['el', 'la', 'es', 'está', 'hola', 'servicio']
        english_words = ['the', 'is', 'hello', 'service', 'and']
        
        spanish_count = sum(1 for w in spanish_words if w in text_lower)
        english_count = sum(1 for w in english_words if w in text_lower)
        
        if spanish_count > english_count:
            return 'es'
        elif english_count > spanish_count:
            return 'en'
        return 'unknown'
    
    def detect_batch(self, texts):
        return [self.detect(t) for t in texts]
    
    def detect_with_confidence(self, text):
        lang = self.detect(text)
        confidence = 0.9 if lang != 'unknown' else 0.1
        return {
            'language': lang,
            'confidence': confidence
        }