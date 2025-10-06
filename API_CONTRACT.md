# Social Media API Contract v1.0

## Base URL
```
Production: https://api.yoursocialapp.com/v1
Development: http://localhost:8000/v1
```

## Authentication
All authenticated endpoints require a JWT Bearer token in the Authorization header:
```
Authorization: Bearer <access_token>
```

---

## 1. Authentication & Authorization

### 1.1 Register User
**POST** `/auth/register`

**Request Body:**
```json
{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "SecurePass123!",
  "date_of_birth": "2000-01-15"
}
```

**Response:** `201 Created`
```json
{
  "success": true,
  "data": {
    "user_id": "uuid-v4",
    "email": "user@example.com",
    "username": "johndoe",
    "created_at": "2025-10-06T10:30:00Z"
  },
  "message": "User registered successfully",
  "timestamp": "2025-10-06T10:30:00Z"
}
```

### 1.2 Login
**POST** `/auth/login`

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expires_in": 3600,
    "user": {
      "email": "user@example.com",
      "username": "johndoe",
      "profile_picture": "https://storage.com/profile.jpg"
    }
  },
  "message": "Login successful",
  "timestamp": "2025-10-06T10:30:00Z"
}
```

---

### 1.4 Logout
**POST** `/auth/logout`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "success": true,
  "data": null,
  "message": "Logged out successfully",
  "timestamp": "2025-10-06T10:30:00Z"
}
```
### error 
```json
{
  "success": false,
  "data": null,
  "message": "Failed to log out",
  "timestamp": "2025-10-06T10:30:00Z"
}
```
---

## 2. User Management

### 2.1 Get Current User Profile
**GET** `/users/profile/<user-id>`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "user_id": "uuid-v4",
    "email": "user@example.com",
    "username": "johndoe",
    "bio": "Software developer and tech enthusiast",
    "profile_picture": "https://storage.com/profile.jpg",
    "followers_count": 150,
    "following_count": 200,
    "posts_count": 45,
    "created_at": "2025-01-15T10:30:00Z",
    "i_am_a_follower": true
  },
  "message": "User profile retrieved successfully",
  "timestamp": "2025-10-06T10:30:00Z"
}
```
### error 
```json
{
  "success": false,
  "data": null,
  "message": "Failed to load profile",
  "timestamp": "2025-10-06T10:30:00Z"
}
```
---

### 2.2 Update User Profile
**PATCH** `/users/me`

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "bio": "Updated bio",
  "profile_picture": "base64_encoded_image_or_url"
}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "user_id": "uuid-v4",
    "username": "johndoe",
    "bio": "Updated bio",
    "profile_picture": "https://storage.com/profile.jpg"
  },
  "message": "Profile updated successfully",
  "timestamp": "2025-10-06T10:30:00Z"
}
```

---

