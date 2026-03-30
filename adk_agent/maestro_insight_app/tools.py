"""
Maestro Insight Agent — MCP Tool Configuration

Configures the MCPToolset to connect to the local Student Mastery MCP server.
"""

from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StreamableHTTPConnectionParams


import os
MCP_URL = os.environ.get("MCP_SERVICE_URL", "http://localhost:8001/mcp")

def get_mastery_mcp_toolset():
    return MCPToolset(
        connection_params=StreamableHTTPConnectionParams(
            url=MCP_URL,
            timeout=30.0,
            sse_read_timeout=300.0,
        )
    )


def get_mastery_mcp_toolset():
    """
    Create and return an MCPToolset connected to the local Student Mastery MCP server.
    The MCP server must be running on port 8001 before starting the ADK agent.
    """
    tools = MCPToolset(
        connection_params=StreamableHTTPConnectionParams(
            url=MCP_SERVER_URL,
            timeout=30.0,
            sse_read_timeout=300.0,
        )
    )
    print(f"MCP Toolset configured for Student Mastery server at {MCP_SERVER_URL}")
    return tools
