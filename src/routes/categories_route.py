from fastapi import APIRouter
from src.schemas.posts import PostSchema

router = APIRouter()

categories = [
    {"id": 1, "name": "💻 Programming"},
    {"id": 2, "name": "🔬 Science"},
    {"id": 3, "name": "💼 Business"},
    {"id": 4, "name": "🎨 Design"},
    {"id": 5, "name": "🌍 Language Learning"},
    {"id": 6, "name": "📊 Data Science"},
    {"id": 7, "name": "📱 Digital Marketing"},
    {"id": 8, "name": "🧠 Personal Development"},
    {"id": 9, "name": "💰 Finance"},
    {"id": 10, "name": "✍️ Creative Writing"},
    {"id": 11, "name": "🌐 Web Development"},
    {"id": 12, "name": "📸 Photography"},
    {"id": 13, "name": "🎵 Music"},
    {"id": 14, "name": "🏥 Health & Wellness"},
    {"id": 15, "name": "🚀 Entrepreneurship"},
    {"id": 16, "name": "🤖 Artificial Intelligence"},
    {"id": 17, "name": "🔐 Cybersecurity"},
    {"id": 18, "name": "📋 Project Management"},
    {"id": 19, "name": "☁️ Cloud Computing"},
    {"id": 20, "name": "👥 Leadership"},
]

@router.get("/")
def get_categories():
    return categories


def get_post_categories(post: PostSchema):
    # Filter global categories where the ID is inside post.categories
    post_cats = [[cat["id"], cat["name"]] for cat in categories if cat["id"] in post.categories]

    return post_cats


# post2 = PostResponseSchema(
#             post_id=post.post_id,
#             user_id=post.user_id,
#             user=post.user,
#             content=post.content,
#             media_url=post.media_url,
#             created_at=post.created_at,
#             likes_nbr=post.likes_nbr,
#             comments_nbr=post.comments_nbr,
#             is_liked_by_me=post.is_liked_by_me,
#             category_objects=post.category_objects
#         )