# Multi-Agent Systems — 01-multi-agent-systems
# Build: docker compose build | Run: docker compose up
FROM python:3.11-slim

WORKDIR /app

# Install dependencies dulu (layer cache optimal)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY src/ ./src/
COPY README.md ./README.md

# Default: jalankan semua demo
CMD ["python", "-m", "src.main", "--demo", "all"]
