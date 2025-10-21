#!/usr/bin/env python3
"""
MCP Client Demo - Demonstrates the complete MCP lifecycle
"""

import asyncio
import json
import subprocess
import sys
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass
class MCPTool:
    """Represents an MCP tool."""
    name: str
    description: str
    input_schema: Dict[str, Any]


class SimpleMCPClient:
    """A simple MCP client that demonstrates the complete MCP lifecycle."""
    
    def __init__(self, server_command: List[str], server_cwd: str = None):
        self.server_command = server_command
        self.server_cwd = server_cwd
        self.process: Optional[subprocess.Popen] = None
        self.tools: List[MCPTool] = []
        self.initialized = False
        self.request_id = 0
    
    def _get_next_id(self) -> int:
        """Get the next request ID."""
        self.request_id += 1
        return self.request_id
    
    async def start_server(self) -> bool:
        """Start the MCP server process."""
        print("🚀 Starting MCP server...")
        try:
            self.process = subprocess.Popen(
                self.server_command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=self.server_cwd
            )
            
            # Give the server a moment to start
            await asyncio.sleep(0.5)
            
            if self.process.poll() is None:
                print("✅ MCP server started successfully!")
                return True
            else:
                print("❌ MCP server failed to start")
                return False
                
        except Exception as e:
            print(f"❌ Error starting MCP server: {e}")
            return False
    
    async def send_request(self, method: str, params: Dict[str, Any] = None, request_id: int = None) -> Dict[str, Any]:
        """Send a JSON-RPC request to the MCP server."""
        if not self.process or self.process.poll() is not None:
            raise Exception("MCP server is not running")
        
        if request_id is None:
            request_id = self._get_next_id()
        
        request = {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": method
        }
        
        if params:
            request["params"] = params
        
        print(f"📤 Sending request: {method}")
        
        # Send the request
        self.process.stdin.write(json.dumps(request) + "\n")
        self.process.stdin.flush()
        
        # Read the response
        response_line = self.process.stdout.readline()
        if not response_line:
            raise Exception("No response from server")
        
        try:
            response_data = json.loads(response_line.strip())
            print(f"📥 Received response for {method}")
            return response_data
        except json.JSONError as e:
            raise Exception(f"Invalid JSON response: {e}")
    
    async def initialize(self) -> bool:
        """Initialize the MCP connection."""
        print("\n🤝 Initializing MCP connection...")
        
        try:
            response = await self.send_request(
                "initialize",
                {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {
                        "name": "simple-mcp-client",
                        "version": "1.0.0"
                    }
                }
            )
            
            if "error" in response:
                print(f"❌ Initialization failed: {response['error']}")
                return False
            
            print("✅ MCP connection initialized!")
            server_info = response.get("result", {}).get("serverInfo", {})
            print(f"   Server: {server_info.get('name', 'Unknown')}")
            print(f"   Version: {server_info.get('version', 'Unknown')}")
            
            # Send initialized notification
            notification = {
                "jsonrpc": "2.0",
                "method": "notifications/initialized"
            }
            print(f"📢 Sending notification: notifications/initialized")
            self.process.stdin.write(json.dumps(notification) + "\n")
            self.process.stdin.flush()
            
            self.initialized = True
            return True
            
        except Exception as e:
            print(f"❌ Initialization error: {e}")
            return False
    
    async def discover_tools(self) -> bool:
        """Discover available tools from the MCP server."""
        print("\n🔍 Discovering available tools...")
        
        try:
            response = await self.send_request("tools/list")
            
            if "error" in response:
                print(f"❌ Tool discovery failed: {response['error']}")
                return False
            
            tools_data = response.get("result", {}).get("tools", [])
            self.tools = []
            
            for tool_data in tools_data:
                tool = MCPTool(
                    name=tool_data["name"],
                    description=tool_data["description"],
                    input_schema=tool_data["inputSchema"]
                )
                self.tools.append(tool)
            
            print(f"✅ Found {len(self.tools)} tools:")
            for tool in self.tools:
                print(f"   • {tool.name}: {tool.description}")
            
            return True
            
        except Exception as e:
            print(f"❌ Tool discovery error: {e}")
            return False
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Optional[str]:
        """Call a tool with the given arguments."""
        print(f"\n🔧 Calling tool: {tool_name}")
        print(f"   Arguments: {arguments}")
        
        try:
            response = await self.send_request(
                "tools/call",
                {
                    "name": tool_name,
                    "arguments": arguments
                }
            )
            
            if "error" in response:
                print(f"❌ Tool call failed: {response['error']}")
                return None
            
            # Extract the result
            content = response.get("result", {}).get("content", [])
            if content and len(content) > 0:
                result_text = content[0].get("text", "")
                print(f"✅ Tool result: {result_text}")
                return result_text
            else:
                print("⚠️ Tool returned no content")
                return None
                
        except Exception as e:
            print(f"❌ Tool call error: {e}")
            return None
    
    async def cleanup(self):
        """Clean up resources."""
        print("\n🧹 Cleaning up...")
        if self.process:
            try:
                self.process.stdin.close()
                self.process.terminate()
                self.process.wait(timeout=5)
                print("✅ MCP server stopped")
            except:
                try:
                    self.process.kill()
                except:
                    pass


async def demo_lifecycle():
    """Demonstrate the complete MCP lifecycle."""
    print("🎯 MCP Client Lifecycle Demo")
    print("============================")
    
    # Configuration
    server_command = [".venv\\Scripts\\python.exe", "-m", "mcp_hello_server.main"]
    server_cwd = "C:\\dev\\code\\MCP-Server"
    
    client = SimpleMCPClient(server_command, server_cwd)
    
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
