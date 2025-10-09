from fastapi import FastAPI
from src.routes import auth, users_route

app = FastAPI(title="My Backend")

app.include_router(auth.router, prefix="/auth")
app.include_router(users_route.router, prefix="/users")
