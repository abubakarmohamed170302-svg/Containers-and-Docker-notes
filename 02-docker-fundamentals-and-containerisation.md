# Docker Fundamentals and Web Application Containerisation

Docker can initially feel complicated because it combines several different topics:

- Linux commands
- Application development
- Python and Flask
- Dockerfiles
- Images and containers
- Ports
- Networking
- Databases
- Git and GitHub

The main concept to remember is:

> Docker packages an application and its dependencies so that it can run consistently across different environments.

---

## Installing Docker on Ubuntu

Update the available package information:

```bash
sudo apt update
```

Install Docker:

```bash
sudo apt install docker.io -y
```

Check that Docker was installed:

```bash
docker --version
```

Test Docker by running the `hello-world` image:

```bash
sudo docker run hello-world
```

If the test is successful, Docker will download the image and start a container that displays a confirmation message.

---

## Running Docker Without `sudo`

By default, Docker commands may require administrator privileges.

Add the current user to the `docker` group:

```bash
sudo usermod -aG docker $USER
```

Apply the new group membership by logging out and back in, restarting the machine or running:

```bash
newgrp docker
```

Test Docker again:

```bash
docker run hello-world
```

> Membership in the `docker` group gives the user powerful access to the machine. It should only be given to trusted users.

---

## Docker Images and Containers

A Docker image is a read-only blueprint used to create containers.

A container is a running instance of an image.

| Docker image | Docker container |
|---|---|
| Blueprint | Running application |
| Static | Active |
| Built using a Dockerfile | Created from an image |
| Can be stored in a registry | Runs on a Docker host |
| Example: `hello-flask` | Running Flask application |

The relationship can be remembered as:

```text
Dockerfile
    |
    | docker build
    v
Docker image
    |
    | docker run
    v
Docker container
```

---

## Recommended Repository Structure

A simple Docker learning repository could use the following structure:

```text
docker-learning/
├── README.md
├── hello_flask/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
└── notes/
```

A normal Git workflow is:

```bash
git status
git add .
git commit -m "Add containerised Flask application"
git push
```

Development-only files should not be committed to GitHub.

Example `.gitignore`:

```gitignore
venv/
__pycache__/
*.pyc
.env
```

This prevents virtual environments, Python cache files and environment-variable files from being tracked.

---

# Understanding Dockerfiles

A `Dockerfile` is a text file containing the instructions Docker follows when building an image.

The filename must be written exactly as:

```text
Dockerfile
```

Linux filenames are case-sensitive, so `dockerfile` and `Dockerfile` are different names.

---

## Simple Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

---

## `FROM`

```dockerfile
FROM python:3.12-slim
```

`FROM` selects the base image.

This example starts with a small Linux-based image that already contains Python 3.12.

Every Dockerfile normally begins with a `FROM` instruction.

---

## `WORKDIR`

```dockerfile
WORKDIR /app
```

`WORKDIR` sets the working directory inside the image.

Docker creates `/app` if it does not already exist. The instructions that follow will operate from this directory.

It is similar to using:

```bash
cd /app
```

inside a Linux environment.

---

## `COPY`

```dockerfile
COPY requirements.txt .
```

This copies `requirements.txt` from the build context into the current working directory inside the image.

The following instruction copies the remaining project files:

```dockerfile
COPY . .
```

In this instruction:

```text
First .  = Current project directory on the host
Second . = Current working directory inside the image
```

---

## `RUN`

```dockerfile
RUN pip install --no-cache-dir -r requirements.txt
```

`RUN` executes a command while Docker is building the image.

This example installs the Python dependencies listed in `requirements.txt`.

The results become part of the image.

---

## `EXPOSE`

```dockerfile
EXPOSE 5000
```

`EXPOSE` documents that the application inside the container listens on port `5000`.

It does not make the application accessible from the host by itself.

The port must still be published when starting the container:

```bash
docker run -p 5000:5000 hello-flask
```

---

## `CMD`

```dockerfile
CMD ["python", "app.py"]
```

`CMD` defines the default command that runs when a container starts.

In this example, Docker starts the Flask application by running:

```bash
python app.py
```

The JSON-array form is preferred because Docker passes the arguments directly to the process.

---

