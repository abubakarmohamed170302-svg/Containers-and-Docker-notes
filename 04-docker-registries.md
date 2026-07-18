# Docker Registries

After building a Docker image, the image initially exists only on the local machine.

To deploy the same image elsewhere, it can be uploaded to a Docker registry.

> A Docker registry is a service used to store and distribute container images.

Registries allow developers, servers and deployment platforms to access the same versioned images.

---

## GitHub Versus a Docker Registry

GitHub and Docker registries store different types of content.

| GitHub | Docker registry |
|---|---|
| Stores source code | Stores built container images |
| Stores files such as `app.py` | Stores packaged applications |
| Stores the Dockerfile | Stores the image built from the Dockerfile |
| Uses `git clone` or `git pull` | Uses `docker pull` |
| Tracks source-code commits | Tracks image tags and digests |

A simple analogy is:

```text
GitHub repository = Recipe and instructions
Container registry = Packaged final product
```

The Dockerfile should normally be kept in the source-code repository. The image produced from it can be stored in a container registry.

---

# Why Container Registries Are Needed

Imagine an application must run on many servers.

Without a registry:

```text
Developer
    |
    v
Manually copies and configures the application on each server
```

This is slow, inconsistent and difficult to maintain.

With a registry:

```text
Developer or CI/CD pipeline
            |
            v
Builds Docker image
            |
            v
Pushes image to registry
            |
            v
Servers pull the same image
            |
            v
Identical application version runs everywhere
```

---

## Benefits of Container Registries

Container registries provide:

- Centralised image storage
- Image sharing
- Image versioning
- Consistent deployments
- Faster server setup
- Integration with CI/CD pipelines
- Access control
- Vulnerability scanning
- Easier rollbacks
- Image lifecycle management

---

# Public and Private Registries

## Public Registry

A public registry or public repository allows images to be downloaded without private access.

Common public images include:

```text
python
nginx
mysql
ubuntu
redis
node
postgres
```

Public images are useful for:

- Base images
- Open-source software
- Public demonstrations
- Reusable development tools

Public images should still be selected carefully. Use trusted publishers, suitable version tags and available security information.

---

## Private Registry

A private registry or repository restricts image access to authorised users and systems.

Companies often use private repositories for:

- Internal APIs
- Customer applications
- Company services
- Proprietary software
- Banking and payment systems
- Private deployment images

Access is controlled through credentials, permissions or cloud identity services.

---

# Docker Hub

Docker Hub is a hosted container-registry service operated by Docker.

It contains public and private image repositories.

Website:

```text
https://hub.docker.com
```

Popular images include:

```text
python
mysql
redis
ubuntu
nginx
node
postgres
```

When a Dockerfile contains:

```dockerfile
FROM python:3.12-slim
```

Docker normally pulls that image from Docker Hub unless another registry is specified or the image already exists locally.

---

## Pulling an Image from Docker Hub

Download the Nginx image:

```bash
docker pull nginx
```

Using an explicit version is normally more predictable:

```bash
docker pull nginx:1.27-alpine
```

Check the locally stored images:

```bash
docker images
```

Run the image:

```bash
docker run -d --name web-server -p 8080:80 nginx:1.27-alpine
```

Open:

```text
http://127.0.0.1:8080
```

---

# Building an Image

Suppose the current project contains:

```text
hello-flask/
├── app.py
├── requirements.txt
└── Dockerfile
```

Build the image:

```bash
docker build -t hello-flask .
```

The image now exists locally:

```bash
docker images hello-flask
```

It cannot be pulled by another machine until it is pushed to a registry.

---

# Image Names and Tags

A registry image reference usually follows this structure:

```text
REGISTRY/NAMESPACE/REPOSITORY:TAG
```

For Docker Hub, the registry hostname can normally be omitted:

```text
USERNAME/REPOSITORY:TAG
```

Example:

```text
username/hello-flask:1.0.0
```

| Part | Example | Meaning |
|---|---|---|
| Registry | Docker Hub default | Storage service |
| Namespace | `username` | User or organisation |
| Repository | `hello-flask` | Image repository |
| Tag | `1.0.0` | Image version |

