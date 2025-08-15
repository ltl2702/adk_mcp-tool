import os
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

FINANCIAL_SERVER_SCRIPT_PATH = os.path.abspath("C:\\Users\\PC\\Downloads\\test\\financial_agent\\mcp-server.py")
print(f"Financial Advisory Agent connecting to: {FINANCIAL_SERVER_SCRIPT_PATH}")

MCP_COMMAND = 'python'  
MCP_ARGS = [
    FINANCIAL_SERVER_SCRIPT_PATH
]

root_agent = LlmAgent(
    model='gemini-2.0-flash',
    name='financial_advisor_agent',
    instruction=(
        'You are an automated financial advisor. '
        'You can retrieve real-time stock prices, historical financial statements, and company news. '
        'Use the available tools to answer questions about financial markets and companies.'
    ),
    tools=[
        MCPToolset(
            connection_params=StdioServerParameters(
                command=MCP_COMMAND,
                args=MCP_ARGS,
            ),
            tool_filter=['get_current_stock_price', 'get_company_news', 'get_historical_stock_prices',
                         'get_income_statements', 'get_balance_sheets', 'get_cash_flow_statements',
                         'get_available_crypto_tickers', 'get_crypto_prices', 'get_sec_fillings',
                         'get_current_crypto_price', 'get_historical_crypto_prices']  # Expose only specific tools
        )
    ]
)