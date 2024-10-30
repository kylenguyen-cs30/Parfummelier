from fastapi import WebSocket
from app.database import Database
# from app.config import settings
from typing import Dict, Set
from datetime import datetime
from .user_service import UserService
from bson import ObjectId

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
    
    
    # async def disconnect(self, websocket: WebSocket, chatroom_id: str):
    #     """
    #     Handle WebSocket disconnection from a chatroom.
    #     """
    #     self.active_connections[chatroom_id].remove(websocket)
    #     if not self.active_connections[chatroom_id]:
    #         del self.active_connections[chatroom_id]
    
    async def create_chatroom(self, chatroom_data: dict):
        """
        Create a new chatroom in the database.
        """
        try:
            result = self.db.chatrooms.insert_one(chatroom_data)
            return {"chatroom_id": str(result.inserted_id)}
        except Exception as e:
            logger.error(f"Error creating chatroom: {str(e)}")
            raise    

    async def get_messages(self, chatroom_id: str):
        """
        Retrieve all messages for a specific chatroom.
        """
        try:
            # Convert chatroom_id to ObjectId for MongoDB query
            room_id = ObjectId(chatroom_id)
            messages = list(self.db.messages.find({"chatroom_id": str(room_id)}))
            for msg in messages:
                msg["_id"] = str(msg["_id"])
            return messages
        except Exception as e:
            logger.error(f"Error getting messages: {str(e)}")
            raise    



    # Handle message and store message into mongodb 
    async def handle_message(self, chatroom_id: str, data: dict, access_token: str):
        try:
            logger.info(f"Processing message for chatroom {chatroom_id}")
            logger.info(f"Message data: {data}")

            # Get user info from token
            user_info = await self.user_service.get_user_chat_info(access_token)
            logger.info(f"Retrieved user info: {user_info}")

            # Validate message format
            if "content" not in data:
                raise ValueError("Message must contain 'content' field")

            # Create message document
            message = {
                "chatroom_id": chatroom_id,
                "user_id": user_info["user_id"],
                "userName": user_info["userName"],
                "firstName": user_info["firstName"],
                "lastName": user_info["lastName"],
                "content": data["content"],
                "timestamp": datetime.now()
            }
            
            # Store in database
            result = self.db.messages.insert_one(message)
            message["_id"] = str(result.inserted_id)
            message["timestamp"] = message["timestamp"].isoformat()
            
            # Broadcast
            await self.broadcast(chatroom_id, message)
            
        except Exception as e:
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
            disconnected = set()

            # Log the broadcast attempt
            logger.info(f"Broadcasting message {message.get('_id')} to room {chatroom_id}")

            for connection in self.active_connections[chatroom_id]:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    logger.error(f"Error broadcasting message: {e}")
                    disconnected.add(connection)
            
            # Remove any disconnected clients
            for connection in disconnected:
                self.active_connections[chatroom_id].remove(connection)
                logger.info(f"Removed disconnected client from room {chatroom_id}")
            if not self.active_connections[chatroom_id]:
                del self.active_connections[chatroom_id]
                logger.info(f"Removed empty room {chatroom_id}")



    async def cleanup(self):
        """
        Clean up resources when shutting down.
        Closes user service client if using persistent connection.
        """
        await self.user_service.close()
