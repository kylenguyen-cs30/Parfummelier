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
        Find existing chatroom or create a new one for given participants.
        
        Args:
            chatroom_data (dict): Dictionary containing 'participants' list
        
        Returns:
            dict: Dictionary containing chatroom_id
        """
        try:
            # Extract and sort participant IDs to ensure consistent room lookup
            participant_ids = sorted(chatroom_data.get('participants', []))
            
            logger.info(f"Looking for chatroom with participants: {participant_ids}")
            
            # Look for existing chatroom with these participants
            existing_room = self.db.chatrooms.find_one({
                "participants": participant_ids
            })
            
            if existing_room:
                logger.info(f"Found existing chatroom: {existing_room['_id']}")
                return {"chatroom_id": str(existing_room["_id"])}
            
            # Create new chatroom if none exists
            new_chatroom = {
                "participants": participant_ids,
                "created_at": datetime.now(),
                "last_message_at": datetime.now()
            }
            
            result = self.db.chatrooms.insert_one(new_chatroom)
            logger.info(f"Created new chatroom: {result.inserted_id}")
            return {"chatroom_id": str(result.inserted_id)}
            
        except Exception as e:
            logger.error(f"Error in create_chatroom: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise    

    async def get_user_chatrooms(self, user_id: int) -> List[dict]:
        """
        Get all chatrooms for a user with latest message preview.
        
        Args:
            user_id (int): ID of the user
            
        Returns:
            List[dict]: List of chatrooms with preview information
        """
        try:
            # Find all chatrooms where user is a participant
            chatrooms = list(self.db.chatrooms.find(
                {"participants": user_id}
            ).sort("last_message_at", -1))

            result = []
            for room in chatrooms:
                # Get the latest message for this room
                latest_message = self.db.messages.find_one(
                    {"chatroom_id": str(room["_id"])},
                    sort=[("timestamp", -1)]
                )
                
                # Get other participant's info
                other_participant_id = next(
                    pid for pid in room["participants"] if pid != user_id
                )
                
                try:
                    # Get user info using your user service
                    other_user = await self.user_service.get_user_chat_info(other_participant_id)
                    
                    result.append({
                        "chatroom_id": str(room["_id"]),
                        "other_user": {
                            "id": other_user["user_id"],
                            "userName": other_user["userName"],
                            "firstName": other_user["firstName"],
                            "lastName": other_user["lastName"]
                        },
                        "latest_message": latest_message if latest_message else None,
                        "last_message_at": room.get("last_message_at", room["created_at"])
                    })
                except Exception as user_err:
                    logger.error(f"Error getting user info for {other_participant_id}: {user_err}")
                    continue
            
            return result
            
        except Exception as e:
            logger.error(f"Error in get_user_chatrooms: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
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
            
            # Update Last_message in chatroom 
            await self.update_last_message_time(chatroom_id)


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

    async def update_last_message_time(self, chatroom_id: str):
        """
        Update the last_message_at timestamp for a chatroom
        """
        try:
            await self.db.chatrooms.update_one(
                {"_id": ObjectId(chatroom_id)},
                {"$set": {"last_message_at": datetime.now()}}
            )
        except Exception as e:
            logger.error(f"Error updating last message time: {str(e)}")


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
