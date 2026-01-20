from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import pickle
import os
import pandas as pd
import json
import datetime

app = FastAPI(title="ForgeSentry: AI-IoT Threat Detection", version="1.0")

# Global variables for model
# Get the directory of the current file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "ai_engine", "model.pkl")
model = None

@app.get("/", include_in_schema=False)
def serve_portal():
    """Serves the main ForgeSentry landing page."""
    return FileResponse(os.path.join(BASE_DIR, "index.html"))

@app.get("/portal", include_in_schema=False)
def serve_monitor():
    """Serves the live SOC monitor."""
    return FileResponse(os.path.join(BASE_DIR, "dashboard", "monitor.html"))

class LogEntry(BaseModel):
    timestamp: str | None = None
    src_ip: str | None = None
    input: str
    session: str | None = None

class Prediction(BaseModel):
    label: str
    input: str
    risk_score: int
    confidence: str
    mitre_id: str

# File paths
THREAT_FEED_JSON = os.path.join(BASE_DIR, "detection", "threat_feed.json")

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
        # Get raw prediction and probability
        prediction = model.predict([entry.input])[0]
        probs = model.predict_proba([entry.input])[0]
        confidence = max(probs)
        
        # Calculate Advanced Risk Score (0-100)
        is_normal = (prediction == "Normal_Business_Ops")
        risk_score = int(confidence * 100) if not is_normal else int((1 - confidence) * 15)
        
        # MITRE ATT&CK Mapping (Titan V3 Spec - Global Coverage)
        mitre_mapping = {
            "Cloud_&_Container_Exploit": "T1613 (Container Escape) / T1552.005 (Cloud Credentials)",
            "Advanced_Persistence_&_LotL": "T1547.001 (Boot/Logon Autostart) / T1053.005 (Scheduled Task)",
            "Advanced_RCE_&_C2": "T1059.004 (Unix Shell) / T1071.001 (Web Protocols)",
            "Critical_Infrastructure_ICS": "T0801 (Impact - Industrial) / T0831 (Manipulation of Control)",
            "Supply_Chain_&_Log4Shell": "T1195 (Supply Chain Compromise) / T1190 (Exploit Public-Facing App)",
            "Ransomware_Prep": "T1486 (Data Encrypted for Impact) / T1490 (Inhibit System Recovery)",
            "Normal_Business_Ops": "N/A"
        }
        
        # Threat Intel Feed: if malicious, log it (Enterprise DB Format)
        if prediction != "Normal_Business_Ops":
            with open(THREAT_FEED_JSON, "a") as f:
                event = {
                    "timestamp": entry.timestamp or datetime.datetime.now().isoformat(),
                    "target": "FORGESENTRY-TITAN-01",
                    "actor_ip": entry.src_ip or "127.0.0.1",
                    "behavior": prediction,
                    "mitre_id": mitre_mapping.get(prediction, "T1210"),
                    "risk_score": risk_score,
                    "confidence": f"{confidence:.2f}"
                }
                f.write(json.dumps(event) + "\n")

        return {
            "label": prediction, 
            "input": entry.input,
            "risk_score": risk_score,
            "confidence": f"{confidence:.2f}",
            "mitre_id": mitre_mapping.get(prediction, "T1210")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/feed/events")
def get_recent_events(limit: int = 10):
    """Returns the most recent threat events in full JSON format."""
    events = []
    if os.path.exists(THREAT_FEED_JSON):
        with open(THREAT_FEED_JSON, "r") as f:
            lines = f.readlines()
            for line in lines[-limit:]:
                events.append(json.loads(line))
    return events[::-1] # Newest first

@app.get("/feed/blacklist")
def export_blacklist():
    """Export list of malicious IPs detected by the Titan Engine."""
    ips = set()
    if os.path.exists(THREAT_FEED_JSON):
        with open(THREAT_FEED_JSON, "r") as f:
            for line in f:
                event = json.loads(line)
                if "actor_ip" in event:
                    ips.add(event["actor_ip"])
    
    return {
        "format": "json",
        "description": "Blacklist of IPs detected by ForgeSentry TITAN AI",
        "count": len(ips),
        "ips": list(ips)
    }

@app.get("/feed/stix")
def export_stix():
    """Export detected threats in STIX 2.1 format for professional intelligence sharing."""
    from stix2 import Indicator, Bundle, Relationship, Identity
    import uuid

    if not os.path.exists(THREAT_FEED_JSON):
        return {"message": "No threats recorded yet."}
    
    intel_forge = Identity(name="Intel Forge", identity_class="organization")
    objects = [intel_forge]
    
    seen_ips = set()
    if os.path.exists(THREAT_FEED_JSON):
        with open(THREAT_FEED_JSON, "r") as f:
            for line in f:
                event = json.loads(line)
                ip = event.get("actor_ip")
                label = event.get("behavior")
                if ip and ip not in seen_ips:
                    indicator = Indicator(
                        name=f"Malicious {label} IP: {ip}",
                        description=f"Risk: {event.get('risk_score')}/100 | TTP: {event.get('mitre_id')}",
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
