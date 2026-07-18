# Docker Compose

Docker Compose is a tool used to define and run applications that require multiple Docker containers.

A real application may contain several separate services:

```text
Web application
      +
Database
      +
Cache
      +
Reverse proxy
```

Without Docker Compose, every container, network and volume would need to be created using separate Docker commands.

With Docker Compose, the complete application is described in one YAML file and started with one command:

```bash
docker compose up
```

Docker Compose can be thought of as a manager that creates, connects and runs all the containers required by an application.

---

## Docker Versus Docker Compose

Docker is used to build images and run individual containers.

Docker Compose is used to manage a group of related containers.

### Without Docker Compose

A network must be created manually:

```bash
docker network create app-network
```

A MySQL container could then be started with:

```bash
docker run -d \
  --name mydb \
  --network app-network \
  -e MYSQL_ROOT_PASSWORD=password \
  -e MYSQL_DATABASE=mydatabase \
  mysql:8
```

The Flask container would be started separately:

```bash
docker run -d \
  --name web \
  --network app-network \
  -p 5002:5002 \
  hello-flask-mysql
```

This involves several commands that must be remembered and repeated correctly.

### With Docker Compose

The services, networks, volumes, ports and configuration are written inside a Compose file.

The whole application can then be started with:

```bash
docker compose up
```

Compose can automatically:

- Build custom images
- Download existing images
- Create containers
- Create a shared network
- Connect services
- Create named volumes
- Publish ports
- Pass environment variables
- Display service logs

---

# Why Docker Compose Is Important in DevOps

DevOps engineers regularly work with applications made from several services.

For example:

```text
Frontend
Backend API
Database
Redis cache
Nginx reverse proxy
Monitoring service
```

Each service can run inside its own container.

Docker Compose allows the environment to be described as configuration and stored alongside the application code.

This configuration can be:

- Stored in Git
- Reviewed by a team
- Recreated on another machine
- Used by different developers
- Updated when the application changes
- Used in development and testing environments

This follows an important DevOps principle:

> Define the required environment as code instead of creating it manually.

---

## Consistent Environments

Without Compose, different developers might use different commands and settings:

```text
Developer A uses port 5000
Developer B uses port 5002
Developer C forgets to create the network
```

With Compose, everyone uses the same configuration:

```bash
docker compose up
```

This makes the environment more consistent and repeatable.

---

# The Compose File

A Compose file is written in YAML.

Common filenames include:

```text
compose.yaml
compose.yml
docker-compose.yaml
docker-compose.yml
```

Modern Docker documentation commonly uses:

```text
compose.yaml
```

The course project can continue using:

```text
docker-compose.yml
```

Modern Docker Compose does not require a top-level version field.

An older file might begin with:

```yaml
version: "3.8"
```

This line can now produce an obsolete-version warning. A modern Compose file can begin directly with:

```yaml
services:
```

---

# Understanding YAML

YAML is a human-readable configuration format.

It uses indentation to represent structure:

```yaml
services:
  web:
    build: .
```

In this example:

```text
web belongs to services
build belongs to web
```

Important YAML rules include:

- Use spaces for indentation
- Do not use tabs
- Keep indentation consistent
- Include a space after each colon
- Use a hyphen for list items
- Quote port mappings to prevent YAML interpretation issues

Incorrect indentation can prevent Docker Compose from reading the file.

Validate a Compose file with:

```bash
docker compose config
```

---

# First Docker Compose Application

The following example defines a Flask web application and a MySQL database:

```yaml
services:
  web:
    build: .
    ports:
      - "5002:5002"
    environment:
      DATABASE_HOST: mydb
      DATABASE_NAME: mydatabase
      DATABASE_USER: root
      DATABASE_PASSWORD: password
    depends_on:
      - mydb

  mydb:
    image: mysql:8
    environment:
      MYSQL_ROOT_PASSWORD: password
      MYSQL_DATABASE: mydatabase
    volumes:
      - mysql-data:/var/lib/mysql

volumes:
  mysql-data:
```

This application contains two services:

| Service | Purpose |
|---|---|
| `web` | Runs the Flask application |
| `mydb` | Runs the MySQL database |

