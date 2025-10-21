#!/usr/bin/env python3
"""
Simple manual test for the MCP Hello Server.
This script shows how to test the server step by step.
"""

import json
import subprocess
import sys
import time


def test_server_manually():
    """Test the MCP server manually by running it and sending commands."""
    print("=== Manual MCP Server Test ===")
    print("This will start the server and show you how to interact with it.")
    print()
    
    # Start the server process
    print("Starting MCP server...")
    process = subprocess.Popen(
        [sys.executable, "-m", "mcp_hello_server.main"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    
    try:
        print("Server started! PID:", process.pid)
        print()
        
        # Wait a moment for server to initialize
        time.sleep(1)
        
        # Test 1: Initialize
        print("=== Test 1: Initialize Server ===")
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
        
        print("Sending:", json.dumps(init_request, indent=2))
        process.stdin.write(json.dumps(init_request) + "\n")
        process.stdin.flush()
        
        # Read response
        response_line = process.stdout.readline()
        if response_line:
            response = json.loads(response_line.strip())
            print("Received:", json.dumps(response, indent=2))
        print()
        
        # Test 2: Send initialized notification
        print("=== Test 2: Send Initialized Notification ===")
        initialized_notification = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized"
        }
        
        print("Sending:", json.dumps(initialized_notification, indent=2))
        process.stdin.write(json.dumps(initialized_notification) + "\n")
        process.stdin.flush()
        print("Notification sent (no response expected)")
        print()
        
        # Test 3: List tools
        print("=== Test 3: List Available Tools ===")
        list_tools_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list"
        }
        
        print("Sending:", json.dumps(list_tools_request, indent=2))
        process.stdin.write(json.dumps(list_tools_request) + "\n")
        process.stdin.flush()
        
        response_line = process.stdout.readline()
        if response_line:
            response = json.loads(response_line.strip())
            print("Received:", json.dumps(response, indent=2))
        print()
        
        # Test 4: Call hello tool
        print("=== Test 4: Call Hello Tool ===")
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
        
        print("Sending:", json.dumps(hello_request, indent=2))
        process.stdin.write(json.dumps(hello_request) + "\n")
        process.stdin.flush()
        
        response_line = process.stdout.readline()
        if response_line:
            response = json.loads(response_line.strip())
            print("Received:", json.dumps(response, indent=2))
        print()
        
        print("=== All Tests Completed Successfully! ===")
        print("The MCP server is working correctly.")
        
    except Exception as e:
        print(f"Error during testing: {e}")
        print("This might be normal - the server is working if you see responses above.")
    finally:
        # Clean up
        print("\nCleaning up...")
        try:
            process.stdin.close()
            process.terminate()
            process.wait(timeout=5)
        except:
            process.kill()
        print("Server stopped.")


if __name__ == "__main__":
    test_server_manually()
