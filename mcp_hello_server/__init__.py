"""
MCP Hello Server - A simple Model Context Protocol server implementation.

This server provides basic tools for greeting and echoing messages.
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
    Tool,
    TextContent,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the MCP server instance
server = Server("mcp-hello-server")


@server.list_tools()
async def list_tools() -> List[Tool]:
    """List available tools."""
    return [
        Tool(
            name="hello",
            description="Say hello to someone",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name of the person to greet"
                    }
                },
                "required": ["name"]
            }
        ),
        Tool(
            name="echo",
            description="Echo back the provided message",
            inputSchema={
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "The message to echo back"
                    }
                },
                "required": ["message"]
            }
        ),
        Tool(
            name="get_time",
            description="Get the current time",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="add_numbers",
            description="Add two numbers together",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "First number"
                    },
                    "b": {
                        "type": "number",
                        "description": "Second number"
                    }
                },
                "required": ["a", "b"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle tool calls."""
    logger.info(f"Tool called: {name} with arguments: {arguments}")
    
    if name == "hello":
        name_arg = arguments.get("name", "World")
        message = f"Hello, {name_arg}! Welcome to the MCP Hello Server!"
        return [TextContent(type="text", text=message)]
    
    elif name == "echo":
        message = arguments.get("message", "")
        return [TextContent(type="text", text=f"Echo: {message}")]
    
    elif name == "get_time":
        import datetime
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return [TextContent(type="text", text=f"Current time: {current_time}")]
    
    elif name == "add_numbers":
        try:
            a = float(arguments.get("a", 0))
            b = float(arguments.get("b", 0))
            result = a + b
            return [TextContent(type="text", text=f"{a} + {b} = {result}")]
        except (ValueError, TypeError) as e:
            return [TextContent(type="text", text=f"Error: Invalid numbers provided - {str(e)}")]
    
    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def main():
    """Main entry point for the MCP server."""
    logger.info("Starting MCP Hello Server...")
    
    # Run the server using stdio transport
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="mcp-hello-server",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities={}
                )
            )
        )


if __name__ == "__main__":
    asyncio.run(main())
