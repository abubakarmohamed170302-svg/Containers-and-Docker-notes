# Multi-Container Flask, Redis and Nginx Project

This project was completed as part of the CoderCo Containers Challenge.

It demonstrates how Docker Compose can be used to build and manage a multi-container application containing:

- A Python Flask web application
- A Redis data store
- An Nginx reverse proxy
- Persistent Docker storage
- Health checks
- Environment-variable configuration
- Multiple scaled Flask containers

---

# Project Objective

The objective was to build a multi-container application in which:

- Flask provides the web interface
- Redis stores and increments a visit counter
- Nginx receives browser traffic
- Docker Compose manages all services
- Redis data persists after containers are recreated
- Flask can be scaled to multiple instances
- Nginx distributes requests between Flask instances

---

# Application Routes

The Flask application provides two routes.

## Homepage

```text
/
```

The homepage displays a welcome message confirming that the application is running.

## Visit Counter

```text
/count
```

Each request to this route:

1. Connects to Redis
2. Increments the shared counter
3. Retrieves the updated value
4. Displays the current visit count

The Flask container hostname was also displayed so that requests handled by different Flask instances could be identified during scaling tests.

---

# Final Architecture

```text
                    Browser
                       |
                       v
                Nginx Container
                Reverse Proxy
                       |
          +------------+------------+
          |            |            |
          v            v            v
      Flask 1       Flask 2       Flask 3
          |            |            |
          +------------+------------+
                       |
                       v
                Redis Container
                       |
                       v
              Persistent Volume
```

The request flow is:

```text
Browser
   |
   v
Nginx
   |
   v
Flask service
   |
   v
Redis
   |
   v
Docker volume
```

---

# Project Structure

```text
containers-challenge/
├── docker-compose.yml
├── flask-app/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── redis/
│   ├── Dockerfile
│   ├── redis.conf
│   └── data/
└── nginx/
    ├── Dockerfile
    └── nginx.conf
```

| File or directory | Purpose |
|---|---|
| `docker-compose.yml` | Defines and manages all application services |
| `flask-app/app.py` | Contains the Flask routes and Redis connection |
| `flask-app/Dockerfile` | Builds the Flask application image |
| `flask-app/requirements.txt` | Lists the Python dependencies |
| `redis/Dockerfile` | Builds the configured Redis image |
| `redis/redis.conf` | Configures Redis persistence and networking |
| `nginx/Dockerfile` | Builds the Nginx reverse-proxy image |
| `nginx/nginx.conf` | Routes requests to the Flask service |

---

# Flask Service

The Flask service contains the application logic.

Its responsibilities are:

- Providing the homepage
- Providing the `/count` route
- Connecting to Redis
- Incrementing the visit counter
- Displaying the responding container’s hostname

A simplified version of the application logic is:

```python
import os
import socket

from flask import Flask
from redis import Redis

app = Flask(__name__)

redis_client = Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", "6379")),
    decode_responses=True,
)


@app.route("/")
def home():
    return "Welcome to the multi-container application!"


@app.route("/count")
def count():
    visits = redis_client.incr("visits")
    hostname = socket.gethostname()

    return f"Visit count: {visits} | Served by: {hostname}"
```

Redis connection details are provided using environment variables instead of being hard-coded into the application.

---

# Flask Dockerfile

The Flask Dockerfile builds the web application image.

Example structure:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install \
    --no-cache-dir \
    -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

The key steps are:

1. Start from a Python base image
2. Set the working directory
3. Copy and install the dependencies
4. Copy the application code
5. Document port `5000`
6. Start the application with Gunicorn

---

# Python Dependencies

The Flask application requires packages such as:

```text
Flask
redis
gunicorn
```

These are listed in:

```text
requirements.txt
```

Using a requirements file provides consistent dependency installation during image builds.

---

# Redis Service

Redis is an in-memory key-value data store.

In this project, Redis stores the visit counter.

Using Redis instead of storing the counter inside Flask provides:

