
from abc import abstractmethod
from math import isfinite

from modelos.entidad import Entidad


class Servicio(Entidad):
    """
    Clase abstracta que representa los servicios ofrecidos
    por la empresa Software FJ.
    """

    def __init__(self, nombre, descripcion, precio_base, disponible=True):
        """
        Inicializa los atributos generales de un servicio.

        Args:
            nombre (str): Nombre del servicio.
            descripcion (str): Descripción del servicio.
            precio_base (float): Precio inicial del servicio.
            disponible (bool): Estado de disponibilidad.
        """
        super().__init__()

        self.nombre = nombre
        self.descripcion = descripcion
        self.precio_base = precio_base
        self.disponible = disponible

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El nombre del servicio no puede estar vacío.")

        self.__nombre = valor.strip()

    @property
    def descripcion(self):
        return self.__descripcion

    @descripcion.setter
    def descripcion(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("La descripción del servicio no puede estar vacía.")

        self.__descripcion = valor.strip()

    @property
    def precio_base(self):
        return self.__precio_base

    @precio_base.setter
    def precio_base(self, valor):
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise ValueError("El precio base debe ser un valor numérico.")

        if not isfinite(valor) or valor <= 0:
            raise ValueError("El precio base debe ser mayor que cero y finito.")

        self.__precio_base = float(valor)

    @property
    def disponible(self):
        return self.__disponible

    @disponible.setter
    def disponible(self, valor):
        if not isinstance(valor, bool):
            raise ValueError("La disponibilidad debe ser verdadera o falsa.")

        self.__disponible = valor

    def validar(self):
        """
        Valida los atributos generales del servicio.
        """
        self.nombre = self.__nombre
        self.descripcion = self.__descripcion
        self.precio_base = self.__precio_base
        self.disponible = self.__disponible

        return True

    @abstractmethod
    def calcular_costo(self, cantidad=1, descuento=0, impuesto=0.19):
        """
        Calcula el costo del servicio según sus características.
        Cada servicio especializado implementará su propio cálculo.
        """
        pass

    @abstractmethod
    def describir(self):
        """
        Devuelve una descripción detallada del servicio.
        """
        pass

    @abstractmethod
    def validar_parametros(self, cantidad=1):
        """
        Valida los parámetros particulares de cada servicio.
        """
        pass

    def __str__(self):
        return (
            f"Servicio: {self.nombre}\n"
            f"Descripción: {self.descripcion}\n"
            f"Precio base: ${self.precio_base:,.2f}\n"
            f"Disponible: {'Sí' if self.disponible else 'No'}"
        )
