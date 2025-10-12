const API_BASE_URL = 'http://localhost:8000';

let authToken = localStorage.getItem('authToken') || null;
let currentUserData = JSON.parse(localStorage.getItem('currentUser')) || null;
let currentPage = 'feed';
let currentProfileUserId = null;

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

    if (!email || !username || !password) {
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
                password
            })
        });

        const data = await response.json();

        if (data.success) {
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

        if (data.success && data.data && data.data.access_token) {
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
    loadFeedPage();
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

        if (data.success && data.data) {
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

function loadFeedPage() {
    currentPage = 'feed';
    document.getElementById('createPostCard').style.display = 'block';
    loadFeed();
}

function loadExplorePage() {
    currentPage = 'explore';
    document.getElementById('createPostCard').style.display = 'block';
    loadExplore();
}

async function loadFeed() {
    const feedContent = document.getElementById('feedContent');
    feedContent.innerHTML = '<div class="loading">Loading your feed...</div>';

    try {
        const response = await fetch(`${API_BASE_URL}/feed/`, {
            headers: getAuthHeaders()
        });

        const data = await response.json();

        if (data.success && data.data && data.data.length > 0) {
            displayFeed(data.data);
        } else {
            feedContent.innerHTML = '<div class="empty-state"><h3>No posts yet</h3><p>Follow people to see their posts in your feed</p></div>';
        }
    } catch (error) {
        feedContent.innerHTML = '<div class="empty-state"><h3>Error loading feed</h3><p>Please try again later</p></div>';
    }
}

async function loadExplore() {
    const feedContent = document.getElementById('feedContent');
    feedContent.innerHTML = '<div class="loading">Loading explore feed...</div>';

    try {
        const response = await fetch(`${API_BASE_URL}/feed/explore`, {
            headers: getAuthHeaders()
        });

        const data = await response.json();

        if (data.success && data.data && data.data.length > 0) {
            displayFeed(data.data);
        } else {
            feedContent.innerHTML = '<div class="empty-state"><h3>No posts yet</h3><p>Be the first to share something!</p></div>';
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

    const authorName = 'Unknown';
    const authorAvatar = 'https://via.placeholder.com/40';
    const postTime = formatTime(post.created_at);
    const isLiked = post.is_liked_by_me || false;
    const likesCount = post.likes_nbr || 0;
    const commentsCount = post.comments_nbr || 0;

    card.innerHTML = `
        <div class="post-header">
            <img class="post-avatar" src="${authorAvatar}" alt="${authorName}" onclick="viewProfile(${post.user_id})" style="cursor: pointer;">
            <div class="post-author-info">
                <div class="post-author-name" onclick="viewProfile(${post.user_id})" style="cursor: pointer;">${authorName}</div>
                <div class="post-time">${postTime}</div>
            </div>
            ${post.user_id == currentUserData.user_id ? `<button class="post-menu-btn" onclick="deletePost(${post.post_id})">🗑️</button>` : ''}
        </div>
        <div class="post-content">${post.content || ''}</div>
        ${post.media_url ? `<img class="post-image" src="${post.media_url}" alt="Post image">` : ''}
        <div class="post-stats">
            <span onclick="viewPostLikes(${post.post_id})">${likesCount} likes</span>
            <span>${commentsCount} comments</span>
        </div>
        <div class="post-actions">
            <button class="post-action-btn ${isLiked ? 'liked' : ''}" onclick="toggleLike(${post.post_id})">
                ${isLiked ? '❤️' : '🤍'} Like
            </button>
            <button class="post-action-btn" onclick="toggleComments(${post.post_id})">
                💬 Comment
            </button>
        </div>
        <div class="comments-section" id="comments-${post.post_id}">
            <div class="comment-input-wrapper">
                <input type="text" class="comment-input" id="comment-input-${post.post_id}" placeholder="Write a comment...">
                <button class="btn-comment" onclick="postComment(${post.post_id})">Post</button>
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

        if (data.success && data.data) {
            const postCard = document.querySelector(`[data-post-id="${postId}"]`);
            const likeBtn = postCard.querySelector('.post-action-btn');
            const isLiked = data.data.is_liked_by_me;

            likeBtn.classList.toggle('liked', isLiked);
            likeBtn.innerHTML = `${isLiked ? '❤️' : '🤍'} Like`;

            const statsDiv = postCard.querySelector('.post-stats span:first-child');
            statsDiv.textContent = `${data.data.likes_nbr} likes`;
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

        if (data.success && data.data && data.data.length > 0) {
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
            <span class="comment-action ${isLiked ? 'liked' : ''}" onclick="toggleCommentLike(${comment.comment_id}, ${comment.post_id})">
                ${isLiked ? '❤️' : '🤍'} Like
            </span>
            <span class="comment-action" onclick="viewCommentLikes(${comment.comment_id})" style="color: #65676b;">
                ${likesCount} ${likesCount !== 1 ? 'likes' : 'like'}
            </span>
            ${comment.user_id == currentUserData.user_id ? `<span class="comment-action" onclick="deleteComment(${comment.comment_id}, ${comment.post_id})">Delete</span>` : ''}
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

async function toggleCommentLike(commentId, postId) {
    try {
        const response = await fetch(`${API_BASE_URL}/posts/comments/like-deslike?comment_id=${parseInt(commentId)}`, {
            method: 'POST',
            headers: getAuthHeaders()
        });

        const data = await response.json();

        if (data.success && data.data) {
            const commentEl = document.querySelector(`[data-comment-id="${commentId}"]`);
            const likeAction = commentEl.querySelector('.comment-action');
            const isLiked = data.data.is_liked_by_me;
            const likesCount = data.data.likes_nbr || 0;

            likeAction.classList.toggle('liked', isLiked);
            likeAction.innerHTML = `${isLiked ? '❤️' : '🤍'} ${likesCount} Like${likesCount !== 1 ? 's' : ''}`;
        }
    } catch (error) {
        console.error('Error toggling comment like:', error);
    }
}

async function deleteComment(commentId, postId) {
    if (!confirm('Delete this comment?')) return;

    try {
        const response = await fetch(`${API_BASE_URL}/posts/comments/delete?comment_id=${commentId}&post_id=${postId}`, {
            method: 'DELETE',
            headers: getAuthHeaders()
        });

        if (response.ok) {
            await loadComments(postId);
            const postCard = document.querySelector(`[data-post-id="${postId}"]`);
            const statsDiv = postCard.querySelector('.post-stats span:last-child');
            const currentCount = parseInt(statsDiv.textContent);
            statsDiv.textContent = `${currentCount - 1} comments`;
        }
    } catch (error) {
        console.error('Error deleting comment:', error);
    }
}

async function deletePost(postId) {
    if (!confirm('Delete this post?')) return;

    try {
        const response = await fetch(`${API_BASE_URL}/posts/delete?post_id=${postId}`, {
            method: 'DELETE',
            headers: getAuthHeaders()
        });

        if (response.ok) {
            if (currentPage === 'feed') {
                loadFeed();
            } else if (currentPage === 'explore') {
                loadExplore();
            } else {
                viewProfile(currentUserData.user_id);
            }
            loadUserProfile();
        }
    } catch (error) {
        console.error('Error deleting post:', error);
    }
}

function openCreatePostModal() {
    document.getElementById('createPostModal').classList.add('active');
}

function closeCreatePostModal() {
    document.getElementById('createPostModal').classList.remove('active');
    document.getElementById('createPostContent').value = '';
    document.getElementById('createPostFile').value = '';
}

async function createPost() {
    const content = document.getElementById('createPostContent').value.trim();
    const fileInput = document.getElementById('createPostFile');
    const file = fileInput.files[0];

    if (!content && !file) {
        alert('Please write something or select an image!');
        return;
    }

    try {
        const formData = new FormData();
        if (content) formData.append('content', content);
        if (file) formData.append('media_file', file);

        const response = await fetch(`${API_BASE_URL}/posts/create`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${authToken}`
            },
            body: formData
        });

        if (response.ok) {
            closeCreatePostModal();
            if (currentPage === 'feed') {
                loadFeed();
            } else if (currentPage === 'explore') {
                loadExplore();
            }
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

            if (data.success && data.data && data.data.length > 0) {
                showSearchResults(data.data);
            } else {
                alert('No users found');
            }
        } catch (error) {
            alert('Search error');
        }
    }
}

function showSearchResults(users) {
    const modal = document.getElementById('searchResultsModal');
    const list = document.getElementById('searchResultsList');

    list.innerHTML = '';

    users.forEach(user => {
        const userCard = document.createElement('div');
        userCard.className = 'user-card';
        userCard.onclick = () => {
            closeSearchResultsModal();
            viewProfile(user.user_id);
        };

        userCard.innerHTML = `
            <img class="user-card-avatar" src="${user.profile_picture || 'https://via.placeholder.com/50'}" alt="${user.username}">
            <div class="user-card-info">
                <div class="user-card-name">${user.username}</div>
                <div class="user-card-bio">${user.bio || 'No bio'}</div>
            </div>
        `;

        list.appendChild(userCard);
    });

    modal.classList.add('active');
}

function closeSearchResultsModal() {
    document.getElementById('searchResultsModal').classList.remove('active');
}

async function viewProfile(userId) {
    currentPage = 'profile';
    document.getElementById('createPostCard').style.display = 'none';

    try {
        const response = await fetch(`${API_BASE_URL}/users/profile/${userId}`, {
            headers: getAuthHeaders()
        });

        const data = await response.json();

        if (data.success && data.data) {
            showProfileModal(data.data);
        }
    } catch (error) {
        console.error('Error loading profile:', error);
    }
}

function viewMyProfile() {
    viewProfile(currentUserData.user_id);
}

async function showProfileModal(profile) {
    currentProfileUserId = profile.user_id;

    document.getElementById('profileModalUsername').textContent = profile.username;
    document.getElementById('profileModalAvatar').src = profile.profile_picture || 'https://via.placeholder.com/100';
    document.getElementById('profileModalName').textContent = profile.username;
    document.getElementById('profileModalEmail').textContent = profile.email;
    document.getElementById('profileModalBio').textContent = profile.bio || 'No bio yet';
    document.getElementById('profileModalPosts').textContent = profile.posts_count || 0;
    document.getElementById('profileModalFollowers').textContent = profile.followers_count || 0;
    document.getElementById('profileModalFollowing').textContent = profile.following_count || 0;

    const actionsDiv = document.getElementById('profileModalActions');
    actionsDiv.innerHTML = '';

    if (profile.user_id != currentUserData.user_id) {
        const followBtn = document.createElement('button');
        followBtn.className = `btn-follow ${profile.is_following ? 'following' : ''}`;
        followBtn.textContent = profile.is_following ? 'Unfollow' : 'Follow';
        followBtn.onclick = () => toggleFollow(profile.user_id, followBtn);
        actionsDiv.appendChild(followBtn);
    }

    await loadUserPosts(profile.user_id);

    document.getElementById('profileModal').classList.add('active');
}

function closeProfileModal() {
    document.getElementById('profileModal').classList.remove('active');
    currentPage = 'feed';
    document.getElementById('createPostCard').style.display = 'block';
}

async function loadUserPosts(userId) {
    const postsList = document.getElementById('profilePostsList');
    postsList.innerHTML = '<div class="loading">Loading posts...</div>';

    try {
        const response = await fetch(`${API_BASE_URL}/posts/${userId}`, {
            headers: getAuthHeaders()
        });

        const data = await response.json();

        if (data.success && data.data && data.data.length > 0) {
            postsList.innerHTML = '';
            data.data.forEach(post => {
                const postCard = createPostCard(post);
                postsList.appendChild(postCard);
            });
        } else {
            postsList.innerHTML = '<div class="empty-state"><h3>No posts yet</h3></div>';
        }
    } catch (error) {
        postsList.innerHTML = '<div class="empty-state"><h3>Error loading posts</h3></div>';
    }
}

async function toggleFollow(userId, button) {
    try {
        const response = await fetch(`${API_BASE_URL}/users/follow-unfollow/?target_user_id=${userId}`, {
            method: 'POST',
            headers: getAuthHeaders()
        });

        const data = await response.json();

        if (data.success && data.data) {
            const isFollowing = data.data.is_following;
            button.className = `btn-follow ${isFollowing ? 'following' : ''}`;
            button.textContent = isFollowing ? 'Unfollow' : 'Follow';
            loadUserProfile();

            const currentFollowers = parseInt(document.getElementById('profileModalFollowers').textContent);
            document.getElementById('profileModalFollowers').textContent = isFollowing ? currentFollowers + 1 : currentFollowers - 1;
        }
    } catch (error) {
        console.error('Error toggling follow:', error);
    }
}

async function viewFollowers() {
    if (!currentProfileUserId) return;

    const modal = document.getElementById('followersModal');
    const list = document.getElementById('followersList');
    const title = document.getElementById('followersModalTitle');

    title.textContent = 'Followers';
    list.innerHTML = '<div class="loading">Loading followers...</div>';
    modal.classList.add('active');

    try {
        const response = await fetch(`${API_BASE_URL}/users/followers?user_id=${currentProfileUserId}`, {
            headers: getAuthHeaders()
        });

        const data = await response.json();

        if (data.success && data.data && data.data.length > 0) {
            list.innerHTML = '';
            data.data.forEach(user => {
                const userCard = createUserCard(user);
                list.appendChild(userCard);
            });
        } else {
            list.innerHTML = '<div class="empty-state"><h3>No followers yet</h3></div>';
        }
    } catch (error) {
        list.innerHTML = '<div class="empty-state"><h3>Error loading followers</h3></div>';
    }
}

async function viewFollowing() {
    if (!currentProfileUserId) return;

    const modal = document.getElementById('followersModal');
    const list = document.getElementById('followersList');
    const title = document.getElementById('followersModalTitle');

    title.textContent = 'Following';
    list.innerHTML = '<div class="loading">Loading following...</div>';
    modal.classList.add('active');

    try {
        const response = await fetch(`${API_BASE_URL}/users/followings?user_id=${currentProfileUserId}`, {
            headers: getAuthHeaders()
        });

        const data = await response.json();

        if (data.success && data.data && data.data.length > 0) {
            list.innerHTML = '';
            data.data.forEach(user => {
                const userCard = createUserCard(user);
                list.appendChild(userCard);
            });
        } else {
            list.innerHTML = '<div class="empty-state"><h3>Not following anyone yet</h3></div>';
        }
    } catch (error) {
        list.innerHTML = '<div class="empty-state"><h3>Error loading following</h3></div>';
    }
}

function closeFollowersModal() {
    document.getElementById('followersModal').classList.remove('active');
}

function createUserCard(user) {
    const userCard = document.createElement('div');
    userCard.className = 'user-card';

    userCard.innerHTML = `
        <img class="user-card-avatar" src="${user.profile_picture || 'https://via.placeholder.com/50'}" alt="${user.username}">
        <div class="user-card-info">
            <div class="user-card-name">${user.username}</div>
            <div class="user-card-bio">${user.bio || 'No bio'}</div>
        </div>
    `;

    userCard.onclick = () => {
        closeFollowersModal();
        closeProfileModal();
        viewProfile(user.user_id);
    };

    return userCard;
}

async function viewPostLikes(postId) {
    const modal = document.getElementById('likesModal');
    const list = document.getElementById('likesList');

    list.innerHTML = '<div class="loading">Loading likes...</div>';
    modal.classList.add('active');

    try {
        const response = await fetch(`${API_BASE_URL}/posts/likes?post_id=${parseInt(postId)}`, {
            headers: getAuthHeaders()
        });

        const data = await response.json();

        if (data.success && data.data && data.data.length > 0) {
            list.innerHTML = '';
            data.data.forEach(user => {
                const userCard = createUserCard(user);
                list.appendChild(userCard);
            });
        } else {
            list.innerHTML = '<div class="empty-state"><h3>No likes yet</h3></div>';
        }
    } catch (error) {
        list.innerHTML = '<div class="empty-state"><h3>Error loading likes</h3><p>This feature may not be available in the API</p></div>';
    }
}

async function viewCommentLikes(commentId) {
    const modal = document.getElementById('likesModal');
    const list = document.getElementById('likesList');

    list.innerHTML = '<div class="loading">Loading likes...</div>';
    modal.classList.add('active');

    try {
        const response = await fetch(`${API_BASE_URL}/posts/comments/${commentId}/likes`, {
            headers: getAuthHeaders()
        });

        const data = await response.json();

        if (data.success && data.data && data.data.length > 0) {
            list.innerHTML = '';
            data.data.forEach(user => {
                const userCard = createUserCard(user);
                list.appendChild(userCard);
            });
        } else {
            list.innerHTML = '<div class="empty-state"><h3>No likes yet</h3></div>';
        }
    } catch (error) {
        list.innerHTML = '<div class="empty-state"><h3>Error loading likes</h3><p>This feature may not be available in the API</p></div>';
    }
}

function closeLikesModal() {
    document.getElementById('likesModal').classList.remove('active');
}
