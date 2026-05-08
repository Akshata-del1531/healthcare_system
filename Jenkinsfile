pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'healthcare-system'
        REGISTRY = 'docker.io/yourusername'  // Replace 'yourusername' with your Docker Hub username
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
                    // Use bat for Windows or ensure kubectl is available
                    if (isUnix()) {
                        sh "kubectl set image deployment/healthcare-app healthcare-app=${REGISTRY}/${DOCKER_IMAGE}:${env.BUILD_NUMBER} --namespace=healthcare-system"
                        sh "kubectl rollout status deployment/healthcare-app --namespace=healthcare-system"
                    } else {
                        bat "kubectl set image deployment/healthcare-app healthcare-app=${REGISTRY}/${DOCKER_IMAGE}:${env.BUILD_NUMBER} --namespace=healthcare-system"
                        bat "kubectl rollout status deployment/healthcare-app --namespace=healthcare-system"
                    }
                }
            }
        }
    }

    post {
        always {
            script {
                if (isUnix()) {
                    sh 'docker system prune -f'
                } else {
                    bat 'docker system prune -f'
                }
            }
        }
    }
}