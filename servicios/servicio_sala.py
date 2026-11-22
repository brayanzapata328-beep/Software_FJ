
from math import isfinite

from modelos.servicio import Servicio


class ServicioSala(Servicio):
    """
    Representa el servicio de alquiler de salas de Software FJ.

    Hereda de Servicio e incorpora características específicas
    como la capacidad y el equipamiento disponible.
    """

    def __init__(
        self,
        nombre,
        descripcion,
        precio_base,
        capacidad,
        equipamiento,
        disponible=True
    ):
        """
        Inicializa una sala con sus características particulares.

        Args:
            nombre (str): Nombre de la sala.
            descripcion (str): Descripción de la sala.
            precio_base (float): Precio por hora de alquiler.
            capacidad (int): Número máximo de personas.
            equipamiento (list): Elementos disponibles en la sala.
            disponible (bool): Estado de disponibilidad.
        """

        super().__init__(
            nombre,
            descripcion,
            precio_base,
            disponible
        )

        self.capacidad = capacidad
        self.equipamiento = equipamiento

        self.validar()

    @property
    def capacidad(self):
        return self.__capacidad

    @capacidad.setter
    def capacidad(self, valor):
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise ValueError("La capacidad debe ser un número entero.")

        if valor <= 0:
            raise ValueError("La capacidad debe ser mayor que cero.")

        self.__capacidad = valor

    @property
    def equipamiento(self):
        return self.__equipamiento

    @equipamiento.setter
    def equipamiento(self, valor):
        if not isinstance(valor, (list, tuple)):
            raise ValueError("El equipamiento debe ser una lista o tupla.")

        if not all(
            isinstance(elemento, str) and elemento.strip()
            for elemento in valor
        ):
            raise ValueError("Todos los elementos del equipamiento deben ser textos válidos.")

        self.__equipamiento = tuple(
            elemento.strip() for elemento in valor
        )

    def validar(self):
        """
        Valida los atributos generales y específicos de la sala.
        """

        super().validar()

        self.capacidad = self.__capacidad
        self.equipamiento = self.__equipamiento

        return True

    def validar_parametros(self, cantidad=1):
        """
        Comprueba que las horas de alquiler sean válidas
        y que la sala se encuentre disponible.
        """

        if not self.disponible:
            raise ValueError("La sala no se encuentra disponible.")

        if isinstance(cantidad, bool) or not isinstance(cantidad, (int, float)):
            raise ValueError("La duración debe ser un valor numérico.")

        if not isfinite(cantidad) or cantidad <= 0:
            raise ValueError("La duración debe ser mayor que cero.")

        return True

    def calcular_costo(self, cantidad=1, descuento=0, impuesto=0.19):
        """
        Calcula el costo del alquiler según las horas contratadas.

        Args:
            cantidad (float): Cantidad de horas de alquiler.
            descuento (float): Descuento expresado entre 0 y 1.
            impuesto (float): Impuesto expresado entre 0 y 1.

        Returns:
            float: Costo total del alquiler.
        """

        self.validar_parametros(cantidad)

        for nombre, porcentaje in (
            ("Descuento", descuento),
            ("Impuesto", impuesto)
        ):
            if (
                isinstance(porcentaje, bool)
                or not isinstance(porcentaje, (int, float))
                or not isfinite(porcentaje)
                or not 0 <= porcentaje <= 1
            ):
                raise ValueError(
                    f"El {nombre.lower()} debe estar entre 0 y 1."
                )

        subtotal = self.precio_base * cantidad
        valor_descuento = subtotal * descuento
        subtotal_con_descuento = subtotal - valor_descuento
        valor_impuesto = subtotal_con_descuento * impuesto

        return round(subtotal_con_descuento + valor_impuesto, 2)

    def describir(self):
        """
        Genera una descripción detallada de la sala.
        """

        elementos = ", ".join(self.equipamiento)

        return (
            f"Nombre: {self.nombre}\n"
            f"Descripción: {self.descripcion}\n"
            f"Capacidad: {self.capacidad} personas\n"
            f"Precio por hora: ${self.precio_base:,.2f}\n"
            f"Equipamiento: {elementos or 'Sin equipamiento adicional'}\n"
            f"Disponible: {'Sí' if self.disponible else 'No'}"
        )
