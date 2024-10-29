
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, status
from app.models.chat import ChatroomCreate, Message
from app.services.chat import ChatService
from typing import List
import json
from bson import ObjectId

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
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# Get messages for a specific chatroom
@router.get("/chatroom/{chatroom_id}/messages")
async def get_messages(chatroom_id: str):
    """
    Retrieves all messages for a specific chatroom
    
    Args:
        chatroom_id (str): MongoDB ObjectId of the chatroom as string
    
    Returns:
        list: List of messages in the chatroom
    
    Raises:
        HTTPException: If chatroom ID is invalid or retrieval fails
    """
    try:
        # Validate chatroom_id format using MongoDB's ObjectId
        if not ObjectId.is_valid(chatroom_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid chatroom ID format"
            )
        messages = await chat_service.get_messages(chatroom_id)
        return messages
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# WebSocket endpoint for real-time chat
@router.websocket("/ws/{chatroom_id}")
async def websocket_endpoint(websocket: WebSocket, chatroom_id: str):
    """
    WebSocket endpoint handling real-time chat connections
    
    Args:
        websocket (WebSocket): FastAPI WebSocket connection
        chatroom_id (str): ID of the chatroom to connect to
    
    This endpoint:
    1. Establishes WebSocket connection
    2. Maintains connection and handles incoming messages
    3. Handles disconnection and cleanup
    """
    try:
        # Accept and store the WebSocket connection
        await chat_service.connect(websocket, chatroom_id)
        try:
            # Infinite loop to handle incoming messages
            while True:
                # Wait for and process incoming messages
                data = await websocket.receive_json()
                await chat_service.handle_message(chatroom_id, data)
        except WebSocketDisconnect:
            # Clean up when client disconnects
            await chat_service.disconnect(websocket, chatroom_id)
        except Exception as e:
            # Handle other errors during message processing
            print(f"Error in websocket connection: {e}")
            await chat_service.disconnect(websocket, chatroom_id)
    except Exception as e:
        # Handle connection establishment errors
        print(f"Failed to establish websocket connection: {e}")
        if websocket.client_state.CONNECTED:
            await websocket.close(code=1000)
