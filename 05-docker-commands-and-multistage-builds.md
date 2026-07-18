# Docker Commands and Multi-Stage Builds

Once the fundamentals of Docker are understood, the next step is learning how to:

- Manage images and containers
- Inspect and debug containers
- Manage networks and volumes
- Remove unused resources
- Reduce image sizes
- Use Docker’s build cache
- Create multi-stage builds

These skills are important because an unmanaged Docker environment can waste storage, slow deployments and make troubleshooting more difficult.

---

# Docker System Commands

## Check the Docker Version

```bash
docker --version
```

This confirms that the Docker client is installed.

---

## View Docker System Information

```bash
docker info
```

This displays information about:

- Docker Engine
- Running and stopped containers
- Images
- Storage driver
- Available runtimes
- Networks
- Plugins
- Docker’s root directory

This is useful when checking whether Docker is running correctly.

---

## View Docker Disk Usage

```bash
docker system df
```

This shows the space used by:

- Images
- Containers
- Local volumes
- Build cache

Show a more detailed breakdown:

```bash
docker system df -v
```

---

# Docker Image Commands

## Pull an Image

```bash
docker pull nginx
```

This downloads the default Nginx image tag from a registry.

Use an explicit version for greater predictability:

```bash
docker pull nginx:1.27
```

If no tag is provided, Docker normally uses:

```text
latest
```

---

## List Images

```bash
docker images
```

The modern equivalent is:

```bash
docker image ls
```

Example output:

```text
REPOSITORY    TAG       IMAGE ID       CREATED       SIZE
hello-flask   1.0.0     abc123def456   2 hours ago   150MB
mysql         8         def456abc123   5 days ago    600MB
```

| Column | Meaning |
|---|---|
| Repository | Image name |
| Tag | Image version |
| Image ID | Image identifier |
| Created | Image age |
| Size | Approximate image size |

---

## Build an Image

```bash
docker build -t hello-flask .
```

| Part | Meaning |
|---|---|
| `docker build` | Builds an image |
| `-t` | Assigns a name and optional tag |
| `hello-flask` | Image name |
| `.` | Uses the current directory as the build context |

---

## Build a Versioned Image

```bash
docker build -t hello-flask:1.0.0 .
```

A later release could use:

```bash
docker build -t hello-flask:1.1.0 .
```

Versioned tags help identify specific releases.

---

## Tag an Existing Image

```bash
docker tag hello-flask:1.0.0 username/hello-flask:1.0.0
```

For Amazon ECR:

```bash
docker tag hello-flask:1.0.0 \
  AWS_ACCOUNT_ID.dkr.ecr.AWS_REGION.amazonaws.com/hello-flask:1.0.0
```

Tagging does not create another complete copy of the image. It creates another reference to the same image ID.

---

## Push an Image

Push to Docker Hub:

```bash
docker push username/hello-flask:1.0.0
```

Push to Amazon ECR:

```bash
docker push \
  AWS_ACCOUNT_ID.dkr.ecr.AWS_REGION.amazonaws.com/hello-flask:1.0.0
```

Authentication must be completed before pushing to a private registry.

---

## View Image History

```bash
docker history hello-flask:1.0.0
```

This shows the image layers and their approximate sizes.

It can help identify which Dockerfile instruction added a large amount of data.

---

## Inspect an Image

```bash
docker inspect hello-flask:1.0.0
```

This displays JSON metadata such as:

- Architecture
- Environment variables
- Exposed ports
- Entrypoint
- Default command
- Filesystem layers

---

## Remove an Image

```bash
docker rmi hello-flask:1.0.0
```

The equivalent command is:

```bash
docker image rm hello-flask:1.0.0
```

Docker may refuse to remove an image if a container still references it.

Check:

```bash
docker ps -a
```

Remove the unused container before removing the image.

---

# Docker Container Commands

## Run a Container

```bash
docker run hello-flask:1.0.0
```

This:

1. Creates a new container
2. Adds a writable container layer
3. Starts the configured process
4. Attaches the terminal to its output

---

## Run With Port Mapping

```bash
docker run -p 5000:5000 hello-flask:1.0.0
```

The format is:

```text
HOST_PORT:CONTAINER_PORT
```

