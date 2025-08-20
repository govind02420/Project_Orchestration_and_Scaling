pipeline {
    agent any

    environment {
        AWS_DEFAULT_REGION = "ap-south-1"
        AWS_ACCOUNT_ID    = "388779989161"
        IMAGE_TAG         = "latest"
        ECR_REGISTRY      = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/govind02420/Project_Orchestration_and_Scaling.git'
            }
        }

        stage('Set Git Commit Short Hash') {
            steps {
                script {
                    GIT_SHORT = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
                    env.GIT_SHORT = GIT_SHORT
                    echo "Using Git commit short hash: ${GIT_SHORT}"
                }
            }
        }

        stage('ECR Login') {
            steps {
                sh """
                  aws ecr get-login-password --region $AWS_DEFAULT_REGION | \
                  docker login --username AWS --password-stdin $ECR_REGISTRY
                """
            }
        }

        stage('Build & Push') {
            parallel {
                stage('Hello Service') {
                    steps {
                        withEnv(['DOCKER_BUILDKIT=1']) {
                            sh """
                              docker build -t hello-service:${GIT_SHORT} ./backend/helloService
                              docker tag hello-service:${GIT_SHORT} $ECR_REGISTRY/hello-service:${GIT_SHORT}
                              docker tag hello-service:${GIT_SHORT} $ECR_REGISTRY/hello-service:${IMAGE_TAG}
                              docker push $ECR_REGISTRY/hello-service:${GIT_SHORT}
                              docker push $ECR_REGISTRY/hello-service:${IMAGE_TAG}
                            """
                        }
                    }
                }
                stage('Profile Service') {
                    steps {
                        withEnv(['DOCKER_BUILDKIT=1']) {
                            sh """
                              docker build -t profile-service:${GIT_SHORT} ./backend/profileService
                              docker tag profile-service:${GIT_SHORT} $ECR_REGISTRY/profile-service:${GIT_SHORT}
                              docker tag profile-service:${GIT_SHORT} $ECR_REGISTRY/profile-service:${IMAGE_TAG}
                              docker push $ECR_REGISTRY/profile-service:${GIT_SHORT}
                              docker push $ECR_REGISTRY/profile-service:${IMAGE_TAG}
                            """
                        }
                    }
                }
                stage('Frontend') {
                    steps {
                        withEnv(['DOCKER_BUILDKIT=1']) {
                            sh """
                              docker build -t frontend:${GIT_SHORT} ./frontend
                              docker tag frontend:${GIT_SHORT} $ECR_REGISTRY/frontend:${GIT_SHORT}
                              docker tag frontend:${GIT_SHORT} $ECR_REGISTRY/frontend:${IMAGE_TAG}
                              docker push $ECR_REGISTRY/frontend:${GIT_SHORT}
                              docker push $ECR_REGISTRY/frontend:${IMAGE_TAG}
                            """
                        }
                    }
                }
            }
        }
    }
}
