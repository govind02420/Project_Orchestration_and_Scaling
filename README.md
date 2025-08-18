# Sample MERN with Microservices



For `helloService`, create `.env` file with the content:
```bash
PORT=3001
```

For `profileService`, create `.env` file with the content:
```bash
PORT=3002
MONGO_URL="specifyYourMongoURLHereWithDatabaseNameInTheEnd"
```

Finally install packages in both the services by running the command `npm install`.

<br/>
For frontend, you have to install and start the frontend server:

```bash
cd frontend
npm install
npm start
```

Note: This will run the frontend in the development server. To run in production, build the application by running the command `npm run build`
######

```bash
MERN_Microservices/
 ├── backend/
 │   ├── helloService/
 │   │   ├── index.js
 │   │   ├── package.json
 │   ├── profileService/
 │       ├── index.js
 │       ├── package.json
 ├── frontend/
 │   ├── package.json
 │   ├── src/
 │   │   ├── App.js
 │   │   ├── components/Home.js
 ├── README.md

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
Step 3 Verify CLI authentication
```bash
aws sts get-caller-identity

```
### Step 1: Ensure pip is installed for Python 3.13
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

1. Create a CodeCommit Repository


