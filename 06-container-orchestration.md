# Container Orchestration

Docker makes it possible to:

- Build images
- Run containers
- Connect containers
- Manage multi-container applications
- Push images to registries

Docker Compose works well for applications running a small number of containers on one machine.

For example:

```text
Flask container
Redis container
Nginx container
```

A company may need to run hundreds or thousands of containers across multiple servers. Managing every container manually would be difficult, slow and unreliable.

Container orchestration solves this problem.

---

# What Is Container Orchestration?

Container orchestration is the automated management of containerised applications across one or more machines.

An orchestration platform can:

- Deploy containers
- Select where containers run
- Restart or replace failed containers
- Scale application workloads
- Distribute network traffic
- Perform rolling updates
- Roll back failed releases
- Manage service discovery
- Monitor workload health
- Attach storage
- Manage configuration

An orchestrator can be thought of as a manager responsible for organising many containers and keeping the system in its required state.

---

# Why Docker Alone May Not Be Enough

Imagine an online shopping platform containing:

```text
Frontend services
Backend services
Payment services
Authentication services
Database services
```

The company might require:

```text
10 frontend containers
15 backend containers
5 payment containers
3 authentication containers
```

Without orchestration, engineers would need to manage questions such as:

- Which server should run each container?
- What happens when a container crashes?
- What happens when a server fails?
- How are new application versions deployed?
- How should the application scale?
- How do services find one another?
- How is traffic distributed?
- How is the desired number of containers maintained?

An orchestration platform automates much of this work.

---

# Desired State

Most orchestration platforms use a desired-state model.

Desired state means:

> The user declares what the system should look like, and the platform continuously works to make the actual state match it.

For example:

```text
Desired state: 3 web replicas
Actual state:  2 web replicas
Action:        Create 1 replacement
```

If four replicas are running when only three are required, the orchestrator can remove the extra replica.

```text
Desired state
      |
      v
Orchestrator compares state
      |
      v
Actual cluster state
      |
      v
Corrective action
```

---

# Declarative Configuration

Orchestration platforms commonly use declarative configuration.

Instead of writing every manual step, the configuration describes the required result.

Example:

```yaml
image: hello-flask:1.0.0
replicas: 3
port: 5000
```

The idea is:

```text
Run three copies of this image and make the application available.
```

The platform decides how to create and maintain that result.

---

# Main Orchestration Responsibilities

## Scheduling

Scheduling selects which machine should run a workload.

Suppose a cluster contains:

```text
Node A
Node B
Node C
```

The scheduler considers information such as:

- Available CPU
- Available memory
- Workload requirements
- Placement rules
- Node health
- Resource limits

It then assigns the workload to a suitable node.

---

## Self-Healing

Self-healing is the automatic recovery of failed workloads.

Example:

```text
Desired state: 3 replicas

Replica 1: Healthy
Replica 2: Failed
Replica 3: Healthy
```

The orchestrator detects the difference and starts a replacement:

```text
Replica 1: Healthy
Replica 2: Replacement created
Replica 3: Healthy
```

Self-healing does not necessarily repair faulty application code. It replaces or restarts failed workload instances to maintain the declared state.

---

## Scaling

Scaling changes the number of workload instances.

Scale up:

```text
3 replicas
     |
     v
10 replicas
```

Scale down:

```text
10 replicas
      |
      v
3 replicas
```

Scaling can be:

- Manual
- Scheduled
- Based on metrics
- Triggered by application demand

---

## Load Balancing

Load balancing distributes incoming traffic across several workload instances.

```text
Users
  |
  v
Load balancer or service
  |
  ├── Replica 1
  ├── Replica 2
  └── Replica 3
```

This reduces the chance of one container receiving all incoming traffic.

---

## Rolling Updates

A rolling update gradually replaces an older application version.

Initial state:

```text
Version 1
Version 1
Version 1
```

During the update:

```text
Version 2
Version 1
Version 1
```

Then:

```text
Version 2
Version 2
Version 1
```

Final state:

```text
Version 2
Version 2
Version 2
```

This allows capacity to remain available while the update is performed.

---

## Rollbacks

If a new release fails, the workload can be returned to a previous working version.

```text
Version 2 deployment fails
             |
             v
Rollback begins
             |
             v
Version 1 is restored
```

---

## Service Discovery

Container and pod IP addresses can change when workloads are replaced.

Service discovery allows applications to use stable service names rather than fixed workload IP addresses.

