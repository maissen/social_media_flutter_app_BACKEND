from fastapi import APIRouter, Depends, status

router = APIRouter(prefix="/follow-unfollow", tags=["Authentication"])