Each service becomes a container when the Compose application starts.

---

# Understanding `services`

The `services` section defines the different parts of the application:

```yaml
services:
  web:
  mydb:
```

The service names are important because Compose provides DNS resolution on the application’s default network.

The web container can connect to the database using:

```text
mydb
```

as the hostname.

Docker resolves `mydb` to the database container’s IP address.

---

# Understanding `build`

```yaml
web:
  build: .
```

This tells Docker Compose to build the image for the `web` service.

The dot means:

```text
Use the current directory as the build context.
```

Compose looks for a file named:

```text
Dockerfile
```

inside that directory.

A more detailed build configuration could be:

```yaml
web:
  build:
    context: .
    dockerfile: Dockerfile
```

This explicitly defines the build context and Dockerfile location.

---

# Understanding `image`

```yaml
mydb:
  image: mysql:8
```

This tells Compose to use the official MySQL 8 image.

If the image does not exist locally, Docker downloads it from the configured container registry.

The difference is:

| Setting | Purpose |
|---|---|
| `build:` | Builds a custom image from a Dockerfile |
| `image:` | Uses an image with the specified name and tag |

A service can sometimes use both:

```yaml
web:
  build: .
  image: hello-flask:1.0
```

Compose builds the image and tags it as `hello-flask:1.0`.

---

# Understanding `ports`

```yaml
ports:
  - "5002:5002"
```

This publishes a container port through the host.

The format is:

```text
HOST_PORT:CONTAINER_PORT
```

In this example:

```text
Host port 5002
       |
       v
Container port 5002
       |
       v
Flask application
```

The application can be opened at:

```text
http://127.0.0.1:5002
```

The Flask application must listen on port `5002` inside the container:

```python
app.run(host="0.0.0.0", port=5002)
```

The host and container ports can be different:

```yaml
ports:
  - "8080:5002"
```

The application would then be opened at:

```text
http://127.0.0.1:8080
```

---

# Understanding Environment Variables

Environment variables provide configuration to containers.

```yaml
environment:
  MYSQL_ROOT_PASSWORD: password
  MYSQL_DATABASE: mydatabase
```

In the MySQL image:

- `MYSQL_ROOT_PASSWORD` sets the root password
- `MYSQL_DATABASE` creates a database during initial setup

The web service can also receive connection settings:

```yaml
environment:
  DATABASE_HOST: mydb
  DATABASE_NAME: mydatabase
  DATABASE_USER: root
  DATABASE_PASSWORD: password
```

The Python application can read them using:

```python
import os

database_host = os.getenv("DATABASE_HOST", "mydb")
database_name = os.getenv("DATABASE_NAME", "mydatabase")
database_user = os.getenv("DATABASE_USER", "root")
database_password = os.getenv("DATABASE_PASSWORD")
```

Passwords should not be committed directly to public repositories.

For local development, values can be placed in an untracked `.env` file:

```env
MYSQL_ROOT_PASSWORD=replace_with_local_password
MYSQL_DATABASE=mydatabase
```

The Compose file can reference them:

```yaml
environment:
  MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
  MYSQL_DATABASE: ${MYSQL_DATABASE}
```

Add `.env` to `.gitignore`:

```gitignore
.env
```

A `.env.example` file containing placeholder values can be committed to show which variables are required.

---

# Understanding `depends_on`

```yaml
depends_on:
  - mydb
```

This tells Compose to start the `mydb` container before the `web` container.

However, basic `depends_on` does not guarantee that MySQL is ready to accept connections.

The container may be running while the database is still initialising. This can result in:

```text
Connection refused
```

A health check can be used to verify readiness:

```yaml
services:
  web:
    build: .
    depends_on:
      mydb:
        condition: service_healthy

  mydb:
    image: mysql:8
    environment:
      MYSQL_ROOT_PASSWORD: password
      MYSQL_DATABASE: mydatabase
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-ppassword"]
      interval: 10s
      timeout: 5s
      retries: 5
```

Applications should also use retry logic because services can become temporarily unavailable after startup.

---

# Understanding Volumes

