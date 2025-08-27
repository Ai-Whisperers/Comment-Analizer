# Personal Paraguay Fiber Comments Analysis System - User Guide

## Table of Contents
1. [Getting Started](#getting-started)
2. [System Requirements](#system-requirements)
3. [Installation & Setup](#installation--setup)
4. [Using the Application](#using-the-application)
5. [Features Overview](#features-overview)
6. [Troubleshooting](#troubleshooting)
7. [FAQ](#faq)

## Getting Started

The Personal Paraguay Fiber Comments Analysis System is an AI-powered tool designed to analyze customer feedback for Personal Paraguay's fiber-to-the-home services. It provides sentiment analysis, language detection (Spanish/Guarani), and business insights.

### Key Benefits
- **Automated Sentiment Analysis**: Classify comments as positive, negative, or neutral
- **Multilingual Support**: Handle Spanish and Guarani customer comments
- **Business Insights**: Identify key themes, pain points, and improvement opportunities
- **Export Capabilities**: Generate reports in Excel, CSV, PDF, and JSON formats
- **Batch Processing**: Analyze large datasets efficiently

## System Requirements

### Software Requirements
- **Python 3.8 or higher**
- **Internet connection** (for AI API access)
- **Web browser** (Chrome, Firefox, Safari, or Edge)

### Hardware Requirements
- **Minimum**: 4GB RAM, 1GB free disk space
- **Recommended**: 8GB RAM, 2GB free disk space

### API Requirements
- **OpenAI API key** (required for analysis)

## Installation & Setup

### Step 1: Download and Extract
1. Extract the project files to your desired location
2. Navigate to the project directory: `Personal_Paraguay_Fiber_Comments_Analysis/`

### Step 2: Install Dependencies
Open command prompt/terminal in the project directory and run:
```bash
pip install -r requirements.txt
```

### Step 3: Configure API Key
1. Copy `.env.example` to `.env`
2. Edit `.env` file and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

### Step 4: Test Installation
Run the test script to verify everything works:
```bash
python test_app.py
```

You should see all tests pass:
```
Configuration: PASS
Data Processing: PASS
AI Analysis: PASS
Streamlit App: PASS
Overall Status: ALL TESTS PASSED
```

### Step 5: Launch Application
Start the application with:
```bash
streamlit run src/main.py
```

The application will open in your web browser at `http://localhost:8501`

## Using the Application

### Navigation
The application has 4 main sections accessible from the sidebar:
- **📁 Data Upload**: Load and process comment data
- **📊 Analysis Dashboard**: Run AI analysis and view results
- **⚙️ Settings**: Configure API keys and settings
- **ℹ️ About**: System information and documentation

### Data Upload Process

#### Option 1: Upload New File
1. Go to **📁 Data Upload**
2. Click **"Choose a file"**
3. Select your file (Excel, CSV, JSON, or Text format)
4. The system will automatically:
   - Detect comment columns
   - Clean and standardize data
   - Show preview and statistics

#### Option 2: Load Existing Dataset
1. Go to **📁 Data Upload**
2. Click **"Load Personal Paraguay Dataset"**
3. This loads the pre-included customer comments dataset

#### Supported File Formats
- **Excel (.xlsx)**: Automatically detects comment columns
- **CSV (.csv)**: Handles various encodings
- **JSON (.json)**: Supports nested structures
- **Text (.txt)**: One comment per line

### Analysis Dashboard

#### Quick Analysis (Recommended for Testing)
1. Go to **📊 Analysis Dashboard**
2. Use the slider to select number of comments (1-200)
3. Click **🔍 Analyze Comments**
4. View results in real-time

#### Batch Processing (For Complete Analysis)
1. Select batch size (50, 100, or 200 comments per batch)
2. Click **🚀 Process All**
3. Monitor progress with the progress bar
4. Review cost estimate before proceeding

#### Understanding Results

**Sentiment Analysis**
- **Positive**: Customer satisfaction, praise, recommendations
- **Negative**: Complaints, problems, frustrations
- **Neutral**: Factual statements, neutral feedback

**Top Themes**
- Most frequently mentioned topics
- Business areas requiring attention
- Service aspects customers discuss most

**Pain Points**
- Specific problems customers experience
- Areas for immediate improvement
- Common complaint categories

**Language Distribution**
- Percentage of comments in Spanish vs Guarani
- Mixed language detection
- Translation quality metrics

### Export Options

#### Available Export Formats
1. **📊 Excel Workbook**: Complete analysis with multiple sheets
   - Analysis results
   - Summary statistics
   - Top themes and pain points
   - Recommendations

2. **📄 CSV Data**: Detailed results for further analysis
   - All comments with analysis results
   - Import into other tools

3. **📝 Summary Report**: Executive summary in text format
   - Key findings
   - Business recommendations
   - Printable format

4. **🔧 JSON Data**: Machine-readable format
   - API integration
   - Further processing
   - Data interchange

#### How to Export
1. Complete analysis first
2. Scroll to **📥 Export Results** section
3. Click desired export button
4. Download files from **📂 Download Files** section

## Features Overview

### AI-Powered Analysis
- **OpenAI GPT-4**: Advanced language understanding
- **Sentiment Detection**: Emotion and opinion analysis
- **Theme Extraction**: Automatic topic identification
- **Translation**: Guarani to Spanish conversion

### Data Processing
- **Multi-format Support**: Excel, CSV, JSON, Text
- **Automatic Cleaning**: Remove duplicates, normalize text
- **Language Detection**: Identify Spanish, Guarani, or mixed content
- **Quality Validation**: Ensure data integrity

### Visualization & Reporting
- **Interactive Charts**: Real-time data visualization
- **Progress Tracking**: Monitor batch processing
- **Export Integration**: Multiple output formats
- **Business Intelligence**: Actionable insights

### Performance Features
- **Batch Processing**: Handle large datasets
- **Progress Indicators**: Real-time status updates
- **Cost Estimation**: API usage transparency
- **Error Handling**: Graceful failure recovery

## Troubleshooting

### Common Issues

#### "Configuration Error: Missing API Key"
**Solution**: 
1. Verify `.env` file exists in project root
2. Check OpenAI API key is correctly set
3. Restart the application

#### "Import Error" or "Module Not Found"
**Solution**:
1. Ensure you're in the correct project directory
2. Reinstall dependencies: `pip install -r requirements.txt`
3. Check Python version (3.8+ required)

#### "File Upload Failed"
**Solution**:
1. Check file format is supported (.xlsx, .csv, .json, .txt)
2. Ensure file contains text data
3. Try with a smaller file first

#### "Analysis Failed" or API Errors
**Solution**:
1. Check internet connection
2. Verify OpenAI API key is valid and has credits
3. Try with fewer comments first
4. Check API rate limits

#### Application Won't Start
**Solution**:
1. Check port 8501 is not in use
2. Try: `streamlit run src/main.py --server.port 8502`
3. Clear browser cache
4. Try different browser

### Performance Optimization

#### For Large Datasets
- Use batch processing instead of analyzing all at once
- Process in smaller batches (50-100 comments)
- Monitor API costs with provided estimates
- Export results frequently to avoid data loss

#### For Better Results
- Clean data before upload (remove empty rows)
- Use consistent language (Spanish preferred)
- Remove personal information before analysis
- Validate file format before upload

## FAQ

### General Questions

**Q: How accurate is the sentiment analysis?**
A: The system achieves 90%+ accuracy for Spanish text using OpenAI's advanced models. Accuracy may vary for mixed languages or informal text.

**Q: What languages are supported?**
A: Primary support for Spanish (Paraguayan dialect) and Guarani. Mixed language comments are automatically detected and translated.

**Q: How much does it cost to run analysis?**
A: Costs depend on the number of comments analyzed. Approximately $0.002 per comment. The system provides cost estimates before processing.

**Q: Can I analyze non-telecommunications comments?**
A: Yes, the system works for any customer feedback. It's optimized for telecommunications but handles general customer comments well.

### Technical Questions

**Q: What file formats are supported?**
A: Excel (.xlsx), CSV (.csv), JSON (.json), and plain text (.txt) files.

**Q: Is my data secure?**
A: Comments are processed through OpenAI's API with standard security measures. No data is permanently stored by the system.

**Q: Can I run this offline?**
A: No, internet connection is required for AI analysis. Data processing and visualization work offline.

**Q: How do I get an OpenAI API key?**
A: Visit https://platform.openai.com/, create an account, and generate an API key from the dashboard.

### Business Questions

**Q: What insights can I expect?**
A: The system identifies sentiment trends, common themes, pain points, language preferences, and provides actionable business recommendations.

**Q: How do I interpret the results?**
A: Focus on sentiment percentages, top pain points, and AI recommendations. Export the summary report for executive sharing.

**Q: Can I schedule automatic analysis?**
A: Currently manual operation only. Future versions may include automation features.

**Q: How often should I analyze comments?**
A: Recommended weekly or monthly analysis for trend monitoring. Daily analysis for high-volume periods.

## Support

For technical support or questions:
1. Check this user guide first
2. Run the test script to identify issues
3. Review error messages carefully
4. Consult the troubleshooting section

## System Information

- **Version**: 1.0
- **Technology**: Python, Streamlit, OpenAI GPT-4
- **License**: Internal use for Personal Paraguay
- **Last Updated**: January 26, 2025

---

*This system was developed specifically for Personal Paraguay's customer feedback analysis needs. For updates or modifications, contact the development team.*