pipeline {
    agent any
    
    environment {
        AWS_DEFAULT_REGION = "ap-south-1"
        AWS_ACCOUNT_ID = "388779989161"
        IMAGE_TAG = "latest"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/govind02420/Project_Orchestration_and_Scaling.git'
            }
        }

        stage('Build Docker Images') {
            steps {
                script {
                    sh 'docker build -t hello-service ./backend/helloService'
                    sh 'docker build -t profile-service ./backend/profileService'
                    sh 'docker build -t frontend ./frontend'
                }
            }
        }

        stage('Tag & Push to ECR') {
            steps {
                script {
                    sh """
                    aws ecr get-login-password --region $AWS_DEFAULT_REGION | \
                      docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com
                    
                    docker tag hello-service:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/hello-service:$IMAGE_TAG
                    docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/hello-service:$IMAGE_TAG

                    docker tag profile-service:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/profile-service:$IMAGE_TAG
                    docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/profile-service:$IMAGE_TAG

                    docker tag frontend:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/frontend:$IMAGE_TAG
                    docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/frontend:$IMAGE_TAG
                    """
                }
            }
        }
    }
}
