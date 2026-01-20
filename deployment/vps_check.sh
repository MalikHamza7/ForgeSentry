#!/bin/bash

echo "🛡️ ForgeSentry System Health Check"
echo "=============================="
echo "Timestamp: $(date)"
echo ""

# 1. Check Docker Status
echo "[1] Checking Docker Containers..."
REQUIRED_CONTAINERS=("cowrie" "conpot" "elasticsearch" "logstash" "kibana")
ALL_UP=true

for container in "${REQUIRED_CONTAINERS[@]}"; do
    if docker ps --format '{{.Names}}' | grep -q "^${container}$"; then
        echo "   ✅ $container: RUNNING"
    else
        echo "   ❌ $container: NOT RUNNING"
        ALL_UP=false
    fi
done

if [ "$ALL_UP" = true ]; then
    echo "   >> All services are operational."
else
    echo "   >> ⚠️  Some services are down. Check 'docker-compose logs <service>'."
fi

# 2. Check Critical Ports
echo -e "\n[2] Checking Critical Ports..."
PORTS=(2222 2223 80 502 9200 5601)
for port in "${PORTS[@]}"; do
    # Using python to check port if netstat/ss not installed or restricted
    (echo > /dev/tcp/127.0.0.1/$port) >/dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "   ✅ Port $port: LISTENING"
    else
        echo "   ❌ Port $port: CLOSED"
    fi
done

# 3. Resource Usage
echo -e "\n[3] Resource Usage..."
# Disk usage of the project folder
DU=$(du -sh . 2>/dev/null | cut -f1)
echo "   📂 Project Size: $DU"
# System Memory
MEM=$(free -h | awk '/^Mem:/ {print $3 "/" $2}')
echo "   🧠 RAM Usage: $MEM"
# Disk Space
DISK=$(df -h / | awk 'NR==2 {print $5}')
echo "   💾 Disk Usage: $DISK"

# 4. API Check (if running locally)
echo -e "\n[4] Detection API Check..."
API_URL="http://127.0.0.1:8000/health"
HTTP_STATUS=$(curl -o /dev/null -s -w "%{http_code}\n" $API_URL)
if [ "$HTTP_STATUS" == "200" ]; then
    echo "   ✅ API is responding (200 OK)"
else
    echo "   ⚠️  API not detected at localhost:8000 (Status: $HTTP_STATUS)"
    echo "      (Make sure you started it with 'uvicorn detection.detection_api:app')"
fi

echo -e "\n=============================="
echo "Health check complete."
