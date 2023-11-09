from flask_sqlalchemy import SQLAlchemy

class Database():
    db = SQLAlchemy()

    @classmethod
    def configura_conexion(cls) -> str:
        USER_DB = 'postgres'
        PASS_DB = 'cUeNtaPosTgrE2023---'
        URL_DB = 'localhost:5432'
        NAME_DB = 'club_socios'
        FULL_URL_DB = f'postgresql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}'
        return FULL_URL_DB
