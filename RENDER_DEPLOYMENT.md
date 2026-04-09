# Render Deployment Guide - Credit Card Fraud Detection

## Overview

This guide explains how to deploy the FastAPI and Flask services to Render with proper environment variables and secret management.

---

## Step 1: GitHub Repository Secrets Setup

GitHub Secrets are encrypted and used by CI/CD pipeline to authenticate with Docker Hub and Render.

### Add GitHub Secrets

Go to your GitHub repository:
1. Settings → Secrets and variables → Actions
2. Click "New repository secret"

Add these secrets:

| Secret Name | Value | Where to Get It |
|---|---|---|
| `DOCKERHUB_USERNAME` | `rithwik2005` | Your Docker Hub account name |
| `DOCKERHUB_PASSWORD` | `dckr_pat_xxxx` | Docker Hub → Account Settings → Security → New Access Token |
| `RENDER_API_KEY` | `rnd_xxxx` | Render Dashboard → Account (bottom left) → API Keys → Create new |
| `RENDER_SERVICE_ID_FASTAPI` | `srv_xxxxx` | Your FastAPI service ID from Render |
| `RENDER_SERVICE_ID_FLASK` | `srv_xxxxx` | Your Flask service ID from Render |

---

## Step 2: Create Docker Hub Access Token

### Why? 
GitHub Actions needs to authenticate with Docker Hub to push images. Using a token is safer than using your password.

### How to Create:

