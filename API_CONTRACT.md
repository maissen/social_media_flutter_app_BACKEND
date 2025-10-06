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
    "user_id": "v4",
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
    "user_id": "v4",
    "email": "user@example.com",
    "username": "johndoe",
    "bio": "Software developer and tech enthusiast",
    "profile_picture": "https://storage.com/profile.jpg",
    "followers_count": 150,
    "following_count": 200,
    "posts_count": 45,
    "created_at": "2025-01-15T10:30:00Z",
    "is_following": false
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
#### update profile bio
**PUT** `/users/update/profile-bio/<user-id>`

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "new_bio": "Updated bio"
}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "new_bio": "Updated bio"
  },
  "message": "Bio updated successfully",
  "timestamp": "2025-10-06T10:30:00Z"
}
```

#### update profile picture
**PUT** `/users/update/profile-picture/<user-id>`

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "profile_picture": "base64_encoded_image_or_url"
}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "profile_picture": "https://storage.com/profile.jpg"
  },
  "message": "Profile picture updated successfully",
  "timestamp": "2025-10-06T10:30:00Z"
}
```

---

### 2.4 Search Users
**GET** /users/search?username=user

**Query Parameters:**
- `user` (required): searched username

**Response:** `200 OK`
```json
{
  "success": true,
  "data": [
    {
      "user_id": "v5",
      "username": "Maissen",
      "profile_picture": "https://storage.com/profile.jpg",
      "followers_count": 150,
      "following_count": 200,
    },
    {
      "user_id": "v4",
      "username": "johndoe",
      "profile_picture": "https://storage.com/profile.jpg",
      "followers_count": 150,
      "following_count": 200,
    },  
  ],
  "message": "Users retrieved successfully",
  "timestamp": "2025-10-06T10:30:00Z"
}
```

---

## 3. Social Features

### 3.1 Follow User
**POST** `/users/follow-unfollow/<user_id>/<target_user_id>`

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "data": {
    "user_id": "v4",
    "target_user_id": "v5",
  }
}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "user_id": "v4",
    "target_user_id": "v5",
    "is_following": true/false
  },
  "message": "User followed/unfollowed successfully",
  "timestamp": "2025-10-06T10:30:00Z"
}
```

---

### 3.3 Get Followers
**GET** `/users/followers/<user-id>`

**Response:** `200 OK`
```json
{
  "success": true,
  "data": [
    {
      "user_id": "v4",
      "username": "janedoe",
      "profile_picture": "https://storage.com/profile.jpg",
    },
    {
      "user_id": "v4",
      "username": "janedoe",
      "profile_picture": "https://storage.com/profile.jpg",
    }
  ],
  "message": "Followers retrieved successfully",
  "timestamp": "2025-10-06T10:30:00Z"
}
```

---

### 3.4 Get Following
**GET** `/users/followings/<user-id>`

**Response:** `200 OK`
```json
{
  "success": true,
  "data": [
    {
      "user_id": "v4",
      "username": "janedoe",
      "profile_picture": "https://storage.com/profile.jpg",
    }
  ],
  "message": "Following list retrieved successfully",
  "timestamp": "2025-10-06T10:30:00Z"
}
```

---

## 4. Posts

### 4.1 Create a Post
**POST** `/posts/create`

**Headers:** 
- `Authorization: Bearer <token>`
- `Content-Type: multipart/form-data` (for media uploads)

**Request Body :**
```json
{
  "content": "This is my post content",
  "media_urls": ["https://storage.com/image1.jpg"],
}
```

**Response:** `201 Created`
```json
{
  "success": true,
  "data": {
    "post_id": "v4",
  },
  "message": "Post created successfully",
  "timestamp": "2025-10-06T10:30:00Z"
}
```

---

### 4.2 Get Posts of a user
**GET** `/posts/<user-id>`

**Response:** `200 OK`
```json
{
  "success": true,
  "data": [
    {
      "post_id": "v4",
      "content": "This is my post content",
      "media_urls": ["https://storage.com/image1.jpg"],
      "likes_count": 42,
      "comments_count": 15,
      "is_liked": false,
      "created_at": "2025-10-06T10:30:00Z",
    }
  ],
  "message": "Post retrieved successfully",
  "timestamp": "2025-10-06T10:30:00Z"
}
```

---

### 4.5 Update Post
**PUT** `/posts/update/<post-id>`

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
    "post_id": "v4",
    "content": "Updated content",
    "updated_at": "2025-10-06T10:35:00Z"
  },
  "message": "Post updated successfully",
  "timestamp": "2025-10-06T10:35:00Z"
}
```

---

### 4.6 Delete Post
**DELETE** `/posts/delete/<post-id>`

**Headers:** `Authorization: Bearer <token>`

**Response:** `204 No Content`

---

### 4.7 Like Post
**POST** `/posts/like-deslike/<post-id>`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "post_id": "v4",
    "is_liked": true/false,
  },
  "message": "Post liked/desliked successfully",
  "timestamp": "2025-10-06T10:30:00Z"
}
```

---

## 5. Comments

### 5.1 Create Comment
**POST** `/posts/comments/<post-id>`

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "content": "Great post!",
}
```

**Response:** `201 Created`
```json
{
  "success": true,
  "data": null,
  "message": "Comment created successfully",
  "timestamp": "2025-10-06T10:30:00Z"
}
```

---

### 5.2 Get Comments of a post
**GET** `/posts/comments/<post-id>`

**Response:** `200 OK`
```json
{
  "success": true,
  "data": [
    {
      "comment_id": "v4",
      "author": {
        "user_id": "v4",
        "username": "johndoe",
        "profile_picture": "https://storage.com/profile.jpg"
      },
      "content": "Great post!",
      "likes_count": 5,
      "is_liked": false,
      "created_at": "2025-10-06T10:30:00Z"
    },
    {
      "comment_id": "v4",
      "author": {
        "user_id": "v4",
        "username": "johndoe",
        "profile_picture": "https://storage.com/profile.jpg"
      },
      "content": "Great post!",
      "likes_count": 5,
      "is_liked": false,
      "created_at": "2025-10-06T10:30:00Z"
    }
  ],
  "message": "Comments retrieved successfully",
  "timestamp": "2025-10-06T10:30:00Z"
}
```

---

### 5.3 Delete Comment
**DELETE** `posts/comments/<comment_id>`

**Headers:** `Authorization: Bearer <token>`

**Response:** `204 No Content`

---

### 5.4 Like Comment
**POST** `posts/comments/like-deslike/<comment-id>`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "comment_id": "v4",
    "is_liked": true,
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
    "thumbnail_url": "https://storage.com/images/v4_thumb.jpg",
  },
  "message": "Image uploaded successfully",
  "timestamp": "2025-10-06T10:30:00Z"
}
```