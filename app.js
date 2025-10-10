const API_BASE_URL = 'http://localhost:8000';

let authToken = localStorage.getItem('authToken') || null;
let currentUserData = JSON.parse(localStorage.getItem('currentUser')) || null;

document.addEventListener('DOMContentLoaded', () => {
    if (authToken && currentUserData) {
        showApp();
    }
});

function showAuthMessage(message, isError = false) {
    const messageDiv = document.getElementById('authMessage');
    messageDiv.className = isError ? 'error-message' : 'success-message';
    messageDiv.textContent = message;
    messageDiv.style.display = 'block';

    setTimeout(() => {
        messageDiv.style.display = 'none';
    }, 5000);
}

function showRegisterForm() {
    document.getElementById('loginForm').style.display = 'none';
    document.getElementById('registerForm').style.display = 'block';
    document.getElementById('authSubtitle').textContent = 'Create a new account';
}

function showLoginForm() {
    document.getElementById('registerForm').style.display = 'none';
    document.getElementById('loginForm').style.display = 'block';
    document.getElementById('authSubtitle').textContent = 'Connect with friends and the world';
}

async function register() {
    const email = document.getElementById('registerEmail').value;
    const username = document.getElementById('registerUsername').value;
    const password = document.getElementById('registerPassword').value;
    const dateOfBirth = document.getElementById('registerDOB').value;

    if (!email || !username || !password || !dateOfBirth) {
        showAuthMessage('Please fill in all fields', true);
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                email,
                username,
                password,
                date_of_birth: dateOfBirth
            })
        });

        const data = await response.json();

        if (response.ok) {
            showAuthMessage('Registration successful! Please log in.');
            showLoginForm();
        } else {
            showAuthMessage(data.message || 'Registration failed', true);
        }
    } catch (error) {
        showAuthMessage('Network error. Please try again.', true);
    }
}

async function login() {
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;

    if (!email || !password) {
        showAuthMessage('Please fill in all fields', true);
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (response.ok && data.data && data.data.access_token) {
            authToken = data.data.access_token;
            currentUserData = data.data.user;
            localStorage.setItem('authToken', authToken);
            localStorage.setItem('currentUser', JSON.stringify(currentUserData));
            showApp();
        } else {
            showAuthMessage(data.message || 'Login failed', true);
        }
    } catch (error) {
        showAuthMessage('Network error. Please try again.', true);
    }
}

async function logout() {
    try {
        await fetch(`${API_BASE_URL}/auth/logout`, {
            method: 'POST',
            headers: getAuthHeaders()
        });
    } catch (error) {
        console.error('Logout error:', error);
    }

    authToken = null;
    currentUserData = null;
    localStorage.removeItem('authToken');
    localStorage.removeItem('currentUser');

    document.getElementById('authContainer').style.display = 'flex';
    document.getElementById('appContainer').classList.remove('active');
}