# Containerising a Flask Application

Containerisation is the process of packaging an application and its required environment into a container image.

The basic workflow is:

```text
Create application
       |
       v
Test application locally
       |
       v
Create Dockerfile
       |
       v
Build image
       |
       v
Run container
       |
       v
Test application in browser
```

---

## 1. Create the Project Directory

```bash
mkdir hello_flask
cd hello_flask
```

Create the application files:

```bash
touch app.py requirements.txt Dockerfile .dockerignore
```

The directory should contain:

```text
hello_flask/
├── app.py
├── requirements.txt
├── Dockerfile
└── .dockerignore
```

---

## 2. Create the Flask Application

Add the following code to `app.py`:

```python
from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello Docker!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

### Import Flask

```python
from flask import Flask
```

This imports the `Flask` class from the installed Flask package.

### Create the application

```python
app = Flask(__name__)
```

This creates the Flask application object.

### Create the homepage route

```python
@app.route("/")
def home():
    return "Hello Docker!"
```

The `/` route represents the application’s homepage.

When someone visits it, Flask returns:

```text
Hello Docker!
```

### Start the development server

```python
app.run(host="0.0.0.0", port=5000)
```

The application listens on port `5000`.

Using `0.0.0.0` tells Flask to listen on all available network interfaces inside the container.

If the application only listens on `127.0.0.1`, it may not accept connections coming through Docker’s published port.

---

## 3. Add the Python Dependency

Add Flask to `requirements.txt`:

```text
Flask==3.1.1
```

Using a requirements file makes the application’s dependencies clear and repeatable.

---

## 4. Add `.dockerignore`

Add the following to `.dockerignore`:

```dockerignore
venv/
__pycache__/
*.pyc
.git/
.gitignore
.env
```

A `.dockerignore` file prevents unnecessary files from being sent to Docker during the build.

This can:

- Make builds faster
- Reduce the image size
- Improve caching
- Prevent sensitive files from entering the image

---

## 5. Test the Application Locally

Create a Python virtual environment:

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Start the application:

```bash
python app.py
```

Open the following address:

```text
http://127.0.0.1:5000
```

The page should display:

```text
Hello Docker!
```

Stop the application with:

```text
Ctrl+C
```

Deactivate the virtual environment:

```bash
deactivate
```

Testing locally first helps separate application errors from Docker errors.

---

## 6. Create the Dockerfile

Add the following to `Dockerfile`:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

The dependency file is copied and installed before the remaining application code.

This allows Docker to reuse the dependency layer when the code changes but `requirements.txt` remains the same.

---

## 7. Build the Docker Image

Run the build command from the directory containing the Dockerfile:

```bash
docker build -t hello-flask .
```

Command breakdown:

| Part | Meaning |
|---|---|
| `docker build` | Builds a Docker image |
| `-t` | Assigns a name or tag |
| `hello-flask` | Image name |
| `.` | Uses the current directory as the build context |

Check that the image exists:

```bash
docker images
```

The output should include an image named:

```text
hello-flask
```

---

## 8. Run the Container

Start the container:

```bash
docker run --name hello-flask-container -p 5000:5000 hello-flask
```

Command breakdown:

| Part | Meaning |
|---|---|
| `docker run` | Creates and starts a container |
| `--name` | Assigns a readable container name |
| `hello-flask-container` | Container name |
| `-p 5000:5000` | Publishes the container port |
| `hello-flask` | Image used to create the container |

Open:

```text
http://127.0.0.1:5000
```

The browser should display:

```text
Hello Docker!
```

---

## Running in Detached Mode

Use `-d` to run the container in the background:

```bash
docker run -d --name hello-flask-container -p 5000:5000 hello-flask
```

Check the running container:

```bash
docker ps
```

View its logs:

```bash
docker logs hello-flask-container
```

Follow the logs continuously:

```bash
docker logs -f hello-flask-container
```

Stop the container:

```bash
docker stop hello-flask-container
```

Remove the stopped container:

```bash
docker rm hello-flask-container
```

---

# Docker Port Mapping

Containers run inside isolated network environments.

Even if an application listens on a port inside its container, the port is not automatically accessible from the host.

The following command publishes the port:

```bash
docker run -p 5000:5000 hello-flask
```

The format is:

```text
-p HOST_PORT:CONTAINER_PORT
```

In this example:

```text
Browser
   |
   | localhost:5000
   v
