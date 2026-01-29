# Part 3: CRUD Operations - Building the Todo Dashboard

## 🎯 Learning Objectives
By the end of this part, you will understand:
- How to create protected API routes using JWT decorators
- How to implement CRUD (Create, Read, Update, Delete) operations
- How to make authenticated API calls from JavaScript
- How to build a dynamic dashboard that updates without page refresh
- How to use the Authorization header with Bearer tokens

---

## 📁 Project Structure
```
part-3-crud-operations/
├── app.py              # Main app with all routes
├── models.py           # Database models
├── auth.py             # Authentication helpers
├── templates/
│   ├── index.html      # Home page
│   ├── login.html      # Login form
│   ├── register.html   # Registration form
│   └── dashboard.html  # Todo dashboard (NEW!)
└── requirements.txt
```

---

## 🔄 CRUD Operations Explained

| Operation | HTTP Method | Endpoint | Description |
|-----------|-------------|----------|-------------|
| **C**reate | POST | /api/todos | Add a new todo |
| **R**ead | GET | /api/todos | Get all user's todos |
| **U**pdate | PUT | /api/todos/<id> | Update a todo |
| **D**elete | DELETE | /api/todos/<id> | Delete a todo |

---

## 🚀 Step-by-Step Instructions

### Step 1: Install Dependencies
```bash
pip install flask flask-sqlalchemy pyjwt werkzeug
```

### Step 2: Run the Application
```bash
python app.py
```

### Step 3: Test the Flow
1. Register a new account: `http://127.0.0.1:5000/register`
2. Login: `http://127.0.0.1:5000/login`
3. Access Dashboard: `http://127.0.0.1:5000/dashboard`
4. Add, complete, and delete todos!

---

## 📡 API Endpoints (Protected)

All todo endpoints require the Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

### GET /api/todos
**Response:**
```json
{
    "todos": [
        {
            "id": 1,
            "task_content": "Learn Flask",
            "is_completed": false,
            "user_id": 1
        }
    ]
}
```

### POST /api/todos
**Request:**
```json
{
    "task_content": "Buy groceries"
}
```

**Response:**
```json
{
    "message": "Todo created",
    "todo": {
        "id": 2,
        "task_content": "Buy groceries",
        "is_completed": false,
        "user_id": 1
    }
}
```

### PUT /api/todos/<id>
**Request:**
```json
{
    "task_content": "Buy groceries and cook",
    "is_completed": true
}
```

### DELETE /api/todos/<id>
**Response:**
```json
{
    "message": "Todo deleted"
}
```

---

## 📝 Key Concepts Explained

### The @token_required Decorator
```python
@app.route('/api/todos')
@token_required
def get_todos(current_user):
    # current_user is automatically passed by the decorator
    # Only returns todos belonging to THIS user
    todos = Todo.query.filter_by(user_id=current_user.id).all()
```

### Making Authenticated Requests (JavaScript)
```javascript
// Get the token from localStorage
const token = localStorage.getItem('token');

// Include it in the Authorization header
const response = await fetch('/api/todos', {
    method: 'GET',
    headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
    }
});
```

### Stateful UI Updates
Instead of reloading the page after each action, we update the UI immediately:
```javascript
// After adding a todo
function addTodoToUI(todo) {
    const todoList = document.getElementById('todo-list');
    // Create and append new element
    // No page reload needed!
}
```

---

## ✅ Practice Exercise
1. Add a feature to edit the task content (not just toggle complete)
2. Add a "Clear Completed" button that deletes all completed todos
3. Add a todo counter showing "3 of 5 tasks completed"

---

## 📚 What's Next?
In **Part 4**, we will:
- Build the Admin Panel
- View all users in the system
- View all todos (global feed)
- Implement admin-only route protection
