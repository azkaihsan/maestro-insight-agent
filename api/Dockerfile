FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY api/ /app/api/
COPY data/ /app/data/
# Cloud Run expects the app to listen on the $PORT environment variable
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8080"]