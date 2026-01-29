# Part 5: Homework - Build a Priority Feature

## 🎯 Assignment Overview

Congratulations on completing the Todo App module! Now it's time to apply everything you've learned by adding a new feature: **Task Priority Levels**.

---

## 📋 The Challenge

Add a **priority system** to the Todo application. Each task should have a priority level that affects how it's displayed and sorted.

### Requirements

1. **Database Change**
   - Add a `priority` column to the Todo model
   - Priority levels: `low`, `medium`, `high` (default: `medium`)

2. **API Changes**
   - Update `POST /api/todos` to accept a `priority` field
   - Update `PUT /api/todos/<id>` to allow changing priority
   - Todos should be returned sorted by priority (high → medium → low)

3. **Frontend Changes**
   - Add a priority dropdown when creating a task
   - Display priority as a colored badge next to each task:
     - High: Red badge
     - Medium: Yellow badge
     - Low: Green badge
   - Add a filter to show only tasks of a specific priority

4. **Admin Panel Update**
   - Show priority in the global todos table
   - Add a summary: "High: X, Medium: Y, Low: Z"

---

## 🚀 Getting Started

### Step 1: Copy the Starter Code
The `starter-code/` folder contains a working copy of Part 4. Start from there.

```bash
cd starter-code
pip install -r requirements.txt
python app.py
```

### Step 2: Make Database Changes
Open `models.py` and add the priority column:

```python
# Hint: Add this to the Todo model
priority = db.Column(db.String(10), default='medium')
```

### Step 3: Delete the Old Database
After changing the model, delete `todo.db` to recreate it:

```bash
# Windows
del todo.db

# Mac/Linux
rm todo.db
```

### Step 4: Update the API
Modify `app.py` to handle the priority field in create and update routes.

### Step 5: Update the Frontend
Modify `dashboard.html` to:
- Add a priority selector
- Display priority badges
- Sort/filter by priority

---

## ✅ Acceptance Criteria

Your solution should:

- [ ] Allow setting priority when creating a task
- [ ] Display priority as a colored badge (red/yellow/green)
- [ ] Allow changing priority of existing tasks
- [ ] Sort todos by priority (high first)
- [ ] Show priority information in admin panel
- [ ] Not break any existing functionality

---

## 💡 Hints

### Database Hint
```python
class Todo(db.Model):
    # ... existing columns ...
    priority = db.Column(db.String(10), default='medium')

    def to_dict(self):
        return {
            'id': self.id,
            'task_content': self.task_content,
            'is_completed': self.is_completed,
            'user_id': self.user_id,
            'priority': self.priority  # Add this
        }
```

### API Hint (Create Todo)
```python
@app.route('/api/todos', methods=['POST'])
@token_required
def create_todo(current_user):
    data = request.get_json()
    # ...
    new_todo = Todo(
        task_content=data['task_content'],
        is_completed=False,
        user_id=current_user.id,
        priority=data.get('priority', 'medium')  # Add this
    )
```

### Sorting Hint
```python
# Sort by priority (custom order)
priority_order = {'high': 1, 'medium': 2, 'low': 3}

todos = Todo.query.filter_by(user_id=current_user.id).all()
todos.sort(key=lambda t: priority_order.get(t.priority, 2))
```

### Frontend Hint (Priority Badge)
```javascript
function getPriorityBadge(priority) {
    const colors = {
        'high': 'bg-danger',
        'medium': 'bg-warning text-dark',
        'low': 'bg-success'
    };
    return `<span class="badge ${colors[priority] || 'bg-secondary'}">${priority}</span>`;
}
```

### Frontend Hint (Priority Selector)
```html
<select class="form-select" id="new-priority" style="width: 120px;">
    <option value="low">Low</option>
    <option value="medium" selected>Medium</option>
    <option value="high">High</option>
</select>
```

---

## 🏆 Bonus Challenges (Optional)

1. **Due Dates**: Add a `due_date` field and highlight overdue tasks
2. **Categories**: Add task categories/tags
3. **Search**: Add a search box to find tasks by content
4. **Bulk Actions**: Add "Mark all as complete" or "Delete completed"

---

## 📚 Skills Practiced

By completing this homework, you will have practiced:

| Skill | Where Used |
|-------|------------|
| Database Modeling | Adding new column |
| API Development | Modifying endpoints |
| JWT Authentication | Protected routes |
| Frontend JS | Dynamic UI updates |
| Conditional Rendering | Priority badges |
| Sorting/Filtering | Priority ordering |

---

## 📝 Submission

When complete, your todo app should:
1. Accept priority when creating tasks
2. Display visual priority indicators
3. Sort tasks by priority
4. Show priority in admin panel

Good luck! 🚀
