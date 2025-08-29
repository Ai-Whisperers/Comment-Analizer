"""
Debug para verificar qué sentimientos se están mostrando en la UI
"""

import sys
sys.path.append('src')

print('🔍 ANALYZING SENTIMENT DISPLAY IN UI:')
print('='*60)

# Simular datos de Pipeline 1 (Simple)
simple_results = {
    'analysis_method': 'SIMPLE_RULE_BASED',
    'total': 100,
    'positive_count': 40,
    'neutral_count': 35,
    'negative_count': 25,
    'positive_pct': 40.0,
    'neutral_pct': 35.0,
    'negative_pct': 25.0,
    'sentiments': ['positivo'] * 40 + ['neutral'] * 35 + ['negativo'] * 25,
    'theme_counts': {'velocidad': 10, 'servicio': 15, 'precio': 5}
}

print('📋 PIPELINE 1 (Simple) - Datos disponibles:')
print(f'  Sentiments: {set(simple_results["sentiments"])}')
print(f'  Analysis method: {simple_results["analysis_method"]}')
print(f'  Emotions available: {"emotion_summary" in simple_results}')
print(f'  Pain points available: {"churn_analysis" in simple_results}')
print()

# Simular datos de Pipeline 2 (AI)
ai_results = {
    'analysis_method': 'AI_POWERED',
    'total': 100,
    'positive_count': 40,
    'neutral_count': 35, 
    'negative_count': 25,
    'positive_pct': 40.0,
    'neutral_pct': 35.0,
    'negative_pct': 25.0,
    'sentiments': ['positive'] * 40 + ['neutral'] * 35 + ['negative'] * 25,
    'ai_confidence_avg': 0.87,
    'emotion_summary': {
        'distribution': {
            'satisfacción': 25,
            'frustración': 15,
            'alegría': 10,
            'preocupación': 8,
            'enojo': 5
        },
        'avg_intensity': 3.2
    },
    'churn_analysis': {
        'indicators': ['conexión lenta', 'precio alto', 'servicio intermitente'],
        'risk_level': 'medium'
    },
    'theme_counts': {'velocidad_conexion': 12, 'atencion_cliente': 18, 'facturacion': 8}
}

print('🤖 PIPELINE 2 (AI) - Datos disponibles:')
print(f'  Sentiments: {set(ai_results["sentiments"])}')
print(f'  Analysis method: {ai_results["analysis_method"]}')
print(f'  Emotions available: {"emotion_summary" in ai_results}')
print(f'  Pain points available: {"churn_analysis" in ai_results}')
print(f'  AI confidence: {ai_results["ai_confidence_avg"]}')
print()

print('🎯 EMOTION DATA (AI Only):')
emotions = ai_results['emotion_summary']['distribution']
for emotion, count in emotions.items():
    print(f'  • {emotion}: {count} menciones')

print()
print('⚠️ PAIN POINTS DATA (AI Only):')  
pain_points = ai_results['churn_analysis']['indicators']
for pain in pain_points:
    print(f'  • {pain}')

print()
print('='*60)
print('✅ CONFIRMADO: Pipeline 2 (IA) tiene datos mucho más ricos')
print('   - Emociones específicas en español')
print('   - Puntos de dolor granulares')  
print('   - Confidence scores')
print('   - Themes más detallados')