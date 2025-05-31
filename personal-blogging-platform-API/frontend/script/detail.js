const titleEl = document.getElementById('post-title');
const contentEl = document.getElementById('post-content');
const authorEl = document.getElementById('post-author');
const dateEl = document.getElementById('post-date');
const deleteBtn = document.getElementById('delete-btn');
const editBtn = document.getElementById('edit-btn');

// 1. Token check and redirect if missing
const token = localStorage.getItem('access');
if (!token) window.location.href = 'login.html';

// 2. Extract slug from URL query string
const params = new URLSearchParams(window.location.search);
const slug = params.get('slug');
if (!slug) {
  contentEl.innerHTML = '<p>Error: No post specified.</p>';
  throw new Error('No post slug in URL');
}

// 3. Decode JWT to get current username
const payload = JSON.parse(atob(token.split('.')[1]));
const currentUser = payload.username;

// 4. Fetch post data by slug
fetch(`http://127.0.0.1:8000/api/posts/${slug}/`, {
  headers: { Authorization: `Bearer ${token}` },
})
  .then((res) => {
    if (!res.ok) throw new Error('Failed to fetch post');
    return res.json();
  })
  .then((post) => {
    // 5. Render post details
    titleEl.textContent = post.title;
    contentEl.innerHTML = post.html_content;
    
    // Normalize author display (string or object)
    const postAuthor = typeof post.author === 'string' ? post.author : post.author.username;
    authorEl.textContent = postAuthor;
    dateEl.textContent = new Date(post.created_at).toLocaleString();

    // 6. Show edit/delete buttons if current user is the author
    if (postAuthor === currentUser) {
      editBtn.style.display = 'inline-block';
      deleteBtn.style.display = 'inline-block';

      // Delete post on button click
      deleteBtn.addEventListener('click', () => {
        if (!confirm('Are you sure you want to delete this post?')) return;

        fetch(`http://127.0.0.1:8000/api/posts/${slug}/`, {
          method: 'DELETE',
          headers: { Authorization: `Bearer ${token}` },
        })
          .then((res) => {
            if (!res.ok) throw new Error('Failed to delete post');
            window.location.href = 'index.html';
          })
          .catch((err) => alert(err.message));
      });

      // TODO: Add edit logic here later
    }
  })
  .catch((err) => {
    contentEl.innerHTML = `<p>Error: ${err.message}</p>`;
  });
