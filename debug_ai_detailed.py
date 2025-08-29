"""
Debug detallado del AI pipeline
"""

import sys
import traceback
import streamlit as st
sys.path.append('src')

print('🔍 DEBUG DETALLADO DEL ERROR AI:')
print('='*60)

# Crear mock file object que replique exactamente el de Streamlit
import pandas as pd
from io import StringIO

# Test data real
test_csv = """Comentario Final
Excelente servicio, muy rápido y eficiente
El internet es muy lento, siempre se corta
Servicio regular, nada especial
Muy buena atención al cliente
"""

class StreamlitMockFile:
    """Mock que replica streamlit.UploadedFile"""
    def __init__(self, content, name):
        self.name = name
        self.size = len(content.encode('utf-8'))
        self._string_data = content
        
    def read(self):
        return self._string_data.encode('utf-8')
        
    def seek(self, offset):
        # Streamlit files don't reset, but we simulate it
        pass
        
    # Add iterator support for pandas
    def __iter__(self):
        return iter(self._string_data.splitlines())

try:
    print('1. Creating Streamlit-compatible mock file...')
    mock_file = StreamlitMockFile(test_csv, "test.csv")
    print(f'   ✅ Mock file: {mock_file.name}, size: {mock_file.size}')
    
    print('2. Testing pandas read directly...')
    # Test same logic as main.py
    string_io = StringIO(test_csv)
    df_test = pd.read_csv(string_io)
    print(f'   ✅ Pandas reads test data: {df_test.shape}')
    print(f'   📋 Columns: {list(df_test.columns)}')
    print(f'   📋 First comment: {df_test.iloc[0]["Comentario Final"]}')
    
    print('3. Testing AI Analysis Adapter...')
    from src.ai_analysis_adapter import AIAnalysisAdapter
    
    # Create adapter and test step by step
    adapter = AIAnalysisAdapter()
    print(f'   ✅ Adapter created - AI Available: {adapter.ai_available}')
    
    # Test the problematic function but step by step
    print('4. Testing file processing step by step...')
    
    # Simulate what the adapter should do
    try:
        # Use StringIO for pandas compatibility  
        string_io = StringIO(test_csv)
        df = pd.read_csv(string_io)
        print(f'   ✅ DataFrame created: {df.shape}')
        
        # Find comment column
        comment_cols = ['comentario final', 'comment', 'comments', 'feedback', 'review', 'texto']
        comment_col = None
        for col in df.columns:
            if any(name in col.lower() for name in comment_cols):
                comment_col = col
                break
        
        print(f'   ✅ Comment column found: {comment_col}')
        
        # Extract comments
        comments = df[comment_col].dropna().tolist()
        print(f'   ✅ Comments extracted: {len(comments)} comments')
        
        print('5. Testing OpenAI analysis...')
        if adapter.openai_analyzer and adapter.ai_available:
            # Try a single comment first
            test_comment = comments[0] if comments else "Test comment"
            print(f'   🧪 Testing with: "{test_comment[:50]}..."')
            
            # This would normally call the OpenAI API
            try:
                single_result = adapter.openai_analyzer.analyze_single_comment(test_comment)
                print(f'   ✅ Single comment analysis: {single_result}')
            except Exception as api_error:
                print(f'   ❌ OpenAI API Error: {str(api_error)}')
        else:
            print('   ❌ OpenAI analyzer not available')
            
    except Exception as step_error:
        print(f'   ❌ Step by step error: {str(step_error)}')
        traceback.print_exc()

except Exception as e:
    print(f'❌ Fatal debug error: {str(e)}')
    traceback.print_exc()

print('='*60)