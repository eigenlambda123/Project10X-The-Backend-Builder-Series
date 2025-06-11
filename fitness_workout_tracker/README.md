## API Endpoints – Fitness Workout Tracker

### Admin

* `GET /admin/`
  Access Django admin interface.

---

### Authentication & User Management

* `POST /api/register/`
  Register a new user.

* `POST /api/token/`
  Obtain JWT access and refresh tokens by submitting user credentials.

* `POST /api/token/refresh/`
  Refresh JWT access token using a valid refresh token.

---

### Workouts (`/api/workouts/`)

* `GET /api/workouts/`
  List all workouts for the authenticated user (supports date range filtering).

* `POST /api/workouts/`
  Create a new workout.

* `GET /api/workouts/{id}/`
  Retrieve a workout by ID.

* `PUT /api/workouts/{id}/`
  Update a workout by ID.

* `PATCH /api/workouts/{id}/`
  Partially update a workout by ID.

* `DELETE /api/workouts/{id}/`
  Delete a workout by ID.

---

### Exercises (`/api/exercises/`)

* `GET /api/exercises/`
  List all exercises for the authenticated user.

* `POST /api/exercises/`
  Create a new exercise.

* `GET /api/exercises/{id}/`
  Retrieve an exercise by ID.

* `PUT /api/exercises/{id}/`
  Update an exercise by ID.

* `PATCH /api/exercises/{id}/`
  Partially update an exercise by ID.

* `DELETE /api/exercises/{id}/`
  Delete an exercise by ID.

---

### Sets (`/api/sets/`)

* `GET /api/sets/`
  List all sets for the authenticated user.

* `POST /api/sets/`
  Create a new set (linked to a workout and exercise).

* `GET /api/sets/{id}/`
  Retrieve a set by ID.

* `PUT /api/sets/{id}/`
  Update a set by ID.

* `PATCH /api/sets/{id}/`
  Partially update a set by ID.

* `DELETE /api/sets/{id}/`
  Delete a set by ID.

---

### Analytics (`/api/analytics/`)

* `GET /api/analytics/personal-records/`
  View your max weight (1RM) per exercise.

* `GET /api/analytics/workout-streaks/`
  Get the number of consecutive workout days.