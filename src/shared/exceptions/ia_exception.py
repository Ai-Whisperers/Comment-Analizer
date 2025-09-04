"""
Excepción específica para errores de IA
"""


class IAException(Exception):
    """
    Excepción lanzada cuando hay errores relacionados con servicios de IA
    """
    
    def __init__(self, mensaje: str, servicio: str = None, codigo_error: str = None):
        super().__init__(mensaje)
        self.servicio = servicio
        self.codigo_error = codigo_error
    
    def __str__(self):
        base_msg = super().__str__()
        if self.servicio:
            base_msg = f"[{self.servicio}] {base_msg}"
        if self.codigo_error:
            base_msg += f" (Código: {self.codigo_error})"
        return base_msg