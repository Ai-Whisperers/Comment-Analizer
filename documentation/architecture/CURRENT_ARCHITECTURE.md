# Current System Architecture - Comment Analyzer

## Executive Summary

This document describes the **actual current architecture** of the Comment Analyzer system as of December 27, 2024. It supersedes any previous architectural documents that may contain outdated information.

## System Overview

### Technology Stack
- **Frontend**: Streamlit 1.28+ (Python-based web framework)
- **Backend**: Python 3.12
- **AI Service**: OpenAI GPT-4 API
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly
- **Export**: XlsxWriter, ReportLab
- **Containerization**: Docker with multi-stage builds
- **Testing**: Pytest with 92+ tests

### Architecture Pattern
The system follows a **modular monolithic architecture** with clear separation of concerns:
- Presentation Layer (Streamlit UI)
- Service Layer (Business Logic)
- Data Access Layer (File I/O, API clients)
- Integration Layer (AI services with fallback)

## Core Components

### 1. Entry Points

#### Primary Entry Point
- **`src/main.py`** - Streamlit application
  - Initializes UI components
  - Manages session state
  - Orchestrates analysis workflow
  - Handles file uploads
  - Renders results

#### Alternative Entry
- **`run.py`** - Python launcher script
  - Executes: `streamlit run src/main.py`

### 2. Configuration Management

#### `src/config.py`
- Environment variable loading via `.env`
- API key management
- Default settings:
  - Port: **8501** (not 8503)
  - Model: GPT-4
  - Max tokens: 4000
  - Temperature: 0.7

### 3. AI Integration Layer

#### `src/ai_analysis_adapter.py`
- **Primary AI interface**
- Manages OpenAI API calls
- Implements fallback mechanism:
  1. Try OpenAI API
  2. Fall back to enhanced analyzer
  3. Fall back to improved analyzer
- Standardizes output format

#### `src/ai_overseer.py`
- **Quality validation system**
- Validates analysis results
- Calculates confidence scores
- Provides quality metrics
- Ensures consistency

#### `src/sentiment_analysis/openai_analyzer.py`
- Direct OpenAI API integration
- Batch processing capabilities
- Response caching
- Error handling with retries

### 4. Data Processing Pipeline

#### `src/data_processing/comment_reader.py`
- File format detection (CSV, Excel)
- Encoding detection and handling
- Column identification
- Data validation

#### `src/data_processing/language_detector.py`
- Spanish/Guarani detection
- Language-specific processing
- Character encoding handling

### 5. Analysis Modules

#### `src/pattern_detection/pattern_detector.py`
- Service pattern detection
- Emotion analysis
- Temporal patterns
- Anomaly detection
- Trend analysis

#### `src/sentiment_analysis/enhanced_analyzer.py`
- Rule-based sentiment analysis
- Spanish language optimization
- Fallback for when AI unavailable

### 6. Export System

#### `src/professional_excel_export.py`
- Multi-sheet Excel reports
- Executive summaries
- Charts and visualizations
- Conditional formatting
- KPI dashboards

#### `src/simple_excel_export.py`
- Basic Excel export
- Lightweight alternative
- Quick data dumps

#### `src/visualization/export_manager.py`
- Export orchestration
- Format selection
- File generation

### 7. UI Components

#### `src/ui_styling.py`
- Theme management (Dark/Light)
- CSS injection
- Responsive design
- Animation effects
- Component styling

#### `src/components/optimized_file_upload_ui.py`
- File upload interface
- Validation feedback
- Progress indicators

#### `src/components/enhanced_results_ui.py`
- Results visualization
- Interactive charts
- Metrics display

### 8. Service Layer

#### `src/services/analysis_service.py`
- Analysis orchestration
- Workflow management
- Result aggregation

#### `src/services/file_upload_service.py`
- File handling
- Size validation
- Format verification

#### `src/services/session_manager.py`
- Streamlit session state
- User context management
- Persistence handling

### 9. Security & Validation

#### `src/utils/validators.py`
- Input sanitization
- SQL injection prevention
- XSS protection
- File validation
- Size limits enforcement

### 10. API Management

#### `src/api/cache_manager.py`
- Response caching
- Cache invalidation
- Performance optimization

#### `src/api/api_optimizer.py`
- Batch processing
- Request optimization
- Rate limiting

#### `src/api/monitoring.py`
- API usage tracking
- Error monitoring
- Performance metrics

## Data Flow

