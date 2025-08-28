# CyberTODO MCP Server

This directory contains the Model Context Protocol (MCP) server for CyberTODO 2077, enabling LLMs to perform CRUD operations on todo items.

## Features

- **Full CRUD Operations**: Create, Read, Update, Delete todos
- **User Management**: Get user information and manage todos by user
- **Filtering**: Filter todos by status, priority, and other criteria
- **API Key Authentication**: Secure access using API keys
- **Database Integration**: Direct integration with the main CyberTODO database

## Available Tools

### 1. `list_todos`
List todos with optional filtering.

**Parameters:**
- `status` (optional): Filter by status ("pending", "in_progress", "completed")
- `priority` (optional): Filter by priority ("low", "medium", "high", "critical")
- `limit` (optional): Maximum number of todos to return (default: 50, max: 100)

### 2. `get_todo`
Get a specific todo by ID.

**Parameters:**
- `todo_id` (required): The ID of the todo to retrieve

### 3. `create_todo`
Create a new todo item.

**Parameters:**
- `title` (required): The title of the todo
- `user_id` (required): The ID of the user who owns this todo
- `description` (optional): Description of the todo
- `status` (optional): Status ("pending", "in_progress", "completed") - default: "pending"
- `priority` (optional): Priority ("low", "medium", "high", "critical") - default: "medium"
- `due_date` (optional): Due date in ISO format (e.g., "2024-12-31T23:59:59Z")

### 4. `update_todo`
Update an existing todo item.

**Parameters:**
- `todo_id` (required): The ID of the todo to update
- `title` (optional): New title
- `description` (optional): New description
- `status` (optional): New status
- `priority` (optional): New priority
- `due_date` (optional): New due date in ISO format (use empty string to clear)

### 5. `delete_todo`
Delete a todo item.

**Parameters:**
- `todo_id` (required): The ID of the todo to delete

### 6. `get_user_info`
Get information about a user.

**Parameters:**
- `user_id` (optional): The ID of the user
- `username` (optional): The username to look up

*Note: Either `user_id` or `username` must be provided.*

## Running the Server

### Method 1: Direct execution
```bash
cd /path/to/cybertodo
python mcp_server/run_server.py
```

### Method 2: Module execution
```bash
cd /path/to/cybertodo
python -m mcp_server.run_server
```

## API Key Authentication

The MCP server uses API keys for authentication. By default, a development API key is created:

- **Default API Key**: `cyber-todo-2077-dev-key`

### Managing API Keys

API keys are stored in `mcp_api_keys.json` (configurable via `MCP_API_KEYS_FILE` environment variable).

To generate a new API key programmatically:

```python
from mcp_server.auth import api_key_manager

# Generate a new API key
api_key = api_key_manager.generate_api_key("My LLM Client", user_id=1)
print(f"Generated API key: {api_key}")
```

### Environment Variables

- `MCP_API_KEYS_FILE`: Path to API keys storage file (default: `mcp_api_keys.json`)
- `MCP_DEFAULT_API_KEY`: Default development API key (default: `cyber-todo-2077-dev-key`)
- `DATABASE_URL`: Database connection string (defaults to main app's database)

## Database Connection

The MCP server connects to the same database as the main CyberTODO application. Make sure the database is properly initialized:

```bash
cd /path/to/cybertodo
python run.py init-db
```

## Integration with LLM Clients

The MCP server communicates via stdio and follows the Model Context Protocol specification. It can be integrated with various LLM clients that support MCP.

### Example Client Configuration

For clients that support MCP configuration:

```json
{
  "servers": {
    "cybertodo": {
      "command": "python",
      "args": ["/path/to/cybertodo/mcp_server/run_server.py"],
      "env": {
        "MCP_DEFAULT_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

## Security Considerations

1. **Change Default API Key**: In production, always change the default API key
2. **Secure Storage**: Store API keys securely and rotate them regularly
3. **User Isolation**: The current implementation allows system-wide access; consider implementing user-specific access controls
4. **Database Security**: Ensure the database connection is secure

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure you're running from the project root directory
2. **Database Connection**: Verify the database exists and is accessible
3. **Permission Errors**: Ensure the MCP server has read/write access to the database and API keys file

### Debug Mode

To run with debug output:

```bash
export PYTHONPATH=/path/to/cybertodo
python -c "
import asyncio
import logging
logging.basicConfig(level=logging.DEBUG)
from mcp_server.server import main
asyncio.run(main())
"
```

## Development

### File Structure

- `__init__.py`: Package initialization
- `config.py`: Configuration settings
- `auth.py`: API key authentication system
- `database.py`: Database interface and operations
- `server.py`: Main MCP server implementation
- `run_server.py`: Startup script

### Testing

Create test todos and users through the main Flask application, then test the MCP server tools.

### Contributing

When adding new tools or modifying existing ones:

1. Update the tool definitions in `server.py`
2. Add corresponding handler methods
3. Update this README documentation
4. Test thoroughly with various scenarios