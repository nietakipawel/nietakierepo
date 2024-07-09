# GitHub Branch & Pull Request Operator
This Kubernetes operator automates the process of creating branches and pull requests on a specified GitHub repository based on custom resource definitions (CRDs).

## Features
- Create a new branch in a GitHub repository.
- Commit a file to the new branch.
- Create a pull request from the new branch to the main branch.

## Prerequisites
- Kubernetes cluster
- kubectl configured to interact with your cluster.
- Docker installed and configured to push images to Docker Hub.
- A GitHub account with a personal access token (PAT) that has the repo scope.

## Setup&use
1. Update [Base64 encode your GitHub PAT](github-secret.yaml)
2. Update
- [rbac.yaml](./rbac.yaml)
- [crd.yaml](./crd.yaml)
- [operator.py](./operator.py)
- [operator.yaml](./operator.yaml)
3. Build docker image
- update [Dockerfile](./Dockerfile)
- build&deploy
```bash
docker build -t your-docker-image .
docker tag your-docker-image your-dockerhub-username/your-docker-image:latest
docker push your-dockerhub-username/your-docker-image:latest
```

3. Apply
```yaml
kubectl apply -f github-secret.yaml
kubectl apply -f rbac.yaml
kubectl apply -f operator.yaml
```
4. Use
- update [example.yaml](./example.yaml)
- apply
```
kubectl apply -f example.yaml
```