The example forwards requests from host port `5000` to port `5000` inside the container.

---

## Run in Detached Mode

```bash
docker run -d -p 5000:5000 hello-flask:1.0.0
```

The `-d` option runs the container in the background.

---

## Assign a Container Name

```bash
docker run -d \
  --name flask-app \
  -p 5000:5000 \
  hello-flask:1.0.0
```

A readable name is easier to use than a long container ID.

---

## Automatically Remove a Temporary Container

```bash
docker run --rm hello-flask:1.0.0
```

The `--rm` option removes the container automatically when its process stops.

This is useful for short tests.

---

## Pass Environment Variables

```bash
docker run \
  -e APP_ENV=development \
  -e DB_HOST=mydb \
  hello-flask:1.0.0
```

Environment variables commonly provide:

- Application mode
- Database hostname
- API address
- Logging level
- Feature configuration

Do not place real passwords or secret tokens in public commands, screenshots or repositories.

---

## List Running Containers

```bash
docker ps
```

The equivalent command is:

```bash
docker container ls
```

This only shows running containers.

---

## List All Containers

```bash
docker ps -a
```

The equivalent command is:

```bash
docker container ls -a
```

This includes:

- Running containers
- Stopped containers
- Exited containers
- Failed containers

---

## View Container Logs

```bash
docker logs flask-app
```

Follow logs continuously:

```bash
docker logs -f flask-app
```

Show the latest 50 lines:

```bash
docker logs --tail 50 flask-app
```

Logs can reveal:

- Application errors
- Database connection failures
- Missing environment variables
- Dependency problems
- Incorrect startup commands

---

## Run a Command Inside a Container

Open Bash inside a running container:

```bash
docker exec -it flask-app bash
```

Some lightweight images do not contain Bash. Use `sh` instead:

```bash
docker exec -it flask-app sh
```

| Option | Meaning |
|---|---|
| `exec` | Runs a command inside an existing container |
| `-i` | Keeps standard input open |
| `-t` | Creates a terminal |
| `bash` or `sh` | Shell to run |

Run one command without opening a shell:

```bash
docker exec flask-app env
```

---

## Inspect a Container

```bash
docker inspect flask-app
```

This displays information about:

- Container state
- Environment variables
- Networks
- IP addresses
- Mounts
- Port mappings
- Startup configuration

Display the container’s network IP addresses:

```bash
docker inspect \
  --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' \
  flask-app
```

---

## View Container Processes

```bash
docker top flask-app
```

This displays the processes running inside the container.

---

## View Container Resource Usage

```bash
docker stats
```

This displays live information about:

- CPU usage
- Memory usage
- Network traffic
- Block input and output
- Process count

Stop the display with:

```text
Ctrl+C
```

---

## Stop a Container

```bash
docker stop flask-app
```

Docker first asks the container’s main process to stop gracefully.

---

## Start a Stopped Container

```bash
docker start flask-app
```

This restarts the same container. It does not create a new one.

---

## Restart a Container

```bash
docker restart flask-app
```

---

## Remove a Container

Stop and remove it:

```bash
docker stop flask-app
docker rm flask-app
```

Force-removing a running container is also possible:

```bash
docker rm -f flask-app
```

Force removal immediately stops and removes the container, so it should be used carefully.

---

# Docker Network Commands

## List Networks

```bash
docker network ls
```

Default networks commonly include:

```text
bridge
host
none
```

Docker Compose also creates project-specific networks.

---

## Create a Network

```bash
docker network create app-network
```

Start a database container on the network:

```bash
docker run -d \
  --name mydb \
  --network app-network \
  -e MYSQL_ROOT_PASSWORD=localpassword \
  mysql:8
```

Start the web container on the same network:

```bash
docker run -d \
  --name web \
  --network app-network \
  -p 5000:5000 \
  hello-flask:1.0.0
```

The web container can use:

```text
mydb
```

as the database hostname.

---

## Connect an Existing Container to a Network

```bash
docker network connect app-network flask-app
```

---

## Disconnect a Container

```bash
docker network disconnect app-network flask-app
```

---

## Inspect a Network

```bash
docker network inspect app-network
```

This displays the connected containers and network configuration.

---

