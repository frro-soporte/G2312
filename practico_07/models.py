from Database import Database

db = Database.db

class Socio(db.Model):
    """Implementar un modelo Socio a traves de Alchemy que cuente con los siguientes campos:
        - id_socio: entero (clave primaria, auto-incremental, unico)
        - dni: entero (unico)
        - nombre: string (longitud 250)
        - apellido: string (longitud 250)
    """
    id = db.Column(db.Integer, primary_key = True)
    dni = db.Column(db.Integer, unique = True)
    nombre = db.Column(db.String(250))
    apellido = db.Column(db.String(250))