import os
from flask import Flask, request, jsonify, render_template
import requests

# During local dev: http://127.0.0.1:8001
# After deploy: set this to your Vercel API URL
API_BASE = os.getenv("API_BASE", "http://127.0.0.1:8001")
API_KEY = os.getenv("API_KEY", "")  # optional

app = Flask(__name__)

@app.get("/healthz")
def health():
    try:
        r = requests.get(f"{API_BASE}/healthz", timeout=4)
        r.raise_for_status()
        return jsonify(r.json()), 200
    except Exception as e:
        return jsonify({"status":"down","error":str(e)}), 503

@app.route("/", methods=["GET", "POST"])
def index():
    category = None
    text = ""
    extra = {}
    if request.method == "POST":
        text = (request.form.get("text") or "").strip()
        try:
            headers = {"x-api-key": API_KEY} if API_KEY else {}
            r = requests.post(f"{API_BASE}/predict", headers=headers, json={"text": text}, timeout=8)
            r.raise_for_status()
            data = r.json()
            category = data.get("category")
            extra = {
                "confidence": data.get("confidence"),
                "model": data.get("model"),
                "version": data.get("version"),
            }
        except requests.RequestException as e:
            category = f"Error: {e}"
    return render_template("index.html", category=category, text=text, extra=extra)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
