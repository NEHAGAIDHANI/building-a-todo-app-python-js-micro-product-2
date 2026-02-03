# Part 6: Protected Routes

## What You Will Learn
- get_current_user() helper function
- Authorization header
- User ownership verification
- 401 and 403 error responses

## Files in This Part
```
part-6-protected-routes/
├── app.py              # Flask app with protected routes
├── models.py           # Database models
├── auth.py             # Auth with get_current_user() helper
├── requirements.txt    # Python dependencies
├── templates/
│   ├── index.html      # Home page
│   ├── register.html   # Registration form
│   ├── login.html      # Login form
│   └── dashboard.html  # Protected dashboard
```

## How to Run
```bash
cd part-6-protected-routes
pip install -r requirements.txt
python app.py
```
Open: http://127.0.0.1:5000

## Key Concepts

### 1. get_current_user() Helper Function
```python
@app.route('/api/todos')
def get_todos():
    # Step 1: Check if user is logged in
    current_user, error = get_current_user()
    if error:
        return error  # Returns 401 if not logged in

    # Step 2: Get user's todos
    todos = Todo.query.filter_by(user_id=current_user.id).all()
```

### 2. Authorization Header
```javascript
fetch('/api/todos', {
    headers: {
        'Authorization': 'Bearer ' + token
    }
})
```

### 3. Ownership Check
```python
if todo.user_id != current_user.id:
    return jsonify({'error': 'Unauthorized'}), 403
```

### How the Helper Function Works
```python
def get_current_user():
    # 1. Check if Authorization header exists
    if 'Authorization' not in request.headers:
        return None, (jsonify({'error': 'Token is missing'}), 401)

    # 2. Extract token from "Bearer <token>"
    token = request.headers['Authorization'].split(' ')[1]

    # 3. Decode token to get user_id
    user_id = decode_token(token)
    if not user_id:
        return None, (jsonify({'error': 'Invalid token'}), 401)

    # 4. Get user from database
    current_user = User.query.get(user_id)

    # 5. Return user (no error)
    return current_user, None
```

### Why Helper Function Instead of Decorator?
We use a helper function instead of a decorator for easier learning:
- You can see exactly what happens step-by-step
- No "magic" - the code is explicit and clear
- Easy to debug with print statements
- In real projects, decorators are cleaner but hide the logic

## Next Part
In Part 7, we will add admin panel to manage users.