## Remove a Network

```bash
docker network rm app-network
```

Docker will not normally remove a network while active containers are connected to it.

---

# Docker Volume Commands

## List Volumes

```bash
docker volume ls
```

Volumes store persistent container data outside a container’s writable layer.

---

## Create a Volume

```bash
docker volume create mysql-data
```

Use the volume with MySQL:

```bash
docker run -d \
  --name mydb \
  -e MYSQL_ROOT_PASSWORD=localpassword \
  -v mysql-data:/var/lib/mysql \
  mysql:8
```

The format is:

```text
VOLUME_NAME:CONTAINER_PATH
```

The database data can remain after the container is removed.

---

## Inspect a Volume

```bash
docker volume inspect mysql-data
```

---

## Remove a Volume

```bash
docker volume rm mysql-data
```

> Removing a database volume can permanently delete the data stored in it. Confirm the exact volume and whether its data is still needed before removing it.

---

# Docker Cleanup Commands

Docker can accumulate stopped containers, unused images, unused networks and build cache.

Always inspect the environment before running cleanup commands.

---

## Remove Stopped Containers

```bash
docker container prune
```

This removes all stopped containers after confirmation.

---

## Remove Dangling Images

```bash
docker image prune
```

Dangling images are untagged layers that are no longer referenced by a named image.

Remove all images not used by any container:

```bash
docker image prune -a
```

The `-a` option is more aggressive and should be used carefully.

---

## Remove Unused Networks

```bash
docker network prune
```

---

## Remove Unused Volumes

```bash
docker volume prune
```

Unused volumes may still contain important application or database data.

Inspect them before removal:

```bash
docker volume ls
docker volume inspect VOLUME_NAME
```

---

## Remove Build Cache

```bash
docker builder prune
```

Remove all unused build cache:

```bash
docker builder prune -a
```

---

## General Cleanup

```bash
docker system prune
```

This normally removes:

- Stopped containers
- Unused networks
- Dangling images
- Unused build cache

More aggressive cleanup:

```bash
docker system prune -a
```

This can also remove unused tagged images.

Volumes are not included unless the volume option is explicitly supplied. Cleanup commands can cause meaningful data loss, so their targets and prompts should be reviewed carefully.

---

# Docker Compose Command Reference

## Start services

```bash
docker compose up
```

## Build and start services

```bash
docker compose up --build
```

## Start in detached mode

```bash
docker compose up -d
```

## Build and start in detached mode

```bash
docker compose up -d --build
```

## View services

```bash
docker compose ps
```

## View logs

```bash
docker compose logs
```

## Follow logs

```bash
docker compose logs -f
```

## Run a command inside a service

```bash
docker compose exec web sh
```

## Stop services

```bash
docker compose stop
```

## Restart services

```bash
docker compose restart
```

## Stop and remove services

```bash
docker compose down
```

## Validate the Compose file

```bash
docker compose config
```

---

# Making Docker Images Smaller

Large Docker images can cause:

- Slower downloads
- Slower deployments
- More registry storage usage
- More local disk usage
- Longer CI/CD pipelines
- A larger potential attack surface

A good runtime image should contain:

> Only the files, dependencies and system libraries required to run the application.

---

## Use a Suitable Base Image

A general Python image:

```dockerfile
FROM python:3.12
```

A smaller variant:

```dockerfile
FROM python:3.12-slim
```

An Alpine-based variant:

```dockerfile
FROM python:3.12-alpine
```

Alpine images can be smaller, but they use different system libraries and may make some Python dependencies more difficult to build.

For many Python applications, a `slim` image provides a useful balance between size and compatibility.

Always select a specific and supported version suitable for the application.

---

# Use `.dockerignore`

A `.dockerignore` file prevents unnecessary files from entering the Docker build context.

Example:

```dockerignore
venv/
__pycache__/
*.pyc
.git/
.gitignore
.env
*.log
.pytest_cache/
.coverage
```

Without `.dockerignore`, the following instruction may copy unwanted files:

```dockerfile
COPY . .
```

Potentially unwanted files include:

- Virtual environments
- Git history
- Python cache files
- Logs
- Local test output
- Secret environment files

Benefits of `.dockerignore` include:

