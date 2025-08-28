"""Main application routes."""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.todo import Todo, TodoStatus, TodoPriority
from app.forms import TodoForm

main = Blueprint('main', __name__)


@main.route('/')
def index():
    """
    Home page route.
    
    Returns:
        Rendered template for home page or redirect to dashboard if logged in
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')


@main.route('/dashboard')
@login_required
def dashboard():
    """
    User dashboard displaying TODO items.
    
    Returns:
        Rendered dashboard template with user's TODO items
    """
    # Get filter parameters
    status_filter = request.args.get('status', 'all')
    priority_filter = request.args.get('priority', 'all')
    
    # Build query
    query = current_user.todos
    
    if status_filter != 'all':
        query = query.filter(Todo.status == status_filter)
    
    if priority_filter != 'all':
        query = query.filter(Todo.priority == priority_filter)
    
    # Order by priority and creation date
    todos = query.order_by(
        Todo.priority.desc(),
        Todo.created_at.desc()
    ).all()
    
    # Get statistics
    stats = {
        'total': current_user.todos.count(),
        'pending': current_user.todos.filter(Todo.status == TodoStatus.PENDING).count(),
        'in_progress': current_user.todos.filter(Todo.status == TodoStatus.IN_PROGRESS).count(),
        'completed': current_user.todos.filter(Todo.status == TodoStatus.COMPLETED).count(),
        'overdue': len([t for t in current_user.todos if t.is_overdue])
    }
    
    return render_template(
        'dashboard.html', 
        todos=todos, 
        stats=stats,
        current_status=status_filter,
        current_priority=priority_filter,
        TodoStatus=TodoStatus,
        TodoPriority=TodoPriority
    )


@main.route('/todo/new', methods=['GET', 'POST'])
@login_required
def new_todo():
    """
    Create a new TODO item.
    
    Returns:
        Rendered form template or redirect to dashboard on success
    """
    form = TodoForm()
    
    if form.validate_on_submit():
        todo = Todo(
            title=form.title.data,
            description=form.description.data,
            status=TodoStatus(form.status.data),
            priority=TodoPriority(form.priority.data),
            due_date=form.due_date.data,
            user_id=current_user.id
        )
        
        db.session.add(todo)
        db.session.commit()
        
        flash('TODO item created successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    
    return render_template('todo_form.html', form=form, title='New TODO')


@main.route('/todo/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_todo(id: int):
    """
    Edit an existing TODO item.
    
    Args:
        id: TODO item ID
        
    Returns:
        Rendered form template or redirect to dashboard on success
    """
    todo = Todo.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    form = TodoForm(obj=todo)
    
    if form.validate_on_submit():
        todo.title = form.title.data
        todo.description = form.description.data
        todo.status = TodoStatus(form.status.data)
        todo.priority = TodoPriority(form.priority.data)
        todo.due_date = form.due_date.data
        
        db.session.commit()
        
        flash('TODO item updated successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    
    return render_template('todo_form.html', form=form, title='Edit TODO', todo=todo)


@main.route('/todo/<int:id>/delete', methods=['POST'])
@login_required
def delete_todo(id: int):
    """
    Delete a TODO item.
    
    Args:
        id: TODO item ID
        
    Returns:
        Redirect to dashboard
    """
    todo = Todo.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    
    db.session.delete(todo)
    db.session.commit()
    
    flash('TODO item deleted successfully!', 'success')
    return redirect(url_for('main.dashboard'))


@main.route('/todo/<int:id>/toggle', methods=['POST'])
@login_required
def toggle_todo(id: int):
    """
    Toggle TODO item status between pending and completed.
    
    Args:
        id: TODO item ID
        
    Returns:
        Redirect to dashboard
    """
    todo = Todo.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    
    if todo.status == TodoStatus.COMPLETED:
        todo.mark_pending()
    else:
        todo.mark_completed()
    
    db.session.commit()
    
    flash('TODO status updated!', 'success')
    return redirect(url_for('main.dashboard'))