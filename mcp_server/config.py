"""Configuration for the MCP Server."""

import os
from typing import Optional


class MCPConfig:
    """Configuration class for the MCP Server."""
    
    # Database connection - reuse the main app's database
    DATABASE_URI: str = os.environ.get('DATABASE_URL') or 'sqlite:///todo_app.db'
    
    # MCP Server settings
    SERVER_NAME: str = "CyberTODO MCP Server"
    SERVER_VERSION: str = "1.0.0"
    
    # API Key settings for authentication
    API_KEY_HEADER: str = "X-API-Key"
    API_KEYS_FILE: str = os.environ.get('MCP_API_KEYS_FILE') or 'mcp_api_keys.json'
    
    # Default API key for development (should be changed in production)
    DEFAULT_API_KEY: str = os.environ.get('MCP_DEFAULT_API_KEY') or 'cyber-todo-2077-dev-key'
    
    @classmethod
    def get_database_uri(cls) -> str:
        """Get the database URI."""
        return cls.DATABASE_URI