- Smaller build context
- Faster builds
- Better cache performance
- Reduced risk of copying secrets
- Cleaner images

---

# `.dockerignore` Versus `.gitignore`

| File | Purpose |
|---|---|
| `.dockerignore` | Controls which files Docker receives during a build |
| `.gitignore` | Controls which files Git tracks |

Example `.gitignore`:

```gitignore
venv/
__pycache__/
*.pyc
.env
```

Example `.dockerignore`:

```dockerignore
venv/
__pycache__/
*.pyc
.git/
.env
*.log
```

Both files can be used in the same project.

---

# Install Dependencies From a Requirements File

Instead of installing packages directly by name:

```dockerfile
RUN pip install flask mysqlclient
```

Create `requirements.txt`:

```text
Flask==3.1.1
mysqlclient==2.2.7
```

Install the dependencies with:

```dockerfile
RUN pip install \
    --no-cache-dir \
    -r requirements.txt
```

The `--no-cache-dir` option prevents pip from keeping downloaded package archives in the image.

---

# Use Docker Layer Caching

Each Dockerfile instruction creates or contributes to an image layer.

A cache-friendly Dockerfile copies the dependency file before the frequently changing application code:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install \
    --no-cache-dir \
    -r requirements.txt

COPY . .

CMD ["python", "app.py"]
```

If the application code changes but `requirements.txt` does not, Docker can reuse the dependency installation layer.

This makes later builds faster.

A less efficient order would be:

```dockerfile
COPY . .

