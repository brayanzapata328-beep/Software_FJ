
from abc import ABC, abstractmethod
from uuid import uuid4


class Entidad(ABC):
    """Clase abstracta que representa una entidad general dentro del sistema Software FJ."""

    def __init__(self):
        """Inicializa una entidad con un identificador único."""
        self.__id = str(uuid4())

    @property
    def id(self):
        """Permite consultar el identificador de la entidad."""
        return self.__id

    @abstractmethod
    def validar(self):
        """Método abstracto que deberán implementar las clases que hereden de Entidad."""
        pass
