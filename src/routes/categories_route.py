from fastapi import APIRouter

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