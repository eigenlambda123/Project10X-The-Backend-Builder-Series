const token = localStorage.getItem('access');
if (!token) window.location.href = 'login.html';

const params = new URLSearchParams(window.location.search);
const slug = params.get('slug');
if (!slug) throw new Error('Missing slug in URL');

const titleInput = document.getElementById('title');
const contentInput = document.getElementById('content');
const form = document.getElementById('edit-form');

// Fetch post data to prefill
fetch(`http://127.0.0.1:8000/api/posts/${slug}/`, {
  headers: {
    Authorization: `Bearer ${token}`,
  },
})
  .then((res) => {
    if (!res.ok) throw new Error('Failed to fetch post');
    return res.json();
  })
  .then((post) => {
    titleInput.value = post.title;
    contentInput.value = post.content; // raw markdown
  })
  .catch((err) => alert(err.message));

// Handle form submission
form.addEventListener('submit', (e) => {
  e.preventDefault();

  const updatedPost = {
    title: titleInput.value,
    content: contentInput.value,
  };

  fetch(`http://127.0.0.1:8000/api/posts/${slug}/`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(updatedPost),
  })
    .then((res) => {
      if (!res.ok) throw new Error('Failed to update post');
      return res.json();
    })
    .then(() => {
      window.location.href = `detail.html?slug=${slug}`;
    })
    .catch((err) => alert(err.message));
});
