from fastapi import APIRouter

router = APIRouter(prefix="", tags=["Authentication"])

@router.post("/create")
def create_post():
    return "hello"