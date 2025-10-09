# IT Ticket Classifier

Classify IT support tickets (e.g., “Outlook not syncing”, “Windows update BSOD”) into categories using a lightweight ML model exposed as a **FastAPI** service, with a simple **Flask** web UI.

- **Live UI:** https://it-ticket-classifier-ui.vercel.app/
- **Live API:** `https://<your-api-project>.vercel.app` ← replace with your API domain from Vercel

---

## ✨ Overview

- **Backend (FastAPI)**  
  REST API with `/predict` and `/healthz`, loading a serialized **TF-IDF + Linear SVM** classifier from `model_bundle/ticket_classifier.pkl`.

- **Frontend (Flask)**  
  Minimal UI that posts the ticket text to the API and renders the predicted category.

- **Deployment**  
  Both tiers are containerized with **Dockerfiles** and deployed to **Vercel** as two separate projects (API + UI).

- **Labels (example)**  
  `ACCESS, HARDWARE, SOFTWARE, WINDOWS, EMAIL, ANTIVIRUS` (+ `Unknown` fallback).

---

## 🧭 Repository Structure

```text
IT-Ticket-Classifier/
|
├─ ticket-api-fastapi/                # Backend (FastAPI)
│  ├─ app.py
│  ├─ requirements.txt
│  ├─ Dockerfile
│  └─ model_bundle/
│     └─ ticket_classifier.pkl        # vectorizer + model + metadata
|
└─ ticket-ui-flask/                   # Frontend (Flask)
   ├─ app.py
   ├─ templates/
   │  └─ index.html
   ├─ requirements.txt
   └─ Dockerfile

```
## 🧰 Setup
## Prerequisites

Python 3.10+

Git

(Optional) Docker

Vercel account + CLI (npm i -g vercel) for cloud deploys

## Clone
git clone https://github.com/Krithikagm/IT-Ticket-Classifier.git

cd IT-Ticket-Classifier

## ▶️ Run Locally (Docker)
## 1) API

```Text
cd ticket-api-fastapi
docker build -t ticket-api .
docker run -p 8080:8080 \
  -e MODEL_PATH="model_bundle/ticket_classifier.pkl" \
  ticket-api
```

## 2) UI
```Text
cd ticket-ui-flask
docker build -t ticket-ui .
# For Mac/Windows Docker Desktop, use host.docker.internal to reach the API
docker run -p 5000:8080 \
  -e API_BASE="http://host.docker.internal:8080" \
  ticket-ui
# UI at http://127.0.0.1:5000
```


## ☁️ Deploy to Vercel (two projects)

You’ll create two Vercel projects from this repo: one for the API and one for the UI.

## A) API Deploy

In Vercel dashboard: Add New → Project → Import Git Repository → select this repo.

Root Directory: `ticket-api-fastapi`.

Framework Preset: Other (Vercel will build using the included `Dockerfile`).

Environment Variables (Project → Settings → Environment Variables):

`MODEL_PATH = model_bundle/ticket_classifier.pkl`

Deploy → copy the Production URL, e.g.
`https://it-ticket-classifier.vercel.app`

## B) UI Deploy

Add a second project from the same repo.

Root Directory: `ticket-ui-flask`.

Framework Preset: Other (uses this folder’s `Dockerfile`).

Environment Variables:

`API_BASE = https://it-ticket-classifier.vercel.app`
(replace with your API URL; include https://)

Deploy → your UI URL will look like
`https://it-ticket-classifier-ui.vercel.app`

If you see “Authentication Required”, disable Settings → Security → Vercel Authentication for Production.













