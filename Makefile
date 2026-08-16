# Requires UV: https://docs.astral.sh/uv/
# Install: curl -LsSf https://astral.sh/uv/install.sh | sh
.PHONY: setup sync run run-agent docker-build docker-run lint format test

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

# Run an Agent Series module (deps via pip: pip install -r requirements.txt)
# Usage: make run-agent MODULE=01-multi-agent-systems DEMO=all
run-agent:
	@if [ -z "$(MODULE)" ]; then echo "Usage: make run-agent MODULE=01-multi-agent-systems"; exit 1; fi
	cd agent-series/$(MODULE) && uv run --active python -m src.main --demo $(DEMO)

# Build Docker image untuk Agent Series module
# Usage: make docker-build MODULE=01-multi-agent-systems
docker-build:
	@if [ -z "$(MODULE)" ]; then echo "Usage: make docker-build MODULE=01-multi-agent-systems"; exit 1; fi
	cd agent-series/$(MODULE) && docker compose build

# Run Agent Series module di Docker
# Usage: make docker-run MODULE=01-multi-agent-systems DEMO=all
docker-run:
	@if [ -z "$(MODULE)" ]; then echo "Usage: make docker-run MODULE=01-multi-agent-systems"; exit 1; fi
	cd agent-series/$(MODULE) && docker compose run --rm multi-agent python -m src.main --demo $(DEMO)

# Lint using ruff
lint:
	uv run ruff check .

# Auto-format using ruff
format:
	uv run ruff format .

# Run tests
test:
	uv run pytest
