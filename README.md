# MCP Hello Server

A simple Model Context Protocol (MCP) server implementation in Python that provides basic tools for greeting, echoing messages, getting time, and performing arithmetic operations.

## What is MCP?

Model Context Protocol (MCP) is a standardized protocol that allows AI models and clients to communicate with external tools and services. Think of it as a universal language that enables AI assistants to:

- **Discover** what tools are available on a server
- **Call** those tools with specific parameters
- **Receive** structured results back

This creates a bridge between AI systems and external functionality, making it easy to extend AI capabilities with custom tools.

## How It Works

### Architecture Overview

The MCP server follows a simple but powerful architecture:

```
┌─────────────────┐    JSON-RPC     ┌─────────────────┐
│   MCP Client    │ ◄─────────────► │   MCP Server    │
│   (AI Model)    │    Messages     │  (Our Python    │
│                 │                 │   Application)  │
└─────────────────┘                 └─────────────────┘
```

### Core Components

#### 1. Server Instance
```python
server = Server("mcp-hello-server")
```
The server is the central component that manages tool registration, handles client connections, and processes tool calls.

#### 2. Tool Registration System
```python
@server.list_tools()
async def list_tools() -> List[Tool]:
    return [
        Tool(
            name="hello",
            description="Say hello to someone",
            inputSchema={...}
        )
    ]
```
This decorator tells the server: "When a client asks what tools you have, return this list." Each tool includes:
- **name**: How to call it
- **description**: What it does  
- **inputSchema**: What parameters it expects (JSON schema)

#### 3. Tool Execution System
```python
@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    if name == "hello":
        name_arg = arguments.get("name", "World")
        message = f"Hello, {name_arg}! Welcome to the MCP Hello Server!"
        return [TextContent(type="text", text=message)]
```
This decorator handles actual tool execution:
- Receives the tool name and arguments
- Performs the requested action
- Returns structured results

#### 4. Communication Protocol
The server uses **stdio transport** - it communicates through standard input/output:
```python
async with stdio_server() as (read_stream, write_stream):
    await server.run(read_stream, write_stream, ...)
```
This means:
- Client sends JSON-RPC messages via stdin
- Server responds via stdout
- No network ports needed - just process communication

### Message Flow Example

Here's what happens when you call the "hello" tool:

**Step 1: Client asks "What tools do you have?"**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list"
}
```

**Step 2: Server responds with tool list**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "tools": [
      {
        "name": "hello",
        "description": "Say hello to someone",
        "inputSchema": {
          "type": "object",
          "properties": {
            "name": {
              "type": "string",
              "description": "The name of the person to greet"
            }
          },
          "required": ["name"]
        }
      }
    ]
  }
}
```

**Step 3: Client calls the hello tool**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "hello",
    "arguments": {
      "name": "Alice"
    }
  }
}
```

**Step 4: Server executes and responds**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Hello, Alice! Welcome to the MCP Hello Server!"
      }
    ]
  }
}
```

### Key Technical Features

#### Async Architecture
Everything is asynchronous for better performance:
- `async def` functions handle requests
- `asyncio.run(main())` starts the event loop
- Multiple requests can be handled concurrently

#### Error Handling
The server includes comprehensive error handling:
```python
except (ValueError, TypeError) as e:
    return [TextContent(type="text", text=f"Error: Invalid numbers provided - {str(e)}")]
```

#### Logging System
Built-in logging helps with debugging:
```python
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info(f"Tool called: {name} with arguments: {arguments}")
```

#### Type Safety
Uses Pydantic models for validation and type safety throughout the application.

### Benefits of This Architecture

1. **Standardized**: Uses MCP protocol - works with any MCP-compatible client
2. **Extensible**: Easy to add new tools by adding more `Tool` definitions
3. **Type-safe**: Uses Pydantic models for validation
4. **Async**: Can handle multiple requests efficiently
5. **Simple**: No complex networking - just stdin/stdout communication
6. **Debuggable**: Comprehensive logging and error handling

## Features

This MCP server provides the following tools:

