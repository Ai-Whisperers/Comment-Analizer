"""
Excepción específica para errores de archivo
"""


class ArchivoException(Exception):
    """
    Excepción lanzada cuando hay errores relacionados con archivos
    """
    
    def __init__(self, mensaje: str, archivo: str = None):
        super().__init__(mensaje)
        self.archivo = archivo
    
    def __str__(self):
        if self.archivo:
            return f"Error en archivo '{self.archivo}': {super().__str__()}"
        return super().__str__()