# CyberTODO 2077 - Docker Configuration
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Try to install uv, but fall back to pip if it fails (for environments with SSL issues)
RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org uv || echo "uv installation failed, falling back to pip"

# Copy both uv project files and requirements.txt for compatibility
COPY pyproject.toml uv.lock requirements.txt ./

# Install Python dependencies - try uv first, fall back to pip
RUN uv sync --frozen --no-dev 2>/dev/null || \
    (echo "uv failed, using pip fallback" && pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --no-cache-dir -r requirements.txt)

# Copy application code
COPY . .

# Create database directory
RUN mkdir -p /app/instance

# Initialize database - use proper Flask CLI commands
ENV FLASK_APP=run.py
RUN flask init-db

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

# Run application - use uv run if available, otherwise python directly
CMD ["sh", "-c", "(uv run python run.py 2>/dev/null) || python run.py"]