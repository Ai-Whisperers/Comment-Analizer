# Configuration Guide - Comment Analyzer

## Overview

This guide covers all configuration options for the Comment Analyzer system, including environment variables, file configurations, and runtime settings.

## Environment Configuration

### Required Environment Variables

#### OpenAI API Key
```bash
OPENAI_API_KEY=sk-...  # Your OpenAI API key (REQUIRED)
```
**Note**: Without this key, the system will fall back to rule-based analysis only.

### Optional Environment Variables

#### AI Configuration
```bash
# Model Selection
OPENAI_MODEL=gpt-4                    # Default: gpt-4
                                       # Options: gpt-4, gpt-3.5-turbo

# Token Limits
OPENAI_MAX_TOKENS=4000                 # Default: 4000
                                       # Range: 100-8000

# Response Creativity
OPENAI_TEMPERATURE=0.7                 # Default: 0.7
                                       # Range: 0.0-1.0 (0=deterministic, 1=creative)
```

#### API Timeout Settings
```bash
API_TIMEOUT_SHORT=10                   # Quick operations (seconds)
API_TIMEOUT_MEDIUM=30                  # Standard operations
API_TIMEOUT_LONG=60                    # Batch operations
API_TIMEOUT_MAX=120                    # Maximum timeout
```

#### Application Settings
```bash
# Environment
APP_ENV=production                     # Options: development, production
DEBUG_MODE=False                       # Enable debug logging

# Processing Limits
MAX_FILE_SIZE_MB=50                    # Maximum upload file size
MAX_COMMENTS_PER_BATCH=1000            # Comments per API call
CACHE_TTL_SECONDS=900                  # Cache duration (15 min default)

# Security
SECRET_KEY=your-secret-key             # Session encryption key
SESSION_TIMEOUT_MINUTES=60             # User session timeout

# Rate Limiting
API_RATE_LIMIT_PER_MINUTE=60          # API calls per minute
API_RATE_LIMIT_PER_DAY=1000           # API calls per day
```

#### Logging Configuration
```bash
LOG_LEVEL=INFO                         # Options: DEBUG, INFO, WARNING, ERROR
LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

#### Server Configuration
```bash
STREAMLIT_PORT=8501                    # Web server port (default: 8501)
STREAMLIT_SERVER_ADDRESS=0.0.0.0       # Bind address
STREAMLIT_SERVER_HEADLESS=true         # Headless mode for Docker
```

## Configuration Files

### 1. `.env` File Template
Create a `.env` file in the project root:

```bash
# ====================================
# Comment Analyzer Configuration
# ====================================

# REQUIRED: OpenAI Configuration
OPENAI_API_KEY=sk-your-api-key-here

# OPTIONAL: Override defaults as needed
OPENAI_MODEL=gpt-4
OPENAI_MAX_TOKENS=4000
OPENAI_TEMPERATURE=0.7

# Application Settings
APP_ENV=production
DEBUG_MODE=False
MAX_FILE_SIZE_MB=50
MAX_COMMENTS_PER_BATCH=1000

# Security
SECRET_KEY=change-this-to-random-string
SESSION_TIMEOUT_MINUTES=60

# Logging
LOG_LEVEL=INFO

# Server (for Docker)
STREAMLIT_PORT=8501
```

### 2. Docker Environment

#### docker-compose.yml Environment Section
```yaml
environment:
  # API Configuration
  - OPENAI_API_KEY=${OPENAI_API_KEY}
  - OPENAI_MODEL=${OPENAI_MODEL:-gpt-4}
  - OPENAI_MAX_TOKENS=${OPENAI_MAX_TOKENS:-4000}
  
  # Application
  - APP_ENV=${APP_ENV:-production}
  - DEBUG_MODE=${DEBUG_MODE:-False}
  
  # Limits
  - MAX_FILE_SIZE_MB=${MAX_FILE_SIZE_MB:-50}
  - MAX_COMMENTS_PER_BATCH=${MAX_COMMENTS_PER_BATCH:-1000}
```

### 3. Python Configuration (`src/config.py`)

The system loads configuration in this order:
1. Environment variables
2. `.env` file
3. Default values

```python
class Config:
    # API Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
    OPENAI_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "4000"))
    OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
    
    # ... additional settings
```

## Streamlit Configuration

### 1. Programmatic Configuration
Set in `src/main.py`:

```python
st.set_page_config(
    page_title="Personal Paraguay — Análisis de Comentarios",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)
```

### 2. Theme Configuration
The application supports Dark and Light themes, controlled via UI toggle.

#### Dark Theme (Default)
- Background: #0E1117
- Primary: #8B5CF6
- Secondary: #06B6D4

#### Light Theme
- Background: #FFFFFF
- Primary: #8B5CF6
- Secondary: #06B6D4

### 3. Custom Streamlit Config
Create `.streamlit/config.toml`:

```toml
[theme]
base = "dark"
primaryColor = "#8B5CF6"
backgroundColor = "#0E1117"
secondaryBackgroundColor = "#262730"
textColor = "#FAFAFA"

[server]
port = 8501
address = "localhost"
headless = true

[browser]
gatherUsageStats = false
```

## Language Configuration

### Supported Languages
- **Spanish** (es) - Primary
- **Guarani** (gn) - Secondary
- **English** (en) - UI elements

### Language Detection Settings
Configure in analysis functions:

```python
LANGUAGE_SETTINGS = {
    'primary': 'es',
    'secondary': 'gn',
    'fallback': 'es',
    'auto_detect': True
}
```

## Processing Configuration

### Analysis Settings
```python
# Sentiment Analysis
SENTIMENT_CONFIDENCE_THRESHOLD = 0.7   # Minimum confidence
SENTIMENT_CATEGORIES = ['positive', 'negative', 'neutral']