Containers are disposable. Data stored only inside a container can be lost when the container is removed.

A named volume stores database data separately:

```yaml
services:
  mydb:
    image: mysql:8
    volumes:
      - mysql-data:/var/lib/mysql

volumes:
  mysql-data:
```

The mapping means:

```text
Named volume: mysql-data
       |
       v
MySQL data directory: /var/lib/mysql
```

The volume remains available after:

```bash
docker compose down
```

To deliberately remove the Compose volumes, use:

```bash
docker compose down -v
```

> Removing database volumes deletes the stored local database data. Use this option carefully.

---

# Example Project Structure

```text
hello_flask/
├── app.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .dockerignore
├── .gitignore
└── .env.example
```

---

# Example Flask Application

```python
import os

import MySQLdb
from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    connection = MySQLdb.connect(
        host=os.getenv("DATABASE_HOST", "mydb"),
        user=os.getenv("DATABASE_USER", "root"),
        password=os.getenv("DATABASE_PASSWORD"),
        database=os.getenv("DATABASE_NAME", "mydatabase"),
    )

    cursor = connection.cursor()
    cursor.execute("SELECT 'Hello from MySQL!'")
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result[0]


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
```

The important hostname is:

```python
host=os.getenv("DATABASE_HOST", "mydb")
```

The default value `mydb` matches the Compose service:

```yaml
services:
  mydb:
```

---

# Example Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       gcc \
       default-libmysqlclient-dev \
       pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5002

CMD ["python", "app.py"]
```

---

# Example `requirements.txt`

```text
Flask==3.1.1
mysqlclient==2.2.7
```

Using `requirements.txt` keeps Python dependencies separate from the Dockerfile and makes them easier to manage.

---

# Starting the Compose Application

Run the following command from the directory containing the Compose file:

```bash
docker compose up
```

This starts the services and attaches the terminal to their logs.

---

## Build Before Starting

If the Dockerfile or dependencies changed, use:

```bash
docker compose up --build
```

The `--build` option rebuilds the required images before starting the containers.

---

## Run in Detached Mode

```bash
docker compose up -d
```

Detached mode runs the containers in the background and returns control of the terminal.

Build and run in detached mode:

```bash
docker compose up -d --build
```

---

## View Service Status

```bash
docker compose ps
```

The command shows the state and published ports of the Compose services.

All running Docker containers can also be viewed with:

```bash
docker ps
```

---

## View Logs

View logs from all services:

```bash
docker compose logs
```

Follow the logs continuously:

```bash
docker compose logs -f
```

View one service:

```bash
docker compose logs web
```

View the database logs:

```bash
docker compose logs mydb
```

Display the most recent 50 lines:

```bash
docker compose logs --tail 50
```

Logs are normally the first place to look when a service fails.

---

## Stop Services

Stop the containers without removing them:

```bash
docker compose stop
```

Start the stopped containers again:

```bash
docker compose start
```

---

## Restart Services

Restart all services:

```bash
docker compose restart
```

Restart one service:

```bash
docker compose restart web
```

---

## Stop and Remove the Application

```bash
docker compose down
```

This normally removes:

- Service containers
- The Compose network

It does not normally remove named volumes or built images.

---

## Rebuild the Application

After changing the application or Dockerfile:

```bash
docker compose down
docker compose up --build
```

To rebuild one service:

```bash
docker compose build web
```

---

# Docker Compose Networking

Compose automatically creates a private default network for the application.

```text
Compose default network
├── web
└── mydb
```

Services can communicate using service names as hostnames.

The Flask service connects to:

```text
mydb:3306
```

In this address:

```text
mydb = Compose service name
3306 = MySQL container port
```

The Flask application should not use `localhost` to connect to the MySQL container.

Inside the Flask container:

```text
localhost = The Flask container itself
```

It does not refer to the database container.

Incorrect:

```python
host="localhost"
```

Correct:

```python
host="mydb"
```

---

# Container Names and Service Names

A Compose service might be defined as:

```yaml
services:
  mydb:
    image: mysql:8
