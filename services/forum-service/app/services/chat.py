from fastapi import WebSocket
from app.database import Database
# from app.config import settings
from typing import Dict, Set
from datetime import datetime
from .user_service import UserService

import json
import traceback
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



class ChatService:
    """
    Service class handling chat operations including WebSocket connections,
    message broadcasting, and database operations.
    """

    def __init__(self):
        """
        Initialize the ChatService with empty connections dictionary,
        database connection, and user service.
        """
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        self.db = Database.get_db()
        self.user_service = UserService()
        self.user_info_cache = {}  # Cache for user information
    
    async def connect(self, websocket: WebSocket, chatroom_id: str):
        """
        Handle new WebSocket connection for a chatroom.
        """
        await websocket.accept()
        if chatroom_id not in self.active_connections:
            self.active_connections[chatroom_id] = set()
        self.active_connections[chatroom_id].add(websocket)
    
    async def disconnect(self, websocket: WebSocket, chatroom_id: str):
        """
        Handle WebSocket disconnection from a chatroom.
        """
        self.active_connections[chatroom_id].remove(websocket)
        if not self.active_connections[chatroom_id]:
            del self.active_connections[chatroom_id]
    
    async def create_chatroom(self, chatroom_data: dict):
        """
        Create a new chatroom in the database.
        """
        result = self.db.chatrooms.insert_one(chatroom_data)
        return {"chatroom_id": str(result.inserted_id)}
    
    async def get_messages(self, chatroom_id: str):
        """
        Retrieve all messages for a specific chatroom.
        """
        messages = list(self.db.messages.find({"chatroom_id": chatroom_id}))
        for msg in messages:
            msg["_id"] = str(msg["_id"])
        return messages
    
    # Handle message and store message into mongodb 
    async def handle_message(self, chatroom_id: str, data: dict, access_token: str):
        """
        Process and store a new chat message, then broadcast it.
        Now includes user information from the user service.
        
        Args:
            chatroom_id (str): ID of the chatroom receiving the message
            data (dict): Message data including content
            access_token (str): JWT token for user authentication
        """
        try:

            # Debug logging
            logger.info(f"Processing message for chatroom {chatroom_id}")
            logger.info(f"Message data: {data}")
            logger.info(f"Using token: {access_token}")


            # Get user info from token
            user_info = await self.user_service.get_user_chat_info(access_token)
            logger.info(f"Retrieve user info: {user_info}")

            user_id = user_info["user_id"]

            # Create message document with user info
            message = {
                "chatroom_id": chatroom_id,
                "user_id": user_id,
                "userName": user_info["userName"],
                "firstName": user_info["firstName"],
                "lastName": user_info["lastName"],
                "content": data["content"],
                "timestamp": datetime.now()
            }
            
            # Store message in database
            result = self.db.messages.insert_one(message)
            message["_id"] = str(result.inserted_id)
            message["timestamp"] = message["timestamp"].isoformat()
            
            # Broadcast message to all connected clients
            await self.broadcast(chatroom_id, message)
            
        except Exception as e:
            # Print full error details
            logger.error(f"Error handling message: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            error_message = {
                "type": "error",
                "content": f"Failed to process message: {str(e)}"
            }
            await self.broadcast(chatroom_id, error_message)    


    async def broadcast(self, chatroom_id: str, message: dict):
        """
        Broadcast a message to all connected clients in a chatroom.
        """
        if chatroom_id in self.active_connections:
            for connection in self.active_connections[chatroom_id]:
                await connection.send_json(message)
    
    async def cleanup(self):
        """
        Clean up resources when shutting down.
        Closes user service client if using persistent connection.
        """
        await self.user_service.close()
