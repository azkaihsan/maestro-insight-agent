"""
Maestro Insight Agent — Startup Script

Starts all three services:
  1. Mock Student Mastery REST API (port 8080)
  2. MCP Server (port 8001)
  3. ADK Web UI (port 8000)

Usage:
    python start.py
"""

import subprocess
import sys
import time
import os
from pathlib import Path

import dotenv


def main():
    # Load .env into the current process environment (override ensures we overwrite blank shell vars)
    env_path = Path(__file__).parent / ".env"
    dotenv.load_dotenv(env_path, override=True)

    project_root = os.path.dirname(os.path.abspath(__file__))
    processes = []

    try:
        print("=" * 60)
        print("  🎓 Maestro Insight Agent — Starting Services")
        print("=" * 60)
        print()

        # Start the Mock REST API (port 8080)
        print("📡 Starting Student Mastery REST API on http://localhost:8080 ...")
        api_process = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8080"],
            cwd=project_root,
            env=os.environ.copy(),
        )
        processes.append(api_process)
        time.sleep(2)

        # Start the MCP Server (port 8001)
        print("🔧 Starting MCP Server on http://localhost:8001 ...")
        mcp_process = subprocess.Popen(
            [sys.executable, "mcp_server/server.py"],
            cwd=project_root,
            env=os.environ.copy(),
        )
        processes.append(mcp_process)
        time.sleep(2)

        # Start the ADK Web UI (port 8000)
        print("🤖 Starting ADK Web UI on http://localhost:8000 ...")
        adk_exe = os.path.join(project_root, ".venv", "Scripts", "adk.exe")
        adk_process = subprocess.Popen(
            [adk_exe, "web"],
            cwd=os.path.join(project_root, "adk_agent"),
            env=os.environ.copy(),
        )
        processes.append(adk_process)
        time.sleep(3)

        print()
        print("=" * 60)
        print("  ✅ All services are running!")
        print("=" * 60)
        print()
        print("  📡 REST API:    http://localhost:8080")
        print("  🔧 MCP Server:  http://localhost:8001")
        print("  🤖 ADK Web UI:  http://localhost:8000")
        print()
        print("  Open http://localhost:8000 in your browser to chat!")
        print()
        print("  Press Ctrl+C to stop all services.")
        print("=" * 60)

        # Wait for processes
        for p in processes:
            p.wait()

    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down all services...")
        for p in processes:
            p.terminate()
        for p in processes:
            p.wait()
        print("✅ All services stopped.")


if __name__ == "__main__":
    main()
