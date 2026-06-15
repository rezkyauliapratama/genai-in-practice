# Requires UV: https://docs.astral.sh/uv/
# Install: curl -LsSf https://astral.sh/uv/install.sh | sh
.PHONY: setup sync run lint format test

# Create .venv and install all deps (including dev)
setup:
	uv sync --extra dev

# Alias: same as setup
sync:
	uv sync --extra dev

# Run the RAG pipeline for a given module
# Usage: make run MODULE=01-rag-foundations
run:
	@if [ -z "$(MODULE)" ]; then echo "Usage: make run MODULE=01-rag-foundations"; exit 1; fi
	cd rag-series/$(MODULE) && uv run python -m src.pipeline

# Lint using ruff
lint:
	uv run ruff check .

# Auto-format using ruff
format:
	uv run ruff format .

# Run tests
test:
	uv run pytest
