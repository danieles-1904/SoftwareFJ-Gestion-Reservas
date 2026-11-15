"""
Módulo de Servicios Especializados (Herencia, Polimorfismo y Sobrecarga)
Proyecto: Sistema Integral de Gestión - Software FJ
Autor: Daniel Esteban Jaramillo Ruiz
"""

from abc import abstractmethod
from modelos_base import EntidadSistema
from excepciones import DatosInvalidosError, ServicioNoDisponibleError


class Servicio(EntidadSistema):
    """Clase abstracta que modela cualquier servicio ofrecido por Software FJ."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, disponible: bool = True):
        super().__init__(id_servicio)
        if not nombre or not nombre.strip():
            raise DatosInvalidosError("El nombre del servicio no puede estar vacío.")
        if tarifa_base <= 0:
            raise DatosInvalidosError("La tarifa base del servicio debe ser mayor a cero.")

        self._nombre = nombre.strip()
        self._tarifa_base = float(tarifa_base)
        self._disponible = bool(disponible)

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def tarifa_base(self) -> float:
        return self._tarifa_base

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, estado: bool):
        self._disponible = bool(estado)

    @abstractmethod
    def validar_parametros(self, duracion: int) -> None:
        """Verifica disponibilidad y reglas particulares antes de cotizar o reservar."""
        pass

    @abstractmethod
    def calcular_costo(self, duracion: int, descuento: float = 0.0, aplicar_iva: bool = True) -> float:
        """
        Método polimórfico y con sobrecarga simulada mediante parámetros opcionales
        para calcular el valor total según el tipo de servicio.
        """
        pass

    def _aplicar_ajustes_financieros(self, subtotal: float, descuento: float, aplicar_iva: bool) -> float:
        """Aplica descuentos e IVA verificando que los porcentajes sean coherentes."""
        if descuento < 0 or descuento > 50:
            raise DatosInvalidosError("El porcentaje de descuento debe estar entre 0% y 50%.")

        total = subtotal * (1 - (descuento / 100))
        if aplicar_iva:
            total *= 1.19  # IVA del 19%
        return round(total, 2)


class ReservaSala(Servicio):
    """Servicio especializado para alquiler por horas de salas de desarrollo o juntas."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_hora: float, capacidad: int, disponible: bool = True):
        super().__init__(id_servicio, nombre, tarifa_hora, disponible)
        if capacidad <= 0:
            raise DatosInvalidosError("La capacidad de la sala debe ser de al menos 1 persona.")
        self._capacidad = int(capacidad)

    def validar_parametros(self, duracion: int) -> None:
        if not self._disponible:
            raise ServicioNoDisponibleError(f"La sala '{self._nombre}' ya se encuentra ocupada.")
        if not isinstance(duracion, int) or duracion <= 0 or duracion > 12:
            raise DatosInvalidosError("La reserva de sala debe ser entre 1 y 12 horas enteras.")

    def calcular_costo(self, duracion: int, descuento: float = 0.0, aplicar_iva: bool = True) -> float:
        self.validar_parametros(duracion)
        subtotal = self._tarifa_base * duracion
        # Si reservan más de 4 horas se aplica un recargo fijo de limpieza y soporte ($25.000)
        if duracion > 4:
            subtotal += 25000.0
        return self._aplicar_ajustes_financieros(subtotal, descuento, aplicar_iva)

    def obtener_resumen(self) -> str:
        estado = "Disponible" if self._disponible else "Ocupada"
        return f"Sala [{self.id_entidad}]: {self._nombre} | Cap: {self._capacidad} pers. | ${self._tarifa_base:,.0f}/h ({estado})"


class AlquilerEquipo(Servicio):
    """Servicio especializado para préstamo de hardware y estaciones de trabajo por días."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_dia: float, stock_disponible: int):
        super().__init__(id_servicio, nombre, tarifa_dia, disponible=(stock_disponible > 0))
        if stock_disponible < 0:
            raise DatosInvalidosError("El inventario de equipos no puede ser negativo.")
        self._stock = int(stock_disponible)

    @property
    def stock(self) -> int:
        return self._stock

    def descontar_unidad(self):
        if self._stock <= 0:
            raise ServicioNoDisponibleError(f"No quedan unidades disponibles de '{self._nombre}'.")
        self._stock -= 1
        self._disponible = self._stock > 0

    def liberar_unidad(self):
        self._stock += 1
        self._disponible = True

    def validar_parametros(self, duracion: int) -> None:
        if self._stock <= 0 or not self._disponible:
            raise ServicioNoDisponibleError(f"El equipo '{self._nombre}' está agotado en inventario.")
        if not isinstance(duracion, int) or duracion <= 0 or duracion > 30:
            raise DatosInvalidosError("El alquiler de equipos debe ser entre 1 y 30 días.")

    def calcular_costo(self, duracion: int, descuento: float = 0.0, aplicar_iva: bool = True) -> float:
        self.validar_parametros(duracion)
        # Seguro obligatorio del 5% sobre el valor base del alquiler
        subtotal = (self._tarifa_base * duracion) * 1.05
        return self._aplicar_ajustes_financieros(subtotal, descuento, aplicar_iva)

    def obtener_resumen(self) -> str:
        return f"Equipo [{self.id_entidad}]: {self._nombre} | Stock: {self._stock} unid. | ${self._tarifa_base:,.0f}/día"


class AsesoriaEspecializada(Servicio):
    """Servicio especializado para consultoría técnica en arquitectura y desarrollo."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_hora: float, especialidad: str, disponible: bool = True):
        super().__init__(id_servicio, nombre, tarifa_hora, disponible)
        if not especialidad or not especialidad.strip():
            raise DatosInvalidosError("Debe especificar el área de especialidad de la asesoría.")
        self._especialidad = especialidad.strip()

    def validar_parametros(self, duracion: int) -> None:
        if not self._disponible:
            raise ServicioNoDisponibleError(f"El consultor de '{self._especialidad}' no tiene agenda abierta.")
        if not isinstance(duracion, int) or duracion < 2 or duracion > 8:
            raise DatosInvalidosError("Las asesorías requieren mínimo 2 horas y máximo 8 horas por sesión.")

    def calcular_costo(self, duracion: int, descuento: float = 0.0, aplicar_iva: bool = True) -> float:
        self.validar_parametros(duracion)
        subtotal = self._tarifa_base * duracion
        return self._aplicar_ajustes_financieros(subtotal, descuento, aplicar_iva)

    def obtener_resumen(self) -> str:
        estado = "Agenda abierta" if self._disponible else "Sin cupo"
        return f"Asesoría [{self.id_entidad}]: {self._nombre} ({self._especialidad}) | ${self._tarifa_base:,.0f}/h ({estado})"