If no tag is provided, Docker normally uses:

```text
latest
```

`latest` is only a tag name. It does not automatically guarantee that an image is the newest or safest version.

Versioned tags are normally clearer for deployments:

```text
1.0.0
1.1.0
2026-07-18
```

---

# Tagging an Image for Docker Hub

Tag the local image:

```bash
docker tag hello-flask username/hello-flask:1.0.0
```

This does not create another full copy of the image.

It creates another reference to the same image.

Check the tags:

```bash
docker images
```

Both names may show the same image ID:

```text
hello-flask
username/hello-flask
```

This means one image has multiple tags.

---

# Logging In to Docker Hub

Authenticate from the terminal:

```bash
docker login
```

Docker will request the account credentials.

A personal access token should be used when required by the account’s security configuration.

Successful authentication displays:

```text
Login Succeeded
```

Log out when necessary:

```bash
docker logout
```

Credentials and access tokens must never be committed to GitHub.

---

# Pushing an Image to Docker Hub

After authenticating and tagging the image:

```bash
docker push username/hello-flask:1.0.0
```

Docker uploads the image layers that are not already present in the registry.

Another machine can then download the image:

```bash
docker pull username/hello-flask:1.0.0
```

Run it:

```bash
docker run -d \
  --name hello-flask \
  -p 5000:5000 \
  username/hello-flask:1.0.0
```

---

# Docker Hub Workflow

```text
Write application
       |
       v
Create Dockerfile
       |
       v
Build image
       |
       v
Test container
       |
       v
Tag image
       |
       v
Log in to Docker Hub
       |
       v
Push image
       |
       v
Other systems pull and run the image
```

Example commands:

```bash
docker build -t hello-flask .
docker run --rm -p 5000:5000 hello-flask
docker tag hello-flask username/hello-flask:1.0.0
docker login
docker push username/hello-flask:1.0.0
```

---

# Amazon Elastic Container Registry

Amazon Elastic Container Registry, commonly called Amazon ECR, is AWS’s managed container-registry service.

Amazon ECR integrates with services such as:

- AWS Identity and Access Management
- Amazon Elastic Container Service
- Amazon Elastic Kubernetes Service
- AWS Lambda container images
- AWS CodeBuild
- AWS CodePipeline

ECR repositories can be private or public, although private repositories are commonly used for internal applications.

---

## Why Companies Use Amazon ECR

Companies running workloads on AWS may use ECR because it provides:

- IAM-based access control
- Private repositories
- Integration with AWS compute services
- Image vulnerability scanning
- Encryption
- Image lifecycle policies
- Versioned image storage
- Automated deployment support

A common AWS container workflow is:

```text
Developer or CI/CD pipeline
            |
            v
Docker image
            |
            v
Amazon ECR
            |
            v
Amazon ECS or Amazon EKS
            |
            v
Running application
```

---

# ECR Repository Address

An ECR repository URI uses the following format:

```text
AWS_ACCOUNT_ID.dkr.ecr.AWS_REGION.amazonaws.com/REPOSITORY_NAME
```

Example using placeholders:

```text
123456789012.dkr.ecr.eu-west-2.amazonaws.com/hello-flask
```

| Part | Meaning |
|---|---|
| `123456789012` | AWS account ID |
| `eu-west-2` | AWS region |
| `hello-flask` | ECR repository name |

The repository must exist in the correct AWS account and region before an image can be pushed to it.

Do not copy an example account ID into a real command. Use the URI shown by the ECR repository in your own AWS account.

---

# Creating an ECR Repository

An ECR repository can be created through the AWS Management Console:

```text
AWS Management Console
        |
        v
Elastic Container Registry
        |
        v
Repositories
        |
        v
Create repository
```

Example repository name:

```text
hello-flask
```

It can also be created using the AWS CLI:

```bash
aws ecr create-repository \
  --repository-name hello-flask \
  --region eu-west-2
```

