"""
Main entry point for the MCP Hello Server.
"""

import asyncio
import logging
from mcp_hello_server import main

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

if __name__ == "__main__":
    asyncio.run(main())
