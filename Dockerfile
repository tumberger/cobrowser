# Use Python 3.11 slim as base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  PIP_NO_CACHE_DIR=1

# Create and set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
  apt-get install -y --no-install-recommends \
  build-essential \
  curl \
  && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml README.md ./
COPY cobrowser/ ./cobrowser/

# Install Python dependencies
RUN pip install --no-cache-dir ".[dev]"

# Expose port
EXPOSE 8000

# Set the default command
CMD ["uvicorn", "cobrowser.api.main:app", "--host", "0.0.0.0", "--port", "8000"] 