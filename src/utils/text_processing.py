"""
Text Processing Utilities
Extracted from main.py to avoid circular imports and Streamlit execution issues
"""

import pandas as pd
import numpy as np
import re
from typing import List, Tuple, Dict


def clean_text(text):
    """Limpia y corrige ortografía en el texto"""
    if pd.isna(text):
        return ""
    
    text = str(text)
    
    # Diccionario de correcciones ortográficas comunes en español paraguayo
    corrections = {
        # Internet/conexión
        'internert': 'internet', 'intrernet': 'internet', 'imternet': 'internet',
        'coneccion': 'conexión', 'conección': 'conexión', 'conecsion': 'conexión',
        'conexion': 'conexión', 'conecxion': 'conexión',
        
        # Servicio
        'serbicio': 'servicio', 'servico': 'servicio', 'cervicio': 'servicio',
        'servisio': 'servicio', 'servició': 'servicio',
        
        # Velocidad
        'velosidad': 'velocidad', 'velocida': 'velocidad', 'belocidad': 'velocidad',
        'belozidad': 'velocidad',
        
        # Calidad
        'calida': 'calidad', 'calidaf': 'calidad', 'calidac': 'calidad',
        
        # Malo/bueno
        'vien': 'bien', 'vn': 'bien',
        
        # Instalación
        'instalasion': 'instalación', 'instalacion': 'instalación',
        'inslatacion': 'instalación', 'istalacion': 'instalación',
        
        # Atención
        'atencion': 'atención', 'atension': 'atención', 'atenció': 'atención',
        
        # Problema
        'prolema': 'problema', 'ploblema': 'problema', 'provlema': 'problema',
        
        # Cliente
        'cliete': 'cliente', 'clente': 'cliente',
        
        # Técnico
        'tecnico': 'técnico', 'tecnco': 'técnico',
        
        # Rápido
        'rapido': 'rápido', 'rapdo': 'rápido',
        
        # Solución
        'solucion': 'solución', 'solusion': 'solución',
        
        # Teléfono
        'telefono': 'teléfono', 'telfono': 'teléfono',
        
        # Demora
        'demoro': 'demoró', 'tardo': 'tardó',
        
        # Mejorar
        'mejorar': 'mejorar', 'megor': 'mejor',
        
        # Excelente
        'exelente': 'excelente', 'excelnte': 'excelente', 'ecelente': 'excelente',
        
        # Pésimo
        'pecimo': 'pésimo', 'pesimo': 'pésimo',
        
        # Está/esta
        'esta': 'está',
        
        # Más
        'mas': 'más',
        
        # Día
        'dia': 'día', 'dias': 'días',
        
        # Correcciones específicas de problemas comunes
        'mui': 'muy', 'mu': 'muy',
        'ase': 'hace', 'ace': 'hace',
        'ai': 'hay', 'ahy': 'hay',
        'asta': 'hasta', 'hata': 'hasta',
        'ora': 'hora', 'oras': 'horas',
        'aber': 'haber', 'aver': 'haber',
        'abia': 'había', 'avia': 'había',
        'alla': 'haya',
        'aya': 'haya',
        'bamos': 'vamos',
        'boy': 'voy',
        'ber': 'ver',
        'bio': 'vio',
        'ise': 'hice', 'hise': 'hice',
        'iso': 'hizo', 'hiso': 'hizo',
        
        # Frases comunes mal escritas
        'se cae': 'se cae', 'se corta': 'se corta',
        'no funciona': 'no funciona', 'no anda': 'no anda',
        'muy lento': 'muy lento', 'muy malo': 'muy malo',
        'muy bueno': 'muy bueno', 'muy bien': 'muy bien',
        'mal servicio': 'mal servicio', 'buen servicio': 'buen servicio',
        'pesima atencion': 'pésima atención', 'buena atencion': 'buena atención',
        'no sirve': 'no sirve', 'no vale': 'no vale',
        'una porqueria': 'una porquería', 'una basura': 'una basura',
        'muy caro': 'muy caro', 'demasiado caro': 'demasiado caro',
        'super lento': 'súper lento', 'super malo': 'súper malo',
        'super bien': 'súper bien', 'super bueno': 'súper bueno',
        
        # Guaraní común
        'mba\'e': 'nada', 'ndaipori': 'no hay',
        'porã': 'bueno', 'vai': 'malo',
        'heta': 'mucho', 'sa\'i': 'poco'
    }
    
    # Aplicar correcciones palabra por palabra
    words = text.split()
    corrected_words = []
    
    for word in words:
        # Preservar capitalización
        lower_word = word.lower()
        # Eliminar puntuación al final para la comparación
        clean_word = lower_word.rstrip('.,!?;:')
        punctuation = lower_word[len(clean_word):]
        
        if clean_word in corrections:
            # Aplicar corrección preservando capitalización original
            if word[0].isupper():
                corrected = corrections[clean_word].capitalize()
            else:
                corrected = corrections[clean_word]
            corrected_words.append(corrected + punctuation)
        else:
            corrected_words.append(word)
    
    text = ' '.join(corrected_words)
    
    # Limpiar espacios múltiples
    text = ' '.join(text.split())
    
    # Limpiar puntuación excesiva
    text = re.sub(r'([.!?])\1+', r'\1', text)
    
    return text


