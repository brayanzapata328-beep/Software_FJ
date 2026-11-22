
"""
Módulo encargado de administrar los clientes de Software FJ.

Permite registrar, consultar, actualizar y eliminar clientes.
La información se mantiene en una lista interna, sin utilizar
bases de datos ni archivos de almacenamiento.
"""

from modelos.cliente import Cliente

from utilidades.excepciones import (
    ErrorValidacion,
    ClienteNoEncontradoError
)

from registros.registro_logs import (
    registrar_evento,
    registrar_error
)


class GestorClientes:
    """
    Administra las operaciones relacionadas con los clientes.

    Los clientes se almacenan temporalmente en una lista interna.
    """

    def __init__(self):
        """Inicializa la lista interna de clientes."""
        self.__clientes = []

        registrar_evento(
            "Gestor de clientes inicializado correctamente"
        )

    @property
    def cantidad_clientes(self):
        """Devuelve la cantidad de clientes registrados."""
        return len(self.__clientes)

    def registrar_cliente(self, cliente):
        """
        Registra un nuevo cliente.

        Args:
            cliente (Cliente): Objeto que se desea registrar.

        Returns:
            Cliente: Cliente registrado.

        Raises:
            ErrorValidacion: Si el objeto no es válido o está duplicado.
        """

        try:
            # Comprueba que el objeto pertenezca a la clase Cliente.
            if not isinstance(cliente, Cliente):
                raise ErrorValidacion(
                    "Solo se pueden registrar objetos de tipo Cliente."
                )

            # Comprueba que el cliente tenga datos válidos.
            cliente.validar()

            # Evita registrar documentos duplicados.
            if any(
                existente.documento == cliente.documento
                for existente in self.__clientes
            ):
                raise ErrorValidacion(
                    f"Ya existe un cliente con documento "
                    f"{cliente.documento}."
                )

            # Incorpora el cliente a la lista interna.
            self.__clientes.append(cliente)

            registrar_evento(
                f"Cliente registrado: {cliente.documento}"
            )

            return cliente

        except ErrorValidacion as error:
            registrar_error(
                "No fue posible registrar el cliente",
                error
            )
            raise

        except (TypeError, ValueError) as error:
            registrar_error(
                "Error de validación al registrar un cliente",
                error
            )

            raise ErrorValidacion(
                "Los datos proporcionados para el cliente no son válidos."
            ) from error

    def buscar_por_documento(self, documento):
        """
        Busca un cliente mediante su número de documento.

        Args:
            documento (str): Documento del cliente.

        Returns:
            Cliente: Cliente encontrado.

        Raises:
            ClienteNoEncontradoError: Si no existe el documento.
        """

        if not isinstance(documento, str) or not documento.strip():
            error = ErrorValidacion(
                "El documento de búsqueda debe ser un texto no vacío."
            )

            registrar_error("Documento de búsqueda inválido", error)
            raise error

        for cliente in self.__clientes:
            if cliente.documento == documento:
                registrar_evento(
                    f"Consulta de cliente realizada: {documento}"
                )
                return cliente

        error = ClienteNoEncontradoError(
            f"No existe un cliente con documento {documento}."
        )

        registrar_error("Cliente no encontrado", error)
        raise error

    def buscar_por_id(self, identificador):
        """
        Busca un cliente mediante su identificador único.

        Args:
            identificador (str): Identificador del cliente.

        Returns:
            Cliente: Cliente encontrado.

        Raises:
            ClienteNoEncontradoError: Si no existe el identificador.
        """

        if not isinstance(identificador, str) or not identificador.strip():
            error = ErrorValidacion(
                "El identificador debe ser un texto no vacío."
            )

            registrar_error("Identificador de búsqueda inválido", error)
            raise error

        for cliente in self.__clientes:
            if cliente.id == identificador:
                registrar_evento(
                    f"Consulta de cliente por identificador: {identificador}"
                )
                return cliente

        error = ClienteNoEncontradoError(
            f"No existe un cliente con identificador {identificador}."
        )

        registrar_error("Cliente no encontrado por identificador", error)
        raise error

    def listar_clientes(self):
        """
        Devuelve una copia de la lista de clientes.

        La copia evita que otros módulos puedan modificar directamente
        la lista interna del gestor.
        """

        registrar_evento(
            f"Consulta general de clientes: {len(self.__clientes)} registros"
        )

        return self.__clientes.copy()

    def actualizar_cliente(
        self,
        documento,
        nombre=None,
        correo=None,
        telefono=None
    ):
        """
        Actualiza los datos de un cliente existente.

        Los campos que no se indiquen conservan su valor anterior.

        Args:
            documento (str): Documento del cliente.
            nombre (str, opcional): Nuevo nombre.
            correo (str, opcional): Nuevo correo.
            telefono (str, opcional): Nuevo teléfono.

        Returns:
            Cliente: Cliente actualizado.
        """

        try:
            cliente = self.buscar_por_documento(documento)

            # Conserva los datos anteriores cuando no se especifican.
            nuevo_nombre = (
                cliente.nombre if nombre is None else nombre
            )

            nuevo_correo = (
                cliente.correo if correo is None else correo
            )

            nuevo_telefono = (
                cliente.telefono if telefono is None else telefono
            )

            # Construye un objeto temporal para validar todos los datos
            # antes de modificar el cliente original.
            cliente_validado = Cliente(
                nuevo_nombre,
                documento,
                nuevo_correo,
                nuevo_telefono
            )

            cliente_validado.validar()

            # Aplica los datos después de validar el conjunto completo.
            cliente.nombre = cliente_validado.nombre
            cliente.correo = cliente_validado.correo
            cliente.telefono = cliente_validado.telefono

            registrar_evento(
                f"Cliente actualizado: {documento}"
            )

            return cliente

        except ClienteNoEncontradoError:
            raise

        except (TypeError, ValueError) as error:
            registrar_error(
                f"No fue posible actualizar el cliente {documento}",
                error
            )

            raise ErrorValidacion(
                "La actualización contiene datos inválidos."
            ) from error

    def eliminar_cliente(self, documento):
        """
        Elimina un cliente mediante su documento.

        Args:
            documento (str): Documento del cliente eliminado.

        Returns:
            Cliente: Objeto del cliente eliminado.
        """

        cliente = self.buscar_por_documento(documento)

        self.__clientes.remove(cliente)

        registrar_evento(
            f"Cliente eliminado: {documento}"
        )

        return cliente

    def existe_documento(self, documento):
        """
        Comprueba si un documento ya está registrado.

        Returns:
            bool: True si existe, False en caso contrario.
        """

        return any(
            cliente.documento == documento
            for cliente in self.__clientes
        )

    def limpiar_clientes(self):
        """
        Elimina todos los clientes registrados en memoria.

        Esta operación se utiliza principalmente para pruebas
        o reiniciar la información de la sesión.
        """

        cantidad = len(self.__clientes)
        self.__clientes.clear()

        registrar_evento(
            f"Lista de clientes reiniciada. Registros eliminados: {cantidad}"
        )
