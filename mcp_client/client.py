#!/usr/bin/env python3
"""
Custom MCP Client - A simple client to understand the MCP lifecycle

This client demonstrates:
1. Starting an MCP server process
2. MCP protocol handshake (initialize)
3. Tool discovery (list tools)
4. Tool calling with user interaction
5. Error handling and cleanup
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


@dataclass
class MCPResponse:
    """Represents an MCP response."""
    id: Optional[int]
    result: Optional[Dict[str, Any]]
    error: Optional[Dict[str, Any]]
    method: Optional[str]


class MCPClient:
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
    
    async def send_request(self, method: str, params: Dict[str, Any] = None, request_id: int = None) -> MCPResponse:
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
            response = MCPResponse(
                id=response_data.get("id"),
                result=response_data.get("result"),
                error=response_data.get("error"),
                method=response_data.get("method")
            )
            
            if response.error:
                print(f"❌ Server error: {response.error}")
            else:
                print(f"📥 Received response for {method}")
            
            return response
            
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
                        "name": "custom-mcp-client",
                        "version": "1.0.0"
                    }
                }
            )
            
            if response.error:
                print(f"❌ Initialization failed: {response.error}")
                return False
            
            print("✅ MCP connection initialized!")
            print(f"   Server: {response.result.get('serverInfo', {}).get('name', 'Unknown')}")
            print(f"   Version: {response.result.get('serverInfo', {}).get('version', 'Unknown')}")
            
            # Send initialized notification
            await self.send_notification("notifications/initialized")
            self.initialized = True
            return True
            
        except Exception as e:
            print(f"❌ Initialization error: {e}")
            return False
    
    async def send_notification(self, method: str) -> None:
        """Send a notification (no response expected)."""
        notification = {
            "jsonrpc": "2.0",
            "method": method
        }
        
        print(f"📢 Sending notification: {method}")
        self.process.stdin.write(json.dumps(notification) + "\n")
        self.process.stdin.flush()
    
    async def discover_tools(self) -> bool:
        """Discover available tools from the MCP server."""
        print("\n🔍 Discovering available tools...")
        
        try:
            response = await self.send_request("tools/list")
            
            if response.error:
                print(f"❌ Tool discovery failed: {response.error}")
                return False
            
            tools_data = response.result.get("tools", [])
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
            
            if response.error:
                print(f"❌ Tool call failed: {response.error}")
                return None
            
            # Extract the result
            content = response.result.get("content", [])
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
    
    def get_tool_by_name(self, name: str) -> Optional[MCPTool]:
        """Get a tool by its name."""
        for tool in self.tools:
            if tool.name == name:
                return tool
        return None
    
    def print_tool_schema(self, tool: MCPTool):
        """Print the input schema for a tool."""
        print(f"\n📋 Tool: {tool.name}")
        print(f"   Description: {tool.description}")
        
        schema = tool.input_schema
        properties = schema.get("properties", {})
        required = schema.get("required", [])
        
        if properties:
            print("   Parameters:")
            for param_name, param_info in properties.items():
                param_type = param_info.get("type", "unknown")
                param_desc = param_info.get("description", "No description")
                is_required = param_name in required
                required_text = " (required)" if is_required else " (optional)"
                print(f"     • {param_name} ({param_type}){required_text}: {param_desc}")
        else:
            print("   Parameters: None")
    
    async def interactive_mode(self):
        """Run the client in interactive mode."""
        print("\n🎮 Interactive Mode")
        print("Commands:")
        print("  list                    - List available tools")
        print("  info <tool_name>        - Show tool information")
        print("  call <tool_name>        - Call a tool")
        print("  quit                    - Exit the client")
        print()
        
        while True:
            try:
                command = input("mcp-client> ").strip()
                
                if command == "quit":
                    break
                elif command == "list":
                    print("\nAvailable tools:")
                    for tool in self.tools:
                        print(f"  • {tool.name}: {tool.description}")
                elif command.startswith("info "):
                    tool_name = command[5:].strip()
                    tool = self.get_tool_by_name(tool_name)
                    if tool:
                        self.print_tool_schema(tool)
                    else:
                        print(f"❌ Tool '{tool_name}' not found")
                elif command.startswith("call "):
                    tool_name = command[5:].strip()
                    tool = self.get_tool_by_name(tool_name)
                    if not tool:
                        print(f"❌ Tool '{tool_name}' not found")
                        continue
                    
                    # Get arguments from user
                    arguments = {}
                    schema = tool.input_schema
                    properties = schema.get("properties", {})
                    required = schema.get("required", [])
                    
                    for param_name, param_info in properties.items():
                        param_type = param_info.get("type", "string")
                        param_desc = param_info.get("description", "")
                        is_required = param_name in required
                        
                        prompt = f"Enter {param_name}"
                        if param_desc:
                            prompt += f" ({param_desc})"
                        if not is_required:
                            prompt += " [optional]"
                        prompt += ": "
                        
                        value = input(prompt).strip()
                        
                        if value:
                            # Convert to appropriate type
                            if param_type == "number":
                                try:
                                    arguments[param_name] = float(value)
                                except ValueError:
                                    print(f"❌ Invalid number: {value}")
                                    break
                            else:
                                arguments[param_name] = value
                        elif is_required:
                            print(f"❌ Required parameter '{param_name}' not provided")
                            break
                    
                    if len(arguments) == len([p for p in properties.keys() if p in arguments or p not in required]):
                        await self.call_tool(tool_name, arguments)
                else:
                    print("❌ Unknown command. Type 'quit' to exit.")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
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


async def main():
    """Main function to run the MCP client."""
    print("🎯 Custom MCP Client")
    print("===================")
    
    # Configuration
    server_command = [".venv\\Scripts\\python.exe", "-m", "mcp_hello_server.main"]
    server_cwd = "C:\\dev\\code\\MCP-Server"
    
    client = MCPClient(server_command, server_cwd)
    
    try:
        # Step 1: Start the server
        if not await client.start_server():
            return
        
        # Step 2: Initialize the connection
        if not await client.initialize():
            return
        
        # Step 3: Discover tools
        if not await client.discover_tools():
            return
        
        # Step 4: Run interactive mode
        await client.interactive_mode()
        
    except Exception as e:
        print(f"❌ Client error: {e}")
    finally:
        await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