Example service names:

```text
frontend
backend
database
```

The frontend can communicate with the backend through its stable service name.

---

## Health Checks

Health checks help the platform understand the state of an application.

A health check may test:

- Whether the process is running
- Whether an HTTP endpoint responds
- Whether a TCP port accepts connections
- Whether the application is ready for traffic
- Whether the application remains healthy

An unhealthy workload can be restarted, replaced or temporarily removed from traffic.

---

## High Availability

High availability means designing the application to remain accessible when components fail.

For example:

```text
Node 1 fails
     |
     v
Application workloads remain on Nodes 2 and 3
```

Multiple replicas and nodes reduce dependence on one container or machine.

High availability requires suitable application, networking, storage and cluster design. Orchestration helps manage it but does not create it automatically.

---

# Clusters and Nodes

## Cluster

A cluster is a group of connected machines managed as one system.

```text
Cluster
├── Node 1
├── Node 2
└── Node 3
```

Application workloads are distributed across the cluster.

---

## Node

A node is one machine participating in the cluster.

A node can be:

- A physical server
- A virtual machine
- A cloud instance

Each node provides resources such as:

```text
CPU
Memory
Storage
Networking
```

---

# Introduction to Kubernetes

Kubernetes is an open-source container orchestration platform.

It is commonly abbreviated as:

```text
K8s
```

The number `8` represents the eight letters between `K` and `s` in the word Kubernetes.

Kubernetes is used to:

- Deploy containerised applications
- Maintain desired state
- Scale workloads
- Replace failed workloads
- Provide service discovery
- Manage networking
- Perform rolling updates
- Manage application configuration
- Connect applications to storage

A simple definition is:

> Kubernetes manages containerised applications across a cluster of machines.

A useful distinction is:

```text
Docker builds and runs containers.
Kubernetes manages containerised workloads at scale.
```

---

# Why Kubernetes Is Used

Container runtimes make it possible to start containers, but large systems need additional management.

Kubernetes helps answer:

```text
Where should the workloads run?
How many copies should run?
What happens when a node fails?
How should an application be updated?
How do users reach changing workloads?
How do services communicate?
```

---

# Kubernetes Cluster Structure

A simplified Kubernetes cluster contains:

```text
Control Plane
     |
     ├── Worker Node 1
     ├── Worker Node 2
     └── Worker Node 3
```

---

## Control Plane

The control plane manages the cluster and makes global decisions.

Its responsibilities include:

- Receiving Kubernetes API requests
- Storing cluster state
- Scheduling workloads
- Running control loops
- Comparing desired and actual state

Major control-plane components include:

| Component | Purpose |
|---|---|
| API server | Provides the Kubernetes API |
| Scheduler | Selects nodes for new pods |
| Controller manager | Runs controllers that maintain desired state |
| `etcd` | Stores cluster configuration and state |

The control plane can be thought of as the management layer or brain of the cluster.

---

## Worker Nodes

Worker nodes run the application workloads.

Important node components include:

| Component | Purpose |
|---|---|
| Kubelet | Ensures assigned pods are running |
| Container runtime | Runs the containers |
| Network component | Supports pod and service networking |

---

# Kubernetes Objects

## Pod

A pod is the smallest deployable unit in Kubernetes.

A pod normally contains one main application container:

```text
Pod
└── Flask container
```

A pod can contain multiple closely related containers that need to share networking or storage.

Containers inside the same pod share:

- A network namespace
- An IP address
- Port space
- Attached volumes

Pods are disposable and can be replaced with new IP addresses.

---

## Replica

A replica is one running copy of an application workload.

For example:

```text
replicas: 3
```

means that Kubernetes should maintain three copies.

---

## Deployment

A Deployment manages a set of application pods.

It can define:

- Container image
- Required replica count
- Pod labels
- Update strategy
- Pod configuration

Example desired state:

```text
Run three copies of hello-flask:1.0.0.
```

Kubernetes creates and manages the required pods.

If a pod fails, the Deployment’s underlying controller ensures that a replacement is created.

---

## Service

Pods can be replaced and their IP addresses can change.

A Kubernetes Service provides stable network access to a selected group of pods.

```text
Users or other applications
            |
            v
Kubernetes Service
            |
            ├── Pod 1
            ├── Pod 2
            └── Pod 3
```

The Service selects pods using labels and can distribute traffic between them.

---

## Namespace

