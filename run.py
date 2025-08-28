#!/usr/bin/env python3
"""
CyberTODO Application Runner

This script starts the Flask development server for the CyberTODO application.
"""

import os
from app import create_app, db
from app.models.user import User
from app.models.todo import Todo

# Create application instance
app = create_app(os.environ.get('FLASK_CONFIG', 'development'))


@app.shell_context_processor
def make_shell_context():
    """
    Add database models to Flask shell context.
    
    Returns:
        Dictionary of objects to make available in shell
    """
    return {
        'db': db,
        'User': User,
        'Todo': Todo
    }


@app.cli.command()
def init_db():
    """Initialize the database with tables."""
    db.create_all()
    print('Database initialized.')


@app.cli.command()
def reset_db():
    """Reset the database (drop and recreate all tables)."""
    db.drop_all()
    db.create_all()
    print('Database reset.')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)