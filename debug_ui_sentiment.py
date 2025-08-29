"""
Debug script para diagnosticar problema de UI sentiment display
"""

import sys
sys.path.append('src')

# Simular datos que llegan desde main.py
test_results = {
    'total': 100,
    'raw_total': 120,
    'duplicates_removed': 20,
    'positive_count': 40,
    'neutral_count': 35,
    'negative_count': 25,
    'positive_pct': 40.0,
    'neutral_pct': 35.0,
    'negative_pct': 25.0,
    'comments': ['Comentario 1', 'Comentario 2', 'Comentario 3'] * 33,  # 99 comments
    'sentiments': ['positivo'] * 40 + ['neutral'] * 35 + ['negativo'] * 25,
    'comment_frequencies': {},
    'theme_counts': {'velocidad': 10, 'servicio': 15},
    'theme_examples': {'velocidad': ['Lento'], 'servicio': ['Malo']},
    'original_filename': 'test.xlsx',
    'analysis_date': '2025-08-29 12:00:00',
    'file_size': 150.5,
    'avg_length': 45.2,
    'analysis_method': 'SIMPLE_RULE_BASED'
}

print("🔍 Datos de prueba generados:")
print(f"Total: {test_results['total']}")
print(f"Positivos: {test_results['positive_count']} ({test_results['positive_pct']}%)")
print(f"Neutrales: {test_results['neutral_count']} ({test_results['neutral_pct']}%)")  
print(f"Negativos: {test_results['negative_count']} ({test_results['negative_pct']}%)")
print(f"Método: {test_results['analysis_method']}")
print(f"Comentarios: {len(test_results['comments'])}")
print(f"Sentimientos: {len(test_results['sentiments'])}")

print("\n🧪 Validando Counter de sentimientos:")
from collections import Counter
sentiment_counter = Counter(test_results['sentiments'])
print(f"Counter resultado: {dict(sentiment_counter)}")

print("\n✅ Datos están correctos para testing UI")