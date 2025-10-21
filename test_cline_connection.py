#!/usr/bin/env python3
"""
Test script to verify Cline can connect to our MCP server
"""

import subprocess
import sys
import json
import time


def test_cline_connection():
    """Test if Cline can connect to our MCP server."""
    print("=== Testing Cline Connection to MCP Server ===")
    print()
    
    # Test the exact command that Cline will use
    command = [
        "C:\\dev\\code\\MCP-Server\\.venv\\Scripts\\python.exe",
        "-m", "mcp_hello_server.main"
    ]
    
    print(f"Testing command: {' '.join(command)}")
    print()
    
    # Prepare test messages
    messages = [
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "cline-test", "version": "1.0.0"}}},
        {"jsonrpc": "2.0", "method": "notifications/initialized"},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}
    ]
    
    input_data = "\n".join(json.dumps(msg) for msg in messages)
    
    try:
        # Start the server process
        process = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd="C:\\dev\\code\\MCP-Server"
        )
        
        # Send test messages
        stdout, stderr = process.communicate(input=input_data, timeout=10)
        
        print("✅ Server started successfully!")
        print("✅ Received responses:")
        
        # Parse responses
        response_lines = stdout.strip().split('\n')
        for i, line in enumerate(response_lines, 1):
            if line.strip():
                try:
                    response = json.loads(line)
                    if response.get("result", {}).get("tools"):
                        print(f"  ✅ Found {len(response['result']['tools'])} tools:")
                        for tool in response['result']['tools']:
                            print(f"    - {tool['name']}: {tool['description']}")
                    else:
                        print(f"  ✅ Response {i}: {response.get('method', 'Unknown')}")
                except json.JSONError:
                    print(f"  ✅ Non-JSON output {i}: {line}")
        
        if stderr:
            print("Server logs:")
            print(stderr)
        
        print()
        print("🎉 Cline should be able to connect to your MCP server!")
        print()
        print("Next steps:")
        print("1. Install Cline extension in Cursor")
        print("2. Add the MCP server configuration")
        print("3. Restart Cursor")
        print("4. Open a chat with Cline and try using the tools!")
        
    except subprocess.TimeoutExpired:
        print("❌ Test timed out")
        process.kill()
    except FileNotFoundError:
        print("❌ Python executable not found at the specified path")
        print("Make sure the virtual environment is set up correctly")
    except Exception as e:
        print(f"❌ Test failed: {e}")


if __name__ == "__main__":
    test_cline_connection()
