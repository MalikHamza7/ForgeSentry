import os
import sys
import subprocess
import requests
import socket

def check_file(path):
    exists = os.path.exists(path)
    status = "[OK]" if exists else "[MISSING]"
    print(f"   {status:<10} {path}")
    return exists

def check_docker():
    print("\n[2] Checking Docker (Local)...")
    try:
        result = subprocess.run(["docker", "ps", "--format", "{{.Names}}"], capture_output=True, text=True)
        running = result.stdout.strip().split('\n')
        required = ["cowrie", "conpot", "elasticsearch", "logstash", "kibana"]
        
        if not result.stdout.strip():
            print("   ⚠️  Docker is running but no containers found (or Docker not started).")
            return

        for req in required:
            if req in running:
                print(f"   [OK] {req:<15} RUNNING")
            else:
                print(f"   [FAIL] {req:<15} NOT RUNNING")
    except FileNotFoundError:
        print("   [WARN]  Docker command not found. Is Docker Desktop installed?")
    except Exception as e:
        print(f"   [WARN]  Docker check failed: {e}")

def check_api():
    print("\n[3] Checking Detection API...")
    url = "http://127.0.0.1:8000/health"
    try:
        response = requests.get(url, timeout=2)
        if response.status_code == 200:
            print(f"   [OK] API is UP (Status: 200 OK)")
            print(f"   Response: {response.json()}")
        else:
            print(f"   [FAIL] API returned status {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("   [FAIL] API is DOWN (Connection refused)")
        print("      Run: uvicorn detection.detection_api:app --reload")

def check_dependencies():
    print("\n[4] Checking Python Dependencies...")
    required = ['fastapi', 'uvicorn', 'pandas', 'sklearn', 'elasticsearch', 'requests']
    for lib in required:
        try:
            __import__(lib)
            print(f"   [OK] {lib:<15} INSTALLED")
        except ImportError:
            # sklearn is imported as sklearn but installed as scikit-learn
            if lib == 'sklearn':
                try:
                    import sklearn
                    print(f"   [OK] {lib:<15} INSTALLED")
                except:
                     print(f"   [FAIL] {lib:<15} MISSING")
            else:
                print(f"   [FAIL] {lib:<15} MISSING")

def main():
    print("ForgeSentry Local Health Check")
    print("===============================")
    
    print("[1] Checking Key Files...")
    check_file("e:/projects antigrav/honey/ai_engine/model.pkl")
    check_file("e:/projects antigrav/honey/ai_engine/train_model.py")
    check_file("e:/projects antigrav/honey/detection/detection_api.py")
    check_file("e:/projects antigrav/honey/deployment/docker-compose.yml")

    check_docker()
    check_api()
    check_dependencies()

    print("\n===============================")

if __name__ == "__main__":
    main()
