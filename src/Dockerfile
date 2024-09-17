# Build stage
FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

COPY pyproject.toml .

RUN poetry config virtualenvs.create false \
    && poetry lock \
    && poetry install --only main --no-interaction --no-ansi


# Runtime stage
FROM python:3.11-slim

WORKDIR /app

# Copy only the necessary files from the builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application files
COPY __init__.py app.py logging.config.yml ./
COPY routers ./routers
COPY templates ./templates

ENV POLLY_HOME_PATH="/app/data/polly"

# Make port 8000 available to the world outside this container
EXPOSE 8080

# Run the application
CMD ["uvicorn", "--app-dir", "/app", "app:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8080", "--log-config", "logging.config.yml", "--reload"]
