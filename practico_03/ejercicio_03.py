"""Dataclasses"""


class Persona:
    """Clase con los siguientes miembros:

    Atributos de instancia:
    - nombre: str
    - edad: int
    - sexo (H hombre, M mujer): str
    - peso: float
    - altura: float

    Métodos:
    - es_mayor_edad(): indica si es mayor de edad, devuelve un booleano.
    """

    def __init__(self, nombre: str, edad: int = 0, sexo: str = "-", peso: float = 0, altura: float = 0):
        self.nombre = nombre
        self.edad = edad if edad >= 0 else 0
        self.sexo = sexo if sexo in ["H", "M"] else "-"
        self.peso = peso if peso >= 0 else 0
        self.altura = altura if altura >= 0 else 0

    def es_mayor_edad(self) -> bool:
        return self.edad >= 18


# NO MODIFICAR - INICIO
assert Persona("Juan", 18, "H", 85, 175.9).es_mayor_edad()
assert not Persona("Julia", 16, "M", 65, 162.4).es_mayor_edad()
# NO MODIFICAR - FIN


###############################################################################


from dataclasses import dataclass


@dataclass
class Persona:
    """Re-Escribir utilizando DataClasses"""

    nombre: str
    edad: int = 0
    sexo: str = "-"
    peso: float = 0
    altura: float = 0

    def es_mayor_edad(self) -> bool:
        return self.edad >= 18


# NO MODIFICAR - INICIO
assert Persona("Juan", 18, "H", 85, 175.9).es_mayor_edad()
assert not Persona("Julia", 16, "M", 65, 162.4).es_mayor_edad()
# NO MODIFICAR - FIN
