# Configuration Guide - Comment Analyzer

## Overview

This guide covers all configuration options for the Comment Analyzer system, including environment variables, configuration files, and runtime settings.

---

## Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key for GPT-4 access | `sk-proj-abc123...` |

### Optional Variables

#### API Configuration

| Variable | Default | Description | Valid Values |
|----------|---------|-------------|--------------|
| `OPENAI_MODEL` | `gpt-4` | OpenAI model to use | `gpt-4`, `gpt-4-turbo`, `gpt-3.5-turbo` |
| `OPENAI_MAX_TOKENS` | `4000` | Maximum tokens per API request | `100-8000` |
| `OPENAI_TEMPERATURE` | `0.7` | Response creativity (0=deterministic, 1=creative) | `0.0-1.0` |
| `OPENAI_TIMEOUT` | `30` | API request timeout in seconds | `10-120` |

#### Application Settings

| Variable | Default | Description | Valid Values |
|----------|---------|-------------|--------------|
| `LOG_LEVEL` | `INFO` | Logging verbosity | `DEBUG`, `INFO`, `WARNING`, `ERROR` |
| `STREAMLIT_PORT` | `8501` | Port for Streamlit application (configurable) | Any available port |
| `MAX_FILE_SIZE_MB` | `50` | Maximum upload file size in MB | `1-100` |
| `CACHE_TTL` | `3600` | Cache time-to-live in seconds | `0-86400` |
| `BATCH_SIZE` | `10` | Comments per API batch | `1-50` |

#### Feature Flags

| Variable | Default | Description |
|----------|---------|-------------|
| `ENABLE_AI_OVERSEER` | `true` | Enable AI quality validation |
| `ENABLE_CACHE` | `true` | Enable API response caching |
| `ENABLE_FALLBACK` | `true` | Enable rule-based fallback |
| `ENABLE_METRICS` | `false` | Enable detailed metrics collection |
| `DEBUG_MODE` | `false` | Enable debug output |

---

## Configuration Files

### `.env` File

Create a `.env` file in the project root:

```bash
# Required
OPENAI_API_KEY=sk-proj-your-key-here

# Optional API Settings
OPENAI_MODEL=gpt-4
OPENAI_MAX_TOKENS=4000
OPENAI_TEMPERATURE=0.7

# Application Settings
LOG_LEVEL=INFO
STREAMLIT_PORT=8501  # Configurable port (default: 8501)
MAX_FILE_SIZE_MB=50

# Features
ENABLE_AI_OVERSEER=true
ENABLE_CACHE=true
ENABLE_FALLBACK=true
```

### `analysis_config.yaml`

Location: `src/analysis_config.yaml`

```yaml
# Analysis Configuration
analysis:
  min_confidence: 0.7
  max_themes: 10
  emotion_detection: true
  language_detection: true
  
# Sentiment Thresholds
sentiment:
  positive_threshold: 0.6
  negative_threshold: -0.6
  neutral_range: [-0.6, 0.6]

# Theme Detection
themes:
  min_frequency: 2
  max_themes: 15
  common_themes:
    - service_quality
    - internet_speed
    - customer_support
    - billing
    - installation

# Processing Options
processing:
  remove_duplicates: true
  clean_text: true
  detect_language: true
  max_comment_length: 5000
```

---

## Streamlit Configuration

### `.streamlit/config.toml`

```toml
[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#0E1117"
secondaryBackgroundColor = "#262730"
textColor = "#FAFAFA"
font = "sans serif"

[server]
port = ${STREAMLIT_PORT:-8501}  # Uses environment variable
address = "localhost"
headless = true
runOnSave = false
maxUploadSize = 50

[browser]
gatherUsageStats = false
```

---

## Docker Configuration

### Environment Variables for Docker

```dockerfile
# Dockerfile
ENV OPENAI_API_KEY=${OPENAI_API_KEY}
ENV OPENAI_MODEL=gpt-4
ENV LOG_LEVEL=INFO
ENV STREAMLIT_PORT=${STREAMLIT_PORT:-8501}
```

### Docker Compose Configuration

```yaml
# docker-compose.yml
version: '3.8'
services:
  comment-analyzer:
    build: .
    ports:
      - "${STREAMLIT_PORT:-8501}:${STREAMLIT_PORT:-8501}"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - OPENAI_MODEL=gpt-4
      - LOG_LEVEL=INFO
    volumes:
      - ./data:/app/data
      - ./outputs:/app/outputs
```

---

## Logging Configuration

### Log Levels

| Level | Description | Use Case |
|-------|-------------|----------|
| `DEBUG` | Detailed information | Development and troubleshooting |
| `INFO` | General information | Normal operation |
| `WARNING` | Warning messages | Potential issues |
| `ERROR` | Error messages | Failures requiring attention |

### Log File Location

```
logs/
├── comment_analyzer.log      # Main application log
├── api_requests.log          # API request/response log
└── error.log                 # Error-only log
```

