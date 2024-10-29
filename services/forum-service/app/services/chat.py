from fastapi import WebSocket
from app.database import Database
from app.config import settings
from typing import Dict, Set
import json

class ChatService:
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        self.db = Database.get_db()
    
    async def connect(self, websocket: WebSocket, chatroom_id: str):
        await websocket.accept()
        if chatroom_id not in self.active_connections:
            self.active_connections[chatroom_id] = set()
        self.active_connections[chatroom_id].add(websocket)
    
    async def disconnect(self, websocket: WebSocket, chatroom_id: str):
        self.active_connections[chatroom_id].remove(websocket)
        if not self.active_connections[chatroom_id]:
            del self.active_connections[chatroom_id]
    
    async def create_chatroom(self, chatroom_data: dict):
        result = self.db.chatrooms.insert_one(chatroom_data)
        return {"chatroom_id": str(result.inserted_id)}
    
    async def get_messages(self, chatroom_id: str):
        messages = list(self.db.messages.find({"chatroom_id": chatroom_id}))
        for msg in messages:
            msg["_id"] = str(msg["_id"])
        return messages
    
    async def handle_message(self, chatroom_id: str, data: dict):
        message = {
            "chatroom_id": chatroom_id,
            "user_id": data["userId"],
            "content": data["content"]
        }
        self.db.messages.insert_one(message)
        message["_id"] = str(message["_id"])
        await self.broadcast(chatroom_id, message)
    
    async def broadcast(self, chatroom_id: str, message: dict):
        if chatroom_id in self.active_connections:
            for connection in self.active_connections[chatroom_id]:
                await connection.send_json(message)
