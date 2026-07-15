# Multi-Container Flask, Redis & Nginx Challenge (Project Summary)

## Objective

Build a multi-container application using Docker Compose consisting of:

- Flask web application
- Redis database
- Nginx reverse proxy

The Flask application stores and retrieves a visit counter from Redis.

---

# Final Architecture

```text
                 Browser
                     │
                     ▼
             Nginx Container
             (Reverse Proxy)
                     │
        ┌────────────┴────────────┐
        ▼                         ▼
    Flask Container          Flask Container
        │                         │
        └────────────┬────────────┘
                     ▼
              Redis Container
                     │
                     ▼
               Docker Volume
```

Later the Flask application was scaled to three containers.

```text
Browser
    │
    ▼
Nginx
 │   │   │
 ▼   ▼   ▼
Flask Flask Flask
      │
      ▼
    Redis
```

---

# Project Structure

```text
containers-challenge/
│
├── docker-compose.yml
│
├── flask-app/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── redis/
│   ├── Dockerfile
│   └── redis.conf
│
└── nginx/
    ├── Dockerfile
    └── nginx.conf
```

---

# Flask Container

The Flask application contains two routes.

## Homepage

```text
/
```

Displays a welcome message.

## Counter Page

```text
/count
```

Each refresh:

- connects to Redis
- increments the counter
- displays the current visit count

Later, the hostname of the Flask container was displayed so it was possible to see which Flask container handled each request when scaling.

---

# Redis Container

Redis is an in-memory key-value database.

Instead of storing the visit count inside Flask, Redis stores it.

Benefits:

- very fast
- data shared between Flask containers
- data survives Flask container restarts

---

# Redis Volume

A Docker volume was attached to Redis.

```yaml
volumes:
  - redis-data:/data
```

This provides persistent storage.

Testing:

```bash
docker compose down
docker compose up
```

The visit counter continued where it left off, proving the data had been persisted.

---

# Environment Variables

Instead of hard-coding Redis details, Flask reads them from environment variables.

Example:

```yaml
environment:
  REDIS_HOST: redis
  REDIS_PORT: 6379
```

Benefits:

- easier configuration
- portable
- follows DevOps best practices

---

# Docker Compose

Docker Compose manages the complete application.

Instead of starting each container manually, one command starts everything.

```bash
docker compose up
```

Compose automatically:

- builds images
- creates containers
- creates a Docker network
- connects the containers
- creates volumes
- starts all services

---

# Docker Network

Compose automatically creates an internal Docker network.

Containers communicate using service names.

Examples:

```text
redis
flask
nginx
```

Flask connects to Redis using:

```python
host="redis"
```

No IP addresses are required.

---

# Nginx Reverse Proxy

Instead of exposing Flask directly, Nginx sits in front of the application.

Flow:

```text
Browser
    │
    ▼
Nginx
    │
    ▼
Flask
    │
    ▼
Redis
```

Benefits:

- handles incoming traffic
- hides backend services
- prepares the application for scaling
- performs load balancing

---

# Scaling the Application

Docker Compose can create multiple Flask containers.

Example:

```bash
docker compose up --build --scale flask=3
```

Result:

```text
1 Nginx container
3 Flask containers
1 Redis container
```

Each refresh of the application could be handled by a different Flask container.

---

# Important Docker Compose Commands

Validate configuration

```bash
docker compose config
```

Build and start

```bash
docker compose up --build
```

Scale Flask

```bash
docker compose up --build --scale flask=3
```

View running containers

```bash
docker compose ps
```

View logs

```bash
docker compose logs
```

Stop containers

```bash
docker compose down
```

---

# Problems Solved During The Project

## Redis Permission Error

Error:

```text
Permission denied
```

Cause:

The Redis configuration file permissions inside the image were incorrect.

Solution:

Adjusted the Redis Dockerfile and configuration so Redis could successfully read `redis.conf`.

---

## Health Check

A Redis health check was added.

```yaml
healthcheck:
  test: ["CMD", "redis-cli", "ping"]
```

This ensured Flask only started after Redis was healthy.

---

## Persistent Storage

A Docker volume was added to Redis.

Verified by restarting the application and confirming the counter value remained.

---

## Reverse Proxy

Added an Nginx container.

Browser traffic now flows through Nginx instead of directly to Flask.

---

## Load Balancing

Scaled Flask to three containers.

Displayed the hostname in the browser to verify that different Flask containers were serving requests.

---

# Key Concepts Learned

- Multi-container applications
- Docker Compose
- Docker networking
- Service discovery
- Reverse proxies
- Nginx
- Redis
- Docker volumes
- Environment variables
- Health checks
- Load balancing
- Scaling containers

---

# Interview Questions

### Why use Redis instead of storing the count in Flask?

Redis provides shared storage that all Flask containers can access.

---

### Why use Docker Compose?

To define and manage multiple containers using one configuration file.

---

### Why use Nginx?

To act as a reverse proxy and load balancer between users and Flask.

---

### Why use a Docker Volume?

To persist data after containers stop or restart.

---

### What is the difference between `ports` and `expose`?

`ports`

- publishes a container port to the host machine.

`expose`

- only makes the port available to other containers on the Docker network.

---

### Why use Environment Variables?

To avoid hard-coded configuration and make applications easier to configure across environments.

---

### What happens when Flask is scaled?

Docker creates multiple Flask containers.

Nginx distributes incoming requests across those containers, while all of them share the same Redis database.

---

# Project Outcome

Successfully built a production-style multi-container application using:

- Flask
- Redis
- Nginx
- Docker
- Docker Compose

Implemented:

- Persistent storage
- Environment variables
- Health checks
- Reverse proxy
- Scaling
- Load balancing

This project demonstrates many of the core Docker and Docker Compose concepts used by DevOps Engineers in real-world environments.

---

## Homepage

![Homepage](screenshots/01-homepage.png)

---

## Visit Counter

![Visit Counter](screenshots/02-visit-counter.png)

---

## Running Containers

![Docker Compose](screenshots/03-docker-compose-ps.png)

---

## Flask Scaling

The Flask service was horizontally scaled to **three running containers** using Docker Compose.

```bash
docker compose up --build --scale flask=3
```

This demonstrates how Docker Compose can run multiple instances of the same service.

![Flask Scaling](screenshots/04-flask-scaling.png)

---

## Load Balancing

Nginx acts as a **reverse proxy** and distributes incoming requests across the three Flask containers.

As the page is refreshed, different Flask containers handle each request, demonstrating that the application is successfully load balanced.

### Request 1

![Load Balancing 1](screenshots/05-load-balancing-1.png)

### Request 2

![Load Balancing 2](screenshots/05-load-balancing-2.png)

### Request 3

![Load Balancing 3](screenshots/05-load-balancing-3.png)

---

## Redis Persistence

Redis stores the visit counter using a Docker volume, allowing the data to persist even after stopping and restarting the application.

![Redis Persistence](screenshots/06-redis-persistence.png)
