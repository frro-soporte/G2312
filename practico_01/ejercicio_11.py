"""Sum, Compresión de Listas, Map, Filter, Reduce."""

from typing import Iterable
from functools import reduce


def suma_cubo_pares_for(numeros: Iterable[int]) -> int:
    """Toma una lista de números, los eleva al cubo, y devuelve la suma de
    los elementos pares.

    Restricción: Utilizar dos bucles for, uno para elevar al cubo y otro para
    separar los pares.
    """
    suma = 0
    for num in numeros:
        cubo = num ** 3
        if cubo % 2 == 0:
            suma += cubo
    return suma


# NO MODIFICAR - INICIO
assert suma_cubo_pares_for([1, 2, 3, 4, 5, 6]) == 288
# NO MODIFICAR - FIN


###############################################################################


def suma_cubo_pares_sum_list(numeros: Iterable[int]) -> int:
    """Re-Escribir utilizando comprensión de listas (debe resolverse en 1 línea)
    y la función built-in sum.

    Referencia: https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
    Referencia: https://docs.python.org/3/library/functions.html#sum
    """
    return sum([num ** 3 for num in numeros if (num ** 3) % 2 == 0])


# NO MODIFICAR - INICIO
assert suma_cubo_pares_sum_list([1, 2, 3, 4, 5, 6]) == 288
# NO MODIFICAR - FIN


###############################################################################


def suma_cubo_pares_sum_gen(numeros: Iterable[int]) -> int:
    """Re-Escribir utilizando expresiones generadoras (debe resolverse en 1 línea)
    y la función sum.

    Referencia: https://docs.python.org/3/reference/expressions.html#generator-expressions
    """
    return sum((num ** 3 for num in numeros if (num ** 3) % 2 == 0))


# NO MODIFICAR - INICIO
assert suma_cubo_pares_sum_gen([1, 2, 3, 4, 5, 6]) == 288
# NO MODIFICAR - FIN


###############################################################################

# PARTE 2
# A continuación se introduce el concepto de Lambdas (Funciones anónimas),
# Escribir las funciones lambdas que corresponda en cada línea
# Referencia: https://docs.python.org/3/reference/expressions.html#lambda

numeros = [1, 2, 3, 4, 5, 6]


# Escribir una función lambda que eleve los elementos al cubo

numeros_al_cubo = lambda numeros: [num ** 3 for num in numeros]


# Escribir una función lambda que permita filtrar todos los elementos pares

numeros_al_cubo_pares = lambda numeros: [num ** 3 for num in numeros if (num ** 3) % 2 == 0]


# Escribir una función Lambda que sume todos los elementos

suma_numeros_al_cubo_pares = lambda numeros: sum([num ** 3 for num in numeros if (num ** 3) % 2 == 0])


# Escribir una función Lambda que permita ordenar los elementos de la numeros
# en base a si son pares o impares

numeros_ordenada = lambda numeros: sorted(numeros, key=lambda num: num % 2, reverse=True)


# NO MODIFICAR - INICIO
assert numeros_al_cubo(numeros) == [1, 8, 27, 64, 125, 216]
assert numeros_al_cubo_pares(numeros) == [8, 64, 216]
assert suma_numeros_al_cubo_pares(numeros) == 288
assert numeros_ordenada(numeros) == [1, 3, 5, 2, 4, 6]
# NO MODIFICAR - FIN
