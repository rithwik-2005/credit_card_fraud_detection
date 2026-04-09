# Credit Card Fraud Detection - Complete Setup & Deployment Guide

## Overview

This project contains a **single Docker image** that runs both FastAPI (backend ML model) and Flask (UI frontend) services simultaneously. The CI/CD pipeline automates building, pushing to Docker Hub, and deploying to Render.

---

## Project Architecture

```
┌─────────────────────────────────────────────┐
│         Single Docker Image                  │
│  (rithwik2005/credit_card_fraud_detection) │
├─────────────────────────────────────────────┤
│                                              │
│  ┌──────────────────┐  ┌────────────────┐  │
│  │  FastAPI Server  │  │  Flask Server  │  │
│  │  Port: 8000      │  │  Port: 5000    │  │
│  │  (ML Backend)    │  │  (Web UI)      │  │
│  └──────────────────┘  └────────────────┘  │
│                                              │
│  Both managed by: entrypoint.sh              │
└─────────────────────────────────────────────┘
```

### Services Inside the Container

1. **FastAPI (Port 8000)**
   - Loads ML model from MLflow Registry or local joblib file
   - Accepts JSON POST requests on `/predict`
   - Returns fraud prediction (`"Fraud Transaction 🚨"` or `"Legitimate Transaction ✅"`)

2. **Flask (Port 5000)**
   - Web UI for entering transaction details
   - Calls FastAPI internally via `FASTAPI_URL` environment variable
   - Renders HTML templates with dropdown menus (loaded from `artifacts/data_ingestion/raw.csv`)

---

## Local Development

### 1. Set up environment

```bash
# Activate virtual environment
cd d:\major_ml\credit_card_fraud_detection
& credit\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 2. Create `.env` file

Copy `.env.example` to `.env` and fill in:

```bash
cp .env.example .env
```

Then edit `.env` with your values:

```env
MLFLOW_TRACKING_URI=https://dagshub.com/<your-user>/<your-repo>.mlflow
MLFLOW_TRACKING_USERNAME=<your-username>
MLFLOW_TRACKING_PASSWORD=<your-token>
FASTAPI_URL=http://127.0.0.1:8000/predict
PORT=5000
```

### 3. Run locally (Two terminals)

**Terminal 1: FastAPI**
```bash
uvicorn app_fastapi:app --host 127.0.0.1 --port 8000
```

**Terminal 2: Flask**
```bash
python app_flask.py
```

Then open browser:
- **FastAPI Docs**: http://localhost:8000/docs
- **Flask UI**: http://localhost:5000

---

## Docker Build & Run

### Build the image locally

```bash
# Build image
docker build -t rithwik2005/credit_card_fraud_detection:latest .

# Verify build
docker images | grep credit_card_fraud_detection
```

### Run locally with Docker

```bash
# Run container (both services will start automatically)
docker run -d \
  -p 8000:8000 \
  -p 5000:5000 \
  --name fraud-detection-app \
  rithwik2005/credit_card_fraud_detection:latest

# Check logs
docker logs fraud-detection-app

# Access services
# FastAPI: http://localhost:8000
# Flask: http://localhost:5000

# Stop container
docker stop fraud-detection-app
```

### Using Docker Compose locally

```bash
# Build and start both services
docker compose up --build

# Run in background
docker compose up -d --build

# View logs
docker compose logs -f

