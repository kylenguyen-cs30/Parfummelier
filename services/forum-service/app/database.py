from pymongo import MongoClient
from pymongo.database import Database as MongoDatabase
from app.config import settings
from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import AgnosticDatabase


# NOTE:
# ----------------------------------------------------------------------#
# Agnostic is database migrations system that is agnostic to programming
# language, framework and database system.
# ----------------------------------------------------------------------#


# NOTE:
# ----------------------------------------------------------------------#
# AgnosticIOClient is an asynchronous MongoDB driver provided by Motor
# library, designed specifically for use with asyncio-based Python
# Application. It allows your application to interact with MongoDB
# database asynchrnously, which is crucial for building effiecient and
# scalable web applications
# ----------------------------------------------------------------------#


# NOTE:
# ----------------------------------------------------------------------#
# Agnostic Database is part of the Motor Lib is designed to provide an
# asynchornous interface for MonggoDB database operations that is agnostic
# to the specific async frameworks being used.
# Agnostic Database is an abstract base class that represent a MongoDB
# database and provides asynchronous methods for database operations
# ----------------------------------------------------------------------#


import logging

logger = logging.getLogger(__name__)


class Database:
    client: MongoClient = None
    db: AgnosticDatabase = None

    @classmethod
    async def init_db(cls):
        """Initialize database with required collections"""
        try:
            if cls.db is None:
                cls.client = AsyncIOMotorClient(settings.MONGO_URI)
                cls.db = cls.client[settings.DATABASE_NAME]

                # List existing collections
                collections = await cls.db.list_collection_names()

                # Create collections if they don't exist
                if "chatrooms" not in collections:
                    await cls.db.create_collection("chatrooms")
                    logger.info("Created chatrooms collection")

                if "messages" not in collections:
                    await cls.db.create_collection("messages")
                    logger.info("Created messages collection")

                logger.info(f"Database initialized: {settings.DATABASE_NAME}")
        except Exception as e:
            logger.error(f"Database initialization error: {e}")
            raise

    @classmethod
    def get_client(cls) -> AsyncIOMotorClient:
        if cls.client is None:
            try:
                cls.client = AsyncIOMotorClient(settings.MONGO_URI)
                logger.info("Created new MongoDB client connection")
            except Exception as e:
                logger.error(f"Failed to create MongoDB client: {e}")
                raise
        return cls.client

    @classmethod
    def get_db(cls) -> AgnosticDatabase:
        if cls.db is None:
            cls.db = cls.get_client()[settings.DATABASE_NAME]
            logger.info(f"Connected to database: {settings.DATABASE_NAME}")
        return cls.db


async def connect_to_mongo():
    try:
        Database.client = AsyncIOMotorClient(settings.MONGO_URI)
        Database.db = Database.client[settings.DATABASE_NAME]
        # Verify connection
        await Database.client.admin.command("ping")
        logger.info("Successfully connected to MongoDB")
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise


async def close_mongo_connection():
    try:
        if Database.client:
            Database.client.close()
            Database.client = None
            Database.db = None
            logger.info("Closed MongoDB connection")
    except Exception as e:
        logger.error(f"Error closing MongoDB connection: {e}")
