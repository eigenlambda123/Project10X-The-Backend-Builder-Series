## API Endpoints – URL Shortener API

### Admin

* `GET /admin/`
  Access the Django admin interface for managing users, short links, and click events.

---

### Authentication & User Management

* `POST /api/token/`
  Obtain JWT access and refresh tokens using valid user credentials.

* `POST /api/token/refresh/`
  Refresh your access token with a valid refresh token.

---

### Short URLs (`/api/urls/`)

* `GET /api/urls/`
  List all short links created by the authenticated user.

* `POST /api/urls/`
  Create a new short link (automatically binds to user).

* `GET /api/urls/{id}/`
  Retrieve details of a specific short link by ID.

* `PUT /api/urls/{id}/`
  Update a short link’s data (e.g., destination URL, expiration).

* `PATCH /api/urls/{id}/`
  Partially update a short link.

* `DELETE /api/urls/{id}/`
  Delete a short link.

---

### Redirection

* `GET /r/{short_code}/`
  Redirects to the original URL if active and not expired.
  Also logs click event with timestamp and IP.

---

### QR Code (`qr_code` field in detail response)

* Automatically included in `GET /api/urls/{id}/`
  Base64-encoded PNG image of QR code pointing to short link.

---

### Click Analytics (`/api/urls/{id}/stats/`)

* `GET /api/urls/{id}/stats/`
  View click statistics for a given short link:

  * Total clicks
  * Latest click timestamps
  * IP address logs

