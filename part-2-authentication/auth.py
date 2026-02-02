# auth.py - Authentication Helpers
# This module handles password hashing and JWT token creation for login/register

import jwt
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

# ============================================================================
# CONFIGURATION
# ============================================================================
# SECRET_KEY: Used to sign JWT tokens. MUST be changed in production!
# Anyone with this key can create valid tokens for any user.
SECRET_KEY = "your-secret-key-change-in-production"

# How long tokens remain valid (24 hours)
TOKEN_EXPIRATION_HOURS = 24


# ============================================================================
# PASSWORD FUNCTIONS
# ============================================================================
def hash_password(password):
    """
    Convert plain text password to secure hash.

    Uses Werkzeug's generate_password_hash which:
    - Adds random salt (prevents rainbow table attacks)
    - Uses PBKDF2 algorithm (slow = harder to brute force)

    Example: "mypassword" -> "pbkdf2:sha256:260000$..."
    """
    return generate_password_hash(password)


def verify_password(password_hash, password):
    """
    Check if plain text password matches stored hash.

    Returns True if password is correct, False otherwise.
    Never compare passwords directly - always hash and compare hashes.
    """
    return check_password_hash(password_hash, password)


# ============================================================================
# JWT TOKEN FUNCTIONS
# ============================================================================
def create_token(user_id, is_admin=False):
    """
    Create a JWT (JSON Web Token) for authenticated user.

    JWT Structure:
    - Header: Algorithm info (HS256)
    - Payload: Our data (user_id, is_admin, expiration)
    - Signature: Proves token wasn't tampered with

    The token is sent to client and stored in localStorage.
    Client sends it back with each request in Authorization header.
    """
    payload = {
        'user_id': user_id,           # Who this token belongs to
        'is_admin': is_admin,         # User's admin status
        'exp': datetime.utcnow() + timedelta(hours=TOKEN_EXPIRATION_HOURS),  # When token expires
        'iat': datetime.utcnow()      # When token was created
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')
