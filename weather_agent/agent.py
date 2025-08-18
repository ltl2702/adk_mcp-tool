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
        You have access to 2 tools:
        - 'get_alerts': Retrieve weather alerts from MCP server.
        - 'get_forecast': Retrieve weather forecast from MCP server.

        Instruction for the agent:

        1. When the user mentions a city or state name:
        - Convert the city/state name into the correct US state code and latitude/longitude.
        - If the input is a country name, assume they mean a location within the US and choose the appropriate state.
        - You may use an internal mapping or geocoding API to resolve names to coordinates/state codes.

        2. When the user asks for weather forecast:
        - Call 'get_forecast(latitude, longitude)' using the resolved coordinates.

        3. When the user asks for active weather alerts:
        - Call 'get_alerts(state_code)' using the resolved US state code.

        4. Always respond with human-readable weather or alert information returned by the tools.
        """,

    tools=[simple_mcp_tools]
)  