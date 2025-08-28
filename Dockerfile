# CyberTODO 2077 - Docker Configuration
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Copy uv project files for better dependency caching
COPY pyproject.toml uv.lock ./

# Install Python dependencies with uv
RUN uv sync --frozen --no-dev

# Copy application code
COPY . .

# Create database directory
RUN mkdir -p /app/instance

# Initialize database
RUN uv run python run.py init-db

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_CONFIG=production
ENV PYTHONPATH=/app

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash cybertodo
RUN chown -R cybertodo:cybertodo /app
USER cybertodo

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1

# Run application
CMD ["uv", "run", "python", "run.py"]