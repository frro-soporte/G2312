class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def toDBCollection(self):
        return{
            "Item_buscado": self.name,
            "Precio": self.price,
            "Titulo": self.quantity
        }