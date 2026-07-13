# Task 02: Docker Build Stage in CI

## Objective
Extend the CI pipeline so it not only tests the code, but packages it into a
deployable Docker image and verifies the containerized app actually runs.

## What Was Built
- `Dockerfile` — containerizes the Flask app using `python:3.11-slim`
- Two new CI steps added to `.github/workflows/ci.yml`:
  1. Build the Docker image, tagged with the Git commit SHA
  2. Run the container and curl its `/health` endpoint to confirm it starts correctly

## Key Concepts Learned
- **Layer caching order matters** — copying `requirements.txt` and installing
  dependencies *before* copying application code means Docker can reuse the
  cached dependency layer across builds, since code changes far more often
  than dependencies do.
- **Tagging images with `github.sha`** ties every built image back to the exact
  commit that produced it — critical for traceability once images start getting
  deployed.
- **`curl --fail`** is required for the pipeline to actually catch a broken
  endpoint — without it, curl treats even a 404/500 as a "successful" request
  and won't fail the CI step.
- **Untracked files are invisible to CI** — a file can exist and look correct
  locally, but if it was never `git add`-ed, it never reaches GitHub, and the
  pipeline (running on GitHub's servers) can't see it. `git status` before
  every commit catches this.

## Issues Encountered & Fixes
- First run failed with `open Dockerfile: no such file or directory` even
  though the file existed locally. Root cause: an earlier commit only staged
  `.github/workflows/ci.yml` specifically, so `Dockerfile` was never actually
  committed — it stayed untracked. Fixed with `git add Dockerfile` followed by
  a commit and push.

## Result
✅ Pipeline builds a Docker image and confirms the container serves traffic
correctly, on every push to `main`.

## Next Steps
- Push the built image to a container registry (Docker Hub or GHCR)
- Add branch protection requiring CI to pass before merge
- Explore deploying the image (e.g. to a local Kubernetes cluster via kind/minikube)
