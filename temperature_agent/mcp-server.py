# import asyncio
# from mcp import types as mcp_types
# from mcp.server.lowlevel import Server, NotificationOptions
# from mcp.server.models import InitializationOptions
# import mcp.server.stdio

# from google.adk.tools.function_tool import FunctionTool
# from google.adk.tools.mcp_tool.conversion_utils import adk_to_mcp_tool_type

# async def convert_celsius_to_fahrenheit(celsius: float) -> str:
#     """
#     Converts a temperature from Celsius to Fahrenheit.
#     Args:
#         celsius: The temperature in Celsius.
#     Returns:
#         The temperature in Fahrenheit as a formatted string.
#     """

#     fahrenheit = (celsius * 9/5) + 32
#     return f"{celsius}C is {fahrenheit:.2f}F."


# print("Initializing ADK 'convert_celsius_to_fahrenheit' tool...")
# adk_tool_to_expose = FunctionTool(convert_celsius_to_fahrenheit)
# print(f"ADK tool '{adk_tool_to_expose.name}' initialized and ready to be exposed via MCP.")

# # Create MCP Server instance
# print("Creating MCP Server instance...")
# app = Server("adk-unit-conversion-mcp-server")

# # Handler to list tools
# @app.list_tools()
# async def list_mcp_tools() -> list[mcp_types.Tool]:
#     print("MCP Server: Received list_tools request.")
#     mcp_tool_schema = adk_to_mcp_tool_type(adk_tool_to_expose)
#     return [mcp_tool_schema]

# # Handler to call a tool
# @app.call_tool()
# async def call_mcp_tool(name: str, arguments: dict) -> list[mcp_types.TextContent]:
#     print(f"MCP Server: Received call_tool request for '{name}' with args: {arguments}")
#     if name == adk_tool_to_expose.name:
#         try:
#             response = await adk_tool_to_expose.run_async(tool_context=None, args=arguments)
#             return [mcp_types.TextContent(type="text", text=response)]
#         except Exception as e:
#             return [mcp_types.TextContent(type="text", text=f"Failed to execute tool '{name}': {str(e)}")]
#     else:
#         return [mcp_types.TextContent(type="text", text=f"Tool '{name}' not implemented by this server.")]
    
# async def run_mcp_stdio_server():
#     async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
#         print("MCP Stdio Server: Starting handshake with client...")
#         await app.run(
#             read_stream,
#             write_stream,
#             InitializationOptions(
#                 server_name=app.name,
#                 server_version="0.1.0",
#                 capabilities=app.get_capabilities(
#                     notification_options=NotificationOptions(),
#                     experimental_capabilities={},
#                 ),
#             ),
#         )
        
# if __name__ == "__main__":
#     print("Launching MCP Server to expose ADK tools via stdio...")
#     try:
#         asyncio.run(run_mcp_stdio_server())
#     except KeyboardInterrupt:
#         print("\nMCP Server (stdio) stopped by user.")
#     except Exception as e:
#         print(f"MCP Server (stdio) encountered an error: {e}")
#     finally:
#         print("MCP Server (stdio) process exiting.")

import logging
import sys
from mcp.server.fastmcp import FastMCP

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("temperature-mcp")

# Initialize FastMCP server
mcp = FastMCP("temperature_agent")


# Expose the tool via MCP
# FastMCP server
@mcp.tool()
async def convert_celsius_to_fahrenheit(celsius: float) -> str:
    """
    Convert a temperature from Celsius to Fahrenheit.

    Args:
        celsius (float): Temperature in degrees Celsius.

    Returns:
        str: A formatted string showing the Celsius input and the converted Fahrenheit value.
             Example: "34C is 93.20F."
    """
    fahrenheit = (celsius * 9 / 5) + 32
    return f"{celsius}C is {fahrenheit:.2f}F."


# Run server
if __name__ == "__main__":
    logger.info("Starting Temperature MCP Server...")
    mcp.run(transport="stdio")  
    logger.info("Temperature MCP Server stopped")
