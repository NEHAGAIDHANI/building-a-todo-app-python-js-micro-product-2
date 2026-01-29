# Part 1: Foundation - Project Setup & Database Models

## 🎯 Learning Objectives
By the end of this part, you will understand:
- How to set up a Flask project structure
- How to create database models using Flask-SQLAlchemy
- How to define a **One-to-Many** relationship between tables
- How to create basic HTML templates with Bootstrap

---

## 📁 Project Structure
```
part-1-foundation/
├── app.py              # Main Flask application
├── models.py           # Database models (User & Todo)
├── templates/
│   └── index.html      # Home page with Bootstrap
└── requirements.txt    # Python dependencies
```

---

## 🗄️ Database Design

### User Table
| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary Key |
| username | String(80) | Unique username |
| email | String(120) | Unique email |
| password_hash | String(256) | Hashed password |
| is_admin | Boolean | Admin flag (default: False) |

### Todo Table
| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary Key |
| task_content | String(200) | The task text |
| is_completed | Boolean | Completion status |
| user_id | Integer | Foreign Key → User.id |

### Relationship
```
One User → Many Todos (One-to-Many)
```

---

## 🚀 Step-by-Step Instructions

### Step 1: Install Dependencies
```bash
pip install flask flask-sqlalchemy
```

### Step 2: Understand the Models (models.py)
Open `models.py` and study:
- How `db.Model` creates a table
- How `db.relationship()` links User to Todos
- How `db.ForeignKey()` creates the connection

### Step 3: Run the Application
```bash
python app.py
```

### Step 4: Visit the App
Open your browser and go to: `http://127.0.0.1:5000`

---

## 📝 Key Concepts Explained

### What is SQLAlchemy?
SQLAlchemy is an ORM (Object-Relational Mapper) that lets you work with databases using Python classes instead of raw SQL.

### What is a Foreign Key?
A Foreign Key creates a link between two tables. In our case, `user_id` in the Todo table points to `id` in the User table.

### What is a Relationship?
```python
todos = db.relationship('Todo', backref='owner', lazy=True)
```
This allows you to access all todos of a user like this: `user.todos`

---

## ✅ Practice Exercise
1. Open `models.py` and add a new column `created_at` to the Todo model
2. Hint: Use `db.Column(db.DateTime, default=datetime.utcnow)`
3. Delete `todo.db` and restart the app to see the change

---

## 📚 What's Next?
In **Part 2**, we will add:
- User Registration API
- User Login API with JWT tokens
- Frontend forms for login/register
