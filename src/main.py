from fastapi import FastAPI
from src.routes import auth

app = FastAPI(title="My Backend")

app.include_router(auth.router, prefix="/auth")