The response includes the repository URI required for tagging and pushing the image.

---

# AWS CLI

The AWS Command Line Interface allows commands to be sent to AWS from the terminal.

Check whether it is available:

```bash
aws --version
```

Confirm which identity is currently authenticated:

```bash
aws sts get-caller-identity
```

This displays information such as:

- AWS account ID
- IAM user or role ARN
- Authenticated principal

The AWS CLI can be configured with:

```bash
aws configure
```

It requests:

```text
AWS Access Key ID
AWS Secret Access Key
Default region
Default output format
```

Example region:

```text
eu-west-2
```

Example output format:

```text
json
```

> Long-term access keys should be protected carefully, given only the permissions required and never committed to GitHub. Temporary credentials or IAM roles are preferred where available.

---

# ECR Authentication

Docker must authenticate before it can push to or pull from a private ECR repository.

Use the AWS CLI to request a temporary ECR authentication password:

```bash
aws ecr get-login-password --region AWS_REGION \
  | docker login \
      --username AWS \
      --password-stdin \
      AWS_ACCOUNT_ID.dkr.ecr.AWS_REGION.amazonaws.com
```

Example with placeholders replaced by sample values:

```bash
aws ecr get-login-password --region eu-west-2 \
  | docker login \
      --username AWS \
      --password-stdin \
      123456789012.dkr.ecr.eu-west-2.amazonaws.com
```

A successful login displays:

```text
Login Succeeded
```

The AWS CLI:

1. Authenticates the current AWS identity
2. Requests a temporary ECR password
3. Sends that password to Docker through standard input
4. Allows Docker to authenticate with the ECR registry

The AWS region used for authentication must match the region containing the ECR repository.

---

# Tagging an Image for ECR

Suppose the local image is:

```text
hello-flask:1.0.0
```

Tag it with the full ECR repository URI:

```bash
docker tag hello-flask:1.0.0 \
  AWS_ACCOUNT_ID.dkr.ecr.AWS_REGION.amazonaws.com/hello-flask:1.0.0
```

Example using sample values:

```bash
docker tag hello-flask:1.0.0 \
  123456789012.dkr.ecr.eu-west-2.amazonaws.com/hello-flask:1.0.0
```

Check the image tags:

```bash
docker images
```

The local and ECR tags may have the same image ID because both tags refer to the same local image.

---

# Pushing an Image to ECR

Push the tagged image:

```bash
docker push \
  AWS_ACCOUNT_ID.dkr.ecr.AWS_REGION.amazonaws.com/hello-flask:1.0.0
```

Example:

```bash
docker push \
  123456789012.dkr.ecr.eu-west-2.amazonaws.com/hello-flask:1.0.0
```

The image layers are uploaded to Amazon ECR.

The image can be viewed through:

```text
Amazon ECR
    |
    v
Repositories
    |
    v
hello-flask
    |
    v
Images
```

---

# Pulling an Image from ECR

A different authorised machine must authenticate with the registry:

```bash
aws ecr get-login-password --region eu-west-2 \
  | docker login \
      --username AWS \
      --password-stdin \
      123456789012.dkr.ecr.eu-west-2.amazonaws.com
```

Pull the image:

```bash
docker pull \
  123456789012.dkr.ecr.eu-west-2.amazonaws.com/hello-flask:1.0.0
```

Run the image:

```bash
docker run -d \
  --name hello-flask \
  -p 5000:5000 \
  123456789012.dkr.ecr.eu-west-2.amazonaws.com/hello-flask:1.0.0
```

---

# Complete Amazon ECR Workflow

## 1. Confirm the AWS identity

```bash
aws sts get-caller-identity
```

## 2. Create the ECR repository

```bash
aws ecr create-repository \
  --repository-name hello-flask \
  --region eu-west-2
```

## 3. Build the image

```bash
docker build -t hello-flask:1.0.0 .
```

## 4. Test the image locally

```bash
docker run --rm -p 5000:5000 hello-flask:1.0.0
```

## 5. Log in to ECR

