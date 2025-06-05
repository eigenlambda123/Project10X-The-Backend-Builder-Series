// Base URL for API endpoints
const apiBaseUrl = 'http://127.0.0.1:8000/api'; // adjust if needed

// Helper function to get authorization headers with JWT token from localStorage
function authHeaders() {
  const token = localStorage.getItem('access');
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`,
  };
}

// DOM element references for updating UI
const balanceEl = document.getElementById('balance');
const incomeEl = document.getElementById('total-income');
const expensesEl = document.getElementById('total-expenses');
const transactionsBody = document.getElementById('transactions-body');
const errorEl = document.getElementById('error');

const prevBtn = document.getElementById('prev-page-btn');
const nextBtn = document.getElementById('next-page-btn');

const createForm = document.getElementById('create-transaction-form');
const logoutBtn = document.getElementById('logout-btn');

const categorySelect = document.getElementById('category'); // Dropdown for categories

// Track the current transactions API URL (for pagination)
let currentTransactionsUrl = `${apiBaseUrl}/transactions/`;

// Fetch and render the summary (balance, income, expenses)
async function fetchSummary() {
  try {
    const res = await fetch(`${apiBaseUrl}/transactions/summary/`, {
      headers: authHeaders(),
    });
    if (!res.ok) throw new Error('Failed to fetch summary');
    const data = await res.json();

    // Update UI with summary values, defaulting to 0 if missing
    balanceEl.textContent = (data.net_balance || 0).toFixed(2);
    incomeEl.textContent = (data.total_income || 0).toFixed(2);
    expensesEl.textContent = (data.total_expenses || 0).toFixed(2);
  } catch (err) {
    showError(err.message);
  }
}

// Fetch and render the list of transactions (paginated)
async function fetchTransactions(url = currentTransactionsUrl) {
  try {
    const res = await fetch(url, { headers: authHeaders() });
    if (!res.ok) {
      if (res.status === 401) {
        redirectToLogin();
        return;
      }
      throw new Error('Failed to fetch transactions');
    }
    const data = await res.json();
    currentTransactionsUrl = url;

    // Render transactions (handle both array and paginated object)
    renderTransactions(Array.isArray(data) ? data : data.results);
    // Disable pagination buttons (API does not support it)
    updatePaginationButtons(null, null);
  } catch (err) {
    showError(err.message);
  }
}

// Render the transactions table in the UI
function renderTransactions(transactions) {
  transactionsBody.innerHTML = '';
  if (!Array.isArray(transactions) || transactions.length === 0) {
    showError('No transactions found.');
    return;
  }
  transactions.forEach(tx => {
    let amount = 0;
    // Parse and validate amount
    if (tx.amount !== undefined && tx.amount !== null) {
      const parsedAmount = typeof tx.amount === 'string' ? 
        parseFloat(tx.amount) : 
        Number(tx.amount);
      amount = isNaN(parsedAmount) ? 0 : parsedAmount;
    }
    
    // Create table row for each transaction
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${tx.title || tx.description || 'N/A'}</td>
      <td>${amount.toFixed(2)}</td>
      <td>${tx.category || 'N/A'}</td>
      <td>${tx.created_at ? new Date(tx.created_at).toLocaleDateString() : ''}</td>
      <td>${tx.type || 'N/A'}</td>
      <td>
        <button class="edit-btn" data-id="${tx.id}">Edit</button>
        <button class="delete-btn" data-id="${tx.id}">Delete</button>
      </td>
    `;
    transactionsBody.appendChild(tr);
  });

  // Attach event listeners to edit and delete buttons
  attachTransactionButtonsListeners();
}

// Enable or disable pagination buttons (currently always disabled)
function updatePaginationButtons(prevUrl, nextUrl) {
  prevBtn.disabled = !prevUrl;
  nextBtn.disabled = !nextUrl;

  prevBtn.onclick = () => { if (prevUrl) fetchTransactions(prevUrl); };
  nextBtn.onclick = () => { if (nextUrl) fetchTransactions(nextUrl); };
}