Host port 5000
   |
   | Docker port mapping
   v
Container port 5000
   |
   v
Flask application
```

---

## Using a Different Host Port

The host and container ports do not need to use the same number.

```bash
docker run -p 5002:5000 hello-flask
```

This means:

```text
Host port:      5002
Container port: 5000
```

The application would be opened at:

```text
http://127.0.0.1:5002
```

The Flask application still listens on port `5000` inside the container.

---

## Common Application Ports

| Service | Common port |
|---|---:|
| HTTP | 80 |
| HTTPS | 443 |
| Flask development server | 5000 |
| MySQL | 3306 |
| Redis | 6379 |
| PostgreSQL | 5432 |

These are common defaults, but applications can be configured to use different ports.

---

# Communication Between Containers

A common multi-container architecture could contain:

```text
Flask container
       |
       v
MySQL container
```

Containers need a shared Docker network to communicate by container or service name.

For example:

```text
Docker Network
├── flask-app
└── mydb
```

When both containers are connected to the same user-defined network, the Flask application can use `mydb` as the database hostname.

---

## Creating a Docker Network Manually

Create a user-defined bridge network:

```bash
docker network create app-network
```

Start the database on the network:

```bash
docker run -d \
  --name mydb \
  --network app-network \
  -e MYSQL_ROOT_PASSWORD=rootpassword \
  -e MYSQL_DATABASE=testdb \
  mysql:8
```

Start the Flask container on the same network:

```bash
docker run -d \
  --name flask-app \
  --network app-network \
  -p 5000:5000 \
  hello-flask
```

The Flask container can now attempt to connect to the hostname:

```text
mydb
```

Docker’s internal DNS resolves that name to the database container.

---

# Docker Compose for Multiple Containers

Docker Compose is normally easier than running every multi-container service manually.

A basic `compose.yml` could contain:

```yaml
services:
  web:
    build: .
    ports:
      - "5000:5000"
    depends_on:
      - mydb

  mydb:
    image: mysql:8
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: testdb
    volumes:
      - mysql-data:/var/lib/mysql

volumes:
  mysql-data:
