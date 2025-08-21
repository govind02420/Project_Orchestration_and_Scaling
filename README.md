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
## Set Up AWS CLI and Boto3
### Install AWS CLI

The AWS Command Line Interface (CLI) allows you to interact with AWS services directly from your terminal.Download the installer from AWS CLI Installer for Windows.
Run the installer and complete setup.

### Configure AWS CLI credentials
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
### Verify CLI authentication
```bash
aws sts get-caller-identity

```
### Ensure pip is installed for Python
```bash
py -3.11 -m ensurepip --upgrade
py -3.11 -m pip install --upgrade pip
```
### Install boto3
```bash
py -3.11 -m pip install boto3

```
### Verify boto3 installation
```bash
py -3.11 -c "import boto3; print(boto3.__version__)"
```
#
## Prepare the MERN Application

### Containerize the MERN Application
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
### Push Docker Images to Amazon ECR
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
#
## Version Control with  GitHub
**AWS has stopped allowing new customers to onboard to CodeCommit**
#
## Continuous Integration with Jenkins

### Set Up Jenkins on EC2
- Jenkins able to run Docker builds and push to ECR (via IAM Role)
- GitHub webhook-ready

1) Launch the EC2 instance

2) SSH into EC2
```bash
ssh -i /path/to/your-key.pem ec2-user@<EC2-PUBLIC-IP>
sudo yum update -y
```
3) Install Java (Jenkins needs Java 17)
```bash
sudo rpm --import https://yum.corretto.aws/corretto.key
sudo curl -Lo /etc/yum.repos.d/corretto.repo https://yum.corretto.aws/corretto.repo
sudo yum install -y java-17-amazon-corretto-devel
java -version
```
4) Install Jenkins
```bash
sudo wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat-stable/jenkins.repo
sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io-2023.key
sudo yum install -y jenkins
sudo systemctl enable jenkins
sudo systemctl status jenkins
```

    - You Get the initial admin password:
```bash
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```
Open your browser: http://<EC2-PUBLIC-IP>:8080 → paste the password → Install Suggested Plugins : Docker Pipeline

- Restart Jenkins after plugin installs (Manage Jenkins → Restart).

5) Install Docker and let Jenkins use it
- Install Docker
```bash
sudo amazon-linux-extras install docker -y || sudo yum install -y docker
sudo systemctl enable --now docker
docker --version
```
- Allow Jenkins user to run Docker
```bash
sudo usermod -aG docker jenkins
sudo systemctl restart docker
sudo systemctl restart jenkins
```

Pitfall: If you forget to add jenkins to the docker group, builds will fail with “permission denied”.

8) Jenkins basic configuration

Manage Jenkins → System → Jenkins URL: set it to http://<EC2-PUBLIC-IP>:8080/

(Optional) Credentials: If you didn’t attach an IAM role and must use keys, add AWS credentials in Manage Jenkins → Credentials → Global.

9) Quick sanity check (optional but useful)
- You should see your AWS account and Docker daemon details.
```bash
aws sts get-caller-identity
docker info | head -n 20
```

10) Set up a GitHub webhook

In GitHub: Repo → Settings → Webhooks → Add webhook

- Payload URL: http://<EC2-PUBLIC-IP>:8080/github-webhook/
- Content type: application/json
- Events: Just the push event
- Security Group: Ensure port 8080 is open to GitHub (0.0.0.0/0 is fine temporarily)


### Create Jenkins Pipeline Job
1) Create Pipeline Job

On Jenkins dashboard → New Item.
Enter a job name: MERN-ECR-Pipeline
Choose Pipeline → Click OK.

2) Configure Pipeline Job

- Under General: Check GitHub project.
- Enter your repo URL: https://github.com/username/repository_name
- Under Build Triggers: Check GitHub hook trigger for GITScm polling 
- Under Pipeline: Choose Pipeline script from SCM.
    - SCM → Git.
    - Repository URL: mention your repository_name url
    - Branch: */main
    - Script Path: Jenkinsfile (your repo already has one).
- Click Save.

3) Build

- Click Build Now to test.
```
Jenkins will:
    Clone your GitHub repo.
    Run the Jenkinsfile you created.
    Build Docker images.
    Push them to your ECR repos.
```
#
## Infrastructure as Code (IaC) with Boto3

This step provisions the networking and IAM base infrastructure required for backend deployment.
- Create Virtual Private Cloud (VPC)
- Create Subnets: Creates public subnets in multiple AZs
- Create Security Group: Creates backend-sg
- Allows inbound ports (5000, 5001, 22 for SSH)
- Create IAM Role for EC2
- Creates IAM Role with EC2 + ECR permissions
- Attaches policy for ECR login & S3

```bash
python infrastructure.py
```

✅ Now you have:
VPC + Subnets
Security Group
IAM Role
#
### Deploy Backend Services (EC2 + ASG)

This step deploys Dockerized backend (hello-service & profile-service) using Launch Template + ASG.
- Create Security Group for Backend: 
    - Creates Security Group backend-sg if not already created
    - Save the SG ID (needed in Launch Template)
```bash
python security_group.py
```
- Prepare User Data (Do not execute directly)
    - Create file userdata.sh:

- Create Launch Template
    Uses:
    - Latest Ubuntu AMI
    - Security Group ID from step 6.1
    - userdata.sh
```bash
python launch_template.py
```

- Create Auto Scaling Group
    - Uses Launch Template
    - Deploys across your VPC Subnets
    - Minimum size: 1
    - Maximum size: 3
    - Desired: 2
```bash
python auto_scaling_group.py
```
- Create Target Group (for Load Balancer)
    - Creates Target Group for backend instances
    - Port: 5000 (hello-service) or 5001 (profile-service)
```bash
python target_group.py 
```
- Now you have:
    - Security Group backend-sg
    - Launch Template with userdata (runs Dockerized backend)
    - Auto Scaling Group that keeps backend instances running
    - Target Group ready for ALB

## Networking
- Create Application Load Balancer (ALB)
- Configure DNS with Route 53

- After Step 7
    - backend-alb (internet-facing) distributes traffic to backend ASG.
    - You can hit 
        - http://ALB_DNS_NAME/ → forwards to hello-service (port 5000 inside container).
        - http://ALB_DNS_NAME/profile/ → forwards to profile-service (port 5001 inside container).
