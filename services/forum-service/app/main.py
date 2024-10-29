from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from app.routes.chat import router as chat_router
from app.config import settings

app = FastAPI(title="Forum Service" , version="1.0.0")

# CORS config 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(chat_router , prefix="/chat" , tags=["chat"])


