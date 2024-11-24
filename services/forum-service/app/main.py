from app.models import comment
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from app.routes.chat import router as chat_router
from app.routes import chat_router, post_router, comment_router
from app.routes.test import router as test_router

# from app.config import settings
from app.database.mongodb import Database
from app.database.postgresql import engine, Base


import logging

logger = logging.getLogger(__name__)

app = FastAPI(title="Forum Service", version="1.0.0")

# CORS config

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# NOTE:
# Initialize the database before FastAPI established
try:
    Base.metadata.create_all(bind=engine)
    logger.info("Postgresql tables created successfully")

except Exception as e:
    logger.info(f"Failed to create Postgresql tables : {e}")
    raise


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    try:
        await Database.init_db()
        logger.info("Database initialized successfully")

        # Postgresql is initialized via SQLAlchemy
        from sqlalchemy import text

        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            logger.info("PostgresSQL initialized and connection verified successfully")

    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Close database connections"""
    if Database.client:
        Database.client.close()
        logger.info("MongoDB connections closed")
    engine.dispose()
    logger.info("PostgreSQL connection closed")


# Check health of the databases
@app.get("/health")
async def health_check():
    """Check health of both databases"""
    try:
        # Check MongoDB
        await Database.init_db()
        mongo_status = "healthy"
    except Exception as e:
        mongo_status = f"unhealthy: {str(e)}"

    try:
        # Check PostgreSQL
        from sqlalchemy import text

        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            postgres_status = "healthy"
    except Exception as e:
        postgres_status = f"unhealthy: {str(e)}"

    return {"mongodb": mongo_status, "postgresql": postgres_status}


app.include_router(chat_router, prefix="/chat", tags=["chat"])
app.include_router(post_router, prefix="/posts", tags=["posts"])
app.include_router(comment_router, prefix="/comments", tags=["comments"])
app.include_router(test_router, prefix="/test", tags=["test"])