1. Go to [Docker Hub](https://hub.docker.com) and sign in
2. Click your avatar → Account Settings
3. Left sidebar → Security → New Access Token
4. Name it: `github-actions-fraud-detection`
5. Read & Write permissions
6. Copy the token and save as `DOCKERHUB_PASSWORD` in GitHub

---

## Step 3: Get Render API Key

### Why?
The CI/CD pipeline uses this to trigger automatic deployments after pushing to Docker Hub.

### How to Get:

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click your avatar at bottom left → Account Settings
3. Scroll to "API Keys"
4. Click "Create new API key"
5. Copy and save as `RENDER_API_KEY` in GitHub Secrets

---

## Step 4: Create Two Render Web Services

You need **two separate services**: one for FastAPI, one for Flask.

### Service 1: FastAPI Backend

1. **Render Dashboard** → New → Web Service
2. **Configuration:**
   - **Name**: `fraud-detection-api`
   - **Environment**: Docker
   - **Repository**: (select your repo)
   - **Branch**: `main`
   - **Dockerfile**: `fastapi_app/Dockerfile`
   - **Region**: Choose your region
   - **Plan**: Free or Starter
3. Click "Create Web Service"

**After Creation:**
- Copy the **Service ID** from URL: `https://dashboard.render.com/services/srv_xxxxx`
- Save as `RENDER_SERVICE_ID_FASTAPI` in GitHub Secrets

### Service 2: Flask Frontend

1. **Render Dashboard** → New → Web Service
2. **Configuration:**
   - **Name**: `fraud-detection-web`
   - **Environment**: Docker
   - **Repository**: (same repo)
   - **Branch**: `main`
   - **Dockerfile**: `flask_app/Dockerfile`
   - **Region**: Same as FastAPI
   - **Plan**: Free or Starter
3. Click "Create Web Service"

**After Creation:**
- Copy the **Service ID** from URL
- Save as `RENDER_SERVICE_ID_FLASK` in GitHub Secrets

---

## Step 5: Configure Environment Variables in Render

Each service needs environment variables. Set them in Render Dashboard.

### FastAPI Service Environment

Click your FastAPI service → Settings → Environment tab

Add:
```
PYTHONUNBUFFERED=1
MLFLOW_TRACKING_URI=https://dagshub.com/rithwik-2005/credit_card_fraud_detection.mlflow
MLFLOW_TRACKING_USERNAME=rithwik-2005
MLFLOW_TRACKING_PASSWORD=fbc0e6d67d11d36103dfda306c2c83b946645a14
```

### Flask Service Environment

Click your Flask service → Settings → Environment tab

Add:
```
PYTHONUNBUFFERED=1
FASTAPI_URL=https://fraud-detection-api.onrender.com/predict
PORT=5000
```

**Important:**
- Replace `fraud-detection-api.onrender.com` with your actual FastAPI URL from Render
- Get the correct URL: Your FastAPI service page shows it

---

## Step 6: Add Service URLs to Render

### Find Your Service URL

For each service in Render Dashboard:
- Click on the service
- Top of page shows: `https://your-service-name.onrender.com`

### Update Flask Service

After FastAPI is deployed:

1. Click Flask service → Settings → Environment
2. Update `FASTAPI_URL`:
   ```
   FASTAPI_URL=https://your-fastapi-service.onrender.com/predict
   ```
3. Click "Save changes"
4. Service auto-redeploys

---

## Step 7: Deploy Manually (First Time)

First deployment might need to be triggered manually:

1. Go to your FastAPI service in Render
2. Click "Manual Deploy" → "Deploy latest commit"
3. Wait for build to complete (check logs)
4. Do the same for Flask service

---

## Step 8: Verify Deployments

### Check FastAPI Health

```bash
curl https://your-fastapi-service.onrender.com/
# Response: {"message": "Fraud Detection API running successfully 🚀"}
```

### Check FastAPI Docs

Open in browser:
```
https://your-fastapi-service.onrender.com/docs
```

### Check Flask UI

Open in browser:
```
https://your-flask-service.onrender.com/
```

### Check Logs

In Render Dashboard:
- Click service → Logs
- See all recent logs including errors

---

## Step 9: Automatic Deployments

After GitHub Secrets are set up, CI/CD pipeline auto-deploys:

1. Push code to `main` branch
2. GitHub Actions builds Docker images
3. Images pushed to Docker Hub
4. CI/CD calls Render API to trigger redeploy
5. Render pulls new images from Docker Hub
6. Services restart automatically

---

## How the Workflow Works

```
┌─────────────────────────────────────────┐
│  You: git push to main branch           │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│  GitHub Actions Triggered               │
│  - Build FastAPI Docker image           │
│  - Build Flask Docker image             │
│  - Push both to Docker Hub              │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│  CI/CD calls Render API                 │
│  - trigger FastAPI service redeploy     │
│  - trigger Flask service redeploy       │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│  Render pulls new images from Docker Hub│
│  Restarts services with new code        │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│  ✅ Services live at:                  │
│  FastAPI: https://your-api.onrender.com│
│  Flask:   https://your-web.onrender.com│
└─────────────────────────────────────────┘
```

---

## Troubleshooting

### "Service failed to start"

Check logs in Render Dashboard:
1. Click service → Logs
2. Look for error messages
3. Common issues:
   - Missing environment variables
   - Port not accessible
   - MLflow connection error (fallback to local model)

### "Cannot connect to FastAPI from Flask"

1. Verify `FASTAPI_URL` in Flask service environment
2. Use full URL: `https://your-fastapi-service.onrender.com`
3. NOT `http://127.0.0.1` (doesn't work on Render)

### "Deployment not triggering"

1. Check GitHub Secrets are correct
2. Verify `RENDER_API_KEY` works:
   ```bash
   curl https://api.render.com/v1/services \
     -H "Authorization: Bearer YOUR_API_KEY"
   ```
3. Verify service IDs are correct:
   ```bash
   echo $RENDER_SERVICE_ID_FASTAPI
   ```

### "Docker Hub authentication failed"

1. Verify `DOCKERHUB_USERNAME` and `DOCKERHUB_PASSWORD` in GitHub Secrets
2. Test Docker login locally:
   ```bash
   docker login -u rithwik2005 -p <DOCKERHUB_PASSWORD>
   ```

---

## Key Environment Variables Reference

| Variable | FastAPI | Flask | Purpose |
|---|---|---|---|
| `PYTHONUNBUFFERED` | ✅ | ✅ | Real-time console output |
| `FASTAPI_URL` | ❌ | ✅ | URL to reach FastAPI service |
| `PORT` | ❌ | ✅ | Flask port (5000) |
| `MLFLOW_TRACKING_URI` | ✅ | ❌ | MLflow model registry URL |
| `MLFLOW_TRACKING_USERNAME` | ✅ | ❌ | MLflow credentials |
| `MLFLOW_TRACKING_PASSWORD` | ✅ | ❌ | MLflow credentials |

---

## GitHub Secrets Quick Reference

Store these in GitHub (Settings → Secrets):

```yaml
DOCKERHUB_USERNAME: rithwik2005
DOCKERHUB_PASSWORD: dckr_pat_xxxx  # From Docker Hub
RENDER_API_KEY: rnd_xxxx  # From Render Account settings
RENDER_SERVICE_ID_FASTAPI: srv_xxxxx  # From FastAPI service URL
RENDER_SERVICE_ID_FLASK: srv_xxxxx  # From Flask service URL
```

---

## Quick Checklist

- [ ] Created Docker Hub access token
- [ ] Created Render API key
- [ ] Added 5 GitHub Secrets
- [ ] Created FastAPI service on Render
- [ ] Created Flask service on Render
- [ ] Added environment variables to FastAPI service
- [ ] Added environment variables to Flask service
- [ ] Updated Flask `FASTAPI_URL` with correct service URL
- [ ] Pushed to `main` branch and CI/CD triggered
- [ ] Verified services are running and accessible

---

## Support

If services don't deploy:

1. Check GitHub Actions logs (your repo → Actions tab)
2. Check Render service logs (Render Dashboard → Service → Logs)
3. Verify all environment variables are set correctly
4. Test Docker images locally first:
   ```bash
   docker compose up --build
   ```

