from fastapi import APIRouter, Depends, HTTPException, Header
from typing import List
from app.services.comment_service import CommentService
from app.models.comment import CommentCreate, CommentResponse
from datetime import datetime

router = APIRouter()


@router.get("/health")
async def comment_health_check():
    """Check if comment service is online"""
    return {
        "status": "healthy",
        "service": "comment",
        "details": {"database": "connected", "timestamp": datetime.now().isoformat()},
    }


@router.post("/{post_id}", response_model=CommentResponse)
async def create_comment(
    post_id: int,
    comment: CommentCreate,
    access_token: str = Header(...),
    service: CommentService = Depends(),
):
    """Create a new comment on a post"""
    try:
        return await service.create_comment(
            post_id=post_id,
            content=comment.content,
            access_token=access_token,
            parent_id=comment.parent_id,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/post/{post_id}", response_model=List[CommentResponse])
async def get_post_comments(
    post_id: int, access_token: str = Header(...), service: CommentService = Depends()
):
    """Get all comments for a specific post"""
    return await service.get_post_comments(post_id, access_token)
