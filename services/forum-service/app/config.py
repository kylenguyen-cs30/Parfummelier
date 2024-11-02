from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    USER_SERVICE_URL: str = "http://user-service:5000"
    MONGO_URI: str = "mongodb://mongo:27017/chat_database"
    DATABASE_NAME: str = "chat_database"
    SECRET_KEY: str

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()


# Create a config class for easy access for settinsg
class Config:
    SECRET_KEY = settings.SECRET_KEY
    USER_SERVICE_URL = settings.USER_SERVICE_URL
    MONGO_URI = settings.MONGO_URI
    DATABASE_NAME = settings.DATABASE_NAME
