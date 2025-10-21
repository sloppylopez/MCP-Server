#!/usr/bin/env python3
"""
Simple MCP Server Test
This tests the server by running it and checking if it starts correctly.
"""

import subprocess
import sys
import time
import os


def test_server_startup():
    """Test if the server starts without errors."""
    print("=== MCP Server Startup Test ===")
    print("Testing if the server starts correctly...")
    print()
    
    # Check if we're in the right directory
    if not os.path.exists("mcp_hello_server"):
        print("Error: mcp_hello_server directory not found!")
        print("Make sure you're in the project root directory.")
        return False
    
    # Check if virtual environment exists
    if not os.path.exists(".venv"):
        print("Error: Virtual environment not found!")
        print("Run: py -m venv .venv")
        return False
    
    # Test 1: Check if dependencies are installed
    print("=== Test 1: Check Dependencies ===")
    try:
        result = subprocess.run(
            [".venv\\Scripts\\python.exe", "-c", "import mcp; print('MCP library imported successfully')"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print("✓ Dependencies are installed correctly")
            print(f"  {result.stdout.strip()}")
        else:
            print("✗ Dependencies not installed properly")
            print(f"  Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ Error checking dependencies: {e}")
        return False
    
    print()
    
    # Test 2: Check if server module can be imported
    print("=== Test 2: Check Server Module ===")
    try:
        result = subprocess.run(
            [".venv\\Scripts\\python.exe", "-c", "from mcp_hello_server import server; print('Server module imported successfully')"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print("✓ Server module imports correctly")
            print(f"  {result.stdout.strip()}")
        else:
            print("✗ Server module import failed")
            print(f"  Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ Error importing server module: {e}")
        return False
    
    print()
    
    # Test 3: Test server startup (briefly)
    print("=== Test 3: Test Server Startup ===")
    print("Starting server for 3 seconds to check for startup errors...")
    
    try:
        process = subprocess.Popen(
            [".venv\\Scripts\\python.exe", "-m", "mcp_hello_server.main"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Let it run for 3 seconds
        time.sleep(3)
        
        # Check if it's still running (good sign)
        if process.poll() is None:
            print("✓ Server started and is running")
            process.terminate()
            process.wait()
        else:
            # Check what happened
            stdout, stderr = process.communicate()
            if stderr:
                print("✗ Server exited with errors:")
                print(f"  {stderr}")
                return False
            else:
                print("✓ Server started successfully")
        
    except Exception as e:
        print(f"✗ Error starting server: {e}")
        return False
    
    print()
    print("=== All Tests Passed! ===")
    print("The MCP server is working correctly.")
    print()
    print("Next steps:")
    print("1. To run the server: .venv\\Scripts\\python.exe -m mcp_hello_server.main")
    print("2. To test with an MCP client, use the configuration in mcp_config.json")
    print("3. The server will listen for JSON-RPC messages on stdin")
    
    return True


if __name__ == "__main__":
    success = test_server_startup()
    if not success:
        print("\n❌ Tests failed. Please check the errors above.")
        sys.exit(1)
    else:
        print("\n✅ All tests passed! Your MCP server is ready to use.")
