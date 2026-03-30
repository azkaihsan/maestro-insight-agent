FROM python:3.11-slim
WORKDIR /app

# Ensure adk paths map correctly
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the agent code
COPY adk_agent/ /app/adk_agent/

# Start the ADK Web server on the Cloud Run mandated port
WORKDIR /app/adk_agent
CMD ["adk", "web", "--port", "8080", "--host", "0.0.0.0"]
