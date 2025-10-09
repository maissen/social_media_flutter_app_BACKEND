from fastapi import APIRouter, Depends
from src.schemas.posts import CreatePostSchema
from src.core.security import get_current_user_from_token

router = APIRouter(prefix="", tags=["Authentication"])

@router.post("/create")
def create_post(
    current_user = Depends(get_current_user_from_token)
):
    return "hello"