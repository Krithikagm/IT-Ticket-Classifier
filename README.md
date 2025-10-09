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








