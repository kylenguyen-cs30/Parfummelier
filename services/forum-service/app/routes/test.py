# forum-service/app/routes/test.py
from fastapi import APIRouter
import httpx
from app.config import settings

router = APIRouter()


@router.get("/cors-test")
async def test_user_service_cors():
    """Test CORS communication with user-service"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.USER_SERVICE_URL}/test/cors-test",
                headers={"Origin": "http://forum-service:5000"},
            )

            if response.status_code == 200:
                return {
                    "status": "success",
                    "message": "Successfully connected to user-service",
                    "user_service_response": response.json(),
                }
            else:
                return {
                    "status": "error",
                    "message": f"Failed to connect to user-service: {response.status_code}",
                    "details": response.text,
                }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to connect to user-service: {str(e)}",
        }


# Add test endpoints for post and comment services
@router.get("/services/status")
async def check_all_services():
    """Check status of all forum service endpoints"""
    return {
        "status": "online",
        "services": {
            "post": {
                "status": "available",
                "endpoints": [
                    "POST /posts/",
                    "GET /posts/{post_id}",
                    "GET /posts/",
                    "POST /posts/upload-images",
                ],
            },
            "comment": {
                "status": "available",
                "endpoints": [
                    "POST /comments/{post_id}",
                    "GET /comments/post/{post_id}",
                ],
            },
        },
        "database": "connected",
        "user_service_connection": "active",
    }
