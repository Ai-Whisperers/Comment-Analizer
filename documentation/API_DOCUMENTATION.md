# API Documentation - Comment Analyzer

## Overview

This document describes the internal APIs and integration points within the Comment Analyzer system. While the application doesn't expose external REST APIs, it has well-defined internal interfaces for AI services and data processing.

## OpenAI API Integration

### Configuration

#### Environment Variables
```bash
OPENAI_API_KEY=sk-...          # Required: Your OpenAI API key
OPENAI_MODEL=gpt-4             # Optional: Model to use (default: gpt-4)
OPENAI_MAX_TOKENS=4000          # Optional: Max tokens per request
OPENAI_TEMPERATURE=0.7          # Optional: Response creativity (0-1)
```

### API Client (`src/sentiment_analysis/openai_analyzer.py`)

#### Class: `OpenAIAnalyzer`

##### Initialization
```python
analyzer = OpenAIAnalyzer(
    api_key=None,      # Uses env var if not provided
    model="gpt-4",     # Model selection
    use_cache=True     # Enable response caching
)
```

##### Methods

###### `analyze_batch(comments, language='es')`
Analyze multiple comments in a single API call.

**Parameters:**
- `comments` (List[str]): List of comments to analyze
- `language` (str): Target language code ('es' for Spanish)

**Returns:**
```python
{
    'results': [
        {
            'text': str,
            'sentiment': 'positive' | 'negative' | 'neutral',
            'confidence': float (0-1),
            'themes': List[str],
            'priority': 'high' | 'medium' | 'low',
            'category': str
        }
    ],
    'metadata': {
        'total': int,
        'processing_time': float,
        'model': str,
        'cached': bool
    }
}
```

**Example:**
```python
results = analyzer.analyze_batch([
    "Excelente servicio, muy rápido",
    "Internet muy lento, no funciona"
])
```

### AI Analysis Adapter (`src/ai_analysis_adapter.py`)

The adapter provides a unified interface with automatic fallback.

#### Class: `AIAnalysisAdapter`

##### Methods

###### `process_uploaded_file_with_ai(uploaded_file)`
Process an uploaded file with AI analysis.

**Parameters:**
- `uploaded_file`: Streamlit UploadedFile object or file-like object

**Returns:**
```python
{
    'total': int,                    # Total unique comments
    'raw_total': int,                # Total before deduplication
    'duplicates_removed': int,        # Number of duplicates
    'positive_count': int,            # Positive sentiments
    'neutral_count': int,             # Neutral sentiments
    'negative_count': int,            # Negative sentiments
    'positive_pct': float,            # Percentage positive
    'neutral_pct': float,             # Percentage neutral
    'negative_pct': float,            # Percentage negative
    'comments': List[str],            # Processed comments
    'sentiments': List[str],          # Sentiment labels
    'theme_counts': Dict[str, int],   # Theme frequency
    'analysis_method': str,           # 'AI_POWERED' or 'RULE_BASED'
    'ai_insights': Dict,              # AI-generated insights
    'overseer_validation': Dict       # Quality metrics
}
```

**Error Handling:**
- Automatically falls back to rule-based analysis if AI fails
- Returns `None` if file processing fails completely

## Internal Service APIs

### Analysis Service (`src/services/analysis_service.py`)

#### `AnalysisService`

##### `analyze_comments(comments, method='auto')`

**Parameters:**
- `comments` (List[str]): Comments to analyze
- `method` (str): 'ai', 'rule', or 'auto'

**Returns:**
```python
{
    'sentiments': List[str],
    'confidence_scores': List[float],
    'themes': Dict[str, int],
    'insights': Dict
}
```

### File Upload Service (`src/services/file_upload_service.py`)

#### `FileUploadService`

##### `validate_file(file_object)`

**Parameters:**
- `file_object`: File to validate

**Returns:**
```python
{
    'valid': bool,
    'error': str | None,
    'file_type': str,
    'size_mb': float
}
```

##### `extract_comments(file_object)`

**Parameters:**
- `file_object`: Validated file object

**Returns:**
```python
{
    'comments': List[str],
    'column_used': str,
    'total_rows': int,
    'metadata': Dict
}
```

### Pattern Detection API (`src/pattern_detection/pattern_detector.py`)

#### `PatternDetector`

##### `detect_patterns(texts)`

**Parameters:**
- `texts` (List[str]): Comments to analyze

**Returns:**
```python
{
    'service_patterns': {
        'connection_issues': int,
        'billing_problems': int,
        'customer_service': int,
        'installation': int
    },
    'emotion_patterns': {
        'frustration': int,
        'satisfaction': int,
        'anger': int,
        'happiness': int
    },
    'temporal_patterns': {
        'morning': int,
        'afternoon': int,
        'evening': int,
        'night': int
    },
    'anomalies': List[str],
    'trends': Dict
}
```

## Export APIs

### Professional Excel Export (`src/professional_excel_export.py`)

#### `create_professional_excel_report(results, output_path=None)`

**Parameters:**
- `results` (Dict): Analysis results dictionary
- `output_path` (str): Optional output file path

**Returns:**
- `bytes`: Excel file content if no output_path
- `str`: File path if output_path provided

