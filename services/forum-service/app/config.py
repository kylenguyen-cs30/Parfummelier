from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    USER_SERVICE_URL: str = "http://user-service:5000"
    MONGO_URI: str = "mongodb://mongo:27017/chat_database"
    DATABASE_NAME: str = "chat_database"

    class Config:
        env_file = ".env"

settings = Settings()

