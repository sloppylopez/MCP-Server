# Custom MCP Client - Understanding the Complete Lifecycle

This directory contains a custom MCP client that demonstrates the complete Model Context Protocol lifecycle. This is an excellent way to understand how MCP works under the hood!

## 🎯 What This Client Demonstrates

### **Complete MCP Lifecycle:**

1. **🚀 Process Management** - Starting and managing MCP server processes
2. **🤝 Protocol Handshake** - MCP initialization and capability negotiation  
3. **🔍 Tool Discovery** - Discovering available tools from the server
4. **🔧 Tool Execution** - Calling tools with parameters and handling responses
5. **🧹 Resource Cleanup** - Properly shutting down connections

### **Key Concepts Covered:**

- **JSON-RPC 2.0 Protocol** - The underlying communication protocol
- **Async Programming** - Using asyncio for non-blocking operations
- **Process Communication** - stdin/stdout communication with subprocess
- **Error Handling** - Robust error handling throughout the lifecycle
- **Interactive CLI** - User-friendly command-line interface

## 📁 Files Overview

### **`mcp_client/client.py`** - Full-Featured Client
- Complete MCP client implementation
- Interactive command-line interface
- Tool schema inspection
- Comprehensive error handling

### **`simple_demo.py`** - Simplified Demo
- Streamlined version for learning
- Step-by-step lifecycle demonstration
- Clear output and explanations

## 🚀 How to Run

### **Option 1: Simple Demo (Recommended for Learning)**
```bash
py simple_demo.py
```

This will:
1. Start your MCP Hello Server
2. Initialize the connection
3. Discover all 4 tools
4. Call each tool with sample parameters
5. Show the complete lifecycle in action

### **Option 2: Interactive Client**
```bash
py mcp_client/client.py
```

This gives you an interactive CLI where you can:
- List available tools
- Inspect tool schemas
- Call tools with custom parameters
- Explore the MCP protocol interactively

## 🔍 Understanding the MCP Lifecycle

### **Step 1: Process Management**
```python
# Start the MCP server as a subprocess
self.process = subprocess.Popen(
    [".venv\\Scripts\\python.exe", "-m", "mcp_hello_server.main"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)
```

**What happens:**
- Creates a subprocess running your MCP server
- Sets up stdin/stdout pipes for communication
- Server waits for JSON-RPC messages

### **Step 2: Protocol Handshake**
```python
# Initialize the MCP connection
response = await self.send_request("initialize", {
    "protocolVersion": "2024-11-05",
    "capabilities": {},
    "clientInfo": {"name": "custom-client", "version": "1.0.0"}
})

# Send initialized notification
await self.send_notification("notifications/initialized")
```

**What happens:**
- Client sends initialization request
- Server responds with capabilities and server info
- Client sends "initialized" notification
- Connection is established

### **Step 3: Tool Discovery**
```python
# Discover available tools
response = await self.send_request("tools/list")
tools_data = response["result"]["tools"]

for tool_data in tools_data:
    tool = MCPTool(
        name=tool_data["name"],
        description=tool_data["description"],
        input_schema=tool_data["inputSchema"]
    )
```

**What happens:**
- Client requests list of available tools
- Server responds with tool definitions
- Client parses tool schemas and capabilities

### **Step 4: Tool Execution**
```python
# Call a tool with parameters
response = await self.send_request("tools/call", {
    "name": "hello",
    "arguments": {"name": "Alice"}
})

result_text = response["result"]["content"][0]["text"]
```

**What happens:**
- Client sends tool call request with parameters
- Server validates parameters against schema
- Server executes the tool function
- Server returns structured result

### **Step 5: Cleanup**
```python
# Clean up resources
self.process.stdin.close()
self.process.terminate()
self.process.wait(timeout=5)
```

**What happens:**
- Close communication pipes
- Terminate server process
- Wait for graceful shutdown

## 🎮 Interactive Commands

When running the interactive client, you can use these commands:

```
mcp-client> list                    # List all available tools
mcp-client> info hello             # Show detailed info about 'hello' tool
mcp-client> call hello             # Call the 'hello' tool
mcp-client> quit                   # Exit the client
```

## 🔧 Example Tool Calls

### **Hello Tool**
```
mcp-client> call hello
Enter name (The name of the person to greet): Alice
✅ Tool result: Hello, Alice! Welcome to the MCP Hello Server!
```

### **Add Numbers Tool**
```
mcp-client> call add_numbers
Enter a (First number): 15
Enter b (Second number): 27
✅ Tool result: 15.0 + 27.0 = 42.0
```

### **Get Time Tool**
```
mcp-client> call get_time
✅ Tool result: Current time: 2024-01-15 14:30:25
```

## 🧠 Key Learning Points

### **1. JSON-RPC Protocol**
- All communication uses JSON-RPC 2.0
- Requests have `id`, `method`, and `params`
- Responses have `id`, `result` or `error`
- Notifications have no `id` and no response

### **2. Async Communication**
- Uses asyncio for non-blocking I/O
- Server can handle multiple requests concurrently
- Client can send requests without waiting for responses

### **3. Schema Validation**
- Tools define input schemas using JSON Schema
- Server validates parameters before execution
- Client can inspect schemas to build UIs

### **4. Error Handling**
- Network errors, protocol errors, and tool errors
- Graceful degradation and cleanup
- User-friendly error messages

### **5. Process Management**
- Server runs as separate process
- Communication via stdin/stdout
- Proper cleanup prevents zombie processes

## 🎯 Benefits of Understanding This

By studying this custom client, you'll understand:

- **How MCP clients work internally**
- **The complete protocol flow**
- **Error handling strategies**
- **Process communication patterns**
- **Async programming with MCP**

This knowledge will help you:
- Debug MCP connection issues
- Build better MCP clients
- Understand MCP server requirements
- Integrate MCP into your applications

## 🚀 Next Steps

1. **Run the demo** to see the lifecycle in action
2. **Try the interactive client** to explore tools
3. **Modify the code** to add new features
4. **Study the JSON-RPC messages** in detail
5. **Build your own MCP client** for specific needs

Happy learning! 🎉
