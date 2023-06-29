"""Magic Methods"""

from __future__ import annotations
from typing import List


# NO MODIFICAR - INICIO
class Article:
    """Agregar los métodos que sean necesarios para que los test funcionen.
    Hint: los métodos necesarios son todos magic methods
    Referencia: https://docs.python.org/3/reference/datamodel.html#basic-customization
    """

    def __init__(self, name: str) -> None:
        self.name = name

    # NO MODIFICAR - FIN

    def __repr__(self) -> str:
        return f"Article('{self.name}')"

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other: Article) -> bool:
        if type(other) is not Article:
            return NotImplemented
        return self.name == other.name


# NO MODIFICAR - INICIO
class ShoppingCart:
    """Agregar los métodos que sean necesarios para que los test funcionen.
    Hint: los métodos necesarios son todos magic methods
    Referencia: https://docs.python.org/3/reference/datamodel.html#basic-customization
    """

    def __init__(self, articles: List[Article] = None) -> None:
        if articles is None:
            self.articles = []
        else:
            self.articles = articles

    def add(self, article: Article) -> ShoppingCart:
        self.articles.append(article)
        return self

    def remove(self, remove_article: Article) -> ShoppingCart:
        new_articles = []

        for article in self.articles:
            if article != remove_article:
                new_articles.append(article)

        self.articles = new_articles

        return self

    # NO MODIFICAR - FIN

    def __repr__(self) -> str:
        # Opción 1:
        return "ShoppingCart([" + ", ".join(repr(article) for article in self.articles) + "])"

        # Opción 2:
        # resultado = "ShoppingCart(["
        # for i in range(len(self.articles)):
        #     if i > 0:
        #         resultado += ", "
        #     resultado += repr(self.articles[i])
        # resultado += "])"
        # return resultado

        # Opción 3:
        # return "ShoppingCart(" + str([eval(repr(article)) for article in self.articles]) + ")"

    def __str__(self) -> str:
        # Opción 1:
        if len(self.articles) > 0:
            return "['" + "', '".join(str(article) for article in self.articles) + "']"
        return "[]"

        # Opción 2:
        # resultado = "["
        # for i in range(len(self.articles)):
        #     if i > 0:
        #         resultado += ", "
        #     resultado += "'" + str(self.articles[i]) + "'"
        # resultado += "]"
        # return resultado

        # Opción 3:
        # return str([str(article) for article in self.articles])

    def __eq__(self, other: ShoppingCart) -> bool:
        if type(other) is not ShoppingCart:
            return NotImplemented
        return self.articles.sort(key=str) == other.articles.sort(key=str)

    def __add__(self, other: ShoppingCart) -> ShoppingCart:
        if type(other) is not ShoppingCart:
            return NotImplemented
        for article in other.articles:
            self.add(article)
        return self


# NO MODIFICAR - INICIO

manzana = Article("Manzana")
pera = Article("Pera")
tv = Article("Television")

# Test de conversión a String
assert str(ShoppingCart().add(manzana).add(pera)) == "['Manzana', 'Pera']"

# Test de reproducibilidad
carrito = ShoppingCart().add(manzana).add(pera)
assert carrito == eval(repr(carrito))

# Test de igualdad
assert ShoppingCart().add(manzana) == ShoppingCart().add(manzana)

# Test de remover objeto
assert ShoppingCart().add(tv).add(pera).remove(tv) == ShoppingCart().add(pera)

# Test de igualdad con distinto orden
assert ShoppingCart().add(tv).add(pera) == ShoppingCart().add(pera).add(tv)

# Test de suma
combinado = ShoppingCart().add(manzana) + ShoppingCart().add(pera)
assert combinado == ShoppingCart().add(manzana).add(pera)

# NO MODIFICAR - FIN
