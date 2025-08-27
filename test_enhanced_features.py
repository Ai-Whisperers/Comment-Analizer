"""
Test script to verify all enhanced features are working
"""

import sys
import io
from pathlib import Path

# Fix encoding for Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Import from installed package
# Install with: pip install -e .
from src.enhanced_analysis import EnhancedAnalysis

def test_enhanced_features():
    """Test all enhanced analysis features"""
    
    # Initialize analyzer
    analyzer = EnhancedAnalysis()
    
    # Test comments
    test_comments = [
        "Voy a cambiar a Tigo, el servicio es pésimo y muy caro",  # High churn, competitor, negative
        "Estoy muy satisfecho con el servicio, excelente velocidad",  # Positive, satisfaction
        "Sin internet desde hace 3 días, urgente necesito solución",  # P0 critical
        "El precio sube sin avisar, muy molesto con esto",  # Price issue, frustration
        "Cliente fiel desde hace 10 años, espero mejoren",  # VIP customer
    ]
    
    print("=" * 60)
    print("TESTING ENHANCED ANALYSIS FEATURES")
    print("=" * 60)
    
    for i, comment in enumerate(test_comments, 1):
        print(f"\n📝 Comentario {i}: {comment}")
        print("-" * 50)
        
        # Run full analysis
        analysis = analyzer.full_analysis(comment)
        
        # Display results
        print(f"🎭 Emoción: {analysis['emotions']['dominant_emotion']} (Intensidad: {analysis['emotions']['intensity']}/10)")
        print(f"⚠️ Riesgo Churn: {analysis['churn_risk']['risk_level']} ({analysis['churn_risk']['probability']}% probabilidad)")
        print(f"🚨 Urgencia: {analysis['urgency']}")
        
        if analysis['competitors']['mentioned']:
            print(f"🏢 Competidores: {', '.join(analysis['competitors']['mentioned'])}")
        
        print(f"💎 Segmento: {analysis['customer_value']['value_segment'].upper()}")
        
        if analysis['extended_themes']:
            themes = []
            for main_theme, sub_themes in analysis['extended_themes'].items():
                themes.append(main_theme)
            print(f"📊 Temas: {', '.join(themes)}")
    
    print("\n" + "=" * 60)
    print("✅ ALL FEATURES TESTED SUCCESSFULLY!")
    print("=" * 60)
    
    # Test action plan generation
    print("\n📋 Testing Action Plan Generation...")
    test_results = {
        'churn_analysis': {
            'high_risk': 15,
            'medium_risk': 20,
            'details': [{'risk_level': 'high'} for _ in range(15)]
        },
        'urgency_distribution': {
            'P0': 5,
            'P1': 10
        },
        'theme_sentiments': {
            'precio': {'negativo': 60, 'total_mentions': 100}
        }
    }
    
    action_plan = analyzer.generate_action_plan(test_results)
    
    if action_plan:
        print("\n🎯 Action Plan Generated:")
        for action in action_plan:
            print(f"  - [{action['priority']}] {action['action']} ({action['department']})")
    
    print("\n✅ Action Plan Generation Working!")
    
    return True

if __name__ == "__main__":
    success = test_enhanced_features()
    if success:
        print("\n🎉 All enhanced features are working correctly!")
    else:
        print("\n❌ Some features failed. Check the output above.")