import asyncio
from mcp import types as mcp_types
from mcp.server.lowlevel import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
 
app = Server("simple-mcp-server")
 
# --- Tool Registry ---
@app.list_tools()
async def list_tools() -> list[mcp_types.Tool]:
    print("MCP Server: Advertising available tools.")
    return [
        mcp_types.Tool(
            name="echo_text",
            description="Trả lại chính chuỗi văn bản bạn gửi vào.",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Chuỗi cần echo"}
                },
                "required": ["text"]
            }
        ),
        mcp_types.Tool(
            name="reverse_text",
            description="Đảo ngược chuỗi văn bản.",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Chuỗi cần đảo ngược"}
                },
                "required": ["text"]
            }
        ),
        mcp_types.Tool(
            name="count_words",
            description="Đếm số từ trong chuỗi.",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Chuỗi cần đếm từ"}
                },
                "required": ["text"]
            }
        ),
        mcp_types.Tool(
            name="uppercase_text",
            description="Viết hoa toàn bộ chuỗi.",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Chuỗi cần viết hoa"}
                },
                "required": ["text"]
            }
        )
    ]
 
# --- Tool Execution ---
@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[mcp_types.Content]:
    text = arguments.get("text", "")
    if name == "echo_text":
        result = f"Echo: {text}"
    elif name == "reverse_text":
        result = f"Reversed: {text[::-1]}"
    elif name == "count_words":
        word_count = len(text.strip().split())
        result = f"Word count: {word_count}"
    elif name == "uppercase_text":
        result = f"Uppercase: {text.upper()}"
    else:
        result = f"Tool '{name}' không tồn tại."
 
    return [mcp_types.TextContent(type="text", text=result)]
 
# --- MCP Server Runner ---
async def run_mcp_stdio_server():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name=app.name,
                server_version="0.1.0",
                capabilities=app.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )
 
if __name__ == "__main__":
    asyncio.run(run_mcp_stdio_server())
 
 