```bash
aws ecr get-login-password --region eu-west-2 \
  | docker login \
      --username AWS \
      --password-stdin \
      123456789012.dkr.ecr.eu-west-2.amazonaws.com
```

## 6. Tag the image

```bash
docker tag hello-flask:1.0.0 \
  123456789012.dkr.ecr.eu-west-2.amazonaws.com/hello-flask:1.0.0
```

## 7. Push the image

```bash
docker push \
  123456789012.dkr.ecr.eu-west-2.amazonaws.com/hello-flask:1.0.0
```

## 8. Pull and run it from an authorised system

```bash
docker pull \
  123456789012.dkr.ecr.eu-west-2.amazonaws.com/hello-flask:1.0.0

docker run -d \
  -p 5000:5000 \
  123456789012.dkr.ecr.eu-west-2.amazonaws.com/hello-flask:1.0.0
```

---

# CI/CD Registry Workflow

In a CI/CD pipeline, the process can be automated:

```text
Code is pushed
      |
      v
Pipeline starts
      |
      v
Application tests run
      |
      v
Docker image is built
      |
      v
Image is tagged
      |
      v
Pipeline authenticates with registry
      |
      v
Image is pushed
      |
      v
Deployment platform pulls image
```

A commit SHA can be used as an image tag:

```text
hello-flask:a1b2c3d
```

This makes it easier to identify which source-code version produced a deployed image.

---

# Troubleshooting Registry Errors

## AWS CLI Command Not Found

Example:

```text
command not found: aws
```

Meaning:

```text
The AWS CLI is not installed or is not available through PATH.
```

Check:

```bash
which aws
aws --version
```

If the command is unavailable, install the AWS CLI using the official instructions for the operating system.

---

## Permission Denied When Running AWS CLI

Example:

```text
permission denied: aws
```

Possible causes include:

- A damaged installation
- Incorrect file permissions
- An incorrect symbolic link
- The wrong executable path
- A mounted filesystem that does not allow execution

Check the resolved executable:

```bash
which aws
ls -l "$(which aws)"
```

A clean reinstall may be required if the installation is incomplete or damaged.

---

## ECR Login Produces an Empty Password

Example:

```text
password is empty
```

The AWS CLI side of the pipe probably failed before producing an ECR password.

Test the AWS command separately:

```bash
aws ecr get-login-password --region eu-west-2
```

Also verify:

```bash
aws --version
aws sts get-caller-identity
```

Possible causes include:

- AWS CLI is not installed correctly
- No credentials are configured
- Credentials have expired
- The region is incorrect
- The AWS identity lacks ECR permissions
- Network access to AWS failed

Do not display or save a successful authentication password.

---

## Invalid or Expired Credentials

Possible errors include:

```text
InvalidClientTokenId
UnrecognizedClientException
ExpiredToken
```

Check the current identity:

```bash
aws sts get-caller-identity
```

Review the configured region and credential source:

```bash
aws configure list
```

The credentials may be incorrect, expired or configured for a different profile.

When using a named profile:

```bash
aws sts get-caller-identity --profile PROFILE_NAME
```

---

## Access Denied

Example:

```text
AccessDeniedException
```

AWS recognised the identity, but it does not have permission to perform the requested action.

The IAM identity may require permissions for operations such as:

- Getting an ECR authentication token
- Checking image layers
- Uploading image layers
- Putting an image
- Downloading image layers
- Reading repository information

Permissions should follow the principle of least privilege.

---

## Repository Not Found

Example:

```text
RepositoryNotFoundException
```

Possible causes include:

- The ECR repository does not exist
- The repository name is misspelled
- The wrong region is being used
- The wrong AWS account ID is in the image URI
- The current credentials belong to another AWS account

Check the current account:

```bash
aws sts get-caller-identity
```

List repositories in the selected region:

```bash
aws ecr describe-repositories --region eu-west-2
```

Confirm that the repository URI exactly matches the value shown by ECR.

---

## `no basic auth credentials`

Example:

```text
no basic auth credentials
```