### 2.3 Get User by ID
**GET** `/users/{user_id}`

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "user_id": "uuid-v4",
    "username": "johndoe",
    "bio": "Software developer",
    "profile_picture": "https://storage.com/profile.jpg",
    "followers_count": 150,
    "following_count": 200,
    "posts_count": 45,
    "is_following": false
  },
  "message": "User retrieved successfully",
  "timestamp": "2025-10-06T10:30:00Z"
}
```

---

### 2.4 Search Users
**GET** `/users/search?query={search_term}&page=1&limit=20`

**Query Parameters:**
- `query` (required): Search term
- `page` (optional, default: 1): Page number
- `limit` (optional, default: 20, max: 100): Results per page

**Response:** `200 OK`
```json
{
  "success": true,
  "data": [
    {
      "user_id": "uuid-v4",
      "username": "johndoe",
      "profile_picture": "https://storage.com/profile.jpg",
      "followers_count": 150
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 45,
    "pages": 3
  },
  "message": "Users retrieved successfully",
  "timestamp": "2025-10-06T10:30:00Z"
}
```

---

## 3. Social Features

### 3.1 Follow User
**POST** `/users/{user_id}/follow`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "user_id": "uuid-v4",
    "is_following": true
  },
  "message": "User followed successfully",
  "timestamp": "2025-10-06T10:30:00Z"
}
```

**Errors:**
- `404` - User not found
- `409` - Already following this user

---

### 3.2 Unfollow User
**DELETE** `/users/{user_id}/follow`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "user_id": "uuid-v4",
    "is_following": false
  },
  "message": "User unfollowed successfully",
  "timestamp": "2025-10-06T10:30:00Z"
}
```

---

### 3.3 Get Followers
**GET** `/users/{user_id}/followers?page=1&limit=20`

**Response:** `200 OK`
```json
{
  "success": true,
  "data": [
    {
      "user_id": "uuid-v4",
      "username": "janedoe",
      "profile_picture": "https://storage.com/profile.jpg",
      "followers_count": 200
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "pages": 8
  },
  "message": "Followers retrieved successfully",
  "timestamp": "2025-10-06T10:30:00Z"
}
```

---

### 3.4 Get Following
**GET** `/users/{user_id}/following?page=1&limit=20`

**Response:** `200 OK`
```json
{
  "success": true,
  "data": [
    {
      "user_id": "uuid-v4",
      "username": "janedoe",
      "profile_picture": "https://storage.com/profile.jpg",
      "followers_count": 200
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 200,
    "pages": 10
  },
  "message": "Following list retrieved successfully",
  "timestamp": "2025-10-06T10:30:00Z"
}
```

---

## 4. Posts

### 4.1 Create Post
**POST** `/posts`

**Headers:** 
- `Authorization: Bearer <token>`
- `Content-Type: multipart/form-data` (for media uploads)

**Request Body (JSON):**
```json
{
  "content": "This is my post content",
  "media_urls": ["https://storage.com/image1.jpg"],
  "topics": ["technology", "science"],
  "visibility": "public"
}
```

**Response:** `201 Created`
```json
{
  "success": true,
  "data": {
    "post_id": "uuid-v4",
    "author": {
      "user_id": "uuid-v4",
      "username": "johndoe",
      "profile_picture": "https://storage.com/profile.jpg"
    },
    "content": "This is my post content",
    "media_urls": ["https://storage.com/image1.jpg"],
    "topics": ["technology", "science"],
    "likes_count": 0,
    "comments_count": 0,
    "created_at": "2025-10-06T10:30:00Z",
    "updated_at": "2025-10-06T10:30:00Z"
  },
  "message": "Post created successfully",
  "timestamp": "2025-10-06T10:30:00Z"
}
```

---

### 4.2 Get Post by ID
**GET** `/posts/{post_id}`

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "post_id": "uuid-v4",
    "author": {
      "user_id": "uuid-v4",
      "username": "johndoe",
      "profile_picture": "https://storage.com/profile.jpg"
    },
    "content": "This is my post content",
    "media_urls": ["https://storage.com/image1.jpg"],
    "topics": ["technology", "science"],
    "likes_count": 42,
    "comments_count": 15,
    "is_liked": false,
    "created_at": "2025-10-06T10:30:00Z",
    "updated_at": "2025-10-06T10:30:00Z"
  },
  "message": "Post retrieved successfully",
  "timestamp": "2025-10-06T10:30:00Z"
}
```

---

### 4.3 Get Feed
**GET** `/posts/feed?page=1&limit=20&topic=technology`

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
- `page` (optional, default: 1)
- `limit` (optional, default: 20, max: 100)
- `topic` (optional): Filter by topic

**Response:** `200 OK`
```json
{
  "success": true,
  "data": [
    {
      "post_id": "uuid-v4",
      "author": {
        "user_id": "uuid-v4",
        "username": "johndoe",
        "profile_picture": "https://storage.com/profile.jpg"
      },
      "content": "This is my post content",
      "media_urls": ["https://storage.com/image1.jpg"],
      "topics": ["technology"],
      "likes_count": 42,
      "comments_count": 15,
      "is_liked": false,
      "created_at": "2025-10-06T10:30:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "pages": 8
  },
  "message": "Feed retrieved successfully",
  "timestamp": "2025-10-06T10:30:00Z"
}
```

---

### 4.4 Get User Posts
**GET** `/users/{user_id}/posts?page=1&limit=20`

**Response:** `200 OK`
```json
{
  "success": true,
  "data": [
    {
      "post_id": "uuid-v4",
      "author": {
        "user_id": "uuid-v4",
        "username": "johndoe",
        "profile_picture": "https://storage.com/profile.jpg"
      },
      "content": "This is my post content",
      "media_urls": ["https://storage.com/image1.jpg"],
      "topics": ["technology"],
      "likes_count": 42,
      "comments_count": 15,
      "is_liked": false,
      "created_at": "2025-10-06T10:30:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 45,
    "pages": 3
  },
  "message": "User posts retrieved successfully",
  "timestamp": "2025-10-06T10:30:00Z"
}
```

---

### 4.5 Update Post
**PATCH** `/posts/{post_id}`

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "content": "Updated content",
  "topics": ["technology", "ai"]
}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "post_id": "uuid-v4",
    "content": "Updated content",
    "topics": ["technology", "ai"],
    "updated_at": "2025-10-06T10:35:00Z"
  },
  "message": "Post updated successfully",
  "timestamp": "2025-10-06T10:35:00Z"
}
```

**Errors:**
- `403` - Not authorized to edit this post
- `404` - Post not found

---

### 4.6 Delete Post
**DELETE** `/posts/{post_id}`

**Headers:** `Authorization: Bearer <token>`

**Response:** `204 No Content`

---

### 4.7 Like Post
**POST** `/posts/{post_id}/like`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "post_id": "uuid-v4",
    "is_liked": true,
    "likes_count": 43
  },
  "message": "Post liked successfully",
  "timestamp": "2025-10-06T10:30:00Z"
}
```

