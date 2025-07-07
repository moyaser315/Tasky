# Tasky – Backend

Tasky is a FastAPI-based backend for a task management system, featuring secure authentication (JWT + API Key), async endpoints, and a clean, modular architecture.

---

## 🚀 Project Setup

1. **Clone the repository:**
   ```sh
   git clone <your-repo-url>
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
   - Edit `app/config.py` or set variables for `SECRET_KEY`, `ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`, and `API_KEY` as needed.

5. **Run the application:**
   ```sh
   uvicorn app.main:app --reload
   ```

6. **Access the API docs:**
   - Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
   - ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 👤 How to Create a User and Login

1. **Sign Up**
   - `POST /signup`
   - Body:
     ```json
     {
       "username": "your_username",
       "email": "your_email",
       "password": "your_password"
     }
     ```

2. **Login**
   - `POST /token`
   - Body (form data):
     ```
     username=your_username
     password=your_password
     ```
   - Response:
     ```json
     {
       "access_token": "<JWT_TOKEN>",
       "token_type": "bearer"
     }
     ```

---

## 🔐 Example: JWT + API Key Authentication

All `/tasks` endpoints require:
- **Authorization**: Bearer token (from `/token`)
- **Header**: `X-API-Key: 123456` (or your configured API key)

**Example request:**
```sh
curl -X GET "http://localhost:8000/tasks" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "X-API-Key: 123456"
```

---

## 📚 API Documentation

- **POST /signup** – Register a new user
- **POST /token** – Obtain JWT token (OAuth2 password flow)
- **POST /tasks** – Create a new task (protected)
- **GET /tasks** – List all tasks for the current user (protected)
- **GET /tasks/{id}** – Get a specific task (protected)
- **PUT /tasks/{id}** – Update a task’s status (protected)
- **DELETE /tasks/{id}** – Delete a task (protected)

See [http://localhost:8000/docs](http://localhost:8000/docs) for full interactive API docs.

---

## 🌐 Live Deployment

- [Live API URL](https://your-deployment-url.com)



