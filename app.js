const API_BASE_URL = 'http://localhost:8000';

let authToken = localStorage.getItem('authToken') || null;
let currentUserData = JSON.parse(localStorage.getItem('currentUser')) || null;

document.addEventListener('DOMContentLoaded', () => {
    setupTabs();
    updateAuthStatus();
});

function setupTabs() {
    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const tabName = tab.getAttribute('data-tab');
            switchTab(tabName);
        });
    });
}

function switchTab(tabName) {
    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });

    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
    document.getElementById(tabName).classList.add('active');
}

function updateAuthStatus() {
    const statusElement = document.getElementById('authStatus');
    const userElement = document.getElementById('currentUser');
    const tokenElement = document.getElementById('tokenDisplay');

    if (authToken && currentUserData) {
        statusElement.textContent = 'Authenticated';
        statusElement.style.color = '#48bb78';
        userElement.textContent = currentUserData.username || currentUserData.email;
        tokenElement.textContent = authToken.substring(0, 30) + '...';
    } else {
        statusElement.textContent = 'Not Authenticated';
        statusElement.style.color = '#f56565';
        userElement.textContent = 'None';
        tokenElement.textContent = 'No token';
    }
}

function displayResponse(elementId, data, isError = false) {
    const element = document.getElementById(elementId);
    element.style.display = 'block';
    element.className = 'response-box ' + (isError ? 'error' : 'success');
    element.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
}