- Shared state between Flask containers
- Fast reads and writes
- Separation between application and data
- Counter persistence when configured with storage
- Support for scaling the Flask service

If the count were stored only in Flask memory, every Flask container would maintain a different value and the count would be lost when a container restarted.

---

# Redis Configuration

The custom Redis configuration includes settings similar to:

```conf
bind 0.0.0.0
port 6379
appendonly yes
appendfsync everysec
dir /data
```

| Setting | Purpose |
|---|---|
| `bind 0.0.0.0` | Allows Redis to accept connections through the container network |
| `port 6379` | Configures the Redis service port |
| `appendonly yes` | Enables append-only persistence |
| `appendfsync everysec` | Writes append-only updates regularly |
| `dir /data` | Stores Redis data in the mounted data directory |

Redis is only intended to be reachable through the internal Docker network in this project.

---

# Persistent Redis Storage

Containers are disposable, so data stored only in a container’s writable layer could be lost when that container is removed.

A named Docker volume is attached to Redis:

```yaml
volumes:
  - redis-data:/data
```

The volume is declared at the end of the Compose file:

```yaml
volumes:
  redis-data:
```

The storage relationship is:

```text
Redis writes data
       |
       v
/data inside container
       |
       v
redis-data Docker volume
```

The volume exists separately from the Redis container.

---

## Persistence Test

The counter was increased by visiting:

```text
/count
```

The application was then stopped and removed:

```bash
docker compose down
```

It was started again:

```bash
docker compose up -d
```

The counter continued from its previous value, demonstrating that the Redis volume preserved the data.

The volume would be deleted if the following command were used:

```bash
docker compose down -v
```

> The `-v` option removes the project’s named volumes and their locally stored data, so it should only be used when that data is no longer required.

---

# Environment Variables

The Flask service receives Redis connection information through environment variables:

```yaml
environment:
  REDIS_HOST: redis
  REDIS_PORT: 6379
```

The application reads these variables:

```python
redis_host = os.getenv("REDIS_HOST", "redis")
redis_port = int(os.getenv("REDIS_PORT", "6379"))
```

Benefits include:

- Avoiding hard-coded configuration
- Supporting different environments
- Making containers more portable
- Separating application code from runtime configuration

The value `redis` matches the Docker Compose service name.

---

# Docker Compose

Docker Compose defines and manages the complete application.

Instead of starting each container manually, the project can be started with:

```bash
docker compose up --build
```

Compose automatically:

- Builds the custom images
- Creates the containers
- Creates an internal network
- Connects the services
- Creates the Redis volume
- Starts services in dependency order
- Applies health-check configuration
- Publishes the Nginx port

---

# Docker Compose Services

A simplified representation of the Compose configuration is:

```yaml
services:
  flask:
    build:
      context: ./flask-app
    environment:
      REDIS_HOST: redis
      REDIS_PORT: 6379
    expose:
      - "5000"
    depends_on:
      redis:
        condition: service_healthy

  redis:
    build:
      context: ./redis
    volumes:
      - redis-data:/data
    expose:
      - "6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5

  nginx:
    build:
      context: ./nginx
    ports:
      - "5000:80"
    depends_on:
      - flask

volumes:
  redis-data:
```

The exact project configuration may contain additional options, but the main service relationships remain the same.

---

# Docker Networking

Docker Compose automatically creates an internal network for the project.

```text
Compose network
├── nginx
├── flask
└── redis
```

Containers communicate through their service names:

| Service | Internal hostname |
|---|---|
| Nginx | `nginx` |
| Flask | `flask` |
| Redis | `redis` |

Flask connects to Redis using:

```text
redis:6379
```

Nginx forwards requests to Flask using:

```text
flask:5000
```

No fixed container IP addresses are required.

Docker’s internal DNS resolves the service names to the correct containers.

---

# Nginx Reverse Proxy

Nginx sits between the user and the Flask containers.

```text
Browser
   |
   v
Nginx
   |
   v
Flask
```

Nginx provides:

