from models import Socio
from Database import Database

class DataSocio():
    @classmethod
    def get_all_socios(cls):
        socios = Socio.query.order_by('id')
        return socios

    @classmethod
    def get_one(cls, id):
        socio = Socio.query.get_or_404(id)
        return socio

    @classmethod
    def add_socio(cls, socio):
        Database.db.session.add(socio)
        Database.db.session.commit()