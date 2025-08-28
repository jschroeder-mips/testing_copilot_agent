# CyberTODO MCP Server Usage Examples

This document provides examples of how to use the CyberTODO MCP Server tools.

## Prerequisites

1. Start the Flask application to initialize the database:
```bash
cd /path/to/cybertodo
python run.py init-db
python run.py  # Start the web app to create some users
```

2. Start the MCP server:
```bash
python mcp_server/run_server.py
```

## Tool Usage Examples

### 1. List Todos

```json
{
  "method": "tools/call",
  "params": {
    "name": "list_todos",
    "arguments": {
      "status": "pending",
      "limit": 10
    }
  }
}
```

### 2. Create a Todo

```json
{
  "method": "tools/call", 
  "params": {
    "name": "create_todo",
    "arguments": {
      "title": "Complete MCP server implementation",
      "description": "Finish the Model Context Protocol server for CyberTODO",
      "status": "in_progress",
      "priority": "high",
      "due_date": "2024-12-31T23:59:59Z",
      "user_id": 1
    }
  }
}
```

### 3. Get a Specific Todo

```json
{
  "method": "tools/call",
  "params": {
    "name": "get_todo", 
    "arguments": {
      "todo_id": 1
    }
  }
}
```

### 4. Update a Todo

```json
{
  "method": "tools/call",
  "params": {
    "name": "update_todo",
    "arguments": {
      "todo_id": 1,
      "status": "completed",
      "priority": "medium"
    }
  }
}
```

### 5. Delete a Todo

```json
{
  "method": "tools/call",
  "params": {
    "name": "delete_todo",
    "arguments": {
      "todo_id": 1
    }
  }
}
```

### 6. Get User Information

```json
{
  "method": "tools/call",
  "params": {
    "name": "get_user_info",
    "arguments": {
      "username": "testuser"
    }
  }
}
```

## Common Workflow

1. **Get user info** to find the user ID
2. **List todos** to see existing items
3. **Create todos** for new tasks
4. **Update todos** to change status/priority
5. **Delete todos** when no longer needed

## Response Format

All tools return text content with formatted output including emojis for better readability:

- ⏳ Pending todos
- 🔄 In progress todos  
- ✅ Completed todos
- 🟢 Low priority
- 🟡 Medium priority
- 🟠 High priority
- 🔴 Critical priority
- ⚠️ Overdue items

## Error Handling

The server provides helpful error messages for common issues:

- Missing required parameters
- Invalid todo IDs
- Invalid status/priority values
- Invalid date formats
- Database connection issues

## Security Notes

- All operations require a valid API key
- System API key allows access to all todos
- User-specific API keys would only allow access to that user's todos (future enhancement)
- Sensitive data is never logged or exposed in error messages