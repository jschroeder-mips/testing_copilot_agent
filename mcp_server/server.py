"""Main MCP Server implementation for CyberTODO 2077."""

import asyncio
from typing import Any, Dict, List, Optional
from datetime import datetime

import mcp.types as types
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
import mcp.server.stdio

from .auth import api_key_manager
from .database import db_manager
from .config import MCPConfig


class CyberTodoMCPServer:
    """MCP Server for CyberTODO 2077 todo management."""
    
    def __init__(self):
        """Initialize the MCP server."""
        self.server = Server(MCPConfig.SERVER_NAME)
        self._setup_tools()
        self._setup_handlers()
    
    def _setup_tools(self):
        """Set up the available tools for the MCP server."""
        
        @self.server.list_tools()
        async def handle_list_tools() -> list[types.Tool]:
            """List available tools."""
            return [
                types.Tool(
                    name="list_todos",
                    description="List todos with optional filtering by status and priority",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "status": {
                                "type": "string",
                                "enum": ["pending", "in_progress", "completed"],
                                "description": "Filter todos by status"
                            },
                            "priority": {
                                "type": "string", 
                                "enum": ["low", "medium", "high", "critical"],
                                "description": "Filter todos by priority"
                            },
                            "limit": {
                                "type": "integer",
                                "default": 50,
                                "maximum": 100,
                                "description": "Maximum number of todos to return"
                            }
                        }
                    }
                ),
                types.Tool(
                    name="get_todo",
                    description="Get a specific todo by ID",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "todo_id": {
                                "type": "integer",
                                "description": "The ID of the todo to retrieve"
                            }
                        },
                        "required": ["todo_id"]
                    }
                ),
                types.Tool(
                    name="create_todo",
                    description="Create a new todo item",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "The title of the todo item"
                            },
                            "description": {
                                "type": "string",
                                "description": "Optional description of the todo item"
                            },
                            "status": {
                                "type": "string",
                                "enum": ["pending", "in_progress", "completed"],
                                "default": "pending",
                                "description": "The status of the todo"
                            },
                            "priority": {
                                "type": "string",
                                "enum": ["low", "medium", "high", "critical"],
                                "default": "medium", 
                                "description": "The priority level of the todo"
                            },
                            "due_date": {
                                "type": "string",
                                "format": "date-time",
                                "description": "Optional due date in ISO format (e.g., 2024-12-31T23:59:59Z)"
                            },
                            "user_id": {
                                "type": "integer",
                                "description": "The ID of the user who owns this todo"
                            }
                        },
                        "required": ["title", "user_id"]
                    }
                ),
                types.Tool(
                    name="update_todo", 
                    description="Update an existing todo item",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "todo_id": {
                                "type": "integer",
                                "description": "The ID of the todo to update"
                            },
                            "title": {
                                "type": "string",
                                "description": "New title for the todo"
                            },
                            "description": {
                                "type": "string",
                                "description": "New description for the todo"
                            },
                            "status": {
                                "type": "string",
                                "enum": ["pending", "in_progress", "completed"],
                                "description": "New status for the todo"
                            },
                            "priority": {
                                "type": "string",
                                "enum": ["low", "medium", "high", "critical"],
                                "description": "New priority for the todo"
                            },
                            "due_date": {
                                "type": "string",
                                "format": "date-time",
                                "description": "New due date in ISO format (use empty string to clear)"
                            }
                        },
                        "required": ["todo_id"]
                    }
                ),
                types.Tool(
                    name="delete_todo",
                    description="Delete a todo item",
                    inputSchema={
                        "type": "object", 
                        "properties": {
                            "todo_id": {
                                "type": "integer",
                                "description": "The ID of the todo to delete"
                            }
                        },
                        "required": ["todo_id"]
                    }
                ),
                types.Tool(
                    name="get_user_info",
                    description="Get information about a user",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "user_id": {
                                "type": "integer",
                                "description": "The ID of the user"
                            },
                            "username": {
                                "type": "string", 
                                "description": "The username to look up"
                            }
                        }
                    }
                )
            ]
        
        @self.server.call_tool()
        async def handle_call_tool(
            name: str, arguments: dict | None
        ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
            """Handle tool calls."""
            
            if name == "list_todos":
                return await self._handle_list_todos(arguments or {})
            elif name == "get_todo":
                return await self._handle_get_todo(arguments or {})
            elif name == "create_todo":
                return await self._handle_create_todo(arguments or {})
            elif name == "update_todo":
                return await self._handle_update_todo(arguments or {})
            elif name == "delete_todo":
                return await self._handle_delete_todo(arguments or {})
            elif name == "get_user_info":
                return await self._handle_get_user_info(arguments or {})
            else:
                raise ValueError(f"Unknown tool: {name}")
    
    def _setup_handlers(self):
        """Set up server event handlers."""
        
        @self.server.list_resources()
        async def handle_list_resources() -> list[types.Resource]:
            """List available resources."""
            return [
                types.Resource(
                    uri="cybertodo://todos",
                    name="CyberTODO Todos",
                    description="Access to todo items in the CyberTODO system",
                    mimeType="application/json"
                )
            ]
        
        @self.server.read_resource()
        async def handle_read_resource(uri: str) -> str:
            """Read a resource."""
            if uri == "cybertodo://todos":
                todos = db_manager.list_todos(limit=50)
                return f"Current todos in CyberTODO system: {len(todos)} items"
            else:
                raise ValueError(f"Unknown resource: {uri}")
    
    async def _handle_list_todos(self, arguments: dict) -> list[types.TextContent]:
        """Handle list_todos tool call."""
        try:
            status = arguments.get("status")
            priority = arguments.get("priority") 
            limit = arguments.get("limit", 50)
            
            # For system API key, allow listing all todos (user_id=None)
            # For user API keys, we would filter by user_id
            todos = db_manager.list_todos(
                user_id=None,  # System access for now
                status=status,
                priority=priority,
                limit=limit
            )
            
            if not todos:
                return [types.TextContent(
                    type="text",
                    text="No todos found matching the specified criteria."
                )]
            
            # Format todos for display
            todo_list = []
            for todo in todos:
                status_emoji = {"pending": "⏳", "in_progress": "🔄", "completed": "✅"}.get(todo["status"], "❓")
                priority_emoji = {"low": "🟢", "medium": "🟡", "high": "🟠", "critical": "🔴"}.get(todo["priority"], "⚪")
                
                due_info = ""
                if todo["due_date"]:
                    due_date = datetime.fromisoformat(todo["due_date"].replace('Z', '+00:00'))
                    due_info = f" (Due: {due_date.strftime('%Y-%m-%d')})"
                
                overdue_info = " ⚠️ OVERDUE" if todo.get("is_overdue") else ""
                
                todo_list.append(
                    f"#{todo['id']} {status_emoji} {priority_emoji} {todo['title']}{due_info}{overdue_info}\n"
                    f"   Status: {todo['status']}, Priority: {todo['priority']}\n"
                    f"   User ID: {todo['user_id']}, Created: {todo['created_at'][:10]}"
                )
            
            result = f"Found {len(todos)} todo(s):\n\n" + "\n\n".join(todo_list)
            
            return [types.TextContent(type="text", text=result)]
            
        except Exception as e:
            return [types.TextContent(
                type="text",
                text=f"Error listing todos: {str(e)}"
            )]
    
    async def _handle_get_todo(self, arguments: dict) -> list[types.TextContent]:
        """Handle get_todo tool call."""
        try:
            todo_id = arguments.get("todo_id")
            if not todo_id:
                return [types.TextContent(
                    type="text",
                    text="Error: todo_id is required"
                )]
            
            todo = db_manager.get_todo_by_id(todo_id)
            if not todo:
                return [types.TextContent(
                    type="text",
                    text=f"Todo with ID {todo_id} not found"
                )]
            
            # Format todo details
            status_emoji = {"pending": "⏳", "in_progress": "🔄", "completed": "✅"}.get(todo["status"], "❓")
            priority_emoji = {"low": "🟢", "medium": "🟡", "high": "🟠", "critical": "🔴"}.get(todo["priority"], "⚪")
            
            result = f"""
Todo #{todo['id']} {status_emoji} {priority_emoji}

Title: {todo['title']}
Description: {todo['description'] or 'No description'}
Status: {todo['status']}
Priority: {todo['priority']}
Owner: User ID {todo['user_id']}
Created: {todo['created_at']}
Updated: {todo['updated_at']}
Due Date: {todo['due_date'] or 'Not set'}
Overdue: {'Yes ⚠️' if todo.get('is_overdue') else 'No'}
            """.strip()
            
            return [types.TextContent(type="text", text=result)]
            
        except Exception as e:
            return [types.TextContent(
                type="text",
                text=f"Error getting todo: {str(e)}"
            )]
    
    async def _handle_create_todo(self, arguments: dict) -> list[types.TextContent]:
        """Handle create_todo tool call."""
        try:
            title = arguments.get("title")
            if not title:
                return [types.TextContent(
                    type="text",
                    text="Error: title is required"
                )]
            
            user_id = arguments.get("user_id")
            if not user_id:
                return [types.TextContent(
                    type="text", 
                    text="Error: user_id is required"
                )]
            
            todo = db_manager.create_todo(
                title=title,
                description=arguments.get("description"),
                status=arguments.get("status", "pending"),
                priority=arguments.get("priority", "medium"),
                due_date=arguments.get("due_date"),
                user_id=user_id
            )
            
            return [types.TextContent(
                type="text",
                text=f"✅ Successfully created todo #{todo['id']}: {todo['title']}"
            )]
            
        except Exception as e:
            return [types.TextContent(
                type="text",
                text=f"Error creating todo: {str(e)}"
            )]
    
    async def _handle_update_todo(self, arguments: dict) -> list[types.TextContent]:
        """Handle update_todo tool call."""
        try:
            todo_id = arguments.get("todo_id")
            if not todo_id:
                return [types.TextContent(
                    type="text",
                    text="Error: todo_id is required"
                )]
            
            # Get current todo first
            current_todo = db_manager.get_todo_by_id(todo_id)
            if not current_todo:
                return [types.TextContent(
                    type="text",
                    text=f"Todo with ID {todo_id} not found"
                )]
            
            # Update the todo
            updated_todo = db_manager.update_todo(
                todo_id=todo_id,
                title=arguments.get("title"),
                description=arguments.get("description"),
                status=arguments.get("status"),
                priority=arguments.get("priority"),
                due_date=arguments.get("due_date")
            )
            
            if not updated_todo:
                return [types.TextContent(
                    type="text",
                    text=f"Failed to update todo #{todo_id}"
                )]
            
            return [types.TextContent(
                type="text",
                text=f"✅ Successfully updated todo #{todo_id}: {updated_todo['title']}"
            )]
            
        except Exception as e:
            return [types.TextContent(
                type="text",
                text=f"Error updating todo: {str(e)}"
            )]
    
    async def _handle_delete_todo(self, arguments: dict) -> list[types.TextContent]:
        """Handle delete_todo tool call."""
        try:
            todo_id = arguments.get("todo_id")
            if not todo_id:
                return [types.TextContent(
                    type="text",
                    text="Error: todo_id is required"
                )]
            
            # Get todo details before deletion
            todo = db_manager.get_todo_by_id(todo_id)
            if not todo:
                return [types.TextContent(
                    type="text",
                    text=f"Todo with ID {todo_id} not found"
                )]
            
            success = db_manager.delete_todo(todo_id)
            if success:
                return [types.TextContent(
                    type="text",
                    text=f"🗑️ Successfully deleted todo #{todo_id}: {todo['title']}"
                )]
            else:
                return [types.TextContent(
                    type="text",
                    text=f"Failed to delete todo #{todo_id}"
                )]
                
        except Exception as e:
            return [types.TextContent(
                type="text", 
                text=f"Error deleting todo: {str(e)}"
            )]
    
    async def _handle_get_user_info(self, arguments: dict) -> list[types.TextContent]:
        """Handle get_user_info tool call.""" 
        try:
            user_id = arguments.get("user_id")
            username = arguments.get("username")
            
            if not user_id and not username:
                return [types.TextContent(
                    type="text",
                    text="Error: Either user_id or username is required"
                )]
            
            if user_id:
                user = db_manager.get_user_by_id(user_id)
            else:
                user = db_manager.get_user_by_username(username)
            
            if not user:
                identifier = f"ID {user_id}" if user_id else f"username '{username}'"
                return [types.TextContent(
                    type="text",
                    text=f"User with {identifier} not found"
                )]
            
            result = f"""
User Information:
ID: {user['id']}
Username: {user['username']}
Email: {user['email']}
Created: {user['created_at']}
Total TODOs: {user['todo_count']}
            """.strip()
            
            return [types.TextContent(type="text", text=result)]
            
        except Exception as e:
            return [types.TextContent(
                type="text",
                text=f"Error getting user info: {str(e)}"
            )]


async def main():
    """Main entry point for the MCP server."""
    # Initialize the server
    server_instance = CyberTodoMCPServer()
    
    # Run the server
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server_instance.server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name=MCPConfig.SERVER_NAME,
                server_version=MCPConfig.SERVER_VERSION,
                capabilities=server_instance.server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={}
                )
            )
        )


if __name__ == "__main__":
    asyncio.run(main())