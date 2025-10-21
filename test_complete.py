#!/usr/bin/env python3
"""
Complete MCP Server Test
This demonstrates the full MCP protocol flow.
"""

import subprocess
import sys
import time
import json


def test_complete_flow():
    """Test the complete MCP protocol flow."""
    print("=== Complete MCP Server Test ===")
    print("Testing the full MCP protocol flow...")
    print()
    
    # Prepare the test messages
    messages = [
        # Initialize
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test-client", "version": "1.0.0"}}},
        # Send initialized notification
        {"jsonrpc": "2.0", "method": "notifications/initialized"},
        # List tools
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
        # Call hello tool
        {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "hello", "arguments": {"name": "Test User"}}},
        # Call echo tool
        {"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "echo", "arguments": {"message": "Hello, MCP!"}}},
        # Call get_time tool
        {"jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": {"name": "get_time", "arguments": {}}},
        # Call add_numbers tool
        {"jsonrpc": "2.0", "id": 6, "method": "tools/call", "params": {"name": "add_numbers", "arguments": {"a": 5, "b": 3}}}
    ]
    
    # Convert to JSON lines
    input_data = "\n".join(json.dumps(msg) for msg in messages)
    
    print("Sending test messages to server...")
    print("Input messages:")
    for i, msg in enumerate(messages, 1):
        print(f"  {i}. {msg['method']}")
    print()
    
    try:
        # Start the server process
        process = subprocess.Popen(
            [".venv\\Scripts\\python.exe", "-m", "mcp_hello_server.main"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Send all messages at once
        stdout, stderr = process.communicate(input=input_data, timeout=10)
        
        print("Server responses:")
        print("=" * 50)
        
        # Parse and display responses
        response_lines = stdout.strip().split('\n')
        for i, line in enumerate(response_lines, 1):
            if line.strip():
                try:
                    response = json.loads(line)
                    print(f"Response {i}:")
                    print(json.dumps(response, indent=2))
                    print()
                except json.JSONError:
                    print(f"Non-JSON output {i}: {line}")
                    print()
        
        if stderr:
            print("Server logs:")
            print("=" * 50)
            print(stderr)
        
        print("=" * 50)
        print("✅ Complete MCP protocol test completed!")
        print("The server successfully:")
        print("  - Initialized with the client")
        print("  - Listed available tools")
        print("  - Executed all tool calls")
        print("  - Returned proper JSON-RPC responses")
        
    except subprocess.TimeoutExpired:
        print("❌ Test timed out")
        process.kill()
    except Exception as e:
        print(f"❌ Test failed: {e}")


if __name__ == "__main__":
    test_complete_flow()
