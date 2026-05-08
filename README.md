# Cloud-Native Healthcare Medical Records System

A simple web-based healthcare record system built with FastAPI, MongoDB, Docker, Jenkins CI/CD, and Kubernetes manifests.

## Features

- FastAPI backend with CRUD APIs for patient records
- MongoDB persistence
- Minimal HTML frontend for record creation and listing
- JWT-based login and token authentication
- Docker containerization
- Jenkins CI/CD pipeline
- Kubernetes deployment manifests for cloud-ready orchestration

## Local development

Open a terminal in the project root folder (`c:\Users\Akshata Madar\healthcare_system`). Then run the commands below.

1. Install dependencies:
   ```powershell
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```
2. Start MongoDB (local or use Docker):
   ```powershell
   docker run -d --name healthcare-mongo -p 27017:27017 mongo:7.0
   ```
3. Run the app from the same project root:
   ```powershell
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
4. Open a browser and visit `http://localhost:8000`.

## CI/CD with Jenkins

The project includes a Jenkinsfile for automated CI/CD pipeline. The pipeline:

- Builds the Docker image
- Pushes to a Docker registry
- Deploys to Kubernetes cluster

Configure Jenkins with:
- Docker registry credentials (`docker-registry-credentials`)
- Kubernetes cluster access (kubectl configured)

## Default user

- username: `admin`
- password: `Health123!`

## Browser login

The web UI supports login via `/login` and stores a JWT in a secure HTTP-only cookie. After login, use the `/patients` interface to add, view, and delete records.

## Docker

Build and run locally:
```bash
docker build -t healthcare-system .
docker run -p 8000:8000 --env MONGO_URL="mongodb://host.docker.internal:27017" healthcare-system
```

## GitHub Actions

A workflow is provided at `.github/workflows/ci.yml` that installs dependencies and lints the app.

## Kubernetes

Manifests are available in the `k8s/` directory for deployment and service configuration.

## AWS Deployment

This repo includes a GitHub Actions workflow at `.github/workflows/aws-deploy.yml` that builds the Docker image, pushes it to Amazon ECR, and deploys to Amazon EKS.

### Required GitHub secrets

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION`
- `ECR_REPOSITORY`
- `EKS_CLUSTER_NAME`

### How it works

1. Push to the `main` branch.
2. GitHub Actions builds and pushes the container image to ECR.
3. The workflow applies the Kubernetes manifests in `k8s/`.
4. `healthcare-app` is exposed through a LoadBalancer service on AWS.

### AWS Kubernetes files

- `k8s/app-deployment.yaml` — deployment for the FastAPI app
- `k8s/app-service-loadbalancer.yaml` — AWS-compatible service for public access
- `k8s/mongo-deployment.yaml` — MongoDB deployment
- `k8s/mongo-service.yaml` — MongoDB service
