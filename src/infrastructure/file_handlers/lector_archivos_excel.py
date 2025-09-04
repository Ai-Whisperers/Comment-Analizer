"""
Implementación de lector de archivos Excel/CSV
"""
import pandas as pd
from typing import List, Dict, Any
from io import BytesIO
import logging

from ...application.interfaces.lector_archivos import ILectorArchivos
from ...shared.exceptions.archivo_exception import ArchivoException


logger = logging.getLogger(__name__)


class LectorArchivosExcel(ILectorArchivos):
    """
    Implementación concreta para leer archivos Excel y CSV
    """
    
    def __init__(self):
        self.formatos_soportados = ['.xlsx', '.xls', '.csv']
        self.columnas_comentario = [
            'comentario final', 'comment', 'comments', 'feedback', 
            'review', 'texto', 'comentario', 'comentarios', 
            'respuesta', 'opinion', 'observacion'
        ]
    
    def leer_comentarios(self, archivo) -> List[Dict[str, Any]]:
        """
        Lee comentarios desde archivo Excel/CSV
        """
        try:
            # Leer el archivo
            df = self._leer_dataframe(archivo)
            
            if df.empty:
                raise ArchivoException("El archivo está vacío")
            
            # Encontrar columna de comentarios
            columna_comentario = self._encontrar_columna_comentario(df)
            
            if not columna_comentario:
                raise ArchivoException("No se encontró una columna de comentarios válida")
            
            # Procesar datos
            comentarios = self._extraer_comentarios(df, columna_comentario)
            
            logger.info(f"Leídos {len(comentarios)} comentarios desde {getattr(archivo, 'name', 'archivo')}")
            
            return comentarios
            
        except Exception as e:
            logger.error(f"Error leyendo archivo: {str(e)}")
            raise ArchivoException(f"Error procesando archivo: {str(e)}")
    
    def es_formato_soportado(self, nombre_archivo: str) -> bool:
        """
        Verifica si el formato es soportado
        """
        return any(nombre_archivo.lower().endswith(fmt) for fmt in self.formatos_soportados)
    
    def obtener_metadatos_archivo(self, archivo) -> Dict[str, Any]:
        """
        Obtiene metadatos del archivo
        """
        try:
            return {
                'nombre': getattr(archivo, 'name', 'desconocido'),
                'tamaño': getattr(archivo, 'size', 0),
                'tipo': getattr(archivo, 'type', 'desconocido')
            }
        except:
            return {
                'nombre': 'desconocido',
                'tamaño': 0,
                'tipo': 'desconocido'
            }
    
    def _leer_dataframe(self, archivo) -> pd.DataFrame:
        """
        Lee el archivo y retorna un DataFrame
        """
        try:
            # Determinar tipo de archivo
            nombre_archivo = getattr(archivo, 'name', '')
            
            if nombre_archivo.lower().endswith('.csv'):
                return self._leer_csv(archivo)
            else:
                return self._leer_excel(archivo)
                
        except Exception as e:
            raise ArchivoException(f"Error leyendo archivo: {str(e)}")
    
    def _leer_csv(self, archivo) -> pd.DataFrame:
        """
        Lee archivo CSV con manejo de errores
        """
        if hasattr(archivo, 'read'):
            archivo.seek(0)
            return pd.read_csv(archivo, encoding='utf-8', errors='ignore')
        else:
            return pd.read_csv(BytesIO(archivo.content), encoding='utf-8', errors='ignore')
    
    def _leer_excel(self, archivo) -> pd.DataFrame:
        """
        Lee archivo Excel con manejo de recursos
        """
        if hasattr(archivo, 'read'):
            archivo.seek(0)
            with BytesIO(archivo.read()) as buffer:
                return pd.read_excel(buffer, engine='openpyxl')
        else:
            with BytesIO(archivo.content) as buffer:
                return pd.read_excel(buffer, engine='openpyxl')
    
    def _encontrar_columna_comentario(self, df: pd.DataFrame) -> str:
        """
        Encuentra la columna que contiene comentarios
        """
        # Buscar por nombres exactos o que contengan las palabras clave
        for col in df.columns:
            col_lower = str(col).lower()
            if any(nombre in col_lower for nombre in self.columnas_comentario):
                return col
        
        # Fallback: primera columna de tipo texto
        for col in df.columns:
            if df[col].dtype == 'object' and not df[col].dropna().empty:
                return col
        
        return None
    
    def _extraer_comentarios(self, df: pd.DataFrame, columna_comentario: str) -> List[Dict[str, Any]]:
        """
        Extrae y procesa los comentarios del DataFrame
        """
        comentarios = []
        
        for index, row in df.iterrows():
            comentario_texto = str(row[columna_comentario]).strip()
            
            # Filtrar comentarios vacíos o inválidos
            if not comentario_texto or comentario_texto.lower() in ['nan', 'none', '']:
                continue
            
            # Crear diccionario con datos del comentario
            comentario_data = {
                'comentario': comentario_texto,
                'indice_original': index
            }
            
            # Agregar campos adicionales si existen
            if 'NPS' in df.columns:
                nps_value = row.get('NPS')
                if pd.notna(nps_value):
                    try:
                        comentario_data['nps'] = int(float(nps_value))
                    except (ValueError, TypeError):
                        pass
            
            if 'Nota' in df.columns:
                nota_value = row.get('Nota')
                if pd.notna(nota_value):
                    try:
                        comentario_data['nota'] = float(nota_value)
                    except (ValueError, TypeError):
                        pass
            
            comentarios.append(comentario_data)
        
        return comentarios