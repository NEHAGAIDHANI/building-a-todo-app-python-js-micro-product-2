# auth.py - Authentication Helpers
# Handles password hashing, JWT tokens, and route protection decorators

import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

# ============================================================================
# CONFIGURATION
# ============================================================================
SECRET_KEY = "your-secret-key-change-in-production"  # Change in production!
TOKEN_EXPIRATION_HOURS = 24


# ============================================================================
# PASSWORD FUNCTIONS
# ============================================================================
def hash_password(password):
    """Hash password using PBKDF2 with random salt."""
    return generate_password_hash(password)


def verify_password(password_hash, password):
    """Verify password against stored hash."""
    return check_password_hash(password_hash, password)


# ============================================================================
# JWT TOKEN FUNCTIONS
# ============================================================================
def create_token(user_id, is_admin=False):
    """
    Create JWT token with user info and expiration.
    Token contains: user_id, is_admin, expiration time
    """
    payload = {'user_id': user_id, 'is_admin': is_admin, 'exp': datetime.utcnow() + timedelta(hours=TOKEN_EXPIRATION_HOURS)}
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')


def decode_token(token):
    """Decode JWT token. Returns None if invalid/expired."""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None


# ============================================================================
# DECORATOR: @token_required
# ============================================================================
def token_required(f):
    """
    Decorator to protect routes requiring authentication.

    How it works:
    1. Extracts JWT from "Authorization: Bearer <token>" header
    2. Decodes and validates the token
    3. Fetches user from database
    4. Passes user as first argument to the wrapped function

    Usage:
        @app.route('/protected')
        @token_required
        def my_route(current_user):  # current_user injected by decorator
            return f"Hello {current_user.username}"
    """
    @wraps(f)  # Preserves original function's name and docstring
    def decorated(*args, **kwargs):
        # Extract token from Authorization header
        if 'Authorization' not in request.headers:
            return jsonify({'error': 'Token is missing'}), 401

        try:
            token = request.headers['Authorization'].split(" ")[1]
        except IndexError:
            return jsonify({'error': 'Invalid token format'}), 401

        # Validate token
        data = decode_token(token)
        if not data:
            return jsonify({'error': 'Token is invalid or expired'}), 401

        # Get user from database (import here to avoid circular imports)
        from models import User
        current_user = User.query.get(data['user_id'])
        if not current_user:
            return jsonify({'error': 'User not found'}), 401

        # Call original function with current_user as first argument
        return f(current_user, *args, **kwargs)
    return decorated


# ============================================================================
# DECORATOR: @admin_required
# ============================================================================
def admin_required(f):
    """
    Decorator to protect admin-only routes.

    Two-layer security:
    1. Checks is_admin flag in JWT token (fast, no DB query)
    2. Verifies is_admin in database (ensures admin wasn't revoked)

    This prevents issues where:
    - User still has old token but admin was revoked in DB
    - Token was tampered with (signature check catches this anyway)
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        # Extract token from Authorization header
        if 'Authorization' not in request.headers:
            return jsonify({'error': 'Token is missing'}), 401

        try:
            token = request.headers['Authorization'].split(" ")[1]
        except IndexError:
            return jsonify({'error': 'Invalid token format'}), 401

        # Validate token
        data = decode_token(token)
        if not data:
            return jsonify({'error': 'Token is invalid or expired'}), 401

        # First check: is_admin in token (fast check)
        if not data.get('is_admin', False):
            return jsonify({'error': 'Admin access required'}), 403

        # Get user from database
        from models import User
        current_user = User.query.get(data['user_id'])
        if not current_user:
            return jsonify({'error': 'User not found'}), 401

        # Second check: verify admin status in database
        # This catches cases where admin was revoked after token was issued
        if not current_user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403

        return f(current_user, *args, **kwargs)
    return decorated
