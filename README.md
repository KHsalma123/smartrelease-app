# SmartRelease — Application API

**A containerized FastAPI application built to demonstrate Kubernetes deployments, Canary releases, and Prometheus observability.**

[GitOps & Progressive Delivery Repository](https://github.com/KHsalma123/smartrelease-gitops)

---

## Overview

SmartRelease is a lightweight REST API developed as part of a hands-on DevOps project. It provides health-check endpoints and Prometheus metrics to support deployment validation and progressive delivery on Kubernetes.

The application is designed to work with the SmartRelease GitOps repository, which contains the Kubernetes manifests and Canary rollout configuration managed using Argo CD and Argo Rollouts.

## Features

- **REST API:** Built with FastAPI.
- **Configurable application version:** Set the version through the `APP_VERSION` environment variable.
- **Configurable application status:** Set the status through the `APP_STATUS` environment variable.
- **Health endpoint:** Provides application status and version for Kubernetes health probes.
- **Prometheus metrics:** Exposes application metrics at `/metrics`.
- **Controlled error endpoint:** Provides a deliberate HTTP 500 response for failure-scenario testing.
- **Automated tests:** Tests the default API response and health endpoint using FastAPI's `TestClient`.
- **Dockerized deployment:** Uses a lightweight Python image and runs as a non-root user.

## Technology Stack

- Python 3.14
- FastAPI
- Uvicorn
- Prometheus FastAPI Instrumentator
- Pytest and FastAPI TestClient
- Docker
- Kubernetes

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Returns project information, application version, status, and a message. |
| `GET` | `/health` | Returns the configured status and application version. |
| `GET` | `/metrics` | Exposes metrics for Prometheus scraping. |
| `GET` | `/test-error` | Intentionally returns HTTP 500 to support failure-scenario testing. |

### Example response

A request to `/health` with the default environment configuration returns:

```json
{
  "status": "healthy",
  "version": "v1"
}
```

The application defaults to `APP_VERSION=v1` and `APP_STATUS=healthy` when the corresponding environment variables are not set.

## Getting Started

### Prerequisites

- Python 3.14 or a compatible Python environment.
- Git.
- Docker, if you want to build and run the container image.

### Clone the repository

```bash
git clone https://github.com/KHsalma123/smartrelease-app.git
cd smartrelease-app
```

### Install dependencies

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the application dependencies:

```bash
pip install -r requirements.txt
```

### Run the API locally

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API is then available at:

- API root: `http://localhost:8000/`
- Health check: `http://localhost:8000/health`
- Prometheus metrics: `http://localhost:8000/metrics`
- Interactive API documentation: `http://localhost:8000/docs`

Stop the development server with `Ctrl + C`.

## Configuration

The application supports the following environment variables:

| Variable | Default | Description |
|---|---|---|
| `APP_VERSION` | `v1` | Identifies the running application version. |
| `APP_STATUS` | `healthy` | Defines the status returned by the API endpoints. |

Example:

```bash
APP_VERSION=v2 APP_STATUS=healthy uvicorn main:app --host 0.0.0.0 --port 8000
```

These variables can be used to simulate different application versions during Canary deployment exercises.

## Automated Tests

The test suite uses FastAPI's `TestClient` to validate the API's default response and health endpoint.

Install the development dependencies:

```bash
pip install -r requirements-dev.txt
```

Run the tests:

```bash
pytest -v
```

The current tests verify that:

- `GET /` returns HTTP 200 and the expected default project, version, and status.
- `GET /health` returns HTTP 200 and the expected healthy status.

The `/metrics` and `/test-error` endpoints are not currently covered by these tests.

## Docker

The Dockerfile uses `python:3.14-slim`, installs the application dependencies, copies the source code into `/app`, and runs Uvicorn on port `8000`.

It also creates a dedicated `appuser` and runs the application without root privileges.

### Build the image

From the repository root:

```bash
docker build -t smartrelease-app:local .
```

### Run the container

```bash
docker run --rm -p 8000:8000 smartrelease-app:local
```

Test the health endpoint:

```bash
curl http://localhost:8000/health
```

### Run with a custom version

```bash
docker run --rm \
  -p 8000:8000 \
  -e APP_VERSION=v2 \
  -e APP_STATUS=healthy \
  smartrelease-app:local
```

The image built locally is for development and testing. The Kubernetes rollout configuration in the GitOps repository specifies the image used by the deployed environment.

## Integration with SmartRelease GitOps

This repository contains the application source code and Docker build configuration. Kubernetes rollout resources and progressive delivery settings are maintained separately.

**Related repository:** [smartrelease-gitops](https://github.com/KHsalma123/smartrelease-gitops)

The GitOps repository includes the configuration for:

- Kubernetes application resources.
- Canary traffic routing through NGINX Ingress.
- Progressive rollout orchestration with Argo Rollouts.
- GitOps synchronization with Argo CD.
- Prometheus-based success-rate analysis.

Together, the two repositories separate application development from deployment configuration.

## Project Objectives

SmartRelease demonstrates practical experience with:

- Building REST APIs using FastAPI.
- Writing automated API tests.
- Containerizing Python applications.
- Running containers with reduced privileges.
- Exposing metrics for Prometheus.
- Supporting Kubernetes health checks and progressive delivery workflows.

## Author

Developed as a hands-on DevOps portfolio project focused on containerization, Kubernetes, GitOps, progressive delivery, and observability.
