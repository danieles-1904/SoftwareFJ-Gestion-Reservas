"""
Módulo de configuración del sistema de registro (Logging)
Proyecto: Sistema Integral de Gestión - Software FJ
Autor: Daniel Esteban Jaramillo Ruiz
"""

import logging


def configurar_logger():
    """Configura y devuelve el logger principal para guardar eventos y errores en un archivo."""
    # Creamos una instancia de logger específica para nuestra aplicación
    logger = logging.getLogger("SoftwareFJ")
    logger.setLevel(logging.INFO)

    # Evitamos duplicar manejadores si la función se llama varias veces
    if not logger.handlers:
        # Configuramos el archivo de salida en UTF-8 para soportar tildes y caracteres especiales
        archivo_handler = logging.FileHandler("sistema_software_fj.log", mode="a", encoding="utf-8")
        archivo_handler.setLevel(logging.INFO)

        # Definimos el formato con fecha, hora exacta, nivel de gravedad y el mensaje
        formato = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        archivo_handler.setFormatter(formato)

        # Conectamos el manejador al logger
        logger.addHandler(archivo_handler)

    return logger