RUN pip install --no-cache-dir -r requirements.txt
```

Any application file change could invalidate the dependency layer.

---

# Combine Package-Manager Commands

Less efficient:

```dockerfile
RUN apt-get update
RUN apt-get install -y gcc
RUN apt-get install -y default-libmysqlclient-dev
```

Better:

```dockerfile
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       gcc \
       default-libmysqlclient-dev \
       pkg-config \
    && rm -rf /var/lib/apt/lists/*
```

This:

- Avoids outdated package-list layers
- Prevents unnecessary recommended packages
- Removes cached package lists
- Keeps the Dockerfile more predictable

---

# Remove Build Tools From Runtime Images

Some dependencies require compilers or development headers during installation.

Examples include:

```text
gcc
build-essential
pkg-config
development headers
```

These tools may not be needed when the application is running.

Leaving unnecessary build tools in the final image can:

- Increase image size
- Add unnecessary packages
- Increase maintenance work
- Increase the potential attack surface

Multi-stage builds solve this by separating the build environment from the runtime environment.

---

# Multi-Stage Docker Builds

A multi-stage build uses more than one `FROM` instruction in one Dockerfile.

Each `FROM` begins a new build stage.

```dockerfile
FROM python:3.12-slim AS builder

# Build dependencies and application artifacts


FROM python:3.12-slim AS runtime

# Copy only the required output
```

A useful analogy is:

```text
Builder stage = Workshop
Runtime stage = Finished product
```

The tools used in the workshop do not need to be included with the finished product.

---

## Benefits of Multi-Stage Builds

Multi-stage builds can:

- Reduce final image size
- Exclude compilers and development tools
- Separate build and runtime responsibilities
- Produce cleaner images
- Reduce unnecessary packages
- Improve maintainability
- Improve security

---

# Simple Python Multi-Stage Build

```dockerfile
FROM python:3.12-slim AS builder

WORKDIR /build

COPY requirements.txt .

RUN pip install \
    --no-cache-dir \
    --prefix=/install \
    -r requirements.txt


FROM python:3.12-slim AS runtime

WORKDIR /app

COPY --from=builder /install /usr/local

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]
```

---

## Builder Stage

```dockerfile
FROM python:3.12-slim AS builder
```

This starts the first stage and names it:

```text
builder
```

The builder stage prepares the application dependencies.

---

## Install Into a Separate Directory

```dockerfile
RUN pip install \
    --no-cache-dir \
    --prefix=/install \
    -r requirements.txt
```

This installs the Python packages under:

```text
/install
```

The directory can then be copied into the runtime stage.

---

## Runtime Stage

```dockerfile
FROM python:3.12-slim AS runtime
```

This starts a fresh stage.

Files from the builder stage are not included automatically.

Only explicitly copied files become part of the final image.

---

## Copy From the Builder Stage

```dockerfile
COPY --from=builder /install /usr/local
```

The syntax is:

```text
COPY --from=STAGE_NAME SOURCE DESTINATION
```

This copies the installed Python dependencies into the final image.

---

## Copy the Application

```dockerfile
COPY app.py .
```

Only the application file is copied.

Temporary build files remain in the builder stage and are not included in the final runtime image.

---

# Multi-Stage Build With `mysqlclient`

The Python `mysqlclient` package may require compilation tools and MySQL development headers.

```dockerfile
FROM python:3.12-slim AS builder

WORKDIR /build

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       gcc \
       default-libmysqlclient-dev \
       pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install \
    --no-cache-dir \
    --prefix=/install \
    -r requirements.txt


FROM python:3.12-slim AS runtime

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /install /usr/local

COPY . .

EXPOSE 5002

CMD ["python", "app.py"]
```

The builder stage contains:

```text
Compiler
Development headers
Package configuration tools
Built Python dependencies
```

The runtime stage contains:

```text
Python runtime
Required MySQL runtime libraries
Installed Python packages
Application files
```

The final image does not contain the compiler from the builder stage.

The exact runtime library required depends on the package and base image. If the application reports a missing shared library, identify and install the required runtime package in the final stage.

---

# Building a Multi-Stage Image

Build the final image:

```bash
docker build -t hello-flask-multistage:1.0.0 .
```

View it:

```bash
docker images hello-flask-multistage
```

Compare image sizes:

```bash
docker images hello-flask
docker images hello-flask-multistage
```

The size difference depends on:

- Base images
- Project files
- Python packages
- Build dependencies
- Runtime libraries

---

## Build a Specific Stage

Build only the builder stage:

```bash
docker build \
  --target builder \
  -t hello-flask-builder .
```

This is useful when debugging a build stage.

Build the runtime stage explicitly:

```bash
docker build \
  --target runtime \
  -t hello-flask-runtime .
```

---

# Multi-Stage Build Mental Model

```text
Stage 1: Builder
├── Compilers
├── Development headers
├── Build tools
├── Source files
└── Built dependencies
             |
             | Copy required output only
             v
Stage 2: Runtime
├── Application
├── Runtime libraries
└── Required dependencies
```

The final image does not need to include everything from the builder.

---

# Common Multi-Stage Build Mistakes

## Incorrect Stage Name

Dockerfile:

```dockerfile
FROM python:3.12-slim AS builder
```

Incorrect:

```dockerfile
COPY --from=build /install /usr/local
```

Correct:

```dockerfile
COPY --from=builder /install /usr/local
```

Stage names must match exactly.

---

## Missing Runtime Libraries

A dependency may compile successfully in the builder stage but fail in the runtime stage.

Example:

```text
error while loading shared libraries
```

This normally means that a required runtime library is missing.

Build packages and runtime packages are not always the same.

---

## Copying Everything From the Builder

Avoid:

```dockerfile
COPY --from=builder / /
```

This can copy unnecessary files and remove the benefits of using separate stages.

Copy only the required build output.

---

## Forgetting `.dockerignore`

Multi-stage builds do not automatically reduce the build context.

A `.dockerignore` file is still needed to prevent unnecessary files from being sent to Docker.

---

## Using Different Incompatible Base Images

The builder and runtime stages should use compatible operating-system environments unless the output is completely portable.

A dependency compiled against one system library may fail when copied into an incompatible runtime image.

---

# Debugging Docker Builds

## Display Detailed Build Output

```bash
docker build \
  --progress=plain \
  -t hello-flask .
```

This displays detailed logs for each build step.

---

## Build Without Cache

```bash
docker build \
  --no-cache \
  -t hello-flask .
```

This forces every Dockerfile step to run again.

It is useful when debugging stale layers, but normal cached builds are much faster.

---

## Build One Stage

```bash
docker build \
  --target builder \
  -t debug-builder .
```

This helps isolate an error to a particular stage.

---

## Inspect Layer Sizes

```bash
docker history hello-flask
```

Look for unusually large layers.

---

## Inspect Image Configuration

```bash
docker inspect hello-flask
```

Check:

- Environment variables
- Entrypoint
- Default command
- Exposed ports
- Architecture

---

## Test the Final Image

```bash
docker run --rm -p 5000:5000 hello-flask
```

View the logs if it fails:

```bash
docker logs CONTAINER_NAME
```

---

# Recommended Simple Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install \
    --no-cache-dir \
    -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]
```

This is suitable for a simple Flask application without build-heavy dependencies.

---

# Recommended Project Files

```text
hello_flask/
├── app.py
├── Dockerfile
├── requirements.txt
├── compose.yaml
├── .dockerignore
├── .gitignore
└── README.md
```

Example `.dockerignore`:

```dockerignore
venv/
__pycache__/
*.pyc
.git/
.env
*.log
```

Example `.gitignore`:

```gitignore
venv/
__pycache__/
*.pyc
.env
```

---

# Command Summary

## Images

```bash
docker pull IMAGE:TAG
docker image ls
docker build -t IMAGE:TAG .
docker tag SOURCE_IMAGE:TAG TARGET_IMAGE:TAG
docker push IMAGE:TAG
docker history IMAGE:TAG
docker inspect IMAGE:TAG
docker rmi IMAGE:TAG
```

## Containers

```bash
docker run IMAGE:TAG
docker run --rm IMAGE:TAG
docker run -d IMAGE:TAG
docker ps
docker ps -a
docker logs CONTAINER
docker logs -f CONTAINER
docker exec -it CONTAINER sh
docker inspect CONTAINER
docker top CONTAINER
docker stats
docker stop CONTAINER
docker start CONTAINER
docker restart CONTAINER
docker rm CONTAINER
```

## Networks

```bash
docker network ls
docker network create NETWORK
docker network connect NETWORK CONTAINER
docker network disconnect NETWORK CONTAINER
docker network inspect NETWORK
docker network rm NETWORK
```

## Volumes

```bash
docker volume ls
docker volume create VOLUME
docker volume inspect VOLUME
docker volume rm VOLUME
```

## Cleanup

```bash
docker system df
docker container prune
docker image prune
docker network prune
docker volume prune
docker builder prune
docker system prune
```

## Docker Compose

```bash
docker compose config
docker compose build
docker compose up
docker compose up --build
docker compose up -d
docker compose ps
docker compose logs
docker compose logs -f
docker compose exec SERVICE sh
docker compose stop
docker compose restart
docker compose down
```

---

# Common Interview Questions

## What is the difference between `docker start` and `docker run`?

`docker start` starts an existing stopped container. `docker run` creates a new container from an image and starts it.

## What does `docker exec` do?

It runs an additional command inside an existing running container.

## Why use `.dockerignore`?

It prevents unnecessary or sensitive files from entering the build context, improving build performance and reducing accidental inclusion in images.

## Why copy `requirements.txt` before the application code?

It allows Docker to reuse the cached dependency layer when application files change but the dependencies remain the same.

## What is a multi-stage build?

A multi-stage build uses multiple `FROM` instructions. Earlier stages build or prepare artifacts, while the final stage contains only what is required at runtime.

## Why are multi-stage builds useful?

They can reduce image size, remove compilers and development tools and create cleaner runtime images.

## What does `COPY --from=builder` do?

It copies selected files from a named build stage into the current stage.

## What is the difference between an image and a container?

An image is a read-only blueprint. A container is a running or stopped instance created from an image.

---

# Summary

- `docker image ls` displays local images.
- `docker ps` displays running containers.
- `docker ps -a` displays all containers.
- `docker logs` helps investigate application errors.
- `docker exec` runs commands inside a running container.
- `docker inspect` displays detailed Docker metadata.
- Docker networks allow containers to communicate.
- Docker volumes store persistent data.
- Cleanup commands remove unused resources and must be used carefully.
- Smaller images are faster to store, transfer and deploy.
- `.dockerignore` prevents unnecessary files from entering the build context.
- Docker layer caching makes repeated builds faster.
- Dependencies should be installed before frequently changing application code is copied.
- Multi-stage builds separate build tools from runtime requirements.
- `COPY --from` transfers selected output between build stages.
- The final image should contain only what the application requires at runtime.
