# Comment Analyzer - Customer Feedback Analysis System

A sophisticated multilingual sentiment analysis and pattern detection system designed for analyzing customer comments about fiber-to-the-home services. Built specifically for Personal Paraguay (Núcleo S.A.) to provide actionable business intelligence from customer feedback.

## 📚 Documentation

For comprehensive documentation, guides, and technical specifications, visit the **[Documentation Center](./documentation/README.md)**.

## 🚀 Current Features

### Core Capabilities
- **Multilingual Support**: Full support for Spanish (Paraguayan dialect) with automatic text correction
- **Advanced Sentiment Analysis**: AI-powered emotion detection and sentiment scoring using OpenAI GPT-4
- **Pattern Recognition**: Automatic theme identification and trend analysis for telecommunications issues
- **Interactive Dashboard**: Real-time visualization with Streamlit interface
- **Professional Reporting**: Multi-sheet Excel exports with detailed analytics and visualizations

### Technical Features
- **API Integration**: OpenAI GPT-4 integration for sentiment analysis and pattern detection
- **Performance Optimization**: Intelligent caching, batch processing, memory management
- **Cost Control**: Built-in API usage monitoring and optimization
- **Responsive Design**: Mobile-friendly Streamlit interface with professional dark theme
- **Security**: Input validation, secure API handling, environment-based configuration

## 📁 Project Structure

```
Comment-Analyzer/
├── src/                          # Source code
│   ├── analysis_service/        # Core analysis logic
│   ├── api/                     # API clients and monitoring
│   ├── components/              # UI components
│   ├── data_processing/         # Data ingestion and cleaning
│   ├── sentiment_analysis/      # Sentiment detection modules
│   ├── pattern_detection/       # Theme and pattern analysis
│   ├── services/                # Business logic services
│   ├── theme/                   # UI theming and styles
│   ├── utils/                   # Utility functions
│   └── visualization/           # Charts and exports
├── data/                        # Data storage
│   ├── raw/                     # Original datasets
│   ├── cache/                   # API response cache
│   └── monitoring/              # Usage metrics
├── outputs/                     # Generated results
│   ├── reports/                 # Analysis reports
│   ├── exports/                 # Excel/CSV exports
│   └── visualizations/          # Generated charts
├── tests/                       # Test suite
└── documentation/               # User guides and docs
```

## 🛠️ Technology Stack

### Core Technologies
- **Framework**: Python 3.8+ with Streamlit web application framework
- **Data Processing**: Pandas, NumPy for data manipulation and analysis
- **Visualization**: Plotly for interactive charts and graphs
- **UI/UX**: Custom CSS with professional dark theme, responsive design

### AI/ML Integration
- **Primary API**: OpenAI GPT-4 for sentiment analysis and pattern detection
- **Text Processing**: Custom Spanish language processing with orthographic correction
- **Analysis Engine**: Multi-layer sentiment analysis with emotion detection

### Data Export & Processing
- **Excel Export**: XlsxWriter for professional multi-sheet reports
- **File Processing**: openpyxl for Excel file reading and validation
- **Report Generation**: Custom professional Excel exporter with charts and summaries

### Development & Testing
- **Testing Framework**: Pytest for unit and integration tests
- **Environment Management**: python-dotenv for configuration management
- **Code Quality**: Built-in logging and error handling

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/aiwhispererwvdp/Comment-Analizer.git
   cd Comment-Analizer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   Create a `.env` file with your API credentials:
   ```env
   # Required: OpenAI API key for sentiment analysis
   OPENAI_API_KEY=your_openai_key_here
   
   # Optional: Configuration settings
   OPENAI_MODEL=gpt-4
   OPENAI_MAX_TOKENS=4000
   OPENAI_TEMPERATURE=0.7
   LOG_LEVEL=INFO
   ```

## 🚀 Usage

### Quick Start
```bash
# Start the application
streamlit run src/main.py

# Alternative: using the run script
python run.py
```

### Using the Application
1. **Navigate to** http://localhost:8501 in your web browser
2. **Upload Excel file** with customer comments using the file uploader
3. **Click "🚀 Análisis Rápido"** to process the comments
4. **View results** in the interactive dashboard with sentiment analysis and metrics
5. **Download reports** using the professional Excel export button

### Supported File Formats
- **Excel files** (.xlsx, .xls) with customer comment data
- **CSV files** with comment columns
- **Required column**: Comment text (automatically detected as "Comentario Final" or similar)
- **Optional columns**: "Nota" (ratings), "NPS" (categories), date fields

## 📊 Input Data Format

The system expects Excel files with the following structure:
- **Comment Column**: Text feedback from customers
- **Date Column** (optional): Timestamp of feedback
- **Category Column** (optional): Pre-existing categories
- **Rating Column** (optional): Numerical ratings

## 📈 Output Capabilities

