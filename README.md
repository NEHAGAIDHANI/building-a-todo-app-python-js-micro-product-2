# Module 07: Building A Micro Product - To-Do List Management

## From Code to Concept: Launching Your First SaaS

> **Psychology:** This is the "Aha!" moment. Students move away from isolated exercises and build a complete, cohesive product. By creating an Admin view, they understand the "Power Dynamic" of software: User vs. System.

---

## Overview

This module guides you through building a complete, production-ready Todo application with:
- User Authentication (JWT)
- CRUD Operations
- Admin Panel
- Role-Based Access Control

---

## Module Structure

```
module-07-todo-app/
│
├── README.md                    # This file
│
├── part-1-foundation/           # Project setup & Database models
│   ├── app.py
│   ├── models.py
│   ├── templates/
│   └── README.md
│
├── part-2-authentication/       # Register & Login with JWT
│   ├── app.py
│   ├── models.py
│   ├── auth.py
│   ├── templates/
│   └── README.md
│
├── part-3-crud-operations/      # Todo CRUD with protected routes
│   ├── app.py
│   ├── models.py
│   ├── auth.py
│   ├── templates/
│   └── README.md
│
├── part-4-admin-panel/          # Admin views (complete app)
│   ├── app.py
│   ├── models.py
│   ├── auth.py
│   ├── templates/
│   └── README.md
│
└── part-5-homework/             # Practice assignment
    ├── README.md
    └── starter-code/
```

---

## Learning Path

| Part | Focus | Skills Learned |
|------|-------|----------------|
| **Part 1** | Foundation | Flask setup, SQLAlchemy models, One-to-Many relationships |
| **Part 2** | Authentication | Password hashing, JWT tokens, localStorage |
| **Part 3** | CRUD Operations | Protected routes, API design, Dynamic UI |
| **Part 4** | Admin Panel | Role-based access, Internal tools, Conditional rendering |
| **Part 5** | Homework | Apply all skills to add a new feature |

---

## Database Design

### Tables

**User Table**
| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary Key |
| username | String(80) | Unique username |
| email | String(120) | Unique email |
| password_hash | String(256) | Hashed password |
| is_admin | Boolean | Admin flag |

**Todo Table**
| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary Key |
| task_content | String(200) | Task text |
| is_completed | Boolean | Completion status |
| user_id | Integer | Foreign Key → User.id |

### Relationship
```
One User → Many Todos (One-to-Many)
```

---

## Technology Stack

| Component | Technology |
|-----------|------------|
| Backend | Flask 3.0 |
| Database | SQLite + Flask-SQLAlchemy |
| Authentication | JWT (PyJWT) |
| Password Hashing | Werkzeug |
| Frontend | Bootstrap 5 |
| API Style | RESTful |

---

## Quick Start

### Prerequisites
- Python 3.8+
- pip

### Run Any Part

```bash
# Navigate to the part you want to run
cd part-4-admin-panel

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

Then open: `http://127.0.0.1:5000`

---

## API Reference

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/register | Create new account |
| POST | /api/login | Login & get JWT token |

### Todos (Protected)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/todos | Get user's todos |
| POST | /api/todos | Create new todo |
| PUT | /api/todos/<id> | Update todo |
| DELETE | /api/todos/<id> | Delete todo |

### Admin (Admin Only)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/admin/users | View all users |
| GET | /api/admin/todos | View all todos |

---

## Key Technical Concepts

### 1. JWT Authentication Flow
```
Register → Login → Get Token → Store in localStorage → Send with every request
```

### 2. Protected Routes
```python
@app.route('/api/todos')
@token_required
def get_todos(current_user):
    # Only authenticated users can access
    pass
```

### 3. Admin Routes
```python
@app.route('/api/admin/users')
@admin_required
def get_all_users(current_user):
    # Only admins can access
    pass
```

### 4. Conditional Rendering
```javascript
if (user.is_admin) {
    // Show admin link
}
```

---

## Test Accounts

After running the app, create a test admin:
1. Go to the login page
2. Click "Create Admin User"
3. Login with:
   - **Email:** admin@example.com
   - **Password:** admin123

---

## Learning Outcomes

By completing this module, students will be able to:

1. **Design Databases** - Create related tables with foreign keys
2. **Build APIs** - Implement RESTful endpoints with Flask
3. **Implement Auth** - Use JWT for stateless authentication
4. **Protect Routes** - Create decorators for access control
5. **Build UIs** - Create dynamic interfaces with Bootstrap & JavaScript
6. **Think in Systems** - Understand User vs. Admin perspectives

---

## Next Steps

After completing this module:
1. Add more features (due dates, categories, search)
2. Deploy to a cloud platform (Heroku, Railway, etc.)
3. Add email verification
4. Implement password reset
5. Add real-time updates with WebSockets

---

Happy Coding! 🚀
