pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'healthcare-system'
        REGISTRY = 'your-docker-registry'  // e.g., 'docker.io/yourusername' or leave as is for local
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
                    docker.withRegistry('', 'docker-registry-credentials') {  // Configure credentials in Jenkins
                        dockerImage.push("${env.BUILD_NUMBER}")
                        dockerImage.push("latest")
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    // Assuming kubectl is configured in Jenkins agent
                    sh "kubectl set image deployment/healthcare-app healthcare-app=${REGISTRY}/${DOCKER_IMAGE}:${env.BUILD_NUMBER} --namespace=healthcare-system"
                    sh "kubectl rollout status deployment/healthcare-app --namespace=healthcare-system"
                }
            }
        }
    }

    post {
        always {
            sh 'docker system prune -f'
        }
    }
}