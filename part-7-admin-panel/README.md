# Part 7: Admin Panel

## What You Will Learn
- is_admin field for users
- get_admin_user() helper function
- Admin dashboard with statistics
- User management (delete users)

## Files in This Part
```
part-7-admin-panel/
├── app.py              # Flask app with admin routes
├── models.py           # User model with is_admin field
├── auth.py             # Auth with get_current_user() and get_admin_user() helpers
├── requirements.txt    # Python dependencies
├── templates/
│   ├── index.html      # Home page
│   ├── register.html   # Registration form
│   ├── login.html      # Login form
│   ├── dashboard.html  # User dashboard
│   └── admin.html      # Admin panel
```

## How to Run
```bash
cd part-7-admin-panel
pip install -r requirements.txt
python app.py
```

## Default Admin Credentials
When you run the app, it creates a default admin:
```
Email:    admin@example.com
Password: admin123
```

Open: http://127.0.0.1:5000

## Key Concepts

### 1. Admin Field in User Model
```python
class User(db.Model):
    is_admin = db.Column(db.Boolean, default=False)
```

### 2. get_admin_user() Helper Function
```python
@app.route('/api/admin/users')
def get_all_users():
    # Check if user is logged in AND is admin
    current_user, error = get_admin_user()
    if error:
        return error  # Returns 401 or 403

    # Only admins reach here
    users = User.query.all()
```

### 3. Two Helper Functions
```python
get_current_user()  # Any logged-in user (returns 401 if not logged in)
get_admin_user()    # Only admins (returns 403 if not admin)
```

### How get_admin_user() Works
```python
def get_admin_user():
    # First, check if user is logged in
    current_user, error = get_current_user()
    if error:
        return None, error  # 401 - not logged in

    # Then check if user is admin
    if not current_user.is_admin:
        return None, (jsonify({'error': 'Admin access required'}), 403)

    return current_user, None
```

### Admin API Routes
| Route                      | Method | Description        |
|----------------------------|--------|--------------------|
| /api/admin/users           | GET    | Get all users      |
| /api/admin/users/:id       | DELETE | Delete a user      |
| /api/admin/stats           | GET    | Get statistics     |
| /api/admin/todos           | GET    | Get all todos      |

### 401 vs 403 Error Codes
```
401 Unauthorized = Not logged in (no token or invalid token)
403 Forbidden    = Logged in but not allowed (not admin)
```

## Next Part
Part 8 is your homework! Add priority feature to todos.
