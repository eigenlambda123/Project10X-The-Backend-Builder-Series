const form = document.getElementById('register-form'); // Get the form element
const errorDisplay = document.getElementById('error'); // Get the error display element

form.addEventListener('submit', async (e) => {
    e.preventDefault(); // Prevent the default form submission
    
    const username = document.getElementById('username').value; // Get the username input value
    const email = document.getElementById('email').value; // Get the email input value
    const password = document.getElementById('password').value; // Get the password input value
    const confirmPassword = document.getElementById('confirm-password').value; // Get the confirm password input value

    if (password !== confirmPassword) { // Check if passwords match
        errorDisplay.textContent = 'Passwords do not match'; // Display error if passwords do not match
        return; 
    }

    try {
        const response = await fetch('http://localhost:8000/api/register/', { 
            method: 'POST', // Set the request method to POST
            headers: {
                'Content-Type': 'application/json' // Set the content type to JSON
            },
            body: JSON.stringify({ username, email, password }) // Convert the form data to JSON
        });

        if (!response.ok) { // Check if the response is not OK
            const errorData = await response.json(); // Parse the error response
            errorDisplay.textContent = errorData.detail || 'Registration failed'; // Display the error message
            return;
        }

        window.location.href = 'login.html'; // Redirect to login page on successful registration
    } catch (error) {
        console.error('Error:', error); // Log any errors to the console
        errorDisplay.textContent = 'An error occurred. Please try again.'; // Display a generic error message
    }
}); 