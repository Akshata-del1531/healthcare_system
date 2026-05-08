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
                    def dockerImage = docker.build("${REGISTRY}/${DOCKER_IMAGE}:${env.BUILD_NUMBER}")
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('', 'docker-registry-credentials') {

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

                    if (isUnix()) {

                        sh "export KUBECONFIG=$HOME/.kube/config"

                        sh """
                        kubectl set image deployment/healthcare-app \
                        healthcare-system=${REGISTRY}/${DOCKER_IMAGE}:${env.BUILD_NUMBER} \
                        --namespace=healthcare-system
                        """

                        sh "kubectl rollout status deployment/healthcare-app --namespace=healthcare-system"

                    } else {

                        bat """
                        set KUBECONFIG=C:\\ProgramData\\Jenkins\\.kube\\config
                        kubectl set image deployment/healthcare-app healthcare-system=${REGISTRY}/${DOCKER_IMAGE}:${env.BUILD_NUMBER} --namespace=healthcare-system
                        kubectl rollout status deployment/healthcare-app --namespace=healthcare-system
                        """
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