```

Compose generates a container name based on the project and service:

```text
project-mydb-1
```

The other services still connect using:

```text
mydb
```

because `mydb` is the service name.

It is usually unnecessary to add:

```yaml
container_name: mydb
```

Allowing Compose to generate container names:

- Reduces name conflicts
- Supports service scaling
- Keeps projects isolated
- Makes configurations more reusable

---

# Debugging a Container-Name Conflict

An error might say:

```text
Conflict. The container name "/mydb" is already in use.
```

Docker does not allow two containers to have the same name.

List all containers:

```bash
docker ps -a
```

If the old container is no longer needed, stop and remove it:

```bash
docker stop mydb
docker rm mydb
```

A stopped container can be removed directly:

```bash
docker rm mydb
```

If the container must be kept, rename it:

```bash
docker rename mydb old-mydb
```

If it was created by the current Compose project, run:

```bash
docker compose down
```

The longer-term solution is normally to remove unnecessary `container_name` settings from the Compose file.

---

# Common Docker Compose Errors

## `docker-compose: command not found`

The older standalone command used a hyphen:

```bash
docker-compose up
```

Docker Compose v2 uses:

```bash
docker compose up
```

There is a space between `docker` and `compose`.

---

## Obsolete Version Warning

A warning may say:

```text
The attribute version is obsolete.
```

Remove the following line:

```yaml
version: "3.8"
```

Start the Compose file with:

```yaml
services:
```

---

## YAML Parsing Error

Possible causes include:

- Incorrect indentation
- Tabs instead of spaces
- Missing colons
- Incorrect list formatting
- Duplicate keys

Validate the file:

```bash
docker compose config
```

This displays the resolved configuration if it is valid.

---

## Port Is Already Allocated

Example:

```text
Bind for 0.0.0.0:5002 failed: port is already allocated
```

Another container or process is already using host port `5002`.

Check running containers:

```bash
docker ps
```

Stop the conflicting container if it is no longer needed:

```bash
docker stop CONTAINER_NAME
```

Alternatively, use a different host port:

```yaml
ports:
  - "5003:5002"
```

Then open:

```text
http://127.0.0.1:5003
```

---

## Unknown Server Host

Example:

```text
Unknown server host 'mydb'
```

Possible causes include:

- The MySQL service is not running
- The services are not on the same Docker network
- The service name is spelled differently
- The web container was started separately with `docker run`
- The application is using the wrong hostname

Check the services:

```bash
docker compose ps
```

Check the database logs:

```bash
docker compose logs mydb
```

Make sure the names match.

Compose:

```yaml
services:
  mydb:
