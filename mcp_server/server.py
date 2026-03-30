"""
Maestro Insight Agent — MCP Server

An MCP server that exposes the Student Mastery API as tools for the ADK agent.
Uses the official MCP Python SDK with FastMCP and Streamable HTTP transport.
"""

import json
import httpx
import os
from mcp.server.fastmcp import FastMCP

# Initialize the MCP server with host/port configuration
mcp = FastMCP(
    "Student Mastery MCP Server",
    instructions=(
        "This MCP server provides tools to query structured student learning data. "
        "Use these tools to retrieve student mastery profiles, misconceptions, "
        "difficulty scores, and identify struggling students."
    ),
    host="0.0.0.0",
    port=8001,
)

# Base URL for the Student Mastery REST API
API_BASE_URL = os.environ.get("STUDENT_API_URL", "http://localhost:8080")


@mcp.tool()
async def list_students() -> str:
    """
    List all students in the system with their summary information.
    Returns each student's ID, name, grade, subject, overall mastery score,
    and last assessment date. Use this tool first to discover available students
    before querying specific student details.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_BASE_URL}/students")
        response.raise_for_status()
        return json.dumps(response.json(), indent=2)


@mcp.tool()
async def get_student_profile(student_id: str) -> str:
    """
    Get the complete mastery profile for a specific student by their student ID
    (e.g., 'STU-001'). Returns all topics, mastery scores, difficulty scores,
    detected misconceptions, and learning status for each topic.
    Use this for a comprehensive overview of a student's learning progress.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_BASE_URL}/students/{student_id}")
        if response.status_code == 404:
            return json.dumps({"error": f"Student '{student_id}' not found. Use list_students to see available students."})
        response.raise_for_status()
        return json.dumps(response.json(), indent=2)


@mcp.tool()
async def get_student_misconceptions(student_id: str) -> str:
    """
    Get the detected misconceptions for a specific student by their student ID
    (e.g., 'STU-001'). Returns misconceptions grouped by topic, along with the
    difficulty score for each topic. Use this tool when the teacher asks about
    what a student is getting wrong or where they have misunderstandings.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_BASE_URL}/students/{student_id}/misconceptions")
        if response.status_code == 404:
            return json.dumps({"error": f"Student '{student_id}' not found. Use list_students to see available students."})
        response.raise_for_status()
        return json.dumps(response.json(), indent=2)


@mcp.tool()
async def get_struggling_topics(student_id: str) -> str:
    """
    Get the topics where a specific student is struggling (status = 'struggling')
    by their student ID (e.g., 'STU-001'). Returns only the topics with the lowest
    mastery and highest difficulty. Use this tool when the teacher asks where a
    student needs the most help or what areas require immediate intervention.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_BASE_URL}/students/{student_id}/struggling-topics")
        if response.status_code == 404:
            return json.dumps({"error": f"Student '{student_id}' not found. Use list_students to see available students."})
        response.raise_for_status()
        return json.dumps(response.json(), indent=2)


@mcp.tool()
async def search_student(name: str) -> str:
    """
    Search for a student by their name (supports partial, case-insensitive matching).
    For example, searching 'anya' will find 'Anya Sharma'.
    Returns the full mastery profile of all matching students.
    Use this tool when the teacher refers to a student by name rather than ID.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_BASE_URL}/students/search", params={"name": name})
        response.raise_for_status()
        return json.dumps(response.json(), indent=2)


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
