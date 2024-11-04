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
    """

    participants: List[int] = Field(
        description="List of user IDs who will be in the chatroom"
    )


class UserInfo(BaseModel):
    """
    Pydantic model for user inforamtion in chat context.
    """

    id: int
    userName: str
    firstName: str
    lastName: str

    class Config:
        arbitrary_types_allowed = True


class MessagePreview:
    """
    Simplified message model for previews in chat lists
    """

    content: str
    timestamp: datetime

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class Message(BaseModel):
    """
    Full message model for chat messages.
    """

    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    chatroom_id: str
    user_id: int
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)
    userName: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        populate_by_name = True


class ChatroomPreview(BaseModel):
    """
    Preview model for chatrooms in the inbox.
    """

    chatroom_id: str
    other_user: UserInfo
    latest_message: Optional[MessagePreview]
    last_message_at: datetime

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class ChatroomList(BaseModel):
    """
    Container model for list of chatroom previews.
    """

    chatrooms: List[ChatroomPreview]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class ChatroomResponse(BaseModel):
    """
    Response model for chatroom operations.
    """

    chatroom_id: str
    participants: List[int]
    created_at: datetime
    last_message_at: Optional[datetime]

    class Config:
        json_encoders = {ObjectId: str}
