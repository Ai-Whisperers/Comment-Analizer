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


def analyze_emotions_enhanced(text) -> Dict:
    """Enhanced emotion detection for Spanish text"""
    if pd.isna(text) or text == "":
        return {'dominant_emotion': 'neutral', 'all_emotions': {}, 'intensity': 0}
    
    text = str(text).lower()
    
    # Spanish emotion patterns
    emotion_patterns = {
        'satisfacción': ['satisfecho', 'satisfactorio', 'contento', 'complacido', 'cumple', 'funciona bien'],
        'frustración': ['frustrado', 'molesto', 'desesperante', 'no funciona', 'problema', 'falla'],
        'alegría': ['feliz', 'alegre', 'encantado', 'genial', 'excelente', 'fantástico'],
        'enojo': ['enojado', 'furioso', 'rabioso', 'indignado', 'terrible', 'pésimo'],
        'preocupación': ['preocupado', 'preocupante', 'inquieto', 'nervioso', 'dudoso'],
        'confianza': ['confío', 'seguro', 'confiable', 'estable', 'sólido'],
        'desilusión': ['decepcionado', 'desilusionado', 'esperaba más', 'no cumple'],
        'agradecimiento': ['gracias', 'agradecido', 'reconozco', 'valoro'],
        'optimismo': ['optimista', 'esperanzado', 'positivo', 'mejorará'],
        'irritación': ['irritado', 'fastidioso', 'molestia', 'incomoda'],
        'sorpresa': ['sorprendido', 'inesperado', 'no esperaba', 'increíble'],
        'tranquilidad': ['tranquilo', 'relajado', 'paz', 'sereno'],
        'ansiedad': ['ansioso', 'nervioso', 'estresado', 'agobiado'],
        'esperanza': ['espero', 'ojalá', 'esperanzado', 'confío en que'],
        'pesimismo': ['pesimista', 'negativo', 'no creo', 'dudo que']
    }
    
    # Detect emotions and calculate intensity
    detected_emotions = {}
    total_intensity = 0
    
    for emotion, patterns in emotion_patterns.items():
        intensity = sum(2 if pattern in text else 1 for pattern in patterns if pattern in text)
        if intensity > 0:
            detected_emotions[emotion] = intensity
            total_intensity += intensity
    
    # Determine dominant emotion
    dominant_emotion = max(detected_emotions.items(), key=lambda x: x[1])[0] if detected_emotions else 'neutral'
    
    # Calculate average intensity (0-10 scale)
    avg_intensity = min(10, round((total_intensity / max(1, len(detected_emotions))) * 1.5)) if detected_emotions else 0
    
    return {
        'dominant_emotion': dominant_emotion,
        'all_emotions': detected_emotions,
        'intensity': avg_intensity
    }


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


def generate_insights_summary(results: Dict, enhanced_ai: bool = False) -> Dict:
    """Generate analysis insights summary"""
    total_comments = results.get('total', 0)
    sentiment_percentages = results.get('sentiment_percentages', {})
    theme_counts = results.get('theme_counts', {})
    
    # Base insights
    insights = {
        'total_comments_analyzed': total_comments,
        'dominant_sentiment': max(sentiment_percentages.items(), key=lambda x: x[1])[0] if sentiment_percentages else 'neutral',
        'sentiment_confidence': max(sentiment_percentages.values()) if sentiment_percentages else 0,
        'top_theme': max(theme_counts.items(), key=lambda x: x[1])[0] if theme_counts else 'general',
        'theme_diversity': len([theme for theme, count in theme_counts.items() if count > 0]),
        'analysis_quality': 'high' if total_comments > 50 else 'medium' if total_comments > 10 else 'basic'
    }
    
    # AI Enhanced insights
    if enhanced_ai:
        insights.update({
            'sentiment_stability': calculate_sentiment_stability(sentiment_percentages),
            'emotional_intensity': calculate_emotional_intensity(sentiment_percentages),
            'priority_action_areas': identify_priority_areas(theme_counts, sentiment_percentages),
            'customer_satisfaction_index': calculate_satisfaction_index(sentiment_percentages),
            'engagement_quality': assess_engagement_quality(total_comments, theme_counts)
        })
    
    return insights


