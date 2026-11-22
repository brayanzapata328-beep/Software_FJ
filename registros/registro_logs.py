
"""
Módulo encargado de configurar y administrar los registros
de eventos y errores del sistema Software FJ.
"""

import logging
from pathlib import Path


# Determina la ubicación de la carpeta de registros.
RUTA_REGISTROS = Path(__file__).resolve().parent

# Define la ubicación del archivo de logs.
RUTA_LOG = RUTA_REGISTROS / "software_fj.log"


def configurar_logger(nombre="SoftwareFJ"):
    """
    Configura el sistema de registro de eventos y errores.

    Args:
        nombre (str): Nombre del logger.

    Returns:
        logging.Logger: Logger configurado.
    """

    # Crea la carpeta si todavía no existe.
    RUTA_REGISTROS.mkdir(parents=True, exist_ok=True)

    # Obtiene el logger principal.
    logger = logging.getLogger(nombre)

    # Establece el nivel mínimo de registro.
    logger.setLevel(logging.DEBUG)

    # Evita agregar manejadores duplicados.
    if not logger.handlers:

        # Define el formato de los registros.
        formato = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Configura el archivo donde se guardarán los registros.
        manejador_archivo = logging.FileHandler(
            RUTA_LOG,
            encoding="utf-8"
        )

        manejador_archivo.setLevel(logging.DEBUG)
        manejador_archivo.setFormatter(formato)

        # Configura también la salida por consola.
        manejador_consola = logging.StreamHandler()
        manejador_consola.setLevel(logging.INFO)
        manejador_consola.setFormatter(formato)

        # Asocia los manejadores al logger.
        logger.addHandler(manejador_archivo)
        logger.addHandler(manejador_consola)

    # Evita que los mensajes se dupliquen en el logger raíz.
    logger.propagate = False

    return logger


# Crea el logger principal del sistema.
logger = configurar_logger()


def registrar_evento(mensaje):
    """
    Registra un evento relevante del sistema.
    """
    logger.info(mensaje)


def registrar_advertencia(mensaje):
    """
    Registra una situación que requiere atención.
    """
    logger.warning(mensaje)


def registrar_error(mensaje, excepcion=None):
    """
    Registra un error y, cuando corresponde, su información técnica.

    Args:
        mensaje (str): Descripción del error.
        excepcion (Exception): Excepción que produjo el error.
    """

    if excepcion is not None:
        logger.error(
            "%s: %s",
            mensaje,
            excepcion,
            exc_info=(
                type(excepcion),
                excepcion,
                excepcion.__traceback__
            )
        )
    else:
        logger.error(mensaje)
