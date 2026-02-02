# app.py - Part 4: Complete App with Admin Panel
# Adds admin dashboard with role-based access control (RBAC)

from flask import Flask, render_template, request, jsonify
from sqlalchemy.orm import joinedload
from models import db, init_db, User, Todo
from auth import hash_password, verify_password, create_token, token_required, admin_required

# ============================================================================
# APP CONFIGURATION
# ============================================================================
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'

init_db(app)


# ============================================================================
# PAGE ROUTES
# ============================================================================
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html')

@app.route('/admin')
def admin_page():
    """Admin panel page - frontend checks token for admin access."""
    return render_template('admin.html')


# ============================================================================
# AUTH API ROUTES
# ============================================================================
@app.route('/api/register', methods=['POST'])
def api_register():
    """Register new user with validation."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    username, email, password = data.get('username'), data.get('email'), data.get('password')
    if not username or not email or not password:
        return jsonify({'error': 'All fields required'}), 400

    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already taken'}), 400

    user = User(username=username, email=email, password_hash=hash_password(password), is_admin=False)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201


@app.route('/api/login', methods=['POST'])
def api_login():
    """Login and return JWT token with admin status."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    email, password = data.get('email'), data.get('password')
    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not verify_password(user.password_hash, password):
        return jsonify({'error': 'Invalid credentials'}), 401

    # Token includes is_admin flag for frontend to show/hide admin features
    token = create_token(user.id, user.is_admin)
    return jsonify({'token': token, 'user': user.to_dict()}), 200


# ============================================================================
# USER TODO CRUD API ROUTES
# ============================================================================
@app.route('/api/todos', methods=['GET'])
@token_required
def get_todos(current_user):
    """Get all todos for logged-in user."""
    todos = Todo.query.filter_by(user_id=current_user.id).all()
    return jsonify({'todos': [t.to_dict() for t in todos]}), 200


@app.route('/api/todos', methods=['POST'])
@token_required
def create_todo(current_user):
    """Create new todo for logged-in user."""
    data = request.get_json()
    if not data or not data.get('task_content'):
        return jsonify({'error': 'Task content required'}), 400

    todo = Todo(task_content=data['task_content'], is_completed=False, user_id=current_user.id)
    db.session.add(todo)
    db.session.commit()
    return jsonify({'message': 'Todo created', 'todo': todo.to_dict()}), 201


@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
@token_required
def update_todo(current_user, todo_id):
    """Update todo (only owner can update)."""
    todo = Todo.query.get(todo_id)
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404
    if todo.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()
    if 'task_content' in data:
        todo.task_content = data['task_content']
    if 'is_completed' in data:
        todo.is_completed = data['is_completed']

    db.session.commit()
    return jsonify({'message': 'Todo updated', 'todo': todo.to_dict()}), 200


@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
@token_required
def delete_todo(current_user, todo_id):
    """Delete todo (only owner can delete)."""
    todo = Todo.query.get(todo_id)
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404
    if todo.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    db.session.delete(todo)
    db.session.commit()
    return jsonify({'message': 'Todo deleted'}), 200


# ============================================================================
# ADMIN API ROUTES
# These routes use @admin_required decorator which:
# 1. Validates JWT token
# 2. Checks is_admin flag in token AND in database
# 3. Returns 403 if user is not an admin
# ============================================================================

@app.route('/api/admin/users', methods=['GET'])
@admin_required
def get_all_users(current_user):
    """
    Admin: Get all users with their todo counts.

    Returns list of users with statistics for admin dashboard.
    Uses to_dict_with_stats() which includes todo_count.
    """
    users = User.query.all()
    return jsonify({'users': [u.to_dict_with_stats() for u in users]}), 200


@app.route('/api/admin/todos', methods=['GET'])
@admin_required
def get_all_todos(current_user):
    """
    Admin: Get all todos with usernames.

    Uses joinedload to fetch user data in single query (fixes N+1 problem).

    N+1 Problem: Without joinedload, fetching 100 todos would cause:
    - 1 query for todos
    - 100 queries for each todo's owner

    With joinedload: Just 1 query total using SQL JOIN.
    """
    todos = Todo.query.options(joinedload(Todo.owner)).all()
    return jsonify({'todos': [t.to_dict_with_user() for t in todos]}), 200


# ============================================================================
# ADMIN SETUP (Development only)
# ============================================================================
@app.route('/api/create-admin', methods=['POST'])
def create_admin():
    """Create default admin user for testing."""
    if User.query.filter_by(email='admin@example.com').first():
        return jsonify({'message': 'Admin already exists. Use admin@example.com to login.'}), 200

    admin = User(username='admin', email='admin@example.com', password_hash=hash_password('admin123'), is_admin=True)
    db.session.add(admin)
    db.session.commit()
    print("Admin created - Email: admin@example.com, Password: admin123")
    return jsonify({'message': 'Admin created. Check console for credentials.'}), 201


# ============================================================================
# RUN SERVER
# ============================================================================
if __name__ == '__main__':
    print("\nTodo App - Part 4: Admin Panel")
    print("http://127.0.0.1:5000")
    print("Admin: admin@example.com / admin123\n")
    app.run(debug=True)
