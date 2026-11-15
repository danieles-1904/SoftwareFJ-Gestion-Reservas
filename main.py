"""
Nombre del Estudiante: Daniel Esteban Jaramillo Ruiz
Programa: Ingeniería de Sistemas
Código Fuente: Autoría Propia
Fase 4 - Sistema Integral de Gestión de Reservas (Software FJ)
"""

from modelos_base import Cliente
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from reservas import Reserva
from excepciones import ErrorSoftwareFJ
from logger_config import configurar_logger

logger = configurar_logger()


class SistemaSoftwareFJ:
    """Agrupa las listas en memoria y centraliza el registro de operaciones."""

    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []

    def registrar_cliente(self, id_cliente: str, nombre: str, correo: str, telefono: str):
        try:
            nuevo_cliente = Cliente(id_cliente, nombre, correo, telefono)
            self.clientes.append(nuevo_cliente)
            logger.info(f"Cliente registrado: {nuevo_cliente.obtener_resumen()}")
            print(f"[OK] {nuevo_cliente.obtener_resumen()}")
            return nuevo_cliente
        except ErrorSoftwareFJ as e:
            logger.error(f"Error al registrar cliente [{id_cliente}]: {e}")
            print(f"[ERROR CONTROLADO] Registro de cliente fallido: {e}")
            return None

    def registrar_servicio(self, servicio):
        self.servicios.append(servicio)
        logger.info(f"Servicio habilitado: {servicio.obtener_resumen()}")
        print(f"[OK] {servicio.obtener_resumen()}")
        return servicio

    def crear_y_confirmar_reserva(
        self,
        id_reserva: str,
        cliente: Cliente,
        servicio,
        duracion: int,
        descuento: float = 0.0,
        aplicar_iva: bool = True,
        recargo_urgencia: float = 0.0
    ):
        try:
            reserva = Reserva(id_reserva, cliente, servicio, duracion)
            reserva.confirmar(descuento=descuento, aplicar_iva=aplicar_iva, recargo_urgencia=recargo_urgencia)
            self.reservas.append(reserva)
            print(f"[OK] {reserva.obtener_resumen()}")
            return reserva
        except ErrorSoftwareFJ as e:
            causa = f" | Causa raíz: {e.__cause__}" if e.__cause__ else ""
            logger.error(f"Fallo en reserva [{id_reserva}]: {e}{causa}")
            print(f"[ERROR CONTROLADO] {e}{causa}")
            return None