- **hello**: Say hello to someone by name
- **echo**: Echo back any message you provide
- **get_time**: Get the current date and time
- **add_numbers**: Add two numbers together

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. Clone or download this repository
2. Create a virtual environment:
   ```bash
   py -m venv .venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Testing Locally

### Quick Test

Run the simple test script to verify everything is working:

```bash
py test_simple.py
```

This will check:
- ✅ Dependencies are installed correctly
- ✅ Server module imports without errors
- ✅ Server starts without crashing

### Manual Testing

#### Method 1: Run the Server Directly

1. **Start the server:**
   ```bash
   .venv\Scripts\python.exe -m mcp_hello_server.main
   ```

2. **The server will start and wait for JSON-RPC messages on stdin.** You'll see:
   ```
   INFO:mcp_hello_server:Starting MCP Hello Server...
   ```

3. **Test with JSON-RPC messages** (you can copy-paste these):

   **Initialize the server:**
   ```json
   {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test-client", "version": "1.0.0"}}}
   ```

   **Send initialized notification:**
   ```json
   {"jsonrpc": "2.0", "method": "notifications/initialized"}
   ```

   **List available tools:**
   ```json
   {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}
   ```

   **Call the hello tool:**
   ```json
   {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "hello", "arguments": {"name": "Test User"}}}
   ```

   **Call the echo tool:**
   ```json
   {"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "echo", "arguments": {"message": "Hello, MCP!"}}}
   ```

4. **Stop the server:** Press `Ctrl+C`

#### Method 2: Test with MCP Client

1. **Configure an MCP client** (like Claude Desktop) with the configuration in `mcp_config.json`:
   ```json
   {
     "mcpServers": {
       "mcp-hello-server": {
         "command": ".venv\\Scripts\\python.exe",
         "args": ["-m", "mcp_hello_server.main"],
         "env": {}
       }
     }
   }
   ```

2. **The client will automatically:**
   - Start the server process
   - Send initialization messages
   - Discover available tools
   - Allow you to call tools through the client interface

#### Method 3: Interactive Testing

For a more interactive experience, you can use the test script:

```bash
py test_interactive.py
```

This tests the server functions directly without the stdio transport.

### Expected Responses

When testing manually, you should see responses like:

**Tools list response:**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "tools": [
      {
        "name": "hello",
        "description": "Say hello to someone",
        "inputSchema": {...}
      },
      {
        "name": "echo", 
        "description": "Echo back the provided message",
        "inputSchema": {...}
      }
    ]
  }
}
```

**Hello tool response:**
```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Hello, Test User! Welcome to the MCP Hello Server!"
      }
    ]
  }
}
```

### Troubleshooting

**Server exits immediately:**
- This is normal! MCP servers wait for JSON-RPC messages on stdin
- The server is working if you see the startup log message

**Import errors:**
- Make sure you activated the virtual environment: `.venv\Scripts\activate`
- Verify dependencies are installed: `pip list | grep mcp`

**Permission errors:**
- On Windows, make sure you're using `.venv\Scripts\python.exe` instead of just `python`
- Check that the virtual environment was created successfully

## Usage

### Running the Server

You can run the MCP server directly:

```bash
py -m mcp_hello_server.main
```

Or using the installed package:

```bash
mcp-hello-server
```

### MCP Client Configuration

To use this server with an MCP client, add the following configuration to your MCP client's configuration file:

```json
{
  "mcpServers": {
    "mcp-hello-server": {
      "command": "py",
      "args": ["-m", "mcp_hello_server.main"],
      "env": {}
    }
  }
}
```

Make sure to adjust the `command` and `args` based on your Python installation and virtual environment setup.

### Available Tools

#### hello
Greets a person by name.

**Parameters:**
- `name` (string, required): The name of the person to greet

**Example:**
```json
{
  "name": "hello",
  "arguments": {
    "name": "Alice"
  }
}
```

**Response:**
```
Hello, Alice! Welcome to the MCP Hello Server!
```

#### echo
Echoes back the provided message.

**Parameters:**
- `message` (string, required): The message to echo back

**Example:**
```json
{
  "name": "echo",
  "arguments": {
    "message": "Hello, MCP!"
  }
}
```

**Response:**
```
Echo: Hello, MCP!
```

#### get_time
Returns the current date and time.

**Parameters:** None

**Example:**
```json
{
  "name": "get_time",
  "arguments": {}
}
```

**Response:**
```
Current time: 2024-01-15 14:30:25
```

#### add_numbers
Adds two numbers together.

**Parameters:**
- `a` (number, required): First number
- `b` (number, required): Second number

**Example:**
```json
{
  "name": "add_numbers",
  "arguments": {
    "a": 5,
    "b": 3
  }
}
```

**Response:**
```
5 + 3 = 8
```

## Development

### Project Structure

```
MCP-Server/
├── mcp_hello_server/
│   ├── __init__.py      # Main server implementation
│   └── main.py          # Entry point
├── requirements.txt     # Python dependencies
├── pyproject.toml       # Project configuration
├── mcp_config.json     # MCP client configuration example
└── README.md           # This file
```

### Adding New Tools

To add new tools to the server:

1. Add the tool definition to the `list_tools()` function in `mcp_hello_server/__init__.py`
2. Add the tool implementation to the `call_tool()` function in the same file
3. Update this README with the new tool's documentation

### Testing

You can test the server by running it and using an MCP client to interact with it. The server uses stdio transport, so it communicates through standard input/output.

## Troubleshooting

### Common Issues

1. **Import errors**: Make sure you've installed all dependencies with `pip install -r requirements.txt`
2. **Permission errors**: Ensure you have the necessary permissions to run Python scripts
3. **Virtual environment**: Make sure you've activated your virtual environment before running the server

### Logging

The server logs important events to help with debugging. Logs include:
- Server startup messages
- Tool call requests and responses
- Error messages

## License

This project is licensed under the MIT License.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this MCP server implementation.
