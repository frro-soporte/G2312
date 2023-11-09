from pymongo import MongoClient

MONGO_URI = 'mongodb+srv://Grupo12:1234@tpisoporte.hpywjgm.mongodb.net/?retryWrites=true&w=majority'

def dbConnection():
    client = MongoClient(MONGO_URI)
    db = client["Grupo12DB"]
    return db

