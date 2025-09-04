"""
Detector de temas híbrido que combina IA y reglas
"""
import re
from typing import List, Dict, Set
import logging

from ...application.interfaces.detector_temas import IDetectorTemas
from ...application.dtos.temas_detectados import TemasDetectados
from ..external_services.analizador_openai import AnalizadorOpenAI


logger = logging.getLogger(__name__)


class DetectorTemasHibrido(IDetectorTemas):
    """
    Detector de temas que combina análisis con IA y reglas predefinidas
    """
    
    def __init__(self, openai_api_key: str = None):
        self.openai_disponible = False
        self.analizador_ia = None
        
        # Inicializar IA si está disponible
        if openai_api_key:
            try:
                self.analizador_ia = AnalizadorOpenAI(openai_api_key)
                self.openai_disponible = self.analizador_ia.es_disponible()
                logger.info("🤖 Detector de temas con IA inicializado")
            except Exception as e:
                logger.warning(f"⚠️ No se pudo inicializar IA para temas: {str(e)}")
        
        # Inicializar diccionarios de reglas
        self._inicializar_diccionarios()
        logger.info("📝 Detector de temas con reglas inicializado")
    
    def detectar_temas(self, texto: str) -> TemasDetectados:
        """
        Detecta temas usando IA si está disponible, sino usa reglas
        """
        if self.openai_disponible:
            return self._detectar_con_ia(texto)
        else:
            return self._detectar_con_reglas(texto)
    
    def detectar_temas_lote(self, textos: List[str]) -> List[TemasDetectados]:
        """
        Detecta temas para múltiples textos
        """
        if self.openai_disponible:
            return self._detectar_lote_con_ia(textos)
        else:
            return [self._detectar_con_reglas(texto) for texto in textos]
    
    def _detectar_con_ia(self, texto: str) -> TemasDetectados:
        """
        Detecta temas usando IA (OpenAI)
        """
        try:
            # Usar el analizador OpenAI para obtener temas
            # Nota: Esto requeriría una extensión del AnalizadorOpenAI para temas
            # Por ahora, usamos fallback a reglas
            logger.debug("🤖 Usando análisis IA para temas (fallback a reglas)")
            return self._detectar_con_reglas(texto)
            
        except Exception as e:
            logger.error(f"Error en análisis IA de temas: {str(e)}")
            return self._detectar_con_reglas(texto)
    
    def _detectar_lote_con_ia(self, textos: List[str]) -> List[TemasDetectados]:
        """
        Detecta temas para múltiples textos usando IA
        """
        # Por ahora usar fallback individual
        return [self._detectar_con_ia(texto) for texto in textos]
    
    def _detectar_con_reglas(self, texto: str) -> TemasDetectados:
        """
        Detecta temas usando reglas predefinidas
        """
        if not texto:
            return TemasDetectados([], [], [], [], 0.0, "reglas")
        
        texto_lower = texto.lower()
        
        # Detectar temas principales
        temas = self._detectar_temas_principales(texto_lower)
        
        # Detectar puntos de dolor
        puntos_dolor = self._detectar_puntos_dolor(texto_lower)
        
        # Detectar emociones
        emociones = self._detectar_emociones(texto_lower)
        
        # Detectar competidores
        competidores = self._detectar_competidores(texto_lower)
        
        # Calcular confianza basada en cantidad de indicadores encontrados
        total_indicadores = len(temas) + len(puntos_dolor) + len(emociones) + len(competidores)
        confianza = min(0.85, 0.4 + (total_indicadores * 0.1))
        
        return TemasDetectados(
            temas_principales=temas,
            puntos_dolor=puntos_dolor,
            emociones_detectadas=emociones,
            competidores_mencionados=competidores,
            confianza=confianza,
            metodo_deteccion="reglas"
        )
    
    def _inicializar_diccionarios(self):
        """
        Inicializa los diccionarios de patrones para detección por reglas
        """
        # Temas principales de telecomunicaciones
        self.patrones_temas = {
            'velocidad': [
                'lent', 'rapid', 'velocidad', 'conexion', 'banda', 'megas',
                'mbps', 'internet', 'navegacion', 'descarga', 'subida'
            ],
            'precio': [
                'caro', 'barato', 'precio', 'cost', 'pago', 'factura',
                'cobr', 'promocion', 'descuento', 'oferta', 'plan'
            ],
            'servicio_cliente': [
                'atencion', 'servicio', 'personal', 'amable', 'cordial',
                'ayuda', 'soporte', 'tecnico', 'call center', 'consulta'
            ],
            'calidad_servicio': [
                'calidad', 'funcionamiento', 'estabilidad', 'confiable',
                'consistente', 'interrupcion', 'corte', 'falla'
            ],
            'cobertura': [
                'cobertura', 'señal', 'zona', 'area', 'region',
                'disponibilidad', 'alcance', 'fibra', 'cable'
            ],
            'instalacion': [
                'instalacion', 'tecnico', 'visita', 'programar',
                'conectar', 'configurar', 'equipo', 'modem', 'router'
            ],
            'facturacion': [
                'factura', 'cobro', 'pago', 'cargo', 'debito',
                'cuenta', 'saldo', 'promocion', 'contrato'
            ]
        }
        
        # Puntos de dolor específicos
        self.patrones_dolor = {
            'sin_servicio': [
                'sin internet', 'no funciona', 'cortado', 'caido',
                'desconectado', 'no hay servicio', 'sin conexion'
            ],
            'servicio_lento': [
                'muy lento', 'lentisimo', 'demora', 'tarda',
                'no carga', 'se traba', 'se cuelga'
            ],
            'mal_servicio_cliente': [
                'mal servicio', 'mala atencion', 'no resuelven',
                'no ayudan', 'incompetente', 'desorganizados'
            ],
            'problemas_tecnicos': [
                'problema tecnico', 'error', 'falla', 'defecto',
                'no anda', 'se apaga', 'se reinicia'
            ],
            'cobros_incorrectos': [
                'cobro mal', 'factura incorrecta', 'cargo extra',
                'no corresponde', 'descuento no aplicado'
            ]
        }
        
        # Emociones detectables
        self.patrones_emociones = {
            'frustracion': [
                'frustrado', 'cansado', 'harto', 'desesperado',
                'no aguanto', 'ya no mas', 'basta'
            ],
            'enojo': [
                'enojado', 'molesto', 'furioso', 'indignado',
                'bronca', 'rabia', 'ira', 'odio'
            ],
            'satisfaccion': [
                'satisfecho', 'contento', 'feliz', 'encantado',
                'complacido', 'agradecido', 'conforme'
            ],
            'decepcion': [
                'decepcionado', 'decepcion', 'esperaba mas',
                'no es lo que', 'no cumple', 'fallido'
            ],
            'preocupacion': [
                'preocupado', 'inquieto', 'nervioso', 'ansioso',
                'temor', 'miedo', 'dudas'
            ]
        }
        
        # Competidores
        self.competidores_conocidos = {
            'tigo', 'claro', 'copaco', 'vox', 'telecel',
            'personal', 'movistar', 'entel'
        }
    
    def _detectar_temas_principales(self, texto: str) -> List[str]:
        """
        Detecta los temas principales en el texto
        """
        temas_encontrados = []
        
        for tema, patrones in self.patrones_temas.items():
            if any(patron in texto for patron in patrones):
                temas_encontrados.append(tema)
        
        return temas_encontrados[:5]  # Máximo 5 temas principales
    
    def _detectar_puntos_dolor(self, texto: str) -> List[str]:
        """
        Detecta puntos de dolor específicos
        """
        dolores_encontrados = []
        
        for dolor, patrones in self.patrones_dolor.items():
            if any(patron in texto for patron in patrones):
                dolores_encontrados.append(dolor.replace('_', ' '))
        
        return dolores_encontrados
    
    def _detectar_emociones(self, texto: str) -> List[str]:
        """
        Detecta emociones en el texto
        """
        emociones_encontradas = []
        
        for emocion, patrones in self.patrones_emociones.items():
            if any(patron in texto for patron in patrones):
                emociones_encontradas.append(emocion)
        
        return emociones_encontradas
    
    def _detectar_competidores(self, texto: str) -> List[str]:
        """
        Detecta menciones de competidores
        """
        competidores_encontrados = []
        
        for competidor in self.competidores_conocidos:
            if competidor in texto:
                competidores_encontrados.append(competidor)
        
        return competidores_encontrados
    
    def obtener_estadisticas_deteccion(self, resultados: List[TemasDetectados]) -> Dict[str, any]:
        """
        Obtiene estadísticas sobre la detección de temas
        """
        if not resultados:
            return {}
        
        # Contar temas más comunes
        from collections import Counter
        
        todos_los_temas = []
        todos_los_dolores = []
        todas_las_emociones = []
        
        for resultado in resultados:
            todos_los_temas.extend(resultado.temas_principales)
            todos_los_dolores.extend(resultado.puntos_dolor)
            todas_las_emociones.extend(resultado.emociones_detectadas)
        
        return {
            'total_analisis': len(resultados),
            'temas_mas_comunes': dict(Counter(todos_los_temas).most_common(10)),
            'dolores_mas_comunes': dict(Counter(todos_los_dolores).most_common(10)),
            'emociones_mas_comunes': dict(Counter(todas_las_emociones).most_common(5)),
            'confianza_promedio': sum(r.confianza for r in resultados) / len(resultados),
            'metodo_predominante': Counter(r.metodo_deteccion for r in resultados).most_common(1)[0][0]
        }