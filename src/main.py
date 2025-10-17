from fastapi import FastAPI
from src.routes import users_route, posts_route, profile_route, feed_route, auth_route, notifications_route, ws
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="My Backend")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


app.include_router(auth_route.router, prefix="/auth")
app.include_router(users_route.router, prefix="/users")
app.include_router(posts_route.router, prefix="/posts")
app.include_router(profile_route.router, prefix="/profile")
app.include_router(feed_route.router, prefix="/feed")
app.include_router(notifications_route.router, prefix="/notifications")
app.include_router(ws.router, prefix="/ws")



# Allow your frontend origin
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # Allow specific origins
    allow_credentials=True,         # Needed for cookies / JWT in Authorization header
    allow_methods=["*"],            # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],            # Allow all headers (Authorization, Content-Type, etc.)
)