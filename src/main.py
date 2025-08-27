"""
Análisis de Comentarios de Clientes - Personal Paraguay
Interfaz simplificada con análisis de datos reales en español
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
from datetime import datetime
import numpy as np
from collections import Counter
import re
import json
from io import BytesIO

# Import from relative package paths
from src.services.session_manager import SessionManager
from src.services.file_upload_service import FileUploadService
from src.sentiment_analysis.enhanced_analyzer import EnhancedAnalyzer
from src.enhanced_analysis import EnhancedAnalysis
from src.improved_analysis import ImprovedAnalysis
from src.professional_excel_export import ProfessionalExcelExporter
from src.ai_analysis_adapter import AIAnalysisAdapter

# Page config
st.set_page_config(
    page_title="Personal Paraguay — Análisis de Comentarios",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for simplified design
st.markdown("""
<style>
    /* Root colors matching HTML */
    :root {
        --bg: #0f1419;
        --card: #18202a;
        --ink: #e6edf3;
        --muted: #9aa6b2;
        --border: #243247;
        --ok: #16c784;
        --warn: #f4bf4f;
        --bad: #ff5e57;
        --brand: #4ea4ff;
    }
    
    /* Main app styling */
    .stApp {
        background: var(--bg);
    }
    
    /* Header styling */
    .main-header {
        background: #0e1520;
        border-bottom: 1px solid var(--border);
        padding: 12px 16px;
        margin: -1rem -1rem 1rem -1rem;
        position: sticky;
        top: 0;
        z-index: 999;
    }
    
    /* Card styling */
    .metric-card {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 14px;
        height: 100%;
    }
    
    .metric-label {
        font-size: 12px;
        color: var(--muted);
        text-transform: uppercase;
        margin-bottom: 4px;
    }
    
    .metric-value {
        font-size: 20px;
        font-weight: 700;
        color: var(--ink);
    }
    
    /* Progress bar */
    .progress-bar {
        height: 6px;
        background: #0c141f;
        border: 1px solid #1f2a3a;
        border-radius: 6px;
        overflow: hidden;
        margin-top: 6px;
    }
    
    .progress-fill {
        height: 100%;
        transition: width 0.5s ease;
    }
    
    /* Button styling */
    .stButton > button {
        background: #0f1a26;
        border: 1px solid var(--border);
        color: var(--ink);
        border-radius: 8px;
        padding: 8px 16px;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        background: #1a2433;
        border-color: var(--brand);
    }
    
    /* Primary button */
    .primary-button > button {
        background: var(--brand) !important;
        border-color: transparent !important;
    }
    
    .primary-button > button:hover {
        background: #3d8fd9 !important;
    }
    
    /* File uploader */
    .stFileUploader {
        border: 2px dashed #2b4060;
        border-radius: 10px;
        padding: 24px;
        background: transparent;
    }
    
    .stFileUploader:hover {
        border-color: var(--brand);
        background: #0f1a26;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        border-bottom: 1px solid var(--border);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border: 1px solid transparent;
        border-radius: 8px 8px 0 0;
        color: var(--ink);
    }
    
    .stTabs [aria-selected="true"] {
        background: #101a26;
        border-color: var(--border);
        border-bottom-color: transparent;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Responsive grid */
    @media (max-width: 900px) {
        .summary-grid {
            grid-template-columns: repeat(2, 1fr) !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'session_manager' not in st.session_state:
    st.session_state.session_manager = SessionManager()
    st.session_state.file_service = FileUploadService()
    st.session_state.analyzer = EnhancedAnalyzer()
    st.session_state.ai_adapter = AIAnalysisAdapter()  # Initialize AI adapter
    st.session_state.analysis_results = None
    st.session_state.raw_data = None
    st.session_state.themes_data = None

# Analysis Functions
def analyze_sentiment_simple(text):
    """Análisis de sentimiento mejorado basado en palabras clave en español"""
    if pd.isna(text) or text == "":
        return "neutral"
    
    text_lower = str(text).lower()
    
    # Palabras positivas en español (expandidas)
    positive_words = ['excelente', 'bueno', 'buena', 'mejor', 'satisfecho', 'satisfecha', 'rápido', 'rapido', 
                     'bien', 'perfecto', 'genial', 'feliz', 'contento', 'contenta', 'funciona', 'estable', 
                     'increíble', 'maravilloso', 'fantástico', 'super', 'súper', 'recomiendo', 'conforme',
                     'efectivo', 'eficiente', 'optimo', 'óptimo', 'impecable', 'exitoso', 'exitosa']
    
    # Palabras y frases negativas en español (muy expandidas)
    negative_words = [
        # Palabras básicas negativas
        'malo', 'mala', 'pésimo', 'pesimo', 'terrible', 'horrible', 'peor', 'mal', 'deficiente',
        'insatisfecho', 'insatisfecha', 'decepcionado', 'decepcionada', 'molesto', 'molesta',
        
        # Problemas técnicos específicos
        'lento', 'lenta', 'cae', 'corta', 'se corta', 'corte', 'intermitencia', 'intermitencias',
        'falla', 'fallas', 'error', 'errores', 'problema', 'problemas', 'inestable', 'desconecta',
        'desconectado', 'interrumpe', 'interrupción', 'interrupciones',
        
        # Frases negativas comunes
        'no funciona', 'no sirve', 'no anda', 'nunca funciona', 'siempre falla', 'no me gusta',
        'está mal', 'funciona mal', 'anda mal', 'muy mal', 'está terrible', 'está horrible',
        'no recomiendo', 'pobre servicio', 'mal servicio', 'servicio malo',
        
        # Quejas específicas de telecomunicaciones
        'se va', 'se cae', 'no hay señal', 'sin señal', 'mala señal', 'señal mala', 'débil',
        'cobertura mala', 'mala cobertura', 'no llega', 'muy caro', 'caro', 'costoso',
        'demora', 'tarda', 'tardó', 'esperé', 'lentitud', 'despacio', 'no responde',
        'nadie responde', 'no atiende', 'no contesta',
        
        # Intensificadores negativos
        'súper mal', 'super mal', 'muy malo', 'muy mala', 'demasiado lento', 'demasiado malo',
        'extremadamente', 'totalmente mal', 'completamente mal', 'absolutamente',
        
        # Emociones negativas
        'enojado', 'enojada', 'furioso', 'furiosa', 'irritado', 'irritada', 'frustrado', 'frustrada',
        'harto', 'harta', 'cansado de', 'cansada de'
    ]
    
    # Frases específicamente negativas (peso mayor)
    negative_phrases = [
        'no funciona', 'no sirve', 'no anda', 'está mal', 'funciona mal', 'anda mal',
        'muy mal', 'súper mal', 'super mal', 'no recomiendo', 'pésimo servicio',
        'mal servicio', 'servicio malo', 'se va', 'se cae', 'no hay señal',
        'sin señal', 'mala señal', 'cobertura mala', 'muy caro', 'nadie responde',
        'no contesta', 'no atiende', 'siempre falla', 'nunca funciona'
    ]
    
    # Contar palabras positivas
    pos_count = sum(1 for word in positive_words if word in text_lower)
    
    # Contar palabras negativas (peso normal)
    neg_count = sum(1 for word in negative_words if word in text_lower)
    
    # Contar frases negativas (peso doble)
    phrase_count = sum(2 for phrase in negative_phrases if phrase in text_lower)
    
    total_negative = neg_count + phrase_count
    
    # Lógica mejorada con umbral más bajo para detectar negatividad
    if total_negative > pos_count:
        return "negativo"
    elif pos_count > total_negative:
        return "positivo"
    else:
        # En caso de empate, revisar si hay indicadores sutiles de negatividad
        subtle_negative = ['podría', 'debería', 'necesita mejorar', 'falta', 'sin embargo',
                          'pero', 'aunque', 'regular', 'normal', 'más o menos']
        
        subtle_neg_count = sum(1 for word in subtle_negative if word in text_lower)
        
        if subtle_neg_count > 0 and pos_count == 0:
            return "negativo"
        elif subtle_neg_count > 0:
            return "neutral"
        else:
            return "neutral"

def clean_text(text):
    """Limpiar y corregir errores ortográficos comunes en español"""
    if pd.isna(text) or text == "":
        return text
    
    text = str(text).strip()
    
    # Correcciones ortográficas comunes (más exhaustivas)
    corrections = {
        # Errores comunes de telecomunicaciones
        'pesimo': 'pésimo',
        'pésimo': 'pésimo',
        'rapido': 'rápido',
        'rapida': 'rápida',
        'lentp': 'lento',
        'lentto': 'lento',
        'atencion': 'atención',
        'solucion': 'solución',
        'instalacion': 'instalación',
        'tecnico': 'técnico',
        'servico': 'servicio',
        'servision': 'servicio',
        'internert': 'internet',
        'intrnet': 'internet',
        'intenet': 'internet',
        'inernet': 'internet',
        'fibra optica': 'fibra óptica',
        'señaal': 'señal',
        'senal': 'señal',
        'cobertura': 'cobertura',
        'covertura': 'cobertura',
        
        # Errores de teclado comunes
        'qeu': 'que',
        'que': 'que',
        'dle': 'del',
        'pra': 'para',
        'ocn': 'con',
        'bein': 'bien',
        'bie': 'bien',
        'maol': 'malo',
        'exelente': 'excelente',
        'excelnte': 'excelente',
        'excelnete': 'excelente',
        'buenno': 'bueno',
        'buenna': 'buena',
        
        # Variaciones de negación y problemas
        'no funcona': 'no funciona',
        'no funiona': 'no funciona',
        'no me fnciona': 'no me funciona',
        'no sirv': 'no sirve',
        'no srive': 'no sirve',
        'funciona mal': 'funciona mal',
        'funiona mal': 'funciona mal',
        'no anda': 'no anda',
        'no anfa': 'no anda',
        
        # Palabras con tildes faltantes
        'tambien': 'también',
        'mas': 'más',
        'telefono': 'teléfono',
        'ultimo': 'último',
        'proxima': 'próxima',
        'proximo': 'próximo',
        'facil': 'fácil',
        'dificil': 'difícil',
        'util': 'útil',
        
        # Problemas de servicio específicos
        'se cae': 'se cae',
        'se corta': 'se corta',
        'muy caro': 'muy caro',
        'demasiado caro': 'demasiado caro',
        'intermitencia': 'intermitencia',
        'intermitencias': 'intermitencias',
        'problema': 'problema',
        'problemas': 'problemas',
    }
    
    # Aplicar correcciones palabra por palabra
    words = text.split()
    corrected_words = []
    
    for word in words:
        # Limpiar puntuación para verificación
        clean_word = word.lower().strip('.,!?;:"()[]{}')
        
        # Buscar corrección
        corrected = corrections.get(clean_word, clean_word)
        
        # Preservar capitalización y puntuación original
        if corrected != clean_word:
            # Si la palabra original empezaba con mayúscula, mantenerla
            if word[0].isupper():
                corrected = corrected.capitalize()
            
            # Restaurar puntuación original
            punctuation = ''
            for char in word:
                if not char.isalnum() and not char.isspace():
                    punctuation += char
            
            # Agregar puntuación al final si existía
            if word != word.strip('.,!?;:"()[]{}'):
                end_punct = ''
                for char in reversed(word):
                    if not char.isalnum():
                        end_punct = char + end_punct
                    else:
                        break
                corrected = corrected + end_punct
            
            corrected_words.append(corrected)
        else:
            corrected_words.append(word)
    
    # Limpiar espacios múltiples y caracteres extra
    result = ' '.join(corrected_words)
    result = result.replace('  ', ' ')  # Espacios dobles
    result = result.replace('   ', ' ')  # Espacios triples
    result = result.replace('....', '.')  # Puntos múltiples
    result = result.replace('???', '?')  # Signos múltiples
    result = result.replace('!!!', '!')  # Exclamaciones múltiples
    
    return result.strip()

def remove_duplicates(comments):
    """Remover comentarios duplicados y contar frecuencias"""
    if not comments:
        return [], {}
    
    # Convertir a DataFrame para facilitar manipulación
    df = pd.DataFrame({'comment': comments})
    df['comment_clean'] = df['comment'].apply(lambda x: str(x).lower().strip())
    
    # Contar frecuencias antes de eliminar duplicados
    comment_counts = df['comment_clean'].value_counts().to_dict()
    
    # Remover duplicados exactos (mantener el primer comentario original)
    df_dedup = df.drop_duplicates(subset=['comment_clean'], keep='first')
    
    # Remover comentarios muy cortos (menos de 3 palabras)
    df_filtered = df_dedup[df_dedup['comment_clean'].str.split().str.len() >= 3]
    
    # Remover comentarios que son solo números o caracteres especiales
    df_filtered = df_filtered[df_filtered['comment_clean'].str.contains('[a-zA-ZáéíóúüñÁÉÍÓÚÜÑ]')]
    
    # Crear diccionario de frecuencias para comentarios únicos
    unique_comment_counts = {}
    for _, row in df_filtered.iterrows():
        original_comment = row['comment']
        clean_comment = row['comment_clean']
        unique_comment_counts[original_comment] = comment_counts[clean_comment]
    
    return df_filtered['comment'].tolist(), unique_comment_counts

def extract_themes(texts):
    """Extraer temas comunes del texto en español"""
    themes = {
        'velocidad_lenta': ['lento', 'lenta', 'velocidad', 'lentitud', 'demora', 'tarda', 'despacio'],
        'intermitencias': ['cae', 'corta', 'corte', 'intermitencia', 'inestable', 'interrumpe', 'desconecta'],
        'atencion_cliente': ['atención', 'atencion', 'servicio', 'cliente', 'respuesta', 'soporte', 'ayuda'],
        'precio': ['caro', 'precio', 'costoso', 'tarifa', 'pago', 'factura', 'cobro'],
        'cobertura': ['cobertura', 'señal', 'alcance', 'zona', 'área', 'area', 'llega'],
        'instalacion': ['instalación', 'instalacion', 'técnico', 'tecnico', 'visita', 'demora', 'cita']
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
                if len(theme_examples[theme]) < 3:  # Mantener top 3 ejemplos
                    theme_examples[theme].append(text[:100])  # Primeros 100 caracteres
    
    return theme_counts, theme_examples

def process_uploaded_file(uploaded_file):
    """Procesar archivo subido y extraer datos"""
    try:
        # Leer archivo
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        # Check for NPS and Nota columns (Personal Paraguay specific)
        has_nps = 'NPS' in df.columns
        has_nota = 'Nota' in df.columns
        nps_data = df['NPS'].tolist() if has_nps else []
        nota_data = df['Nota'].tolist() if has_nota else []
        
        # Buscar columna de comentarios (nombres comunes) - incluir 'Comentario Final'
        comment_cols = ['comentario final', 'comment', 'comments', 'feedback', 'review', 'texto', 
                       'comentario', 'comentarios', 'respuesta', 'opinion', 'observacion']
        
        comment_col = None
        for col in df.columns:
            if any(name in col.lower() for name in comment_cols):
                comment_col = col
                break
        
        if comment_col is None and len(df.columns) > 0:
            # Usar primera columna de texto si no se encuentra columna de comentarios
            for col in df.columns:
                if df[col].dtype == 'object':
                    comment_col = col
                    break
        
        if comment_col is None:
            st.error("No se encontró columna de texto en el archivo")
            return None
        
        # Analizar cada comentario con limpieza de datos
        raw_comments = df[comment_col].dropna().tolist()
        
        # Limpiar comentarios y corregir errores ortográficos
        cleaned_comments = [clean_text(comment) for comment in raw_comments]
        
        # Remover duplicados y obtener frecuencias
        unique_comments, comment_frequencies = remove_duplicates(cleaned_comments)
        
        # Analizar sentimientos de comentarios limpios
        sentiments = [analyze_sentiment_simple(comment) for comment in unique_comments]
        
        # Usar comentarios únicos y limpios para el análisis
        comments = unique_comments
        
        # Initialize analyzers
        enhanced_analyzer = EnhancedAnalysis()
        improved_analyzer = ImprovedAnalysis()
        
        # Perform enhanced and improved analysis on each comment
        enhanced_results = []
        churn_risks = []
        urgency_levels = []
        emotion_analysis = []
        competitor_mentions = []
        customer_segments = []
        nps_scores = []
        improved_results = []
        comment_quality = []
        service_issues = []
        
        for i, comment in enumerate(comments):
            # Enhanced analysis
            analysis = enhanced_analyzer.full_analysis(comment)
            enhanced_results.append(analysis)
            
            # Extract key metrics
            churn_risks.append(analysis['churn_risk'])
            urgency_levels.append(analysis['urgency'])
            emotion_analysis.append(analysis['emotions'])
            competitor_mentions.append(analysis['competitors'])
            customer_segments.append(analysis['customer_value'])
            
            # Calculate NPS
            intensity = analysis['emotions']['intensity']
            nps_score = enhanced_analyzer.calculate_nps_from_sentiment(sentiments[i], intensity)
            nps_scores.append(nps_score)
            
            # Improved analysis
            quality = improved_analyzer.analyze_comment_quality(comment)
            comment_quality.append(quality)
            
            themes = improved_analyzer.detect_themes_improved(comment)
            issues = improved_analyzer.analyze_service_issues(comment)
            service_issues.append(issues)
            
            # Enhanced sentiment with rating if available
            nota = nota_data[i] if has_nota and i < len(nota_data) else None
            enhanced_sentiment = improved_analyzer.enhanced_sentiment_analysis(comment, nota)
            
            improved_results.append({
                'quality': quality,
                'themes': themes,
                'issues': issues,
                'enhanced_sentiment': enhanced_sentiment
            })
        
        # Calcular estadísticas
        total = len(comments)
        sentiment_counts = Counter(sentiments)
        
        positive_pct = (sentiment_counts['positivo'] / total * 100) if total > 0 else 0
        neutral_pct = (sentiment_counts['neutral'] / total * 100) if total > 0 else 0
        negative_pct = (sentiment_counts['negativo'] / total * 100) if total > 0 else 0
        
        # Extraer temas
        theme_counts, theme_examples = extract_themes(comments)
        
        # Calculate enhanced metrics
        high_churn_count = sum(1 for r in churn_risks if r['risk_level'] == 'high')
        medium_churn_count = sum(1 for r in churn_risks if r['risk_level'] == 'medium')
        
        urgency_distribution = Counter(urgency_levels)
        
        # Calculate NPS - Use actual NPS data if available  
        if has_nps and nps_data:
            # Use improved analyzer for real NPS calculation
            df_for_nps = pd.DataFrame({
                'NPS': nps_data[:len(comments)],
                'Nota': nota_data[:len(comments)] if has_nota else None
            })
            nps_analysis = improved_analyzer.calculate_real_nps(df_for_nps)
            
            if nps_analysis:
                promoters = nps_analysis['promoters']
                passives = nps_analysis['passives']
                detractors = nps_analysis['detractors']
                nps = nps_analysis['nps_score']
            else:
                # Fallback
                promoters = sum(1 for nps in nps_data[:len(comments)] if str(nps).lower() == 'promotor')
                passives = sum(1 for nps in nps_data[:len(comments)] if str(nps).lower() == 'pasivo')
                detractors = sum(1 for nps in nps_data[:len(comments)] if str(nps).lower() == 'detractor')
                nps = ((promoters - detractors) / total * 100) if total > 0 else 0
        else:
            # Fallback to calculated NPS
            promoters = sum(1 for score in nps_scores if score >= 9)
            detractors = sum(1 for score in nps_scores if score <= 6)
            passives = total - promoters - detractors
            nps = ((promoters - detractors) / total * 100) if total > 0 else 0
        
        # Calculate average rating and CSI if Nota column exists
        avg_rating = 0
        csi_analysis = None
        if has_nota and nota_data:
            avg_rating = np.mean([n for n in nota_data[:len(comments)] if pd.notna(n)])
            # Calculate Customer Satisfaction Index
            df_for_csi = pd.DataFrame({'Nota': nota_data[:len(comments)]})
            csi_analysis = improved_analyzer.calculate_customer_satisfaction_index(df_for_csi)
        
        # Analyze competitors
        total_competitor_mentions = sum(1 for m in competitor_mentions if m['mentioned'])
        
        # Emotion summary
        dominant_emotions = Counter([e['dominant_emotion'] for e in emotion_analysis])
        avg_intensity = np.mean([e['intensity'] for e in emotion_analysis])
        
        # Simple satisfaction trend calculation
        positive_ratio = sentiment_counts['positivo'] / total if total > 0 else 0
        negative_ratio = sentiment_counts['negativo'] / total if total > 0 else 0
        
        if positive_ratio > 0.4:
            trend = 'improving'
            confidence = min(95, positive_ratio * 100)
        elif negative_ratio > 0.3:
            trend = 'declining'
            confidence = min(95, negative_ratio * 100)
        else:
            trend = 'stable'
            confidence = 70
            
        satisfaction_trend = {
            'trend': trend,
            'confidence': round(confidence, 1),
            'positive_ratio': round(positive_ratio * 100, 1),
            'negative_ratio': round(negative_ratio * 100, 1)
        }
        
        # Simple alert generation
        alerts = []
        if negative_pct > 30:
            alerts.append({
                'severity': 'high',
                'message': f'Alto porcentaje de comentarios negativos: {negative_pct:.1f}%',
                'action': 'Revisar causas principales de insatisfacción'
            })
        
        if high_churn_count > 10:
            alerts.append({
                'severity': 'critical',
                'message': f'{high_churn_count} clientes en alto riesgo de cancelación',
                'action': 'Activar campaña de retención urgente'
            })
        
        if urgency_distribution.get('P0', 0) > 0:
            alerts.append({
                'severity': 'critical',
                'message': f'{urgency_distribution["P0"]} casos críticos sin servicio',
                'action': 'Respuesta técnica inmediata'
            })
        
        if total_competitor_mentions > total * 0.15:
            alerts.append({
                'severity': 'medium',
                'message': f'Competidores mencionados en {(total_competitor_mentions/total*100):.1f}% de comentarios',
                'action': 'Análisis competitivo requerido'
            })
        
        # Calcular estadísticas del archivo
        file_size_kb = uploaded_file.size / 1024
        avg_length = np.mean([len(str(c)) for c in comments]) if comments else 0
        
        return {
            'total': total,
            'positive_pct': round(positive_pct, 1),
            'neutral_pct': round(neutral_pct, 1),
            'negative_pct': round(negative_pct, 1),
            'positive_count': sentiment_counts['positivo'],
            'neutral_count': sentiment_counts['neutral'],
            'negative_count': sentiment_counts['negativo'],
            'theme_counts': theme_counts,
            'theme_examples': theme_examples,
            'file_size': round(file_size_kb, 1),
            'avg_length': round(avg_length),
            'comments': comments,  # Todos los comentarios limpios para descarga
            'sentiments': sentiments,  # Todos los sentimientos para descarga
            'comment_frequencies': comment_frequencies,  # Frecuencias de cada comentario
            'original_filename': uploaded_file.name,
            'analysis_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'raw_total': len(raw_comments),  # Total antes de limpieza
            'duplicates_removed': len(raw_comments) - len(unique_comments),  # Duplicados eliminados
            'cleaning_applied': True,
            # Enhanced analysis results
            'enhanced_results': enhanced_results,
            'churn_analysis': {
                'high_risk': high_churn_count,
                'medium_risk': medium_churn_count,
                'low_risk': total - high_churn_count - medium_churn_count,
                'details': churn_risks
            },
            'urgency_distribution': dict(urgency_distribution),
            'nps': {
                'score': round(nps, 1),
                'promoters': promoters,
                'detractors': detractors,
                'passives': passives,
                'has_real_nps': has_nps
            },
            'rating_data': {
                'average': round(avg_rating, 1) if avg_rating else 0,
                'has_ratings': has_nota,
                'ratings': nota_data[:len(comments)] if has_nota else []
            },
            'nps_categories': nps_data[:len(comments)] if has_nps else [],
            'competitor_analysis': {
                'total_mentions': total_competitor_mentions,
                'percentage': round((total_competitor_mentions / total * 100), 1) if total > 0 else 0,
                'details': competitor_mentions
            },
            'emotion_summary': {
                'distribution': dict(dominant_emotions),
                'avg_intensity': round(avg_intensity, 1)
            },
            'customer_segments': customer_segments,
            # Keep only essential advanced analytics
            'satisfaction_trend': satisfaction_trend,
            'alerts': alerts,
            # Improved analysis results
            'improved_results': improved_results,
            'comment_quality_summary': Counter([q['quality'] for q in comment_quality]),
            'informative_comments': sum(1 for q in comment_quality if q['informative']),
            'service_issues_summary': Counter([i['severity'] for i in service_issues]),
            'csi_analysis': csi_analysis,
            'insights': improved_analyzer.generate_insights({
                'nps': {'nps_score': nps} if has_nps else None,
                'service_issues': service_issues
            })
        }
    except Exception as e:
        st.error(f"Error procesando archivo: {str(e)}")
        return None

def generate_report_excel(results):
    """Generar reporte Excel profesional con toda la información"""
    # Use professional Excel exporter
    exporter = ProfessionalExcelExporter()
    return exporter.create_professional_excel(results)
    
def generate_report_excel_old(results):
    """Legacy Excel generation (kept for backup)"""
    output = BytesIO()
    
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        # Hoja 1: Metadata y Resumen General
        metadata_data = {
            'Campo': [
                'Archivo Original', 'Fecha de Análisis', 'Total de Comentarios', 'Comentarios Originales',
                'Duplicados Eliminados', 'Sentimiento Positivo (%)', 'Sentimiento Neutral (%)', 
                'Sentimiento Negativo (%)', 'Cantidad Positivos', 'Cantidad Neutrales', 
                'Cantidad Negativos', 'Tamaño del Archivo (KB)', 'Longitud Promedio (chars)'
            ],
            'Valor': [
                results['original_filename'], results['analysis_date'], results['total'], results['raw_total'],
                results['duplicates_removed'], results['positive_pct'], results['neutral_pct'], 
                results['negative_pct'], results['positive_count'], results['neutral_count'],
                results['negative_count'], results['file_size'], results['avg_length']
            ]
        }
        metadata_df = pd.DataFrame(metadata_data)
        metadata_df.to_excel(writer, sheet_name='Metadata y Resumen', index=False)
        
        # Hoja 2: Comentarios Analizados (con frecuencias y sentimientos)
        detailed_data = {
            'Comentario Limpio': results['comments'],
            'Sentimiento': results['sentiments'],
            'Frecuencia': [results['comment_frequencies'].get(comment, 1) for comment in results['comments']]
        }
        detailed_df = pd.DataFrame(detailed_data)
        # Ordenar por frecuencia descendente
        detailed_df = detailed_df.sort_values('Frecuencia', ascending=False)
        detailed_df.to_excel(writer, sheet_name='Comentarios Analizados', index=False)
        
        # Hoja 3: Distribución de Sentimientos
        sentiment_summary = {
            'Sentimiento': ['Positivo', 'Neutral', 'Negativo'],
            'Cantidad': [results['positive_count'], results['neutral_count'], results['negative_count']],
            'Porcentaje': [results['positive_pct'], results['neutral_pct'], results['negative_pct']]
        }
        sentiment_df = pd.DataFrame(sentiment_summary)
        sentiment_df.to_excel(writer, sheet_name='Distribución Sentimientos', index=False)
        
        # Hoja 4: Temas Detectados
        theme_labels = {
            'velocidad_lenta': 'Velocidad Lenta',
            'intermitencias': 'Intermitencias',
            'atencion_cliente': 'Atención al Cliente',
            'precio': 'Precio',
            'cobertura': 'Cobertura',
            'instalacion': 'Instalación'
        }
        
        themes_data = {
            'Tema': [theme_labels.get(theme, theme.replace('_', ' ').title()) for theme in results['theme_counts'].keys()],
            'Código de Tema': list(results['theme_counts'].keys()),
            'Cantidad de Menciones': list(results['theme_counts'].values())
        }
        themes_df = pd.DataFrame(themes_data)
        # Ordenar por cantidad de menciones descendente
        themes_df = themes_df.sort_values('Cantidad de Menciones', ascending=False)
        themes_df.to_excel(writer, sheet_name='Temas Detectados', index=False)
        
        # Hoja 5: Ejemplos por Tema
        examples_data = []
        for theme, examples in results['theme_examples'].items():
            theme_display = theme_labels.get(theme, theme.replace('_', ' ').title())
            for i, example in enumerate(examples[:5], 1):  # Aumentar a 5 ejemplos
                examples_data.append({
                    'Tema': theme_display,
                    'Código de Tema': theme,
                    'Ejemplo #': i,
                    'Texto del Ejemplo': example,
                    'Longitud': len(example)
                })
        
        if examples_data:
            examples_df = pd.DataFrame(examples_data)
            examples_df.to_excel(writer, sheet_name='Ejemplos por Tema', index=False)
        
        # Hoja 6: Dashboard Ejecutivo (NEW)
        dashboard_data = {
            'KPI': [
                'Net Promoter Score (NPS)',
                'Riesgo de Churn Alto',
                'Riesgo de Churn Medio',
                'Casos Críticos (P0)',
                'Casos Urgentes (P1)',
                'Menciones a Competidores',
                'Intensidad Emocional Promedio',
                'Clientes VIP Identificados'
            ],
            'Valor': [
                f"{results.get('nps', {}).get('score', 0)}%",
                results.get('churn_analysis', {}).get('high_risk', 0),
                results.get('churn_analysis', {}).get('medium_risk', 0),
                results.get('urgency_distribution', {}).get('P0', 0),
                results.get('urgency_distribution', {}).get('P1', 0),
                f"{results.get('competitor_analysis', {}).get('total_mentions', 0)} ({results.get('competitor_analysis', {}).get('percentage', 0)}%)",
                results.get('emotion_summary', {}).get('avg_intensity', 0),
                sum(1 for seg in results.get('customer_segments', []) if seg.get('value_segment') == 'vip')
            ],
            'Estado': [
                '🟢 Bueno' if results.get('nps', {}).get('score', 0) > 0 else '🔴 Crítico',
                '🔴 Alerta' if results.get('churn_analysis', {}).get('high_risk', 0) > 10 else '🟡 Monitorear',
                '🟡 Monitorear' if results.get('churn_analysis', {}).get('medium_risk', 0) > 20 else '🟢 Normal',
                '🔴 Crítico' if results.get('urgency_distribution', {}).get('P0', 0) > 0 else '🟢 Sin casos',
                '🟡 Atención' if results.get('urgency_distribution', {}).get('P1', 0) > 5 else '🟢 Controlado',
                '🔴 Alto' if results.get('competitor_analysis', {}).get('percentage', 0) > 15 else '🟢 Normal',
                '🟡 Medio' if results.get('emotion_summary', {}).get('avg_intensity', 0) > 6 else '🟢 Normal',
                '🟢 Identificados' if sum(1 for seg in results.get('customer_segments', []) if seg.get('value_segment') == 'vip') > 0 else '🟡 No detectados'
            ]
        }
        dashboard_df = pd.DataFrame(dashboard_data)
        dashboard_df.to_excel(writer, sheet_name='Dashboard Ejecutivo', index=False)
        
        # Hoja 7: Análisis de Churn (NEW)
        churn_data = []
        for i, comment in enumerate(results.get('comments', [])):
            if i < len(results.get('enhanced_results', [])):
                churn_info = results['enhanced_results'][i]['churn_risk']
                churn_data.append({
                    'Comentario': comment[:100],
                    'Nivel de Riesgo': churn_info['risk_level'],
                    'Score (0-10)': churn_info['score'],
                    'Probabilidad (%)': churn_info['probability'],
                    'Indicadores': ', '.join(churn_info['indicators']) if churn_info['indicators'] else 'N/A',
                    'Acción Recomendada': 'Llamada urgente' if churn_info['risk_level'] == 'high' else 
                                         'Oferta especial' if churn_info['risk_level'] == 'medium' else 'Monitorear'
                })
        
        if churn_data:
            churn_df = pd.DataFrame(churn_data)
            churn_df = churn_df.sort_values('Score (0-10)', ascending=False)
            churn_df.to_excel(writer, sheet_name='Análisis de Churn', index=False)
        
        # Hoja 8: Análisis de Emociones (NEW)
        emotion_data = []
        for i, comment in enumerate(results.get('comments', [])):
            if i < len(results.get('enhanced_results', [])):
                emotion_info = results['enhanced_results'][i]['emotions']
                emotion_data.append({
                    'Comentario': comment[:100],
                    'Emoción Dominante': emotion_info['dominant_emotion'],
                    'Intensidad (1-10)': emotion_info['intensity'],
                    'Todas las Emociones': ', '.join([f"{k}: {v}" for k, v in emotion_info['all_emotions'].items()]) if emotion_info['all_emotions'] else 'Neutral'
                })
        
        if emotion_data:
            emotion_df = pd.DataFrame(emotion_data)
            emotion_df = emotion_df.sort_values('Intensidad (1-10)', ascending=False)
            emotion_df.to_excel(writer, sheet_name='Análisis de Emociones', index=False)
        
        # Hoja 9: Análisis Competitivo (NEW)
        competitor_data = []
        for i, comment in enumerate(results.get('comments', [])):
            if i < len(results.get('enhanced_results', [])):
                comp_info = results['enhanced_results'][i]['competitors']
                if comp_info['mentioned']:
                    competitor_data.append({
                        'Comentario': comment[:100],
                        'Competidores Mencionados': ', '.join(comp_info['mentioned']),
                        'Contexto': '; '.join([f"{k}: {v}" for k, v in comp_info['context'].items()])[:200]
                    })
        
        if competitor_data:
            competitor_df = pd.DataFrame(competitor_data)
            competitor_df.to_excel(writer, sheet_name='Análisis Competitivo', index=False)
        
        # Hoja 10: Plan de Acción (NEW)
        # Generate action plan based on analysis
        enhanced_analyzer = EnhancedAnalysis()
        action_plan = enhanced_analyzer.generate_action_plan(results)
        
        if action_plan:
            action_df = pd.DataFrame(action_plan)
            action_df.to_excel(writer, sheet_name='Plan de Acción', index=False)
        
        # Removed CLV, ROI, Revenue at Risk, and Cohorts sheets
        
        # Hoja 17: Alertas y Notificaciones - NEW
        if 'alerts' in results and results['alerts']:
            alert_df = pd.DataFrame(results['alerts'])
            alert_df.to_excel(writer, sheet_name='Alertas Críticas', index=False)
        
        # Removed Segmentación de Clientes sheet
        
        # Removed separate sentiment comment sheets
        
        # Hoja 7: Estadísticas de Limpieza
        cleaning_stats = {
            'Proceso': [
                'Comentarios Originales', 'Después de Corrección Ortográfica', 
                'Duplicados Eliminados', 'Comentarios Únicos Finales',
                'Tasa de Duplicación (%)', 'Comentarios Muy Cortos Eliminados'
            ],
            'Cantidad': [
                results['raw_total'], results['raw_total'], results['duplicates_removed'],
                results['total'], round((results['duplicates_removed'] / results['raw_total']) * 100, 2) if results['raw_total'] > 0 else 0,
                'N/A'  # Podríamos agregar esto si queremos
            ]
        }
        cleaning_df = pd.DataFrame(cleaning_stats)
        cleaning_df.to_excel(writer, sheet_name='Estadísticas Limpieza', index=False)
    
    return output.getvalue()


# Encabezado
st.markdown("""
<div class="main-header">
    <strong style="font-size: 16px;">🔬 Personal Paraguay</strong> · 
    <span style="color: var(--muted);">Análisis de Comentarios de Clientes</span>
</div>
""", unsafe_allow_html=True)

# Contenedor principal
container = st.container()

with container:
    # Métricas resumen - Dinámicas basadas en análisis
    col1, col2, col3, col4 = st.columns(4)
    
    if st.session_state.analysis_results:
        results = st.session_state.analysis_results
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total</div>
                <div class="metric-value">{results['total']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Positivo</div>
                <div class="metric-value" style="color: var(--ok);">{results['positive_pct']}%</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {results['positive_pct']}%; background: var(--ok);"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Neutral</div>
                <div class="metric-value" style="color: var(--warn);">{results['neutral_pct']}%</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {results['neutral_pct']}%; background: var(--warn);"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Negativo</div>
                <div class="metric-value" style="color: var(--bad);">{results['negative_pct']}%</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {results['negative_pct']}%; background: var(--bad);"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        # Estado vacío por defecto
        for col in [col1, col2, col3, col4]:
            with col:
                labels = ["Total", "Positivo", "Neutral", "Negativo"]
                idx = [col1, col2, col3, col4].index(col)
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">{labels[idx]}</div>
                    <div class="metric-value">—</div>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Sección de Carga y Análisis
    with st.container():
        st.markdown("## Cargar y Analizar")
        
        uploaded_file = st.file_uploader(
            "Arrastra Excel/CSV aquí o haz clic para buscar",
            type=['xlsx', 'xls', 'csv'],
            help="Sube comentarios de clientes para análisis"
        )
        
        # Solo marcar el archivo como cargado, sin análisis automático
        if uploaded_file:
            # Safe session state assignment
            if 'last_uploaded_file' not in st.session_state:
                st.session_state.last_uploaded_file = None
            st.session_state.last_uploaded_file = uploaded_file.name
            st.info("📁 Archivo cargado. Haz clic en '🚀 Análisis Rápido' para procesar los comentarios.")
        

        # Analysis buttons - Quick and AI options
        if uploaded_file:
            st.markdown("### 🔬 Selecciona el tipo de análisis")
            
            col1, col2 = st.columns([1, 1])
            
            # Quick Analysis (existing functionality)
            with col1:
                st.markdown("""
                <div style="text-align: center; padding: 10px; border: 2px solid #10B981; border-radius: 10px; margin: 5px;">
                    <h4 style="color: #10B981; margin: 0;">🚀 Análisis Rápido</h4>
                    <p style="margin: 5px 0; font-size: 0.9em;">Análisis inmediato basado en patrones<br/>
                    <strong>Gratis • Instantáneo • Confiable</strong></p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("Iniciar Análisis Rápido", key="quick", use_container_width=True, type="secondary"):
                    with st.spinner("🧹 Limpiando datos y analizando comentarios..."):
                        results = process_uploaded_file(uploaded_file)
                        if results:
                            results['analysis_method'] = 'RULE_BASED'  # Mark as rule-based
                            st.session_state.analysis_results = results
                            st.success("✅ ¡Análisis rápido completado!")
                            st.rerun()
            
            # AI Analysis (new functionality)
            with col2:
                st.markdown("""
                <div style="text-align: center; padding: 10px; border: 2px solid #3B82F6; border-radius: 10px; margin: 5px;">
                    <h4 style="color: #3B82F6; margin: 0;">🤖 Análisis con IA</h4>
                    <p style="margin: 5px 0; font-size: 0.9em;">Análisis avanzado con OpenAI GPT-4<br/>
                    <strong>Más preciso • Emociones • Multiidioma</strong></p>
                </div>
                """, unsafe_allow_html=True)
                
                # Show AI availability status
                ai_available = st.session_state.ai_adapter.ai_available
                if ai_available:
                    st.info("🟢 IA disponible - GPT-4 conectado")
                else:
                    st.warning("🟡 IA no disponible - Se usará análisis de respaldo")
                
                if st.button("Iniciar Análisis con IA", key="ai", use_container_width=True, type="primary"):
                    with st.spinner("🤖 Analizando comentarios con inteligencia artificial..."):
                        with st.status("Procesando con IA...", expanded=True) as status:
                            st.write("🔄 Inicializando análisis AI...")
                            
                            # Use AI adapter for analysis
                            ai_results = st.session_state.ai_adapter.process_uploaded_file_with_ai(uploaded_file)
                            
                            if ai_results:
                                st.write("✅ Análisis completado exitosamente")
                                status.update(label="✅ Análisis AI completado", state="complete", expanded=False)
                                
                                st.session_state.analysis_results = ai_results
                                
                                # Show analysis method used
                                method = ai_results.get('analysis_method', 'UNKNOWN')
                                if method == 'AI_POWERED':
                                    st.success("🤖 ¡Análisis con IA completado! Utilizando OpenAI GPT-4")
                                elif method == 'RULE_BASED_FALLBACK':
                                    st.warning("⚠️ IA no disponible - Se completó con análisis de respaldo")
                                    
                                st.rerun()
                            else:
                                st.write("❌ Error en el análisis")
                                status.update(label="❌ Error en análisis AI", state="error", expanded=False)
                                st.error("Error en el análisis. Por favor intente de nuevo o use el análisis rápido.")
        
        # Verificación permanente de limpieza (siempre visible si hay resultados)
        if st.session_state.analysis_results:
            results = st.session_state.analysis_results
            
            # Show analysis method badge
            analysis_method = results.get('analysis_method', 'UNKNOWN')
            ai_confidence = results.get('ai_confidence_avg', 0)
            
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.markdown("### 📋 Verificación de Limpieza de Datos")
            with col2:
                if analysis_method == 'AI_POWERED':
                    st.markdown(f"""
                    <div style="background: linear-gradient(90deg, #3B82F6, #1E40AF); color: white; padding: 8px; border-radius: 20px; text-align: center; font-size: 0.8em; margin-top: 10px;">
                        🤖 Análisis con IA (Confianza: {ai_confidence:.1%})
                    </div>
                    """, unsafe_allow_html=True)
                elif analysis_method == 'RULE_BASED_FALLBACK':
                    st.markdown("""
                    <div style="background: linear-gradient(90deg, #F59E0B, #D97706); color: white; padding: 8px; border-radius: 20px; text-align: center; font-size: 0.8em; margin-top: 10px;">
                        🔄 Análisis de Respaldo
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style="background: linear-gradient(90deg, #10B981, #059669); color: white; padding: 8px; border-radius: 20px; text-align: center; font-size: 0.8em; margin-top: 10px;">
                        🚀 Análisis Rápido
                    </div>
                    """, unsafe_allow_html=True)
            with col3:
                if analysis_method in ['AI_POWERED', 'RULE_BASED_FALLBACK']:
                    ai_model = results.get('ai_model_used', 'GPT-4')
                    if ai_model:
                        st.markdown(f"""
                        <div style="background: #1F2937; color: #E5E7EB; padding: 8px; border-radius: 15px; text-align: center; font-size: 0.7em; margin-top: 10px;">
                            {ai_model}
                        </div>
                        """, unsafe_allow_html=True)
            
            # Enhanced Metrics Display (NEW)
            st.markdown("### 🎯 Métricas Avanzadas")
            
            # Display Rating and CSI if available
            if results.get('rating_data', {}).get('has_ratings'):
                avg_rating = results['rating_data']['average']
                st.info(f"⭐ **Calificación Promedio**: {avg_rating}/10 (basado en columna 'Nota' del archivo)")
                
                # Display Customer Satisfaction Index
                if results.get('csi_analysis'):
                    csi = results['csi_analysis']
                    csi_color = '🟢' if csi['level'] in ['Excelente', 'Bueno'] else '🟡' if csi['level'] == 'Regular' else '🔴'
                    st.metric(
                        "Índice de Satisfacción del Cliente (CSI)",
                        f"{csi['csi_score']}%",
                        f"{csi_color} {csi['level']}"
                    )
                    st.caption(csi['interpretation'])
            
            # Display Comment Quality Analysis
            if results.get('comment_quality_summary'):
                st.markdown("### 📝 Calidad de Comentarios")
                quality_col1, quality_col2, quality_col3 = st.columns(3)
                
                with quality_col1:
                    informative = results.get('informative_comments', 0)
                    total = results.get('total', 1)
                    st.metric(
                        "Comentarios Informativos",
                        f"{informative}/{total}",
                        f"{informative/total*100:.0f}%"
                    )
                
                with quality_col2:
                    quality_summary = results.get('comment_quality_summary', {})
                    detailed = quality_summary.get('detailed', 0) + quality_summary.get('moderate', 0)
                    st.metric(
                        "Comentarios Detallados",
                        detailed,
                        "20+ caracteres"
                    )
                
                with quality_col3:
                    non_info = quality_summary.get('non_informative', 0) + quality_summary.get('too_short', 0)
                    st.metric(
                        "Respuestas No Útiles",
                        non_info,
                        "ej: 'No', '.', 'Nada'"
                    )
            
            # Display Service Issues
            if results.get('service_issues_summary'):
                issues = results['service_issues_summary']
                if issues.get('critical', 0) > 0 or issues.get('high', 0) > 0:
                    st.markdown("### 🔧 Problemas de Servicio Detectados")
                    issue_col1, issue_col2, issue_col3 = st.columns(3)
                    
                    with issue_col1:
                        critical = issues.get('critical', 0)
                        color = 'red' if critical > 0 else 'gray'
                        st.metric(
                            "🔴 Críticos",
                            critical,
                            "Sin servicio"
                        )
                    
                    with issue_col2:
                        high = issues.get('high', 0)
                        st.metric(
                            "🟠 Altos",
                            high,
                            "Intermitencias"
                        )
                    
                    with issue_col3:
                        medium = issues.get('medium', 0)
                        st.metric(
                            "🟡 Medios",
                            medium,
                            "Lentitud"
                        )
            
            # Display Insights
            if results.get('insights'):
                st.markdown("### 💡 Insights Clave")
                for insight in results['insights']:
                    icon = '🔴' if insight['type'] == 'critical' else '🟠' if insight['type'] == 'warning' else '💡'
                    st.info(f"{icon} **{insight['area']}**: {insight['insight']}\n\n**Acción recomendada**: {insight['action']}")
            
            # Display Alerts if any
            if results.get('alerts'):
                st.markdown("### ⚠️ Alertas Críticas")
                for alert in results['alerts']:
                    severity_color = {'critical': '🔴', 'high': '🟠', 'medium': '🟡'}.get(alert['severity'], '⚪')
                    st.warning(f"{severity_color} **{alert['message']}** - Acción: {alert['action']}")
            
            
            # Satisfaction Trend
            if results.get('satisfaction_trend'):
                trend = results['satisfaction_trend']
                trend_icon = {'improving': '📈', 'declining': '📉', 'stable': '➡️'}.get(trend['trend'], '❓')
                st.info(f"{trend_icon} **Tendencia de Satisfacción**: {trend['trend']} (Confianza: {trend['confidence']}%)")
            
            # NPS and Churn Metrics
            met_col1, met_col2, met_col3, met_col4 = st.columns(4)
            
            with met_col1:
                nps_score = results.get('nps', {}).get('score', 0)
                nps_color = 'var(--ok)' if nps_score > 0 else 'var(--bad)' if nps_score < 0 else 'var(--warn)'
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Net Promoter Score</div>
                    <div class="metric-value" style="color: {nps_color};">{nps_score}%</div>
                </div>
                """, unsafe_allow_html=True)
            
            with met_col2:
                high_churn = results.get('churn_analysis', {}).get('high_risk', 0)
                churn_color = 'var(--bad)' if high_churn > 10 else 'var(--warn)' if high_churn > 5 else 'var(--ok)'
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Riesgo Churn Alto</div>
                    <div class="metric-value" style="color: {churn_color};">{high_churn}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with met_col3:
                p0_cases = results.get('urgency_distribution', {}).get('P0', 0)
                p0_color = 'var(--bad)' if p0_cases > 0 else 'var(--ok)'
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Casos Críticos (P0)</div>
                    <div class="metric-value" style="color: {p0_color};">{p0_cases}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with met_col4:
                comp_percent = results.get('competitor_analysis', {}).get('percentage', 0)
                comp_color = 'var(--bad)' if comp_percent > 15 else 'var(--warn)' if comp_percent > 10 else 'var(--ok)'
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Menciones Competencia</div>
                    <div class="metric-value" style="color: {comp_color};">{comp_percent}%</div>
                </div>
                """, unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("📄 Originales", results['raw_total'])
            
            with col2:
                duplicates = results.get('duplicates_removed', 0)
                st.metric("🗑️ Duplicados Eliminados", duplicates)
            
            with col3:
                st.metric("✨ Únicos Limpios", results['total'])
            
            with col4:
                reduction_pct = round((duplicates / results['raw_total'] * 100), 1) if results['raw_total'] > 0 else 0
                st.metric("📉 Reducción", f"{reduction_pct}%")
            
            # Status de limpieza
            if duplicates > 0:
                st.success(f"✅ **Limpieza completada:** Se eliminaron {duplicates} comentarios duplicados y se corrigieron errores ortográficos automáticamente.")
            else:
                st.success("✅ **Limpieza completada:** Se corrigieron errores ortográficos automáticamente. No se encontraron comentarios duplicados.")
            
            st.markdown("---")

        # Download section - Solo Excel
        if st.session_state.analysis_results:
            st.markdown("### 📥 Descargar Resultados")
            
            # Centrar el botón de Excel
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                # Excel download
                excel_data = generate_report_excel(st.session_state.analysis_results)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename_excel = f"analisis_personal_paraguay_{timestamp}.xlsx"
                
                st.download_button(
                    label="📊 Descargar Reporte Profesional Excel (15+ Hojas)",
                    data=excel_data,
                    file_name=filename_excel,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                    help="Reporte profesional completo con: Portada, Resumen Ejecutivo, Metodología, KPIs Dashboard, Análisis NPS, Sentimientos, Emociones, Temas, Problemas de Servicio, Competencia, Churn, Plan de Acción, Comentarios Detallados, Estadísticas, Glosario y Anexos"
                )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Pestañas de Vista General
    tab1, tab2, tab3 = st.tabs(["📊 Sentimiento", "📈 NPS", "📉 Tendencias"])
    
    with tab1:
        if st.session_state.analysis_results:
            results = st.session_state.analysis_results
            col1, col2 = st.columns(2)
            
            with col1:
                # Gráfico de distribución de sentimiento
                fig = go.Figure(data=[
                    go.Bar(
                        x=['Positivo', 'Neutral', 'Negativo'], 
                        y=[results['positive_count'], results['neutral_count'], results['negative_count']],
                        marker_color=['#16c784', '#f4bf4f', '#ff5e57'],
                        text=[f"{results['positive_pct']}%", f"{results['neutral_pct']}%", f"{results['negative_pct']}%"],
                        textposition='auto'
                    )
                ])
                fig.update_layout(
                    title="Distribución de Sentimientos",
                    plot_bgcolor='#0f1419',
                    paper_bgcolor='#18202a',
                    font=dict(color='#e6edf3'),
                    height=300,
                    showlegend=False,
                    yaxis_title="Cantidad",
                    xaxis_title=""
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Gráfico de temas principales
                theme_data = results['theme_counts']
                top_themes = sorted(theme_data.items(), key=lambda x: x[1], reverse=True)[:5]
                
                theme_labels = {
                    'velocidad_lenta': 'Velocidad Lenta',
                    'intermitencias': 'Intermitencias',
                    'atencion_cliente': 'Atención al Cliente',
                    'precio': 'Precio',
                    'cobertura': 'Cobertura',
                    'instalacion': 'Instalación'
                }
                
                if top_themes:
                    themes_fig = go.Figure(data=[
                        go.Bar(
                            x=[count for _, count in top_themes], 
                            y=[theme_labels.get(theme, theme.replace('_', ' ').title()) for theme, _ in top_themes],
                            orientation='h',
                            marker_color='#4ea4ff',
                            text=[count for _, count in top_themes],
                            textposition='auto'
                        )
                    ])
                    themes_fig.update_layout(
                        title="Temas Principales",
                        plot_bgcolor='#0f1419',
                        paper_bgcolor='#18202a',
                        font=dict(color='#e6edf3'),
                        height=300,
                        showlegend=False,
                        xaxis_title="Menciones",
                        yaxis_title=""
                    )
                    st.plotly_chart(themes_fig, use_container_width=True)
                else:
                    st.info("No se detectaron temas aún")
        else:
            col1, col2 = st.columns(2)
            with col1:
                st.info("📊 La distribución de sentimientos aparecerá aquí después del análisis")
            with col2:
                st.info("📊 Los temas principales aparecerán aquí después del análisis")
    
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### NPS por Tema")
            if st.session_state.analysis_results:
                st.info("Cálculo de NPS basado en mapeo de sentimientos")
                # Estimación simple de NPS desde sentimiento
                results = st.session_state.analysis_results
                promoters = results['positive_count']
                passives = results['neutral_count']
                detractors = results['negative_count']
                total = results['total']
                nps = ((promoters - detractors) / total * 100) if total > 0 else 0
                st.metric("Puntuación NPS Estimada", f"{nps:.1f}")
            else:
                st.info("Sube datos para ver el análisis de NPS")
        
        with col2:
            st.markdown("### Promotores / Pasivos / Detractores")
            if st.session_state.analysis_results:
                results = st.session_state.analysis_results
                fig = go.Figure(data=[go.Pie(
                    labels=['Promotores', 'Pasivos', 'Detractores'],
                    values=[results['positive_count'], results['neutral_count'], results['negative_count']],
                    hole=.3,
                    marker_colors=['#16c784', '#f4bf4f', '#ff5e57']
                )])
                fig.update_layout(
                    plot_bgcolor='#0f1419',
                    paper_bgcolor='#18202a',
                    font=dict(color='#e6edf3'),
                    height=250,
                    showlegend=True
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Sube datos para ver la categorización de clientes")
    
    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Sentimiento Semana a Semana")
            st.info("El análisis de tendencias históricas requiere datos de series temporales")
        with col2:
            st.markdown("### Tendencias de Problemas")
            st.info("La evolución de problemas requiere datos históricos")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Temas y Puntos de Dolor
    with st.container():
        st.markdown("## Temas y Puntos de Dolor")
        
        if st.session_state.analysis_results:
            results = st.session_state.analysis_results
            theme_data = results['theme_counts']
            theme_examples = results['theme_examples']
            
            theme_labels = {
                'velocidad_lenta': 'Velocidad Lenta',
                'intermitencias': 'Intermitencias',
                'atencion_cliente': 'Atención al Cliente',
                'precio': 'Precio',
                'cobertura': 'Cobertura',
                'instalacion': 'Instalación'
            }
            
            # Obtener top 3 temas
            top_themes = sorted(theme_data.items(), key=lambda x: x[1], reverse=True)[:3]
            
            if top_themes:
                cols = st.columns(3)
                for idx, (theme, count) in enumerate(top_themes):
                    with cols[idx]:
                        theme_display = theme_labels.get(theme, theme.replace('_', ' ').title())
                        if st.button(f"{theme_display} ({count})", key=f"theme_{idx}", use_container_width=True):
                            with st.expander("Ejemplos", expanded=True):
                                examples = theme_examples.get(theme, [])
                                if examples:
                                    for example in examples[:3]:
                                        st.write(f"• {example}")
                                else:
                                    st.write("No hay ejemplos disponibles")
            else:
                st.info("No se detectaron temas. Sube datos para ver el análisis de temas.")
        else:
            col1, col2, col3 = st.columns(3)
            for idx, col in enumerate([col1, col2, col3]):
                with col:
                    st.button("—", disabled=True, use_container_width=True, key=f"empty_theme_{idx}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Recomendaciones
    with st.container():
        st.markdown("## Recomendaciones")
        
        if st.session_state.analysis_results:
            results = st.session_state.analysis_results
            
            # Generar recomendaciones basadas en análisis
            recommendations = []
            
            # Verificar distribución de sentimientos
            if results['negative_pct'] > 30:
                recommendations.append("**Experiencia del Cliente (P1):** Alto sentimiento negativo detectado. Se necesita acción inmediata para abordar las preocupaciones de los clientes.")
            
            # Verificar temas
            theme_counts = results['theme_counts']
            if theme_counts.get('velocidad_lenta', 0) > 10:
                recommendations.append("**Operaciones de Red (P1):** Problemas de velocidad reportados frecuentemente. Se requiere optimización de red.")
            
            if theme_counts.get('intermitencias', 0) > 10:
                recommendations.append("**Técnico (P1):** Interrupciones de servicio detectadas. Se necesita revisión de estabilidad de infraestructura.")
            
            if theme_counts.get('atencion_cliente', 0) > 5:
                recommendations.append("**Atención al Cliente (P2):** Se necesitan mejoras en el servicio al cliente basadas en los comentarios.")
            
            if theme_counts.get('precio', 0) > 5:
                recommendations.append("**Comercial (P2):** Revisar estructura de precios según percepción de clientes.")
            
            if theme_counts.get('cobertura', 0) > 5:
                recommendations.append("**Expansión de Red (P2):** Considerar mejoras de cobertura en zonas afectadas.")
            
            if not recommendations:
                if results['positive_pct'] > 60:
                    recommendations.append("**Continuar Estrategia Actual:** Alta satisfacción del cliente detectada.")
                else:
                    recommendations.append("**Monitorear Tendencias:** Continuar monitoreando los comentarios de clientes para problemas emergentes.")
            
            for rec in recommendations:
                st.markdown(f"- {rec}")
        else:
            st.markdown("""
            - **Sube datos** para recibir recomendaciones generadas por IA
            - **Analiza patrones** en los comentarios de clientes
            - **Obtén insights accionables** para mejoras
            """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Estadísticas de Datos
    with st.container():
        st.markdown("## Estadísticas de Datos")
        
        col1, col2, col3 = st.columns(3)
        
        if st.session_state.analysis_results:
            results = st.session_state.analysis_results
            
            with col1:
                st.metric("Tamaño del Archivo", f"{results['file_size']} KB")
            
            with col2:
                st.metric("Total de Registros", results['total'])
            
            with col3:
                st.metric("Longitud Promedio", f"{results['avg_length']} caracteres")
        else:
            with col1:
                st.metric("Tamaño del Archivo", "—")
            
            with col2:
                st.metric("Total de Registros", "—")
            
            with col3:
                st.metric("Longitud Promedio", "—")