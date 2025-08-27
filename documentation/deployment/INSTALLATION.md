# Installation Guide

## Quick Start

Follow these steps to properly install and run the Comment Analyzer application:

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Comment-Analizer
```

### 2. Create a Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install the Package in Development Mode
This is the **most important step** to ensure all imports work correctly:

```bash
pip install -e .
```

This command installs the package in "editable" mode, which means:
- All imports will work correctly without sys.path modifications
- Changes to the code are immediately reflected without reinstalling
- The package structure is properly recognized by Python

### 4. Install Additional Dependencies (if needed)
If the setup.py installation didn't capture all dependencies:

```bash
pip install -r requirements.txt
```

### 5. Set Up Environment Variables
Create a `.env` file in the project root:

```env
# Add your OpenAI API key if using OpenAI features
OPENAI_API_KEY=your_api_key_here

# Other configuration variables
DEBUG=False
```

## Running the Application

### Option 1: Using the run.py script
```bash
python run.py
```

### Option 2: Using Streamlit directly
```bash
streamlit run src/main.py
```

### Option 3: As a module (after installation)
```bash
python -m streamlit run src/main.py
```

## Running Tests

After proper installation, run tests with:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_data_processing.py
```

## Troubleshooting

### Import Errors
If you encounter import errors like `ModuleNotFoundError`:

1. **Ensure the package is installed**: Run `pip install -e .` from the project root
2. **Verify installation**: Run `pip list | grep comment-analyzer`
3. **Check Python path**: Run `python -c "import sys; print(sys.path)"`

### "No module named 'src'" Error
This means the package hasn't been properly installed. Solution:
```bash
pip install -e .
```

### Streamlit Not Found
Install Streamlit:
```bash
pip install streamlit
```

### Tests Failing Due to Imports
Make sure you've installed the package in development mode:
```bash
pip install -e .
```

## Development Workflow

1. **Make changes** to the source code
2. **No reinstallation needed** - changes are immediately available due to `-e` flag
3. **Run tests** to verify changes: `pytest`
4. **Run the app** to test functionality: `python run.py`

## Package Structure

After proper installation, the package structure allows imports like:

```python
# From anywhere in the project or external scripts
from src.services.session_manager import SessionManager
from src.components import EnhancedResultsUI
from src.sentiment_analysis.enhanced_analyzer import EnhancedAnalyzer
```

## Important Notes

- **Never modify sys.path** in production code
- Always use the package installation method (`pip install -e .`)
- Keep all imports consistent with the package structure
- Use relative imports only within the same package/module

## CI/CD Considerations

For deployment or CI/CD pipelines, use:

```bash
# Install in production mode (not editable)
pip install .

# Or install from git
pip install git+https://github.com/yourrepo/comment-analyzer.git
```

## Additional Resources

- [Python Packaging Guide](https://packaging.python.org/guides/distributing-packages-using-setuptools/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Pytest Documentation](https://docs.pytest.org/)