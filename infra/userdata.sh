#!/bin/bash
# Update and install Docker
apt update -y
apt install -y docker.io awscli
systemctl start docker
systemctl enable docker

# Login to ECR
aws ecr get-login-password --region ap-south-1 | \
docker login --username AWS --password-stdin 388779989161.dkr.ecr.ap-south-1.amazonaws.com

# Pull and run backend services
docker run -d -p 5000:5000 388779989161.dkr.ecr.ap-south-1.amazonaws.com/hello-service:latest
docker run -d -p 5001:5001 388779989161.dkr.ecr.ap-south-1.amazonaws.com/profile-service:latest
