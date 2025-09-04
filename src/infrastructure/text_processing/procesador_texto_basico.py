"""
Implementación básica del procesador de texto
"""
import re
from typing import List, Dict
from collections import defaultdict
import logging

from ...domain.entities.comentario import Comentario
from ...application.interfaces.procesador_texto import IProcesadorTexto


logger = logging.getLogger(__name__)


class ProcesadorTextoBasico(IProcesadorTexto):
    """
    Implementación básica de procesamiento de texto con funcionalidades esenciales
    """
    
    def __init__(self):
        self._inicializar_patrones()
    
    def limpiar_texto(self, texto: str) -> str:
        """
        Limpia y normaliza un texto
        """
        if not texto:
            return ""
        
        # Convertir a string si no lo es
        texto = str(texto).strip()
        
        # Remover caracteres especiales pero mantener acentos y ñ
        texto = re.sub(r'[^\w\sáéíóúñüÁÉÍÓÚÑÜ]', ' ', texto)
        
        # Normalizar espacios múltiples
        texto = re.sub(r'\s+', ' ', texto)
        
        # Remover espacios al inicio y final
        texto = texto.strip()
        
        # Convertir a minúsculas para procesamiento
        return texto.lower()
    
    def consolidar_duplicados(self, comentarios: List[Comentario]) -> List[Comentario]:
        """
        Consolida comentarios duplicados sumando sus frecuencias
        """
        if not comentarios:
            return []
        
        # Agrupar por texto limpio
        grupos_texto = defaultdict(list)
        
        for comentario in comentarios:
            clave_agrupacion = self._generar_clave_agrupacion(comentario.texto_limpio)
            grupos_texto[clave_agrupacion].append(comentario)
        
        comentarios_consolidados = []
        duplicados_removidos = 0
        
        for grupo in grupos_texto.values():
            if len(grupo) == 1:
                # No hay duplicados
                comentarios_consolidados.append(grupo[0])
            else:
                # Consolidar duplicados
                comentario_consolidado = self._consolidar_grupo(grupo)
                comentarios_consolidados.append(comentario_consolidado)
                duplicados_removidos += len(grupo) - 1
        
        logger.info(f"🔄 Consolidación: {len(comentarios)} → {len(comentarios_consolidados)} "
                   f"({duplicados_removidos} duplicados removidos)")
        
        return comentarios_consolidados
    
    def detectar_idioma(self, texto: str) -> str:
        """
        Detecta el idioma del texto (implementación básica)
        """
        if not texto:
            return "desconocido"
        
        texto_limpio = self.limpiar_texto(texto)
        palabras = texto_limpio.split()
        
        if not palabras:
            return "desconocido"
        
        # Contadores para diferentes idiomas
        indicadores_espanol = 0
        indicadores_guarani = 0
        indicadores_ingles = 0
        
        # Palabras indicadoras de español
        palabras_espanol = {
            'el', 'la', 'los', 'las', 'de', 'del', 'que', 'en', 'un', 'una',
            'por', 'con', 'para', 'es', 'muy', 'pero', 'cuando', 'como',
            'servicio', 'internet', 'problema', 'bueno', 'malo'
        }
        
        # Palabras indicadoras de guaraní
        palabras_guarani = {
            'che', 'nde', 'ha', 'pe', 'ko', 'rehe', 'gui', 'me', 'piko',
            'ñandu', 'mba\'eiko', 'aipo', 'upei', 'aníke'
        }
        
        # Palabras indicadoras de inglés
        palabras_ingles = {
            'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'with', 'by', 'from', 'is', 'are', 'was', 'were', 'have', 'has'
        }
        
        # Contar indicadores
        for palabra in palabras:
            if palabra in palabras_espanol:
                indicadores_espanol += 1
            elif palabra in palabras_guarani:
                indicadores_guarani += 1
            elif palabra in palabras_ingles:
                indicadores_ingles += 1
        
        # Determinar idioma predominante
        max_indicadores = max(indicadores_espanol, indicadores_guarani, indicadores_ingles)
        
        if max_indicadores == 0:
            return "desconocido"
        elif indicadores_espanol == max_indicadores:
            return "es"
        elif indicadores_guarani == max_indicadores:
            return "gn"
        elif indicadores_ingles == max_indicadores:
            return "en"
        else:
            return "es"  # Fallback a español
    
    def _inicializar_patrones(self):
        """
        Inicializa patrones de expresiones regulares útiles
        """
        self.patron_email = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        self.patron_telefono = re.compile(r'\b\d{3,4}[-\s]?\d{3,4}[-\s]?\d{3,4}\b')
        self.patron_urls = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    
    def _generar_clave_agrupacion(self, texto_limpio: str) -> str:
        """
        Genera una clave para agrupar textos similares
        """
        if not texto_limpio:
            return ""
        
        # Remover palabras muy comunes que no aportan significado
        palabras_vacias = {
            'el', 'la', 'los', 'las', 'un', 'una', 'de', 'del', 'que', 
            'en', 'y', 'a', 'con', 'por', 'para', 'es', 'son', 'está',
            'muy', 'más', 'pero', 'si', 'no', 'me', 'te', 'se'
        }
        
        palabras = [p for p in texto_limpio.split() if p not in palabras_vacias]
        
        # Ordenar palabras para que textos con mismo contenido pero diferente orden se agrupen
        palabras_ordenadas = sorted(palabras)
        
        # Crear clave única
        return ' '.join(palabras_ordenadas)
    
    def _consolidar_grupo(self, comentarios_grupo: List[Comentario]) -> Comentario:
        """
        Consolida un grupo de comentarios similares
        """
        # Usar el primer comentario como base
        comentario_base = comentarios_grupo[0]
        
        # Sumar frecuencias
        frecuencia_total = sum(c.frecuencia for c in comentarios_grupo)
        
        # Usar el texto original más representativo (el más largo)
        texto_mas_representativo = max(
            comentarios_grupo, 
            key=lambda c: len(c.texto)
        ).texto
        
        # Crear nuevo comentario consolidado
        comentario_consolidado = Comentario(
            id=f"{comentario_base.id}_consolidado",
            texto=texto_mas_representativo,
            texto_limpio=comentario_base.texto_limpio,
            frecuencia=frecuencia_total,
            fecha_analisis=comentario_base.fecha_analisis,
            # Mantener otros atributos del comentario base
            calificacion_nps=comentario_base.calificacion_nps,
            calificacion_nota=comentario_base.calificacion_nota
        )
        
        return comentario_consolidado
    
    def remover_informacion_personal(self, texto: str) -> str:
        """
        Remueve información personal del texto (emails, teléfonos, etc.)
        """
        # Remover emails
        texto = self.patron_email.sub('[EMAIL]', texto)
        
        # Remover teléfonos
        texto = self.patron_telefono.sub('[TELEFONO]', texto)
        
        # Remover URLs
        texto = self.patron_urls.sub('[URL]', texto)
        
        return texto
    
    def obtener_estadisticas_texto(self, comentarios: List[Comentario]) -> Dict[str, any]:
        """
        Obtiene estadísticas sobre los textos procesados
        """
        if not comentarios:
            return {
                'total_comentarios': 0,
                'longitud_promedio': 0,
                'idiomas_detectados': {},
                'palabras_totales': 0
            }
        
        longitudes = [len(c.texto) for c in comentarios]
        idiomas = [self.detectar_idioma(c.texto) for c in comentarios]
        palabras_totales = sum(len(c.texto_limpio.split()) for c in comentarios)
        
        from collections import Counter
        distribucion_idiomas = Counter(idiomas)
        
        return {
            'total_comentarios': len(comentarios),
            'longitud_promedio': sum(longitudes) / len(longitudes),
            'longitud_minima': min(longitudes),
            'longitud_maxima': max(longitudes),
            'idiomas_detectados': dict(distribucion_idiomas),
            'palabras_totales': palabras_totales,
            'palabras_promedio': palabras_totales / len(comentarios)
        }