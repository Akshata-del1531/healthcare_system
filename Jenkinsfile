pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'healthcare-system'
        REGISTRY = 'docker.io/akshata234'
        AWS_REGION = 'ap-south-1'
        CLUSTER_NAME = 'healthcare-cluster'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${REGISTRY}/${DOCKER_IMAGE}:${env.BUILD_NUMBER}")
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'docker-registry-credentials') {
                        bat "docker push ${REGISTRY}/${DOCKER_IMAGE}:${env.BUILD_NUMBER}"
                        bat "docker tag ${REGISTRY}/${DOCKER_IMAGE}:${env.BUILD_NUMBER} ${REGISTRY}/${DOCKER_IMAGE}:latest"
                        bat "docker push ${REGISTRY}/${DOCKER_IMAGE}:latest"
                    }
                }
            }
        }

        stage('Configure AWS & EKS Access') {
            steps {
                withCredentials([
                    [$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-credentials']
                ]) {
                    bat """
                    aws --version
                    aws sts get-caller-identity
                    aws eks update-kubeconfig --region %AWS_REGION% --name %CLUSTER_NAME%
                    kubectl get nodes
                    """
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                bat """
                kubectl set image deployment/healthcare-app ^
                healthcare-system=%REGISTRY%/%DOCKER_IMAGE%:%BUILD_NUMBER% ^
                --namespace=healthcare-system

                kubectl rollout status deployment/healthcare-app ^
                --namespace=healthcare-system
                """
            }
        }
    }

    post {
        always {
            bat "docker system prune -f"
        }
    }
}