# MERN Microservices – Orchestration & Scaling
This project demonstrates a microservices-based MERN stack application orchestrated with Docker Compose / Kubernetes, showcasing containerization, scaling, and inter-service communication.

It includes:
- Backend Services
    - helloService – A simple Node.js service (Hello World).
    - profileService – A Node.js + MongoDB service (manages user profiles).
- Frontend
    - React.js client for interacting with backend APIs.
- Database
    - MongoDB (for profile service).
#
## Project Structure
```bash
MERN_Microservices/
│── backend/
│   ├── helloService/
│   │   ├── Dockerfile
│   │   ├── index.js
│   │   ├── package.json
│   │   └── .env
│   ├── profileService/
│   │   ├── Dockerfile
│   │   ├── index.js
│   │   ├── package.json
│   │   └── .env
│
│── frontend/
│   ├── Dockerfile
│   ├── package.json
│   ├── src/
│   ├── public/
│   └── .env
│
│── docker-compose.yml
└── README.md

```
#
## Step 1: Set Up AWS CLI and Boto3
### Step 1: Install AWS CLI

The AWS Command Line Interface (CLI) allows you to interact with AWS services directly from your terminal.Download the installer from AWS CLI Installer for Windows.
Run the installer and complete setup.

### Step 2: Configure AWS CLI credentials
After installation, configure your AWS CLI with your Access Key ID and Secret Access Key (from the AWS console → IAM → Users → Security Credentials).

```bash
aws configure
```
You’ll be prompted for:
```
AWS Access Key ID [None]: <your-access-key-id>
AWS Secret Access Key [None]: <your-secret-access-key>
Default region name [None]: ap-south-1
Default output format [None]: json
```
### Step 3 Verify CLI authentication
```bash
aws sts get-caller-identity

```
### Step 4: Ensure pip is installed for Python
```bash
py -3.11 -m ensurepip --upgrade
py -3.11 -m pip install --upgrade pip
```
### Step 2: Install boto3
```bash
py -3.11 -m pip install boto3

```
### Step 3: Verify boto3 installation
```bash
py -3.11 -c "import boto3; print(boto3.__version__)"
```
#
## SETP 2  Prepare the MERN Application

### 2.1 Containerize the MERN Application
1. .env Files
    Create .env files inside each backend service directory.
    - backend/helloService/.env
    - backend/profileService/.env

2. Dockerfiles Containerization for This Project
    Create Dockerfiles inside each backend service and frontend.
    - backend/helloService/Dockerfile
    - backend/profileService/Dockerfile
    - frontend/Dockerfile

3. Docker Compose for Local Testing
    Inside root directory ce=reate docker-compose.yml for local tessting

4. Local Testing
    After preparing the .env files and Dockerfiles, test locally:
```bash
docker-compose up --build
```
 - Frontend: http://localhost:8090
 - HelloService: http://localhost:3001
 - ProfileService: http://localhost:3002

#
### 2.2 Push Docker Images to Amazon ECR
1. Build Docker Images Locally
``` bash
# Backend services
docker build -t hello-service:latest ./backend/helloService
docker build -t profile-service:latest ./backend/profileService

# Frontend
docker build -t frontend:latest ./frontend
```

2. Create ECR Repositories
Run these AWS CLI commands (replace <aws-region> with your region, e.g. ap-south-1):
```bash
aws ecr create-repository --repository-name hello-service --region <aws-region>
aws ecr create-repository --repository-name profile-service --region <aws-region>
aws ecr create-repository --repository-name frontend --region <aws-region>
```

4. Authenticate Docker to ECR
```bash
aws ecr get-login-password --region <aws-region> | docker login --username AWS --password-stdin <aws_account_id>.dkr.ecr.<region>.amazonaws.com

```

5. Tag Images for ECR
Replace <aws_account_id> and <region> with your details:
```bash
docker tag hello-service:latest <aws_account_id>.dkr.ecr.<region>.amazonaws.com/hello-service:latest
docker tag profile-service:latest <aws_account_id>.dkr.ecr.<region>.amazonaws.com/profile-service:latest
docker tag frontend:latest <aws_account_id>.dkr.ecr.<region>.amazonaws.com/frontend:latest
```
6. Push Images to ECR

```bash
docker push <aws_account_id>.dkr.ecr.<region>.amazonaws.com/hello-service:latest
docker push <aws_account_id>.dkr.ecr.<region>.amazonaws.com/profile-service:latest
docker push <aws_account_id>.dkr.ecr.<region>.amazonaws.com/frontend:latest
```

## Step 3: Version Control with AWS CodeCommit
**AWS has stopped allowing new customers to onboard to CodeCommit**
Version Control with GitHub
👉 https://github.com/govind02420/Project_Orchestration_and_Scaling.git

1. Create a CodeCommit Repository
```bash
aws codecommit create-repository --repository-name mern-microservices --repository-description "MERN microservices project V1" --region ap-south-1
```

