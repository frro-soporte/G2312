"""Base de Datos SQL - Búsqueda"""

import datetime
import sqlite3

from practico_04.ejercicio_01 import reset_tabla
from practico_04.ejercicio_02 import agregar_persona


def buscar_persona(id_persona):
    """Implementar la funcion buscar_persona, que devuelve el registro de una 
    persona basado en su id. El return es una tupla que contiene sus campos: 
    id, nombre, nacimiento, dni y altura. Si no encuentra ningun registro, 
    devuelve False."""
    con = sqlite3.connect(
        "practico4.db",
        detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
    )
    cur = con.cursor()
    try:
        formatos_fecha = [
            "date",  # date -> fecha (datetime.date)
            "timestamp",  # timestamp -> fecha y hora (datetime.datetime)
        ]

        persona = None
        for i, formato in enumerate(formatos_fecha, 1):
            try:
                cur.execute(
                    f"""SELECT
                    id_persona,
                    nombre,
                    fecha_nacimiento as "fecha_nac [{formato}]",
                    dni,
                    altura
                    FROM persona WHERE id_persona = ?""",
                    (id_persona,)
                )
                persona = cur.fetchone()
                break
            except ValueError as e:
                if i < len(formatos_fecha):
                    pass  # Error con el formato del campo; probar siguiente formato
                else:
                    raise e
        return persona or False
    finally:
        cur.close()
        con.close()


# NO MODIFICAR - INICIO
@reset_tabla
def pruebas():
    juan = buscar_persona(agregar_persona('juan perez', datetime.datetime(1988, 5, 15), 32165498, 180))
    assert juan == (1, 'juan perez', datetime.datetime(1988, 5, 15), 32165498, 180)
    assert buscar_persona(12345) is False

if __name__ == '__main__':
    pruebas()
# NO MODIFICAR - FIN
