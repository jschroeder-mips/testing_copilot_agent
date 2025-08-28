"""Authentication system for the MCP Server using API keys."""

import json
import hashlib
import secrets
from typing import Dict, List, Optional
from pathlib import Path
from datetime import datetime, timezone
from .config import MCPConfig


class APIKeyManager:
    """Manages API keys for MCP server authentication."""
    
    def __init__(self, keys_file: Optional[str] = None):
        """Initialize the API key manager.
        
        Args:
            keys_file: Path to the JSON file storing API keys
        """
        self.keys_file = Path(keys_file or MCPConfig.API_KEYS_FILE)
        self._api_keys: Dict[str, Dict] = {}
        self._load_keys()
    
    def _load_keys(self) -> None:
        """Load API keys from file."""
        if self.keys_file.exists():
            try:
                with open(self.keys_file, 'r') as f:
                    self._api_keys = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load API keys from {self.keys_file}: {e}")
                self._api_keys = {}
        else:
            # Create default API key for development
            self._create_default_key()
    
    def _save_keys(self) -> None:
        """Save API keys to file."""
        try:
            self.keys_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.keys_file, 'w') as f:
                json.dump(self._api_keys, f, indent=2)
        except IOError as e:
            print(f"Error: Could not save API keys to {self.keys_file}: {e}")
    
    def _create_default_key(self) -> None:
        """Create a default API key for development."""
        default_key = MCPConfig.DEFAULT_API_KEY
        hashed_key = self._hash_key(default_key)
        
        self._api_keys[hashed_key] = {
            "name": "Default Development Key",
            "user_id": None,  # No specific user - system key
            "created_at": datetime.now(timezone.utc).isoformat(),
            "last_used": None,
            "is_active": True
        }
        self._save_keys()
        print(f"Created default API key: {default_key}")
    
    def _hash_key(self, api_key: str) -> str:
        """Hash an API key for secure storage.
        
        Args:
            api_key: The raw API key
            
        Returns:
            Hashed API key
        """
        return hashlib.sha256(api_key.encode()).hexdigest()
    
    def generate_api_key(self, name: str, user_id: Optional[int] = None) -> str:
        """Generate a new API key.
        
        Args:
            name: Human-readable name for the API key
            user_id: Optional user ID to associate with the key
            
        Returns:
            The generated API key
        """
        # Generate a secure random API key
        api_key = f"cyber_{secrets.token_urlsafe(32)}"
        hashed_key = self._hash_key(api_key)
        
        self._api_keys[hashed_key] = {
            "name": name,
            "user_id": user_id,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "last_used": None,
            "is_active": True
        }
        
        self._save_keys()
        return api_key
    
    def validate_api_key(self, api_key: str) -> Optional[Dict]:
        """Validate an API key and return associated metadata.
        
        Args:
            api_key: The API key to validate
            
        Returns:
            API key metadata if valid, None otherwise
        """
        if not api_key:
            return None
            
        hashed_key = self._hash_key(api_key)
        key_info = self._api_keys.get(hashed_key)
        
        if key_info and key_info.get("is_active", False):
            # Update last used timestamp
            key_info["last_used"] = datetime.now(timezone.utc).isoformat()
            self._save_keys()
            return key_info
        
        return None
    
    def revoke_api_key(self, api_key: str) -> bool:
        """Revoke an API key.
        
        Args:
            api_key: The API key to revoke
            
        Returns:
            True if key was found and revoked, False otherwise
        """
        hashed_key = self._hash_key(api_key)
        if hashed_key in self._api_keys:
            self._api_keys[hashed_key]["is_active"] = False
            self._save_keys()
            return True
        return False
    
    def list_api_keys(self) -> List[Dict]:
        """List all API keys (without showing the actual keys).
        
        Returns:
            List of API key metadata
        """
        return [
            {
                "name": info["name"],
                "user_id": info["user_id"],
                "created_at": info["created_at"],
                "last_used": info["last_used"],
                "is_active": info["is_active"]
            }
            for info in self._api_keys.values()
        ]


# Global API key manager instance
api_key_manager = APIKeyManager()