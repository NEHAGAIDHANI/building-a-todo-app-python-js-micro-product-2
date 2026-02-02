# models.py - Database Models
# Defines User and Todo tables using SQLAlchemy ORM
# Includes additional methods for admin views

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# ============================================================================
# USER MODEL
# ============================================================================
class User(db.Model):
    """
    User model - stores registered users.

    Relationships:
    - One user has many todos (user.todos)
    - Each todo has one owner (todo.owner)
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)  # Never store plain passwords!
    is_admin = db.Column(db.Boolean, default=False)

    # Relationship: user.todos returns all todos for this user
    # backref='owner' creates todo.owner to access the user
    todos = db.relationship('Todo', backref='owner', lazy=True)

    def to_dict(self):
        """Convert to dict for JSON response (excludes password)."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_admin': self.is_admin
        }

    def to_dict_with_stats(self):
        """
        Convert to dict with statistics for admin view.

        Includes todo_count for admin dashboard metrics.
        Note: len(self.todos) triggers a query if todos not loaded.
        For large datasets, consider using a COUNT subquery instead.
        """
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_admin': self.is_admin,
            'todo_count': len(self.todos)
        }


# ============================================================================
# TODO MODEL
# ============================================================================
class Todo(db.Model):
    """
    Todo model - stores tasks.

    Each todo belongs to one user (via user_id foreign key).
    """
    __tablename__ = 'todos'

    id = db.Column(db.Integer, primary_key=True)
    task_content = db.Column(db.String(200), nullable=False)
    is_completed = db.Column(db.Boolean, default=False)

    # Foreign key links todo to user
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def to_dict(self):
        """Convert to dict for JSON response."""
        return {
            'id': self.id,
            'task_content': self.task_content,
            'is_completed': self.is_completed,
            'user_id': self.user_id
        }

    def to_dict_with_user(self):
        """
        Convert to dict with username for admin view.

        Includes the owner's username so admin can see who created each todo.

        IMPORTANT: To avoid N+1 queries, use joinedload when fetching:
            Todo.query.options(joinedload(Todo.owner)).all()

        Without joinedload, accessing self.owner.username triggers
        a separate database query for EACH todo.
        """
        return {
            'id': self.id,
            'task_content': self.task_content,
            'is_completed': self.is_completed,
            'user_id': self.user_id,
            'username': self.owner.username
        }


# ============================================================================
# DATABASE INITIALIZATION
# ============================================================================
def init_db(app):
    """Initialize database with Flask app and create tables."""
    db.init_app(app)
    with app.app_context():
        db.create_all()
