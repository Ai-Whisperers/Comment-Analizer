"""
Internationalization Support
Simple translation system for multi-language support
"""

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
    
    def __init__(self, language='es'):
        """Initialize with default language (Spanish)"""
        self.current_language = language
    
    def get(self, key: str, default: str = None) -> str:
        """Get translated string for current language"""
        lang_dict = self.TRANSLATIONS.get(self.current_language, self.TRANSLATIONS['es'])
        return lang_dict.get(key, default or key)
    
    def set_language(self, language: str):
        """Change current language"""
        if language in self.LANGUAGES:
            self.current_language = language
        else:
            self.current_language = 'es'
    
    def get_available_languages(self):
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

def get_translator(language='es') -> Translations:
    """Get or create global translator"""
    global _translator
    if _translator is None:
        _translator = Translations(language)
    return _translator

def t(key: str, default: str = None) -> str:
    """Convenience function for translations"""
    translator = get_translator()
    return translator.get(key, default)