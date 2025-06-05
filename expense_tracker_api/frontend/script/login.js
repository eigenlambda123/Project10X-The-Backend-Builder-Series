document.getElementById('login-form').addEventListener('submit', async function (e) {
    e.preventDefault();

    const username = document.getElementById('username').value.trim(); // get username input
    const password = document.getElementById('password').value; // get password input

    // send POST request to the Django backend for token authentication
    const response = await fetch('http://127.0.0.1:8000/api/token/', { 
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password }) // send username and password as JSON
    });

    const data = await response.json(); // parse the JSON response

    if (response.ok) {
        localStorage.setItem('access', data.access);   // JWT access token
        localStorage.setItem('refresh', data.refresh); // JWT refresh token
        window.location.href = 'index.html'; // redirect relative to current frontend folder
    } else {
        document.getElementById('error').textContent = data.detail || 'Login failed.';
    }
});