def calculate_sentiment_stability(sentiment_percentages: Dict) -> str:
    """Calculate how balanced/stable the sentiment distribution is"""
    values = list(sentiment_percentages.values())
    if not values:
        return 'unknown'
    
    max_val = max(values)
    if max_val > 80:
        return 'muy_polarizado'
    elif max_val > 60:
        return 'polarizado' 
    elif max_val > 40:
        return 'balanceado'
    else:
        return 'muy_balanceado'


def calculate_emotional_intensity(sentiment_percentages: Dict) -> str:
    """Calculate the emotional intensity of the feedback"""
    positive = sentiment_percentages.get('positivo', 0)
    negative = sentiment_percentages.get('negativo', 0)
    
    intensity = positive + negative  # Total non-neutral sentiment
    
    if intensity > 80:
        return 'muy_alto'
    elif intensity > 60:
        return 'alto'
    elif intensity > 40:
        return 'medio'
    else:
        return 'bajo'


def identify_priority_areas(theme_counts: Dict, sentiment_percentages: Dict) -> List[str]:
    """Identify priority areas for business action using AI logic"""
    priorities = []
    
    # High frequency themes become priorities
    sorted_themes = sorted(theme_counts.items(), key=lambda x: x[1], reverse=True)
    high_frequency_themes = [theme for theme, count in sorted_themes[:3] if count > 2]
    
    for theme in high_frequency_themes:
        priorities.append(f"{theme}_optimization")
    
    # Sentiment-based priorities
    if sentiment_percentages.get('negativo', 0) > 25:
        priorities.append('negative_sentiment_mitigation')
    
    if sentiment_percentages.get('positivo', 0) > 70:
        priorities.append('positive_experience_amplification')
    
    return priorities[:4]  # Top 4 priorities


def calculate_satisfaction_index(sentiment_percentages: Dict) -> float:
    """Calculate customer satisfaction index (0-100)"""
    positive = sentiment_percentages.get('positivo', 0)
    neutral = sentiment_percentages.get('neutral', 0) 
    negative = sentiment_percentages.get('negativo', 0)
    
    # Weighted satisfaction score (neutral counts as 0.5)
    satisfaction = (positive * 1.0) + (neutral * 0.5) + (negative * 0.0)
    return round(satisfaction, 1)


def assess_engagement_quality(total_comments: int, theme_counts: Dict) -> str:
    """Assess the quality/depth of customer engagement"""
    active_themes = len([theme for theme, count in theme_counts.items() if count > 0])
    
    if total_comments > 100 and active_themes > 4:
        return 'excelente'
    elif total_comments > 50 and active_themes > 3:
        return 'bueno'
    elif total_comments > 20 and active_themes > 2:
        return 'moderado'
    else:
        return 'basico'


def create_recommendations(results: Dict, enhanced_ai: bool = False) -> List[str]:
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
    
    # Enhanced AI recommendations
    if enhanced_ai:
        insights = results.get('insights', {})
        satisfaction_index = insights.get('customer_satisfaction_index', 50)
        emotional_intensity = insights.get('emotional_intensity', 'medio')
        priority_areas = insights.get('priority_action_areas', [])
        
        # Advanced strategic recommendations
        if satisfaction_index > 80:
            recommendations.append("🎯 EXCELENCIA: Capitalizar alta satisfacción - implementar programa de referidos")
        elif satisfaction_index < 40:
            recommendations.append("🚨 CRÍTICO: Plan de mejora urgente - satisfacción por debajo del 40%")
        
        if emotional_intensity == 'muy_alto':
            recommendations.append("⚡ INTENSIDAD ALTA: Comentarios muy emocionales - respuesta personalizada recomendada")
        
        # Priority area specific recommendations
        for area in priority_areas:
            if 'velocidad' in area:
                recommendations.append("🚀 VELOCIDAD: Optimizar infraestructura de red en zonas críticas")
            elif 'precio' in area:
                recommendations.append("💰 PRECIO: Evaluar estrategia de precios vs competencia")
            elif 'servicio' in area:
                recommendations.append("🎯 SERVICIO: Capacitación adicional al equipo de atención")
    
    if not recommendations:
        recommendations.append("Mantener calidad actual del servicio - comentarios en rango normal")
    
    return recommendations