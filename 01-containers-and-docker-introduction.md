# Introduction to Containers and Docker

Containers are one of the most important technologies in modern software development.

They are commonly used in:

- DevOps
- Cloud engineering
- Platform engineering
- Site reliability engineering
- Software engineering

Major technology companies use containers to build, test and deploy applications consistently.

---

## Why Containers Matter

Before containers, developers regularly experienced the following problem:

```text
"It works on my machine."
```

An application might work correctly on a developer’s computer but fail when moved to a testing or production environment.

This could happen because the environments had different:

- Operating systems
- Software versions
- Libraries
- Dependencies
- Configuration
- Environment variables

Containers help solve this problem by packaging the application and its required environment together.

---

## What Is a Container?

A container is a lightweight, isolated package containing everything an application needs to run.

This can include:

- Application code
- Libraries
- Dependencies
- Runtime
- Configuration

A container can be thought of as a portable box for an application. The box contains the application and everything required to run it consistently.

### Real-world analogy

Imagine opening a restaurant. To operate it successfully, you need:

- Ingredients
- Kitchen equipment
- Staff
- Recipes

Now imagine being able to package the entire setup into a portable box.

Wherever that box is moved, it provides:

```text
The same setup
The same equipment
The same results
```

Containers provide similar portability and consistency for applications.

---

## Why Containers Exist

Without containers, development and production environments might use different software versions.

For example, the development environment might use:

```text
Python version: 3.10
Node.js version: 18
Ubuntu version: 22.04
```

The production server might use:

```text
Python version: 3.8
Node.js version: 16
Ubuntu version: 20.04
```

These differences could cause the application to fail.

With containers, the application uses the same packaged environment during development, testing and production.

```text
Development environment
          +
Testing environment
          +
Production environment
          =
Consistent application environment
```

---

## Benefits of Containers

### 1. Portability

A containerised application can run on different environments, including:

- A developer’s laptop
- A physical server
- A virtual machine
- A cloud platform
- A Kubernetes cluster

A useful phrase to remember is:

```text
Build once, run anywhere.
```

### 2. Consistency

Containers provide the same application environment throughout the development lifecycle.

This reduces problems caused by differences between development, testing and production systems.

### 3. Fast deployment

Containers normally start within seconds because they do not need to boot a complete operating system.

Virtual machines usually take longer because each VM must start its own guest operating system.

### 4. Lightweight

Containers share the host machine’s operating-system kernel.

This generally means they require:

- Less memory
- Less storage
- Fewer system resources
- Less startup time

### 5. Scalability

Multiple instances of the same application container can be started to handle additional traffic.

```text
Application Container 1
Application Container 2
Application Container 3
```

Container orchestration tools can automatically increase or decrease the number of running containers.

### 6. Isolation

Each container runs in an isolated environment.

Applications can have separate:

- Processes
- Filesystems
- Networks
- Dependencies
- Configuration

If one container stops, the other containers can continue running.

---

## What Is Docker?

Docker is a platform used to build, run, manage and share containers.

Docker provides tools that make it easier to:

- Build container images
- Start containers
- Stop containers
- Manage container networks
- Manage container storage
- Share images through registries

The difference between Docker and containers can be remembered as:

```text
Container = The technology
Docker    = A platform used to work with containers
```

Docker is not the container itself. It is one of the tools used to create and manage containers.

---

## Basic Docker Architecture

A simplified Docker workflow looks like this:

```text
Dockerfile
    |
    v
Docker Image
    |
    | docker run
    v
Docker Container
```

The Dockerfile provides the instructions used to build an image. The image is then used to start one or more containers.

---

## What Is a Docker Image?

A Docker image is a read-only blueprint used to create containers.

An image can contain:

- A base operating-system layer
- Application files
- Dependencies
- Runtime software
- Configuration
- Startup instructions

An image can be compared to a recipe. It describes what is needed to create the final result.

```text
Docker image = Cake recipe
Container    = The finished cake
```

Images are static. They do not become active applications until they are used to start containers.

---

## What Is a Docker Container?

A container is a running instance of a Docker image.

For example:

```text
Image:     nginx
Container: Running Nginx web server
```

Several containers can be created from the same image.

```text
                 +--> Container 1
Nginx Image -----+--> Container 2
                 +--> Container 3
```

Each container is a separate running instance, even though all three were created from the same image.

---

## Docker Image Versus Container

| Docker image | Docker container |
|---|---|
| Blueprint | Running instance |
| Static | Active |
| Read-only template | Has a writable container layer |
| Used to create containers | Created from an image |
| Can be stored in a registry | Runs on a container host |

A useful way to remember the difference is:

```text
Image + docker run = Container
```

---

## Basic Docker Workflow

An image can be downloaded from a container registry using:

```bash
docker pull nginx
```

The image can then be used to start a container:

```bash
docker run nginx
```

The process is:

```text
Docker registry
      |
      | docker pull
      v
Docker image
      |
      | docker run
      v
Running container
```

---

