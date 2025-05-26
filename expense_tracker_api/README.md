## API Endpoints

### Admin
- `GET /admin/`  
  Access Django admin interface.

---

### Authentication & User Management

- `POST /api/register/`  
  Register a new user.

- `POST /api/token/`  
  Obtain JWT access and refresh tokens by submitting user credentials.

- `POST /api/token/refresh/`  
  Refresh JWT access token using a valid refresh token.

---

### Categories (`/api/categories/`)

- `GET /api/categories/`  
  List all categories of the authenticated user.

- `POST /api/categories/`  
  Create a new category.

- `GET /api/categories/{slug}/`  
  Retrieve a category by slug.

- `PUT /api/categories/{slug}/`  
  Update a category by slug.

- `PATCH /api/categories/{slug}/`  
  Partially update a category by slug.

- `DELETE /api/categories/{slug}/`  
  Delete a category by slug.

---

### Transactions (`/api/transactions/`)

- `GET /api/transactions/`  
  List all transactions of the authenticated user (supports filtering).

- `POST /api/transactions/`  
  Create a new transaction.

- `GET /api/transactions/{id}/`  
  Retrieve a transaction by ID.

- `PUT /api/transactions/{id}/`  
  Update a transaction by ID.

- `PATCH /api/transactions/{id}/`  
  Partially update a transaction by ID.

- `DELETE /api/transactions/{id}/`  
  Delete a transaction by ID.

---

### Custom Transactions Actions

- `GET /api/transactions/summary/`  
  Get total income, total expenses, and net balance summary.  
  - Optional query parameter: `month=YYYY-MM` to filter by month.

- `GET /api/transactions/expense-category-summary/`  
  Get aggregated expenses grouped by category.

- `GET /api/transactions/income-category-summary/`  
  Get aggregated income grouped by category.

- `GET /api/transactions/export-csv/`  
  Export all transactions as a downloadable CSV file.


Link: https://project10x-the-backend-builder-series-1.onrender.com/api/