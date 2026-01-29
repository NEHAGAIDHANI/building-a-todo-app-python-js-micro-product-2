# models.py - Database Models
# HOMEWORK: Add 'priority' column to Todo model

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    todos = db.relationship('Todo', backref='owner', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_admin': self.is_admin
        }

    def to_dict_with_stats(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_admin': self.is_admin,
            'todo_count': len(self.todos)
        }


class Todo(db.Model):
    __tablename__ = 'todos'

    id = db.Column(db.Integer, primary_key=True)
    task_content = db.Column(db.String(200), nullable=False)
    is_completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # TODO: Add priority column - priority = db.Column(db.String(10), default='medium')

    def to_dict(self):
        return {
            'id': self.id,
            'task_content': self.task_content,
            'is_completed': self.is_completed,
            'user_id': self.user_id
            # TODO: Add 'priority': self.priority
        }

    def to_dict_with_user(self):
        return {
            'id': self.id,
            'task_content': self.task_content,
            'is_completed': self.is_completed,
            'user_id': self.user_id,
            'username': self.owner.username
            # TODO: Add 'priority': self.priority
        }


def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
