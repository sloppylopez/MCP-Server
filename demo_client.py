#!/usr/bin/env python3
"""
MCP Client Demo - Demonstrates the complete MCP lifecycle
"""

import asyncio
import sys
import os

# Add the client directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'mcp_client'))

try:
    from client import MCPClient
except ImportError:
    # If import fails, try direct import
    sys.path.append('mcp_client')
    from client import MCPClient


async def demo_lifecycle():
    """Demonstrate the complete MCP lifecycle."""
    print("🎯 MCP Client Lifecycle Demo")
    print("============================")
    
    # Configuration
    server_command = [".venv\\Scripts\\python.exe", "-m", "mcp_hello_server.main"]
    server_cwd = "C:\\dev\\code\\MCP-Server"
    
    client = MCPClient(server_command, server_cwd)
    
    try:
        print("\n📋 MCP Lifecycle Steps:")
        print("1. 🚀 Start MCP Server Process")
        print("2. 🤝 Initialize MCP Connection")
        print("3. 🔍 Discover Available Tools")
        print("4. 🔧 Call Tools with Parameters")
        print("5. 🧹 Cleanup and Exit")
        print()
        
        # Step 1: Start server
        print("Step 1: Starting MCP server...")
        if not await client.start_server():
            print("❌ Failed to start server")
            return
        
        # Step 2: Initialize
        print("\nStep 2: Initializing MCP connection...")
        if not await client.initialize():
            print("❌ Failed to initialize")
            return
        
        # Step 3: Discover tools
        print("\nStep 3: Discovering tools...")
        if not await client.discover_tools():
            print("❌ Failed to discover tools")
            return
        
        # Step 4: Demo tool calls
        print("\nStep 4: Demonstrating tool calls...")
        
        # Call hello tool
        print("\n🔧 Calling 'hello' tool:")
        await client.call_tool("hello", {"name": "MCP Demo User"})
        
        # Call echo tool
        print("\n🔧 Calling 'echo' tool:")
        await client.call_tool("echo", {"message": "Hello from MCP Client Demo!"})
        
        # Call get_time tool
        print("\n🔧 Calling 'get_time' tool:")
        await client.call_tool("get_time", {})
        
        # Call add_numbers tool
        print("\n🔧 Calling 'add_numbers' tool:")
        await client.call_tool("add_numbers", {"a": 42, "b": 8})
        
        print("\n✅ Demo completed successfully!")
        print("\n🎮 To try interactive mode, run: py mcp_client/client.py")
        
    except Exception as e:
        print(f"❌ Demo error: {e}")
    finally:
        # Step 5: Cleanup
        print("\nStep 5: Cleaning up...")
        await client.cleanup()


if __name__ == "__main__":
    asyncio.run(demo_lifecycle())