def remove_duplicates(comments):
    """Elimina comentarios duplicados y filtra comentarios muy cortos"""
    # Convertir todos a string y lowercase para comparación
    comments_lower = [str(comment).lower().strip() for comment in comments]
    
    # Diccionario para contar frecuencias
    comment_freq = {}
    unique_indices = []
    
    for i, comment in enumerate(comments_lower):
        if comment not in comment_freq:
            comment_freq[comment] = 1
            unique_indices.append(i)
        else:
            comment_freq[comment] += 1
    
    # Obtener comentarios únicos preservando el original (no lowercase)
    unique_comments = [comments[i] for i in unique_indices]
    
    # Filtrar comentarios muy cortos (menos de 3 palabras) o que no contienen letras
    filtered_comments = []
    filtered_frequencies = {}
    
    for comment in unique_comments:
        # Verificar longitud y contenido
        if len(str(comment).split()) >= 3 and any(c.isalpha() for c in str(comment)):
            filtered_comments.append(comment)
            # Obtener frecuencia del comentario original
            comment_lower = str(comment).lower().strip()
            filtered_frequencies[comment] = comment_freq.get(comment_lower, 1)
    
    return filtered_comments, filtered_frequencies


def extract_themes(comments: List[str]) -> Tuple[Dict[str, int], Dict[str, List[str]]]:
    """Extrae temas principales de los comentarios"""
    themes = {
        'velocidad_lenta': ['lento', 'lentitud', 'demora', 'tarda', 'despacio', 'lag', 'ping'],
        'intermitencias': ['corta', 'cae', 'intermitente', 'inestable', 'desconecta', 'pierde'],
        'atencion_cliente': ['atencion', 'atención', 'servicio al cliente', 'soporte', 'ayuda', 'respuesta'],
        'precio': ['caro', 'precio', 'cobro', 'factura', 'pago', 'costoso', 'barato'],
        'cobertura': ['cobertura', 'señal', 'alcance', 'llega', 'zona'],
        'instalacion': ['instalacion', 'instalación', 'técnico', 'visita', 'demora instalacion']
    }
    
    theme_counts = {theme: 0 for theme in themes}
    theme_examples = {theme: [] for theme in themes}
    
    for comment in comments:
        comment_lower = str(comment).lower()
        for theme, keywords in themes.items():
            if any(keyword in comment_lower for keyword in keywords):
                theme_counts[theme] += 1
                if len(theme_examples[theme]) < 3:  # Keep top 3 examples
                    theme_examples[theme].append(comment[:100])  # Truncate long comments
    
    return theme_counts, theme_examples