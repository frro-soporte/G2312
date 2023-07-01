"""Base de Datos SQL - Creación de tablas auxiliares"""
import sqlite3

from practico_04.ejercicio_01 import borrar_tabla, crear_tabla


def crear_tabla_peso():
    """Implementar la funcion crear_tabla_peso, que cree una tabla PersonaPeso con:
        - IdPersona: Int() (Clave Foranea Persona)
        - Fecha: Date()
        - Peso: Int()
    """
    con = sqlite3.connect("practico4.db")
    try:
        con.execute(
            """CREATE TABLE persona_peso (
                id_persona INTEGER NOT NULL,
                fecha DATE,
                peso INTEGER,
                FOREIGN KEY (id_persona)
                    REFERENCES persona (id_persona)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE
            )"""
        )
    except sqlite3.OperationalError as e:
        if str(e).lower() != "table persona_peso already exists":
            print(e.sqlite_errorname, e.sqlite_errorcode)
            raise e
        else:
            print("Error ignorado: la tabla Persona_Peso ya existe")
    finally:
        con.close()


def borrar_tabla_peso():
    """Implementar la funcion borrar_tabla, que borra la tabla creada 
    anteriormente."""
    con = sqlite3.connect("practico4.db")
    try:
        con.execute("DROP TABLE IF EXISTS persona_peso")
    except sqlite3.OperationalError as e:
        print(e.sqlite_errorname, e.sqlite_errorcode)
        raise e
    finally:
        con.close()


# NO MODIFICAR - INICIO
def reset_tabla(func):
    def func_wrapper():
        crear_tabla()
        crear_tabla_peso()
        func()
        borrar_tabla_peso()
        borrar_tabla()
    return func_wrapper
# NO MODIFICAR - FIN
