# Importa el módulo re para validar el formato del correo con expresiones regulares
import re
# Importa la clase abstracta Entidad de la que hereda Cliente
from modelos.entidad import Entidad


# Define la clase Cliente heredando de Entidad
class Cliente(Entidad):
    """
    Representa un cliente registrado en el sistema Software FJ.

    Hereda de Entidad y administra de manera encapsulada
    los datos personales de cada cliente.
    """

    # Constructor que recibe los datos básicos del cliente
    def __init__(self, nombre, documento, correo, telefono):
        """
        Inicializa un cliente con sus datos personales.

        Args:
            nombre (str): Nombre completo del cliente.
            documento (str): Número de identificación.
            correo (str): Correo electrónico.
            telefono (str): Número de contacto.
        """
        # Llama al constructor de Entidad para asignar el identificador único
        super().__init__()

        # Almacena temporalmente los atributos privados antes de validarlos
        self.__nombre = nombre
        self.__documento = documento
        self.__correo = correo
        self.__telefono = telefono

        # Ejecuta la validación completa usando los setters de cada propiedad
        self.validar()

    # Define el getter para consultar el nombre del cliente
    @property
    def nombre(self):
        # Retorna el nombre almacenado en el atributo privado
        return self.__nombre

    # Define el setter para validar y asignar el nombre del cliente
    @nombre.setter
    def nombre(self, valor):
        # Verifica que el nombre sea una cadena de texto no vacía
        if not isinstance(valor, str) or not valor.strip():
            # Lanza ValueError si el nombre está vacío o no es texto
            raise ValueError("El nombre no puede estar vacío.")

        # Verifica que todos los caracteres sean letras, espacios o guiones
        if not all(
            caracter.isalpha() or caracter.isspace()
            or caracter in "-'"
            for caracter in valor.strip()
        ):
            # Lanza ValueError si hay números o símbolos inválidos en el nombre
            raise ValueError("El nombre contiene caracteres no permitidos.")

        # Limpia espacios múltiples y guarda el nombre normalizado
        self.__nombre = " ".join(valor.split())

    # Define el getter para consultar el documento del cliente
    @property
    def documento(self):
        # Retorna el documento almacenado en el atributo privado
        return self.__documento

    # Define el setter para validar y asignar el documento
    @documento.setter
    def documento(self, valor):
        # Comprueba que el documento sea una cadena de texto
        if not isinstance(valor, str):
            # Lanza ValueError si el tipo de dato es incorrecto
            raise ValueError("El documento debe ser una cadena de texto.")

        # Elimina espacios en blanco al inicio y al final
        valor = valor.strip()

        # Verifica que el documento contenga únicamente dígitos numéricos
        if not valor.isdigit():
            # Lanza ValueError si contiene letras u otros caracteres
            raise ValueError("El documento solo debe contener números.")

        # Comprueba que la longitud del documento esté entre 6 y 15 dígitos
        if not 6 <= len(valor) <= 15:
            # Lanza ValueError si el documento es muy corto o muy largo
            raise ValueError("El documento debe tener entre 6 y 15 dígitos.")

        # Guarda el documento ya validado en el atributo privado
        self.__documento = valor

    # Define el getter para consultar el correo electrónico
    @property
    def correo(self):
        # Retorna el correo almacenado en el atributo privado
        return self.__correo

    # Define el setter para validar y asignar el correo electrónico
    @correo.setter
    def correo(self, valor):
        # Verifica que el correo sea una cadena de texto
        if not isinstance(valor, str):
            # Lanza ValueError si no es texto
            raise ValueError("El correo debe ser una cadena de texto.")

        # Elimina espacios y convierte el correo a minúsculas
        valor = valor.strip().lower()

        # Define la expresión regular para validar la estructura básica de un correo
        patron = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

        # Comprueba que el correo coincida completamente con la expresión regular
        if not re.fullmatch(patron, valor):
            # Lanza ValueError si el formato del correo es inválido
            raise ValueError("El formato del correo electrónico no es válido.")

        # Guarda el correo validado en el atributo privado
        self.__correo = valor

    # Define el getter para consultar el teléfono de contacto
    @property
    def telefono(self):
        # Retorna el teléfono almacenado en el atributo privado
        return self.__telefono

    # Define el setter para validar y asignar el teléfono
    @telefono.setter
    def telefono(self, valor):
        # Verifica que el teléfono sea una cadena de texto
        if not isinstance(valor, str):
            # Lanza ValueError si no es texto
            raise ValueError("El teléfono debe ser una cadena de texto.")

        # Elimina espacios alrededor del número telefónico
        valor = valor.strip()

        # Verifica que el teléfono contenga solo dígitos
        if not valor.isdigit():
            # Lanza ValueError si tiene letras o símbolos
            raise ValueError("El teléfono solo debe contener números.")

        # Verifica que la longitud del teléfono esté entre 7 y 15 dígitos
        if not 7 <= len(valor) <= 15:
            # Lanza ValueError si no cumple el rango de longitud permitido
            raise ValueError("El teléfono debe tener entre 7 y 15 dígitos.")

        # Guarda el teléfono validado en el atributo privado
        self.__telefono = valor

    # Implementa el método abstracto validar heredado de Entidad
    def validar(self):
        """
        Comprueba que todos los datos del cliente sean válidos.
        """
        # Reasigna cada atributo a través de su setter para disparar las validaciones
        self.nombre = self.__nombre
        self.documento = self.__documento
        self.correo = self.__correo
        self.telefono = self.__telefono

        # Retorna True si todas las validaciones pasaron sin errores
        return True

    # Define la representación en texto legible del objeto Cliente
    def __str__(self):
        """
        Devuelve una representación legible del cliente.
        """
        # Construye y retorna la cadena formateada con los datos del cliente
        return (
            f"Cliente: {self.nombre}\n"
            f"Documento: {self.documento}\n"
            f"Correo: {self.correo}\n"
            f"Teléfono: {self.telefono}"
        )
