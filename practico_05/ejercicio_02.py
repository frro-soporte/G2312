"""Base de Datos - ORM"""

from sqlalchemy import create_engine, select, delete, func, ScalarResult
from sqlalchemy.orm import Session
from practico_05.ejercicio_01 import Base, Socio

from typing import List, Optional, cast


class DatosSocio:

    def __init__(self):
        self._engine = create_engine("sqlite+pysqlite:///practico5.db")
        Base.metadata.create_all(self._engine)
        self._sess = Session(self._engine)

    def __del__(self):  # se ejecuta siempre que termine la ejecución, incluso por error
        self._sess.rollback()
        if self.borrar_todos():
            print("fin - todos los socios borrados")
        else:
            print("fin - no se pudieron borrar socios")

    def buscar(self, id_socio: int) -> Optional[Socio]:
        """Devuelve la instancia del socio, dado su id. Devuelve None si no 
        encuentra nada.
        """
        soc: Optional[Socio] = self._sess.get(Socio, id_socio)
        return soc

    def buscar_dni(self, dni_socio: int) -> Optional[Socio]:
        """Devuelve la instancia del socio, dado su dni. Devuelve None si no 
        encuentra nada.
        """
        soc: Optional[Socio] = self._sess.scalar(
            select(Socio)
            .where(Socio.dni == dni_socio)
        )
        return soc
        
    def todos(self) -> List[Socio]:
        """Devuelve listado de todos los socios en la base de datos."""
        res: ScalarResult[Socio] = self._sess.scalars(select(Socio))
        return list(res)

    def borrar_todos(self) -> bool:
        """Borra todos los socios de la base de datos. Devuelve True si el 
        borrado fue exitoso.
        """
        self._sess.execute(delete(Socio))
        self._sess.commit()
        return True

    def alta(self, socio: Socio) -> Socio:
        """Agrega un nuevo socio a la tabla y lo devuelve"""
        self._sess.add(socio)
        self._sess.commit()
        return socio

    def baja(self, id_socio: int) -> bool:
        """Borra el socio especificado por el id. Devuelve True si el borrado 
        fue exitoso.
        """
        soc = self.buscar(id_socio)
        if soc is None:
            raise ValueError()  # no existe socio con id={id_socio}. no se puede borrar
        self._sess.delete(soc)
        self._sess.commit()
        return True

    def modificacion(self, socio: Socio) -> Socio:
        """Guarda un socio con sus datos modificados. Devuelve el Socio 
        modificado.
        """
        with self._sess.no_autoflush:  # para consultar la base de datos sin hacer update
            soc_por_id = self.buscar(socio.id)
            # se validan casos no cubiertos en los test
            if soc_por_id is None:  # el socio no fue creado en la base de datos
                raise ValueError(f"No existe socio con id={socio.id} en tabla {Socio.__tablename__!r}")
            soc_por_dni = self.buscar_dni(socio.dni)
            if soc_por_dni is not None and soc_por_dni.id != socio.id:  # el dni a guardar es de otro socio
                # las 3 lineas siguientes: guarda el socio modificado a la vez que recupera el original
                # de la base de datos (posiblemente (soc_por_id is socio) == True) para lanzar error descriptivo
                modificado = Socio(id=socio.id, dni=socio.dni, nombre=socio.nombre, apellido=socio.apellido)
                self._sess.rollback()
                raise ValueError(
                    f"Ya existe socio con dni={soc_por_dni.dni} en tabla {Socio.__tablename__!r}. No se puede aplicar"
                    f" la modificación del socio: {soc_por_id} => {modificado}"
                )
            if soc_por_id is not socio:
                soc_por_id.dni = socio.dni
                soc_por_id.nombre = socio.nombre
                soc_por_id.apellido = socio.apellido
        self._sess.commit()
        return soc_por_id
    
    def contar_socios(self) -> int:
        """Devuelve el total de socios que existen en la tabla"""
        cantidad: int = self._sess.scalar(func.count(Socio.id))
        return cantidad


# NO MODIFICAR - INICIO

# Test Creación
datos = DatosSocio()

# Test Alta
socio = datos.alta(Socio(dni=12345678, nombre='Juan', apellido='Perez'))
assert socio.id > 0

# Test Baja
assert datos.baja(socio.id) == True

# Test Consulta
socio_2 = datos.alta(Socio(dni=12345679, nombre='Carlos', apellido='Perez'))
assert datos.buscar(socio_2.id) == socio_2

# Test Buscar DNI
socio_2 = datos.alta(Socio(dni=12345670, nombre='Carlos', apellido='Perez'))
assert datos.buscar_dni(socio_2.dni) == socio_2

# Test Modificación
socio_3 = datos.alta(Socio(dni=12345680, nombre='Susana', apellido='Gimenez'))
socio_3.nombre = 'Moria'
socio_3.apellido = 'Casan'
socio_3.dni = 13264587
datos.modificacion(socio_3)
socio_3_modificado = datos.buscar(socio_3.id)
assert socio_3_modificado.id == socio_3.id
assert socio_3_modificado.nombre == 'Moria'
assert socio_3_modificado.apellido == 'Casan'
assert socio_3_modificado.dni == 13264587

# Test Conteo
assert len(datos.todos()) == 3

# Test Delete
datos.borrar_todos()
assert len(datos.todos()) == 0

# NO MODIFICAR - FIN
