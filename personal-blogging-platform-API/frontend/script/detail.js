const titleEl = document.getElementById('post-title'); // Get the title element
const contentEl = document.getElementById('post-content'); // Get the content element
const authorEl = document.getElementById('post-author'); // Get the author element
const dateEl = document.getElementById('post-date'); // Get the date element
const deleteBtn = document.getElementById('delete-btn'); // Get the delete button
const editBtn = document.getElementById('edit-btn'); // Get the edit button

// 1. Token check and redirect if missing
const token = localStorage.getItem('access'); // Get JWT access token from local storage
if (!token) window.location.href = 'login.html'; // Redirect to login if not authenticated

// 2. Extract slug from URL query string
const params = new URLSearchParams(window.location.search); // Parse the query string from the URL
const slug = params.get('slug'); // Get the 'slug' parameter from the query string
if (!slug) { // If no slug is found in the URL
  contentEl.innerHTML = '<p>Error: No post specified.</p>'; // Show error message in content area
  throw new Error('No post slug in URL'); // Stop script execution with error
}

// 3. Decode JWT to get current username
const payload = JSON.parse(atob(token.split('.')[1])); // Decode the JWT payload to get user info
const currentUser = payload.username; // Extract the username from the payload

// 4. Fetch post data by slug
fetch(`http://127.0.0.1:8000/api/posts/${slug}/`, { // Make GET request to fetch post details by slug
  headers: { Authorization: `Bearer ${token}` }, // Add Authorization header with JWT token
})
  .then((res) => { // When response is received
    if (!res.ok) throw new Error('Failed to fetch post'); // If response is not OK, throw error
    return res.json(); // Otherwise, parse response as JSON
  })
  .then((post) => { // When post data is available
    // 5. Render post details
    titleEl.textContent = post.title; // Set the post title
    contentEl.innerHTML = post.html_content; // Set the post content (HTML)
    authorEl.textContent = post.author; // Set the author (may be username or ID)
    dateEl.textContent = new Date(post.created_at).toLocaleString(); // Format and set the creation date

    // 6. Show edit/delete buttons if current user is the author
    if (post.author === currentUser) { // If the current user is the author
      editBtn.style.display = 'inline-block'; // Show the edit button
      deleteBtn.style.display = 'inline-block'; // Show the delete button

      // Delete post on button click
      deleteBtn.addEventListener('click', () => { // When delete button is clicked
        if (!confirm('Are you sure you want to delete this post?')) return; // Confirm deletion

        fetch(`http://127.0.0.1:8000/api/posts/${slug}/`, { // Send DELETE request to API
          method: 'DELETE', // HTTP DELETE method
          headers: { Authorization: `Bearer ${token}` }, // Add Authorization header
        })
          .then((res) => { // When response is received
            if (!res.ok) throw new Error('Failed to delete post'); // If not OK, throw error
            window.location.href = 'index.html'; // Redirect to index page on success
          })
          .catch((err) => alert(err.message)); // Show error alert if deletion fails
      });

      // TODO: Add edit logic here later
    }
  })
  .catch((err) => { // If any error occurs during fetch or rendering
    contentEl.innerHTML = `<p>Error: ${err.message}</p>`; // Show error message in content area
  });