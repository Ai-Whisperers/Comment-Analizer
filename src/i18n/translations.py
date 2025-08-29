"""
Internationalization Support
Simple translation system for multi-language support
"""

from typing import Dict, Any, List, Optional

class Translations:
    """Simple translation manager"""
    
    # Available languages
    LANGUAGES = {
        'es': 'Español',
        'en': 'English',
        'pt': 'Português',
        'gn': 'Guaraní'
    }
    
    # Translation dictionary
    TRANSLATIONS = {
        'es': {
            # UI Elements
            'title': 'Análisis de Comentarios',
            'subtitle': 'Sistema de análisis de sentimientos',
            'upload_file': 'Cargar archivo',
            'select_file': 'Selecciona un archivo Excel o CSV',
            'analysis_type': 'Selecciona el tipo de análisis',
            'quick_analysis': 'Análisis Rápido',
            'ai_analysis': 'Análisis con IA',
            'analyzing': 'Analizando comentarios...',
            'completed': 'Análisis completado',
            'download': 'Descargar resultados',
            'export_simple': 'Excel Simple (3 hojas)',
            'export_full': 'Excel Completo (16 hojas)',
            
            # Results
            'positive': 'Positivo',
            'neutral': 'Neutral', 
            'negative': 'Negativo',
            'total_comments': 'Total de comentarios',
            'sentiment_distribution': 'Distribución de sentimientos',
            'top_themes': 'Temas principales',
            'key_insights': 'Insights clave',
            'summary': 'Resumen',
            'details': 'Detalles',
            'confidence': 'Confianza',
            'language': 'Idioma',
            'translation': 'Traducción',
            'pain_points': 'Puntos de dolor',
            'emotions': 'Emociones',
            
            # OpenAI Sentiment Analysis Variables
            'sentiment_analysis': 'Análisis de Sentimientos',
            'confidence_score': 'Nivel de Confianza',
            'detected_language': 'Idioma Detectado',
            'spanish_translation': 'Traducción al Español',
            'key_themes': 'Temas Clave',
            'customer_pain_points': 'Puntos de Dolor del Cliente',
            'emotional_analysis': 'Análisis Emocional',
            'comment_quality': 'Calidad del Comentario',
            
            # Emotions (Spanish translations for OpenAI variables)
            'frustración': 'Frustración',
            'satisfacción': 'Satisfacción',
            'enojo': 'Enojo',
            'alegría': 'Alegría',
            'preocupación': 'Preocupación',
            'decepción': 'Decepción',
            'esperanza': 'Esperanza',
            'neutral_emotion': 'Neutral',
            'ira': 'Ira',
            'felicidad': 'Felicidad',
            'inquietud': 'Inquietud',
            'tristeza': 'Tristeza',
            'optimismo': 'Optimismo',
            'ansiedad': 'Ansiedad',
            'entusiasmo': 'Entusiasmo',
            
            # Themes (Spanish for OpenAI categories)
            'velocidad': 'Velocidad',
            'calidad_servicio': 'Calidad del Servicio',
            'precio': 'Precio',
            'soporte_tecnico': 'Soporte Técnico',
            'cobertura': 'Cobertura',
            'facturacion': 'Facturación',
            'instalacion': 'Instalación',
            'conectividad': 'Conectividad',
            'atencion_cliente': 'Atención al Cliente',
            'disponibilidad': 'Disponibilidad',
            'mantenimiento': 'Mantenimiento',
            'equipos': 'Equipos',
            'promociones': 'Promociones',
            'sin_clasificar': 'Sin Clasificar',
            
            # Pain Points Categories
            'conexion_lenta': 'Conexión Lenta',
            'servicio_interrumpido': 'Servicio Interrumpido',
            'mala_atencion': 'Mala Atención',
            'precio_alto': 'Precio Alto',
            'instalacion_demora': 'Demora en Instalación',
            'falta_cobertura': 'Falta de Cobertura',
            'problemas_facturacion': 'Problemas de Facturación',
            'equipos_defectuosos': 'Equipos Defectuosos',
            
            # Quality Indicators
            'high_quality': 'Alta Calidad',
            'medium_quality': 'Calidad Media',
            'low_quality': 'Baja Calidad',
            'informative': 'Informativo',
            'detailed': 'Detallado',
            'brief': 'Breve',
            
            # AI Analysis Metadata
            'ai_powered': 'Con IA',
            'rule_based': 'Basado en Reglas',
            'analysis_method': 'Método de Análisis',
            'ai_confidence_avg': 'Confianza Promedio IA',
            'ai_model_used': 'Modelo IA Utilizado',
            
            # Errors
            'error': 'Error',
            'no_file': 'No se seleccionó archivo',
            'no_comments': 'No se encontraron comentarios',
            'analysis_failed': 'El análisis falló',
            
            # Themes
            'slow_speed': 'Velocidad lenta',
            'intermittent': 'Intermitencias',
            'customer_service': 'Atención al cliente',
            'price': 'Precio',
            'coverage': 'Cobertura',
            'installation': 'Instalación'
        },
        
        'en': {
            # UI Elements
            'title': 'Comment Analysis',
            'subtitle': 'Sentiment analysis system',
            'upload_file': 'Upload file',
            'select_file': 'Select an Excel or CSV file',
            'analysis_type': 'Select analysis type',
            'quick_analysis': 'Quick Analysis',
            'ai_analysis': 'AI Analysis',
            'analyzing': 'Analyzing comments...',
            'completed': 'Analysis completed',
            'download': 'Download results',
            'export_simple': 'Simple Excel (3 sheets)',
            'export_full': 'Full Excel (16 sheets)',
            
            # Results
            'positive': 'Positive',
            'neutral': 'Neutral',
            'negative': 'Negative',
            'total_comments': 'Total comments',
            'sentiment_distribution': 'Sentiment distribution',
            'top_themes': 'Top themes',
            'key_insights': 'Key insights',
            'summary': 'Summary',
            'details': 'Details',
            
            # Errors
            'error': 'Error',
            'no_file': 'No file selected',
            'no_comments': 'No comments found',
            'analysis_failed': 'Analysis failed',
            
            # Themes
            'slow_speed': 'Slow speed',
            'intermittent': 'Intermittent',
            'customer_service': 'Customer service',
            'price': 'Price',
            'coverage': 'Coverage',
            'installation': 'Installation'
        },
        
        'pt': {
            # UI Elements
            'title': 'Análise de Comentários',
            'subtitle': 'Sistema de análise de sentimentos',
            'upload_file': 'Carregar arquivo',
            'select_file': 'Selecione um arquivo Excel ou CSV',
            'analysis_type': 'Selecione o tipo de análise',
            'quick_analysis': 'Análise Rápida',
            'ai_analysis': 'Análise com IA',
            'analyzing': 'Analisando comentários...',
            'completed': 'Análise concluída',
            'download': 'Baixar resultados',
            'export_simple': 'Excel Simples (3 folhas)',
            'export_full': 'Excel Completo (16 folhas)',
            
            # Results
            'positive': 'Positivo',
            'neutral': 'Neutro',
            'negative': 'Negativo',
            'total_comments': 'Total de comentários',
            'sentiment_distribution': 'Distribuição de sentimentos',
            'top_themes': 'Temas principais',
            'key_insights': 'Insights principais',
            'summary': 'Resumo',
            'details': 'Detalhes',
            
            # Errors
            'error': 'Erro',
            'no_file': 'Nenhum arquivo selecionado',
            'no_comments': 'Nenhum comentário encontrado',
            'analysis_failed': 'Análise falhou',
            
            # Themes
            'slow_speed': 'Velocidade lenta',
            'intermittent': 'Intermitente',
            'customer_service': 'Atendimento ao cliente',
            'price': 'Preço',
            'coverage': 'Cobertura',
            'installation': 'Instalação'
        },
        
        'gn': {
            # UI Elements (Basic Guaraní translations)
            'title': "Ñe'ẽ Jesareko",
            'subtitle': "Ñe'ẽ py'ã jesareko",
            'upload_file': "Marandurenda jehupi",
            'select_file': "Eiporavo peteĩ marandurenda",
            'analysis_type': "Eiporavo jesareko mba'éichapa",
            'quick_analysis': "Jesareko pya'e",
            'ai_analysis': "Jesareko AI ndive",
            'analyzing': "Ojesareko hína ñe'ẽ...",
            'completed': "Jesareko opáma",
            'download': "Emboguejy jehupyre",
            'export_simple': "Excel mbykymi (3 rogue)",
            'export_full': "Excel tuicha (16 rogue)",
            
            # Results
            'positive': 'Porã',
            'neutral': "Mbyte",
            'negative': 'Vai',
            'total_comments': "Ñe'ẽ paite",
            'sentiment_distribution': "Mba'éichapa oñeñandu",
            'top_themes': "Mba'e tuichavéva",
            'key_insights': "Mba'e iñimportánteva",
            'summary': 'Mbyky',
            'details': 'Detalle',
            
            # Errors
            'error': 'Jejavy',
            'no_file': "Ndojeporavói marandurenda",
            'no_comments': "Ndojejuhúi ñe'ẽ",
            'analysis_failed': 'Jesareko ndoikói',
            
            # Themes
            'slow_speed': "Mbegue",
            'intermittent': "Oñembyai-mbyai",
            'customer_service': "Ñepytyvõ",
            'price': "Tepy",
            'coverage': "Ojepohýi",
            'installation': "Ñemoĩ"
        }
    }
    
    def __init__(self, language: str = 'es') -> None:
        """Initialize with default language (Spanish)"""
        self.current_language = language
    
    def get(self, key: str, default: Optional[str] = None) -> str:
        """Get translated string for current language"""
        lang_dict = self.TRANSLATIONS.get(self.current_language, self.TRANSLATIONS['es'])
        return lang_dict.get(key, default or key)
    
    def set_language(self, language: str) -> None:
        """Change current language"""
        if language in self.LANGUAGES:
            self.current_language = language
        else:
            self.current_language = 'es'
    
    def get_available_languages(self) -> Dict[str, str]:
        """Get list of available languages"""
        return self.LANGUAGES
    
    def translate_theme(self, theme: str) -> str:
        """Translate theme names"""
        theme_map = {
            'velocidad_lenta': 'slow_speed',
            'intermitencias': 'intermittent',
            'atencion_cliente': 'customer_service',
            'precio': 'price',
            'cobertura': 'coverage',
            'instalacion': 'installation'
        }
        
        theme_key = theme_map.get(theme, theme)
        return self.get(theme_key, theme.replace('_', ' ').title())


