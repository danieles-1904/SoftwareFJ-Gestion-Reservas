"""
Nombre del Estudiante: Daniel Esteban Jaramillo Ruiz
Programa: Ingeniería de Sistemas
Código Fuente: Autoría Propia
Fase 4 - Sistema Integral de Gestión de Reservas (Software FJ)
"""

import logging


def configurar_logger():
    """Inicializa y devuelve el logger que guarda la actividad en el archivo .log."""
    logger = logging.getLogger("SoftwareFJ")
    logger.setLevel(logging.INFO)

    # Evita que se dupliquen los registros si se llama varias veces
    if not logger.handlers:
        archivo_handler = logging.FileHandler("sistema_software_fj.log", mode="a", encoding="utf-8")
        archivo_handler.setLevel(logging.INFO)

        formato = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        archivo_handler.setFormatter(formato)
        logger.addHandler(archivo_handler)

    return logger