const form = document.getElementById('login-form'); // Get the form element
const errorDisplay = document.getElementById('error'); // Get the error display element

form.addEventListener('submit', async (e) => {
    e.preventDefault(); // Prevent the default form submission
    errorDisplay.textContent = ''; // Clear any previous error messages

    const username = document.getElementById('username').value; // Get the username from the form
    const password = document.getElementById('password').value; // Get the password from the form

    try {
        // Send a POST request to the API endpoint
        const response = await fetch('http://127.0.0.1:8000/api/login/', { 
            method: 'POST',
            headers: {
                'Content-Type': 'application/json', // Set the content type to JSON
            },
            body: JSON.stringify({ username, password }), // Send the username and password as JSON
        });

        if (!response.ok) { // Check if the response is not OK
            const errorData = await response.json(); // Parse the error response
            throw new Error(errorData.detail || 'Login failed'); // Throw an error with the message from the response
        }

        const data = await response.json(); // Parse the JSON response
        localStorage.setItem('access', data.access); // Store the access token in local storage
        localStorage.setItem('refresh', data.refresh); // Store the refresh token in local storage
        window.location.href = 'index.html'; // Redirect to the index page on successful login
    } catch (error) {
        errorDisplay.textContent = error.message || 'Login failed'; // Display the error message in the error display element
    }
});