# Global translator instance
_translator = None

def get_translator(language: str = 'es') -> Translations:
    """Get or create global translator"""
    global _translator
    if _translator is None:
        _translator = Translations(language)
    return _translator

def t(key: str, default: Optional[str] = None) -> str:
    """Convenience function for translations"""
    translator = get_translator()
    return translator.get(key, default)

def translate_sentiment_data(openai_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Translate OpenAI sentiment analysis result to Spanish for UI display
    
    Args:
        openai_result: Original OpenAI result with English keys
        
    Returns:
        Dictionary with Spanish labels for UI display
    """
    translator = get_translator('es')
    
    translated = {}
    
    # Basic sentiment (keep English internally, translate for display)
    if 'sentiment' in openai_result:
        sentiment = openai_result['sentiment']
        translated['sentimiento'] = translator.get(sentiment, sentiment)
        translated['sentiment_original'] = sentiment  # Keep original for logic
    
    # Confidence score
    if 'confidence' in openai_result:
        translated['confianza'] = openai_result['confidence']
        translated['confianza_porcentaje'] = f"{openai_result['confidence'] * 100:.1f}%"
    
    # Language
    if 'language' in openai_result:
        lang_map = {'es': 'Español', 'en': 'Inglés', 'gn': 'Guaraní', 'mixed': 'Mixto'}
        translated['idioma'] = lang_map.get(openai_result['language'], openai_result['language'])
        translated['idioma_codigo'] = openai_result['language']
    
    # Translation
    if 'translation' in openai_result:
        translated['traduccion'] = openai_result['translation']
    
    # Themes - translate each theme
    if 'themes' in openai_result:
        themes_spanish: List[str] = []
        for theme in openai_result['themes']:
            # Try direct translation first, fallback to cleaned theme
            spanish_theme = translator.get(theme, theme.replace('_', ' ').title())
            themes_spanish.append(spanish_theme)
        translated['temas'] = ', '.join(themes_spanish)
        translated['temas_originales'] = openai_result['themes']  # Keep originals for logic
    
    # Pain points - translate each pain point
    if 'pain_points' in openai_result:
        pain_points_spanish: List[str] = []
        for pain_point in openai_result['pain_points']:
            spanish_pain = translator.get(pain_point.replace(' ', '_').lower(), pain_point)
            pain_points_spanish.append(spanish_pain)
        translated['puntos_dolor'] = ', '.join(pain_points_spanish)
        translated['puntos_dolor_originales'] = openai_result['pain_points']
    
    # Emotions - translate each emotion
    if 'emotions' in openai_result:
        emotions_spanish: List[str] = []
        for emotion in openai_result['emotions']:
            spanish_emotion = translator.get(emotion, emotion.title())
            emotions_spanish.append(spanish_emotion)
        translated['emociones'] = ', '.join(emotions_spanish)
        translated['emociones_originales'] = openai_result['emotions']
    
    return translated

def get_comprehensive_sentiment_labels() -> Dict[str, Any]:
    """
    Get comprehensive sentiment analysis labels in Spanish for Excel export
    
    Returns:
        Dictionary with all possible sentiment analysis labels in Spanish
    """
    translator = get_translator('es')
    
    return {
        'columns': {
            'comment_id': 'ID Comentario',
            'original_comment': 'Comentario Original', 
            'sentiment': 'Sentimiento',
            'confidence': 'Confianza (%)',
            'language': 'Idioma',
            'translation': 'Traducción',
            'themes': 'Temas Principales',
            'pain_points': 'Puntos de Dolor',
            'emotions': 'Emociones',
            'quality_score': 'Puntuación Calidad',
            'ai_enhanced': 'Mejorado con IA'
        },
        'values': {
            'positive': 'Positivo',
            'negative': 'Negativo', 
            'neutral': 'Neutral',
            'spanish': 'Español',
            'english': 'Inglés',
            'guarani': 'Guaraní',
            'mixed': 'Mixto',
            'high': 'Alta',
            'medium': 'Media',
            'low': 'Baja',
            'yes': 'Sí',
            'no': 'No'
        },
        'sections': {
            'summary': 'Resumen de Análisis',
            'detailed_analysis': 'Análisis Detallado',
            'sentiment_distribution': 'Distribución de Sentimientos',
            'theme_analysis': 'Análisis de Temas',
            'emotion_analysis': 'Análisis Emocional',
            'pain_point_analysis': 'Análisis de Puntos de Dolor',
            'quality_metrics': 'Métricas de Calidad',
            'ai_metadata': 'Metadatos de IA'
        }
    }