from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.postgresql import get_db
from app.models.comment import Comment, CommentResponse
from app.services.user_service import UserService


class CommentService:
    def __init__(
        self, db: Session = Depends(get_db), user_service: UserService = Depends()
    ):
        self.db = db
        self.user_service = user_service

    async def create_comment(
        self,
        post_id: int,
        user_id: int,
        content: str,
        access_token: str,
        parent_id: Optional[int] = None,
    ) -> CommentResponse:
        try:
            # Verify user exists
            user_info = await self.user_service.get_user_chat_info(access_token)

            # If this is a reply, verify parent comment exists
            if parent_id is not None:  # Changed from if parent_id:
                parent_comment = (
                    self.db.query(Comment).filter(Comment.id == parent_id).first()
                )
                if not parent_comment:
                    raise HTTPException(
                        status_code=404, detail="Parent comment not found"
                    )

            comment = Comment(
                post_id=post_id,
                user_id=user_info["user_id"],  # Use user_id from token
                parent_id=parent_id,
                content=content,
            )

            self.db.add(comment)
            self.db.commit()
            self.db.refresh(comment)

            return CommentResponse(
                id=comment.id,
                post_id=post_id,
                user_id=user_info["user_id"],
                content=comment.content,
                parent_id=comment.parent_id,
                created_at=comment.created_at,
                updated_at=comment.updated_at,
                replies=[],
            )
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    async def get_post_comments(self, post_id: int, access_token: str) -> List[dict]:
        """Get all comments for a post, including replies"""
        # Get top-level comments first
        comments = (
            self.db.query(Comment)
            .filter(Comment.post_id == post_id, Comment.parent_id.is_(None))
            .order_by(Comment.created_at)
            .all()
        )

        return await self._enrich_comments_with_replies(comments, access_token)

    async def _enrich_comments_with_replies(
        self, comments: List[Comment], access_token: str
    ) -> List[dict]:
        """Recursively enrich comments with user info and replies"""
        result = []
        for comment in comments:
            try:
                user_info = await self.user_service.get_user_chat_info(
                    comment.user_id, access_token
                )
                comment_dict = {
                    "id": comment.id,
                    "content": comment.content,
                    "created_at": comment.created_at,
                    "user": {
                        "user_id": user_info["user_id"],
                        "userName": user_info["userName"],
                        "firstName": user_info["firstName"],
                        "lastName": user_info["lastName"],
                    },
                }

                # Recursively get replies
                if comment.replies:
                    comment_dict["replies"] = await self._enrich_comments_with_replies(
                        comment.replies, access_token
                    )
                else:
                    comment_dict["replies"] = []

                result.append(comment_dict)
            except HTTPException:
                continue

        return result
