import os
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

UNIT_CONVERTER_SERVER_PATH = os.path.abspath("C:\\Users\\PC\\Downloads\\test\\temperature_agent\\mcp-server.py")
print(f"Unit Converter Agent connecting to: {UNIT_CONVERTER_SERVER_PATH}")

# Configure how to launch the server
MCP_COMMAND = 'python' 
MCP_ARGS = [
    UNIT_CONVERTER_SERVER_PATH
]

# Set up the ADK agent that will use the external tool
root_agent = LlmAgent(
    model='gemini-2.0-flash',
    name='unit_conversion_agent', 
    instruction=(
        "You are a helpful unit conversion assistant. "
        "You **must always use the 'convert_celsius_to_fahrenheit' tool** to answer any temperature conversion questions. "
        "Do not calculate conversions yourself. Return only the result from the tool."
    )
    ,
    tools=[
        MCPToolset(
            connection_params=StdioServerParameters(
                    command=MCP_COMMAND,
                    args=MCP_ARGS,
                    timeout=30.0
                    
                ),
                tool_filter=['convert_celsius_to_fahrenheit']
        )
    ]  
)

#example: what is 34 degree celsius in Farenheit
