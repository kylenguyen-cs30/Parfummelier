from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.postgresql import Base
from pydantic import BaseModel
from typing import Optional, List


# SQLAlchemy Model
class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(
        Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False
    )
    user_id = Column(Integer, index=True, nullable=False)
    parent_id = Column(
        Integer, ForeignKey("comments.id", ondelete="CASCADE"), nullable=True
    )  # for tracking reply of the comments
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relationships
    post = relationship("Post", back_populates="comments")
    replies = relationship(
        "Comment",
        backref=relationship("Comment", remote_side=[id]),
        cascade="all, delete-orphan",
    )


# Pydantic models for API
class CommentBase(BaseModel):
    content: str
    parent_id: Optional[int] = None


class CommentCreate(CommentBase):
    pass


class CommentResponse(CommentBase):
    id: int
    post_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    replies: List["CommentResponse"] = []

    class Config:
        orm_mode = True


# This is needed for the self-referential relationship in CommentResponse
CommentResponse.update_forward_refs()