// Attach click handlers for edit and delete buttons in the transaction list
function attachTransactionButtonsListeners() {
  // Edit button: redirect to edit page with transaction ID
  document.querySelectorAll('.edit-btn').forEach(btn => {
    btn.onclick = (e) => {
      const txId = e.target.dataset.id;
      window.location.href = `edit.html?id=${txId}`;
    };
  });

  // Delete button: send DELETE request, refresh list and summary on success
  document.querySelectorAll('.delete-btn').forEach(btn => {
    btn.onclick = async (e) => {
      const txId = e.target.dataset.id;
      if (confirm('Are you sure you want to delete this transaction?')) {
        try {
          const res = await fetch(`${apiBaseUrl}/transactions/${txId}/`, {
            method: 'DELETE',
            headers: authHeaders(),
          });
          if (!res.ok) throw new Error('Failed to delete transaction');
          fetchTransactions(); // refresh list after deletion
          fetchSummary();      // refresh summary
        } catch (err) {
          showError(err.message);
        }
      }
    };
  });
}

// Handle transaction creation form submission
createForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  clearError();

  // Gather form data and build transaction object
  const formData = new FormData(createForm);
  const newTransaction = {
    title: formData.get('description').trim(), // <-- use 'title' key
    amount: parseFloat(formData.get('amount')),
    category: parseInt(formData.get('category'), 10),
    date: formData.get('date'),
    type: formData.get('type'),
  };

  // Basic validation for required fields
  if (!newTransaction.title || isNaN(newTransaction.amount) || !newTransaction.category || !newTransaction.date || !newTransaction.type) {
    showError('Please fill all fields correctly.');
    return;
  }

  try {
    // Send POST request to create transaction
    const res = await fetch(`${apiBaseUrl}/transactions/`, {
      method: 'POST',
      headers: authHeaders(),
      body: JSON.stringify(newTransaction),
    });
    if (!res.ok) {
      const errData = await res.json();
      console.error('Transaction creation error:', errData); // <-- Add this line
      // Show all field errors if present
      let msg = errData.detail || 'Failed to create transaction';
      if (typeof errData === 'object') {
        msg = Object.entries(errData)
          .map(([k, v]) => `${k}: ${Array.isArray(v) ? v.join(', ') : v}`)
          .join(' | ');
      }
      throw new Error(msg);
    }
    createForm.reset();
    fetchTransactions();  // refresh list to include new
    fetchSummary();       // refresh summary
  } catch (err) {
    showError(err.message);
  }
});

// Handle logout: remove tokens and redirect to login page
logoutBtn.addEventListener('click', () => {
  localStorage.removeItem('access');
  localStorage.removeItem('refresh');
  window.location.href = 'login.html';
});

// Show error message in the UI
function showError(msg) {
  errorEl.textContent = msg;
  errorEl.style.display = 'block';
}

// Clear error message from the UI
function clearError() {
  errorEl.textContent = '';
  errorEl.style.display = 'none';
}

// Redirect to login page and clear tokens (for unauthorized access)
function redirectToLogin() {
  localStorage.removeItem('access');
  localStorage.removeItem('refresh');
  window.location.href = 'login.html';
}

// Fetch categories from API and populate the category dropdown
async function populateCategoryDropdown() {
  try {
    const res = await fetch('http://127.0.0.1:8000/api/categories/', {
      headers: authHeaders(),
    });
    if (!res.ok) throw new Error('Failed to fetch categories');
    const categories = await res.json();

    // Clear existing options and add a default option
    categorySelect.innerHTML = '<option value="">Select Category</option>';

    // Add each category as an option in the dropdown
    categories.forEach(cat => {
      const option = document.createElement('option');
      option.value = cat.id;
      option.textContent = cat.name || cat.title || `Category ${cat.id}`;
      categorySelect.appendChild(option);
    });
  } catch (err) {
    showError(err.message);
  }
}

// Initialize dashboard: fetch summary, transactions, and categories on page load
document.addEventListener('DOMContentLoaded', () => {
  fetchSummary();
  fetchTransactions();
  populateCategoryDropdown();
});