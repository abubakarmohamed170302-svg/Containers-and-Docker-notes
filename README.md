# Containers and Docker Notes

This repository documents my learning and hands-on experience from the Containers and Docker module of the CoderCo DevOps Academy.

The notes cover container fundamentals, Dockerfiles, networking, Docker Compose, container registries, multi-stage builds and container orchestration.

I also completed a practical multi-container project using Flask, Redis, Nginx and Docker Compose.

---

## Module Contents

### 1. Containers and Docker Introduction

Learn the fundamental concepts behind containers and Docker, including:

- What containers are
- Why containers are used
- Docker images and containers
- Docker architecture
- Virtual machines versus containers
- Common Docker terminology

[View Containers and Docker Introduction](./01-containers-and-docker-introduction.md)

---

### 2. Docker Fundamentals and Containerisation

Learn how to create and run containerised applications, including:

- Installing Docker
- Understanding Dockerfiles
- Dockerfile instructions
- Building Docker images
- Running Docker containers
- Containerising a Flask application
- Port mapping
- Docker networking
- Troubleshooting common errors

[View Docker Fundamentals and Containerisation](./02-docker-fundamentals-and-containerisation.md)

---

### 3. Docker Compose

Learn how Docker Compose manages multi-container applications, including:

- Understanding YAML
- Creating a `docker-compose.yml` file
- Defining services
- Environment variables
- Service dependencies
- Compose networking
- Building and starting services
- Viewing logs
- Debugging Compose errors

[View Docker Compose Notes](./03-docker-compose.md)

---

### 4. Docker Registries

Learn how container images are stored and distributed, including:

- Docker registries
- Docker Hub
- Public and private registries
- Tagging images
- Pushing and pulling images
- Amazon Elastic Container Registry
- Authenticating with Amazon ECR
- Registry troubleshooting

[View Docker Registries Notes](./04-docker-registries.md)

---

### 5. Docker Commands and Multi-Stage Builds

A practical reference covering:

- Docker image commands
- Docker container commands
- Docker network commands
- Docker volume commands
- Docker Compose commands
- Cleaning unused Docker resources
- Reducing image sizes
- Using `.dockerignore`
- Multi-stage Docker builds
- Build troubleshooting

[View Docker Commands and Multi-Stage Builds](./05-docker-commands-and-multistage-builds.md)

---

### 6. Container Orchestration

Learn how containers are managed at scale, including:

- Container orchestration
- Clusters and nodes
- Desired state
- Scheduling
- Scaling
- Load balancing
- Self-healing
- Rolling updates and rollbacks
- Kubernetes fundamentals
- Docker Swarm
- Docker Swarm versus Kubernetes

[View Container Orchestration Notes](./06-container-orchestration.md)

---

### 7. Multi-Container Project

A practical application built using:

- Python Flask
- Redis
- Nginx
- Docker Compose
- Docker networks
- Docker volumes
- Environment variables
- Health checks
- Reverse proxying
- Load balancing

The application contains a homepage and a page that stores and increments a visit counter in Redis.

[View Multi-Container Project Summary](./07-multicontainer-project.md)

---

## Project Architecture

```text
User
  |
  v
Nginx
  |
  v
Flask Containers
  |
  v
Redis
  |
  v
Persistent Docker Volume
```

Nginx receives the browser request and distributes traffic between the Flask containers. The Flask application communicates with Redis, while the Docker volume preserves the counter data.

---

## Technologies Used

| Technology | Purpose |
|---|---|
| Docker | Builds and runs containers |
| Docker Compose | Manages the multi-container application |
| Python Flask | Provides the web application |
| Redis | Stores the visit count |
| Nginx | Provides reverse proxying and load balancing |
| Amazon ECR | Stores Docker images in AWS |
| Git and GitHub | Provides version control and documentation |

---

## Key Skills Developed

- Writing Dockerfiles
- Building and managing Docker images
- Running and troubleshooting containers
- Creating Docker networks and volumes
- Managing applications with Docker Compose
- Configuring persistent Redis storage
- Using environment variables
- Configuring health checks
- Scaling Flask containers
- Configuring Nginx as a reverse proxy
- Pushing images to Docker Hub and Amazon ECR
- Understanding container orchestration

---

## Author

**Abubakar Mohamed**

Aspiring DevOps Engineer currently completing the CoderCo DevOps Academy.

[Connect with me on LinkedIn](https://www.linkedin.com/in/abubakar-mohamed-3047a5211/)
