from pymongo import MongoClient
from pymongo.database import Database as MongoDatabase
from app.config import settings

class Database:
    client: MongoClient = None 

    @classmethod 
    def get_client(cls) -> MongoClient:
        if cls.client is None:
            cls.client = MongoClient(settings.MONGO_URI)
        return cls.client
    
    @classmethod
    def get_db(cls) ->MongoDatabase:
        return cls.get_client()[settings.DATABASE_NAME]


async def connect_to_mongo():
    Database.client = MongoClient(settings.MONGO_URI)

async def close_mongo_connection():
    if Database.client:
        Database.client.close()
