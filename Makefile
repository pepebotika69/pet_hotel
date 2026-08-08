RUFF_VERSION = 0.9.10
RUFF_DOCKER = docker run --rm -v $(PWD):/code -w /code ghcr.io/astral-sh/ruff:$(RUFF_VERSION)

lint:
	ruff check .

lint-fix:
	ruff check --fix .

format:
	ruff format .

format-check:
	ruff format --check .

fix:
	ruff check --fix .
	ruff format .
