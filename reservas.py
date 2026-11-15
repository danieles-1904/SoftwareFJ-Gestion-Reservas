"""
Nombre del Estudiante: Daniel Esteban Jaramillo Ruiz
Programa: Ingeniería de Sistemas
Código Fuente: Autoría Propia
Fase 4 - Sistema Integral de Gestión de Reservas (Software FJ)
"""

from modelos_base import EntidadSistema, Cliente
from servicios import Servicio, AlquilerEquipo
from excepciones import (
    DatosInvalidosError,
    ServicioNoDisponibleError,
    ReservaInvalidaError,
    OperacionNoPermitidaError,
)
from logger_config import configurar_logger

logger = configurar_logger()


class Reserva(EntidadSistema):
    """Conecta a un cliente con un servicio y controla los cambios de estado de la solicitud."""

    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio, duracion: int):
        super().__init__(id_reserva)

        if not isinstance(cliente, Cliente):
            raise DatosInvalidosError("La reserva requiere una instancia válida de Cliente.")
        if not isinstance(servicio, Servicio):
            raise DatosInvalidosError("La reserva requiere una instancia válida de Servicio.")
        if not isinstance(duracion, int) or duracion <= 0:
            raise DatosInvalidosError("La duración de la reserva debe ser un número entero mayor a cero.")

        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._estado = "PENDIENTE"
        self._costo_total = 0.0

    @property
    def cliente(self) -> Cliente:
        return self._cliente

    @property
    def servicio(self) -> Servicio:
        return self._servicio

    @property
    def duracion(self) -> int:
        return self._duracion

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def costo_total(self) -> float:
        return self._costo_total

    def calcular_total(
        self,
        descuento: float = 0.0,
        aplicar_iva: bool = True,
        recargo_urgencia: float = 0.0
    ) -> float:
        """Cotiza el valor de la reserva permitiendo sumar un recargo por atención urgente."""
        if recargo_urgencia < 0:
            raise DatosInvalidosError("El recargo por urgencia no puede ser un valor negativo.")

        valor_base = self._servicio.calcular_costo(
            duracion=self._duracion,
            descuento=descuento,
            aplicar_iva=aplicar_iva
        )
        return round(valor_base + recargo_urgencia, 2)

    def confirmar(self, descuento: float = 0.0, aplicar_iva: bool = True, recargo_urgencia: float = 0.0) -> None:
        """Valida cupo, liquida el costo total y deja la reserva en estado CONFIRMADA."""
        logger.info(f"Iniciando confirmación para reserva {self.id_entidad}...")
        try:
            if self._estado != "PENDIENTE":
                raise ReservaInvalidaError(
                    f"No se puede confirmar la reserva {self.id_entidad} porque su estado actual es '{self._estado}'."
                )

            total = self.calcular_total(descuento, aplicar_iva, recargo_urgencia)

            # Descuenta inventario si es un equipo o marca ocupada la sala/asesoría
            if isinstance(self._servicio, AlquilerEquipo):
                self._servicio.descontar_unidad()
            else:
                self._servicio.disponible = False

        except (ServicioNoDisponibleError, DatosInvalidosError) as error_origen:
            # Encadena la excepción original para no perder el motivo exacto del rechazo
            raise ReservaInvalidaError(
                f"Fallo al confirmar reserva {self.id_entidad} para '{self._servicio.nombre}'."
            ) from error_origen
        else:
            self._costo_total = total
            self._estado = "CONFIRMADA"
            logger.info(
                f"Reserva {self.id_entidad} CONFIRMADA | Cliente: {self._cliente.nombre} | "
                f"Servicio: {self._servicio.nombre} | Total: ${self._costo_total:,.2f}"
            )
        finally:
            logger.info(f"Cierre de validación en {self.id_entidad} con estado: {self._estado}")

    def procesar(self) -> None:
        """Marca una reserva confirmada como ejecutada y libera la agenda del servicio."""
        try:
            if self._estado != "CONFIRMADA":
                raise OperacionNoPermitidaError(
                    f"Solo se pueden procesar reservas en estado CONFIRMADA (estado actual: '{self._estado}')."
                )
        except OperacionNoPermitidaError:
            raise
        else:
            self._estado = "PROCESADA"
            if not isinstance(self._servicio, AlquilerEquipo):
                self._servicio.disponible = True
            logger.info(f"Reserva {self.id_entidad} PROCESADA exitosamente.")

    def cancelar(self) -> None:
        """Anula una reserva activa y devuelve el recurso o unidad al inventario."""
        try:
            if self._estado in ("CANCELADA", "PROCESADA"):
                raise ReservaInvalidaError(
                    f"Imposible cancelar la reserva {self.id_entidad}: ya se encuentra '{self._estado}'."
                )

            estado_anterior = self._estado

            if estado_anterior == "CONFIRMADA":
                if isinstance(self._servicio, AlquilerEquipo):
                    self._servicio.liberar_unidad()
                else:
                    self._servicio.disponible = True

        except ReservaInvalidaError:
            raise
        else:
            self._estado = "CANCELADA"
            logger.info(f"Reserva {self.id_entidad} CANCELADA (provenía de estado '{estado_anterior}').")
        finally:
            logger.info(f"Revisión de liberación de recursos lista para {self.id_entidad}.")

    def obtener_resumen(self) -> str:
        return (
            f"Reserva [{self.id_entidad}] | Estado: {self._estado} | Cliente: {self._cliente.nombre} | "
            f"Servicio: {self._servicio.nombre} ({self._duracion} u.) | Total: ${self._costo_total:,.2f}"
        )