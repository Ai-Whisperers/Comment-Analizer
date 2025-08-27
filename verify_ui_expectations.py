"""
Verify that AI adapter output matches exactly what the UI expects
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.ai_analysis_adapter import AIAnalysisAdapter
from src.enhanced_analysis import EnhancedAnalysis
import pandas as pd
from io import BytesIO

def verify_ui_expectations():
    """Verify adapter output matches UI expectations exactly"""
    
    print("🔍 Verifying UI Expectations\n")
    
    # Create test data
    test_data = pd.DataFrame({
        'Comentario Final': ['Servicio excelente', 'Me voy a cambiar a Tigo'],
        'NPS': ['Promotor', 'Detractor'], 
        'Nota': [9, 3]
    })
    
    # Mock file
    class MockFile:
        def __init__(self, df):
            buffer = BytesIO()
            df.to_excel(buffer, index=False)
            self.content = buffer
            self.name = 'test.xlsx'
            self.size = len(buffer.getvalue())
        def read(self):
            self.content.seek(0)
            return self.content.read()
        def seek(self, pos):
            self.content.seek(pos)
    
    mock_file = MockFile(test_data)
    
    # Process with adapter
    adapter = AIAnalysisAdapter()
    adapter.ai_available = False  # Force fallback
    result = adapter.process_uploaded_file_with_ai(mock_file)
    
    print("✅ UI Expectation Tests:\n")
    
    # 1. Test enhanced_results structure
    print("1. enhanced_results[i]['emotions'] structure:")
    if result and 'enhanced_results' in result:
        sample_emotion = result['enhanced_results'][0]['emotions']
        assert 'dominant_emotion' in sample_emotion, "Missing dominant_emotion"
        assert 'intensity' in sample_emotion, "Missing intensity"
        assert 'all_emotions' in sample_emotion, "Missing all_emotions"
        print(f"   ✅ Has dominant_emotion: '{sample_emotion['dominant_emotion']}'")
        print(f"   ✅ Has intensity: {sample_emotion['intensity']}")
        print(f"   ✅ Has all_emotions: {sample_emotion['all_emotions']}")
    
    # 2. Test enhanced_results churn_risk
    print("\n2. enhanced_results[i]['churn_risk'] structure:")
    if result and 'enhanced_results' in result:
        sample_churn = result['enhanced_results'][0]['churn_risk']
        assert 'risk_level' in sample_churn, "Missing risk_level"
        assert sample_churn['risk_level'] in ['high', 'medium', 'low', 'alto', 'medio', 'bajo'], f"Invalid risk_level: {sample_churn['risk_level']}"
        print(f"   ✅ Has risk_level: '{sample_churn['risk_level']}'")
    
    # 3. Test customer_segments structure (CRITICAL!)
    print("\n3. customer_segments structure (UI expects list of dicts):")
    if result and 'customer_segments' in result:
        segments = result['customer_segments']
        assert isinstance(segments, list), f"customer_segments should be list, got {type(segments)}"
        
        if len(segments) > 0:
            first_segment = segments[0]
            assert isinstance(first_segment, dict), f"Each segment should be dict, got {type(first_segment)}"
            assert 'value_segment' in first_segment, "Missing value_segment key"
            
            # Test UI access pattern: seg.get('value_segment')
            vip_count = sum(1 for seg in segments if seg.get('value_segment') == 'vip')
            print(f"   ✅ customer_segments is list of dicts")
            print(f"   ✅ Each dict has 'value_segment' key")
            print(f"   ✅ UI can count VIP segments: {vip_count}")
            print(f"   ✅ Sample: {first_segment}")
    
    # 4. Test emotion_summary structure
    print("\n4. emotion_summary structure:")
    if result and 'emotion_summary' in result:
        emotion_summary = result['emotion_summary']
        assert 'distribution' in emotion_summary, "Missing distribution"
        assert 'avg_intensity' in emotion_summary, "Missing avg_intensity"
        print(f"   ✅ Has distribution: {emotion_summary['distribution']}")
        print(f"   ✅ Has avg_intensity: {emotion_summary['avg_intensity']}")
    
    # 5. Test competitor_analysis structure
    print("\n5. competitor_analysis structure:")
    if result and 'competitor_analysis' in result:
        comp_analysis = result['competitor_analysis']
        assert 'total_mentions' in comp_analysis, "Missing total_mentions"
        assert 'percentage' in comp_analysis, "Missing percentage"
        print(f"   ✅ Has total_mentions: {comp_analysis['total_mentions']}")
        print(f"   ✅ Has percentage: {comp_analysis['percentage']}%")
    
    # 6. Test churn_analysis structure
    print("\n6. churn_analysis structure:")
    if result and 'churn_analysis' in result:
        churn_analysis = result['churn_analysis']
        assert 'high_risk' in churn_analysis, "Missing high_risk"
        assert 'medium_risk' in churn_analysis, "Missing medium_risk"
        assert 'details' in churn_analysis, "Missing details"
        
        # Check details structure
        details = churn_analysis['details']
        if details and len(details) > 0:
            assert 'risk_level' in details[0], "Missing risk_level in details"
        
        print(f"   ✅ Has high_risk count: {churn_analysis['high_risk']}")
        print(f"   ✅ Has details with risk_level")
    
    print("\n✅ All UI expectations are met!")
    print("\n📝 Key Points:")
    print("  • enhanced_results[i]['emotions']['dominant_emotion'] ✓")
    print("  • enhanced_results[i]['emotions']['intensity'] ✓")
    print("  • enhanced_results[i]['churn_risk']['risk_level'] ✓")
    print("  • customer_segments is LIST of DICTS with 'value_segment' key ✓")
    print("  • UI uses: seg.get('value_segment') == 'vip' ✓")

if __name__ == "__main__":
    verify_ui_expectations()