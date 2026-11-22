"""
Módulo encargado de configurar y administrar los registros
de eventos y errores del sistema Software FJ.
"""

# Importa el módulo estándar de Python para manejar logs
import logging
# Importa Path para construir rutas de archivos de forma segura entre sistemas operativos
from pathlib import Path

# Determina la ubicación de la carpeta de registros.
RUTA_REGISTROS = Path(__file__).resolve().parent

# Define la ubicación del archivo de logs.
RUTA_LOG = RUTA_REGISTROS / "software_fj.log"


# Define la función que inicializa y configura el logger del sistema
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

        # Configura el nivel DEBUG para guardar todo el detalle en el archivo
        manejador_archivo.setLevel(logging.DEBUG)
        # Aplica el formato de fecha, nivel y mensaje al manejador de archivo
        manejador_archivo.setFormatter(formato)

        # Configura también la salida por consola.
        manejador_consola = logging.StreamHandler()
        # Muestra en consola únicamente mensajes desde nivel INFO en adelante
        manejador_consola.setLevel(logging.INFO)
        # Aplica el mismo formato de salida para los mensajes en consola
        manejador_consola.setFormatter(formato)

        # Asocia los manejadores al logger.
        logger.addHandler(manejador_archivo)
        logger.addHandler(manejador_consola)

    # Evita que los mensajes se dupliquen en el logger raíz.
    logger.propagate = False

    # Devuelve el objeto logger ya configurado para usarse en el sistema
    return logger


# Crea el logger principal del sistema.
logger = configurar_logger()


# Define la función auxiliar para registrar eventos informativos normales
def registrar_evento(mensaje):
    """
    Registra un evento relevante del sistema.
    """
    # Envía el mensaje con nivel INFO al logger configurado
    logger.info(mensaje)


# Define la función auxiliar para registrar advertencias del sistema
def registrar_advertencia(mensaje):
    """
    Registra una situación que requiere atención.
    """
    # Envía el mensaje con nivel WARNING al logger configurado
    logger.warning(mensaje)


# Define la función auxiliar para registrar errores y su traza técnica opcional
def registrar_error(mensaje, excepcion=None):
    """
    Registra un error y, cuando corresponde, su información técnica.

    Args:
        mensaje (str): Descripción del error.
        excepcion (Exception): Excepción que produjo el error.
    """

    # Verifica si se recibió una instancia de excepción para incluir el traceback
    if excepcion is not None:
        # Registra el error junto con el tipo, mensaje y traza completa de la excepción
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
    # Si no se pasó una excepción específica, registra solo el mensaje de error
    else:
        # Envía el mensaje con nivel ERROR al logger
        logger.error(mensaje)
