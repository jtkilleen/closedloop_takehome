# Use Python 3.11 slim image for smaller size
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files and package directory for better caching
COPY pyproject.toml uv.lock README.md ./
COPY medical_diagnostic_agent/ ./medical_diagnostic_agent/

# Install uv for dependency management
RUN pip install uv

# Install Python dependencies with cache clearing for problematic packages
RUN pip cache purge || true && \
    uv sync --frozen --no-cache

# Copy remaining application code
COPY . .

# Create non-root user for security
RUN useradd --create-home --no-log-init --shell /bin/bash app && \
    chown -R app:app /app
USER app

# Expose port (if needed for web interface in future)
EXPOSE 8000

# Set the default command
CMD ["uv", "run", "adk", "web", "--host", "0.0.0.0"]