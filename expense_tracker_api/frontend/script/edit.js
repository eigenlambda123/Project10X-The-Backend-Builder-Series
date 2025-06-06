const token = localStorage.getItem("access"); // get JWT token from localStorage
// if token is not present, redirect to login page
if (!token) {
  window.location.href = "login.html";
}


const id = new URLSearchParams(window.location.search).get("id"); // get transaction ID from URL parameters
const API_BASE = "http://127.0.0.1:8000/api/"; // base URL for API requests

// DOM elements
const descriptionInput = document.getElementById("description");
const amountInput = document.getElementById("amount");
const typeSelect = document.getElementById("type");
const categorySelect = document.getElementById("category");
const dateInput = document.getElementById("date");
const error = document.getElementById("error");
const form = document.getElementById("edit-transaction-form");



async function fetchTransaction() { // Fetch transaction details by ID
  try {
    const res = await fetch(`${API_BASE}transactions/${id}/`, { // Use the transaction ID from URL
      headers: { Authorization: `Bearer ${token}` }, // Include JWT token in headers
    });

    if (!res.ok) throw new Error("Failed to fetch transaction"); // Check if the response is OK

    const data = await res.json(); // Parse the JSON response

    descriptionInput.value = data.title; // Use 'title' field for description
    amountInput.value = data.amount; // Use 'amount' field for amount
    typeSelect.value = data.type; // Use 'type' field for transaction type
    dateInput.value = data.date; // Use 'date' field for date
    await fetchCategories(data.category); // Fetch categories and set the selected one

    } catch (err) { // Handle errors during fetch
    error.textContent = err.message; // Display error message
  }
}


async function fetchCategories(currentCategoryId) { // Fetch categories from the API and populate the category dropdown
  try { 
    const res = await fetch(`${API_BASE}categories/`, { // Fetch categories from the API
      headers: { Authorization: `Bearer ${token}` }, // Include JWT token in headers
    });

    const categories = await res.json(); // Parse the JSON response
    categorySelect.innerHTML = ""; // Clear existing options in the category select element

    categories.forEach((cat) => { // Loop through each category and create an option element
      const opt = document.createElement("option"); // Create a new option element
      opt.value = cat.id; // Set the value of the option to the category ID
      opt.textContent = cat.name; // Set the text content of the option to the category name
      if (cat.id === currentCategoryId) opt.selected = true; // If this category matches the current transaction's category, mark it as selected
      categorySelect.appendChild(opt); // Append the option to the category select element
    });
  } catch (err) { // Handle errors during fetch
    error.textContent = "Could not load categories."; // Display error message
    }
}


form.addEventListener("submit", async (e) => { // Handle form submission to update the transaction
  e.preventDefault(); // Prevent the default form submission behavior

  const updatedData = { // Create an object with the updated transaction data
    title: descriptionInput.value,
    amount: parseFloat(amountInput.value),
    type: typeSelect.value,
    category: parseInt(categorySelect.value),
    date: dateInput.value,
  };

  try { // Send a PUT request to update the transaction
    const res = await fetch(`${API_BASE}transactions/${id}/`, { // Use the transaction ID from URL
      method: "PUT", // Specify the HTTP method as PUT
      headers: {
        "Content-Type": "application/json", // Set the content type to JSON
        Authorization: `Bearer ${token}`, // Include JWT token in headers
      },
      body: JSON.stringify(updatedData), // Convert the updated data to a JSON string
    });

    // Check if the response is OK
    if (!res.ok) {
      const errorData = await res.json(); // Parse the error response
      throw new Error(JSON.stringify(errorData)); // Throw an error with the error data
    }

    window.location.href = "index.html"; // Redirect to the index on successful update
  } catch (err) { // Handle errors during the update request
    error.textContent = "Failed to update: " + err.message; // Display error message
  }
});

fetchTransaction(); // Fetch the transaction details when the page loads