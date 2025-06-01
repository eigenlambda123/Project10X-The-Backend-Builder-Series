const token = localStorage.getItem('access'); // Get JWT token from localStorage
if (!token) window.location.href = 'login.html'; // Redirect to login if token is missing

const params = new URLSearchParams(window.location.search); // Parse URL query parameters
const slug = params.get('slug'); // Get the 'slug' parameter from URL
if (!slug) throw new Error('Missing slug in URL'); // Throw error if slug is missing

const titleInput = document.getElementById('title'); // Get title input element
const contentInput = document.getElementById('content'); // Get content input element
const form = document.getElementById('edit-form'); // Get the edit form element


// Fetch post data to prefill
fetch(`http://127.0.0.1:8000/api/posts/${slug}/`, { // Fetch the post by slug
  headers: {
    Authorization: `Bearer ${token}`, // Add JWT token to Authorization header
  },
})
  .then((res) => {
    if (!res.ok) throw new Error('Failed to fetch post'); // Throw error if fetch fails
    return res.json(); // Parse response as JSON
  })
  .then((post) => {
    titleInput.value = post.title; // Prefill title input with post title
    contentInput.value = post.content; // Prefill content input with post content (markdown)
  })
  .catch((err) => alert(err.message)); // Alert error if fetch fails

// Handle form submission
form.addEventListener('submit', (e) => { // Listen for form submit event
  e.preventDefault(); // Prevent default form submission

  const updatedPost = {
    title: titleInput.value, // Get updated title from input
    content: contentInput.value, // Get updated content from input
  };


  fetch(`http://127.0.0.1:8000/api/posts/${slug}/`, { // Send PATCH request to update post
    method: 'PATCH', // Use PATCH method for partial update
    headers: {
      'Content-Type': 'application/json', // Set content type to JSON
      Authorization: `Bearer ${token}`, // Add JWT token to Authorization header
    },
    body: JSON.stringify(updatedPost), // Send updated post data as JSON
  })
    .then((res) => {
      if (!res.ok) throw new Error('Failed to update post'); // Throw error if update fails
      return res.json(); // Parse response as JSON
    })
    .then(() => {
      window.location.href = `detail.html?slug=${slug}`; // Redirect to post detail page after update
    })
    .catch((err) => alert(err.message)); // Alert error if update fails
});
