"""
Módulo de excepciones personalizadas del sistema Software FJ.

Define los errores específicos que pueden presentarse durante
la gestión de clientes, servicios y reservas.
"""


# Define la clase base de excepciones del sistema heredando de Exception
class SoftwareFJError(Exception):
    """Excepción base de todos los errores propios del sistema."""
    # Mantiene la estructura estándar de Exception sin agregar comportamiento extra
    pass


# Define la excepción para datos o parámetros que incumplen validaciones
class ErrorValidacion(SoftwareFJError):
    """Se presenta cuando un dato o parámetro no cumple las reglas."""
    # Hereda directamente de SoftwareFJError para agrupar errores del sistema
    pass


# Define la excepción para búsquedas de clientes inexistentes
class ClienteNoEncontradoError(SoftwareFJError):
    """Se presenta cuando no existe el cliente solicitado."""
    # Hereda de SoftwareFJError sin lógica adicional
    pass


# Define la excepción para búsquedas de servicios inexistentes
class ServicioNoEncontradoError(SoftwareFJError):
    """Se presenta cuando no existe el servicio solicitado."""
    # Hereda de SoftwareFJError sin lógica adicional
    pass


# Define la excepción cuando un servicio está ocupado o inactivo
class ServicioNoDisponibleError(SoftwareFJError):
    """Se presenta cuando se intenta utilizar un servicio no disponible."""
    # Hereda de SoftwareFJError sin lógica adicional
    pass


# Define la excepción para búsquedas de reservas inexistentes
class ReservaNoEncontradaError(SoftwareFJError):
    """Se presenta cuando no existe la reserva solicitada."""
    # Hereda de SoftwareFJError sin lógica adicional
    pass


# Define la excepción para acciones prohibidas según el estado o regla de negocio
class OperacionNoPermitidaError(SoftwareFJError):
    """Se presenta cuando se intenta ejecutar una operación no permitida."""
    # Hereda de SoftwareFJError sin lógica adicional
    pass


# Define la excepción cuando la capacidad o stock solicitado supera el disponible
class CapacidadInsuficienteError(SoftwareFJError):
    """Se presenta cuando no hay suficientes unidades o capacidad."""
    # Hereda de SoftwareFJError sin lógica adicional
    pass


# Define la excepción para fallos aritméticos o de tarifas al calcular costos
class ErrorCalculoError(SoftwareFJError):
    """Se presenta cuando ocurre un error durante un cálculo."""
    # Hereda de SoftwareFJError sin lógica adicional
    pass
