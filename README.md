# Sistema Integral de Gestión de Reservas - Software FJ

Proyecto desarrollado para la Fase 4 del curso de Programación Orientada a Objetos (Ingeniería de Sistemas - UNAD). Implementa un sistema modular en Python para administrar clientes, catálogo de servicios especializados y reservas con manejo avanzado de excepciones y bitácora de auditoría.

**Autor:** Daniel Esteban Jaramillo Ruiz  
**Programa:** Ingeniería de Sistemas  

## Arquitectura del Proyecto

El código está dividido en módulos independientes según su responsabilidad:

* **`excepciones.py`**: Define la jerarquía de excepciones personalizadas (`ErrorSoftwareFJ`, `DatosInvalidosError`, `ServicioNoDisponibleError`, `ReservaInvalidaError` y `OperacionNoPermitidaError`).
* **`logger_config.py`**: Configura el sistema de registro (`logging`) que almacena cada operación y fallo controlado en `sistema_software_fj.log`.
* **`modelos_base.py`**: Contiene la clase abstracta `EntidadSistema` y la clase `Cliente` con encapsulación mediante decoradores `@property` y validaciones estrictas en sus atributos.
* **`servicios.py`**: Implementa la clase abstracta `Servicio` y tres especializaciones (`ReservaSala`, `AlquilerEquipo` y `AsesoriaEspecializada`) aplicando herencia, polimorfismo y sobrecarga simulada en el cálculo de tarifas.
* **`reservas.py`**: Gestiona el ciclo de vida de la clase `Reserva` (`PENDIENTE`, `CONFIRMADA`, `PROCESADA`, `CANCELADA`) mediante bloques completos `try / except / else / finally` y encadenamiento de excepciones (`raise ... from`).
* **`main.py`**: Ejecuta 12 escenarios de prueba (operaciones válidas y errores provocados) demostrando que la aplicación se mantiene estable ante fallos.

## Requisitos y Ejecución

1. Tener instalado **Python 3.10 o superior**.
2. Clonar este repositorio y entrar a la carpeta del proyecto:
   ```bash
   git clone [https://github.com/danieles-1904/SoftwareFJ-Gestion-Reservas.git](https://github.com/danieles-1904/SoftwareFJ-Gestion-Reservas.git)
   cd SoftwareFJ-Gestion-Reservas