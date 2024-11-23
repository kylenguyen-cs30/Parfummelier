from fastapi import APIRouter, Depends, HTTPException, Header
from typing import List
from app.services.comment_service import CommentService
from app.models.comment import CommentCreate, CommentResponse
from datetime import datetime

import logging

logger = logging.getLogger(__name__)
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
    authorization: str = Header(..., description="Bearer {token}"),
    service: CommentService = Depends(),
):
    """Create a new comment on a post"""
    try:
        token = authorization.split("Bearer ")[-1]
        return await service.create_comment(
            post_id=post_id,
            content=comment.content,
            access_token=token,
            parent_id=comment.parent_id,
        )
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error in create_comment endpoint : {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/post/{post_id}", response_model=List[CommentResponse])
async def get_post_comments(
    post_id: int,
    authorization: str = Header(..., description="Bearer {token}"),
    # access_token: str = Header(...),
    service: CommentService = Depends(),
):
    """Get all comments for a specific post"""
    # return await service.get_post_comments(post_id, access_token)
    try:
        # Extract token from Bearer header
        token = authorization.split("Bearer ")[-1]
        comments = await service.get_post_comments(post_id, token)
        # Ensure we return empty list if no comments
        return comments or []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
