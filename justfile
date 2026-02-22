# dcm2jpeg development commands

# Run all checks (lint + type check + test)
check: lint typecheck test

# Lint with ruff
lint:
    uv run ruff check .

# Format with ruff
fmt:
    uv run ruff format .

# Auto-fix lint issues
fix:
    uv run ruff check --fix .

# Type check with mypy
typecheck:
    uv run mypy .

# Run tests
test:
    uv run pytest tests/ -v

# Install dev dependencies
install:
    uv sync

# Format check (CI mode)
fmt-check:
    uv run ruff format --check .
