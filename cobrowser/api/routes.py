from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def root():
    return {
        "message": "Welcome to CoBrowser API",
        "version": "1.0.0",
        "endpoints": {
            "instagram_post": "/instagram/post"
        }
    }

@router.post("/instagram/post")
async def post_to_instagram(image: str, username: str, password: str):
    # TODO - Route Instagram post requests through policy engine
    pass
