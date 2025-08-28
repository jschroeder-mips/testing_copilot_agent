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
        from werkzeug.datastructures import MultiDict
        
        with self.app.test_request_context():
            formdata = MultiDict([
                ('title', 'Test TODO'),
                ('description', 'Test description'),
                ('status', 'pending'),
                ('priority', 'medium'),
                ('due_date', '2077-12-31 23:59')
            ])
            form = TodoForm(formdata=formdata)
            
            self.assertTrue(form.validate(), f"Form validation failed: {form.errors}")
            self.assertIsInstance(form.due_date.data, datetime)
    
    def test_invalid_datetime_format(self):
        """Test that invalid datetime format is rejected."""
        from werkzeug.datastructures import MultiDict
        
        with self.app.test_request_context():
            formdata = MultiDict([
                ('title', 'Test TODO'),
                ('description', 'Test description'),
                ('status', 'pending'),
                ('priority', 'medium'),
                ('due_date', '31/12/2077 23:59')  # Wrong format
            ])
            form = TodoForm(formdata=formdata)
            
            self.assertFalse(form.validate())
            self.assertIn('due_date', form.errors)
    
    def test_empty_datetime_is_valid(self):
        """Test that empty datetime is valid (optional field)."""
        from werkzeug.datastructures import MultiDict
        
        with self.app.test_request_context():
            formdata = MultiDict([
                ('title', 'Test TODO'),
                ('description', 'Test description'),
                ('status', 'pending'),
                ('priority', 'medium'),
                ('due_date', '')
            ])
            form = TodoForm(formdata=formdata)
            
            self.assertTrue(form.validate(), f"Form validation failed: {form.errors}")
            self.assertIsNone(form.due_date.data)
    
    def test_issue_reproduction_not_valid_datetime_value(self):
        """
        Test that reproduces the original issue: 'Not a valid datetime value.'
        
        This test demonstrates that the FlexibleDateTimeField fix resolves the issue
        where datetime-local input sends ISO format (with T) but server expected space format.
        """
        from werkzeug.datastructures import MultiDict
        
        with self.app.test_request_context():
            # Before the fix, this would produce "Not a valid datetime value" error
            # because datetime-local inputs send '2077-12-31T23:59' but the original
            # DateTimeField expected '2077-12-31 23:59'
            formdata = MultiDict([
                ('title', 'Test TODO'),
                ('description', 'Testing datetime validation fix'),
                ('status', 'pending'),
                ('priority', 'medium'),
                ('due_date', '2077-12-31T23:59')  # ISO format from datetime-local
            ])
            form = TodoForm(formdata=formdata)
            
            # With our FlexibleDateTimeField, this should now validate successfully
            self.assertTrue(form.validate(), 
                          f"Expected form to validate but got errors: {form.errors}")
            
            # The datetime should be properly parsed
            self.assertIsInstance(form.due_date.data, datetime)
            
            # Values should be correct
            self.assertEqual(form.due_date.data.year, 2077)
            self.assertEqual(form.due_date.data.month, 12)
            self.assertEqual(form.due_date.data.day, 31)
            self.assertEqual(form.due_date.data.hour, 23)
            self.assertEqual(form.due_date.data.minute, 59)

    def test_datetime_local_format_from_browser(self):
        """Test datetime-local format from browser (ISO format with T separator)."""
        from werkzeug.datastructures import MultiDict
        
        with self.app.test_request_context():
            # This is what datetime-local input sends
            formdata = MultiDict([
                ('title', 'Test TODO'),
                ('description', 'Test description'),
                ('status', 'pending'),
                ('priority', 'medium'),
                ('due_date', '2077-12-31T23:59')  # datetime-local format
            ])
            form = TodoForm(formdata=formdata)
            
            # This should now pass with our fix
            self.assertTrue(form.validate(), f"Form validation failed: {form.errors}")
            self.assertIsInstance(form.due_date.data, datetime)
            self.assertEqual(form.due_date.data.year, 2077)
            self.assertEqual(form.due_date.data.month, 12)
            self.assertEqual(form.due_date.data.day, 31)
            self.assertEqual(form.due_date.data.hour, 23)
            self.assertEqual(form.due_date.data.minute, 59)
    
    def test_form_submission_with_datetime_local_input(self):
        """Test form submission specifically with datetime-local format that was causing issues."""
        # First login using session
        with self.client.session_transaction() as sess:
            sess['_user_id'] = str(self.user.id)
            sess['_fresh'] = True
        
        # Submit form with datetime-local format (what browsers send)
        response = self.client.post('/todo/new', data={
            'title': 'Test TODO with Datetime',
            'description': 'Testing the datetime fix',
            'status': 'pending',
            'priority': 'medium',
            'due_date': '2077-12-31T23:59',  # datetime-local format with T separator
            'submit': 'Save TODO'
        }, follow_redirects=False)
        
        # Should redirect on success (status 302)
        self.assertEqual(response.status_code, 302)
        
        # Check if todo was created successfully
        todo = Todo.query.filter_by(title='Test TODO with Datetime').first()
        self.assertIsNotNone(todo, "Todo should have been created")
        self.assertIsNotNone(todo.due_date, "Due date should be set")
        self.assertEqual(todo.due_date.year, 2077)
        self.assertEqual(todo.due_date.month, 12)
        self.assertEqual(todo.due_date.day, 31)
        self.assertEqual(todo.due_date.hour, 23)
        self.assertEqual(todo.due_date.minute, 59)

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