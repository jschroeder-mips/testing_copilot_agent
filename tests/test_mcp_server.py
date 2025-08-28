"""Tests for the CyberTODO MCP Server."""

import unittest
import os
import sys
import tempfile
import json
from unittest.mock import patch

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from app import create_app, db
from app.models.user import User
from app.models.todo import Todo, TodoStatus, TodoPriority
from mcp_server.auth import APIKeyManager
from mcp_server.database import DatabaseManager
from mcp_server.config import MCPConfig


class MCPServerTestCase(unittest.TestCase):
    """Test case for MCP Server functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create test app
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        # Create test user
        self.test_user = User(username='testuser', email='test@example.com')
        self.test_user.set_password('testpass')
        db.session.add(self.test_user)
        db.session.commit()
        
        # Create temporary API keys file
        self.temp_keys_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_keys_file.close()
        
        # Initialize database manager with test database (use Flask DB)
        self.db_manager = DatabaseManager(use_flask_db=True)
        
        # Initialize API key manager with temp file
        self.api_key_manager = APIKeyManager(self.temp_keys_file.name)
    
    def tearDown(self):
        """Clean up after tests."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
        # Clean up temp file
        if os.path.exists(self.temp_keys_file.name):
            os.unlink(self.temp_keys_file.name)
    
    def test_api_key_generation(self):
        """Test API key generation and validation."""
        # Generate a new API key
        api_key = self.api_key_manager.generate_api_key("Test Key", user_id=self.test_user.id)
        
        # Validate the generated key
        key_info = self.api_key_manager.validate_api_key(api_key)
        self.assertIsNotNone(key_info)
        self.assertEqual(key_info['name'], "Test Key")
        self.assertEqual(key_info['user_id'], self.test_user.id)
        self.assertTrue(key_info['is_active'])
    
    def test_api_key_revocation(self):
        """Test API key revocation."""
        # Generate and then revoke a key
        api_key = self.api_key_manager.generate_api_key("Test Key")
        self.assertTrue(self.api_key_manager.revoke_api_key(api_key))
        
        # Key should no longer be valid
        key_info = self.api_key_manager.validate_api_key(api_key)
        self.assertIsNone(key_info)
    
    def test_create_todo_via_database(self):
        """Test creating a todo via database manager."""
        todo_data = self.db_manager.create_todo(
            title="Test Todo",
            description="Test description", 
            status="pending",
            priority="high",
            user_id=self.test_user.id
        )
        
        self.assertIsNotNone(todo_data)
        self.assertEqual(todo_data['title'], "Test Todo")
        self.assertEqual(todo_data['description'], "Test description")
        self.assertEqual(todo_data['status'], "pending")
        self.assertEqual(todo_data['priority'], "high")
        self.assertEqual(todo_data['user_id'], self.test_user.id)
    
    def test_list_todos_via_database(self):
        """Test listing todos via database manager."""
        # Create some test todos
        self.db_manager.create_todo("Todo 1", user_id=self.test_user.id)
        self.db_manager.create_todo("Todo 2", status="completed", user_id=self.test_user.id)
        
        # List all todos
        todos = self.db_manager.list_todos()
        self.assertEqual(len(todos), 2)
        
        # Filter by status
        pending_todos = self.db_manager.list_todos(status="pending")
        self.assertEqual(len(pending_todos), 1)
        self.assertEqual(pending_todos[0]['title'], "Todo 1")
        
        completed_todos = self.db_manager.list_todos(status="completed")
        self.assertEqual(len(completed_todos), 1)
        self.assertEqual(completed_todos[0]['title'], "Todo 2")
    
    def test_update_todo_via_database(self):
        """Test updating a todo via database manager."""
        # Create a todo
        todo_data = self.db_manager.create_todo(
            title="Original Title",
            user_id=self.test_user.id
        )
        todo_id = todo_data['id']
        
        # Update the todo
        updated_todo = self.db_manager.update_todo(
            todo_id=todo_id,
            title="Updated Title",
            status="in_progress",
            priority="critical"
        )
        
        self.assertIsNotNone(updated_todo)
        self.assertEqual(updated_todo['title'], "Updated Title")
        self.assertEqual(updated_todo['status'], "in_progress")
        self.assertEqual(updated_todo['priority'], "critical")
    
    def test_delete_todo_via_database(self):
        """Test deleting a todo via database manager."""
        # Create a todo
        todo_data = self.db_manager.create_todo(
            title="To Be Deleted",
            user_id=self.test_user.id
        )
        todo_id = todo_data['id']
        
        # Verify it exists
        self.assertIsNotNone(self.db_manager.get_todo_by_id(todo_id))
        
        # Delete it
        success = self.db_manager.delete_todo(todo_id)
        self.assertTrue(success)
        
        # Verify it's gone
        self.assertIsNone(self.db_manager.get_todo_by_id(todo_id))
    
    def test_get_user_info_via_database(self):
        """Test getting user info via database manager."""
        # Get user by ID
        user_data = self.db_manager.get_user_by_id(self.test_user.id)
        self.assertIsNotNone(user_data)
        self.assertEqual(user_data['username'], 'testuser')
        self.assertEqual(user_data['email'], 'test@example.com')
        
        # Get user by username
        user_data = self.db_manager.get_user_by_username('testuser')
        self.assertIsNotNone(user_data)
        self.assertEqual(user_data['id'], self.test_user.id)
    
    def test_invalid_todo_operations(self):
        """Test error handling for invalid operations."""
        # Try to create todo without title
        with self.assertRaises(ValueError):
            self.db_manager.create_todo(title="", user_id=self.test_user.id)
        
        # Try to create todo without user_id
        with self.assertRaises(ValueError):
            self.db_manager.create_todo(title="Test")
        
        # Try to create todo with invalid status
        with self.assertRaises(ValueError):
            self.db_manager.create_todo(
                title="Test",
                status="invalid_status",
                user_id=self.test_user.id
            )
        
        # Try to get non-existent todo
        self.assertIsNone(self.db_manager.get_todo_by_id(999999))
        
        # Try to update non-existent todo
        self.assertIsNone(self.db_manager.update_todo(999999, title="New Title"))
        
        # Try to delete non-existent todo
        self.assertFalse(self.db_manager.delete_todo(999999))


if __name__ == '__main__':
    unittest.main()