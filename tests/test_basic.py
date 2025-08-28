"""Basic tests for the CyberTODO application."""

import unittest
from datetime import datetime, timezone
from app import create_app, db
from app.models.user import User
from app.models.todo import Todo, TodoStatus, TodoPriority


class CyberTODOTestCase(unittest.TestCase):
    """Test case for CyberTODO application."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()
    
    def tearDown(self):
        """Clean up after tests."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_app_exists(self):
        """Test that the app exists."""
        self.assertIsNotNone(self.app)
    
    def test_app_is_testing(self):
        """Test that the app is in testing mode."""
        self.assertTrue(self.app.config['TESTING'])
    
    def test_home_page(self):
        """Test home page loads."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Calcifer\'s Tasks', response.data)
    
    def test_user_model(self):
        """Test User model functionality."""
        user = User(username='testuser', email='test@example.com')
        user.set_password('testpass')
        db.session.add(user)
        db.session.commit()
        
        # Test password checking
        self.assertTrue(user.check_password('testpass'))
        self.assertFalse(user.check_password('wrongpass'))
        
        # Test user representation
        self.assertEqual(str(user), '<User testuser>')
    
    def test_todo_model(self):
        """Test Todo model functionality."""
        user = User(username='testuser', email='test@example.com')
        user.set_password('testpass')
        db.session.add(user)
        db.session.commit()
        
        todo = Todo(
            title='Test TODO',
            description='Test description',
            status=TodoStatus.PENDING,
            priority=TodoPriority.HIGH,
            user_id=user.id
        )
        db.session.add(todo)
        db.session.commit()
        
        # Test todo representation
        self.assertEqual(str(todo), '<Todo Test TODO>')
        
        # Test status changes
        todo.mark_completed()
        self.assertEqual(todo.status, TodoStatus.COMPLETED)
        
        todo.mark_in_progress()
        self.assertEqual(todo.status, TodoStatus.IN_PROGRESS)
    
    def test_api_docs_endpoint(self):
        """Test that API documentation is accessible."""
        response = self.client.get('/api/docs/')
        self.assertEqual(response.status_code, 200)
    
    def test_timezone_comparison_fix(self):
        """Test that timezone comparison issue is fixed in is_overdue property."""
        user = User(username='testuser', email='test@example.com')
        user.set_password('testpass')
        db.session.add(user)
        db.session.commit()
        
        # Test with offset-naive due_date (typical case from form input)
        todo_naive = Todo(
            title='Test TODO with naive date',
            status=TodoStatus.PENDING,
            due_date=datetime(2023, 1, 1, 12, 0, 0),  # Past date, offset-naive
            user_id=user.id
        )
        db.session.add(todo_naive)
        
        # Test with offset-aware due_date
        todo_aware = Todo(
            title='Test TODO with aware date',
            status=TodoStatus.PENDING,
            due_date=datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc),  # Past date, offset-aware
            user_id=user.id
        )
        db.session.add(todo_aware)
        db.session.commit()
        
        # Both should work without TypeError and return True (overdue)
        self.assertTrue(todo_naive.is_overdue)
        self.assertTrue(todo_aware.is_overdue)
        
        # Test future dates are not overdue
        todo_future = Todo(
            title='Test TODO future',
            status=TodoStatus.PENDING,
            due_date=datetime(2030, 12, 31, 23, 59, 59),  # Future date, offset-naive
            user_id=user.id
        )
        db.session.add(todo_future)
        db.session.commit()
        
        self.assertFalse(todo_future.is_overdue)
        
        # Test completed todos are not overdue even with past due_date
        todo_completed = Todo(
            title='Test TODO completed',
            status=TodoStatus.COMPLETED,
            due_date=datetime(2023, 1, 1, 12, 0, 0),  # Past date
            user_id=user.id
        )
        db.session.add(todo_completed)
        db.session.commit()
        
        self.assertFalse(todo_completed.is_overdue)


if __name__ == '__main__':
    unittest.main()