from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Header
from typing import List, Optional
from sqlalchemy.orm import Session
from app.database.postgresql import get_db
from app.models.post import Post, PostCreate, PostResponse
from app.services.post_service import PostService
from datetime import datetime

import logging
import traceback

router = APIRouter()

logger = logging.getLogger(__name__)


# Create a dependency for PostService
def get_post_service(db: Session = Depends(get_db)):
    return PostService(db)


# NOTE: Health check router
@router.get("/health")
async def post_health_check():
    """Check if post service is online"""
    return {
        "status": "healthy",
        "service": "post",
        "details": {"database": "connected", "timestamp": datetime.now().isoformat()},
    }


# NOTE: Create new post
@router.post("/", response_model=PostResponse)
async def create_post(
    post: PostCreate,
    # access_token: str = Header(...),
    authorization: str = Header(..., description="Bearer {token}"),
    service: PostService = Depends(get_post_service),
):
    """Create a new post"""
    try:
        # Log the incoming post data
        token = authorization.split("Bearer ")[-1]
        logger.info(f"Attempting to create post: {post.dict()}")
        result = await service.create_post(post, token)
        logger.info(f"Successfully created post: {result}")
        return result

    except Exception as e:
        # Log the full error traceback
        error_traceback = traceback.format_exc()
        logger.error(f"Failed to create post. Error: {str(e)}")
        logger.error(f"Traceback: {error_traceback}")

        # Return more detailed error information
        raise HTTPException(
            status_code=500,
            detail={
                "message": "Failed to create post",
                "error": str(e),
                "traceback": error_traceback,
            },
        )


# NOTE: Get all posts
@router.get("/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: int,
    service: PostService = Depends(get_post_service),
):
    """Get a specific post by ID"""
    try:
        return await service.get_post(post_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/", response_model=List[PostResponse])
async def get_posts(
    skip: int = 0,
    limit: int = 10,
    topic: Optional[str] = None,
    service: PostService = Depends(get_post_service),
):
    """Get all posts with optional filtering"""
    try:
        return await service.get_posts(skip=skip, limit=limit, topic=topic)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# NOTE: Add image upload endpoint
@router.post("/upload-images")
async def upload_images(
    files: List[UploadFile] = File(...),
    service: PostService = Depends(get_post_service),
):
    """Upload images for a post"""
    try:
        image_urls = []
        for file in files:
            image_url = await service.save_image(file)
            image_urls.append(image_url)
        return {"image_urls": image_urls}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
