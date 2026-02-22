# Context

Homebrew tap for `dcm2jpeg` — a CLI tool that converts DICOM medical images to JPEG. The source (`dcm2jpeg.py`) and the Homebrew formula (`Formula/dcm2jpeg.rb`) live in the same repo.

## Structure

```
dcm2jpeg.py          # CLI entry point (single-file app)
Formula/dcm2jpeg.rb  # Homebrew formula with pydicom resource block
tests/               # pytest tests
pyproject.toml       # hatchling build, dependencies, mypy config
ruff.toml            # linter/formatter config
justfile             # dev commands
```

## Build

Python 3.10+, managed with [uv](https://docs.astral.sh/uv/).

```sh
uv sync   # install all deps (or: just install)
```

## Commands

Use `just` for all dev tasks:

| Command          | Purpose                   |
|------------------|---------------------------|
| `just check`     | Run lint + typecheck + test |
| `just lint`      | Ruff check                |
| `just fmt`       | Ruff format               |
| `just fix`       | Ruff auto-fix             |
| `just typecheck` | Mypy (strict mode)        |
| `just test`      | Pytest                    |
| `just fmt-check` | Format check (CI mode)    |

## Code Style

- Ruff: rules B, E, F, I, SIM, UP, W. Target py310. Double quotes.
- Mypy: strict mode, all warnings enabled.

## CI/CD

- **ci.yml** — Runs lint + test matrix (Python 3.10–3.13) on push to main and PRs. Also callable via `workflow_call`.
- **release.yml** — On `v*` tag push: runs CI, then creates a GitHub Release with categorized changelog notes.
- **update-formula.yml** — On release published: updates `Formula/dcm2jpeg.rb` sha256 and pushes to main.

## Release Flow

```
git tag vX.Y.Z && git push --tags
  → release.yml (CI + GitHub Release)
    → update-formula.yml (formula sha256 update)
```
