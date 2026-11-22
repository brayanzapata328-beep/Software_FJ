
from math import isfinite

from modelos.servicio import Servicio


class ServicioAsesoria(Servicio):
    """
    Representa el servicio de asesorías especializadas
    ofrecido por la empresa Software FJ.

    Hereda de Servicio e incorpora características como
    la especialidad, el profesional y la modalidad.
    """

    def __init__(
        self,
        nombre,
        descripcion,
        precio_base,
        especialidad,
        profesional,
        modalidad,
        disponible=True
    ):
        """
        Inicializa un servicio de asesoría.

        Args:
            nombre (str): Nombre de la asesoría.
            descripcion (str): Descripción del servicio.
            precio_base (float): Precio por hora de asesoría.
            especialidad (str): Área de conocimiento.
            profesional (str): Profesional encargado.
            modalidad (str): Modalidad virtual o presencial.
            disponible (bool): Estado de disponibilidad.
        """

        super().__init__(
            nombre,
            descripcion,
            precio_base,
            disponible
        )

        self.especialidad = especialidad
        self.profesional = profesional
        self.modalidad = modalidad

        self.validar()

    @property
    def especialidad(self):
        return self.__especialidad

    @especialidad.setter
    def especialidad(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError(
                "La especialidad no puede estar vacía."
            )

        self.__especialidad = valor.strip()

    @property
    def profesional(self):
        return self.__profesional

    @profesional.setter
    def profesional(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError(
                "El nombre del profesional no puede estar vacío."
            )

        self.__profesional = valor.strip()

    @property
    def modalidad(self):
        return self.__modalidad

    @modalidad.setter
    def modalidad(self, valor):
        if not isinstance(valor, str):
            raise ValueError(
                "La modalidad debe ser un texto."
            )

        valor = valor.strip().lower()

        modalidades_validas = ("virtual", "presencial")

        if valor not in modalidades_validas:
            raise ValueError(
                "La modalidad debe ser virtual o presencial."
            )

        self.__modalidad = valor

    def validar(self):
        """
        Valida los atributos generales y específicos
        del servicio de asesoría.
        """

        super().validar()

        self.especialidad = self.__especialidad
        self.profesional = self.__profesional
        self.modalidad = self.__modalidad

        return True

    def validar_parametros(self, cantidad=1):
        """
        Valida la duración de la asesoría y la disponibilidad.

        Args:
            cantidad (float): Duración de la asesoría en horas.
        """

        if not self.disponible:
            raise ValueError(
                "El servicio de asesoría no está disponible."
            )

        if (
            isinstance(cantidad, bool)
            or not isinstance(cantidad, (int, float))
        ):
            raise ValueError(
                "La duración debe ser un valor numérico."
            )

        if not isfinite(cantidad) or cantidad <= 0:
            raise ValueError(
                "La duración debe ser mayor que cero."
            )

        return True

    def calcular_costo(
        self,
        cantidad=1,
        descuento=0,
        impuesto=0.19
    ):
        """
        Calcula el costo de la asesoría según su duración.

        Args:
            cantidad (float): Duración en horas.
            descuento (float): Descuento expresado entre 0 y 1.
            impuesto (float): Impuesto expresado entre 0 y 1.

        Returns:
            float: Costo total de la asesoría.
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

        return round(
            subtotal_con_descuento + valor_impuesto,
            2
        )

    def describir(self):
        """
        Genera una descripción detallada del servicio
        de asesoría.
        """

        return (
            f"Nombre: {self.nombre}\n"
            f"Descripción: {self.descripcion}\n"
            f"Especialidad: {self.especialidad}\n"
            f"Profesional: {self.profesional}\n"
            f"Modalidad: {self.modalidad.capitalize()}\n"
            f"Precio por hora: ${self.precio_base:,.2f}\n"
            f"Disponible: {'Sí' if self.disponible else 'No'}"
        )
