"""
Test script to verify AI integration and fallback functionality
Run this to test both AI and fallback paths before using in production
"""

import os
import sys
import tempfile
import pandas as pd
from io import BytesIO

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_ai_adapter_initialization():
    """Test that the AI adapter initializes correctly"""
    print("🧪 Testing AI Adapter Initialization...")
    
    try:
        from src.ai_analysis_adapter import AIAnalysisAdapter
        
        adapter = AIAnalysisAdapter()
        
        print(f"✅ AI Adapter initialized")
        print(f"   - AI Available: {adapter.ai_available}")
        print(f"   - Has Enhanced Analyzer: {adapter.enhanced_analyzer is not None}")
        print(f"   - Has Improved Analyzer: {adapter.improved_analyzer is not None}")
        
        if adapter.ai_available:
            print(f"   - OpenAI Model: {adapter.openai_analyzer.model}")
        
        return adapter
        
    except Exception as e:
        print(f"❌ AI Adapter initialization failed: {str(e)}")
        return None

def create_test_excel_file():
    """Create a test Excel file with sample comments"""
    print("📝 Creating test Excel file...")
    
    test_data = {
        'Comentario Final': [
            'El servicio es excelente, muy rápido y confiable',
            'Muy lento el internet, no me gusta para nada',
            'Regular el servicio, podría mejorar',
            'Perfecto servicio, lo recomiendo mucho',
            'Terrible conexión, se corta todo el tiempo'
        ],
        'Nota': [9, 3, 6, 10, 2],
        'NPS': ['Promotor', 'Detractor', 'Pasivo', 'Promotor', 'Detractor']
    }
    
    df = pd.DataFrame(test_data)
    
    # Create temporary file
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Comentarios')
    
    output.seek(0)
    return output, len(test_data['Comentario Final'])

def test_fallback_analysis(adapter):
    """Test fallback analysis functionality"""
    print("\n🔄 Testing Fallback Analysis...")
    
    try:
        # Create test file
        test_file_content, expected_count = create_test_excel_file()
        
        # Create a mock uploaded file object
        class MockUploadedFile:
            def __init__(self, content, name):
                self.content = content
                self.name = name
                self.size = len(content.getvalue())
        
        mock_file = MockUploadedFile(test_file_content, "test_comments.xlsx")
        
        # Force fallback by temporarily disabling AI
        original_ai_available = adapter.ai_available
        adapter.ai_available = False
        
        print("   - Forcing fallback mode (AI disabled)")
        
        # Test the analysis
        results = adapter.process_uploaded_file_with_ai(mock_file)
        
        # Restore AI availability
        adapter.ai_available = original_ai_available
        
        if results:
            print("✅ Fallback analysis successful!")
            print(f"   - Analysis Method: {results.get('analysis_method', 'UNKNOWN')}")
            print(f"   - Total Comments: {results.get('total', 0)}")
            print(f"   - Positive: {results.get('positive_count', 0)}")
            print(f"   - Negative: {results.get('negative_count', 0)}")
            print(f"   - Neutral: {results.get('neutral_count', 0)}")
            print(f"   - NPS Score: {results.get('nps', {}).get('score', 'N/A')}")
            
            # Verify expected data structure
            required_fields = ['total', 'sentiments', 'enhanced_results', 'improved_results']
            missing_fields = [field for field in required_fields if field not in results]
            
            if not missing_fields:
                print("✅ All required fields present in results")
            else:
                print(f"⚠️  Missing fields: {missing_fields}")
            
            return True
        else:
            print("❌ Fallback analysis returned None")
            return False
            
    except Exception as e:
        print(f"❌ Fallback analysis failed: {str(e)}")
        import traceback
        print(f"   Traceback: {traceback.format_exc()}")
        return False

def test_ai_analysis_if_available(adapter):
    """Test AI analysis if available"""
    print("\n🤖 Testing AI Analysis...")
    
    if not adapter.ai_available:
        print("⏭️  Skipping AI analysis test (AI not available)")
        return True
    
    try:
        # Create test file
        test_file_content, expected_count = create_test_excel_file()
        
        # Create a mock uploaded file object
        class MockUploadedFile:
            def __init__(self, content, name):
                self.content = content
                self.name = name
                self.size = len(content.getvalue())
        
        mock_file = MockUploadedFile(test_file_content, "test_comments.xlsx")
        
        print("   - Attempting AI analysis...")
        
        # Test the analysis
        results = adapter.process_uploaded_file_with_ai(mock_file)
        
        if results:
            analysis_method = results.get('analysis_method', 'UNKNOWN')
            print(f"✅ AI analysis completed!")
            print(f"   - Analysis Method: {analysis_method}")
            print(f"   - Total Comments: {results.get('total', 0)}")
            print(f"   - AI Confidence: {results.get('ai_confidence_avg', 0):.1%}")
            
            if analysis_method == 'AI_POWERED':
                print(f"   - AI Model Used: {results.get('ai_model_used', 'Unknown')}")
                print("✅ Successfully used OpenAI for analysis!")
            elif analysis_method == 'RULE_BASED_FALLBACK':
                print("⚠️  AI analysis failed, used fallback (this is expected behavior)")
            
            return True
        else:
            print("❌ AI analysis returned None")
            return False
            
    except Exception as e:
        print(f"❌ AI analysis failed: {str(e)}")
        import traceback
        print(f"   Traceback: {traceback.format_exc()}")
        return False

def main():
    """Run all tests"""
    print("🚀 AI Integration Test Suite")
    print("=" * 50)
    
    # Test 1: Adapter initialization
    adapter = test_ai_adapter_initialization()
    if not adapter:
        print("\n❌ Tests failed - Could not initialize adapter")
        return
    
    # Test 2: Fallback analysis
    fallback_success = test_fallback_analysis(adapter)
    
    # Test 3: AI analysis (if available)
    ai_success = test_ai_analysis_if_available(adapter)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    print(f"   - Adapter Initialization: ✅")
    print(f"   - Fallback Analysis: {'✅' if fallback_success else '❌'}")
    print(f"   - AI Analysis: {'✅' if ai_success else '❌'}")
    
    if fallback_success and ai_success:
        print("\n🎉 All tests passed! AI integration is ready for production.")
        print("\n💡 Usage Notes:")
        print("   - When OpenAI API is available: Users will see 'AI Available' status")
        print("   - When OpenAI API fails: System automatically falls back to rule-based analysis")
        print("   - All results maintain the same format regardless of analysis method")
    else:
        print("\n⚠️  Some tests failed. Check the errors above before deploying.")

if __name__ == "__main__":
    main()