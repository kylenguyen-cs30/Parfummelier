from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.postgresql import get_db
from app.models.comment import Comment, CommentResponse
from app.services.user_service import UserService
import logging

logger = logging.getLogger(__name__)


class CommentService:
    def __init__(
        self, db: Session = Depends(get_db), user_service: UserService = Depends()
    ):
        self.db = db
        self.user_service = user_service

    async def create_comment(
        self,
        post_id: int,
        content: str,
        access_token: str,
        parent_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> CommentResponse:
        try:
            # Get User info from Token
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
                user_id=user_info["user_id"],
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
                user={
                    "user_id": user_info["user_id"],
                    "userName": user_info["userName"],
                    "firstName": user_info["firstName"],
                    "lastName": user_info["lastName"],
                },
                replies=[],
            )
        except HTTPException as he:
            self.db.rollback()
            raise he
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating comment: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    async def get_post_comments(self, post_id: int, access_token: str) -> List[dict]:
        """Get all comments for a post, including replies"""
        try:
            # Get top-level comments first
            logger.info(f"Fetching comments for post {post_id}")
            comments = (
                self.db.query(Comment)
                .filter(Comment.post_id == post_id, Comment.parent_id.is_(None))
                .order_by(Comment.created_at)
                .all()
            )

            logger.info(f"Found {len(comments)} top-level comments")
            if not comments:
                return []

            enriched_comments = await self._enrich_comments_with_replies(
                comments, access_token
            )
            logger.info("Successfully enriched comments with user info")
            return enriched_comments

        except Exception as e:
            logger.error(f"Error fetching comments for post {post_id} : {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

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
                    "post_id": comment.post_id,
                    "user_id": user_info["user_id"],
                    "content": comment.content,
                    "parent_id": comment.parent_id,
                    "created_at": comment.created_at,
                    "updated_at": comment.updated_at,
                    "user": {
                        "user_id": user_info["user_id"],
                        "userName": user_info["userName"],
                        "firstName": user_info["firstName"],
                        "lastName": user_info["lastName"],
                    },
                }

                # Recursively get replies
                if comment.replies:
                    # recursive call till there is no more reply the in
                    # the same comment.parent_id
                    comment_dict["replies"] = await self._enrich_comments_with_replies(
                        comment.replies, access_token
                    )
                else:
                    comment_dict["replies"] = []

                result.append(comment_dict)
            except Exception as e:
                logger.error(f"Error enriching comment {comment.id}: {str(e)}")
                """
                still include the comment if user info fails
                """

                comment_dict = {
                    "id": comment.id,
                    "post_id": comment.post_id,
                    "content": comment.content,
                    "created_at": comment.created_at,
                    "updated_at": comment.updated_at,
                    "parent_id": comment.parent_id,
                    "user": {
                        "user_id": comment.user_id,
                        "userName": f"User {comment.user_id}",
                        "firstName": "",
                        "lastName": "",
                    },
                    "replies": [],
                }
                result.append(comment_dict)

        return result