```

Docker Compose automatically creates:

- The Flask container
- The MySQL container
- A shared network
- Service-name DNS resolution
- The named database volume

The Flask application can use `mydb` as the database hostname because it matches the Compose service name.

> `depends_on` controls startup order, but it does not guarantee that MySQL is ready to accept connections. A health check or retry logic may still be required.

Docker Compose is covered in more detail in the next notes file.

---

# Troubleshooting Common Errors

## Unknown Server Host

Example:

```text
Unknown server host 'mydb'
```

This means the application cannot resolve the hostname `mydb`.

Possible causes include:

- The database container is not running
- The containers are not on the same network
- The service or container name is incorrect
- The application uses the wrong hostname
- Only the Flask container was started

Useful checks:

```bash
docker ps
docker network ls
docker network inspect app-network
```

Make sure the hostname in the application matches the database service name.

---

## Connection Refused

Example:

```text
Connection refused
```

This normally means the host was found, but the service did not accept the connection.

Possible causes include:

- The database is still starting
- The service has stopped
- The wrong port is being used
- The service is listening on a different interface
- The application started before the database was ready

Check the logs:

```bash
docker logs mydb
```

Check whether the container is running:

```bash
docker ps -a
```

For Compose applications, health checks and application retry logic can help.

---

## Access Denied

Example:

```text
Access denied
```

This normally indicates an authentication or authorisation problem.

Check:

- Database username
- Database password
- Database name
- Environment variables
- User permissions
- Whether the database was previously initialised with different credentials

Avoid placing real passwords directly inside files committed to GitHub.

---

## Dockerfile Not Found

Example:

```text
failed to read dockerfile
```

Check that:

- The file is named `Dockerfile`
- The capitalisation is correct
- The build command is being run from the correct directory
- The build context contains the Dockerfile

Check the current directory:

```bash
pwd
ls -la
```

Build again:

```bash
docker build -t hello-flask .
```

---

## Application Cannot Be Opened in the Browser

Check whether the container is running:

```bash
docker ps
```

Check its logs:

```bash
docker logs hello-flask-container
```

Check the published ports:

```bash
docker port hello-flask-container
```

Make sure Flask listens on:

```python
app.run(host="0.0.0.0", port=5000)
```

Make sure the container is started with the correct mapping:

```bash
docker run -p 5000:5000 hello-flask
```

---

## Port Is Already in Use

Example:

```text
bind: address already in use
```

Another process or container is already using the host port.

View running containers:

```bash
docker ps
```

Either stop the conflicting container or use a different host port:

```bash
docker run -p 5002:5000 hello-flask
```

The application would then be available at:

```text
http://127.0.0.1:5002
```

---

## Incorrect Python Package Name

A space can accidentally turn one package name into multiple package names.

Incorrect:

```dockerfile
RUN pip install flask my sqlclient
```

This tries to install separate packages called `my` and `sqlclient`.

Correct:

```dockerfile
RUN pip install flask mysqlclient
```

A better approach is to list dependencies inside `requirements.txt`:

```text
Flask==3.1.1
mysqlclient==2.2.7
```

Then install them with:

```dockerfile
RUN pip install --no-cache-dir -r requirements.txt
```

Some Python database packages require additional operating-system libraries during the image build.

---

# Useful Debugging Commands

## View running containers

```bash
docker ps
```

## View all containers

```bash
docker ps -a
```

## View container logs

```bash
docker logs container_name_or_id
```

## Follow container logs

```bash
docker logs -f container_name_or_id
```

## Inspect a container

```bash
docker inspect container_name_or_id
```

## Stop a container

```bash
docker stop container_name_or_id
```

## Remove a stopped container

```bash
docker rm container_name_or_id
```

## View images

```bash
docker images
```

## Remove an unused image

```bash
docker rmi image_name_or_id
```

## View networks

```bash
docker network ls
```

## Inspect a network

```bash
docker network inspect network_name
```

---

# Beginner Containerisation Workflow

```text
1. Write the application
2. Test the application locally
3. Create requirements.txt
4. Create .dockerignore
5. Create the Dockerfile
6. Build the Docker image
7. Check that the image exists
8. Run a container
9. Publish the required port
10. Test the application
11. Read the container logs if it fails
12. Add additional services using Docker Compose
13. Commit the clean project files to GitHub
```

---

# Mental Model

| Component | Simple meaning |
|---|---|
| Dockerfile | Image build instructions |
| Docker image | Application blueprint |
| Docker container | Running application instance |
| Port mapping | Connects a host port to a container port |
| Docker network | Allows containers to communicate |
| Docker volume | Stores persistent data |
| Docker Compose | Defines and manages multiple services |
| Docker registry | Stores and distributes images |

---

# Common Interview Questions

## Why must Flask use `0.0.0.0` inside a container?

`0.0.0.0` makes Flask listen on every network interface inside the container. This allows requests forwarded through Docker’s published port to reach the application.

## What is the difference between `EXPOSE` and `-p`?

`EXPOSE` documents the port the image expects to use. The `-p` option publishes a container port to a port on the host.

## How do containers communicate with one another?

Containers connected to the same user-defined Docker network can communicate using container names or service names as hostnames.

## Why should an application be tested before it is containerised?

Testing it locally confirms that the application itself works. This makes it easier to identify whether a later error comes from the application or the Docker configuration.

## Why should dependencies be placed in `requirements.txt`?

A requirements file documents the dependencies and allows them to be installed consistently during local development, image builds and automated deployments.

---

# Summary

- Docker packages applications and their dependencies into images.
- A Dockerfile contains the instructions used to build an image.
- Containers are running instances of images.
- Flask must listen on `0.0.0.0` to accept connections through Docker.
- `EXPOSE` documents a port, while `-p` publishes it.
- Port mappings use the format `HOST_PORT:CONTAINER_PORT`.
- Containers require a shared network to communicate by name.
- Docker Compose simplifies multi-container application management.
- Logs, container status and network inspection are important debugging tools.
- Virtual environments, secrets and cache files should not be committed to GitHub.
- Applications should be tested before and after containerisation.
