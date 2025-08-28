#!/usr/bin/env python3
"""Test script to simulate the exact dashboard scenario that was failing"""

import sys
import os
import unittest

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from datetime import datetime, timezone
from app import create_app, db
from app.models.user import User
from app.models.todo import Todo, TodoStatus, TodoPriority

class DashboardScenarioTest(unittest.TestCase):
    """Test the exact scenario from the dashboard that was causing the error"""
    
    def setUp(self):
        """Set up test fixtures."""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()
        
        # Create a test user
        self.user = User(username='testuser', email='test@example.com')
        self.user.set_password('testpass')
        db.session.add(self.user)
        db.session.commit()
    
    def tearDown(self):
        """Clean up after tests."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_dashboard_overdue_calculation(self):
        """Test the exact line from main.py that was failing:
        'overdue': len([t for t in current_user.todos if t.is_overdue])
        """
        
        # Create some todos with different scenarios
        todos = [
            Todo(
                title='Past due naive',
                status=TodoStatus.PENDING,
                due_date=datetime(2023, 1, 1, 12, 0, 0),  # Past, naive
                user_id=self.user.id
            ),
            Todo(
                title='Past due aware',
                status=TodoStatus.PENDING,
                due_date=datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc),  # Past, aware
                user_id=self.user.id
            ),
            Todo(
                title='Future due',
                status=TodoStatus.PENDING,
                due_date=datetime(2030, 12, 31, 23, 59, 59),  # Future
                user_id=self.user.id
            ),
            Todo(
                title='No due date',
                status=TodoStatus.PENDING,
                due_date=None,
                user_id=self.user.id
            ),
            Todo(
                title='Completed past due',
                status=TodoStatus.COMPLETED,
                due_date=datetime(2023, 1, 1, 12, 0, 0),  # Past but completed
                user_id=self.user.id
            ),
        ]
        
        for todo in todos:
            db.session.add(todo)
        db.session.commit()
        
        # This is the exact line that was failing in main.py line 59
        try:
            overdue_count = len([t for t in self.user.todos if t.is_overdue])
            
            # We expect 2 overdue todos (the past due ones that are pending)
            self.assertEqual(overdue_count, 2)
            print(f"✓ Dashboard overdue calculation successful: {overdue_count} overdue todos")
            
        except TypeError as e:
            self.fail(f"Dashboard overdue calculation failed with TypeError: {e}")
    
    def test_dashboard_stats_dict(self):
        """Test the complete stats calculation from the dashboard"""
        
        # Create some test todos
        todos = [
            Todo(title='Todo1', status=TodoStatus.PENDING, user_id=self.user.id),
            Todo(title='Todo2', status=TodoStatus.IN_PROGRESS, user_id=self.user.id),
            Todo(title='Todo3', status=TodoStatus.COMPLETED, user_id=self.user.id),
            Todo(title='Todo4', status=TodoStatus.PENDING, 
                 due_date=datetime(2023, 1, 1, 12, 0, 0), user_id=self.user.id),  # Overdue
        ]
        
        for todo in todos:
            db.session.add(todo)
        db.session.commit()
        
        # Simulate the stats calculation from main.py lines 54-60
        try:
            stats = {
                'total': self.user.todos.count(),
                'pending': self.user.todos.filter(Todo.status == TodoStatus.PENDING).count(),
                'in_progress': self.user.todos.filter(Todo.status == TodoStatus.IN_PROGRESS).count(),
                'completed': self.user.todos.filter(Todo.status == TodoStatus.COMPLETED).count(),
                'overdue': len([t for t in self.user.todos if t.is_overdue])
            }
            
            expected_stats = {
                'total': 4,
                'pending': 2,
                'in_progress': 1,
                'completed': 1,
                'overdue': 1
            }
            
            self.assertEqual(stats, expected_stats)
            print(f"✓ Complete dashboard stats calculation successful: {stats}")
            
        except Exception as e:
            self.fail(f"Dashboard stats calculation failed: {e}")

if __name__ == "__main__":
    unittest.main()