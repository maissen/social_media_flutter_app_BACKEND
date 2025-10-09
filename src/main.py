from fastapi import FastAPI
from src.routes import auth, users_route, posts_route, profile_route, feed_route
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="My Backend")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


app.include_router(auth.router, prefix="/auth")
app.include_router(users_route.router, prefix="/users")
app.include_router(posts_route.router, prefix="/posts")
app.include_router(profile_route.router, prefix="/profile")
app.include_router(feed_route.router, prefix="/feed")
