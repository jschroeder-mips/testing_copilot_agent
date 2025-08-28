"""User model for authentication and user management."""

from datetime import datetime, timezone
from typing import List
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


def utc_now():
    """Return current UTC datetime for database defaults."""
    return datetime.now(timezone.utc)


class User(UserMixin, db.Model):
    """
    User model for authentication and TODO list ownership.
    
    Attributes:
        id: Primary key
        username: Unique username for login
        email: User's email address
        password_hash: Hashed password for security
        created_at: Account creation timestamp
        todos: Relationship to user's TODO items
    """
    
    __tablename__ = 'users'
    
    id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email: str = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash: str = db.Column(db.String(256), nullable=False)
    created_at: datetime = db.Column(db.DateTime, default=utc_now)
    
    # Relationship to TODO items
    todos = db.relationship('Todo', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def set_password(self, password: str) -> None:
        """
        Set user password with secure hashing.
        
        Args:
            password: Plain text password to hash and store
        """
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password: str) -> bool:
        """
        Check if provided password matches stored hash.
        
        Args:
            password: Plain text password to verify
            
        Returns:
            True if password matches, False otherwise
        """
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self) -> dict:
        """
        Convert user object to dictionary for API responses.
        
        Returns:
            Dictionary representation of user (excluding sensitive data)
        """
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'todo_count': self.todos.count()
        }
    
    def __repr__(self) -> str:
        """String representation of User object."""
        return f'<User {self.username}>'