from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, ARRAY
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.postgresql import Base
from pydantic import BaseModel, HttpUrl
from typing import Optional, List


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    topic = Column(String(100), nullable=False, index=True)
    # Store array of image URLs
    image_urls = Column(ARRAY(String), nullable=True)

    # time of the post
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relationship with comments
    comments = relationship(
        "Comment", back_populates="post", cascade="all, delete-orphan"
    )


class PostBase(BaseModel):
    title: str
    content: str
    topic: str
    image_urls: Optional[List[str]] = None


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    user: Optional[dict] = None

    class Config:
        # orm_mode = True
        from_attributes = True