# Pattern Detection
PATTERN_MIN_FREQUENCY = 3              # Minimum occurrences
PATTERN_CONFIDENCE = 0.6               # Detection threshold

# Batch Processing
BATCH_SIZE = 100                       # Comments per batch
MAX_RETRIES = 3                        # Retry failed requests
RETRY_DELAY = 2                        # Seconds between retries
```

### Theme Detection Configuration
```python
THEME_KEYWORDS = {
    'velocidad': ['lento', 'velocidad', 'demora'],
    'interrupciones': ['corte', 'cae', 'intermitente'],
    'servicio': ['atención', 'soporte', 'ayuda'],
    'precio': ['caro', 'costoso', 'tarifa'],
    'cobertura': ['señal', 'zona', 'alcance']
}
```

## Export Configuration

### Excel Export Settings
```python
EXCEL_CONFIG = {
    'max_rows': 1048576,           # Excel limit
    'max_comments_display': 10000,  # UI display limit
    'include_charts': True,
    'include_formatting': True,
    'compression': True
}
```

### PDF Export Settings
```python
PDF_CONFIG = {
    'page_size': 'A4',
    'orientation': 'portrait',
    'include_charts': True,
    'compress': True
}
```

## Security Configuration

### Input Validation
```python
VALIDATION_RULES = {
    'max_comment_length': 5000,
    'allowed_file_types': ['.csv', '.xlsx', '.xls'],
    'max_file_size_mb': 50,
    'sanitize_html': True,
    'prevent_sql_injection': True,
    'check_encoding': True
}
```

### Session Security
```python
SESSION_CONFIG = {
    'timeout_minutes': 60,
    'secure_cookies': True,
    'csrf_protection': True,
    'max_sessions': 100
}
```

## Performance Tuning

### Cache Configuration
```python
CACHE_CONFIG = {
    'enabled': True,
    'ttl_seconds': 900,              # 15 minutes
    'max_size_mb': 100,
    'eviction_policy': 'LRU'
}
```

### Memory Management
```python
MEMORY_CONFIG = {
    'max_memory_mb': 2048,
    'gc_threshold': 0.8,             # Trigger at 80% usage
    'chunk_size': 1000,              # Process in chunks
}
```

## Docker Configuration

### Resource Limits
```yaml
deploy:
  resources:
    limits:
      cpus: '2'
      memory: 2G
    reservations:
      cpus: '1'
      memory: 1G
```

### Health Check
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

## Development Configuration

### Debug Mode
```bash
# Enable debug mode
export DEBUG_MODE=True
export LOG_LEVEL=DEBUG

# Run with debug
streamlit run src/main.py --logger.level=debug
```

### Testing Configuration
```python
# pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = --cov=src --cov-report=term-missing
```

## Production Configuration

### Recommended Production Settings
```bash
# .env.production
OPENAI_API_KEY=sk-production-key
APP_ENV=production
DEBUG_MODE=False
LOG_LEVEL=WARNING
MAX_FILE_SIZE_MB=25
SESSION_TIMEOUT_MINUTES=30
API_RATE_LIMIT_PER_MINUTE=30
CACHE_TTL_SECONDS=1800
```

### Nginx Proxy Configuration
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Monitoring Configuration

### Logging Outputs
```python
LOGGING_CONFIG = {
    'handlers': {
        'file': {
            'filename': 'logs/app.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5
        },
        'console': {
            'level': 'INFO'
        }
    }
}
```

### Metrics Collection
```python
METRICS_CONFIG = {
    'enabled': True,
    'interval_seconds': 60,
    'export_format': 'json',
    'include_system_metrics': True
}
```

## Troubleshooting Configuration Issues

### Common Issues and Solutions

#### 1. API Key Not Found
```bash
# Check if key is set
echo $OPENAI_API_KEY

# Set temporarily
export OPENAI_API_KEY=sk-...

# Or add to .env file
echo "OPENAI_API_KEY=sk-..." >> .env
```

#### 2. Port Already in Use
```bash
# Change port
export STREAMLIT_PORT=8502
# Or
streamlit run src/main.py --server.port=8502
```

#### 3. Memory Issues
```bash
# Increase memory limits
export MAX_COMMENTS_PER_BATCH=500
export CHUNK_SIZE=500
```

#### 4. Slow Performance
```bash
# Enable caching
export CACHE_TTL_SECONDS=1800
export CACHE_ENABLED=True
```

## Configuration Validation

### Validate Configuration
Run the configuration validator:

```bash
python -c "from src.config import validate_config; validate_config()"
```

### Check Current Configuration
```bash
python -c "from src.config import Config; import json; print(json.dumps(Config.__dict__, indent=2))"
```

## Best Practices

1. **Never commit `.env` files** to version control
2. **Use different `.env` files** for development and production
3. **Rotate API keys** regularly
4. **Monitor API usage** to avoid rate limits
5. **Set appropriate timeouts** based on your data size
6. **Enable caching** for better performance
7. **Use DEBUG mode** only in development
8. **Configure logging** appropriately for each environment
9. **Set resource limits** in Docker to prevent memory issues
10. **Validate configuration** before deployment

---

**Document Version**: 1.0.0  
**Last Updated**: December 27, 2024  
**Configuration Schema Version**: 2.0.0