Docker is not currently authenticated with the registry.

Run the ECR login command again and confirm:

- The account ID is correct
- The region is correct
- The registry hostname is correct
- The AWS credentials are valid

ECR authentication tokens are temporary and eventually require renewal.

---

## Requested Access Is Denied

Example:

```text
requested access to the resource is denied
```

For Docker Hub, check:

- The Docker Hub username
- The repository name
- The image tag
- Whether `docker login` succeeded
- Whether the user can push to that repository

The image name must normally begin with the correct Docker Hub namespace:

```text
username/repository:tag
```

---

## TLS Handshake Timeout

Example:

```text
TLS handshake timeout
```

Docker could not complete a secure connection to the registry.

Possible causes include:

- Unstable internet connection
- DNS problems
- Firewall restrictions
- VPN or proxy issues
- Temporary registry problems
- Slow network connection

Useful checks include:

```bash
docker info
curl -I https://hub.docker.com
```

Retry after confirming the network connection.

---

## Push Uses the Wrong Repository or Region

Inspect the complete image name:

```bash
docker images
```

An ECR image must use the correct structure:

```text
AWS_ACCOUNT_ID.dkr.ecr.AWS_REGION.amazonaws.com/REPOSITORY:TAG
```

If the local tag is wrong, create the correct tag:

```bash
docker tag SOURCE_IMAGE:TAG CORRECT_ECR_URI:TAG
```

Then push the corrected reference.

---

# Useful Registry Commands

## Pull an image

```bash
docker pull IMAGE_NAME:TAG
```

## Tag an image

```bash
docker tag SOURCE_IMAGE:TAG TARGET_IMAGE:TAG
```

## Push an image

```bash
docker push IMAGE_NAME:TAG
```

## Log in to Docker Hub

```bash
docker login
```

## Log out of Docker Hub

```bash
docker logout
```

## Log in to ECR

```bash
aws ecr get-login-password --region AWS_REGION \
  | docker login \
      --username AWS \
      --password-stdin \
      AWS_ACCOUNT_ID.dkr.ecr.AWS_REGION.amazonaws.com
```

## List ECR repositories

```bash
aws ecr describe-repositories --region AWS_REGION
```

## List images in an ECR repository

```bash
aws ecr list-images \
  --repository-name REPOSITORY_NAME \
  --region AWS_REGION
```

## Confirm the AWS identity

```bash
aws sts get-caller-identity
```

---

# Common Interview Questions

## What is a container registry?

A container registry is a service used to store, version and distribute container images.

## What is the difference between GitHub and a container registry?

GitHub normally stores source code and build instructions. A container registry stores the built images produced from that source code.

## Why must an image be tagged before it is pushed?

The full tag identifies the target registry, namespace, repository and image version.

## What is Amazon ECR?

Amazon ECR is AWS’s managed container-registry service. It integrates with IAM and AWS container deployment services.

## Why does ECR require the AWS CLI login command?

The AWS CLI uses the current AWS identity to obtain a temporary registry password, which is passed securely to Docker through standard input.

## Can one Docker image have multiple tags?

Yes. Multiple tags can refer to the same image ID.

## Is `latest` always the newest image?

No. `latest` is an ordinary tag name and only points to whichever image was assigned that tag.

## Why use versioned image tags?

Versioned tags make deployments more predictable and allow teams to identify or restore specific application versions.

---

# Summary

- A container registry stores and distributes container images.
- GitHub normally stores source code, while registries store built images.
- Registries support consistent deployments and CI/CD automation.
- Docker Hub provides public and private image repositories.
- Amazon ECR is AWS’s managed container-registry service.
- An image must be correctly tagged before it is pushed.
- One Docker image can have multiple tags.
- `latest` is a normal tag and does not guarantee freshness.
- Docker Hub uses `docker login` for authentication.
- Private ECR repositories use AWS identity and temporary authentication.
- The ECR account ID, region and repository name must all be correct.
- Credentials, tokens and passwords must never be committed to GitHub.
- Logs and identity checks should be used when registry operations fail.
