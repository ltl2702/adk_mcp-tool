import sys
import os
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioConnectionParams, StdioServerParameters
 
MCP_SERVER_PATH = r"C:/Users/PC/Downloads/test/weather_agent/mcp_server.py"
 
 
simple_mcp_tools = MCPToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command=sys.executable,
            args=[MCP_SERVER_PATH],
            timeout=5.0
        )
    ),
    tool_filter=["get_alerts", "get_forecast"]
)
 
root_agent = LlmAgent(
    model="gemini-2.0-flash",
    name="echo_agent",
    instruction = """
    "You have access to 2 tools:\n"
    - 'get_alerts': Retrieve weather alerts from MCP server.
    - 'get_forecast': Retrieve weather forecast from MCP server.
    Use these tools to help the user with text processing or weather information as requested.
    """,
    tools=[simple_mcp_tools]
)  