### Custom Logging Configuration

```python
# src/config.py
LOGGING_CONFIG = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        }
    },
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'logs/comment_analyzer.log',
            'formatter': 'default'
        }
    },
    'root': {
        'level': os.getenv('LOG_LEVEL', 'INFO'),
        'handlers': ['file']
    }
}
```

---

## Performance Tuning

### Memory Management

```bash
# Optimize for large files
export MAX_FILE_SIZE_MB=100
export BATCH_SIZE=20
export CACHE_TTL=7200
```

### API Optimization

```bash
# Reduce API costs
export OPENAI_MODEL=gpt-3.5-turbo
export OPENAI_MAX_TOKENS=2000
export ENABLE_CACHE=true
export BATCH_SIZE=25
```

### High-Volume Processing

```bash
# Optimize for speed
export BATCH_SIZE=50
export ENABLE_CACHE=true
export CACHE_TTL=86400
export OPENAI_TIMEOUT=60
```

---

## Security Configuration

### API Key Management

1. **Never commit API keys to version control**
2. **Use environment variables or secrets management**
3. **Rotate keys regularly**
4. **Use different keys for dev/prod**

### Secure Configuration Example

```bash
# Production setup
export OPENAI_API_KEY=$(vault read -field=key secret/openai)
export LOG_LEVEL=WARNING
export DEBUG_MODE=false
export ENABLE_METRICS=true
```

---

## Development vs Production

### Development Configuration

```bash
# .env.development
OPENAI_API_KEY=sk-dev-key
OPENAI_MODEL=gpt-3.5-turbo
LOG_LEVEL=DEBUG
DEBUG_MODE=true
ENABLE_METRICS=true
CACHE_TTL=60
```

### Production Configuration

```bash
# .env.production
OPENAI_API_KEY=sk-prod-key
OPENAI_MODEL=gpt-4
LOG_LEVEL=WARNING
DEBUG_MODE=false
ENABLE_METRICS=true
CACHE_TTL=3600
```

---

## Configuration Validation

### Startup Validation

The application validates configuration on startup:

1. **API Key Check**: Verifies OPENAI_API_KEY is set
2. **Model Validation**: Ensures selected model is available
3. **Port Availability**: Checks if configured port is free
4. **Directory Creation**: Creates required directories

### Health Check Endpoint

```bash
curl http://localhost:${STREAMLIT_PORT:-8501}/_stcore/health
```

Response:
```json
{
  "status": "healthy",
  "config": {
    "api_configured": true,
    "cache_enabled": true,
    "overseer_enabled": true
  }
}
```

---

## Troubleshooting Configuration Issues

### Common Issues and Solutions

#### API Key Not Working
```bash
# Verify key is set
echo $OPENAI_API_KEY

# Test API connection
python -c "from openai import OpenAI; client = OpenAI(); print('OK')"
```

#### Port Already in Use
```bash
# Change port
export STREAMLIT_PORT=8502
streamlit run src/main.py --server.port 8502
```

#### Cache Not Working
```bash
# Check cache directory permissions
ls -la data/cache/

# Clear cache
rm -rf data/cache/*
```

---

## Configuration Best Practices

1. **Use `.env` files** for local development
2. **Never hardcode sensitive values**
3. **Document all custom configurations**
4. **Use consistent naming conventions**
5. **Validate configuration on startup**
6. **Provide sensible defaults**
7. **Log configuration values (except secrets)**
8. **Use feature flags for experimental features**

---

## Migration Guide

### From Version 0.x to 1.0

```bash
# Old configuration
OPENAI_KEY=sk-old-key

# New configuration
OPENAI_API_KEY=sk-old-key  # Note: renamed variable
```

---

## Configuration Schema Reference

### Complete ENV Schema

```typescript
interface EnvironmentConfig {
  // Required
  OPENAI_API_KEY: string;
  
  // API Settings
  OPENAI_MODEL?: 'gpt-4' | 'gpt-3.5-turbo';
  OPENAI_MAX_TOKENS?: number;  // 100-8000
  OPENAI_TEMPERATURE?: number; // 0.0-1.0
  OPENAI_TIMEOUT?: number;     // seconds
  
  // Application
  LOG_LEVEL?: 'DEBUG' | 'INFO' | 'WARNING' | 'ERROR';
  STREAMLIT_PORT?: number;
  MAX_FILE_SIZE_MB?: number;
  CACHE_TTL?: number;
  BATCH_SIZE?: number;
  
  // Features
  ENABLE_AI_OVERSEER?: boolean;
  ENABLE_CACHE?: boolean;
  ENABLE_FALLBACK?: boolean;
  ENABLE_METRICS?: boolean;
  DEBUG_MODE?: boolean;
}
```

---

**Document Version**: 1.0.0  
**Last Updated**: August 27, 2025  
**Configuration Status**: Current