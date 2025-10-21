#!/usr/bin/env python3
"""
Interactive MCP Server Test
Run this to test the server interactively.
"""

import asyncio
import json
import sys
from mcp_hello_server import main


async def interactive_test():
    """Test the server by importing and calling its functions directly."""
    print("=== Interactive MCP Server Test ===")
    print("Testing server functions directly...")
    print()
    
    # Import the server components
    from mcp_hello_server import server
    
    # Test 1: List tools
    print("=== Test 1: List Tools ===")
    try:
        tools = await server.list_tools()
        print("Available tools:")
        for tool in tools:
            print(f"  - {tool.name}: {tool.description}")
        print()
    except Exception as e:
        print(f"Error listing tools: {e}")
        return
    
    # Test 2: Call hello tool
    print("=== Test 2: Call Hello Tool ===")
    try:
        result = await server.call_tool("hello", {"name": "Test User"})
        print("Hello tool result:")
        for content in result:
            print(f"  {content.text}")
        print()
    except Exception as e:
        print(f"Error calling hello tool: {e}")
        return
    
    # Test 3: Call echo tool
    print("=== Test 3: Call Echo Tool ===")
    try:
        result = await server.call_tool("echo", {"message": "Hello, MCP!"})
        print("Echo tool result:")
        for content in result:
            print(f"  {content.text}")
        print()
    except Exception as e:
        print(f"Error calling echo tool: {e}")
        return
    
    # Test 4: Call get_time tool
    print("=== Test 4: Call Get Time Tool ===")
    try:
        result = await server.call_tool("get_time", {})
        print("Get time tool result:")
        for content in result:
            print(f"  {content.text}")
        print()
    except Exception as e:
        print(f"Error calling get_time tool: {e}")
        return
    
    # Test 5: Call add_numbers tool
    print("=== Test 5: Call Add Numbers Tool ===")
    try:
        result = await server.call_tool("add_numbers", {"a": 5, "b": 3})
        print("Add numbers tool result:")
        for content in result:
            print(f"  {content.text}")
        print()
    except Exception as e:
        print(f"Error calling add_numbers tool: {e}")
        return
    
    print("=== All Tests Passed! ===")
    print("The MCP server functions are working correctly.")
    print()
    print("To test the full server with stdio transport, run:")
    print("  py -m mcp_hello_server.main")
    print("Then send JSON-RPC messages to stdin.")


if __name__ == "__main__":
    asyncio.run(interactive_test())
