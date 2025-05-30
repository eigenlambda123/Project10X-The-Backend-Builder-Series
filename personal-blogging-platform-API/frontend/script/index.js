// Get DOM elements
const postList = document.getElementById('post-list'); // Get the post list element where posts will be displayed
const logoutBtn = document.getElementById('logout'); // Get the logout button element

// Handle logout button click
logoutBtn.addEventListener('click', async () => {
    localStorage.clear(); // Remove all local storage data
    window.location.href = 'login.html'; // Redirect to login page
});

// Retrieve access token from local storage
const token = localStorage.getItem('access');

// Redirect to login if token is missing
if (!token) {
    window.location.href = 'login.html';
} else {
    // Fetch posts from API with Authorization header
    fetch('http://127.0.0.1:8000/api/posts/', {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    })
    .then((res) => {
        // Throw error if response is not successful
        if (!res.ok) throw new Error('Failed to fetch posts');
        return res.json();
    })
    .then((data) => {
        // Use data.results because API returns { results: [...] }
        (data.results || []).forEach((post) => {
            const li = document.createElement('li'); // Create a list item for each post
            const link = document.createElement('a'); // Create a link for the post
            link.href = `post.html?id=${post.id}`; // Set the link to the post details page
            link.textContent = post.title; // Set the link text to the post title
            li.appendChild(link); // Append the link to the list item
            postList.appendChild(li); // Append the list item to the post list
        });
    })
    .catch((err) => {
        // Display error message in the post list
        postList.innerHTML = `<li>Error: ${err.message}</li>`;
    });
}