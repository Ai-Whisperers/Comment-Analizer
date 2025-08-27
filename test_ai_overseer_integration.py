"""
Test script to verify AI Overseer integration
"""

import sys
sys.path.insert(0, '.')

from src.ai_overseer import apply_ai_oversight
import pandas as pd

def test_overseer():
    print("=" * 60)
    print("PRUEBA DE INTEGRACIÓN - SUPERVISOR IA")
    print("=" * 60)
    
    # Create realistic test data
    test_results = {
        'total': 25,
        'positive_count': 10,
        'neutral_count': 8,
        'negative_count': 7,
        'positive_pct': 40.0,
        'neutral_pct': 32.0,
        'negative_pct': 28.0,
        'comments': [
            "Excelente servicio, muy rápido",
            "Pésimo, no funciona nada",
            "Regular, podría mejorar", 
            "Internet muy lento",
            "Buena atención al cliente",
            "Se corta constantemente",
            "Precio muy caro para el servicio",
            "Funciona bien",
            "No recomiendo para nada",
            "Estoy satisfecho"
        ],
        'sentiments': [
            "positivo", "negativo", "neutral", "negativo", "positivo",
            "negativo", "negativo", "positivo", "negativo", "positivo"
        ],
        'theme_counts': {
            'velocidad': 5,
            'interrupciones': 3,
            'servicio': 4,
            'precio': 2,
            'cobertura': 1
        },
        'theme_examples': {
            'velocidad': ["Internet muy lento", "muy rápido"],
            'interrupciones': ["Se corta constantemente"]
        },
        'analysis_date': '2025-08-27 11:45:00',
        'original_filename': 'test_comments.xlsx',
        'file_size': 12.5,
        'avg_length': 45,
        'raw_total': 30,
        'duplicates_removed': 5,
        'analysis_method': 'SIMPLE_RULE_BASED'
    }
    
    print("\n📊 Datos de prueba:")
    print(f"  - Total comentarios: {test_results['total']}")
    print(f"  - Positivos: {test_results['positive_pct']}%")
    print(f"  - Neutrales: {test_results['neutral_pct']}%")
    print(f"  - Negativos: {test_results['negative_pct']}%")
    
    print("\n🔄 Aplicando Supervisión IA...")
    
    try:
        # Apply AI oversight
        enhanced = apply_ai_oversight(test_results, strict=False, language='es')
        
        print("✅ Supervisión completada exitosamente\n")
        
        # Check validation data
        if 'overseer_validation' in enhanced:
            validation = enhanced['overseer_validation']
            print("📈 Métricas de Validación:")
            print(f"  - Validado: {validation.get('validated', False)}")
            print(f"  - Confianza: {validation.get('confidence', 0):.1%}")
            print(f"  - Calidad: {validation.get('quality_score', 0):.1%}")
            print(f"  - Mejorado con IA: {validation.get('ai_enhanced', False)}")
        
        # Display report
        if 'oversight_report' in enhanced:
            print("\n" + "=" * 60)
            print("REPORTE COMPLETO:")
            print("=" * 60)
            print(enhanced['oversight_report'])
        
        # Check AI insights
        if 'ai_insights' in enhanced:
            print("\n🤖 Insights de IA:")
            for insight in enhanced['ai_insights']:
                print(f"  - {insight}")
        
        print("\n✅ PRUEBA EXITOSA - El sistema está funcionando correctamente")
        
    except Exception as e:
        print(f"\n❌ ERROR en la prueba: {e}")
        import traceback
        traceback.print_exc()
        
        print("\n⚠️ Verificar:")
        print("  1. ¿Está configurada la API key de OpenAI?")
        print("  2. ¿Están instaladas todas las dependencias?")
        print("  3. ¿Hay conexión a internet?")

if __name__ == "__main__":
    test_overseer()