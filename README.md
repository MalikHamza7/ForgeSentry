# 🛡️ ForgeSentry: AI-Powered IoT Threat Intelligence System

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)
![ELK Stack](https://img.shields.io/badge/-ElasticStack-005571?style=flat&logo=elasticsearch)

**ForgeSentry** is an autonomous cybersecurity ecosystem that deploys high-interaction honeypots to capture real-time attacks, aggregates logs via the ELK stack, and utilizes a **Random Forest Machine Learning model** to classify attack vectors (e.g., Mirai Botnet, Brute Force, RCE) instantly.

---

## 🚀 Key Features

*   **🍯 Dual-Layer Decoys**:
    *   **Cowrie**: Simulates SSH/Telnet authentication to capture brute-force attempts and shell interaction.
    *   **Conpot**: Simulates Industrial Control Systems (ICS/SCADA) and IoT devices (Modbus, S7).
*   **🧠 Cognitive Engine**:
    *   Trained on 10,000+ synthetic attack vectors (TF-IDF Vectorization + Random Forest).
    *   **99% Accuracy** in distinguishing between benign traffic and known IoT botnet patterns.
*   **⚡ Real-Time Detection API**:
    *   FastAPI microservice that provides sub-millisecond threat classification.
*   **📊 Visualization**:
    *   **Live Web Portal**: Dedicated product landing page (`index.html`).
    *   **Cyberpunk SOC Monitor**: Real-time threat visualization interface (`dashboard/monitor.html`).
    *   **Kibana Integration**: Geolocation mapping and attack frequency analysis.

## 🏗️ Architecture

```mermaid
graph TD
    A[Attacker] -->|SSH/Telnet| B(Cowrie Honeypot)
    A -->|Modbus/HTTP| C(Conpot Honeypot)
    B -->|JSON Logs| D{Logstash}
    C -->|Syslog| D
    D -->|Ingest| E[(Elasticsearch)]
    E -->|Training Data| F[AI Engine / Scikit-Learn]
    F -->|Model| G(Detection API)
    G -->|Export| I[Threat Intel Feed / Blacklist]
    E -->|Visualize| H(Kibana Dashboard)

    subgraph "Feedback Loop"
    H_Real[Real Attacks] --> E
    E -->|Extract| J[Retraining Pipeline]
    J -->|Update| F
    end

    subgraph "Sandbox"
    B -->|Downloads| K[Payload Analyzer]
    K -->|Hash/Malware Report| L[Threat Intel]
    end
```

## 🛠️ Installation & Deployment

### Prerequisites
*   Docker & Docker Compose
*   Python 3.9+
*   1x VPS (AWS Lightsail, DigitalOcean, etc.) - **Do NOT run locally.**

### 1. Deploy Infrastructure
```bash
git clone https://github.com/yourusername/ForgeSentry.git
cd ForgeSentry/deployment
chmod +x setup.sh
./setup.sh
```

### 2. Train the AI Model (The Feedback Loop)
You can train on synthetic data OR real-world logs captured by your honeypot.

**Option A: Virtual Training (Synthetic)**
```bash
cd ../ai_engine
python generate_dummy_data.py
python train_model.py --input ../data_processing/training_data.csv
```

**Option B: Real-World Feedback Loop**
Once your honeypot has been running and attracting hackers:
```bash
python retrain_pipeline.py
```
*This extracts real logs from Elasticsearch and retrains the model to adapt to new threats.*

### 3. Threat Intelligence & Sandbox
**Payload Analysis**:
Scan captured malware files dropped by bots:
```bash
python ../threat_intel/payload_analyzer.py
```

**Export Threat Feed**:
The API serves live intelligence feeds of detected malicious IPs:
- **JSON Blacklist**: `GET /feed/blacklist`
- **STIX 2.1 (Interop)**: `GET /feed/stix` (Professional format for SIEM/Firewall integration)

---

## 🏛️ Powered by Intel Forge
ForgeSentry is built in collaboration with **Intel Forge**, focusing on "Data Beyond History." It implements advanced security standards to ensure that captured threat data is actionable and interoperable across the global cybersecurity ecosystem.


### 4. Start Detection Service
```bash
cd ..
uvicorn detection.detection_api:app --reload
```

### 🌍 View Web Interfaces
- **Main Portal**: Open `index.html` in your browser.
- **Live Monitor**: Open `dashboard/monitor.html` in your browser.

## 📊 Dashboard
Access Kibana at `http://<your-vps-ip>:5601` to view your Threat Map.

## 🤝 Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## 👨‍💻 Author

**Muhammad Hamza Iqbal** - [Connect on LinkedIn](https://www.linkedin.com/in/muhammad-hamza-iqbal-0b4413293/)
**Intel Forge** — [*“Data Beyond History”*](https://intelforge.org)

## 📜 License
[MIT](https://choosealicense.com/licenses/mit/)
