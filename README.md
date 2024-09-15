# VirtuaFit

VirtuaFit is a microservices-based fitness application built to provide a comprehensive system for user authentication, workout tracking, and data analytics. It uses Flask for the services, PostgreSQL as the database, SQLAlchemy for ORM, JWT for authentication, and Kubernetes for deployment and orchestration.

## Infrastructure Architecture Diagram
```
        ┌──────────────────────────┐
        │        Client            │
        └──────────────────────────┘
                ↓
┌───────────────────────────────────────────────────────┐
│                                                       │
│           Google Cloud Load Balancer                  │
│                                                       │
└───────────────────────────────────────────────────────┘
                ↓

┌──────────────────────────────────────────────────────────┐
│                                                          │
│           Virtual Private Cloud (VPC)                    │
│                                                          │
│ ┌────────────────────────────────────────────────────┐   │
│ │                                                    │   │
│ │        Google Kubernetes Engine (GKE)              │   │
│ │                                                    │   │
│ │ ┌────────────────────────────────────────────┐     │   │
│ │ │     NGINX (Reverse Proxy & Load Balancer)  │     │   │
│ │ └────────────────────────────────────────────┘     │   │
│ │                                                    │   │
│ │ ┌─────────────┐  ┌─────────────┐  ┌──────────────┐ │   │
│ │ │  Auth Svc   │  │ Workout Svc │  │ Analytics Svc│ │   │
│ │ └─────────────┘  └─────────────┘  └──────────────┘ │   │
│ │                                                    │   │
│ │ ┌────────────────────────────────────────────────┐ │   │
│ │ │            PostgreSQL Database                 │ │   │
│ │ └────────────────────────────────────────────────┘ │   │
│ └────────────────────────────────────────────────────┘   │
│                                                          │
└──────────────────────────────────────────────────────────┘

```

## Installation and Setup

### Prerequisites

- Google Cloud account and project
- Terraform and Terragrunt installed locally
- Docker installed locally
- PostgreSQL

## Table of Contents

- Project Structure
- Services Overview
- Auth Service
- Workout Service
- Analytics Service
- Infrastructure
- NGINX
- CI/CD Pipeline
- End-to-End Testing
---

## Project Structure

```bash
├── README.md
├── dockerconfig.json               # Docker config for Google Artifact Registry
├── infrastructure/                 # Terraform and Terragrunt infrastructure files
│   ├── live/
│   │   ├── envs/
│   │   │   └── dev/                # Dev environment configurations
│   │   ├── main.tf                 # Shared Main Terraform configuration file accros environments
│   │   ├── modules/
│   │   │   ├── gke/                # GKE module
│   │   │   └── vpc/                # VPC module
│   │   └── variables.tf            # Shared Varibles Terraform configuration file accros environments
├── nginx/                          # NGINX configurations and Helm chart
│   ├── nginx-configmap.yaml
│   ├── nginx-deployment.yaml
│   ├── nginx-service.yaml
│   └── nginx-chart/                # NGINX Helm chart for Kubernetes
├── services/                       # Microservices source code
│   ├── analytics_service/
│   ├── auth_service/
│   ├── workout_service/
│   └── db/                         # Database setup using SQLAlchemy and PostgreSQL
├── tests/                          # Test files for the project
│   └── e2e/                        # End-to-end tests
│       ├── test_e2e.py             # e2e test file
├── venv/                           # Virtual environment for Python testing dependencies
```

---

## Services Overview

VirtuaFit has three key microservices: **Auth**, **Workout**, and **Analytics**. Each of these is built with Flask, and they all interact with a PostgreSQL database using **SQLAlchemy** ORM. **JWT** tokens are used for secure authentication and authorization across the services.

### Auth Service

The **Auth Service** manages user registration, login, and token generation for secure access.

- **Endpoints:**
  - `POST /register`: Registers a new user.
  - `POST /login`: Logs in a user and provides a JWT token.
  - `GET /health`: Health check for the Auth service.

- **Technologies:**
  - **Flask**
  - **JWT** for token-based authentication
  - **SQLAlchemy** ORM
  - **PostgreSQL**

- **Source code:** `services/auth_service`

### Workout Service

The **Workout Service** allows users to create and retrieve their workout data. JWT tokens are required for all requests to this service.

- **Endpoints:**
  - `POST /workouts`: Adds a new workout (JWT token required).
  - `GET /workouts`: Retrieves all workouts for the current user (JWT token required).
  - `GET /health`: Health check for the Workout service.

- **Technologies:**
  - **Flask**
  - **JWT** for token-based authentication
  - **SQLAlchemy** ORM
  - **PostgreSQL**

- **Source code:** `services/workout_service`

### Analytics Service

The **Analytics Service** provides workout statistics for the current user. JWT tokens are used here too.

- **Endpoints:**
  - `GET /analyticsdata`: Fetches analytics data (JWT token required).
  - `GET /health`: Health check for the Analytics service.

- **Technologies:**
  - **Flask**
  - **JWT**
  - **SQLAlchemy**
  - **PostgreSQL**

- **Source code:** `services/analytics_service`

---

## Infrastructure

VirtuaFit's infrastructure is managed using **Terraform** and **Terragrunt**. The setup includes:

- **Google Kubernetes Engine (GKE)**: Main Kubernetes cluster.
- **Virtual Private Cloud (VPC)**: Manages network isolation for the services.
- **PostgreSQL**: Managed database deployed using StatefulSet in Kubernetes.
- **NGINX**: Reverse proxy for routing traffic.

### Database (PostgreSQL)

The PostgreSQL database is used by all microservices, and it’s set up via a StatefulSet in Kubernetes. SQLAlchemy is used to interact with the database.

SQLAlchemy Setup:
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Config

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

---

## NGINX

NGINX is set up as a reverse proxy, routing traffic to the correct microservices. The Helm chart is used to deploy it on Kubernetes.

Key Files:
- `nginx-configmap.yaml`: Configures routing between services.
- `nginx-deployment.yaml`: Defines the NGINX deployment.
- `nginx-service.yaml`: Exposes NGINX as a service.

---

## CI/CD Pipeline

VirtuaFit’s CI/CD pipeline is configured via GitHub Actions and automates the deployment process, including building Docker images, provisioning infrastructure, and running tests.

### Pipeline Jobs

1. **Setup GKE and VPC**: Provisions the GKE cluster and VPC.
2. **Build and Push Docker Images**: Builds Docker images for all services and pushes them to Artifact Registry.
3. **Run End-to-End Tests**: Runs tests on the deployed application.

### Triggering the Pipeline

- The pipeline runs on push events to the `main` branch and pull request events.

---

## End-to-End Testing

End-to-end (E2E) tests are located in the `tests/e2e/` folder. They verify the overall functionality of the application.

Key Tests:
- Health checks for the Auth, Workout, and Analytics services.
- User registration and login functionality.
- Basic workout creation and retrieval.
- Analytics data fetch.