function getAuthHeaders() {
    return {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authToken}`
    };
}

function showApp() {
    document.getElementById('authContainer').style.display = 'none';
    document.getElementById('appContainer').classList.add('active');

    updateNavbar();
    loadUserProfile();
    loadFeed();
}

function updateNavbar() {
    const username = currentUserData.username || currentUserData.email;
    const profilePicture = currentUserData.profile_picture || 'https://via.placeholder.com/40';

    document.getElementById('navUsername').textContent = username;
    document.getElementById('navAvatar').src = profilePicture;
}

async function loadUserProfile() {
    try {
        const response = await fetch(`${API_BASE_URL}/users/profile/${currentUserData.user_id}`, {
            headers: getAuthHeaders()
        });

        const data = await response.json();

        if (response.ok && data.data) {
            document.getElementById('sidebarUsername').textContent = data.data.username;
            document.getElementById('sidebarBio').textContent = data.data.bio || 'No bio yet';
            document.getElementById('postsCount').textContent = data.data.posts_count || 0;
            document.getElementById('followersCount').textContent = data.data.followers_count || 0;
            document.getElementById('followingCount').textContent = data.data.following_count || 0;
        }
    } catch (error) {
        console.error('Error loading profile:', error);
    }
}

async function loadFeed() {
    const feedContent = document.getElementById('feedContent');
    feedContent.innerHTML = '<div class="loading">Loading your feed...</div>';

    try {
        const response = await fetch(`${API_BASE_URL}/feed/explore`, {
            headers: getAuthHeaders()
        });

        const data = await response.json();

        if (response.ok && data.data) {
            displayFeed(data.data);
        } else {
            feedContent.innerHTML = '<div class="empty-state"><h3>No posts yet</h3><p>Follow people to see their posts in your feed</p></div>';
        }
    } catch (error) {
        feedContent.innerHTML = '<div class="empty-state"><h3>Error loading feed</h3><p>Please try again later</p></div>';
    }
}

function displayFeed(posts) {
    const feedContent = document.getElementById('feedContent');

    if (!posts || posts.length === 0) {
        feedContent.innerHTML = '<div class="empty-state"><h3>No posts yet</h3><p>Be the first to share something!</p></div>';
        return;
    }

    feedContent.innerHTML = '';

    posts.forEach(post => {
        const postCard = createPostCard(post);
        feedContent.appendChild(postCard);
    });
}

function createPostCard(post) {
    const card = document.createElement('div');
    card.className = 'post-card';
    card.dataset.postId = post.post_id;

    const authorName = post.author ? post.author.username : 'Unknown';
    const authorAvatar = post.author && post.author.profile_picture ? post.author.profile_picture : 'https://via.placeholder.com/40';
    const postTime = formatTime(post.created_at);
    const isLiked = post.is_liked || false;
    const likesCount = post.likes_count || 0;
    const commentsCount = post.comments_count || 0;

    card.innerHTML = `
        <div class="post-header">
            <img class="post-avatar" src="${authorAvatar}" alt="${authorName}">
            <div class="post-author-info">
                <div class="post-author-name">${authorName}</div>
                <div class="post-time">${postTime}</div>
            </div>
        </div>
        <div class="post-content">${post.content}</div>
        ${post.media_url ? `<img class="post-image" src="${post.media_url}" alt="Post image">` : ''}
        <div class="post-stats">
            <span>${likesCount} likes</span>
            <span>${commentsCount} comments</span>
        </div>
        <div class="post-actions">
            <button class="post-action-btn ${isLiked ? 'liked' : ''}" onclick="toggleLike('${post.post_id}')">
                ${isLiked ? '❤️' : '🤍'} Like
            </button>
            <button class="post-action-btn" onclick="toggleComments('${post.post_id}')">
                💬 Comment
            </button>
        </div>
        <div class="comments-section" id="comments-${post.post_id}">
            <div class="comment-input-wrapper">
                <input type="text" class="comment-input" id="comment-input-${post.post_id}" placeholder="Write a comment...">
                <button class="btn-comment" onclick="postComment('${post.post_id}')">Post</button>
            </div>
            <div id="comments-list-${post.post_id}">
                <div class="loading">Loading comments...</div>
            </div>
        </div>
    `;

    return card;
}

function formatTime(timestamp) {
    const date = new Date(timestamp);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;

    return date.toLocaleDateString();
}

async function toggleLike(postId) {
    try {
        const response = await fetch(`${API_BASE_URL}/posts/like-deslike/${postId}`, {
            method: 'POST',
            headers: getAuthHeaders()
        });

        const data = await response.json();

        if (response.ok) {
            const postCard = document.querySelector(`[data-post-id="${postId}"]`);
            const likeBtn = postCard.querySelector('.post-action-btn');
            const isLiked = data.data.is_liked;

            likeBtn.classList.toggle('liked', isLiked);
            likeBtn.innerHTML = `${isLiked ? '❤️' : '🤍'} Like`;

            const statsDiv = postCard.querySelector('.post-stats span:first-child');
            const currentLikes = parseInt(statsDiv.textContent);
            statsDiv.textContent = `${isLiked ? currentLikes + 1 : currentLikes - 1} likes`;
        }
    } catch (error) {
        console.error('Error toggling like:', error);
    }
}

async function toggleComments(postId) {
    const commentsSection = document.getElementById(`comments-${postId}`);
    const isVisible = commentsSection.classList.contains('active');

    if (isVisible) {
        commentsSection.classList.remove('active');
    } else {
        commentsSection.classList.add('active');
        await loadComments(postId);
    }
}

async function loadComments(postId) {
    const commentsList = document.getElementById(`comments-list-${postId}`);
    commentsList.innerHTML = '<div class="loading">Loading comments...</div>';

    try {
        const response = await fetch(`${API_BASE_URL}/posts/comments/all?post_id=${postId}`, {
            headers: getAuthHeaders()
        });

        const data = await response.json();

        if (response.ok && data.data && data.data.length > 0) {
            commentsList.innerHTML = '';
            data.data.forEach(comment => {
                const commentEl = createCommentElement(comment);
                commentsList.appendChild(commentEl);
            });
        } else {
            commentsList.innerHTML = '<p style="text-align: center; color: #65676b;">No comments yet</p>';
        }
    } catch (error) {
        commentsList.innerHTML = '<p style="text-align: center; color: #65676b;">Error loading comments</p>';
    }
}

function createCommentElement(comment) {
    const div = document.createElement('div');
    div.className = 'comment';
    div.dataset.commentId = comment.comment_id;

    const isLiked = comment.is_liked_by_me || false;
    const likesCount = comment.likes_nbr || 0;

    div.innerHTML = `
        <div class="comment-header">
            <img class="comment-avatar" src="${comment.profile_picture || 'https://via.placeholder.com/32'}" alt="${comment.username}">
            <div>
                <div class="comment-author">${comment.username}</div>
                <div class="comment-time">${formatTime(comment.created_at)}</div>
            </div>
        </div>
        <div class="comment-content">${comment.comment_payload}</div>
        <div class="comment-actions">
            <span class="comment-action ${isLiked ? 'liked' : ''}" onclick="toggleCommentLike('${comment.comment_id}')">
                ${isLiked ? '❤️' : '🤍'} ${likesCount} Like${likesCount !== 1 ? 's' : ''}
            </span>
        </div>
    `;

    return div;
}

async function postComment(postId) {
    const input = document.getElementById(`comment-input-${postId}`);
    const content = input.value.trim();

    if (!content) return;

    try {
        const response = await fetch(`${API_BASE_URL}/posts/comments/create?post_id=${postId}`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify({ content })
        });

        if (response.ok) {
            input.value = '';
            await loadComments(postId);

            const postCard = document.querySelector(`[data-post-id="${postId}"]`);
            const statsDiv = postCard.querySelector('.post-stats span:last-child');
            const currentCount = parseInt(statsDiv.textContent);
            statsDiv.textContent = `${currentCount + 1} comments`;
        }
    } catch (error) {
        console.error('Error posting comment:', error);
    }
}

async function toggleCommentLike(commentId) {
    try {
        const response = await fetch(`${API_BASE_URL}/posts/comments/like-deslike/${commentId}`, {
            method: 'POST',
            headers: getAuthHeaders()
        });

        const data = await response.json();

        if (response.ok) {
            const commentEl = document.querySelector(`[data-comment-id="${commentId}"]`);
            const likeAction = commentEl.querySelector('.comment-action');
            const isLiked = data.data.is_liked;
            const likesCount = data.data.likes_nbr || 0;

            likeAction.classList.toggle('liked', isLiked);
            likeAction.innerHTML = `${isLiked ? '❤️' : '🤍'} ${likesCount} Like${likesCount !== 1 ? 's' : ''}`;
        }
    } catch (error) {
        console.error('Error toggling comment like:', error);
    }
}

function openCreatePostModal() {
    document.getElementById('createPostModal').classList.add('active');
}

function closeCreatePostModal() {
    document.getElementById('createPostModal').classList.remove('active');
    document.getElementById('createPostContent').value = '';
    document.getElementById('createPostImage').value = '';
}

async function createPost() {
    const content = document.getElementById('createPostContent').value.trim();
    const mediaUrl = document.getElementById('createPostImage').value.trim();

    if (!content) {
        alert('Please write something!');
        return;
    }

    const body = { content };
    if (mediaUrl) {
        body.media_url = mediaUrl;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/posts/create`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify(body)
        });

        if (response.ok) {
            closeCreatePostModal();
            loadFeed();
            loadUserProfile();
        } else {
            alert('Failed to create post');
        }
    } catch (error) {
        alert('Network error. Please try again.');
    }
}

async function handleSearch(event) {
    if (event.key === 'Enter') {
        const username = document.getElementById('searchInput').value.trim();

        if (!username) return;

        try {
            const response = await fetch(`${API_BASE_URL}/users/search?username=${encodeURIComponent(username)}`, {
                headers: getAuthHeaders()
            });

            const data = await response.json();

            if (response.ok && data.data) {
                alert(`Found user: ${data.data.username}\nFollowers: ${data.data.followers_count}\nFollowing: ${data.data.following_count}`);
            } else {
                alert('User not found');
            }
        } catch (error) {
            alert('Search error');
        }
    }
}