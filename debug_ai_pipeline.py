"""
Debug específico para el error de análisis IA
"""

import sys
import traceback
sys.path.append('src')

print('🔍 DEBUGGING AI PIPELINE ERROR:')
print('='*50)

try:
    # Test AIAnalysisAdapter import y inicialización
    print('1. Testing AIAnalysisAdapter import...')
    from src.ai_analysis_adapter import AIAnalysisAdapter
    print('   ✅ Import successful')
    
    print('2. Testing AIAnalysisAdapter initialization...')
    adapter = AIAnalysisAdapter()
    print(f'   ✅ Initialization successful - AI Available: {adapter.ai_available}')
    
    # Test mock file object (similar a uploaded_file de Streamlit)
    print('3. Creating mock uploaded file...')
    from io import BytesIO
    import pandas as pd
    
    # Crear CSV de prueba
    test_data = """Comentario Final
Excelente servicio, muy rápido y eficiente
El internet es muy lento, siempre se corta
Servicio regular, nada especial
"""
    
    class MockUploadedFile:
        def __init__(self, content, name):
            self.name = name
            self.size = len(content.encode('utf-8'))
            self._content = BytesIO(content.encode('utf-8'))
        
        def read(self):
            return self._content.read()
        
        def seek(self, offset):
            return self._content.seek(offset)
    
    mock_file = MockUploadedFile(test_data, "test.csv")
    print('   ✅ Mock file created')
    
    print('4. Testing AI analysis...')
    try:
        result = adapter.process_uploaded_file_with_ai(mock_file)
        
        if result:
            print('   ✅ AI analysis returned result')
            print(f'   📊 Analysis method: {result.get("analysis_method", "unknown")}')
            print(f'   📊 Total comments: {result.get("total", 0)}')
            print(f'   📊 Has emotions: {"emotion_summary" in result}')
            print(f'   📊 Has pain points: {"churn_analysis" in result}')
        else:
            print('   ❌ AI analysis returned None/empty result')
            
    except Exception as ai_error:
        print(f'   ❌ AI analysis failed with error: {str(ai_error)}')
        print('   📋 Full traceback:')
        traceback.print_exc()
        
except Exception as e:
    print(f'❌ Fatal error in debugging: {str(e)}')
    traceback.print_exc()

print('='*50)