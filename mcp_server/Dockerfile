FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY mcp_server/ /app/mcp_server/
# Expose the port Cloud Run passes dynamically
CMD ["fastmcp", "run", "mcp_server/server.py", "--transport", "streamable-http", "--host", "0.0.0.0", "--port", "8080"]