.PHONY: setup run lint format

setup:
	pip install -e .

run:
	@if [ -z "$(MODULE)" ]; then echo "Usage: make run MODULE=01"; exit 1; fi
	cd rag-series/0$(MODULE)-rag-foundations && python -m src.pipeline

lint:
	ruff check .

format:
	ruff format .