# Stop services
docker compose down
```

---

## GitHub Actions CI/CD Pipeline

### What the workflow does:

1. **Triggers** on `push` to `main` branch or manual `workflow_dispatch`
2. **Builds** the Docker image using BuildX (faster)
3. **Pushes** to Docker Hub:
   - `rithwik2005/credit_card_fraud_detection:latest`
   - `rithwik2005/credit_card_fraud_detection:<git-sha>`
4. **Triggers** Render API to redeploy the service

### Setting up GitHub Secrets

Go to your GitHub repo → Settings → Secrets and variables → Actions

Add these secrets:

| Secret Name | Value |
|---|---|
| `DOCKERHUB_USERNAME` | Your Docker Hub username (e.g., `rithwik2005`) |
| `DOCKERHUB_PASSWORD` | Your Docker Hub access token (not password!) |
| `RENDER_API_KEY` | Your Render API key |
| `RENDER_SERVICE_ID` | Your Render service ID |

### How to get Render credentials:

1. **Render API Key**:
   - Go to Render dashboard → Settings (bottom left) → API Keys
   - Create a new key, copy it

2. **Render Service ID**:
   - Go to your service in Render dashboard
   - URL: `https://dashboard.render.com/services/<SERVICE_ID>`
   - Copy that ID

---

## Deployment to Render

### 1. Create Render Service