A namespace provides logical separation inside a Kubernetes cluster.

Namespaces can help organise:

- Teams
- Applications
- Environments
- Access controls
- Resource policies

Example namespaces:

```text
development
staging
production
```

---

## ConfigMap and Secret

A ConfigMap stores non-sensitive configuration.

A Secret stores sensitive configuration values.

Examples include:

```text
Application mode
Service URL
Database hostname
API token
Database password
```

Sensitive values still require proper access control and encryption practices.

---

# Kubernetes Self-Healing Example

Desired state:

```text
3 pods
```

Actual state after a failure:

```text
Pod 1: Healthy
Pod 2: Failed
Pod 3: Healthy
```

Kubernetes creates a replacement:

```text
Pod 1: Healthy
Pod 4: New replacement
Pod 3: Healthy
```

The identity of the individual pod is not important. The required number of healthy replicas is what matters.

---

# Kubernetes Scaling Example

Initial state:

```text
2 web pods
```

Traffic increases:

```text
2 web pods
     |
     v
8 web pods
```

The Service can distribute traffic across the available pods.

When demand decreases, the number of replicas can be reduced.

---

# Kubernetes and Container Images

Kubernetes normally does not build application images.

A typical workflow is:

```text
Write code
      |
      v
Build and test image
      |
      v
Push image to registry
      |
      v
Kubernetes pulls image
      |
      v
Kubernetes creates pods
```

Possible registries include:

- Docker Hub
- Amazon ECR
- Azure Container Registry
- Google Artifact Registry
- Private self-hosted registries

---

# DevOps Workflow With Kubernetes

```text
Developer pushes code
          |
          v
CI/CD pipeline runs tests
          |
          v
Container image is built
          |
          v
Image is pushed to a registry
          |
          v
Kubernetes configuration is updated
          |
          v
New pods are created gradually
          |
          v
Old pods are removed
          |
          v
Health and deployment status are checked
```

---

# Docker Swarm

Docker Swarm mode is Docker Engine’s built-in orchestration feature.

It allows multiple Docker hosts to operate as one cluster.

A Swarm contains:

```text
Manager nodes
Worker nodes
```

---

## Swarm Manager

A manager node controls the cluster.

Its responsibilities include:

- Managing cluster membership
- Maintaining desired state
- Scheduling services
- Managing service configuration
- Coordinating updates

---

## Swarm Worker

Worker nodes run tasks assigned by manager nodes.

A task represents one container instance belonging to a Swarm service.

---

## Swarm Service

A Swarm service defines:

- The image to run
- Number of replicas
- Published ports
- Update behaviour
- Network configuration

Example desired state:

```text
Run three copies of Nginx.
```

---

# Basic Docker Swarm Commands

## Initialise a Swarm

```bash
docker swarm init
```

The command outputs a join token that workers can use to join the cluster.

Join tokens should be protected because they authorise nodes to join the Swarm.

---

## View Nodes

```bash
docker node ls
```

This command must be run from a manager node.

---

## Create a Service

```bash
docker service create \
  --name web \
  --replicas 3 \
  --publish 80:80 \
  nginx
```

---

## View Services

```bash
docker service ls
```

---

## View Service Tasks

```bash
docker service ps web
```

---

## Scale a Service

```bash
docker service scale web=5
```

---

## View Service Logs

```bash
docker service logs web
```

---

## Remove a Service

```bash
docker service rm web
```

---

## Leave the Swarm

A worker can leave with:

```bash
docker swarm leave
```

A manager leaving a single-node learning Swarm may require:

```bash
docker swarm leave --force
```

Forcing a manager to leave can affect the cluster and should only be done when the consequences are understood.

---

# Docker Swarm Versus Kubernetes

Both platforms manage containers across clusters, but they differ in features, complexity and adoption.

| Docker Swarm | Kubernetes |
|---|---|
| Built into Docker Engine | Separate orchestration platform |
| Easier initial setup | More complex initial setup |
| Uses familiar Docker commands | Uses Kubernetes objects and APIs |
| Smaller feature set | Larger feature set |
| Smaller ecosystem | Large cloud-native ecosystem |
| Suitable for simpler use cases | Suitable for simple through large systems |
| Less common in enterprise roles | Widely requested in DevOps roles |
| Basic orchestration model | Extensive workload-management features |

---

## Setup

A local Swarm can begin with:

```bash
docker swarm init
```

Kubernetes requires several components and more configuration.

