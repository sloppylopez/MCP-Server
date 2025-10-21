#!/usr/bin/env python3
"""
Simple test script for the MCP Hello Server.
This script demonstrates how to interact with the MCP server programmatically.
"""

import asyncio
import json
import subprocess
import sys
from typing import Dict, Any


async def test_mcp_server():
    """Test the MCP server by sending requests and checking responses."""
    print("Testing MCP Hello Server...")
    
    # Start the server process
    process = subprocess.Popen(
        [sys.executable, "-m", "mcp_hello_server.main"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    try:
        # Send initialization request
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }
        
        print("Sending initialization request...")
        process.stdin.write(json.dumps(init_request) + "\n")
        process.stdin.flush()
        
        # Read initialization response
        response_line = process.stdout.readline()
        if response_line:
            response = json.loads(response_line.strip())
            print(f"Initialization response: {response}")
        
        # Send initialized notification
        initialized_notification = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized"
        }
        
        print("Sending initialized notification...")
        process.stdin.write(json.dumps(initialized_notification) + "\n")
        process.stdin.flush()
        
        # Test list tools
        list_tools_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list"
        }
        
        print("Testing list tools...")
        process.stdin.write(json.dumps(list_tools_request) + "\n")
        process.stdin.flush()
        
        response_line = process.stdout.readline()
        if response_line:
            response = json.loads(response_line.strip())
            print(f"Tools list: {json.dumps(response, indent=2)}")
        
        # Test hello tool
        hello_request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "hello",
                "arguments": {
                    "name": "Test User"
                }
            }
        }
        
        print("Testing hello tool...")
        process.stdin.write(json.dumps(hello_request) + "\n")
        process.stdin.flush()
        
        response_line = process.stdout.readline()
        if response_line:
            response = json.loads(response_line.strip())
            print(f"Hello response: {json.dumps(response, indent=2)}")
        
        # Test echo tool
        echo_request = {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {
                "name": "echo",
                "arguments": {
                    "message": "Hello, MCP!"
                }
            }
        }
        
        print("Testing echo tool...")
        process.stdin.write(json.dumps(echo_request) + "\n")
        process.stdin.flush()
        
        response_line = process.stdout.readline()
        if response_line:
            response = json.loads(response_line.strip())
            print(f"Echo response: {json.dumps(response, indent=2)}")
        
        print("All tests completed successfully!")
        
    except Exception as e:
        print(f"Error during testing: {e}")
    finally:
        # Clean up
        process.stdin.close()
        process.terminate()
        process.wait()


if __name__ == "__main__":
    asyncio.run(test_mcp_server())
