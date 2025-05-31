const form = document.getElementById('create-form'); // Get the form element
const errorMsg = document.getElementById('error-msg'); // Get the error message element
const token = localStorage.getItem('access'); // Get JWT access token from local storage
if (!token) {
  window.location.href = 'login.html'; // Redirect to login if not authenticated
}

form.addEventListener('submit', async (e) => { // Listen for form submission
  e.preventDefault(); // Prevent default form submission

  const formData = new FormData(form); // Get form data
  const payload = {
    title: formData.get('title'), // Get title from form
    content: formData.get('content'), // Get content from form
    category: formData.get('category'), // Get category from form
    tags: formData.get('tags').split(',').map(tag => tag.trim()).filter(Boolean), // Split tags by comma, trim, and remove empty
  };

  try {
    const res = await fetch('http://127.0.0.1:8000/api/posts/', { // Send POST request to API
      method: 'POST',
      headers: {
        'Content-Type': 'application/json', // Set content type to JSON
        Authorization: `Bearer ${token}`, // Add JWT token to Authorization header
      },
      body: JSON.stringify(payload), // Convert payload to JSON string
    });

    if (!res.ok) {
      const data = await res.json(); // Parse error response
      throw new Error(JSON.stringify(data)); // Throw error with details
    }

    window.location.href = 'index.html'; // Redirect to index page on success
  } catch (err) {
    errorMsg.textContent = `Error: ${err.message}`; // Display error message
  }
});
