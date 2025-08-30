"""
Analysis Engine - Core business logic extracted from main.py
Preserves all sentiment analysis and processing functionality
"""

import pandas as pd
import re
from collections import Counter
from typing import List, Dict, Tuple
import logging

logger = logging.getLogger(__name__)


def analyze_sentiment_simple(text):
    """Simple sentiment analysis for Spanish text"""
    if pd.isna(text) or text == "":
        return 'neutral'
    
    text = str(text).lower()
    
    # Enhanced Spanish sentiment lexicon
    positive_words = [
        'excelente', 'bueno', 'bien', 'perfecto', 'genial', 'fantástico',
        'rápido', 'eficiente', 'recomiendo', 'satisfecho', 'contento',
        'funciona', 'estable', 'claro', 'fácil', 'útil', 'práctico'
    ]
    
    negative_words = [
        'malo', 'pésimo', 'terrible', 'horrible', 'lento', 'demora',
        'caro', 'costoso', 'problemático', 'deficiente', 'falla',
        'corta', 'interrumpe', 'molesto', 'complicado', 'difícil'
    ]
    
    positive_score = sum(1 for word in positive_words if word in text)
    negative_score = sum(1 for word in negative_words if word in text)
    
    if positive_score > negative_score:
        return 'positivo'
    elif negative_score > positive_score:
        return 'negativo'
    else:
        return 'neutral'


def clean_text_simple(text):
    """Clean and normalize text"""
    if pd.isna(text) or text == "":
        return text
    
    text = str(text).strip()
    
    # Basic corrections for common typos
    corrections = {
        'pesimo': 'pésimo', 'lentp': 'lento', 'servico': 'servicio',
        'internert': 'internet', 'intenet': 'internet', 'señaal': 'señal',
        'exelente': 'excelente', 'buenno': 'bueno', 'no funcona': 'no funciona'
    }
    
    for wrong, correct in corrections.items():
        text = text.replace(wrong, correct)
    
    return text.strip()


def remove_duplicates_simple(comments):
    """Remove duplicate comments"""
    if not comments:
        return [], {}
    
    # Remove exact duplicates and very short comments
    seen = set()
    unique_comments = []
    frequencies = {}
    
    for comment in comments:
        if pd.isna(comment):
            continue
        
        clean = str(comment).lower().strip()
        if len(clean.split()) >= 3 and clean not in seen:  # At least 3 words
            seen.add(clean)
            unique_comments.append(comment)
            frequencies[comment] = 1
        elif clean in seen:
            # Count frequency of duplicates
            for uc in unique_comments:
                if str(uc).lower().strip() == clean:
                    frequencies[uc] = frequencies.get(uc, 1) + 1
                    break
    
    return unique_comments, frequencies


def extract_themes_simple(texts):
    """Extract themes from comments"""
    themes = {
        'velocidad': ['lento', 'lenta', 'velocidad', 'demora', 'tarda'],
        'interrupciones': ['cae', 'corta', 'corte', 'intermitencia', 'interrumpe'],
        'servicio': ['atención', 'servicio', 'cliente', 'soporte', 'ayuda'],
        'precio': ['caro', 'precio', 'costoso', 'tarifa', 'factura'],
        'cobertura': ['cobertura', 'señal', 'zona', 'área', 'alcance'],
        'instalacion': ['instalación', 'técnico', 'visita', 'demora']
    }
    
    theme_counts = {theme: 0 for theme in themes}
    theme_examples = {theme: [] for theme in themes}
    
    for text in texts:
        if pd.isna(text):
            continue
        text_lower = str(text).lower()
        for theme, keywords in themes.items():
            if any(keyword in text_lower for keyword in keywords):
                theme_counts[theme] += 1
                if len(theme_examples[theme]) < 3:
                    theme_examples[theme].append(text[:100])
    
    return theme_counts, theme_examples


def calculate_sentiment_percentages(sentiments: List[str]) -> Dict[str, float]:
    """Calculate sentiment distribution percentages"""
    if not sentiments:
        return {'positivo': 0, 'neutral': 0, 'negativo': 0}
    
    sentiment_counts = Counter(sentiments)
    total = len(sentiments)
    
    return {
        'positivo': round((sentiment_counts.get('positivo', 0) / total) * 100, 1),
        'neutral': round((sentiment_counts.get('neutral', 0) / total) * 100, 1),
        'negativo': round((sentiment_counts.get('negativo', 0) / total) * 100, 1)
    }


def generate_insights_summary(results: Dict) -> Dict:
    """Generate analysis insights summary"""
    total_comments = results.get('total', 0)
    sentiment_percentages = results.get('sentiment_percentages', {})
    theme_counts = results.get('theme_counts', {})
    
    # Key insights
    insights = {
        'total_comments_analyzed': total_comments,
        'dominant_sentiment': max(sentiment_percentages.items(), key=lambda x: x[1])[0] if sentiment_percentages else 'neutral',
        'sentiment_confidence': max(sentiment_percentages.values()) if sentiment_percentages else 0,
        'top_theme': max(theme_counts.items(), key=lambda x: x[1])[0] if theme_counts else 'general',
        'theme_diversity': len([theme for theme, count in theme_counts.items() if count > 0]),
        'analysis_quality': 'high' if total_comments > 50 else 'medium' if total_comments > 10 else 'basic'
    }
    
    return insights


def create_recommendations(results: Dict) -> List[str]:
    """Generate actionable recommendations based on analysis"""
    recommendations = []
    
    sentiment_percentages = results.get('sentiment_percentages', {})
    theme_counts = results.get('theme_counts', {})
    
    # Sentiment-based recommendations
    if sentiment_percentages.get('negativo', 0) > 30:
        recommendations.append("Atención prioritaria a comentarios negativos - más del 30% requiere intervención")
    
    if sentiment_percentages.get('positivo', 0) > 70:
        recommendations.append("Excelente percepción del servicio - mantener estándares actuales")
    
    # Theme-based recommendations
    if theme_counts.get('velocidad', 0) > 5:
        recommendations.append("Optimizar velocidad del servicio - tema recurrente en comentarios")
    
    if theme_counts.get('interrupciones', 0) > 3:
        recommendations.append("Revisar estabilidad de conexión - interrupciones reportadas frecuentemente")
    
    if theme_counts.get('precio', 0) > 3:
        recommendations.append("Evaluar competitividad de precios - mencionado en múltiples comentarios")
    
    if not recommendations:
        recommendations.append("Mantener calidad actual del servicio - comentarios en rango normal")
    
    return recommendations