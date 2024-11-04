from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.chat import router as chat_router
from app.config import settings
from app.database import Database
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


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    try:
        await Database.init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Close database connections"""
    if Database.client:
        Database.client.close()
        logger.info("Database connections closed")


app.include_router(chat_router, prefix="/chat", tags=["chat"])
