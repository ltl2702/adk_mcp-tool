import sys
import os
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioConnectionParams, StdioServerParameters
 
MCP_SERVER_PATH = r"C:/Users/PC/Downloads/test/simple_agent/mcp_server.py"
 
 
simple_mcp_tools = MCPToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command=sys.executable,
            args=[MCP_SERVER_PATH],
            timeout=5.0
        )
    ),
    tool_filter=["echo_text", "reverse_text", "count_words", "uppercase_text"]
)
 
root_agent = LlmAgent(
    model="gemini-2.0-flash",
    name="echo_agent",
    instruction = """
    "You have access to four tools:\n"
    "- 'echo_text': Repeat back any text the user provides.\n"
    "- 'reverse_text': Return the reversed version of the input text.\n"
    "- 'count_words': Count how many words are in the input text.\n"
    "- 'uppercase_text': Convert the input text to uppercase.\n"
    "Use these tools to help the user manipulate or analyze text as requested."
    """,
    tools=[simple_mcp_tools]
)