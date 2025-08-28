"""Todo model for task management."""

from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from app import db


def utc_now():
    """Return current UTC datetime for database defaults."""
    return datetime.now(timezone.utc)


class TodoStatus(Enum):
    """Enumeration for TODO item status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress" 
    COMPLETED = "completed"


class TodoPriority(Enum):
    """Enumeration for TODO item priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Todo(db.Model):
    """
    Todo model representing individual TODO items.
    
    Attributes:
        id: Primary key
        title: TODO item title
        description: Optional detailed description
        status: Current status (pending, in_progress, completed)
        priority: Priority level (low, medium, high, critical)
        created_at: Creation timestamp
        updated_at: Last modification timestamp
        due_date: Optional due date
        user_id: Foreign key to User who owns this TODO
    """
    
    __tablename__ = 'todos'
    
    id: int = db.Column(db.Integer, primary_key=True)
    title: str = db.Column(db.String(200), nullable=False)
    description: Optional[str] = db.Column(db.Text)
    status: str = db.Column(
        db.Enum(TodoStatus), 
        default=TodoStatus.PENDING, 
        nullable=False
    )
    priority: str = db.Column(
        db.Enum(TodoPriority), 
        default=TodoPriority.MEDIUM, 
        nullable=False
    )
    created_at: datetime = db.Column(db.DateTime, default=utc_now)
    updated_at: datetime = db.Column(
        db.DateTime, 
        default=utc_now, 
        onupdate=utc_now
    )
    due_date: Optional[datetime] = db.Column(db.DateTime)
    
    # Foreign key to User
    user_id: int = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def mark_completed(self) -> None:
        """Mark the TODO item as completed."""
        self.status = TodoStatus.COMPLETED
        self.updated_at = datetime.now(timezone.utc)
    
    def mark_in_progress(self) -> None:
        """Mark the TODO item as in progress."""
        self.status = TodoStatus.IN_PROGRESS
        self.updated_at = datetime.now(timezone.utc)
    
    def mark_pending(self) -> None:
        """Mark the TODO item as pending."""
        self.status = TodoStatus.PENDING
        self.updated_at = datetime.now(timezone.utc)
    
    @property
    def is_overdue(self) -> bool:
        """
        Check if the TODO item is overdue.
        
        Returns:
            True if due date has passed and item is not completed
        """
        if self.due_date and self.status != TodoStatus.COMPLETED:
            return datetime.now(timezone.utc) > self.due_date
        return False
    
    def to_dict(self) -> dict:
        """
        Convert TODO object to dictionary for API responses.
        
        Returns:
            Dictionary representation of TODO item
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status.value if isinstance(self.status, TodoStatus) else self.status,
            'priority': self.priority.value if isinstance(self.priority, TodoPriority) else self.priority,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'user_id': self.user_id,
            'is_overdue': self.is_overdue
        }
    
    def __repr__(self) -> str:
        """String representation of Todo object."""
        return f'<Todo {self.title}>'