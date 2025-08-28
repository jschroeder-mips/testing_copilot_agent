#!/usr/bin/env python3
"""Startup script for the CyberTODO MCP Server."""

import asyncio
import sys
import os

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from mcp_server.server import main

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nMCP Server stopped by user.")
    except Exception as e:
        print(f"Error starting MCP server: {e}")
        sys.exit(1)