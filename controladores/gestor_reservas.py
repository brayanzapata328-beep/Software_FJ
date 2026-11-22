
"""
Módulo encargado de administrar las reservas de Software FJ.

Integra los gestores de clientes y servicios para crear y administrar
reservas. Mantiene las reservas en una lista interna y registra
los eventos y errores de las operaciones realizadas.
"""

from modelos.reserva import Reserva
from servicios.servicio_equipo import ServicioEquipo

from utilidades.excepciones import (
    ErrorValidacion,
    ClienteNoEncontradoError,
    ServicioNoEncontradoError,
    ServicioNoDisponibleError,
    ReservaNoEncontradaError,
    OperacionNoPermitidaError,
    CapacidadInsuficienteError
)

from registros.registro_logs import (
    registrar_evento,
    registrar_error
)


class GestorReservas:
    """
    Administra las reservas y coordina los gestores de clientes
    y servicios.
    """

    def __init__(self, gestor_clientes, gestor_servicios):
        """
        Inicializa el gestor de reservas.

        Args:
            gestor_clientes: Gestor encargado de administrar clientes.
            gestor_servicios: Gestor encargado de administrar servicios.
        """

        if gestor_clientes is None or gestor_servicios is None:
            raise ErrorValidacion(
                "Se requieren los gestores de clientes y servicios."
            )

        self.__gestor_clientes = gestor_clientes
        self.__gestor_servicios = gestor_servicios
        self.__reservas = []

        registrar_evento(
            "Gestor de reservas inicializado correctamente"
        )

    @property
    def cantidad_reservas(self):
        """Devuelve la cantidad de reservas registradas."""
        return len(self.__reservas)

    def crear_reserva(
        self,
        documento_cliente,
        identificador_servicio,
        duracion,
        unidades=1
    ):
        """
        Crea una reserva utilizando un cliente y un servicio existentes.

        La reserva se crea inicialmente en estado pendiente.
        Su confirmación y cálculo definitivo se realizan por separado.

        Args:
            documento_cliente (str): Documento del cliente.
            identificador_servicio (str): ID del servicio.
            duracion (float): Duración solicitada.
            unidades (int): Unidades de equipo solicitadas.

        Returns:
            Reserva: Reserva creada y registrada.
        """

        try:
            # Recupera el cliente y el servicio desde sus gestores.
            cliente = self.__gestor_clientes.buscar_por_documento(
                documento_cliente
            )

            servicio = self.__gestor_servicios.buscar_por_id(
                identificador_servicio
            )

            # Comprueba que el servicio esté disponible.
            if not servicio.disponible:
                raise ServicioNoDisponibleError(
                    f"El servicio '{servicio.nombre}' no está disponible."
                )

            # Comprueba las unidades solicitadas cuando se alquilan equipos.
            if isinstance(servicio, ServicioEquipo):
                if unidades > servicio.unidades_disponibles:
                    raise CapacidadInsuficienteError(
                        f"Se solicitaron {unidades} unidades, "
                        f"pero solo hay {servicio.unidades_disponibles} "
                        "disponibles."
                    )

            # Construye la reserva con los objetos existentes.
            reserva = Reserva(
                cliente,
                servicio,
                duracion,
                unidades
            )

            # Valida la relación entre cliente, servicio y duración.
            reserva.validar()

            # Incorpora la reserva a la lista interna.
            self.__reservas.append(reserva)

            registrar_evento(
                f"Reserva creada: {reserva.id} | "
                f"Cliente: {cliente.documento} | "
                f"Servicio: {servicio.nombre}"
            )

            return reserva

        except (
            ClienteNoEncontradoError,
            ServicioNoEncontradoError,
            ServicioNoDisponibleError,
            CapacidadInsuficienteError,
            ErrorValidacion
        ) as error:
            registrar_error(
                "No fue posible crear la reserva",
                error
            )
            raise

        except (TypeError, ValueError) as error:
            registrar_error(
                "Datos inválidos durante la creación de una reserva",
                error
            )

            raise ErrorValidacion(
                "No se pudo crear la reserva debido a datos inválidos."
            ) from error

    def buscar_por_id(self, identificador):
        """
        Busca una reserva mediante su identificador único.

        Args:
            identificador (str): Identificador de la reserva.

        Returns:
            Reserva: Reserva encontrada.

        Raises:
            ErrorValidacion: Si el identificador es inválido.
            ReservaNoEncontradaError: Si no existe la reserva.
        """

        if (
            not isinstance(identificador, str)
            or not identificador.strip()
        ):
            error = ErrorValidacion(
                "El identificador de la reserva debe ser un texto no vacío."
            )

            registrar_error("Identificador de reserva inválido", error)
            raise error

        for reserva in self.__reservas:
            if reserva.id == identificador:
                registrar_evento(
                    f"Reserva consultada: {identificador}"
                )
                return reserva

        error = ReservaNoEncontradaError(
            f"No existe una reserva con identificador {identificador}."
        )

        registrar_error("Reserva no encontrada", error)
        raise error

    def listar_reservas(self):
        """
        Devuelve una copia de todas las reservas registradas.
        """

        registrar_evento(
            f"Consulta general de reservas: {len(self.__reservas)} registros"
        )

        return self.__reservas.copy()

    def buscar_por_cliente(self, documento_cliente):
        """
        Obtiene todas las reservas asociadas a un cliente.

        Args:
            documento_cliente (str): Documento del cliente.

        Returns:
            list: Reservas pertenecientes al cliente.
        """

        # Verifica primero que el cliente exista.
        self.__gestor_clientes.buscar_por_documento(documento_cliente)

        resultados = [
            reserva
            for reserva in self.__reservas
            if reserva.cliente.documento == documento_cliente
        ]

        registrar_evento(
            f"Consulta de reservas del cliente {documento_cliente}: "
            f"{len(resultados)} resultados"
        )

        return resultados

    def filtrar_por_estado(self, estado):
        """
        Filtra las reservas según su estado actual.

        Estados permitidos:
        pendiente, confirmada, cancelada y completada.
        """

        estados_validos = Reserva.ESTADOS_VALIDOS

        if not isinstance(estado, str) or estado not in estados_validos:
            error = ErrorValidacion(
                f"Estado inválido. Estados permitidos: {estados_validos}."
            )

            registrar_error("Filtro de reservas con estado inválido", error)
            raise error

        resultados = [
            reserva
            for reserva in self.__reservas
            if reserva.estado == estado
        ]

        registrar_evento(
            f"Reservas filtradas por estado '{estado}': "
            f"{len(resultados)} resultados"
        )

        return resultados

    def confirmar_reserva(self, identificador, descuento=0, impuesto=0.19):
        """
        Confirma una reserva pendiente y calcula su costo.

        Args:
            identificador (str): Identificador de la reserva.
            descuento (float): Descuento aplicado, entre 0 y 1.
            impuesto (float): Impuesto aplicado, entre 0 y 1.

        Returns:
            float: Costo total de la reserva.
        """

        reserva = self.buscar_por_id(identificador)

        if reserva.estado != "pendiente":
            error = OperacionNoPermitidaError(
                "Solo se pueden confirmar reservas pendientes."
            )

            registrar_error("Confirmación de reserva no permitida", error)
            raise error

        if not reserva.servicio.disponible:
            error = ServicioNoDisponibleError(
                f"El servicio '{reserva.servicio.nombre}' "
                "no está disponible para confirmar la reserva."
            )

            registrar_error("Servicio no disponible al confirmar", error)
            raise error

        if isinstance(reserva.servicio, ServicioEquipo):
            if reserva.unidades > reserva.servicio.unidades_disponibles:
                error = CapacidadInsuficienteError(
                    "No hay suficientes unidades de equipo disponibles."
                )

                registrar_error("Unidades insuficientes al confirmar", error)
                raise error

        try:
            costo = reserva.confirmar(
                descuento=descuento,
                impuesto=impuesto
            )

            registrar_evento(
                f"Reserva confirmada: {identificador} | "
                f"Costo total: {costo}"
            )

            return costo

        except (TypeError, ValueError) as error:
            registrar_error(
                f"Error al confirmar la reserva {identificador}",
                error
            )

            raise OperacionNoPermitidaError(
                "No fue posible confirmar la reserva. "
                "Verifique sus parámetros y estado."
            ) from error

    def cancelar_reserva(self, identificador):
        """
        Cancela una reserva pendiente o confirmada.
        """

        reserva = self.buscar_por_id(identificador)

        try:
            reserva.cancelar()

            registrar_evento(
                f"Reserva cancelada: {identificador}"
            )

            return reserva

        except (TypeError, ValueError) as error:
            registrar_error(
                f"No fue posible cancelar la reserva {identificador}",
                error
            )

            raise OperacionNoPermitidaError(
                "La reserva no puede cancelarse en su estado actual."
            ) from error

    def completar_reserva(self, identificador):
        """
        Marca como completada una reserva confirmada.
        """

        reserva = self.buscar_por_id(identificador)

        try:
            reserva.completar()

            registrar_evento(
                f"Reserva completada: {identificador}"
            )

            return reserva

        except (TypeError, ValueError) as error:
            registrar_error(
                f"No fue posible completar la reserva {identificador}",
                error
            )

            raise OperacionNoPermitidaError(
                "Solo se pueden completar reservas confirmadas."
            ) from error

    def existe_reserva(self, identificador):
        """
        Comprueba si existe una reserva con el identificador indicado.
        """

        return any(
            reserva.id == identificador
            for reserva in self.__reservas
        )

    def limpiar_reservas(self):
        """
        Elimina todas las reservas de la lista interna.

        Se utiliza para pruebas y reinicio de sesiones.
        """

        cantidad = len(self.__reservas)
        self.__reservas.clear()

        registrar_evento(
            f"Lista de reservas reiniciada. "
            f"Registros eliminados: {cantidad}"
        )
