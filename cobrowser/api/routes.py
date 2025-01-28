from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from cobrowser.tasks.instagram_tasks import InstagramManager
from typing import Optional

router = APIRouter()


class InstagramPostRequest(BaseModel):
    image: str  # Base64 encoded image
    username: str
    password: str
    unique_id: str
    caption: Optional[str] = None


@router.get("/")
async def root():
    return {
        "message": "Welcome to CoBrowser API",
        "version": "1.0.0",
        "endpoints": {"instagram_post": "/instagram/post"},
    }


@router.post("/instagram/post")
async def post_to_instagram(request: InstagramPostRequest):
    instagram_manager = InstagramManager()
    return instagram_manager.upload_photo(
        unique_id=request.unique_id,
        username=request.username,
        password=request.password,
        image_base64=request.image,
        caption=request.caption,
    )
