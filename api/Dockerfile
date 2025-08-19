FROM python:3.12-slim

# System dependencies for psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY app /app/app

# Install dependencies
RUN pip install --no-cache-dir fastapi uvicorn psycopg2-binary

# Env defaults (overridden in k8s)
ENV DB_HOST=localhost DB_PORT=5432 DB_NAME=m2db

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
