# API Endpoints for Project10X Backend — 1st Project (Blog API)

## Base URL Prefix  
All API endpoints are prefixed with `/api/`.

---

## Authentication

- `POST /api/login/`  
  Obtain JWT access and refresh tokens by providing username and password.

- `POST /api/token/refresh/`  
  Refresh JWT access token using a valid refresh token.

---

## User Registration

- `POST /api/register/`  
  Register a new user account.

---

## Posts

- `GET /api/posts/`  
  List all posts (supports filtering).

- `POST /api/posts/`  
  Create a new post (authentication required).

- `GET /api/posts/{slug}/`  
  Retrieve a single post by its **slug**.

- `PUT /api/posts/{slug}/`  
  Update a post by its **slug** (authentication and ownership required).

- `PATCH /api/posts/{slug}/`  
  Partially update a post by its **slug** (authentication and ownership required).

- `DELETE /api/posts/{slug}/`  
  Delete a post by its **slug** (authentication and ownership required).

---

## Categories

- `GET /api/categories/`  
  List all categories.

- `POST /api/categories/`  
  Create a new category.

- `GET /api/categories/{pk}/`  
  Retrieve a category by primary key.

- `PUT /api/categories/{pk}/`  
  Update a category by primary key.

- `PATCH /api/categories/{pk}/`  
  Partially update a category by primary key.

- `DELETE /api/categories/{pk}/`  
  Delete a category by primary key.

---

## Tags

- `GET /api/tags/`  
  List all tags.

- `POST /api/tags/`  
  Create a new tag.

- `GET /api/tags/{pk}/`  
  Retrieve a tag by primary key.

- `PUT /api/tags/{pk}/`  
  Update a tag by primary key.

- `PATCH /api/tags/{pk}/`  
  Partially update a tag by primary key.

- `DELETE /api/tags/{pk}/`  
  Delete a tag by primary key.

---

## Admin Panel

- `/admin/`  
  Django admin interface (site management).

---

Link: https://project10x-the-backend-builder-series.onrender.com/api/ 