from .chat import router as chat_router
from .post import router as post_router
from .comment import router as comment_router


__all__ = [
    "chat_router",
    "post_router",
    "comment_router",
]