1. Go to [render.com](https://render.com)
2. Create new **Web Service**
3. Select **Docker** as environment
4. Use image: `rithwik2005/credit_card_fraud_detection:latest`
5. Set environment variables:

```env
PYTHONUNBUFFERED=1
FASTAPI_URL=http://127.0.0.1:8000/predict
PORT=5000
MLFLOW_TRACKING_URI=<your-mlflow-uri>
MLFLOW_TRACKING_USERNAME=<your-username>
MLFLOW_TRACKING_PASSWORD=<your-token>
```

### 2. Configure Ports

Render exposes **port 5000** by default (Flask). 

If you need to access FastAPI (8000) from outside, create a second service or use port forwarding.

### 3. Set Auto-Deploy

- Enable "Auto-Deploy" after pushing to Docker Hub (optional)
- Or CI/CD pipeline will manually trigger deploys via API

### 4. Deployment Flow

```
1. Push code to main branch
   ↓
2. GitHub Actions builds Docker image
   ↓
3. Docker image pushed to Docker Hub with tags
   ↓
4. GitHub Actions calls Render API
   ↓
5. Render pulls new image and restarts service
   ↓
6. Flask (port 5000) running on render.com
   FastAPI (port 8000) running internally
```

---

## Environment Variables - Security Best Practices

### `.env` file (Local only)

**Location**: Project root directory  
**Never commit**: Already in `.gitignore`  
**Contains**: Sensitive credentials, API keys

```env
MLFLOW_TRACKING_PASSWORD=fbc0e6d67d11d36103dfda306c2c83b946645a14
DOCKERHUB_PASSWORD=<your-token>
RENDER_API_KEY=rnd_1a2b3c4d5e6f7g8h...
```

### GitHub Secrets

**Location**: repo → Settings → Secrets and variables  
**Purpose**: Provide creds to CI/CD pipeline  
**Access**: `${{ secrets.SECRET_NAME }}` in workflows

**Never commit secrets to `.git/` or `.github/workflows/`** — always use GitHub Secrets.

### Render Environment Variables

**Location**: Render Dashboard → Service Settings → Environment  
**Purpose**: Provide runtime configs to production containers  
**Access**: Container can read via `os.getenv()`

For sensitive values (passwords), use Render's **Environment Groups** or **Secrets** feature.

---

## Running the Entrypoint Script

The `entrypoint.sh` script:

1. Starts **FastAPI** on port 8000
2. Waits 2 seconds for FastAPI to initialize
3. Starts **Flask** on port 5000
4. Handles signals (SIGTERM, SIGINT) to gracefully shut down both

The script is automatically executed when the container starts:

```dockerfile
ENTRYPOINT ["/app/entrypoint.sh"]
```

### Logs from entrypoint

```
Starting FastAPI service on port 8000...
Waiting for FastAPI to start...
Starting Flask service on port 5000...
Both services started successfully!
FastAPI PID: 123
Flask PID: 456
```

---

## Dockerfile Breakdown

| Stage | Purpose |
|---|---|
| `FROM python:3.10-slim` | Minimal Python image (~150MB) |
| Install `libgomp1 bash` | Dependencies for scikit-learn + entrypoint script |
| `pip install -r requirements.txt` | Install ML packages, FastAPI, Flask, etc. |
| Copy application code | Bring in app files |
| Copy + chmod `entrypoint.sh` | Make startup script executable |
| `EXPOSE 8000 5000` | Document which ports are used |
| `ENTRYPOINT ["/app/entrypoint.sh"]` | Run both services on startup |

---

## DVC (Data Version Control) - Introduction & Role

### What is DVC?

DVC is a **version control system for data and models**, similar to Git but optimized for large files and machine learning workflows.

**Key idea**: Store only *"pointers"* (`.dvc` files) in Git, while actual data/models live in remote storage (S3, Google Drive, local NAS, etc.).

### Why DVC for this project?

**Current state**: Large files committed to Git
- `data/credit_data.csv` (raw data)
- `artifacts/model_trainer/model.joblib` (trained model)
- `artifacts/data_transformation/feature_columns.pkl` (feature list)
- `artifacts/data_ingestion/raw.csv` (reference dataset)

**Problems**:
- Git repo becomes large (~hundreds of MB)
- Slow clones, pushes, pulls
- Model versioning is manual
- Hard to collaborate on experiments

**With DVC**:
- Git tracks only `.dvc` files (small text files)
- Remote storage holds actual data/models
- Automatic versioning by Git commits
- Easy reproducibility: `dvc repro` re-runs pipeline from scratch

### DVC Workflow for this project

#### 1. Initialize DVC

```bash
# Initialize DVC in project (creates .dvc/ folder)
dvc init

# Configure remote storage (example: local folder)
dvc remote add -d myremote /path/to/dvc-storage

# Or use cloud storage (S3 example)
dvc remote add -d s3_storage s3://my-bucket/fraud-detection
```

#### 2. Track Data & Models

```bash
# Track raw data
dvc add data/credit_data.csv
# Creates: data/credit_data.csv.dvc

# Track transformed data
dvc add artifacts/data_ingestion/raw.csv
# Creates: artifacts/data_ingestion/raw.csv.dvc

# Track trained model
dvc add artifacts/model_trainer/model.joblib
# Creates: artifacts/model_trainer/model.joblib.dvc

# Track feature columns
dvc add artifacts/data_transformation/feature_columns.pkl
# Creates: artifacts/data_transformation/feature_columns.pkl.dvc
```

#### 3. Commit `.dvc` files to Git

```bash
git add data/credit_data.csv.dvc
git add artifacts/data_ingestion/raw.csv.dvc
git add artifacts/model_trainer/model.joblib.dvc
git commit -m "Track data files with DVC"
```

#### 4. Push to Remote Storage

```bash
# Push data/models to remote
dvc push

# Pull data/models from remote
dvc pull
```

#### 5. Version different datasets/models

```bash
# Switch between versions by Git branch
git checkout experiment-v1  # DVC auto-switches data to that version
dvc pull                    # Fetch that version's data

git checkout main
dvc pull  # Fetch main branch's data
```

### DVC in CI/CD Pipeline

Update `.github/workflows/ci-cd.yml` to pull DVC data before building:

```yaml
- name: Set up DVC
  uses: iterative/setup-dvc@v1

- name: Pull training data and models
  run: |
    dvc remote add -d myremote <your-remote-path>
    dvc pull

- name: Build and push Docker image
  # ... rest of build steps
```

Then Docker image includes the correct data for that commit.

### DVC Configuration for this project

Create `dvc.yaml` to define the ML pipeline:

```yaml
stages:
  data_ingestion:
    cmd: python -m src.credit_card_fraud_detection.components.data_ingestion
    deps:
      - data/credit_data.csv
    outs:
      - artifacts/data_ingestion/raw.csv

  data_validation:
    cmd: python -m src.credit_card_fraud_detection.components.data_validation
    deps:
      - artifacts/data_ingestion/raw.csv
    outs:
      - artifacts/data_validation/status.txt

  data_transformation:
    cmd: python -m src.credit_card_fraud_detection.components.data_transformation
    deps:
      - artifacts/data_ingestion/raw.csv
    outs:
      - artifacts/data_transformation/transformed.csv
      - artifacts/data_transformation/feature_columns.pkl

  model_trainer:
    cmd: python -m src.credit_card_fraud_detection.components.model_trainer
    deps:
      - artifacts/data_transformation/transformed.csv
    outs:
      - artifacts/model_trainer/model.joblib

  model_evaluation:
    cmd: python -m src.credit_card_fraud_detection.components.model_evaluation
    deps:
      - artifacts/model_trainer/model.joblib
    outs:
      - artifacts/model_evaluation/metrics.json
```

Then run entire pipeline:

```bash
dvc repro  # Re-runs all stages if inputs change
```

### Do you need DVC now?

| Scenario | Recommendation |
|---|---|
| Small demo project (~100MB) | Maybe later |
| Team collaboration | **Yes, use DVC now** |
| Frequent model retraining | **Yes, use DVC now** |
| Multiple data versions | **Yes, use DVC now** |
| Production deployment | **Yes, required** |

### Minimal DVC setup (recommended)

```bash
# Initialize
dvc init

# Configure S3 remote (or local storage)
dvc remote add -d s3_store s3://your-bucket/fraud-detection

# Track important files only
dvc add artifacts/model_trainer/model.joblib

# Commit .dvc file
git add artifacts/model_trainer/model.joblib.dvc
git commit -m "Track model with DVC"

# Push
dvc push
```

---

## Troubleshooting

### FastAPI not responding in container

Check logs:
```bash
docker logs fraud-detection-app | grep FastAPI
```

Ensure `entrypoint.sh` is executable:
```bash
docker exec fraud-detection-app ls -la /app/entrypoint.sh
```

### Flask can't reach FastAPI

Inside container, FastAPI runs on `127.0.0.1:8000`, not Docker network. The entrypoint script sets:
```bash
export FASTAPI_URL=http://127.0.0.1:8000/predict
```

### Model not loading

Check MLflow connection:
```bash
python -c "from src.credit_card_fraud_detection.pipeline.prediction_pipeline import PredictionPipeline; p = PredictionPipeline()"
```

Fallback model loads from: `artifacts/model_trainer/model.joblib`

### Docker image too large

Check what's included:
```bash
docker history rithwik2005/credit_card_fraud_detection:latest
```

Exclude large files in `.dockerignore`:
```
credit/  (virtual environment)
data/    (raw data)
artifacts/data_*/ (intermediate artifacts)
```

---

## Quick Commands Reference

### Local Development
```bash
# Run FastAPI + Flask manually
uvicorn app_fastapi:app --host 127.0.0.1 --port 8000 &
python app_flask.py

# Or use compose
docker compose up --build
```

### Docker Commands
```bash
# Build
docker build -t rithwik2005/credit_card_fraud_detection:latest .

# Run
docker run -d -p 8000:8000 -p 5000:5000 rithwik2005/credit_card_fraud_detection:latest

# Logs
docker logs -f <container-id>

# Push to Docker Hub
docker push rithwik2005/credit_card_fraud_detection:latest
```

### Git & CI/CD
```bash
# Push triggers GitHub Actions
git add .
git commit -m "Update model"
git push origin main

# Monitor workflow in GitHub Actions tab
```

### DVC Commands (when enabled)
```bash
dvc init
dvc remote add -d myremote s3://bucket/path
dvc add artifacts/model_trainer/model.joblib
dvc push
dvc pull
dvc repro
```

---

## Summary

✅ **Single Docker image** runs FastAPI + Flask simultaneously  
✅ **Entrypoint script** manages both processes  
✅ **GitHub Actions** automates build → Docker Hub → Render  
✅ **Environment variables** secured in GitHub Secrets  
✅ **DVC ready** for future data/model versioning  

For production, enable DVC to version data and models alongside code.

