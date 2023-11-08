"""Base de Datos - Creación de Clase en ORM"""


from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String


class Base(DeclarativeBase):
    pass


class Socio(Base):
    """Implementar un modelo Socio a traves de Alchemy que cuente con los siguientes campos:
        - id: entero (clave primaria, auto-incremental, unico)
        - dni: entero (unico)
        - nombre: string (longitud 250)
        - apellido: string (longitud 250)
    """
    __tablename__ = 'socio'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    dni: Mapped[int] = mapped_column(unique=True)
    nombre: Mapped[str] = mapped_column(String(250))
    apellido: Mapped[str] = mapped_column(String(250))

    def __repr__(self) -> str:
        return f"Socio(id={self.id!r}, dni={self.dni!r}, nombre={self.nombre!r}, apellido={self.apellido!r})"
