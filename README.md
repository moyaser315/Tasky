# Tasky – Backend

Tasky is a FastAPI-based backend for a task management system, featuring secure authentication, async endpoints, and a clean, modular architecture.

---

## 🚀 Project Setup

1. **Clone the repository:**
   ```sh
   git clone https://github.com/moyaser315/Tasky.git
   cd tasky
   ```

2. **Create and activate a virtual environment:**
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set environment variables (optional):**
   - Make a .env file as follows:
   ```sh
   SECRET_KEY=sssssssssssssss
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=120
   DATABASE_URL=Your_Url_Here
   ```

5. **Run the application:**
   ```sh
   uvicorn app.main:app --reload
   ```

6. **Access the API docs:**
   - Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
   - ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## Calling APIs

### 1. Sign Up

```bash
curl -X POST "http://localhost:8000/signup" \
     -H "Content-Type: application/json" \
     -d '{
        "username": "user",
        "email": "user@example.com",
        "password": "SecurePassword123"
     }'
```

**Response:**
```json
{
   "id": 1,
   "email": "user@example.com",
   "api_key": "your-api-key-here"
}
```

### 2. Login

```bash
curl -X POST "http://localhost:8000/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=user@example.com&password=SecurePassword123"
```

**Response:**
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "api_key": "your-api-key-here"
}
```

### 3. Create a Task

```bash
curl -X POST "http://localhost:8000/tasks/" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -H "X-API-Key: YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Complete project documentation",
       "description": "Write comprehensive README and API documentation",
       "status": "pending"
     }'
```

**Response:**
```json
{
  "id": 1,
  "title": "Complete project documentation",
  "description": "Write comprehensive README and API documentation",
  "status": "pending",
  "user_id": 1,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": null
}
```

### 4. Get All Tasks

```bash
curl -X GET "http://localhost:8000/tasks/" \
     -H "X-API-Key: YOUR_API_KEY" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "Complete project documentation",
    "description": "Write comprehensive README and API documentation",
    "status": "pending",
    "user_id": 1,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": null
  }
]
```

### 5. Get a Specific Task

```bash
curl -X GET "http://localhost:8000/tasks/1" \
     -H "X-API-Key: YOUR_API_KEY" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 6. Update a Task

```bash
curl -X PUT "http://localhost:8000/tasks/1" \
     -H "X-API-Key: YOUR_API_KEY" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "status": "completed"
     }'
```

### 7. Delete a Task

```bash
curl -X DELETE "http://localhost:8000/tasks/1" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -H "X-API-Key: YOUR_API_KEY"
```

---

## Example: JWT + API Key Authentication

All `/tasks` endpoints require:
- **Authorization**: Bearer token 
- **Header**: `X-API-Key: 123456` 

---

## API Documentation

- **POST /signup** – Register a new user
- **POST /token** – Obtain JWT token (OAuth2 password flow)
- **POST /tasks** – Create a new task (protected)
- **GET /tasks** – List all tasks for the current user (protected)
- **GET /tasks/{id}** – Get a specific task (protected)
- **PUT /tasks/{id}** – Update a task's status (protected)
- **DELETE /tasks/{id}** – Delete a task (protected)

See [http://localhost:8000/docs](http://localhost:8000/docs) for full interactive API docs.

---

## Live Deployment

- [Live URL](https://tasky-sable.vercel.app/)
