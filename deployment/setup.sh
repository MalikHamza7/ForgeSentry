#!/bin/bash

# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install Docker
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
sudo apt-get install -y docker-ce

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Create directories for logs
mkdir -p cowrie/var
mkdir -p cowrie/etc
mkdir -p conpot/logs

# Start services
sudo docker-compose up -d

echo "Honeypots deployed successfully!"
echo "Cowrie SSH running on port 2222"
echo "Conpot services running on ports 80, 102, 502, 161"
