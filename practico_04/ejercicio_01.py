"""Base de Datos SQL - Crear y Borrar Tablas"""

import sqlite3

def crear_tabla():
    """Implementar la funcion crear_tabla, que cree una tabla Persona con:
        - IdPersona: Int() (autoincremental)
        - Nombre: Char(30)
        - FechaNacimiento: Date()
        - DNI: Int()
        - Altura: Int()
    """
    con = sqlite3.connect("practico4.db")
    try:
        con.execute("""CREATE TABLE persona (
            id_persona INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT(30),
            fecha_nacimiento DATE,
            dni INTEGER,
            altura INTEGER
        )""")
    except sqlite3.OperationalError as e:
        if str(e) != "table persona already exists":
            print(e.sqlite_errorname, e.sqlite_errorcode)
            raise e
        else:
            print("Error ignorado: la tabla Persona ya existe")
    finally:
        con.close()


def borrar_tabla():
    """Implementar la funcion borrar_tabla, que borra la tabla creada 
    anteriormente."""
    con = sqlite3.connect("practico4.db")
    try:
        con.execute("""DROP TABLE IF EXISTS persona""")
    except sqlite3.OperationalError as e:
        print(e.sqlite_errorname, e.sqlite_errorcode)
        raise e
    finally:
        con.close()


# NO MODIFICAR - INICIO
def reset_tabla(func):
    def func_wrapper():
        crear_tabla()
        func()
        borrar_tabla()
    return func_wrapper
# NO MODIFICAR - FIN