**Sheets Generated:**
1. Executive Summary
2. Detailed Analysis
3. Comments with Sentiment
4. Theme Analysis
5. Pain Points Matrix
6. Recommendations
7. Raw Data

### Export Manager (`src/visualization/export_manager.py`)

#### `ExportManager`

##### `export(data, format='excel', **options)`

**Parameters:**
- `data` (Dict): Data to export
- `format` (str): 'excel', 'csv', 'json', 'pdf'
- `**options`: Format-specific options

**Returns:**
```python
{
    'success': bool,
    'file_path': str | None,
    'content': bytes | None,
    'error': str | None
}
```

## Cache Management API (`src/api/cache_manager.py`)

### `CacheManager`

#### Methods

##### `get(key)`
Retrieve cached value.

**Parameters:**
- `key` (str): Cache key

**Returns:**
- Cached value or `None`

##### `set(key, value, ttl=900)`
Store value in cache.

**Parameters:**
- `key` (str): Cache key
- `value`: Value to cache
- `ttl` (int): Time to live in seconds

##### `invalidate(pattern=None)`
Clear cache entries.

**Parameters:**
- `pattern` (str): Optional pattern to match

## Validation APIs (`src/utils/validators.py`)

### Input Validation Functions

#### `validate_comment(text)`

**Parameters:**
- `text` (str): Comment text to validate

**Returns:**
```python
{
    'valid': bool,
    'sanitized': str,
    'issues': List[str]
}
```

#### `validate_file_upload(file_object)`

**Parameters:**
- `file_object`: File to validate

**Returns:**
```python
{
    'valid': bool,
    'error': str | None,
    'file_info': Dict
}
```

#### `sanitize_for_export(text)`

**Parameters:**
- `text` (str): Text to sanitize

**Returns:**
- `str`: Sanitized text safe for export

## Session Management API (`src/services/session_manager.py`)

### `SessionManager`

#### Methods

##### `get_session_id()`
Get or create session identifier.

**Returns:**
- `str`: Session ID

##### `store_results(results)`
Store analysis results in session.

**Parameters:**
- `results` (Dict): Results to store

##### `get_results()`
Retrieve stored results.

**Returns:**
- `Dict`: Stored results or empty dict

## Error Handling

### Standard Error Response Format
```python
{
    'success': False,
    'error': {
        'code': str,           # Error code
        'message': str,        # Human-readable message
        'details': Dict,       # Additional context
        'timestamp': str       # ISO timestamp
    }
}
```

### Common Error Codes
- `API_KEY_MISSING`: OpenAI API key not configured
- `API_RATE_LIMIT`: Rate limit exceeded
- `FILE_TOO_LARGE`: File exceeds size limit
- `INVALID_FORMAT`: Unsupported file format
- `PROCESSING_ERROR`: General processing failure
- `VALIDATION_ERROR`: Input validation failed

## Rate Limiting

### OpenAI API Limits
- Requests per minute: 60 (configurable)
- Tokens per minute: 90,000 (GPT-4)
- Automatic retry with exponential backoff

### Internal Limits
- Max file size: 50MB
- Max comments per batch: 1,000
- Max concurrent sessions: 20

## Monitoring & Metrics

### Available Metrics

#### API Metrics
```python
{
    'api_calls_total': int,
    'api_calls_failed': int,
    'api_response_time_avg': float,
    'cache_hit_rate': float,
    'tokens_used': int
}
```

#### Processing Metrics
```python
{
    'files_processed': int,
    'comments_analyzed': int,
    'processing_time_avg': float,
    'fallback_count': int
}
```

## Testing APIs

### Mock API Client
For testing without consuming API credits:

```python
from tests.test_stubs import MockOpenAIClient

mock_client = MockOpenAIClient()
mock_client.analyze_batch(comments)  # Returns mock data
```

## Usage Examples

### Complete Analysis Pipeline
```python
from src.ai_analysis_adapter import AIAnalysisAdapter
from src.professional_excel_export import create_professional_excel_report

# Initialize adapter
adapter = AIAnalysisAdapter()

# Process file
with open('comments.csv', 'rb') as f:
    results = adapter.process_uploaded_file_with_ai(f)

# Generate report
if results:
    excel_content = create_professional_excel_report(results)
    with open('report.xlsx', 'wb') as f:
        f.write(excel_content)
```

### Direct OpenAI Analysis
```python
from src.sentiment_analysis.openai_analyzer import OpenAIAnalyzer

analyzer = OpenAIAnalyzer()
results = analyzer.analyze_batch([
    "El servicio es excelente",
    "Muy mal servicio, no lo recomiendo"
])

for r in results['results']:
    print(f"{r['text']}: {r['sentiment']} ({r['confidence']:.0%})")
```

## API Versioning

Current API version: **1.0.0**

### Version History
- 1.0.0 (2024-12): Initial stable release

### Deprecation Policy
- APIs marked deprecated will be maintained for 3 months
- Breaking changes require major version increment
- Backward compatibility maintained within major versions

---

**Document Version**: 1.0.0  
**Last Updated**: December 27, 2024  
**API Status**: Stable