function getAuthHeaders() {
    return {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authToken}`
    };
}

async function register() {
    const email = document.getElementById('registerEmail').value;
    const username = document.getElementById('registerUsername').value;
    const password = document.getElementById('registerPassword').value;
    const dateOfBirth = document.getElementById('registerDOB').value;

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
        displayResponse('registerResponse', data, !response.ok);
    } catch (error) {
        displayResponse('registerResponse', { error: error.message }, true);
    }
}

async function login() {
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;

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
            updateAuthStatus();
        }

        displayResponse('loginResponse', data, !response.ok);
    } catch (error) {
        displayResponse('loginResponse', { error: error.message }, true);
    }
}

async function logout() {
    try {
        const response = await fetch(`${API_BASE_URL}/auth/logout`, {
            method: 'POST',
            headers: getAuthHeaders()
        });

        const data = await response.json();

        if (response.ok) {
            authToken = null;
            currentUserData = null;
            localStorage.removeItem('authToken');
            localStorage.removeItem('currentUser');
            updateAuthStatus();
        }

        displayResponse('logoutResponse', data, !response.ok);
    } catch (error) {
        displayResponse('logoutResponse', { error: error.message }, true);
    }
}

async function searchUsers() {
    const username = document.getElementById('searchUsername').value;

    try {
        const response = await fetch(`${API_BASE_URL}/users/search?username=${encodeURIComponent(username)}`, {
            headers: getAuthHeaders()
        });

        const data = await response.json();
        displayResponse('searchUsersResponse', data, !response.ok);
    } catch (error) {
        displayResponse('searchUsersResponse', { error: error.message }, true);
    }
}

async function getUserProfile() {
    const userId = document.getElementById('profileUserId').value;

    try {
        const response = await fetch(`${API_BASE_URL}/users/profile/${userId}`, {
            headers: getAuthHeaders()
        });

        const data = await response.json();
        displayResponse('profileResponse', data, !response.ok);
    } catch (error) {
        displayResponse('profileResponse', { error: error.message }, true);
    }
}

async function updateBio() {
    const newBio = document.getElementById('updateBio').value;

    try {
        const response = await fetch(`${API_BASE_URL}/users/update/bio`, {
            method: 'PUT',
            headers: getAuthHeaders(),
            body: JSON.stringify({ new_bio: newBio })
        });

        const data = await response.json();
        displayResponse('updateBioResponse', data, !response.ok);
    } catch (error) {
        displayResponse('updateBioResponse', { error: error.message }, true);
    }
}

async function updateProfilePicture() {
    const profilePicture = document.getElementById('updateProfilePicture').value;

    try {
        const response = await fetch(`${API_BASE_URL}/users/update/profile-picture`, {
            method: 'PUT',
            headers: getAuthHeaders(),
            body: JSON.stringify({ profile_picture: profilePicture })
        });

        const data = await response.json();
        displayResponse('updatePictureResponse', data, !response.ok);
    } catch (error) {
        displayResponse('updatePictureResponse', { error: error.message }, true);
    }
}

async function followUnfollow() {
    const targetUserId = document.getElementById('followUserId').value;

    try {
        const response = await fetch(`${API_BASE_URL}/users/follow-unfollow/?target_user_id=${targetUserId}`, {
            method: 'POST',
            headers: getAuthHeaders()
        });

        const data = await response.json();
        displayResponse('followResponse', data, !response.ok);
    } catch (error) {
        displayResponse('followResponse', { error: error.message }, true);
    }
}

async function getFollowers() {
    const userId = document.getElementById('followersUserId').value;

    try {
        const response = await fetch(`${API_BASE_URL}/users/followers?user_id=${userId}`, {
            headers: getAuthHeaders()
        });

        const data = await response.json();
        displayResponse('followersResponse', data, !response.ok);
    } catch (error) {
        displayResponse('followersResponse', { error: error.message }, true);
    }
}

async function getFollowing() {
    const userId = document.getElementById('followingUserId').value;

    try {
        const response = await fetch(`${API_BASE_URL}/users/followings?user_id=${userId}`, {
            headers: getAuthHeaders()
        });

        const data = await response.json();
        displayResponse('followingResponse', data, !response.ok);
    } catch (error) {
        displayResponse('followingResponse', { error: error.message }, true);
    }
}

async function createPost() {
    const content = document.getElementById('postContent').value;
    const mediaUrl = document.getElementById('postMediaUrl').value;

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

        const data = await response.json();
        displayResponse('createPostResponse', data, !response.ok);
    } catch (error) {
        displayResponse('createPostResponse', { error: error.message }, true);
    }
}

async function getUserPosts() {
    const userId = document.getElementById('postsUserId').value;

    try {
        const response = await fetch(`${API_BASE_URL}/posts/${userId}`, {
            headers: getAuthHeaders()
        });

        const data = await response.json();
        displayResponse('userPostsResponse', data, !response.ok);
    } catch (error) {
        displayResponse('userPostsResponse', { error: error.message }, true);
    }
}

async function updatePost() {
    const postId = document.getElementById('updatePostId').value;
    const newContent = document.getElementById('updatePostContent').value;

    try {
        const response = await fetch(`${API_BASE_URL}/posts/update/${postId}`, {
            method: 'PUT',
            headers: getAuthHeaders(),
            body: JSON.stringify({ new_content: newContent })
        });

        const data = await response.json();
        displayResponse('updatePostResponse', data, !response.ok);
    } catch (error) {
        displayResponse('updatePostResponse', { error: error.message }, true);
    }
}

async function deletePost() {
    const postId = document.getElementById('deletePostId').value;

    try {
        const response = await fetch(`${API_BASE_URL}/posts/delete/${postId}`, {
            method: 'DELETE',
            headers: getAuthHeaders()
        });

        if (response.status === 204) {
            displayResponse('deletePostResponse', { success: true, message: 'Post deleted successfully' }, false);
        } else {
            const data = await response.json();
            displayResponse('deletePostResponse', data, !response.ok);
        }
    } catch (error) {
        displayResponse('deletePostResponse', { error: error.message }, true);
    }
}

async function likeUnlikePost() {
    const postId = document.getElementById('likePostId').value;

    try {
        const response = await fetch(`${API_BASE_URL}/posts/like-deslike/${postId}`, {
            method: 'POST',
            headers: getAuthHeaders()
        });

        const data = await response.json();
        displayResponse('likePostResponse', data, !response.ok);
    } catch (error) {
        displayResponse('likePostResponse', { error: error.message }, true);
    }
}

async function createComment() {
    const postId = document.getElementById('commentPostId').value;
    const content = document.getElementById('commentContent').value;

    try {
        const response = await fetch(`${API_BASE_URL}/posts/comments/create?post_id=${postId}`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify({ content })
        });

        const data = await response.json();
        displayResponse('createCommentResponse', data, !response.ok);
    } catch (error) {
        displayResponse('createCommentResponse', { error: error.message }, true);
    }
}

async function getComments() {
    const postId = document.getElementById('getCommentsPostId').value;

    try {
        const response = await fetch(`${API_BASE_URL}/posts/comments/all?post_id=${postId}`, {
            headers: getAuthHeaders()
        });

        const data = await response.json();
        displayResponse('getCommentsResponse', data, !response.ok);
    } catch (error) {
        displayResponse('getCommentsResponse', { error: error.message }, true);
    }
}

async function deleteComment() {
    const commentId = document.getElementById('deleteCommentId').value;
    const postId = document.getElementById('deleteCommentPostId').value;

    try {
        const response = await fetch(`${API_BASE_URL}/posts/comments/delete?comment_id=${commentId}&post_id=${postId}`, {
            method: 'DELETE',
            headers: getAuthHeaders()
        });

        if (response.status === 204) {
            displayResponse('deleteCommentResponse', { success: true, message: 'Comment deleted successfully' }, false);
        } else {
            const data = await response.json();
            displayResponse('deleteCommentResponse', data, !response.ok);
        }
    } catch (error) {
        displayResponse('deleteCommentResponse', { error: error.message }, true);
    }
}

async function likeUnlikeComment() {
    const commentId = document.getElementById('likeCommentId').value;

    try {
        const response = await fetch(`${API_BASE_URL}/posts/comments/like-deslike/${commentId}`, {
            method: 'POST',
            headers: getAuthHeaders()
        });

        const data = await response.json();
        displayResponse('likeCommentResponse', data, !response.ok);
    } catch (error) {
        displayResponse('likeCommentResponse', { error: error.message }, true);
    }
}

async function getUserFeed() {
    try {
        const response = await fetch(`${API_BASE_URL}/feed/`, {
            headers: getAuthHeaders()
        });

        const data = await response.json();
        displayResponse('userFeedResponse', data, !response.ok);
    } catch (error) {
        displayResponse('userFeedResponse', { error: error.message }, true);
    }
}

async function getExploreFeed() {
    try {
        const response = await fetch(`${API_BASE_URL}/feed/explore`, {
            headers: getAuthHeaders()
        });

        const data = await response.json();
        displayResponse('exploreFeedResponse', data, !response.ok);
    } catch (error) {
        displayResponse('exploreFeedResponse', { error: error.message }, true);
    }
}