```

Application:

```python
host="mydb"
```

---

## Connection Refused

Example:

```text
Can't connect to MySQL server
```

This usually means that the hostname was resolved but the database was not accepting connections.

Possible reasons include:

- MySQL is still initialising
- MySQL exited with an error
- The wrong port is being used
- The web service started too quickly
- The database health check is failing

Check the database logs:

```bash
docker compose logs mydb
```

Check the service state:

```bash
docker compose ps
```

Restart the web service after the database becomes healthy:

```bash
docker compose restart web
```

---

## Access Denied

Example:

```text
Access denied for user 'root'
```

The application reached MySQL, but the credentials were rejected.

Make sure the settings match.

Compose configuration:

```yaml
MYSQL_ROOT_PASSWORD: password
MYSQL_DATABASE: mydatabase
```

Application configuration:

```python
password="password"
database="mydatabase"
```

If MySQL was previously initialised with different settings, changing the environment variables does not automatically replace the credentials stored in an existing volume.

For a disposable learning database, the old volume can be removed and recreated:

```bash
docker compose down -v
docker compose up --build
```

> This deletes the database data stored in the Compose volume.

---

## Service Exited

Check its current state:

```bash
docker compose ps -a
```

Read its logs:

```bash
docker compose logs SERVICE_NAME
```

Inspect the fully resolved Compose configuration:

```bash
docker compose config
```

Do not repeatedly restart the application without reading the error shown in the logs.

---

# Recommended Debugging Process

## 1. Validate the Compose File

```bash
docker compose config
```

This identifies YAML and configuration errors.

## 2. Check Service Status

```bash
docker compose ps -a
```

Look for services that:

- Exited
- Restarted repeatedly
- Failed their health checks
- Did not start

## 3. Read the Logs

```bash
docker compose logs
```

For one service:

```bash
docker compose logs web
docker compose logs mydb
```

## 4. Check Existing Containers

```bash
docker ps -a
```

Look for:

- Name conflicts
- Old containers
- Exited containers
- Unexpected port mappings

## 5. Inspect Networks

```bash
docker network ls
```

Inspect the Compose network:

```bash
docker network inspect NETWORK_NAME
```

Confirm that the expected containers are connected.

## 6. Restart Cleanly

```bash
docker compose down
docker compose up --build
```

Only remove volumes when the stored local data is no longer needed.

---

# Useful Docker Compose Commands

| Command | Purpose |
|---|---|
| `docker compose config` | Validate and display the resolved configuration |
| `docker compose build` | Build service images |
| `docker compose pull` | Download service images |
| `docker compose up` | Create and start services |
| `docker compose up --build` | Rebuild images and start services |
| `docker compose up -d` | Start services in the background |
| `docker compose ps` | Show service containers |
| `docker compose logs` | Display service logs |
| `docker compose logs -f` | Follow service logs |
| `docker compose exec SERVICE COMMAND` | Run a command inside a service container |
| `docker compose stop` | Stop services without removing them |
| `docker compose start` | Start existing stopped services |
| `docker compose restart` | Restart services |
| `docker compose down` | Stop and remove containers and networks |
| `docker compose down -v` | Also remove named volumes |
| `docker compose images` | Show images used by the project |

---

# Complete Compose Workflow

```text
1. Create the application
2. Create requirements.txt
3. Create the Dockerfile
4. Create the Compose file
5. Add environment-variable configuration
6. Add required volumes
7. Run docker compose config
8. Run docker compose up --build
9. Check docker compose ps
10. Read docker compose logs
11. Test the application
12. Run docker compose down when finished
```

---

# Mental Model

| Component | Purpose |
|---|---|
| Dockerfile | Describes how to build one image |
| Docker image | Acts as a blueprint for containers |
| Docker container | Runs an instance of an image |
| Compose file | Describes how several services work together |
| Docker Compose | Creates and manages the application |
| Service name | Provides a hostname on the Compose network |
| Port mapping | Exposes a container service through the host |
| Environment variable | Provides runtime configuration |
| Volume | Preserves data outside the container lifecycle |
| Health check | Reports whether a service is functioning correctly |

---

# Common Interview Questions

## What is Docker Compose?

Docker Compose is a tool for defining and managing multi-container Docker applications using a YAML configuration file.

## What is the difference between Docker and Docker Compose?

Docker builds images and runs individual containers. Docker Compose defines and manages several related services as one application.

## How do Compose services communicate?

Compose connects services to a shared network. Containers can communicate using their service names as hostnames.

## Why should a container not use `localhost` to reach another container?

Inside a container, `localhost` refers to that same container. Another service must be reached through its service name or network address.

## Does `depends_on` guarantee that a database is ready?

Basic `depends_on` controls startup order, but it does not guarantee service readiness. Health checks and application retry logic can be used for that.

## Why are volumes used with databases?

Volumes store database data outside the container’s writable layer, allowing the data to remain when the container is replaced or removed.

## Why should `container_name` normally be avoided?

Compose already creates unique container names. Manually setting names can cause conflicts and can prevent a service from being scaled normally.

---

# Summary

- Docker Compose manages multi-container applications.
- Compose files are written in YAML.
- The `services` section defines the application’s containers.
- `build` creates an image from a Dockerfile.
- `image` uses an existing image.
- `ports` maps host ports to container ports.
- Environment variables provide runtime configuration.
- Volumes preserve data outside the container lifecycle.
- Compose automatically creates a shared network.
- Services communicate using their service names.
- `localhost` inside one container does not refer to another container.
- `depends_on` controls startup order but does not always guarantee readiness.
- Health checks help report whether services are functioning.
- `docker compose up` starts the application.
- `docker compose down` stops and removes its containers and network.
- Logs, status checks and configuration validation should be used during debugging.
