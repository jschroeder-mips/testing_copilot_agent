#!/usr/bin/env python3
"""Test script to reproduce the timezone issue"""

import sys
import os

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from datetime import datetime, timezone
from app.models.todo import Todo, TodoStatus, TodoPriority

def test_timezone_issue():
    """Reproduce the timezone comparison issue"""
    
    # Create a mock Todo object with offset-naive due_date
    todo = Todo()
    todo.due_date = datetime(2023, 1, 1, 12, 0, 0)  # offset-naive
    todo.status = TodoStatus.PENDING
    
    print(f"due_date: {todo.due_date}")
    print(f"due_date timezone: {todo.due_date.tzinfo}")
    print(f"current datetime: {datetime.now(timezone.utc)}")
    print(f"current datetime timezone: {datetime.now(timezone.utc).tzinfo}")
    
    try:
        # This should trigger the TypeError
        result = todo.is_overdue
        print(f"is_overdue result: {result}")
    except TypeError as e:
        print(f"TypeError occurred: {e}")
        return True
    
    return False

if __name__ == "__main__":
    has_error = test_timezone_issue()
    if has_error:
        print("✓ Successfully reproduced the timezone issue")
        sys.exit(0)
    else:
        print("✗ Could not reproduce the timezone issue")
        sys.exit(1)