from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
import os
import uvicorn
import pandas as pd

app = FastAPI(title="ForgeSentry: AI-IoT Threat Detection", version="1.0")

# Global variables for model
# Get the directory of the current file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "ai_engine", "model.pkl")
model = None

class LogEntry(BaseModel):
    timestamp: str | None = None
    src_ip: str | None = None
    input: str
    session: str | None = None

class Prediction(BaseModel):
    label: str
    input: str

def load_model():
    global model
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        print(f"Model loaded from {MODEL_PATH}")
    else:
        print(f"Error: Model not found at {MODEL_PATH}")

@app.on_event("startup")
async def startup_event():
    load_model()

@app.get("/health")
def health_check():
    return {"status": "running", "model_loaded": model is not None}

@app.post("/predict", response_model=Prediction)
def predict_threat(entry: LogEntry):
    if not model:
        raise HTTPException(status_code=503, detail="Model not initialized")
    
    try:
        # The model expects an iterable of strings (like a pandas Series or list)
        prediction = model.predict([entry.input])[0]
        
        # Threat Intel Feed: if malicious, log it (simple in-memory implementation for demo)
        if prediction != "Normal":
            # In a real app, write to DB. Here we just log to file for the Feed.
            with open("threat_feed.csv", "a") as f:
                f.write(f"{entry.timestamp},{entry.src_ip},{prediction}\n")

        return {"label": prediction, "input": entry.input}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/feed/blacklist")
def export_blacklist():
    """Export list of malicious IPs detected by the system."""
    if not os.path.exists("threat_feed.csv"):
        return {"count": 0, "ips": []}
    
    ips = set()
    with open("threat_feed.csv", "r") as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) >= 2:
                ips.add(parts[1]) # src_ip
    
    return {
        "format": "json",
        "description": "Blacklist of IPs detected by ForgeSentry AI",
        "count": len(ips),
        "ips": list(ips)
    }

@app.get("/feed/stix")
def export_stix():
    """Export detected threats in STIX 2.1 format for professional intelligence sharing."""
    from stix2 import Indicator, Bundle, Relationship, Identity
    import uuid

    if not os.path.exists("threat_feed.csv"):
        return {"message": "No threats recorded yet."}
    
    intel_forge = Identity(name="Intel Forge", identity_class="organization")
    objects = [intel_forge]
    
    seen_ips = set()
    with open("threat_feed.csv", "r") as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) >= 3:
                ts, ip, label = parts[0], parts[1], parts[2]
                if ip not in seen_ips:
                    indicator = Indicator(
                        name=f"Malicious {label} IP: {ip}",
                        description=f"Detected by ForgeSentry AI-IoT Honeypot as {label}",
                        indicator_types=["malware"],
                        pattern=f"[ipv4-addr:value = '{ip}']",
                        pattern_type="stix",
                        created_by_ref=intel_forge.id
                    )
                    objects.append(indicator)
                    seen_ips.add(ip)
    
    if len(objects) == 1: # Only Identity
        return {"message": "No unique indicators found."}

    bundle = Bundle(objects=objects)
    return bundle.serialize()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
