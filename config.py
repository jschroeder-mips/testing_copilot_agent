"""Application configuration module."""
import os
from typing import Any, Dict


class Config:
    """Base configuration class with common settings."""
    
    SECRET_KEY: str = os.environ.get('SECRET_KEY') or 'cyberpunk-todo-secret-key-2077'
    SQLALCHEMY_DATABASE_URI: str = os.environ.get('DATABASE_URL') or 'sqlite:///todo_app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    WTF_CSRF_ENABLED: bool = True
    
    # API Configuration
    RESTX_MASK_SWAGGER: bool = False
    SWAGGER_UI_DOC_EXPANSION: str = 'list'
    
    @staticmethod
    def init_app(app: Any) -> None:
        """Initialize application with configuration."""
        pass


class DevelopmentConfig(Config):
    """Development configuration."""
    
    DEBUG: bool = True
    SQLALCHEMY_ECHO: bool = True


class ProductionConfig(Config):
    """Production configuration."""
    
    DEBUG: bool = False


class TestingConfig(Config):
    """Testing configuration."""
    
    TESTING: bool = True
    SQLALCHEMY_DATABASE_URI: str = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED: bool = False


config: Dict[str, type] = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}