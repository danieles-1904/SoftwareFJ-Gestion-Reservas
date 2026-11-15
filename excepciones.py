"""
Módulo de Excepciones Personalizadas
Proyecto: Sistema Integral de Gestión - Software FJ
Autor: Daniel Esteban Jaramillo Ruiz
"""


class ErrorSoftwareFJ(Exception):
    """Excepción base de la cual heredan todos los errores propios del sistema."""
    def __init__(self, mensaje="Ocurrió un error general en el sistema de Software FJ."):
        self.mensaje = mensaje
        super().__init__(self.mensaje)


class DatosInvalidosError(ErrorSoftwareFJ):
    """Se lanza cuando ingresan valores vacíos, negativos, en cero o con formato incorrecto."""
    def __init__(self, mensaje="Los datos ingresados no son válidos o están fuera de rango."):
        super().__init__(mensaje)


class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """Se lanza cuando una sala, equipo o asesor no tiene cupo o está ocupado."""
    def __init__(self, mensaje="El servicio solicitado no se encuentra disponible en este momento."):
        super().__init__(mensaje)


class ReservaInvalidaError(ErrorSoftwareFJ):
    """Se lanza cuando se intenta confirmar, cancelar o crear una reserva en un estado incoherente."""
    def __init__(self, mensaje="La operación sobre la reserva no es válida."):
        super().__init__(mensaje)


class OperacionNoPermitidaError(ErrorSoftwareFJ):
    """Se lanza cuando se viola una regla de negocio de la empresa."""
    def __init__(self, mensaje="Esta operación no está permitida por las políticas del sistema."):
        super().__init__(mensaje)