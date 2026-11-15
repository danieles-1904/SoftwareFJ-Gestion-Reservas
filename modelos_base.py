"""
Módulo de Entidades Base y Gestión de Clientes
Proyecto: Sistema Integral de Gestión - Software FJ
Autor: Daniel Esteban Jaramillo Ruiz
"""

from abc import ABC, abstractmethod
from excepciones import DatosInvalidosError


class EntidadSistema(ABC):
    """Clase abstracta base que define la estructura común de las entidades en Software FJ."""

    def __init__(self, id_entidad: str):
        if not id_entidad or not str(id_entidad).strip():
            raise DatosInvalidosError("El identificador de la entidad no puede estar vacío.")
        self._id_entidad = str(id_entidad).strip()

    @property
    def id_entidad(self) -> str:
        return self._id_entidad

    @abstractmethod
    def obtener_resumen(self) -> str:
        """Método obligatorio que cada clase hija debe implementar para describirse."""
        pass


class Cliente(EntidadSistema):
    """Representa un cliente de Software FJ con encapsulación y validación de datos personales."""

    def __init__(self, id_cliente: str, nombre: str, correo: str, telefono: str):
        super().__init__(id_cliente)
        # Usamos los setters para aplicar todas las validaciones desde la creación
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor or len(valor.strip()) < 3:
            raise DatosInvalidosError("El nombre del cliente debe tener al menos 3 caracteres.")
        self.__nombre = valor.strip()

    @property
    def correo(self) -> str:
        return self.__correo

    @correo.setter
    def correo(self, valor: str):
        if not valor or "@" not in valor or "." not in valor.split("@")[-1]:
            raise DatosInvalidosError(f"El correo '{valor}' no tiene un formato válido.")
        self.__correo = valor.strip().lower()

    @property
    def telefono(self) -> str:
        return self.__telefono

    @telefono.setter
    def telefono(self, valor: str):
        limpio = str(valor).strip()
        if not limpio.isdigit() or len(limpio) < 7:
            raise DatosInvalidosError("El teléfono debe contener solo números y mínimo 7 dígitos.")
        self.__telefono = limpio

    def obtener_resumen(self) -> str:
        return f"Cliente [{self.id_entidad}]: {self.__nombre} | Correo: {self.__correo} | Tel: {self.__telefono}"