"""Basic tests for the CyberTODO application."""

import unittest
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
        self.assertIn(b'CyberTODO 2077', response.data)
    
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


if __name__ == '__main__':
    unittest.main()