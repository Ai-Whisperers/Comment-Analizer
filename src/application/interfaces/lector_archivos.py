"""
Interface para lectura de archivos
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any


class ILectorArchivos(ABC):
    """
    Interface para lectura de diferentes tipos de archivos
    """
    
    @abstractmethod
    def leer_comentarios(self, archivo) -> List[Dict[str, Any]]:
        """
        Lee comentarios desde un archivo y retorna una lista de diccionarios
        con los datos extraídos
        """
        pass
    
    @abstractmethod
    def es_formato_soportado(self, nombre_archivo: str) -> bool:
        """
        Verifica si el formato del archivo es soportado
        """
        pass
    
    @abstractmethod
    def obtener_metadatos_archivo(self, archivo) -> Dict[str, Any]:
        """
        Obtiene metadatos del archivo (tamaño, tipo, etc.)
        """
        pass