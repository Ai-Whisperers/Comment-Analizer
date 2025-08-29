"""
Simplified Streamlit App for Cloud Deployment
Minimal version for testing deployment
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
import re
from io import BytesIO

# Page config
st.set_page_config(
    page_title="Personal Paraguay — Análisis de Comentarios",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Title
st.title("📊 Personal Paraguay — Análisis de Comentarios")
st.markdown("### Sistema de análisis de sentimientos para comentarios de clientes")

# Check for OpenAI API key
api_key_configured = st.secrets.get("OPENAI_API_KEY") is not None

if not api_key_configured:
    st.error("⚠️ **Configuración Requerida**: OpenAI API key no configurada en Streamlit Cloud secrets.")
    st.info("""
    **Para administradores**: Configura la clave API en Streamlit Cloud:
    1. Ve a la configuración de la app
    2. Añade en **Secrets**:
    ```
    OPENAI_API_KEY = "tu-clave-api-aqui"
    ```
    """)
    st.stop()

# Simple sentiment analysis for testing
def analyze_sentiment_simple(text):
    """Basic sentiment analysis for testing"""
    if pd.isna(text) or text == "":
        return "neutral"
    
    text = str(text).lower()
    
    positive_words = ['excelente', 'bueno', 'buena', 'mejor', 'satisfecho', 'rápido', 'bien']
    negative_words = ['malo', 'mala', 'pésimo', 'terrible', 'lento', 'problema']
    
    positive_count = sum(word in text for word in positive_words)
    negative_count = sum(word in text for word in negative_words)
    
    if positive_count > negative_count:
        return "positive"
    elif negative_count > positive_count:
        return "negative"
    else:
        return "neutral"

# File upload
st.markdown("#### 📁 Subir Archivo")
uploaded_file = st.file_uploader(
    "Selecciona un archivo Excel o CSV con comentarios",
    type=['xlsx', 'xls', 'csv']
)

if uploaded_file:
    try:
        # Read file
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        st.success(f"✅ Archivo cargado: {len(df)} filas")
        
        # Show first few rows
        st.markdown("#### 👀 Vista previa de datos")
        st.dataframe(df.head())
        
        # Look for comment columns
        comment_columns = []
        for col in df.columns:
            if any(keyword in col.lower() for keyword in ['comment', 'comentario', 'texto', 'feedback']):
                comment_columns.append(col)
        
        if comment_columns:
            selected_column = st.selectbox("Selecciona la columna de comentarios:", comment_columns)
            
            if st.button("🚀 Analizar Sentimientos"):
                with st.spinner("Analizando sentimientos..."):
                    # Simple analysis
                    df['sentimiento'] = df[selected_column].apply(analyze_sentiment_simple)
                    
                    # Results
                    sentiment_counts = df['sentimiento'].value_counts()
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("😊 Positivos", sentiment_counts.get('positive', 0))
                    with col2:
                        st.metric("😐 Neutrales", sentiment_counts.get('neutral', 0))
                    with col3:
                        st.metric("😞 Negativos", sentiment_counts.get('negative', 0))
                    
                    # Chart
                    fig = px.pie(
                        values=sentiment_counts.values,
                        names=sentiment_counts.index,
                        title="Distribución de Sentimientos"
                    )
                    st.plotly_chart(fig)
                    
                    # Download results
                    csv = df.to_csv(index=False)
                    st.download_button(
                        "📥 Descargar Resultados",
                        csv,
                        "resultados_sentimientos.csv",
                        "text/csv"
                    )
        else:
            st.warning("No se encontraron columnas de comentarios. Busca columnas que contengan: 'comment', 'comentario', 'texto', o 'feedback'")
    
    except Exception as e:
        st.error(f"Error procesando archivo: {str(e)}")

else:
    st.info("👆 Sube un archivo para comenzar el análisis")

# Footer
st.markdown("---")
st.markdown("**Personal Paraguay** - Sistema de Análisis de Comentarios v2.0")
st.markdown(f"🕐 Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M')}")