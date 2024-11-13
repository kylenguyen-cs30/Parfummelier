# app/services/post_service.py
from fastapi import HTTPException, UploadFile, File
import aiofiles
import os
from typing import List, Optional
from datetime import datetime
import uuid
from sqlalchemy.orm import Session
from app.models.post import Post, PostCreate  # Added PostCreate import
from app.models.post import PostResponse  # Optional, if needed


class PostService:
    def __init__(self, db: Session):
        self.db = db
        # Configure image upload settings
        self.UPLOAD_DIR = "uploads/images"
        self.MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB
        self.ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif"}

        # Ensure upload directory exists
        os.makedirs(self.UPLOAD_DIR, exist_ok=True)

    async def save_image(self, image: UploadFile) -> str:
        """Save uploaded image and return its URL"""
        try:
            # Validate file size
            file_size = 0
            async for chunk in image.file:
                file_size += len(chunk)
                if file_size > self.MAX_IMAGE_SIZE:
                    raise HTTPException(
                        status_code=400, detail="Image size should not exceed 5MB"
                    )

            # Validate file extension
            ext = os.path.splitext(image.filename)[1].lower()
            if ext not in self.ALLOWED_EXTENSIONS:
                raise HTTPException(
                    status_code=400,
                    detail="Only .jpg, .jpeg, .png, and .gif files are allowed",
                )

            # Generate unique filename
            filename = f"{uuid.uuid4()}{ext}"
            filepath = os.path.join(self.UPLOAD_DIR, filename)

            # Save the file
            async with aiofiles.open(filepath, "wb") as out_file:
                content = await image.read()
                await out_file.write(content)

            # Return the URL path
            return f"/images/{filename}"

        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to upload image: {str(e)}"
            )

    async def create_post(self, post: PostCreate) -> Post:
        """Create a new post"""
        try:
            db_post = Post(
                title=post.title,
                content=post.content,
                topic=post.topic,
                image_urls=post.image_urls,
                user_id=1,  # TODO: Get from auth token
            )
            self.db.add(db_post)
            self.db.commit()
            self.db.refresh(db_post)
            return db_post
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    async def get_post(self, post_id: int) -> Post:
        """Get a post by ID"""
        post = self.db.query(Post).filter(Post.id == post_id).first()
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        return post

    async def get_posts(
        self, skip: int = 0, limit: int = 10, topic: Optional[str] = None
    ) -> List[Post]:
        """Get all posts with optional topic filter"""
        query = self.db.query(Post)
        if topic:
            query = query.filter(Post.topic == topic)
        return query.offset(skip).limit(limit).all()
