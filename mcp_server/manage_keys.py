#!/usr/bin/env python3
"""API Key management utility for the CyberTODO MCP Server."""

import sys
import os
import argparse

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from mcp_server.auth import api_key_manager


def list_keys():
    """List all API keys."""
    keys = api_key_manager.list_api_keys()
    
    if not keys:
        print("No API keys found.")
        return
    
    print(f"Found {len(keys)} API key(s):\n")
    
    for i, key_info in enumerate(keys, 1):
        status = "🟢 Active" if key_info['is_active'] else "🔴 Revoked"
        user_info = f"User ID: {key_info['user_id']}" if key_info['user_id'] else "System key"
        last_used = key_info['last_used'] or "Never"
        
        print(f"{i}. {key_info['name']}")
        print(f"   Status: {status}")
        print(f"   {user_info}")
        print(f"   Created: {key_info['created_at'][:19]}")
        print(f"   Last used: {last_used[:19] if last_used != 'Never' else last_used}")
        print()


def generate_key(name: str, user_id: int = None):
    """Generate a new API key."""
    try:
        api_key = api_key_manager.generate_api_key(name, user_id)
        print(f"✅ Generated new API key: {api_key}")
        print(f"   Name: {name}")
        if user_id:
            print(f"   User ID: {user_id}")
        else:
            print(f"   Type: System key")
        print(f"\n💡 Save this key - you won't be able to see it again!")
        
    except Exception as e:
        print(f"❌ Error generating API key: {e}")


def revoke_key(api_key: str):
    """Revoke an API key."""
    try:
        success = api_key_manager.revoke_api_key(api_key)
        if success:
            print(f"✅ API key revoked successfully")
        else:
            print(f"❌ API key not found")
    except Exception as e:
        print(f"❌ Error revoking API key: {e}")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Manage API keys for CyberTODO MCP Server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python mcp_server/manage_keys.py list
  python mcp_server/manage_keys.py generate "My LLM Client"
  python mcp_server/manage_keys.py generate "User API Key" --user-id 123
  python mcp_server/manage_keys.py revoke cyber_abc123...
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List all API keys')
    
    # Generate command  
    gen_parser = subparsers.add_parser('generate', help='Generate a new API key')
    gen_parser.add_argument('name', help='Human-readable name for the API key')
    gen_parser.add_argument('--user-id', type=int, help='Associate key with specific user ID')
    
    # Revoke command
    revoke_parser = subparsers.add_parser('revoke', help='Revoke an API key') 
    revoke_parser.add_argument('api_key', help='The API key to revoke')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    print("🔑 CyberTODO MCP Server - API Key Manager\n")
    
    if args.command == 'list':
        list_keys()
    elif args.command == 'generate':
        generate_key(args.name, args.user_id)
    elif args.command == 'revoke':
        revoke_key(args.api_key)


if __name__ == "__main__":
    main()