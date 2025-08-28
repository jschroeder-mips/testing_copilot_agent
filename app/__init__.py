"""
CyberTODO - A cyberpunk-themed TODO application built with Flask.

This application provides user authentication and personal TODO list management
with a dark cyberpunk aesthetic and mobile-ready responsive design.
"""

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_restx import Api
from config import config

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()


def create_app(config_name: str = None) -> Flask:
    """
    Create and configure the Flask application.
    
    Args:
        config_name: Configuration name ('development', 'production', 'testing')
        
    Returns:
        Configured Flask application instance
    """
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG', 'default')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    
    # Configure Flask-Login
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # Register blueprints
    from app.routes.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from app.routes.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    
    from app.routes.api import api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app


@login_manager.user_loader
def load_user(user_id: str):
    """Load user by ID for Flask-Login."""
    from app.models.user import User
    return User.query.get(int(user_id))