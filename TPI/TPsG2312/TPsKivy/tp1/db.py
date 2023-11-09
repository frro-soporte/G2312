import sqlite3


def crear_tabla():
    con = sqlite3.connect("myapp.db")
    try:
        con.execute(
            """CREATE TABLE producto (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT(30) NOT NULL UNIQUE,
                descripcion TEXT(100),
                categoria TEXT(20),
                precio REAL NOT NULL,
                stock INTEGER
            )"""
        )
    except sqlite3.OperationalError as e:
        if str(e) != "table producto already exists":
            print(e.sqlite_errorname, e.sqlite_errorcode)
            raise e
        else:
            print("Error ignorado: la tabla producto ya existe")
    finally:
        con.close()


def crear_producto(nombre, descripcion, categoria, precio, stock):
    con = sqlite3.connect("myapp.db")
    try:
        con.execute(
            """INSERT INTO producto (nombre, descripcion, categoria, precio, stock)
            VALUES (?,?,?,?,?)""",
            (nombre, descripcion, categoria, precio, stock)
        )
        con.commit()
        print("alta con exito:", nombre, descripcion, categoria, precio, stock)
    finally:
        con.close()


def buscar_producto_por_nombre(nombre):
    crear_tabla()
    con = sqlite3.connect("myapp.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    try:
        cur.execute(
            """SELECT id, nombre, categoria, stock FROM producto WHERE nombre LIKE ?""",
            ("%" + nombre + "%",)
        )
        print("busqueda con exito:", nombre)
        return cur.fetchall()
    finally:
        con.close()


def get_producto_por_id(id):
    con = sqlite3.connect("myapp.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    try:
        cur.execute(
            """SELECT * FROM producto WHERE id = ?""",
            (id,)
        )
        return cur.fetchone()
    finally:
        con.close()


def borrar_producto_por_id(id):
    con = sqlite3.connect("myapp.db")
    cur = con.cursor()
    try:
        cur.execute(
            """DELETE FROM producto WHERE id = ?""",
            (id,)
        )
        con.commit()
        print(f"ID {id} borrado con exito")
        return cur.fetchall()
    finally:
        con.close()


def borrar_producto_por_nombre(nombre):
    con = sqlite3.connect("myapp.db")
    cur = con.cursor()
    try:
        cur.execute(
            """DELETE FROM producto WHERE nombre = ?""",
            (nombre,)
        )
        con.commit()
        print(f"'{nombre}' borrado con exito")
        return cur.fetchall()
    finally:
        con.close()


def modificar_producto_por_id(id, nombre, descripcion, categoria, precio, stock):
    con = sqlite3.connect("myapp.db")
    cur = con.cursor()
    try:
        cur.execute(
            """UPDATE producto SET
            nombre = ?, 
            descripcion = ?, 
            categoria = ?, 
            precio = ?, 
            stock = ? 
            WHERE id = ?""",
            (nombre, descripcion, categoria, precio, stock, id)
        )
        con.commit()
        print(f"'{nombre}' modificado con exito")
        return cur.fetchall()
    finally:
        con.close()