## Docker in Modern Development

Before containers, application deployment often involved:

```text
Build the application
Deploy it manually
Install dependencies
Resolve version conflicts
Fix environment problems
```

With Docker, the workflow becomes more consistent:

```text
Write application
Build Docker image
Test image
Push image to registry
Deploy the same image
Run container
```

The same tested image can be used across multiple environments.

---

## Where Docker Is Used

Docker is commonly used in:

- Development environments
- Testing environments
- CI/CD pipelines
- Cloud deployments
- Microservice architectures
- Kubernetes environments
- Automated testing
- Application modernisation

---

## Example DevOps Workflow

A common container-based DevOps workflow is:

```text
Developer pushes code
          |
          v
GitHub repository
          |
          v
CI/CD pipeline starts
          |
          v
Docker image is built
          |
          v
Automated tests run
          |
          v
Image is pushed to a registry
          |
          v
Deployment system pulls the image
          |
          v
Application container starts
```

This creates a repeatable deployment process and ensures the same image is tested and deployed.

---

## Virtual Machines Versus Containers

Understanding the difference between virtual machines and containers is a common Docker interview topic.

### What Is a Virtual Machine?

A virtual machine is a software-based computer that runs a complete operating system inside another physical or virtual machine.

For example:

```text
Physical laptop
      |
      v
VirtualBox
      |
      v
Ubuntu virtual machine
```

Each virtual machine contains:

- A guest operating system
- Its own kernel
- System libraries
- Application dependencies
- The application

### Virtual machine structure

```text
Physical Hardware
        |
        v
Host Operating System
        |
        v
Hypervisor
        |
        v
Guest Operating System
        |
        v
Application
```

### Container structure

```text
Physical Hardware
        |
        v
Host Operating System
        |
        v
Container Runtime
        |
        v
Containerised Application
```

Containers share the host operating-system kernel instead of running a complete guest operating system for every application.

---

## Main Difference

A virtual machine contains a complete guest operating system.

A container shares the host kernel while isolating the application and its dependencies.

```text
Virtual machine = Virtualises an entire machine
Container       = Isolates an application and its environment
```

---

## Virtual Machine and Container Comparison

| Virtual machine | Container |
|---|---|
| Contains a complete guest OS | Shares the host kernel |
| Usually larger | Usually smaller |
| Uses more memory and storage | Uses fewer resources |
| Slower to start | Faster to start |
| Strong hardware-level isolation | Process-level isolation |
| Can run a different guest OS | Must use a compatible host kernel |
| Suitable for full system virtualisation | Suitable for application packaging |

Containers and virtual machines are not direct replacements for one another. They solve different problems and are often used together.

For example, a cloud virtual machine can act as the host for several Docker containers.

---

## When to Use Virtual Machines

Virtual machines are useful when:

- A complete operating system is required
- Stronger workload isolation is needed
- Different operating systems must run on the same hardware
- Working with legacy applications
- Testing operating-system-level changes
- Running applications that require their own kernel

---

## When to Use Containers

Containers are useful when:

- Applications must be deployed quickly
- Consistency is needed between environments
- Building CI/CD pipelines
- Developing microservices
- Scaling application instances
- Running cloud-native applications
- Efficient use of resources is important

---

## Key Terms

| Term | Meaning |
|---|---|
| Container | An isolated package containing an application and its dependencies |
| Docker | A platform used to build and manage containers |
| Dockerfile | A file containing instructions for building an image |
| Image | A read-only blueprint used to create containers |
| Container instance | A running instance of an image |
| Registry | A service used to store and distribute images |
| Portability | The ability to run an application across different environments |
| Isolation | Separation between application processes and resources |
| Virtual machine | A software-based computer containing a complete guest OS |
| Container runtime | Software responsible for running and managing containers |

---

## Common Interview Questions

### What is the difference between a Docker image and a container?

A Docker image is a read-only blueprint containing an application and its required environment. A container is a running instance created from that image.

### What problem do containers solve?

Containers reduce differences between development, testing and production by packaging the application and its dependencies together.

### Why are containers lightweight?

Containers share the host operating-system kernel instead of running a complete guest operating system for each application.

### What is the difference between a virtual machine and a container?

A virtual machine virtualises an entire computer and includes a guest operating system. A container isolates an application while sharing the host kernel.

### Can multiple containers be created from one image?

Yes. Multiple isolated containers can run from the same Docker image.

---

## Summary

- Containers package applications and their dependencies together.
- Containers provide portability and consistency.
- Docker is a popular platform for building and managing containers.
- A Docker image is a blueprint used to create containers.
- A container is a running instance of an image.
- Multiple containers can be created from one image.
- Containers share the host operating-system kernel.
- Virtual machines contain complete guest operating systems.
- Containers normally start faster and use fewer resources than virtual machines.
- Docker is commonly used in development, testing, CI/CD and cloud deployments.
- Container registries store and distribute Docker images.
- Kubernetes and other orchestration platforms manage containers at scale.
