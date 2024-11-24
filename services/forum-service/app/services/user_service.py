from fastapi import HTTPException
from typing import Dict, Optional, Union
from cachetools import TTLCache
import httpx
import logging

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self) -> None:
        self.base_url = "http://user-service:5000"
        self._client = None
        self.user_cache = TTLCache(maxsize=100, ttl=300)

    # NOTE: create async client for the object
    @property
    def client(self):
        if self._client is None:
            self._client = httpx.AsyncClient()
        return self._client

    # NOTE: this is for chat features
    async def get_user_chat_info(
        self, identifier: Union[str, int], access_token: Optional[str] = None
    ) -> dict:
        """
        Fetch minimal user information needed for chat.
        Can be called with either an access token (str) or user_id (int)
        """
        try:
            async with httpx.AsyncClient() as client:
                headers = {
                    "Authorization": f"Bearer {access_token if access_token else identifier}",
                    "Content-Type": "application/json",
                }

                if isinstance(identifier, str):
                    # Token-based request (for current user)
                    response = await client.get(
                        f"{self.base_url}/user/chat-info", headers=headers, timeout=10.0
                    )
                else:
                    # User ID-based request (for other users)
                    response = await client.get(
                        f"{self.base_url}/user/{identifier}/chat-info",
                        headers=headers,  # Include headers for authentication
                        timeout=10.0,
                    )

                if response.status_code == 200:
                    user_info = response.json()
                    # Ensure all required fields are present
                    required_fields = ["userId", "userName", "firstName", "lastName"]
                    if not all(field in user_info for field in required_fields):
                        logger.error(
                            f"Missing required fields in user info: {user_info}"
                        )
                        raise ValueError("Incomplete user data received")

                    return {
                        "user_id": user_info["userId"],
                        "userName": user_info["userName"],
                        "firstName": user_info["firstName"],
                        "lastName": user_info["lastName"],
                    }
                else:
                    error_msg = (
                        f"Failed to get user info. Status: {response.status_code}"
                    )
                    logger.error(error_msg)
                    raise HTTPException(
                        status_code=response.status_code, detail=error_msg
                    )

        except Exception as e:
            logger.error(f"Error in get_user_chat_info: {str(e)}")
            logger.error("Error in get_user_chat_info:")
            raise HTTPException(
                status_code=500, detail=f"Failed to get user info: {str(e)}"
            )
