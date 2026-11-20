
import re

from modelos.entidad import Entidad


class Cliente(Entidad):
    """
    Representa un cliente registrado en el sistema Software FJ.

    Hereda de Entidad y administra de manera encapsulada
    los datos personales de cada cliente.
    """

    def __init__(self, nombre, documento, correo, telefono):
        """
        Inicializa un cliente con sus datos personales.

        Args:
            nombre (str): Nombre completo del cliente.
            documento (str): Número de identificación.
            correo (str): Correo electrónico.
            telefono (str): Número de contacto.
        """
        super().__init__()

        self.__nombre = nombre
        self.__documento = documento
        self.__correo = correo
        self.__telefono = telefono

        self.validar()

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El nombre no puede estar vacío.")

        if not all(
            caracter.isalpha() or caracter.isspace()
            or caracter in "-'"
            for caracter in valor.strip()
        ):
            raise ValueError("El nombre contiene caracteres no permitidos.")

        self.__nombre = " ".join(valor.split())

    @property
    def documento(self):
        return self.__documento

    @documento.setter
    def documento(self, valor):
        if not isinstance(valor, str):
            raise ValueError("El documento debe ser una cadena de texto.")

        valor = valor.strip()

        if not valor.isdigit():
            raise ValueError("El documento solo debe contener números.")

        if not 6 <= len(valor) <= 15:
            raise ValueError("El documento debe tener entre 6 y 15 dígitos.")

        self.__documento = valor

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        if not isinstance(valor, str):
            raise ValueError("El correo debe ser una cadena de texto.")

        valor = valor.strip().lower()

        patron = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

        if not re.fullmatch(patron, valor):
            raise ValueError("El formato del correo electrónico no es válido.")

        self.__correo = valor

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        if not isinstance(valor, str):
            raise ValueError("El teléfono debe ser una cadena de texto.")

        valor = valor.strip()

        if not valor.isdigit():
            raise ValueError("El teléfono solo debe contener números.")

        if not 7 <= len(valor) <= 15:
            raise ValueError("El teléfono debe tener entre 7 y 15 dígitos.")

        self.__telefono = valor

    def validar(self):
        """
        Comprueba que todos los datos del cliente sean válidos.
        """
        self.nombre = self.__nombre
        self.documento = self.__documento
        self.correo = self.__correo
        self.telefono = self.__telefono

        return True

    def __str__(self):
        """
        Devuelve una representación legible del cliente.
        """
        return (
            f"Cliente: {self.nombre}\n"
            f"Documento: {self.documento}\n"
            f"Correo: {self.correo}\n"
            f"Teléfono: {self.telefono}"
        )
