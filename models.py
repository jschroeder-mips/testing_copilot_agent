"""Database models for the TODO application."""
from datetime import datetime
from typing import List, Optional
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """User model for authentication and todo ownership."""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationship with todos
    todos = db.relationship('Todo', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def __init__(self, username: str, email: str, password: str) -> None:
        """Initialize a new user."""
        self.username = username
        self.email = email
        self.set_password(password)
    
    def set_password(self, password: str) -> None:
        """Set password hash for the user."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password: str) -> bool:
        """Check if provided password matches the user's password."""
        return check_password_hash(self.password_hash, password)
    
    def get_todos(self) -> List['Todo']:
        """Get all todos for this user."""
        return self.todos.all()
    
    def get_completed_todos(self) -> List['Todo']:
        """Get completed todos for this user."""
        return self.todos.filter_by(completed=True).all()
    
    def get_pending_todos(self) -> List['Todo']:
        """Get pending todos for this user."""
        return self.todos.filter_by(completed=False).all()
    
    def __repr__(self) -> str:
        """String representation of the user."""
        return f'<User {self.username}>'


class Todo(db.Model):
    """Todo model for individual tasks."""
    
    __tablename__ = 'todos'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    priority = db.Column(db.String(20), default='medium')  # low, medium, high, critical
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=True)
    
    # Foreign key to users table
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __init__(self, title: str, user_id: int, description: str = '', priority: str = 'medium', due_date: Optional[datetime] = None) -> None:
        """Initialize a new todo."""
        self.title = title
        self.user_id = user_id
        self.description = description
        self.priority = priority
        self.due_date = due_date
    
    def toggle_completed(self) -> None:
        """Toggle the completed status of the todo."""
        self.completed = not self.completed
        self.updated_at = datetime.utcnow()
    
    def update(self, title: Optional[str] = None, description: Optional[str] = None, 
               priority: Optional[str] = None, due_date: Optional[datetime] = None) -> None:
        """Update todo fields."""
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        if priority is not None:
            self.priority = priority
        if due_date is not None:
            self.due_date = due_date
        self.updated_at = datetime.utcnow()
    
    def to_dict(self) -> dict:
        """Convert todo to dictionary for API responses."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'priority': self.priority,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'user_id': self.user_id
        }
    
    def __repr__(self) -> str:
        """String representation of the todo."""
        return f'<Todo {self.title} ({"✓" if self.completed else "✗"})>'