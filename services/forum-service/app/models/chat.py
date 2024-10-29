from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from bson import ObjectId

class PyObjectId(ObjectId):
    """
    Custom type for handling MongoDB ObjectId fields in Pydantic models.
    Extends bson.ObjectId to add validation and serialization support.
    """
    @classmethod
    def __get_validators__(cls):
        """
        Get Pydantic validators for this type.
        Required for Pydantic custom types.
        
        Yields:
            callable: The validate method to be used by Pydantic
        """
        yield cls.validate

    @classmethod
    def validate(cls, v):
        """
        Validate that a given value is a valid MongoDB ObjectId.
        
        Args:
            v: Value to validate (string or ObjectId)
            
        Returns:
            ObjectId: Validated MongoDB ObjectId
            
        Raises:
            ValueError: If the value is not a valid ObjectId
        """
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

class ChatroomCreate(BaseModel):
    """
    Pydantic model for creating a new chatroom.
    Used for request validation when creating chatrooms.
    
    Attributes:
        participants (List[int]): List of user IDs who will be in the chatroom
    """
    participants: List[int]

class Message(BaseModel):
    """
    Pydantic model for chat messages.
    Represents the structure of chat messages in the system.
    
    Attributes:
        id (PyObjectId): MongoDB ObjectId for the message, aliased as '_id'
        chatroom_id (str): ID of the chatroom this message belongs to
        user_id (int): ID of the user who sent the message
        content (str): The actual message content
        timestamp (datetime): When the message was sent, defaults to current time
        
    Config:
        json_encoders: Custom JSON encoding for ObjectId type
        populate_by_name: Allow population by field name including aliases
    """
    id: PyObjectId = Field(
        default_factory=PyObjectId,
        alias="_id",
        description="Unique identifier for the message"
    )
    chatroom_id: str = Field(
        ...,  # ... means required
        description="ID of the chatroom containing this message"
    )
    user_id: int = Field(
        ...,
        description="ID of the user who sent the message"
    )
    content: str = Field(
        ...,
        description="Content of the message"
    )
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="Time when the message was sent"
    )

    class Config:
        """
        Pydantic model configuration.
        
        Attributes:
            json_encoders: Custom JSON encoding rules
            populate_by_name: Allow population by field name
        """
        json_encoders = {ObjectId: str}  # Convert ObjectId to string in JSON
        populate_by_name = True  # Allow both alias and field names
