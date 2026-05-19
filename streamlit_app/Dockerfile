# Multi-stage build for minimal image size
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

WORKDIR /app

# Install dependencies into an isolated venv
COPY --from=parent requirements.txt ./
RUN uv venv .venv && \
    uv pip install --python .venv -r requirements.txt

# Production stage - minimal base image
FROM python:3.12-slim

WORKDIR /app

# Install only runtime system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application code (streamlit_app/ contents from project root context)
COPY ./ .

# Copy dataset
COPY --from=parent ./data /app/data

# Copy output files
COPY --from=parent ./output /app/output

# Create non-root user for security
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Add venv to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Expose Streamlit default port
EXPOSE 8501

# Run Streamlit
ENTRYPOINT ["streamlit", "run", "Home.py", \
            "--server.port=8501", \
            "--server.address=0.0.0.0"]