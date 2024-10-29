from pydantic import BaseModel, Field
from datetime import datetime 
from typing import List, Optional
from bson import ObjectId 


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)


class ChatroomCreate(BaseModel):
    participants: List[int]

class Message(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    chatroom_id: str 
    user_id: int 
    content: str 
    timestamp: datetime = Field(default_factory=datetime.now)

    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True