Managed cloud services reduce the work involved in operating the Kubernetes control plane.

Examples include:

```text
Amazon Elastic Kubernetes Service
Azure Kubernetes Service
Google Kubernetes Engine
```

---

## Complexity

Docker Swarm uses familiar Docker concepts and commands.

Kubernetes introduces additional concepts, including:

- Pods
- Deployments
- Services
- Namespaces
- ConfigMaps
- Secrets
- Ingress
- Persistent volumes
- Resource requests and limits
- Role-based access control

Kubernetes has a steeper learning curve but provides more control and a larger ecosystem.

---

## Scaling

Both platforms support replica-based scaling.

Docker Swarm:

```bash
docker service scale web=5
```

Kubernetes uses the desired replica count and can also support metric-based automatic scaling.

---

## Networking

Docker Swarm provides:

- Service discovery
- Overlay networks
- Routing mesh

Kubernetes provides:

- Pod networking
- Services
- Internal DNS
- Ingress and Gateway options
- Network policies

---

## Self-Healing

Both platforms can replace failed workload instances.

Kubernetes provides several health-check and workload-management mechanisms for controlling readiness, liveness and startup behaviour.

---

## Ecosystem

Kubernetes has a large cloud-native ecosystem.

Common related technologies include:

```text
Helm
Prometheus
Grafana
Argo CD
Service meshes
```

Each tool solves a separate problem around areas such as packaging, monitoring, visualisation, delivery or service communication.

---

# Which Orchestration Platform Should Be Learned?

Docker Swarm can be useful for learning basic orchestration concepts because it is built into Docker and has a simpler setup.

Kubernetes is generally more important for a DevOps career because it is widely used by cloud providers and employers.

A sensible learning path is:

```text
Docker
  |
  v
Docker Compose
  |
  v
Container registries
  |
  v
Orchestration concepts
  |
  v
Kubernetes
```

---

# Benefits of Container Orchestration

## High Availability

Workloads can run across multiple nodes so that one node failure does not necessarily stop the whole application.

---

## Automatic Recovery

Without orchestration:

```text
Container fails
      |
      v
Engineer receives alert
      |
      v
Engineer manually restarts container
```

With orchestration:

```text
Workload fails
      |
      v
Orchestrator detects difference
      |
      v
Replacement is created
```

Monitoring and alerting are still required because repeated replacements may indicate a deeper problem.

---

## Easier Scaling

Workloads can be increased during busy periods:

```text
Normal traffic: 3 replicas
High traffic:  15 replicas
```

This can support services such as:

- Online shops
- Streaming platforms
- Banking applications
- Ticketing websites
- Social platforms

---

## Safer Deployments

Rolling updates replace workloads gradually.

If the new release fails its health checks, the deployment can be stopped or rolled back.

---

## Better Resource Usage

The scheduler places workloads according to available cluster resources and declared requirements.

Example:

```text
Node 1: High CPU usage
Node 2: Available capacity
```

A new workload may be scheduled on Node 2.

---

## Centralised Management

Instead of manually logging in to every server, engineers interact with the orchestration platform’s API and tools.

This provides a consistent management layer across the cluster.

---

# When Orchestration May Not Be Needed

Not every project requires Kubernetes or Docker Swarm.

A small application containing:

```text
One web container
One database container
```

may work well with Docker Compose on a single machine.

Adding Kubernetes to a small project can introduce unnecessary:

- Complexity
- Operational work
- Cost
- Security configuration
- Monitoring requirements

The orchestration platform should match the application’s actual needs.

---

# Docker Compose Versus Orchestration

| Docker Compose | Container orchestration |
|---|---|
| Commonly used on one machine | Manages workloads across clusters |
| Excellent for local development | Designed for managed deployments |
| Simple setup | More advanced setup |
| Starts related services | Maintains desired state |
| Manual or basic scaling | Managed or automatic scaling |
| Limited recovery features | Self-healing workload management |
| Useful for learning and testing | Useful for resilient production systems |

Docker Compose and Kubernetes are not identical tools. Compose describes a multi-container application, while Kubernetes manages distributed workloads through cluster-level objects and controllers.

---

# Real-World Scaling Scenario

An online shop receives a large increase in traffic during a sale.

Without suitable scaling:

```text
Traffic increases
      |
      v
One web container becomes overloaded
      |
      v
Application becomes slow or unavailable
```

With orchestration:

