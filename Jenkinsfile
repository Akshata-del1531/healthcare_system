pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'healthcare-system'
        REGISTRY = 'docker.io/akshata234'
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
                    dockerImage = docker.build("${REGISTRY}/${DOCKER_IMAGE}:${env.BUILD_NUMBER}")
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

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    bat '''
                    echo ===== Updating kubeconfig =====
                    aws eks update-kubeconfig --region ap-south-1 --name healthcare-cluster

                    echo ===== Checking cluster access =====
                    kubectl get nodes

                    echo ===== Deploying new image =====
                    kubectl set image deployment/healthcare-app healthcare-system=docker.io/akshata234/healthcare-system:%BUILD_NUMBER% --namespace=healthcare-system

                    echo ===== Waiting for rollout =====
                    kubectl rollout status deployment/healthcare-app --namespace=healthcare-system
                    '''
                }
            }
        }
    }

    post {
        always {
            script {
                bat 'docker system prune -f'
            }
        }
    }
}
