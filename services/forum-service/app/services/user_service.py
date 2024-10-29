from fastapi import HTTPException
from typing import Dict, Optional

import httpx
import logging

logger = logging.getLogger(__name__)

class UserService:
    def __init__(self) -> None:
        self.base_url = "http://user-service:5000"
    
    async def get_user_chat_info(self, access_token: str) -> dict:
        """
        Fetch minimal user information needed for chat
        """
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/user/chat-info",
                    headers=headers,
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    user_info = response.json()
                    # Map the fields to match our Message model
                    return {
                        "user_id": user_info["userId"],  # Note the case change
                        "userName": user_info["userName"],
                        "firstName": user_info["firstName"],
                        "lastName": user_info["lastName"]
                    }
                elif response.status_code == 401:
                    raise HTTPException(status_code=401, detail="Invalid or expired token")
                elif response.status_code == 404:
                    raise HTTPException(status_code=404, detail="User not found")
                else:
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=f"Error from user service: {response.text}"
                    )
                    
        except httpx.RequestError as e:
            logger.error(f"Request error: {str(e)}")
            raise HTTPException(
                status_code=503,
                detail=f"User service unavailable: {str(e)}"
            )
    async def close(self):
        pass
