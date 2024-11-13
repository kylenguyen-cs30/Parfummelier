# app/routes/post.py
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from typing import List, Optional
from sqlalchemy.orm import Session
from app.database.postgresql import get_db
from app.models.post import Post, PostCreate, PostResponse
from app.services.post_service import PostService
from datetime import datetime

router = APIRouter()


@router.get("/health")
async def post_health_check():
    """Check if post service is online"""
    return {
        "status": "healthy",
        "service": "post",
        "details": {"database": "connected", "timestamp": datetime.now().isoformat()},
    }


@router.post("/", response_model=PostResponse)
async def create_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    service: PostService = Depends(lambda: PostService(db)),
):
    """Create a new post"""
    try:
        return await service.create_post(post)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: int,
    db: Session = Depends(get_db),
    service: PostService = Depends(lambda: PostService(db)),
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
    db: Session = Depends(get_db),
    service: PostService = Depends(lambda: PostService(db)),
):
    """Get all posts with optional filtering"""
    try:
        return await service.get_posts(skip=skip, limit=limit, topic=topic)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Add image upload endpoint
@router.post("/upload-images")
async def upload_images(
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    service: PostService = Depends(lambda: PostService(db)),
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
