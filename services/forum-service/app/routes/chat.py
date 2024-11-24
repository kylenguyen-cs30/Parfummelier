from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect,
    HTTPException,
    status,
    Depends,
)
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config import Config
from app.models.chat import ChatroomCreate, Message
from app.services.chat import ChatService
from typing import List
from bson import ObjectId

import logging
import jwt


logger = logging.getLogger(__name__)

# Initialize FastAPI router
router = APIRouter()
# Initialize chat service singleton
chat_service = ChatService()
# Security
security = HTTPBearer()


# Dependency function for user authentication
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Dependency function for user authentication

    Returns:
        credentials : HTTP Authorization credentials containing the token
    """
    try:
        token_str = credentials.credentials
        if token_str.startswith("Bearer "):
            token_str = token_str[7:]

        payload = jwt.decode(token_str, Config.SECRET_KEY, algorithms=["HS256"])

        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token"
        )


# Health check endpoint
@router.get("/")
async def health_check():
    """
    Health check endpoint to verify if the chat service is running
    Returns:
        dict: Status and service information
    """
    return {"status": "online", "service": "chat"}


# Create new chatroom endpoint
@router.post("/chatroom", status_code=status.HTTP_201_CREATED)
async def create_chatroom(
    chatroom: ChatroomCreate, current_user: dict = Depends(get_current_user)
):
    """Creates a new chatroom with specified participants"""

    try:
        # Get the current user's ID
        current_user_id = current_user["user_id"]

        # Create participant list with both users
        participants = list(set(chatroom.participants + [current_user_id]))

        # Sort participants to ensure consistent lookup
        participants.sort()

        result = await chat_service.create_chatroom({"participants": participants})

        # Verify the chatroom was created
        created_room = await chat_service.db.chatrooms.find_one(
            {"_id": ObjectId(result["chatroom_id"])}
        )
        logger.info(f"Verified created chatroom: {created_room}")
        return {"chatroom_id": result["chatroom_id"]}
    except Exception as e:
        logger.error(f"Error creating chatroom: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# Get user chatrooms
@router.get("/user/chatrooms")
async def get_user_chatrooms(
    current_user: dict = Depends(get_current_user),
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """Get all chatrooms for the current user"""
    try:
        user_id = current_user["user_id"]

        # Get the token
        token_str = credentials.credentials
        if token_str.startswith("Bearer "):
            token_str = token_str[7:]

        chatrooms = await chat_service.get_user_chatrooms(
            user_id=user_id, access_token=token_str
        )
        return {"chatrooms": chatrooms}
    except Exception as e:
        logger.error(f"Error getting user chatrooms: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# Get messages for a specific chatroom
@router.get("/chatroom/{chatroom_id}/messages")
async def get_messages(
    chatroom_id: str, current_user: dict = Depends(get_current_user)
):
    """Get messages for a specific chatroom"""
    try:
        if not ObjectId.is_valid(chatroom_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid chatroom ID format",
            )
        messages = await chat_service.get_messages(chatroom_id)
        return {"messages": messages}
    except Exception as e:
        logger.error(f"Error getting messages: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# WebSocket endpoint
@router.websocket("/ws/{chatroom_id}")
async def websocket_endpoint(websocket: WebSocket, chatroom_id: str):
    """WebSocket endpoint for chat connections"""
    try:
        token = websocket.query_params.get("token")
        logger.info(f"WebSocket connection attempt for room {chatroom_id}")

        if not token:
            logger.warning("No token provided in WebSocket connection")
            await websocket.close(code=4001, reason="No token provided")
            return

        # Verify token before accepting connection
        try:
            jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        except jwt.InvalidTokenError:
            await websocket.close(code=4001, reason="Invalid token")
            return

        await websocket.accept()
        logger.info(f"WebSocket connection accepted for room {chatroom_id}")

        try:
            if chatroom_id not in chat_service.active_connections:
                chat_service.active_connections[chatroom_id] = set()
            chat_service.active_connections[chatroom_id].add(websocket)
            logger.info(f"Added to active connections for room {chatroom_id}")

            while True:
                try:
                    data = await websocket.receive_json()
                    await chat_service.handle_message(chatroom_id, data, token)
                except WebSocketDisconnect:
                    logger.info(f"WebSocket disconnected for room {chatroom_id}")
                    break
                except Exception as e:
                    logger.error(f"Error handling message: {e}")
                    await websocket.send_json(
                        {"type": "error", "content": "Failed to process message"}
                    )
        finally:
            if chatroom_id in chat_service.active_connections:
                chat_service.active_connections[chatroom_id].remove(websocket)
                if not chat_service.active_connections[chatroom_id]:
                    del chat_service.active_connections[chatroom_id]
                logger.info(f"Cleaned up connection for room {chatroom_id}")

    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
        if websocket.client_state.CONNECTED:
            await websocket.close(code=1011)


@router.get("/chatroom/{chatroom_id}/info")
async def get_chatroom_info(
    chatroom_id: str,
    current_user: dict = Depends(get_current_user),
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """Get information about a specific chatroom"""
    try:
        logger.info(f"Getting info for chatroom {chatroom_id}")

        # Get the token from credentials
        token_str = credentials.credentials
        if token_str.startswith("Bearer "):
            token_str = token_str[7:]

        if not ObjectId.is_valid(chatroom_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid chatroom ID format",
            )

        # Get the MongoDB collection
        collection = chat_service.db.chatrooms

        # Convert string ID to ObjectId
        room_id = ObjectId(chatroom_id)
        logger.info(f"Looking for chatroom with ID: {room_id}")

        # Find the chatroom using motor's async find_one
        chatroom = await collection.find_one({"_id": room_id})

        # Debug logs
        if chatroom:
            logger.info(f"Found chatroom: {chatroom}")
        else:
            logger.error(f"No chatroom found with ID: {room_id}")
            # Let's check what chatrooms exist
            all_rooms = await collection.find({}).to_list(None)
            logger.info(f"Available chatrooms: {all_rooms}")

        if not chatroom:
            logger.error(f"Chatroom {chatroom_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Chatroom not found"
            )

        logger.info(f"Found chatroom with participants: {chatroom['participants']}")

        # Get other participant's info
        try:
            current_user_id = current_user["user_id"]
            logger.info(f"Current user ID: {current_user_id}")
            logger.info(f"All participants: {chatroom['participants']}")

            other_user_id = next(
                pid for pid in chatroom["participants"] if pid != current_user_id
            )

            logger.info(f"Getting info for other user: {other_user_id}")

            # Pass both user_id and access token to get_user_chat_info
            other_user = await chat_service.user_service.get_user_chat_info(
                identifier=other_user_id,
                access_token=token_str,
            )

            if not other_user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Other user not found"
                )

            response = {
                "roomId": str(chatroom["_id"]),
                "otheruser": {
                    "id": other_user["user_id"],
                    "userName": other_user["userName"],
                    "firstName": other_user["firstName"],
                    "lastName": other_user["lastName"],
                },
            }

            logger.info(f"Successfully got chatroom info: {response}")
            return response

        except StopIteration:
            logger.error(f"No other participant found in chatroom {chatroom_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Other participant not found in chatroom",
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting chatroom info: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get chatroom info: {str(e)}",
        )