```text
Traffic increases
      |
      v
Metrics show higher demand
      |
      v
More application replicas are created
      |
      v
Traffic is distributed
      |
      v
Application capacity increases
```

When traffic falls, unnecessary replicas can be removed.

Effective automatic scaling still requires appropriate metrics, resource settings and application design.

---

# DevOps Responsibilities

DevOps engineers may use orchestration platforms to:

- Deploy applications
- Manage clusters
- Configure scaling
- Troubleshoot failed workloads
- Monitor workload health
- Manage rolling updates
- Connect CI/CD pipelines
- Configure networking
- Configure persistent storage
- Manage access controls
- Define resource requests and limits
- Maintain application configuration

---

# Important Terms

| Term | Meaning |
|---|---|
| Orchestration | Automated management of containerised workloads |
| Cluster | A group of connected machines |
| Node | One machine participating in a cluster |
| Scheduling | Selecting where a workload runs |
| Desired state | The declared system configuration |
| Actual state | The system’s current condition |
| Replica | One running copy of a workload |
| Scaling | Increasing or decreasing workload copies |
| Self-healing | Replacing failed workloads |
| Load balancing | Distributing network traffic |
| Rolling update | Gradually replacing an application version |
| Rollback | Returning to a previous version |
| Service discovery | Allowing services to find one another |
| Kubernetes | A widely used orchestration platform |
| Docker Swarm | Docker Engine’s built-in orchestration feature |
| Pod | Kubernetes’ smallest deployable unit |
| Deployment | Kubernetes object that manages replicated application pods |
| Service | Stable Kubernetes network access to selected pods |
| Namespace | Logical separation inside a Kubernetes cluster |

---

# Mental Model

```text
Docker
Builds images and runs individual containers

Docker Compose
Defines and runs related containers, commonly on one machine

Docker Swarm
Orchestrates Docker services across a Swarm cluster

Kubernetes
Manages containerised workloads across a cluster using declarative objects
```

---

# Complete Container Journey

```text
Write application
      |
      v
Create Dockerfile
      |
      v
Build and test image
      |
      v
Push image to registry
      |
      v
Orchestration platform pulls image
      |
      v
Workloads are scheduled across nodes
      |
      v
Traffic is distributed
      |
      v
Failed workloads are replaced
      |
      v
Application scales when required
```

---

# Common Interview Questions

## What is container orchestration?

Container orchestration is the automated deployment, scheduling, scaling, networking and recovery of containerised workloads across one or more machines.

## What is the difference between Docker and Kubernetes?

Docker can build images and run containers. Kubernetes deploys, scales and manages containerised workloads across a cluster.

## What is self-healing?

Self-healing means that the orchestration platform detects a difference between the desired and actual state and creates or replaces workloads to restore the declared state.

## What is a Kubernetes pod?

A pod is Kubernetes’ smallest deployable unit. It contains one or more closely related containers that share networking and can share storage.

## What is the difference between a pod and a container?

A container packages and runs an application process. A pod is a Kubernetes object that provides the environment in which one or more containers run.

## What is a Kubernetes Deployment?

A Deployment declaratively manages replicated application pods and supports controlled updates and rollbacks.

## What is a Kubernetes Service?

A Service provides a stable network endpoint for a selected group of pods whose individual IP addresses may change.

## What is the difference between Docker Compose and Kubernetes?

Docker Compose defines and runs related containers, commonly for development or smaller single-host environments. Kubernetes manages distributed workloads across a cluster and maintains their desired state.

## Docker Swarm or Kubernetes?

Docker Swarm is simpler and built into Docker Engine. Kubernetes provides a larger feature set, ecosystem and level of industry adoption.

---

# Summary

- Container orchestration automates workload management.
- It becomes useful when applications run many containers across multiple machines.
- A cluster is a group of connected nodes.
- Scheduling chooses where workloads run.
- Desired state describes the required system.
- Self-healing replaces failed workloads.
- Scaling changes the number of workload replicas.
- Load balancing distributes traffic.
- Rolling updates replace application versions gradually.
- Kubernetes is a widely used orchestration platform.
- Kubernetes manages workloads using objects such as pods, Deployments and Services.
- Docker Swarm is Docker Engine’s built-in orchestration feature.
- Docker Swarm has a simpler initial setup.
- Kubernetes provides more features and a larger ecosystem.
- Docker Compose is well suited to development and smaller single-host applications.
- Not every application requires an orchestration platform.