def ejecutar_simulaciones():
    print("\nSISTEMA DE GESTIÓN SOFTWARE FJ: SIMULACIÓN DE OPERACIONES")
    logger.info("INICIO DE EJECUCIÓN DEL SISTEMA SOFTWARE FJ")

    sistema = SistemaSoftwareFJ()

    # Simulación 1: registro válido de clientes
    print("\n[Simulación 1] Registro de clientes válidos")
    cli_1 = sistema.registrar_cliente("CLI-01", "Laura Gómez", "laura.gomez@empresa.co", "3104567890")
    cli_2 = sistema.registrar_cliente("CLI-02", "Carlos Méndez", "cmendez@techmail.com", "3009876543")
    cli_3 = sistema.registrar_cliente("CLI-03", "Andrés Restrepo", "andres.r@innovasoft.co", "6043214567")

    # Simulación 2: registro inválido de cliente por correo sin arroba
    print("\n[Simulación 2] Intento de registro con correo inválido")
    sistema.registrar_cliente("CLI-ERR1", "Pedro Pérez", "pedro.sin.arroba.com", "3112223344")

    # Simulación 3: registro inválido de cliente por teléfono con letras
    print("\n[Simulación 3] Intento de registro con teléfono alfabético")
    sistema.registrar_cliente("CLI-ERR2", "Ana Torres", "ana@correo.com", "315ABC99")

    # Simulación 4: creación válida de los 3 tipos de servicios
    print("\n[Simulación 4] Creación de catálogo de servicios especializados")
    sala_juntas = sistema.registrar_servicio(
        ReservaSala("SRV-S01", "Sala Innovación Ágil", tarifa_hora=80000, capacidad=10)
    )
    estacion_gpu = sistema.registrar_servicio(
        AlquilerEquipo("SRV-E01", "Workstation RTX 4090", tarifa_dia=120000, stock_disponible=1)
    )
    asesoria_arq = sistema.registrar_servicio(
        AsesoriaEspecializada("SRV-A01", "Consultoría Cloud y Microservicios", tarifa_hora=150000, especialidad="Arquitectura")
    )

    # Simulación 5: creación inválida de servicio con tarifa negativa
    print("\n[Simulación 5] Intento de crear servicio con tarifa negativa")
    try:
        ReservaSala("SRV-ERR", "Sala Fantasma", tarifa_hora=-50000, capacidad=5)
    except ErrorSoftwareFJ as e:
        logger.error(f"Error al crear servicio inválido: {e}")
        print(f"[ERROR CONTROLADO] Creación de servicio bloqueada: {e}")

    # Simulación 6: reserva exitosa de sala por 5 horas con recargo y 10% de descuento
    print("\n[Simulación 6] Reserva exitosa de Sala por 5 horas con descuento del 10%")
    res_1 = sistema.crear_y_confirmar_reserva("RES-101", cli_1, sala_juntas, duracion=5, descuento=10.0)

    # Simulación 7: alquiler exitoso de equipo que consume la única unidad disponible
    print("\n[Simulación 7] Alquiler exitoso de Workstation por 3 días")
    res_2 = sistema.crear_y_confirmar_reserva("RES-102", cli_2, estacion_gpu, duracion=3, recargo_urgencia=15000)

    # Simulación 8: reserva fallida porque el equipo ya quedó sin stock
    print("\n[Simulación 8] Intento fallido de alquilar Workstation ya agotada")
    sistema.crear_y_confirmar_reserva("RES-103", cli_3, estacion_gpu, duracion=2)

    # Simulación 9: reserva fallida por duración menor al mínimo permitido en asesorías
    print("\n[Simulación 9] Intento fallido de asesoría de 1 hora (mínimo son 2h)")
    sistema.crear_y_confirmar_reserva("RES-104", cli_3, asesoria_arq, duracion=1)

    # Simulación 10: procesar una reserva y bloquear su cancelación posterior
    print("\n[Simulación 10] Procesar reserva de sala e intentar cancelarla después")
    if res_1:
        try:
            res_1.procesar()
            print(f"[OK] Estado actualizado: {res_1.obtener_resumen()}")
            res_1.cancelar()
        except ErrorSoftwareFJ as e:
            logger.error(f"Operación inválida sobre reserva procesada [{res_1.id_entidad}]: {e}")
            print(f"[ERROR CONTROLADO] {e}")

    # Simulación 11: cancelación exitosa de equipo que devuelve la unidad al inventario
    print("\n[Simulación 11] Cancelar alquiler de Workstation y verificar liberación de stock")
    if res_2:
        try:
            res_2.cancelar()
            print(f"[OK] {res_2.obtener_resumen()} | Stock actual equipo: {estacion_gpu.stock}")
        except ErrorSoftwareFJ as e:
            logger.error(f"Error al cancelar reserva [{res_2.id_entidad}]: {e}")
            print(f"[ERROR CONTROLADO] {e}")

    # Simulación 12: nueva reserva exitosa sobre el equipo recién liberado
    print("\n[Simulación 12] Nueva reserva exitosa de Workstation para Cliente 3")
    sistema.crear_y_confirmar_reserva("RES-105", cli_3, estacion_gpu, duracion=4, descuento=5.0)

    print(f"\nRESUMEN FINAL: {len(sistema.clientes)} clientes | {len(sistema.servicios)} servicios | {len(sistema.reservas)} reservas válidas")
    print("Todas las excepciones fueron controladas y registradas en 'sistema_software_fj.log'.\n")
    logger.info("FIN DE EJECUCIÓN EXITOSA SIN INTERRUPCIONES")


if __name__ == "__main__":
    ejecutar_simulaciones()