---

### 4.8 Unlike Post
**DELETE** `/posts/{post_id}/like`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "post_id": "uuid-v4",
    "is_liked": false,
    "likes_count": 42
  },
  "message": "Post unliked successfully",
  "timestamp": "2025-10-06T10:30:00Z"
}
```

---

## 5. Comments

### 5.1 Create Comment
**POST** `/posts/{post_id}/comments`

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "content": "Great post!",
  "parent_comment_id": null
}
```

**Response:** `201 Created`
```json
{
  "success": true,
  "data": {
    "comment_id": "uuid-v4",
    "post_id": "uuid-v4",
    "author": {
      "user_id": "uuid-v4",
      "username": "johndoe",
      "profile_picture": "https://storage.com/profile.jpg"
    },
    "content": "Great post!",
    "likes_count": 0,
    "replies_count": 0,
    "created_at": "2025-10-06T10:30:00Z"
  },
  "message": "Comment created successfully",
  "timestamp": "2025-10-06T10:30:00Z"
}
```

---

### 5.2 Get Comments
**GET** `/posts/{post_id}/comments?page=1&limit=20`

**Response:** `200 OK`
```json
{
  "success": true,
  "data": [
    {
      "comment_id": "uuid-v4",
      "author": {
        "user_id": "uuid-v4",
        "username": "johndoe",
        "profile_picture": "https://storage.com/profile.jpg"
      },
      "content": "Great post!",
      "likes_count": 5,
      "replies_count": 2,
      "is_liked": false,
      "created_at": "2025-10-06T10:30:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 15,
    "pages": 1
  },
  "message": "Comments retrieved successfully",
  "timestamp": "2025-10-06T10:30:00Z"
}
```

---

### 5.3 Delete Comment
**DELETE** `/comments/{comment_id}`

**Headers:** `Authorization: Bearer <token>`

**Response:** `204 No Content`

---

### 5.4 Like Comment
**POST** `/comments/{comment_id}/like`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "comment_id": "uuid-v4",
    "is_liked": true,
    "likes_count": 6
  },
  "message": "Comment liked successfully",
  "timestamp": "2025-10-06T10:30:00Z"
}
```

---

## 6. Media Upload

### 6.1 Upload Image
**POST** `/upload/image`

**Headers:** 
- `Authorization: Bearer <token>`
- `Content-Type: multipart/form-data`

**Request Body (Form Data):**
- `file`: Image file (JPEG, PNG, max 5MB)

**Response:** `201 Created`
```json
{
  "success": true,
  "data": {
    "url": "https://storage.com/images/uuid-v4.jpg",
    "thumbnail_url": "https://storage.com/images/uuid-v4_thumb.jpg",
    "size": 1024000,
    "mime_type": "image/jpeg"
  },
  "message": "Image uploaded successfully",
  "timestamp": "2025-10-06T10:30:00Z"
}
```

**Errors:**
- `400` - Invalid file format or size exceeds limit
- `413` - File too large

---

### 6.2 Upload Video
**POST** `/upload/video`

**Headers:** 
- `Authorization: Bearer <token>`
- `Content-Type: multipart/form-data`

**Request Body (Form Data):**
- `file`: Video file (MP4, MOV, max 100MB)

**Response:** `201 Created`
```json
{
  "success": true,
  "data": {
    "url": "https://storage.com/videos/uuid-v4.mp4",
    "thumbnail_url": "https://storage.com/videos/uuid-v4_thumb.jpg",
    "size": 50240000,
    "duration": 120,
    "mime_type": "video/mp4"
  },
  "message": "Video uploaded successfully",
  "timestamp": "2025-10-06T10:30:00Z"
}
```

---

## 7. Notifications

### 7.1 Get Notifications
**GET** `/notifications?page=1&limit=20&unread_only=true`

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
- `page` (optional, default: 1)
- `limit` (optional, default: 20)
- `unread_only` (optional, default: false)

**Response:** `200 OK`
```json
{
  "success": true,
  "data": [
    {
      "notification_id": "uuid-v4",
      "type": "like",
      "actor": {
        "user_id": "uuid-v4",
        "username": "janedoe",
        "profile_picture": "https://storage.com/profile.jpg"
      },
      "target": {
        "type": "post",
        "id": "uuid-v4"
      },
      "message": "janedoe liked your post",
      "is_read": false,
      "created_at": "2025-10-06T10:30:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 45,
    "pages": 3
  },
  "message": "Notifications retrieved successfully",
  "timestamp": "2025-10-06T10:30:00Z"
}
```

**Notification Types:**
- `like` - Someone liked your post/comment
- `comment` - Someone commented on your post
- `follow` - Someone followed you
- `mention` - Someone mentioned you
- `quiz_invite` - Invited to a quiz
- `group_invite` - Invited to a group

---

### 7.2 Mark