### Analysis Pipeline
```
1. User uploads file (CSV/Excel)
   ↓
2. File validation (validators.py)
   ↓
3. Data extraction (comment_reader.py)
   ↓
4. Language detection (language_detector.py)
   ↓
5. AI Analysis (ai_analysis_adapter.py)
   ├─→ Success: OpenAI API
   └─→ Fallback: Rule-based
   ↓
6. Quality validation (ai_overseer.py)
   ↓
7. Pattern detection (pattern_detector.py)
   ↓
8. Results formatting
   ↓
9. UI rendering (main.py)
   ↓
10. Export generation (Excel/PDF)
```

## Deployment Architecture

### Docker Container Structure
```
Multi-stage build:
1. Base stage (Python 3.12-slim)
2. Dependencies stage (pip packages)
3. Runtime stage (application)

Security:
- Non-root user (appuser:1000)
- Read-only mount for .env
- Volume mounts for data persistence
```

### Directory Structure
```
/app/
├── src/                 # Application code
├── data/               # User data
│   ├── raw/           # Uploaded files
│   └── processed/     # Processed data
├── outputs/            # Generated reports
│   ├── exports/       # Excel/CSV files
│   └── reports/       # PDF reports
├── logs/              # Application logs
└── client_input/      # Upload staging
```

### Health Monitoring
- Endpoint: `http://localhost:8501/_stcore/health`
- Interval: 30 seconds
- Timeout: 10 seconds
- Retries: 3

## Bootstrap Process

### Initialization Sequence
1. **Environment Setup**
   - Load .env file
   - Validate API keys
   - Set configuration

2. **Directory Creation**
   - Ensure required directories exist
   - Set permissions

3. **Logging Setup**
   - Configure rotating file handler
   - Set log levels

4. **Streamlit Configuration**
   - Page configuration
   - Theme initialization
   - Session state setup

5. **Service Initialization**
   - AI adapter setup
   - Cache manager init
   - Validator loading

6. **UI Rendering**
   - Component initialization
   - Style injection
   - Event handlers

7. **Ready State**
   - Listening on port 8501
   - Health check active

## Key Design Decisions

### 1. Streamlit Over React
- **Rationale**: Faster development, Python ecosystem, built-in components
- **Trade-offs**: Less UI flexibility, Python-only

### 2. Monolithic Architecture
- **Rationale**: Simpler deployment, easier maintenance, sufficient for scale
- **Trade-offs**: Less scalability, harder to distribute

### 3. AI with Fallback
- **Rationale**: Reliability, cost management, offline capability
- **Trade-offs**: Complexity, maintenance of dual systems

### 4. File-based Processing
- **Rationale**: Simple, stateless, easy to debug
- **Trade-offs**: Not real-time, batch-oriented

## Performance Characteristics

### Capacity
- Max file size: 50MB
- Max comments: 10,000 per batch
- Concurrent users: ~10-20 (Streamlit limitation)

### Response Times
- File upload: < 2 seconds
- AI analysis: 5-30 seconds (depends on size)
- Rule-based: < 5 seconds
- Excel generation: 2-10 seconds

### Resource Usage
- Memory: 1-2GB typical, 4GB max
- CPU: 1-2 cores typical
- Disk: 100MB for app, 1GB+ for data

## Security Architecture

### Input Validation
- File type restrictions
- Size limitations
- Content sanitization
- Encoding validation

### API Security
- Key management via environment
- No hardcoded credentials
- Rate limiting
- Request validation

### Data Protection
- No persistent storage of sensitive data
- Session isolation
- Sanitized outputs

## Monitoring & Observability

### Logging
- Rotating file logs
- Structured logging
- Multiple log levels
- Separate AI pipeline logger

### Metrics
- API call counts
- Processing times
- Error rates
- Cache hit rates

### Health Checks
- Streamlit health endpoint
- Docker health check
- Resource monitoring

## Future Architecture Considerations

### Potential Improvements
1. **Microservices Split**
   - Separate AI service
   - Independent export service
   - Dedicated API gateway

2. **Database Integration**
   - Result persistence
   - Historical analysis
   - User management

3. **Real-time Processing**
   - WebSocket support
   - Streaming analysis
   - Live dashboards

4. **Horizontal Scaling**
   - Load balancer
   - Multiple instances
   - Shared cache (Redis)

### Technical Debt
1. Port configuration scattered across files
2. Some duplicate analysis code remains
3. Testing coverage could be improved
4. Documentation needs continuous updates

## Conclusion

The current architecture is a **production-ready monolithic application** with strong AI integration, comprehensive error handling, and professional export capabilities. It's optimized for the current use case of batch comment analysis with modest concurrent usage.

The modular structure allows for future evolution toward microservices if scale demands increase, while maintaining simplicity and reliability for current operations.

---

**Document Version**: 1.0.0  
**Last Updated**: December 27, 2024  
**Status**: Current and Accurate