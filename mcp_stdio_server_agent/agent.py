import os
from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.mcp_tool import StdioConnectionParams
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from mcp import StdioServerParameters
 
_allowed_path = os.path.dirname(os.path.abspath(__file__))
 
# Khởi tạo agent
root_agent = LlmAgent(
    model='gemini-2.0-flash',
    name='enterprise_assistant',
    instruction=f"""\
    You are an assistant that helps users explore and understand their file system.
 
    You are allowed to access this directory:
    {_allowed_path}
    """,
    tools=[
        MCPToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command='npx',
                    args=[
                        '-y',
                        '@modelcontextprotocol/server-filesystem',
                        _allowed_path,
                    ],
                ),
                timeout=40,
            ),
            tool_filter=[
                'read_file',
                'read_multiple_files',
                'list_directory',
                'directory_tree',
                'search_files',
                'get_file_info',
                'list_allowed_directories',
            ],
        )
    ],
)
 
 