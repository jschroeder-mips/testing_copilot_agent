"""Database interface for the MCP Server to interact with CyberTODO data."""

from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
import sys
import os

# Add the parent directory to sys.path to import from the main app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.todo import Todo, TodoStatus, TodoPriority
from app.models.user import User
from app import db
from .config import MCPConfig


class DatabaseManager:
    """Manages database connections and operations for the MCP server."""
    
    def __init__(self, use_flask_db=False):
        """Initialize the database manager.
        
        Args:
            use_flask_db: If True, use the Flask app's database session
        """
        self.use_flask_db = use_flask_db
        if not use_flask_db:
            self.database_uri = MCPConfig.get_database_uri()
            self.engine = create_engine(self.database_uri)
            self.SessionLocal = sessionmaker(bind=self.engine)
    
    @contextmanager
    def get_session(self) -> Session:
        """Get a database session with proper cleanup.
        
        Yields:
            Database session
        """
        if self.use_flask_db:
            # Use Flask app's database session
            yield db.session
        else:
            session = self.SessionLocal()
            try:
                yield session
                session.commit()
            except Exception:
                session.rollback()
                raise
            finally:
                session.close()
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get a user by ID.
        
        Args:
            user_id: The user ID
            
        Returns:
            User data as dictionary, or None if not found
        """
        with self.get_session() as session:
            user = session.query(User).filter(User.id == user_id).first()
            if user:
                return user.to_dict()
            return None
    
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Get a user by username.
        
        Args:
            username: The username
            
        Returns:
            User data as dictionary, or None if not found
        """
        with self.get_session() as session:
            user = session.query(User).filter(User.username == username).first()
            if user:
                return user.to_dict()
            return None
    
    def list_todos(self, user_id: Optional[int] = None, status: Optional[str] = None, 
                   priority: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """List todos with optional filtering.
        
        Args:
            user_id: Filter by user ID (None for system-wide access)
            status: Filter by status
            priority: Filter by priority  
            limit: Maximum number of todos to return
            
        Returns:
            List of todo dictionaries
        """
        with self.get_session() as session:
            query = session.query(Todo)
            
            if user_id is not None:
                query = query.filter(Todo.user_id == user_id)
            
            if status:
                try:
                    status_enum = TodoStatus(status)
                    query = query.filter(Todo.status == status_enum)
                except ValueError:
                    return []  # Invalid status
            
            if priority:
                try:
                    priority_enum = TodoPriority(priority)
                    query = query.filter(Todo.priority == priority_enum)
                except ValueError:
                    return []  # Invalid priority
            
            todos = query.order_by(Todo.created_at.desc()).limit(limit).all()
            return [todo.to_dict() for todo in todos]
    
    def get_todo_by_id(self, todo_id: int, user_id: Optional[int] = None) -> Optional[Dict[str, Any]]:
        """Get a specific todo by ID.
        
        Args:
            todo_id: The todo ID
            user_id: Optional user ID for ownership check
            
        Returns:
            Todo data as dictionary, or None if not found
        """
        with self.get_session() as session:
            query = session.query(Todo).filter(Todo.id == todo_id)
            
            if user_id is not None:
                query = query.filter(Todo.user_id == user_id)
            
            todo = query.first()
            if todo:
                return todo.to_dict()
            return None
    
    def create_todo(self, title: str, description: Optional[str] = None, 
                    status: str = "pending", priority: str = "medium",
                    due_date: Optional[str] = None, user_id: int = None) -> Dict[str, Any]:
        """Create a new todo.
        
        Args:
            title: Todo title
            description: Optional description
            status: Todo status
            priority: Todo priority
            due_date: Optional due date (ISO format string)
            user_id: User ID who owns the todo
            
        Returns:
            Created todo data as dictionary
            
        Raises:
            ValueError: If required data is missing or invalid
        """
        if not title or not title.strip():
            raise ValueError("Title is required")
        
        if user_id is None:
            raise ValueError("User ID is required")
        
        try:
            status_enum = TodoStatus(status)
            priority_enum = TodoPriority(priority)
        except ValueError as e:
            raise ValueError(f"Invalid status or priority: {e}")
        
        with self.get_session() as session:
            # Verify user exists
            user = session.query(User).filter(User.id == user_id).first()
            if not user:
                raise ValueError(f"User with ID {user_id} not found")
            
            todo = Todo(
                title=title.strip(),
                description=description.strip() if description else None,
                status=status_enum,
                priority=priority_enum,
                user_id=user_id
            )
            
            if due_date:
                try:
                    todo.due_date = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
                except ValueError:
                    raise ValueError('Invalid due_date format. Use ISO format.')
            
            session.add(todo)
            session.flush()  # Get the ID
            session.refresh(todo)
            
            return todo.to_dict()
    
    def update_todo(self, todo_id: int, user_id: Optional[int] = None, 
                    title: Optional[str] = None, description: Optional[str] = None,
                    status: Optional[str] = None, priority: Optional[str] = None,
                    due_date: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Update an existing todo.
        
        Args:
            todo_id: The todo ID
            user_id: Optional user ID for ownership check
            title: New title
            description: New description
            status: New status
            priority: New priority
            due_date: New due date (ISO format string)
            
        Returns:
            Updated todo data as dictionary, or None if not found
            
        Raises:
            ValueError: If invalid data is provided
        """
        with self.get_session() as session:
            query = session.query(Todo).filter(Todo.id == todo_id)
            
            if user_id is not None:
                query = query.filter(Todo.user_id == user_id)
            
            todo = query.first()
            if not todo:
                return None
            
            # Update fields if provided
            if title is not None:
                if not title.strip():
                    raise ValueError("Title cannot be empty")
                todo.title = title.strip()
            
            if description is not None:
                todo.description = description.strip() if description else None
            
            if status is not None:
                try:
                    todo.status = TodoStatus(status)
                except ValueError:
                    raise ValueError(f"Invalid status: {status}")
            
            if priority is not None:
                try:
                    todo.priority = TodoPriority(priority)
                except ValueError:
                    raise ValueError(f"Invalid priority: {priority}")
            
            if due_date is not None:
                if due_date == "":
                    todo.due_date = None
                else:
                    try:
                        todo.due_date = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
                    except ValueError:
                        raise ValueError('Invalid due_date format. Use ISO format.')
            
            todo.updated_at = datetime.now(timezone.utc)
            session.flush()
            session.refresh(todo)
            
            return todo.to_dict()
    
    def delete_todo(self, todo_id: int, user_id: Optional[int] = None) -> bool:
        """Delete a todo.
        
        Args:
            todo_id: The todo ID
            user_id: Optional user ID for ownership check
            
        Returns:
            True if deleted, False if not found
        """
        with self.get_session() as session:
            query = session.query(Todo).filter(Todo.id == todo_id)
            
            if user_id is not None:
                query = query.filter(Todo.user_id == user_id)
            
            todo = query.first()
            if todo:
                session.delete(todo)
                return True
            return False


# Global database manager instance
db_manager = DatabaseManager()