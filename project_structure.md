# Backend Project Structure

```
backend/
│
├── app/
│   ├── main.py                 # Entry point
│   ├── core/
│   │   ├── config.py           # Env vars, DB config
│   │   ├── security.py         # JWT, password hashing
│   ├── models/                 # SQLAlchemy models
│   ├── schemas/                # Pydantic schemas
│   ├── routes/                 # API endpoints
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── posts.py
│   │   ├── comments.py
│   │   ├── groups.py
│   │   ├── quizzes.py
│   │   └── notifications.py
│   ├── services/               # Business logic
│   ├── database.py             # SQLAlchemy session
│   ├── utils/                  # Helpers
│   └── static/media/           # Uploaded files
│
├── requirements.txt
├── alembic/                    # DB migrations
└── .env
```