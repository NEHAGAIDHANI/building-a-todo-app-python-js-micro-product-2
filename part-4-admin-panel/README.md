# Part 4: Admin Panel - The Command Center

## 🎯 Learning Objectives
By the end of this part, you will understand:
- How to create admin-only protected routes
- How to implement role-based access control (RBAC)
- How to build internal tools for monitoring users and data
- How to use conditional rendering based on user roles
- The "Power Dynamic" of software: User vs. System

---

## 📁 Project Structure
```
part-4-admin-panel/
├── app.py              # Complete app with admin routes
├── models.py           # Database models
├── auth.py             # Auth with admin_required decorator
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   └── admin.html      # Admin panel (NEW!)
└── requirements.txt
```

---

## 🔐 Role-Based Access Control

### User Roles
| Role | is_admin | Can Access |
|------|----------|------------|
| Regular User | False | Own todos only |
| Admin | True | All users + All todos |

### Access Matrix
| Endpoint | Regular User | Admin |
|----------|-------------|-------|
| /api/todos | Own todos | Own todos |
| /api/admin/users | 403 Forbidden | All users |
| /api/admin/todos | 403 Forbidden | All todos |

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

### Step 3: Create an Admin User
1. Go to login page
2. Click "Create Admin User" button
3. Login with: `admin@example.com` / `admin123`

### Step 4: Access Admin Panel
- Login as admin
- You'll see "Admin" link in the navbar
- View all users and all todos in the system

---

## 📡 Admin API Endpoints

### GET /api/admin/users
**Access:** Admin only
**Response:**
```json
{
    "users": [
        {
            "id": 1,
            "username": "admin",
            "email": "admin@example.com",
            "is_admin": true,
            "todo_count": 5
        },
        {
            "id": 2,
            "username": "john",
            "email": "john@example.com",
            "is_admin": false,
            "todo_count": 3
        }
    ]
}
```

### GET /api/admin/todos
**Access:** Admin only
**Response:**
```json
{
    "todos": [
        {
            "id": 1,
            "task_content": "Learn Flask",
            "is_completed": false,
            "user_id": 2,
            "username": "john"
        }
    ]
}
```

---

## 📝 Key Concepts Explained

### The @admin_required Decorator
```python
@app.route('/api/admin/users')
@admin_required
def get_all_users(current_user):
    # This route is ONLY accessible to admins
    # Regular users get 403 Forbidden
    pass
```

### How It Works
```python
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # ... token verification ...

        # CHECK IF USER IS ADMIN
        if not data.get('is_admin', False):
            return jsonify({'error': 'Admin access required'}), 403

        # ... continue if admin ...
    return decorated
```

### Conditional Rendering in JavaScript
```javascript
// Only show Admin link if user is admin
if (user.is_admin) {
    navLinks.innerHTML += '<a class="nav-link" href="/admin">Admin</a>';
}
```

### Security Best Practices
1. **Never trust the frontend** - Always verify admin status on the backend
2. **Use decorators** - Centralize access control logic
3. **Return 403, not 404** - Be honest about unauthorized access
4. **Log admin actions** - Track who did what (advanced)

---

## 🏗️ The Complete Application Flow

```
┌─────────────────────────────────────────────────────────┐
│                    TODO APP FLOW                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────┐    ┌─────────┐    ┌─────────────┐         │
│  │ Register│───►│  Login  │───►│  Dashboard  │         │
│  └─────────┘    └────┬────┘    │  (My Todos) │         │
│                      │         └─────────────┘         │
│                      │                                  │
│                      │ if admin                         │
│                      ▼                                  │
│              ┌───────────────┐                         │
│              │  Admin Panel  │                         │
│              │ - All Users   │                         │
│              │ - All Todos   │                         │
│              └───────────────┘                         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## ✅ Practice Exercise
1. Add a "Delete User" button in the admin panel (admin only)
2. Add a "Toggle Admin" button to promote/demote users
3. Add a search/filter feature to find specific users or todos

---

## 📚 Congratulations!
You have completed the full Todo App with:
- User Authentication (JWT)
- CRUD Operations
- Admin Panel with Role-Based Access

Proceed to **Part 5** for a homework activity!
