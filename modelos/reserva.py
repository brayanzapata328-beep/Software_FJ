
from math import isfinite

from modelos.entidad import Entidad
from modelos.cliente import Cliente
from modelos.servicio import Servicio
from servicios.servicio_equipo import ServicioEquipo


class Reserva(Entidad):
    """
    Representa una reserva realizada por un cliente
    para utilizar alguno de los servicios de Software FJ.
    """

    ESTADOS_VALIDOS = (
        "pendiente",
        "confirmada",
        "cancelada",
        "completada"
    )

    def __init__(self, cliente, servicio, duracion, unidades=1):
        """
        Inicializa una reserva.

        Args:
            cliente (Cliente): Cliente que realiza la reserva.
            servicio (Servicio): Servicio solicitado.
            duracion (float): Duración en horas.
            unidades (int): Cantidad de equipos solicitados.
        """

        super().__init__()

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.unidades = unidades

        self.__estado = "pendiente"
        self.__costo_total = 0.0

        self.validar()

    # --------------------------------------------------
    # PROPIEDADES Y ENCAPSULACIÓN
    # --------------------------------------------------

    @property
    def cliente(self):
        return self.__cliente

    @cliente.setter
    def cliente(self, valor):
        if not isinstance(valor, Cliente):
            raise ValueError(
                "La reserva debe estar asociada a un cliente válido."
            )

        self.__cliente = valor

    @property
    def servicio(self):
        return self.__servicio

    @servicio.setter
    def servicio(self, valor):
        if not isinstance(valor, Servicio):
            raise ValueError(
                "La reserva debe estar asociada a un servicio válido."
            )

        self.__servicio = valor

    @property
    def duracion(self):
        return self.__duracion

    @duracion.setter
    def duracion(self, valor):
        if (
            isinstance(valor, bool)
            or not isinstance(valor, (int, float))
        ):
            raise ValueError(
                "La duración debe ser un valor numérico."
            )

        if not isfinite(valor) or valor <= 0:
            raise ValueError(
                "La duración debe ser mayor que cero y finita."
            )

        self.__duracion = float(valor)

    @property
    def unidades(self):
        return self.__unidades

    @unidades.setter
    def unidades(self, valor):
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise ValueError(
                "Las unidades deben ser un número entero."
            )

        if valor <= 0:
            raise ValueError(
                "Debe solicitar al menos una unidad."
            )

        self.__unidades = valor

    @property
    def estado(self):
        return self.__estado

    @property
    def costo_total(self):
        return self.__costo_total

    # --------------------------------------------------
    # VALIDACIONES
    # --------------------------------------------------

    def validar(self):
        """
        Valida los datos generales de la reserva.
        """

        if not isinstance(self.__cliente, Cliente):
            raise ValueError("El cliente de la reserva no es válido.")

        if not isinstance(self.__servicio, Servicio):
            raise ValueError("El servicio de la reserva no es válido.")

        self.cliente = self.__cliente
        self.servicio = self.__servicio
        self.duracion = self.__duracion
        self.unidades = self.__unidades

        if (
            not isinstance(self.servicio, ServicioEquipo)
            and self.unidades != 1
        ):
            raise ValueError(
                "Solo se pueden solicitar varias unidades "
                "en el servicio de alquiler de equipos."
            )

        return True

    # --------------------------------------------------
    # CÁLCULO DE COSTOS
    # --------------------------------------------------

    def calcular_total(self, descuento=0, impuesto=0.19):
        """
        Calcula el costo total de la reserva según el servicio.

        Args:
            descuento (float): Descuento expresado entre 0 y 1.
            impuesto (float): Impuesto expresado entre 0 y 1.

        Returns:
            float: Costo total de la reserva.
        """

        if (
            isinstance(descuento, bool)
            or not isinstance(descuento, (int, float))
            or not isfinite(descuento)
            or not 0 <= descuento <= 1
        ):
            raise ValueError(
                "El descuento debe estar entre 0 y 1."
            )

        if (
            isinstance(impuesto, bool)
            or not isinstance(impuesto, (int, float))
            or not isfinite(impuesto)
            or not 0 <= impuesto <= 1
        ):
            raise ValueError(
                "El impuesto debe estar entre 0 y 1."
            )

        if isinstance(self.servicio, ServicioEquipo):
            return self.servicio.calcular_costo(
                cantidad=self.duracion,
                descuento=descuento,
                impuesto=impuesto,
                unidades=self.unidades
            )

        return self.servicio.calcular_costo(
            cantidad=self.duracion,
            descuento=descuento,
            impuesto=impuesto
        )

    # --------------------------------------------------
    # CONFIRMACIÓN Y PROCESAMIENTO
    # --------------------------------------------------

    def procesar(self, descuento=0, impuesto=0.19):
        """
        Procesa una reserva pendiente, calcula su costo
        y cambia su estado a confirmada.
        """

        if self.estado != "pendiente":
            raise ValueError(
                "Solo se pueden procesar reservas pendientes."
            )

        # Valida la disponibilidad y los parámetros del servicio.
        self.servicio.validar_parametros(self.duracion) if (
            not isinstance(self.servicio, ServicioEquipo)
        ) else self.servicio.validar_parametros(
            self.duracion, self.unidades
        )

        costo = self.calcular_total(descuento, impuesto)

        if not isfinite(costo) or costo <= 0:
            raise ValueError(
                "El costo calculado de la reserva no es válido."
            )

        self.__costo_total = costo
        self.__estado = "confirmada"

        return self.__costo_total

    def confirmar(self, descuento=0, impuesto=0.19):
        """
        Confirma una reserva mediante su procesamiento.
        """

        return self.procesar(descuento, impuesto)

    # --------------------------------------------------
    # CANCELACIÓN Y FINALIZACIÓN
    # --------------------------------------------------

    def cancelar(self):
        """
        Cancela una reserva pendiente o confirmada.
        """

        if self.estado not in ("pendiente", "confirmada"):
            raise ValueError(
                "No se puede cancelar una reserva "
                "que ya está cancelada o completada."
            )

        self.__estado = "cancelada"

        return True

    def completar(self):
        """
        Marca como completada una reserva confirmada.
        """

        if self.estado != "confirmada":
            raise ValueError(
                "Solo se pueden completar reservas confirmadas."
            )

        self.__estado = "completada"

        return True

    # --------------------------------------------------
    # REPRESENTACIÓN DEL OBJETO
    # --------------------------------------------------

    def __str__(self):
        """
        Devuelve una representación legible de la reserva.
        """

        return (
            f"Reserva: {self.id}\n"
            f"Cliente: {self.cliente.nombre}\n"
            f"Servicio: {self.servicio.nombre}\n"
            f"Duración: {self.duracion} horas\n"
            f"Unidades: {self.unidades}\n"
            f"Estado: {self.estado.capitalize()}\n"
            f"Costo total: ${self.costo_total:,.2f}"
        )
