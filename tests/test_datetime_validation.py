"""Tests for datetime validation in TodoForm."""

import unittest
from datetime import datetime
from app import create_app, db
from app.models.user import User
from app.models.todo import Todo, TodoStatus, TodoPriority
from app.forms import TodoForm


class TodoFormDateTimeTestCase(unittest.TestCase):
    """Test case for TodoForm datetime validation."""
    
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
    
    def test_valid_datetime_format(self):
        """Test that valid datetime format is accepted."""
        with self.app.test_request_context():
            form = TodoForm(data={
                'title': 'Test TODO',
                'description': 'Test description',
                'status': 'pending',
                'priority': 'medium',
                'due_date': '2077-12-31 23:59'
            })
            
            self.assertTrue(form.validate(), f"Form validation failed: {form.errors}")
            self.assertIsInstance(form.due_date.data, datetime)
    
    def test_invalid_datetime_format(self):
        """Test that invalid datetime format is rejected."""
        with self.app.test_request_context():
            form = TodoForm(data={
                'title': 'Test TODO',
                'description': 'Test description',
                'status': 'pending',
                'priority': 'medium',
                'due_date': '31/12/2077 23:59'  # Wrong format
            })
            
            self.assertFalse(form.validate())
            self.assertIn('due_date', form.errors)
    
    def test_empty_datetime_is_valid(self):
        """Test that empty datetime is valid (optional field)."""
        with self.app.test_request_context():
            form = TodoForm(data={
                'title': 'Test TODO',
                'description': 'Test description',
                'status': 'pending',
                'priority': 'medium',
                'due_date': ''
            })
            
            self.assertTrue(form.validate(), f"Form validation failed: {form.errors}")
            self.assertIsNone(form.due_date.data)
    
    def test_form_submission_with_datetime(self):
        """Test actual form submission with datetime via HTTP request."""
        # First login
        with self.client.session_transaction() as sess:
            sess['_user_id'] = str(self.user.id)
            sess['_fresh'] = True
        
        # Submit form with datetime
        response = self.client.post('/todo/new', data={
            'title': 'Test TODO',
            'description': 'Test description',
            'status': 'pending',
            'priority': 'medium',
            'due_date': '2077-12-31 23:59',
            'submit': 'Save TODO'
        }, follow_redirects=False)
        
        # Should redirect on success, or stay on page with errors
        if response.status_code == 302:
            # Success - check if todo was created
            todo = Todo.query.filter_by(title='Test TODO').first()
            self.assertIsNotNone(todo)
            self.assertIsNotNone(todo.due_date)
        else:
            # Check if there are validation errors in response
            self.fail(f"Form submission failed with status {response.status_code}: {response.get_data(as_text=True)}")


if __name__ == '__main__':
    unittest.main()