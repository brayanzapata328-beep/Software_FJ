
"""
Módulo de excepciones personalizadas del sistema Software FJ.

Define los errores específicos que pueden presentarse durante
la gestión de clientes, servicios y reservas.
"""


class SoftwareFJError(Exception):
    """Excepción base de todos los errores propios del sistema."""
    pass


class ErrorValidacion(SoftwareFJError):
    """Se presenta cuando un dato o parámetro no cumple las reglas."""
    pass


class ClienteNoEncontradoError(SoftwareFJError):
    """Se presenta cuando no existe el cliente solicitado."""
    pass


class ServicioNoEncontradoError(SoftwareFJError):
    """Se presenta cuando no existe el servicio solicitado."""
    pass


class ServicioNoDisponibleError(SoftwareFJError):
    """Se presenta cuando se intenta utilizar un servicio no disponible."""
    pass


class ReservaNoEncontradaError(SoftwareFJError):
    """Se presenta cuando no existe la reserva solicitada."""
    pass


class OperacionNoPermitidaError(SoftwareFJError):
    """Se presenta cuando se intenta ejecutar una operación no permitida."""
    pass


class CapacidadInsuficienteError(SoftwareFJError):
    """Se presenta cuando no hay suficientes unidades o capacidad."""
    pass


class ErrorCalculoError(SoftwareFJError):
    """Se presenta cuando ocurre un error durante un cálculo."""
    pass