- A single entry point
- Reverse proxying
- Separation between users and backend containers
- Request forwarding
- Support for load balancing
- A standard HTTP-facing service

Only Nginx needs to publish a port to the host.

Flask and Redis communicate internally through the Docker network.

---

# Port Exposure

The project uses `ports` and `expose` for different purposes.

## `ports`

Example:

```yaml
ports:
  - "5000:80"
```

This publishes a container port to the host.

In this example:

```text
Host port 5000
       |
       v
Nginx container port 80
```

The application can be opened at:

```text
http://localhost:5000
```

## `expose`

Example:

```yaml
expose:
  - "5000"
```

This documents the internal service port without publishing it directly to the host.

The service remains available to other containers on the Compose network.

| Configuration | Host access | Container-network access |
|---|---|---|
| `ports` | Yes | Yes |
| `expose` | No direct host publication | Yes |

---

# Redis Health Check

A health check verifies that Redis is responding:

```yaml
healthcheck:
  test: ["CMD", "redis-cli", "ping"]
  interval: 5s
  timeout: 3s
  retries: 5
```

The command:

```bash
redis-cli ping
```

should return:

```text
PONG
```

The Flask service can wait for Redis to become healthy:

```yaml
depends_on:
  redis:
    condition: service_healthy
```

This reduces connection errors caused by Flask starting before Redis is ready.

Application retry logic is still valuable because dependencies may become unavailable after startup.

---

# Scaling the Flask Service

Docker Compose can create multiple instances of the Flask service:

```bash
docker compose up -d --build --scale flask=3
```

This creates:

```text
1 Nginx container
3 Flask containers
1 Redis container
```

Check the services:

```bash
docker compose ps
```

The Flask service should not use a fixed `container_name`, because multiple replicas require unique container names.

Compose generates names similar to:

```text
containers-challenge-flask-1
containers-challenge-flask-2
containers-challenge-flask-3
```

---

# Load-Balancing Test

The Flask application displays its container hostname.

Refreshing the page can produce responses from different containers:

```text
Visit count: 10 | Served by: flask-1
Visit count: 11 | Served by: flask-2
Visit count: 12 | Served by: flask-3
```

This demonstrates that:

- Several Flask containers are running
- Requests are reaching different instances
- Every Flask instance uses the same Redis counter
- Application state is stored outside the Flask containers

---

# Testing the Application

## Validate the Compose Configuration

```bash
docker compose config
```

## Build and Start

```bash
docker compose up --build
```

## Start in the Background

```bash
docker compose up -d --build
```

## Check the Homepage

Open:

```text
http://localhost:5000
```

## Test the Counter

Open:

```text
http://localhost:5000/count
```

Refresh the page and confirm that the count increases.

## View Service Status

```bash
docker compose ps
```

## Follow Logs

```bash
docker compose logs -f
```

## Test Redis Health

```bash
docker compose exec redis redis-cli ping
```

Expected response:

```text
PONG
```

## Test Persistence

```bash
docker compose down
docker compose up -d
```

Open `/count` and confirm that the value continues from its previous number.

## Test Scaling

```bash
docker compose up -d --scale flask=3
```

Refresh the application and compare the responding hostnames.

---

# Problems Solved During the Project

## Redis Configuration Permission Error

The Redis container initially reported:

```text
Permission denied
```

### Cause

The Redis process could not read the custom configuration file because its permissions inside the image were incorrect.

### Solution

The Redis Dockerfile and file permissions were adjusted so that Redis could read:

```text
redis.conf
```

### Lesson

File ownership and permissions inside an image can affect whether a service starts successfully.

Container logs should be checked when a process exits.

---

## Redis Readiness

### Problem

Flask could attempt to connect before Redis was ready.

### Solution

A Redis health check was added:

```yaml
healthcheck:
  test: ["CMD", "redis-cli", "ping"]
```

The Flask dependency was configured to use the Redis health status.

### Lesson

Container startup and application readiness are different. A running container may not yet be ready to accept connections.

---

## Persistent Data

### Problem

