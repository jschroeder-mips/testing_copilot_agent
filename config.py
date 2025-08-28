import os
from typing import Type


class Config:
    """Base configuration class for the Flask application."""
    
    SECRET_KEY: str = os.environ.get('SECRET_KEY') or 'cyberpunk-todo-secret-key-2077'
    SQLALCHEMY_DATABASE_URI: str = os.environ.get('DATABASE_URL') or 'sqlite:///todo_app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    
    # API Documentation
    RESTX_MASK_SWAGGER: bool = False
    SWAGGER_UI_DOC_EXPANSION: str = 'list'
    

class DevelopmentConfig(Config):
    """Development configuration."""
    
    DEBUG: bool = True
    

class ProductionConfig(Config):
    """Production configuration."""
    
    DEBUG: bool = False
    

class TestConfig(Config):
    """Testing configuration."""
    
    TESTING: bool = True
    SQLALCHEMY_DATABASE_URI: str = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED: bool = False


config: dict[str, Type[Config]] = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestConfig,
    'default': DevelopmentConfig
}