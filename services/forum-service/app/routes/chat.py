from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, status
from app.models.chat import ChatroomCreate, Message
from app.services.chat import ChatService
from typing import List
from bson import ObjectId

import logging

logger = logging.getLogger(__name__)

# Initialize FastAPI router
router = APIRouter()
# Initialize chat service singleton
chat_service = ChatService()


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
async def create_chatroom(chatroom: ChatroomCreate):
    """
    Creates a new chatroom with specified participants

    Args:
        chatroom (ChatroomCreate): Pydantic model containing participant list

    Returns:
        dict: Created chatroom ID

    Raises:
        HTTPException: If chatroom creation fails
    """
    try:
        result = await chat_service.create_chatroom(chatroom.dict())
        return {"chatroom_id": result["chatroom_id"]}
    except Exception as e:
        logger.error(f"Error creating chatroom: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/user/chatrooms")
async def get_user_chatrooms(user_id: int):
    """
    Get All chatrooms for a user
    """
    try:
        chatrooms = await chat_service.get_user_chatrooms(user_id)
        return {"chatrooms": chatrooms}
    except Exception as e:
        logger.error(f"Error gettings user chatrooms: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# Get messages for a specific chatroom
@router.get("/chatroom/{chatroom_id}/messages")
async def get_messages(chatroom_id: str):
    try:
        # Validate chatroom_id format using MongoDB's ObjectId
        if not ObjectId.is_valid(chatroom_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid chatroom ID format",
            )
        messages = await chat_service.get_messages(chatroom_id)
        return {
            "messages": messages
        }  # Wrap in dictionary to match frontend expectations
    except Exception as e:
        logger.error(f"Error getting messages: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.websocket("/ws/{chatroom_id}")
async def websocket_endpoint(websocket: WebSocket, chatroom_id: str):
    """
    WebSocket endpoint for chat connections.
    URL format: ws://localhost:5004/chat/ws/CHATROOM_ID?token=JWT_TOKEN
    """
    try:
        # Extract token from URL query parameters
        token = websocket.query_params.get("token")
        logger.info(f"WebSocket connection attempt for room {chatroom_id}")

        if not token:
            logger.warning("No token provided in WebSocket connection")
            await websocket.close(code=4001, reason="No token provided")
            return

        # Accept the connection first
        await websocket.accept()
        logger.info(f"WebSocket connection accepted for room {chatroom_id}")

        try:
            # Add to chat service WITHOUT accepting again
            if chatroom_id not in chat_service.active_connections:
                chat_service.active_connections[chatroom_id] = set()
            chat_service.active_connections[chatroom_id].add(websocket)
            logger.info(f"Added to active connections for room {chatroom_id}")

            # Message handling loop
            while True:
                try:
                    # Wait for and parse JSON message from client
                    data = await websocket.receive_json()
                    # Handle the message with user's token
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
            # Clean up on disconnect
            if chatroom_id in chat_service.active_connections:
                chat_service.active_connections[chatroom_id].remove(websocket)
                if not chat_service.active_connections[chatroom_id]:
                    del chat_service.active_connections[chatroom_id]
                logger.info(f"Cleaned up connection for room {chatroom_id}")

    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
        if websocket.client_state.CONNECTED:
            await websocket.close(code=1011)
