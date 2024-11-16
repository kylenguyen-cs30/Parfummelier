from fastapi import WebSocket
from app.database.mongodb import Database
from app.models.chat import ChatroomResponse, PyObjectId

# from app.config import settings
from typing import Dict, Set, List, Optional, Any
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
        """
        try:
            participant_ids = chatroom_data["participants"]
            logger.info(f"Looking for chatroom with participants: {participant_ids}")

            # Look for existing chatroom with these participants
            existing_room = await self.db.chatrooms.find_one(
                {"participants": participant_ids}
            )

            if existing_room:
                logger.info(f"Found existing chatroom: {existing_room['_id']}")
                return {"chatroom_id": str(existing_room["_id"])}

            # Create new chatroom
            current_time = datetime.now()
            new_chatroom = {
                "participants": participant_ids,
                "created_at": current_time,
                "last_message_at": current_time,
            }

            # Insert into database
            result = await self.db.chatrooms.insert_one(new_chatroom)
            chatroom_id = str(result.inserted_id)
            logger.info(f"Created new chatroom with ID: {chatroom_id}")

            # Verify creation
            created_room = await self.db.chatrooms.find_one({"_id": result.inserted_id})

            if not created_room:
                raise Exception("Failed to verify chatroom creation")

            # Log the created room structure
            logger.info(f"Created chatroom structure: {created_room}")

            # Create response using Pydantic model
            response = ChatroomResponse(
                chatroom_id=chatroom_id,
                participants=participant_ids,
                created_at=current_time,
                last_message_at=current_time,
            )

            return response.dict()

        except Exception as e:
            logger.error(f"Error in create_chatroom: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise

    async def get_user_chatrooms(
        self, user_id: int, access_token: Optional[str] = None
    ) -> List[dict]:
        """
        Get all chatrooms for a user with latest message preview.
        """
        try:
            logger.info(f"Fetching chatrooms for user_id: {user_id}")

            # Find all chatrooms where user is a participant
            cursor = self.db.chatrooms.find({"participants": user_id})
            chatrooms = await cursor.to_list(length=None)

            logger.info(f"Found {len(chatrooms)} chatrooms")

            result = []
            for room in chatrooms:
                try:
                    # Get the latest message for this room
                    message_cursor = (
                        self.db.messages.find({"chatroom_id": str(room["_id"])})
                        .sort("timestamp", -1)
                        .limit(1)
                    )
                    latest_messages = await message_cursor.to_list(length=1)
                    # latest_message = latest_messages[0] if latest_messages else None
                    latest_message = None
                    if latest_message:
                        latest_message = latest_message[0]
                        if "_id" in latest_message:
                            latest_message["_id"] = str(latest_message["_id"])
                        if "timestamp" in latest_message:
                            latest_message["timestamp"] = (
                                latest_message["timestamp"].isoformat()
                                if isinstance(latest_message["timestamp"], datetime)
                                else latest_message["timestamp"]
                            )

                    # Get other participant's info
                    try:
                        other_user_id = next(
                            pid for pid in room["participants"] if pid != user_id
                        )

                        logger.info(f"Fetching info for other user: {other_user_id}")

                        # Pass the access token when getting user info
                        other_user = await self.user_service.get_user_chat_info(
                            identifier=other_user_id,
                            access_token=access_token,  # Pass the token here
                        )

                        # Convert datetime objects to ISO format strings
                        last_message_at = room.get(
                            "last_message_at", room["created_at"]
                        )
                        if isinstance(last_message_at, datetime):
                            last_message_at = last_message_at.isoformat()

                        chatroom_preview = {
                            "chatroom_id": str(
                                room["_id"]
                            ),  # Convert ObjectId to string
                            "other_user": {
                                "id": other_user["user_id"],
                                "userName": other_user["userName"],
                                "firstName": other_user["firstName"],
                                "lastName": other_user["lastName"],
                            },
                            "latest_message": latest_message,
                            "last_message_at": last_message_at,
                        }

                        result.append(chatroom_preview)

                    except Exception as user_err:
                        logger.error(
                            f"Error getting user info for {other_user_id}: {user_err}"
                        )
                        continue

                except Exception as room_err:
                    logger.error(f"Error processing room: {room_err}")
                    continue

            return result

        except Exception as e:
            logger.error(f"Error in get_user_chatrooms: {str(e)}")
            raise

    async def get_messages(self, chatroom_id: str):
        """
        Retrieve all messages for a specific chatroom.
        """
        try:
            # Convert chatroom_id to ObjectId for MongoDB query
            room_id = ObjectId(chatroom_id)
            cursor = self.db.messages.find({"chatroom_id": str(room_id)})
            # Convert cursor to list using Motor's to list method
            messages = await cursor.to_list(length=None)

            # Convert ObjectId to string for each messages
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
                "timestamp": datetime.now(),
            }

            # Store in database
            result = await self.db.messages.insert_one(message)
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
                "content": f"Failed to process message: {str(e)}",
            }
            await self.broadcast(chatroom_id, error_message)

    async def update_last_message_time(self, chatroom_id: str):
        """
        Update the last_message_at timestamp for a chatroom
        """
        try:
            result = self.db.chatrooms.update_one(
                {"_id": ObjectId(chatroom_id)},
                {"$set": {"last_message_at": datetime.now()}},
            )

            # Don't await the result winsce it's not a coroutine
            return result

        except Exception as e:
            logger.error(f"Error updating last message time: {str(e)}")

    async def broadcast(self, chatroom_id: str, message: dict):
        """
        Broadcast a message to all connected clients in a chatroom.
        """
        if chatroom_id in self.active_connections:
            disconnected = set()

            # Log the broadcast attempt
            logger.info(f"Broadcasting message to room {chatroom_id}: {message}")

            for connection in self.active_connections[chatroom_id]:
                try:
                    await connection.send_json(message)
                    logger.info("Message sent successfully")
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
