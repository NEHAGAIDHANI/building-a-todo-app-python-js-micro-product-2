# app.py - Part 2: Authentication

from flask import Flask, render_template, request, jsonify
from models import db, init_db, User
from auth import hash_password, verify_password, create_token

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'

init_db(app)


# Page Routes
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register')
def register_page():
    return render_template('register.html')


@app.route('/login')
def login_page():
    return render_template('login.html')


# API Routes
@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    username, email, password = data.get('username'), data.get('email'), data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'All fields are required'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already taken'}), 400

    new_user = User(username=username, email=email, password_hash=hash_password(password), is_admin=False)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201


@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    email, password = data.get('email'), data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not verify_password(user.password_hash, password):
        return jsonify({'error': 'Invalid credentials'}), 401

    token = create_token(user.id, user.is_admin)
    return jsonify({'token': token, 'user': user.to_dict()}), 200


@app.route('/api/create-admin', methods=['POST'])
def create_admin():
    if User.query.filter_by(email='admin@example.com').first():
        return jsonify({'message': 'Admin exists', 'email': 'admin@example.com'}), 200

    admin = User(username='admin', email='admin@example.com', password_hash=hash_password('admin123'), is_admin=True)
    db.session.add(admin)
    db.session.commit()

    return jsonify({'message': 'Admin created', 'email': 'admin@example.com', 'password': 'admin123'}), 201


if __name__ == '__main__':
    print("\n" + "="*40)
    print("Todo App - Part 2: Authentication")
    print("http://127.0.0.1:5000")
    print("="*40 + "\n")
    app.run(debug=True)
