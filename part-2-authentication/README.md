# Part 2: Authentication - Register & Login with JWT

## 🎯 Learning Objectives
By the end of this part, you will understand:
- How to hash passwords securely using Werkzeug
- How to create REST API endpoints for registration and login
- How JWT (JSON Web Tokens) work for authentication
- How to store tokens in the browser's localStorage
- How to build login/register forms with Bootstrap

---

## 📁 Project Structure
```
part-2-authentication/
├── app.py              # Main Flask application with routes
├── models.py           # Database models (same as Part 1)
├── auth.py             # Authentication helper functions
├── templates/
│   ├── index.html      # Home page
│   ├── login.html      # Login form
│   └── register.html   # Registration form
└── requirements.txt
```

---

## 🔐 Authentication Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Register  │ ──► │   Login     │ ──► │  Get Token  │
│   (Create   │     │   (Verify   │     │  (JWT)      │
│   Account)  │     │   Password) │     │             │
└─────────────┘     └─────────────┘     └──────┬──────┘
                                               │
                                               ▼
                                        ┌─────────────┐
                                        │   Store in  │
                                        │ localStorage│
                                        └─────────────┘
```

---

## 🚀 Step-by-Step Instructions

### Step 1: Install New Dependencies
```bash
pip install flask flask-sqlalchemy pyjwt werkzeug
```

### Step 2: Understand Password Hashing (auth.py)
```python
# NEVER store plain text passwords!
# Werkzeug provides secure hashing functions

from werkzeug.security import generate_password_hash, check_password_hash

# When registering: hash the password
hashed = generate_password_hash("user_password")

# When logging in: verify the password
is_valid = check_password_hash(hashed, "user_password")
```

### Step 3: Understand JWT Tokens (auth.py)
```python
import jwt

# Create a token (after successful login)
token = jwt.encode(
    {"user_id": 1, "exp": expiration_time},
    "secret_key",
    algorithm="HS256"
)

# Decode a token (to verify user)
data = jwt.decode(token, "secret_key", algorithms=["HS256"])
user_id = data["user_id"]
```

### Step 4: Run the Application
```bash
python app.py
```

### Step 5: Test the Endpoints
1. Go to: `http://127.0.0.1:5000/register` - Create an account
2. Go to: `http://127.0.0.1:5000/login` - Login with your credentials
3. Check browser console (F12) to see the token stored

---

## 📡 API Endpoints

### POST /api/register
**Request Body:**
```json
{
    "username": "john",
    "email": "john@example.com",
    "password": "secret123"
}
```

**Response (Success - 201):**
```json
{
    "message": "User registered successfully"
}
```

### POST /api/login
**Request Body:**
```json
{
    "email": "john@example.com",
    "password": "secret123"
}
```

**Response (Success - 200):**
```json
{
    "token": "eyJhbGciOiJIUzI1NiIs...",
    "user": {
        "id": 1,
        "username": "john",
        "is_admin": false
    }
}
```

---

## 📝 Key Concepts Explained

### What is JWT?
JWT (JSON Web Token) is a secure way to transmit information between parties. It contains:
- **Header**: Type and algorithm
- **Payload**: User data (id, role, expiration)
- **Signature**: Verification that the token hasn't been tampered with

### Why localStorage?
After login, we store the token in the browser's localStorage so that:
- The user stays logged in across page refreshes
- We can send the token with every API request
- The token persists until we explicitly remove it (logout)

### Token Storage in JavaScript
```javascript
// Store token after login
localStorage.setItem('token', response.token);
localStorage.setItem('user', JSON.stringify(response.user));

// Retrieve token for API calls
const token = localStorage.getItem('token');

// Remove token on logout
localStorage.removeItem('token');
```

---

## ✅ Practice Exercise
1. Try registering with the same email twice - observe the error
2. Try logging in with wrong password - observe the error
3. Open browser DevTools (F12) → Application → Local Storage
4. See the token and user data stored there after login

---

## 📚 What's Next?
In **Part 3**, we will:
- Create protected API routes using the JWT token
- Build CRUD operations for Todo items
- Create a dashboard to manage tasks
