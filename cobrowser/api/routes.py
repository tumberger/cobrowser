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


class InstagramStoryRequest(BaseModel):
    image: str  # Base64 encoded image
    username: str
    password: str
    unique_id: str
    caption: Optional[str] = None
    mentions: Optional[list] = None
    locations: Optional[list] = None
    links: Optional[list] = None
    hashtags: Optional[list] = None
    stickers: Optional[list] = None


class InstagramThreadsRequest(BaseModel):
    username: str
    password: str
    unique_id: str
    amount: Optional[int] = 20
    selected_filter: Optional[str] = ""
    thread_message_limit: Optional[int] = None


@router.get("/")
async def root():
    return {
        "message": "Welcome to CoBrowser API",
        "version": "1.0.0",
        "endpoints": {"instagram_post": "/instagram/post", "instagram_story": "/instagram/story"},
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


@router.post("/instagram/story")
async def post_story_to_instagram(request: InstagramStoryRequest):
    instagram_manager = InstagramManager()
    return instagram_manager.upload_story(
        unique_id=request.unique_id,
        username=request.username,
        password=request.password,
        image_base64=request.image,
        caption=request.caption,
        mentions=request.mentions,
        locations=request.locations,
        links=request.links,
        hashtags=request.hashtags,
        stickers=request.stickers,
    )


@router.post("/instagram/threads")
async def get_instagram_threads(request: InstagramThreadsRequest):
    instagram_manager = InstagramManager()
    return instagram_manager.get_direct_threads(
        unique_id=request.unique_id,
        username=request.username,
        password=request.password,
        amount=request.amount,
        selected_filter=request.selected_filter,
        thread_message_limit=request.thread_message_limit
    )
