import hashlib
import os
import csv
import datetime

# Path to Cowrie downloads (mapped in Docker)
DOWNLOADS_DIR = "../deployment/cowrie/var/lib/cowrie/downloads"
REPORT_FILE = "malware_report.csv"

def calculate_sha256(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def analyze_payloads():
    if not os.path.exists(DOWNLOADS_DIR):
        print(f"Warning: Downloads directory not found at {DOWNLOADS_DIR}")
        print("Ensure the honeypot has started and volumes are mapped correctly.")
        return

    print(f"Scanning payloads in {DOWNLOADS_DIR}...")
    
    report_data = []
    
    for root, dirs, files in os.walk(DOWNLOADS_DIR):
        for file in files:
            filepath = os.path.join(root, file)
            file_hash = calculate_sha256(filepath)
            file_size = os.path.getsize(filepath)
            timestamp = datetime.datetime.fromtimestamp(os.path.getmtime(filepath)).isoformat()
            
            report_data.append({
                "timestamp": timestamp,
                "filename": file,
                "sha256": file_hash,
                "size_bytes": file_size,
                "status": "Malicious (Honeypot Capture)"
            })
            
    # Save to CSV
    if report_data:
        keys = report_data[0].keys()
        with open(REPORT_FILE, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(report_data)
        print(f"Analysis complete. Report saved to {REPORT_FILE}")
        print(f"Found {len(report_data)} payloads.")
    else:
        print("No payloads found yet.")

if __name__ == "__main__":
    analyze_payloads()
