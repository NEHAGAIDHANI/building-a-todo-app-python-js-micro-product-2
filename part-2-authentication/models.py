# models.py - Database Models
# This module defines the database structure using SQLAlchemy ORM

from flask_sqlalchemy import SQLAlchemy

# Create SQLAlchemy instance (will be initialized with Flask app later)
db = SQLAlchemy()


# ============================================================================
# USER MODEL
# ============================================================================
class User(db.Model):
    """
    User model representing registered users in the system.

    Database Table: 'users'
    """
    __tablename__ = 'users'

    # Primary key - unique identifier for each user
    id = db.Column(db.Integer, primary_key=True)

    # Username - must be unique, used for display
    username = db.Column(db.String(80), unique=True, nullable=False)

    # Email - must be unique, used for login
    email = db.Column(db.String(120), unique=True, nullable=False)

    # Password hash - NEVER store plain text passwords!
    # Stores result of hash_password() from auth.py
    password_hash = db.Column(db.String(256), nullable=False)

    # Admin flag - determines access to admin features
    is_admin = db.Column(db.Boolean, default=False)

    def to_dict(self):
        """
        Convert User object to dictionary for JSON responses.
        NOTE: Never include password_hash in API responses!
        """
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_admin': self.is_admin
        }


# ============================================================================
# DATABASE INITIALIZATION
# ============================================================================
def init_db(app):
    """
    Initialize database with Flask app.

    This function:
    1. Connects SQLAlchemy to the Flask app
    2. Creates all tables defined by our models

    Called once when app starts (in app.py)
    """
    db.init_app(app)
    with app.app_context():
        db.create_all()  # Creates tables if they don't exist
