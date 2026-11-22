# Importa ABC y abstractmethod para poder definir clases y métodos abstractos
from abc import ABC, abstractmethod
# Importa uuid4 para generar identificadores únicos universales aleatorios
from uuid import uuid4


# Define la clase abstracta Entidad heredando de ABC
class Entidad(ABC):
    """Clase abstracta que representa una entidad general dentro del sistema Software FJ."""

    # Define el método constructor que se ejecuta al crear una subclase de Entidad
    def __init__(self):
        """Inicializa una entidad con un identificador único."""
        # Genera un UUID versión 4, lo convierte a texto y lo guarda en el atributo privado __id
        self.__id = str(uuid4())

    # Decorador que convierte el método id en una propiedad de solo lectura
    @property
    # Define el getter para consultar el identificador privado de la entidad
    def id(self):
        """Permite consultar el identificador de la entidad."""
        # Retorna el valor almacenado en el atributo privado __id
        return self.__id

    # Decorador que obliga a las clases hijas a implementar este método
    @abstractmethod
    # Define la firma del método abstracto validar para las entidades del sistema
    def validar(self):
        """Método abstracto que deberán implementar las clases que hereden de Entidad."""
        # No ejecuta lógica aquí porque cada clase hija implementará su propia validación
        pass
