document.getElementById('register-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const username = document.getElementById('username').value.trim(); // get username input
    const email = document.getElementById('email').value.trim(); // get email input
    const password = document.getElementById('password').value; // get password input
    const confirmPassword = document.getElementById('confirm-password').value; // get confirm password input

    const errorElem = document.getElementById('error');
    errorElem.textContent = ''; // clear previous error message

    // check if password and confirm password match
    if (password !== confirmPassword) {
        errorElem.textContent = 'Passwords do not match.';
        return;
    }

    try {
        // send POST request to the Django backend for user registration
        const response = await fetch('http://127.0.0.1:8000/api/register/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, email, password }), // send username, email, and password as JSON
    });

    const data = await response.json(); // parse the JSON response

    if (response.ok) {
      // Registration successful, redirect to login page
      window.location.href = 'login.html';
    } else {
      // Show error message from backend or generic
      errorElem.textContent = data.detail || JSON.stringify(data);
    }  
    } catch (err) {
        // Handle network errors
        errorElem.textContent = 'Network error. Please try again.';
    }
});
  