### Analysis Results
- Sentiment scores and classifications
- Emotion detection (joy, anger, sadness, fear, surprise)
- Key themes and patterns
- Trend analysis over time
- Customer satisfaction metrics

### Export Formats
- **Professional Excel Report**: Comprehensive workbook with 15+ sheets including:
  - Executive summary with key metrics
  - Sentiment analysis results with confidence scores
  - Detailed comment-by-comment analysis
  - Theme detection and pattern analysis
  - NPS calculations and customer segmentation
  - Advanced analytics (churn risk, emotion analysis)
  - Data quality and cleaning statistics
  - Actionable recommendations and insights

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run specific test module
pytest tests/test_file_upload_service.py

# Run with coverage
pytest --cov=src tests/
```

## 📖 Documentation

### Current Implementation Guides
- [Installation Guide](INSTALLATION.md) - Complete setup and installation instructions
- [Docker Deployment](DOCKER_DEPLOYMENT.md) - Containerization and deployment guide
- [Architecture Analysis](ARCHITECTURAL_ANALYSIS_REPORT.md) - Detailed technical analysis

### Development & Analysis Reports
- [Domain Logic Analysis](DOMAIN_LOGIC_ANALYSIS_REPORT.md) - Code quality and improvement recommendations
- [Critical Fixes Quickstart](CRITICAL_FIXES_QUICKSTART.md) - Priority bug fixes and patches

### Future Roadmap & Advanced Features
- [Future Roadmap](#-future-roadmap--advanced-features) - Planned enhancements and architectural improvements
- [Hexagonal Architecture Plan](HEXAGONAL_IMPLEMENTATION_PLAN.md) - Detailed refactoring strategy for improved maintainability

## 🔒 Security & Privacy

- All data processing is performed locally
- API calls use encrypted connections
- No customer data is stored permanently
- Configurable data retention policies
- Input validation and sanitization

## 🎯 Use Cases

- **Customer Service**: Identify common complaints and issues
- **Product Development**: Understand feature requests and needs
- **Marketing**: Gauge campaign effectiveness and brand sentiment
- **Quality Assurance**: Track service quality trends
- **Business Intelligence**: Data-driven decision making

## 📝 License

Proprietary - Personal Paraguay (Núcleo S.A.)

## 🤝 Support

For support, feature requests, or bug reports, please contact the development team or create an issue in this repository.

## 🏗️ Development Status

**Version**: 1.0.0  
**Status**: Production Ready  
**Last Updated**: July 2025

---

## 🚀 Future Roadmap & Advanced Features

This section outlines planned enhancements and architectural improvements identified through comprehensive code analysis and business requirements.

### 🏗️ Phase 1: Architecture & Code Quality (Priority: High)

#### Hexagonal Architecture Refactoring
- **Domain-Driven Design**: Implement clean separation between business logic and infrastructure
- **Port-Adapter Pattern**: Create interfaces for external dependencies (APIs, file systems, databases)
- **Improved Testability**: Enable unit testing of business logic in isolation
- **Framework Independence**: Reduce coupling to Streamlit for easier future migrations

#### Critical Code Quality Fixes
- **Error Handling**: Replace all `except: pass` statements with proper error logging and recovery
- **Input Validation**: Add comprehensive validation for all user inputs and API calls
- **State Management**: Fix unsafe session state access patterns in Streamlit
- **Import Cleanup**: Remove 22+ unused imports identified in codebase analysis
- **Global State Elimination**: Refactor global variables to proper dependency injection

### 🔌 Phase 2: API Integration Expansion (Priority: Medium)

#### Additional AI/ML Services
- **Azure Text Analytics**: Multi-language sentiment analysis with confidence scores
- **Google Cloud Translation**: Real-time translation for Guaraní and other regional languages
- **Amazon Comprehend**: Enhanced entity recognition and key phrase extraction
- **Hybrid Analysis**: Combine multiple AI services for improved accuracy

#### Performance & Cost Optimization
- **Smart Caching**: Multi-layer caching for API responses and analysis results
- **Batch Processing**: Optimize API calls with intelligent batching strategies
- **Circuit Breaker Pattern**: Implement resilience patterns for external API failures
- **Cost Monitoring**: Real-time API usage tracking and budget alerts

### 📱 Phase 3: Frontend Enhancement Options (Priority: Low)

#### React Migration Path (Optional)
If business requirements demand a full web application:
- **FastAPI Backend**: RESTful API with proper OpenAPI documentation
- **React Frontend**: Modern TypeScript-based UI with component libraries
- **Authentication**: JWT-based authentication with role-based access control
- **Real-time Updates**: WebSocket integration for live analysis updates

#### Streamlit Advanced Features
Alternative enhancement within current architecture:
- **Multi-page Applications**: Organized navigation for different analysis views
- **Custom Components**: Build specialized UI components for complex visualizations
- **Authentication Integration**: Add user management and access control
- **Mobile Optimization**: Enhanced responsive design for mobile devices

### 📊 Phase 4: Advanced Analytics Features (Priority: High)

#### Customer Intelligence
- **Churn Risk Scoring**: ML models to identify customers likely to cancel
- **Customer Lifetime Value**: Predictive analytics for customer value assessment
- **Sentiment Trends**: Time-series analysis of sentiment changes
- **Competitive Analysis**: Automated detection of competitor mentions and context

#### Business Intelligence Dashboard
- **Executive Dashboards**: High-level KPIs for management reporting
- **Drill-down Analysis**: Interactive exploration of sentiment patterns
- **Predictive Analytics**: Forecasting models for customer satisfaction trends
- **Alerting System**: Automated alerts for significant sentiment changes

### 🔧 Phase 5: Infrastructure & DevOps (Priority: Medium)

#### Docker & Containerization
- **Multi-stage Builds**: Optimized container images for different environments
- **Health Checks**: Comprehensive monitoring and alerting
- **Auto-scaling**: Kubernetes deployment with horizontal pod autoscaling
- **Secret Management**: Secure handling of API keys and sensitive configuration

#### Database Integration
- **PostgreSQL**: Persistent storage for analysis history and user data
- **Time-series Database**: Specialized storage for trend analysis
- **Data Warehouse**: Integration with business intelligence platforms
- **Backup & Recovery**: Automated data protection strategies

### 📈 Phase 6: Enterprise Features (Priority: Medium)

#### Security & Compliance
- **Audit Logging**: Comprehensive tracking of all user actions and system events
- **Data Encryption**: End-to-end encryption for sensitive customer data
- **GDPR Compliance**: Data privacy controls and customer data management
- **Role-based Access**: Granular permissions for different user types

#### Integration & APIs
- **REST API**: Programmatic access for other business systems
- **Webhook Integration**: Real-time notifications to external systems
- **CRM Integration**: Seamless connection with customer relationship management systems
- **Business Intelligence**: Integration with PowerBI, Tableau, or similar platforms

### 🔍 Phase 7: Advanced Text Analysis (Priority: High)

#### Natural Language Processing
- **Named Entity Recognition**: Automatic identification of products, services, and issues
- **Topic Modeling**: Unsupervised discovery of themes in customer feedback
- **Aspect-based Sentiment**: Granular sentiment analysis for specific product features
- **Emotion Detection**: Advanced emotional intelligence beyond basic sentiment

#### Multilingual Enhancements
- **Guaraní Language Support**: Native processing for Paraguay's indigenous language
- **Regional Dialects**: Specialized handling of regional Spanish variations
- **Code-switching Detection**: Analysis of mixed-language communications
- **Cultural Context**: Culturally-aware sentiment interpretation

### 📋 Implementation Priorities

#### Immediate (Next Sprint)
1. Fix critical error handling issues (9 locations identified)
2. Add input validation to prevent runtime errors
3. Clean up unused imports and improve code quality
4. Implement proper session state management

#### Short-term (Next Month)
1. Begin hexagonal architecture refactoring
2. Enhance professional Excel export with more advanced analytics
3. Implement comprehensive logging and monitoring
4. Add basic API integration for additional services

#### Medium-term (Next Quarter)
1. Complete architecture refactoring
2. Add advanced analytics features (churn scoring, customer segmentation)
3. Implement Docker deployment with proper CI/CD
4. Enhance multilingual support with additional AI services

#### Long-term (Next 6 Months)
1. Consider React migration if business requirements demand it
2. Add enterprise security and compliance features
3. Implement real-time analytics and dashboard
4. Create API ecosystem for third-party integrations

### 💡 Innovation Opportunities

#### Emerging Technologies
- **Large Language Models**: Integration with latest models for improved analysis
- **Edge Computing**: Local processing for sensitive data privacy
- **Automated Insights**: AI-generated business recommendations and action items
- **Voice Analytics**: Extension to analyze customer call recordings

#### Business Value Expansion
- **Competitive Intelligence**: Market analysis through social media and review platforms
- **Customer Journey Mapping**: End-to-end analysis of customer experience touchpoints
- **Predictive Maintenance**: Proactive identification of service quality issues
- **Revenue Optimization**: Price sensitivity analysis from customer feedback

### 📚 Resources & References

- [Hexagonal Architecture Implementation Plan](HEXAGONAL_IMPLEMENTATION_PLAN.md) - Detailed technical roadmap
- [Domain Logic Analysis Report](DOMAIN_LOGIC_ANALYSIS_REPORT.md) - Code quality improvements
- [Docker Deployment Guide](DOCKER_DEPLOYMENT.md) - Infrastructure setup
- [Architectural Analysis Report](ARCHITECTURAL_ANALYSIS_REPORT.md) - Current state assessment

---

**Note**: This roadmap is based on comprehensive analysis of the current codebase and business requirements. Implementation priorities can be adjusted based on changing business needs and resource availability.

---

Built with ❤️ for Personal Paraguay to enhance customer experience through data-driven insights.