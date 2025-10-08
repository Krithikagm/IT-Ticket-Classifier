import os, pickle
from typing import Optional, Literal
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel, Field

# ---- Load model once at startup ----
ARTIFACT_PATH = os.getenv("MODEL_PATH", "model_bundle/ticket_classifier.pkl")
with open(ARTIFACT_PATH, "rb") as f:
    art = pickle.load(f)

clf  = art["model"]
vect = art["vectorizer"]
meta = art.get("metadata", {})
ALLOWED = {"ACCESS","HARDWARE","SOFTWARE","WINDOWS","EMAIL","ANTIVIRUS"}

def predict_text(text: str):
    X = vect.transform([text or ""])
    if X.nnz < 1:
        return "Unknown", 0.0
    if hasattr(clf, "predict_proba"):
        proba = clf.predict_proba(X)[0]
        idx = proba.argmax()
        pred = clf.classes_[idx]
        score = float(proba[idx])
    else:
        pred = clf.predict(X)[0]
        if hasattr(clf, "decision_function"):
            import numpy as np
            m = float(clf.decision_function(X).max())
            score = float(1 / (1 + np.exp(-m)))
        else:
            score = 0.0
    pred = pred if pred in ALLOWED else "Unknown"
    return pred, score

class PredictIn(BaseModel):
    text: str = Field(..., description="Ticket description")

class PredictOut(BaseModel):
    category: Literal["ACCESS","HARDWARE","SOFTWARE","WINDOWS","EMAIL","ANTIVIRUS","Unknown"]
    confidence: float
    model: Optional[str] = None
    version: Optional[str] = None

app = FastAPI(title="Ticket Classifier API", version="1.0.0")

@app.get("/healthz")
def health():
    return {"status":"ok","model": meta.get("algorithm","unknown"), "labels": sorted(list(ALLOWED))}

API_KEY = os.getenv("API_KEY")  # optional

@app.post("/predict", response_model=PredictOut)
def predict(body: PredictIn, x_api_key: str = Header(None)):
    if API_KEY and x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    text = (body.text or "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="Empty text")
    category, conf = predict_text(text)
    return {
        "category": category,
        "confidence": round(conf, 4),
        "model": meta.get("algorithm","LinearSVM"),
        "version": meta.get("version","1"),
    }
