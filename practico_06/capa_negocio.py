# Implementar los metodos de la capa de negocio de socios.

from practico_05.ejercicio_01 import Socio
from practico_05.ejercicio_02 import DatosSocio


class DniRepetido(Exception):
    """Se levanta cuando el dni del socio ya esta registrado"""
    def __init__(self, dni, message= "El DNI del socio ya existe"):
        self.dni = dni
        self.message = message
        super().__init__(self.message)

class LongitudInvalida(Exception):
    """Se levanta cuando se excede el limite maximo de caracteres
    o no se alcanza el limite minimo caracteres"""
    def __init__(self, longitud, message= "El nombre o apellido no está dentro del rango (3, 15)"):
        self.longitud = longitud
        self.message = message
        super().__init__(self.message)


class MaximoAlcanzado(Exception):
    """Se levanta cuando se llega al maximo de socios"""
    def __init__(self, message= "Se excedió la capacidad máxima de socios"):
        self.message = message
        super().__init__(self.message)


class NegocioSocio(object):

    MIN_CARACTERES = 3
    MAX_CARACTERES = 15
    MAX_SOCIOS = 200

    def __init__(self):
        self.datos = DatosSocio()

    def buscar(self, id_socio):
        """
        Devuelve la instancia del socio, dado su id.
        Devuelve None si no encuentra nada.
        :rtype: Socio
        """
        return self.datos.buscar(id_socio)

    def buscar_dni(self, dni_socio):
        """
        Devuelve la instancia del socio, dado su dni.
        Devuelve None si no encuentra nada.
        :rtype: Socio
        """
        return self.datos.buscar_dni(dni_socio)

    def todos(self):
        """
        Devuelve listado de todos los socios.
        :rtype: list
        """
        return self.datos.todos()

    def alta(self, socio):
        """
        Da de alta un socio.
        Se deben validar las 3 reglas de negocio primero.
        Si no validan, levantar la excepcion correspondiente.
        Devuelve True si el alta fue exitoso.
        :type socio: Socio
        :rtype: bool
        """
        if self.regla_1(socio) and self.regla_2(socio) and self.regla_3():
            self.datos.alta(socio)
            return True
        else:
            return False

    def baja(self, id_socio):
        """
        Borra el socio especificado por el id.
        Devuelve True si el borrado fue exitoso.
        :rtype: bool
        """
        return self.datos.baja(id_socio)

    def modificacion(self, socio):
        """
        Modifica un socio.
        Se debe validar la regla 2 primero.
        Si no valida, levantar la excepcion correspondiente.
        Devuelve True si la modificacion fue exitosa.
        :type socio: Socio
        :rtype: bool
        """
        if self.regla_2(socio):
            self.datos.modificacion(socio)
            return True
        else:
            return False

    def regla_1(self, socio):
        """
        Validar que el DNI del socio es unico (que ya no este usado).
        :type socio: Socio
        :raise: DniRepetido
        :return: bool
        """
        if self.buscar_dni(socio.dni) is not None:
            raise DniRepetido(socio.dni)
        return True

    def regla_2(self, socio):
        """
        Validar que el nombre y el apellido del socio cuenten con mas de 3 caracteres pero menos de 15.
        :type socio: Socio
        :raise: LongitudInvalida
        :return: bool
        """
        if not self.MIN_CARACTERES <= len(socio.nombre) <= self.MAX_CARACTERES:
            raise LongitudInvalida(len(socio.nombre))
        if not self.MIN_CARACTERES <= len(socio.apellido) <= self.MAX_CARACTERES:
            raise LongitudInvalida(len(socio.apellido))
        return True

    def regla_3(self):
        """
        Validar que no se esta excediendo la cantidad maxima de socios.
        :raise: MaximoAlcanzado
        :return: bool
        """
        if len(self.todos()) >= self.MAX_SOCIOS:
            raise MaximoAlcanzado()
        return True
