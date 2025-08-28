#!/usr/bin/env python3
"""Test script to verify the timezone fix works correctly"""

import sys
import os
import unittest

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from datetime import datetime, timezone
from app.models.todo import Todo, TodoStatus, TodoPriority

class TestTimezoneFix(unittest.TestCase):
    """Test cases for the timezone fix in Todo.is_overdue property"""
    
    def test_offset_naive_past_date(self):
        """Test that offset-naive past due_date is considered overdue"""
        todo = Todo()
        todo.due_date = datetime(2023, 1, 1, 12, 0, 0)  # Past date, offset-naive
        todo.status = TodoStatus.PENDING
        
        # Should be overdue (no TypeError should occur)
        self.assertTrue(todo.is_overdue)
    
    def test_offset_naive_future_date(self):
        """Test that offset-naive future due_date is not considered overdue"""
        todo = Todo()
        todo.due_date = datetime(2030, 12, 31, 23, 59, 59)  # Future date, offset-naive
        todo.status = TodoStatus.PENDING
        
        # Should not be overdue
        self.assertFalse(todo.is_overdue)
    
    def test_offset_aware_past_date(self):
        """Test that offset-aware past due_date is considered overdue"""
        todo = Todo()
        todo.due_date = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)  # Past date, offset-aware
        todo.status = TodoStatus.PENDING
        
        # Should be overdue
        self.assertTrue(todo.is_overdue)
    
    def test_offset_aware_future_date(self):
        """Test that offset-aware future due_date is not considered overdue"""
        todo = Todo()
        todo.due_date = datetime(2030, 12, 31, 23, 59, 59, tzinfo=timezone.utc)  # Future date, offset-aware
        todo.status = TodoStatus.PENDING
        
        # Should not be overdue
        self.assertFalse(todo.is_overdue)
    
    def test_completed_todo_not_overdue(self):
        """Test that completed todos are never considered overdue"""
        todo = Todo()
        todo.due_date = datetime(2023, 1, 1, 12, 0, 0)  # Past date
        todo.status = TodoStatus.COMPLETED
        
        # Should not be overdue even with past due date
        self.assertFalse(todo.is_overdue)
    
    def test_no_due_date_not_overdue(self):
        """Test that todos without due_date are not considered overdue"""
        todo = Todo()
        todo.due_date = None
        todo.status = TodoStatus.PENDING
        
        # Should not be overdue
        self.assertFalse(todo.is_overdue)
    
    def test_in_progress_todo_can_be_overdue(self):
        """Test that in-progress todos can be overdue"""
        todo = Todo()
        todo.due_date = datetime(2023, 1, 1, 12, 0, 0)  # Past date
        todo.status = TodoStatus.IN_PROGRESS
        
        # Should be overdue
        self.assertTrue(todo.is_overdue)

if __name__ == "__main__":
    unittest.main()