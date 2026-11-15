"""
Nombre del Estudiante: Daniel Esteban Jaramillo Ruiz
Programa: Ingeniería de Sistemas
Código Fuente: Autoría Propia
Fase 4 - Sistema Integral de Gestión de Reservas (Software FJ)
"""


class ErrorSoftwareFJ(Exception):
    """Clase base para cualquier error propio de la aplicación."""
    def __init__(self, mensaje="Ocurrió un error general en el sistema de Software FJ."):
        self.mensaje = mensaje
        super().__init__(self.mensaje)


class DatosInvalidosError(ErrorSoftwareFJ):
    """Salta cuando llegan datos vacíos, negativos, en cero o mal escritos."""
    def __init__(self, mensaje="Los datos ingresados no son válidos o están fuera de rango."):
        super().__init__(mensaje)


class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """Salta cuando una sala, equipo o asesor no tiene cupo disponible."""
    def __init__(self, mensaje="El servicio solicitado no se encuentra disponible en este momento."):
        super().__init__(mensaje)


class ReservaInvalidaError(ErrorSoftwareFJ):
    """Salta al intentar confirmar, cancelar o crear una reserva en un estado que no corresponde."""
    def __init__(self, mensaje="La operación sobre la reserva no es válida."):
        super().__init__(mensaje)


class OperacionNoPermitidaError(ErrorSoftwareFJ):
    """Salta cuando una acción va en contra de las reglas de negocio definidas."""
    def __init__(self, mensaje="Esta operación no está permitida por las políticas del sistema."):
        super().__init__(mensaje)