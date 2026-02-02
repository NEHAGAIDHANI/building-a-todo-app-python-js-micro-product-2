# app.py - Part 2: Authentication
# Main Flask application with user registration and login

from flask import Flask, render_template, request, jsonify
from models import db, init_db, User
from auth import hash_password, verify_password, create_token

# ============================================================================
# APP CONFIGURATION
# ============================================================================
app = Flask(__name__)

# Database config - SQLite file stored in instance folder
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable overhead

# Secret key for sessions (change in production!)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'

# Initialize database tables
init_db(app)


# ============================================================================
# PAGE ROUTES - Serve HTML templates
# ============================================================================
@app.route('/')
def home():
    """Landing page with links to login/register."""
    return render_template('index.html')


@app.route('/register')
def register_page():
    """Registration form page."""
    return render_template('register.html')


@app.route('/login')
def login_page():
    """Login form page."""
    return render_template('login.html')


# ============================================================================
# API ROUTES - Handle form submissions (JSON)
# ============================================================================
@app.route('/api/register', methods=['POST'])
def api_register():
    """
    Register a new user.

    Expected JSON: { "username": "...", "email": "...", "password": "..." }

    Process:
    1. Validate all fields present
    2. Check password strength
    3. Check email/username not taken
    4. Hash password and save user
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    username, email, password = data.get('username'), data.get('email'), data.get('password')

    # Validate required fields
    if not username or not email or not password:
        return jsonify({'error': 'All fields are required'}), 400

    # Validate password strength
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400

    # Check for existing users
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already taken'}), 400

    # Create new user with hashed password
    new_user = User(username=username, email=email, password_hash=hash_password(password), is_admin=False)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201


@app.route('/api/login', methods=['POST'])
def api_login():
    """
    Authenticate user and return JWT token.

    Expected JSON: { "email": "...", "password": "..." }

    Process:
    1. Find user by email
    2. Verify password hash
    3. Generate JWT token
    4. Return token to client (stored in localStorage)
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    email, password = data.get('email'), data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400

    # Find user and verify credentials
    user = User.query.filter_by(email=email).first()

    if not user or not verify_password(user.password_hash, password):
        return jsonify({'error': 'Invalid credentials'}), 401

    # Create JWT token containing user_id and admin status
    token = create_token(user.id, user.is_admin)
    return jsonify({'token': token, 'user': user.to_dict()}), 200


# ============================================================================
# ADMIN SETUP ROUTE (Development only)
# ============================================================================
@app.route('/api/create-admin', methods=['POST'])
def create_admin():
    """
    Create default admin user for testing.

    WARNING: This endpoint should be removed or protected in production!
    Credentials are printed to console, not returned in response.
    """
    if User.query.filter_by(email='admin@example.com').first():
        return jsonify({'message': 'Admin already exists. Use admin@example.com to login.'}), 200

    admin = User(username='admin', email='admin@example.com', password_hash=hash_password('admin123'), is_admin=True)
    db.session.add(admin)
    db.session.commit()

    # Print to console only - never expose credentials in API response!
    print("Admin created - Email: admin@example.com, Password: admin123")
    return jsonify({'message': 'Admin created. Check console for credentials.'}), 201


# ============================================================================
# RUN SERVER
# ============================================================================
if __name__ == '__main__':
    print("\n" + "="*40)
    print("Todo App - Part 2: Authentication")
    print("http://127.0.0.1:5000")
    print("="*40 + "\n")
    app.run(debug=True)
