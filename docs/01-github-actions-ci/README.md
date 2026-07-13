# Task 01: GitHub Actions CI Pipeline

## Objective
Build a working CI/CD pipeline from scratch for a Flask app, using GitHub Actions,
and understand the reasoning behind each pipeline stage rather than just copying a template.

## What Was Built
- A minimal Flask API (`app/main.py`) with two endpoints: `/` and `/health`
- Unit tests (`tests/test_main.py`) using pytest
- A GitHub Actions workflow (`.github/workflows/ci.yml`) that runs on every push/PR to `main`

## Pipeline Stages
1. **Checkout code** — clones the repo into a fresh, disposable Ubuntu VM
2. **Set up Python 3.11** — pinned version to avoid environment drift
3. **Install dependencies** — installs Flask, pytest, and flake8 from `requirements.txt`
4. **Lint (flake8)** — runs first since it's fast; fails fast on style issues before
   running the more expensive test suite
5. **Test (pytest)** — verifies actual application behavior

## Key Concepts Learned
- **CI runs in a clean, disposable environment every time** — nothing from a local
  machine carries over, which is why dependencies must be explicitly installed in
  the workflow itself.
- **Pinned dependency versions** (`requirements.txt`, Python version) prevent
  "works on my machine" drift, since CI reinstalls everything from scratch on
  every run.
- **Fail-fast ordering** — cheap checks (lint) run before expensive ones (tests),
  so pipelines fail quickly on trivial issues.
- **`.gitignore` matters for CI hygiene** — committed `__pycache__`/`.pyc` files
  are machine-specific and have no place in version control.
- **Every pipeline run is a permanent historical record** — a failed run doesn't
  get "overwritten"; a new push creates a new run. Only the latest run on `main`
  reflects current pipeline health.

## Issues Encountered & Fixes
- flake8 flagged `E302`/`E305` (missing blank lines between function definitions)
  in both `tests/test_main.py` and `app/main.py`. Fixed by adding the required
  2 blank lines between top-level function definitions (PEP8 standard).

## Result
✅ Pipeline passes on every push to `main` — lint and tests both green.

## Next Steps
- Add a Docker build stage to package the app as a container image
- Add branch protection requiring CI to pass before merging
- Add a live build-status badge to the repo README
