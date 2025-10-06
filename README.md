# Social Media App Architecture

## 🎨 Frontend (Flutter App)

### Main Responsibilities

#### User Interface (UI)
- Build screens using Flutter widgets
- Implement smooth navigation (e.g., Navigator, GoRouter, etc.)
- Manage app themes and responsive layouts

#### State Management
- Manage user and post states (e.g., with Provider, Riverpod, Bloc, or GetX)
- Listen to Firestore streams for real-time updates

#### User Authentication (via Firebase SDK)
- Registration, login, and logout using Firebase Authentication
- Display user info from Firestore (profile picture, bio, etc.)
- Maintain session persistence (auto-login)

#### Post Management
- Create posts (text, image, video)
- Upload images/videos to Firebase Storage
- Display posts in a chronological feed
- Implement likes and comments (through Firestore)

#### Social Interactions
- Follow/unfollow users
- Show friend activity in feed
- Display user profiles

#### Notifications
- Receive push notifications via Firebase Cloud Messaging (FCM)
- Display in-app alerts for friend requests, comments, etc.

#### Search & Discovery
- Search for users by name or username
- View public profiles and posts
- Filter posts by topics (science, art, sports…)

#### Educational Features
- Interactive quizzes UI
- Create/join discussion groups
- Display educational posts

---

## ⚙️ Backend (FastAPI)

### 🧠 Overview

The backend replaces Firebase and becomes your API + business logic + database layer. It exposes REST (and optionally WebSocket) endpoints consumed by the Flutter app.

### 🗄️ Main Components

#### 1. Authentication & Authorization

**JWT-based authentication** (python-jose, fastapi-users, or custom logic)

**Routes for:**
- `/auth/register`
- `/auth/login`
- `/auth/logout`
- `/auth/refresh`

**Additional features:**
- Password hashing using bcrypt
- Role-based access (normal user / admin)
- Token validation middleware

#### 2. Database

**Use PostgreSQL** (or MySQL/MongoDB, depending on your comfort)

**ORM:** SQLAlchemy + Alembic for migrations

**Example tables:**
- `users`
- `posts`
- `comments`
- `likes`
- `follows`
- `groups`
- `quizzes`
- `notifications`

#### 3. Posts & Media

**API routes for CRUD:**
- `/posts/` → Create/read/update/delete posts
- `/posts/{id}/like` → Like/unlike
- `/posts/{id}/comments` → Comment

**Media uploads handled via:**
- `/upload/image`
- `/upload/video`

**Media stored in:**
- Local folder (`/media/`) during development
- Or cloud storage (e.g., AWS S3, MinIO) in production

#### 4. Social Features

- `/users/{id}/follow` → Follow/unfollow users
- `/feed/` → Fetch posts from followed users
- `/users/search?query=...` → Search by username

#### 5. Notifications

**Real-time updates using:**
- WebSocket (FastAPI supports it natively), or
- Background tasks + push notifications via FCM

**Example event triggers:**
- When someone likes/comments your post
- When a new friend joins

#### 6. Educational Features

- `/quizzes/` → Create, join, or fetch quizzes
- `/groups/` → Thematic groups (science, sports, art)
- `/resources/` → Educational content API

---

## 📋 Summary

This architecture separates concerns between:
- **Flutter Frontend**: Handles UI/UX, state management, and user interactions
- **FastAPI Backend**: Manages business logic, data persistence, authentication, and API endpoints

The combination provides a scalable, maintainable foundation for your social media application with educational features.