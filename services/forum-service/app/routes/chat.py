
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
    WebSocket endpoint for chat connections.
    URL format: ws://localhost:5004/chat/ws/CHATROOM_ID?token=JWT_TOKEN
    
    Flow:
    1. Client connects with token in URL query
    2. Validate token presence
    3. Accept connection and add to chat service
    4. Enter message listening loop
    5. Handle disconnection
    """
    
    # First try block: Connection setup
    try:
        # Extract token from URL query parameters
        # Example URL: ws://localhost:5004/chat/ws/123?token=abc123
        token = websocket.query_params.get("token")
        
        # If no token provided, reject the connection
        if not token:
            await websocket.close(code=1008)  # 1008 = Policy violation
            return
        
        # Accept the connection and add to chat service
        await chat_service.connect(websocket, chatroom_id)
        
        # Second try block: Message handling loop
        try:
            # Infinite loop to handle incoming messages
            while True:
                # Wait for and parse JSON message from client
                data = await websocket.receive_json()
                # Example data: {"content": "Hello everyone!"}
                
                # Handle the message with user's token
                await chat_service.handle_message(chatroom_id, data, token)
                
        except WebSocketDisconnect:
            # Handle client disconnection gracefully
            await chat_service.disconnect(websocket, chatroom_id)
            
    except Exception as e:
        # Handle any other errors
        print(f"WebSocket error: {e}")
        if websocket.client_state.CONNECTED:
            await websocket.close(code=1011)  # 1011 = Internal error
