# app.py - Part 1: Foundation

from flask import Flask, render_template
from models import db, init_db, User, Todo

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db(app)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/test-db')
def test_db():
    user = User.query.filter_by(username='testuser').first()

    if not user:  # Create test user if not exists
        user = User(
            username='testuser',
            email='test@example.com',
            password_hash='placeholder',
            is_admin=False
        )
        db.session.add(user)
        db.session.commit()

        todo = Todo(
            task_content='Learn Flask-SQLAlchemy',
            is_completed=False,
            user_id=user.id
        )
        db.session.add(todo)
        db.session.commit()

    return f'''
    <h2>Database Test</h2>
    <p><b>User:</b> {user.username} (ID: {user.id})</p>
    <p><b>Email:</b> {user.email}</p>
    <p><b>Todos:</b> {len(user.todos)}</p>
    <p><a href="/">Back to Home</a></p>
    '''


if __name__ == '__main__':
    print("\n" + "="*40)
    print("Todo App - Part 1: Foundation")
    print("http://127.0.0.1:5000")
    print("="*40 + "\n")
    app.run(debug=True)