The visit count needed to remain after the Redis container was removed and recreated.

### Solution

A named volume was mounted at:

```text
/data
```

### Lesson

Persistent data should be stored outside a disposable container’s writable layer.

---

## Reverse Proxy

### Problem

The Flask service was initially exposed directly.

### Solution

Nginx was added as the application’s external entry point.

### Lesson

A reverse proxy can receive incoming traffic and forward it to internal application services.

---

## Scaling

### Problem

The application needed to demonstrate more than one Flask instance.

### Solution

The service was scaled:

```bash
docker compose up -d --scale flask=3
```

### Lesson

Stateless application containers can be replicated when shared state is stored in an external service such as Redis.

---

## Load Balancing

### Problem

It was necessary to confirm that requests reached different Flask instances.

### Solution

The application displayed the container hostname with each response.

### Lesson

Including instance information during testing helps demonstrate request distribution.

---

# Useful Commands

## Validate the Compose file

```bash
docker compose config
```

## Build the images

```bash
docker compose build
```

## Build and start

```bash
docker compose up --build
```

## Start in detached mode

```bash
docker compose up -d
```

## Scale Flask

```bash
docker compose up -d --scale flask=3
```

## View services

```bash
docker compose ps
```

## View all logs

```bash
docker compose logs
```

## Follow logs

```bash
docker compose logs -f
```

## View Flask logs

```bash
docker compose logs flask
```

## View Redis logs

```bash
docker compose logs redis
```

## View Nginx logs

```bash
docker compose logs nginx
```

## Test Redis

```bash
docker compose exec redis redis-cli ping
```

## Stop and remove containers

```bash
docker compose down
```

---

# Key Concepts Demonstrated

- Multi-container applications
- Docker images
- Dockerfiles
- Docker Compose
- Compose services
- Docker networking
- Internal DNS
- Service discovery
- Environment variables
- Redis
- Persistent volumes
- Health checks
- Dependency readiness
- Nginx reverse proxying
- Port publishing
- Service exposure
- Horizontal scaling
- Load balancing
- Container logging
- Troubleshooting

---

# Common Interview Questions

## Why use Redis instead of storing the counter in Flask?

Redis provides shared storage that every Flask instance can access. If the value were stored only in Flask memory, each container would have its own counter and the data would be lost when the container stopped.

## Why use Docker Compose?

Docker Compose defines and manages all related services, networks, volumes and configuration in one YAML file.

## Why use Nginx?

Nginx provides a single entry point and forwards requests to the internal Flask service. It can also distribute requests when multiple Flask instances are running.

## Why use a Docker volume?

A volume stores Redis data separately from the container so that the data can remain when the container is replaced.

## What is the difference between `ports` and `expose`?

`ports` publishes a container port through the host. `expose` documents an internal port without directly publishing it to the host.

## Why use environment variables?

Environment variables separate runtime configuration from application code and make the container easier to use across different environments.

## Why use a health check?

A health check reports whether a service is responding correctly rather than only whether its container process has started.

## What happens when Flask is scaled?

Docker Compose creates multiple Flask containers from the same image. Nginx distributes incoming requests, while every Flask instance uses the shared Redis data store.

## Why should Flask remain stateless?

A stateless Flask container can be replaced or scaled without losing shared application data. Persistent or shared state is stored in Redis instead.

## How do the containers find one another?

Docker Compose connects the services to a shared network and provides internal DNS. Services use names such as `flask` and `redis` instead of fixed IP addresses.

---

# Project Outcome

The project successfully demonstrated a production-style multi-container architecture for learning purposes using:

- Python Flask
- Redis
- Nginx
- Docker
- Docker Compose

The completed application included:

- Two Flask routes
- A Redis-backed visit counter
- Persistent Redis storage
- Environment-variable configuration
- Service-name networking
- A Redis health check
- An Nginx reverse proxy
- Three scaled Flask instances
- Request distribution
- Container troubleshooting

This project strengthened my understanding of how separate containerised services communicate and work together as one application.
