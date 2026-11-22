
from math import isfinite

from modelos.servicio import Servicio


class ServicioEquipo(Servicio):
    """
    Representa el servicio de alquiler de equipos tecnológicos
    de Software FJ.
    """

    def __init__(
        self,
        nombre,
        descripcion,
        precio_base,
        tipo_equipo,
        unidades_disponibles,
        estado,
        disponible=True
    ):
        """
        Inicializa un servicio de alquiler de equipos.

        Args:
            nombre (str): Nombre del equipo.
            descripcion (str): Descripción del equipo.
            precio_base (float): Precio de alquiler por hora y unidad.
            tipo_equipo (str): Categoría del equipo.
            unidades_disponibles (int): Cantidad disponible para alquiler.
            estado (str): Estado de conservación del equipo.
            disponible (bool): Disponibilidad del servicio.
        """

        super().__init__(
            nombre,
            descripcion,
            precio_base,
            disponible
        )

        self.tipo_equipo = tipo_equipo
        self.unidades_disponibles = unidades_disponibles
        self.estado = estado

        self.validar()

    @property
    def tipo_equipo(self):
        return self.__tipo_equipo

    @tipo_equipo.setter
    def tipo_equipo(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El tipo de equipo no puede estar vacío.")

        self.__tipo_equipo = valor.strip()

    @property
    def unidades_disponibles(self):
        return self.__unidades_disponibles

    @unidades_disponibles.setter
    def unidades_disponibles(self, valor):
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise ValueError(
                "Las unidades disponibles deben ser un número entero."
            )

        if valor < 0:
            raise ValueError(
                "Las unidades disponibles no pueden ser negativas."
            )

        self.__unidades_disponibles = valor

    @property
    def estado(self):
        return self.__estado

    @estado.setter
    def estado(self, valor):
        if not isinstance(valor, str):
            raise ValueError("El estado debe ser un texto.")

        valor = valor.strip().lower()

        estados_validos = ("nuevo", "bueno", "regular")

        if valor not in estados_validos:
            raise ValueError(
                "El estado debe ser nuevo, bueno o regular."
            )

        self.__estado = valor

    def validar(self):
        """
        Valida los atributos generales y específicos del equipo.
        """

        super().validar()

        self.tipo_equipo = self.__tipo_equipo
        self.unidades_disponibles = self.__unidades_disponibles
        self.estado = self.__estado

        return True

    def validar_parametros(self, cantidad=1, unidades=1):
        """
        Valida la duración del alquiler y la cantidad de equipos
        solicitados.

        Args:
            cantidad (float): Duración del alquiler en horas.
            unidades (int): Cantidad de equipos solicitados.
        """

        if not self.disponible:
            raise ValueError("El servicio de alquiler no está disponible.")

        if (
            isinstance(cantidad, bool)
            or not isinstance(cantidad, (int, float))
        ):
            raise ValueError("La duración debe ser un valor numérico.")

        if not isfinite(cantidad) or cantidad <= 0:
            raise ValueError("La duración debe ser mayor que cero.")

        if isinstance(unidades, bool) or not isinstance(unidades, int):
            raise ValueError("La cantidad de equipos debe ser un entero.")

        if unidades <= 0:
            raise ValueError("Debe solicitar al menos un equipo.")

        if unidades > self.unidades_disponibles:
            raise ValueError(
                "No hay suficientes unidades disponibles para el alquiler."
            )

        return True

    def calcular_costo(
        self,
        cantidad=1,
        descuento=0,
        impuesto=0.19,
        unidades=1
    ):
        """
        Calcula el costo del alquiler según las horas y unidades solicitadas.

        Args:
            cantidad (float): Duración del alquiler en horas.
            descuento (float): Descuento expresado entre 0 y 1.
            impuesto (float): Impuesto expresado entre 0 y 1.
            unidades (int): Cantidad de equipos solicitados.

        Returns:
            float: Costo total del alquiler.
        """

        self.validar_parametros(cantidad, unidades)

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

        subtotal = self.precio_base * cantidad * unidades
        valor_descuento = subtotal * descuento
        subtotal_con_descuento = subtotal - valor_descuento
        valor_impuesto = subtotal_con_descuento * impuesto

        return round(subtotal_con_descuento + valor_impuesto, 2)

    def describir(self):
        """
        Genera una descripción detallada del equipo disponible.
        """

        return (
            f"Nombre: {self.nombre}\n"
            f"Descripción: {self.descripcion}\n"
            f"Tipo de equipo: {self.tipo_equipo}\n"
            f"Precio por hora y unidad: ${self.precio_base:,.2f}\n"
            f"Unidades disponibles: {self.unidades_disponibles}\n"
            f"Estado: {self.estado.capitalize()}\n"
            f"Disponible: {'Sí' if self.disponible else 'No'}"
        )
