---
title: "Kubernetes Create Images in Azure Container Registry"
date: 2020-06-09T12:55:48+02:00
draft: false
toc: false
description: 
author: loeken
images:
tags:
  - kubernetes
  - registry
  - k3s
---

## Creating a Container registry @ azure 

For this we'll be using the azure container registry, alternatively you can use docker.io or google/aws based services.

I will name my registry demoregistry
[this guide will get you started](https://docs.microsoft.com/en-us/azure/container-registry/container-registry-get-started-portal)

### dependencies for azure registry:

now we login via the azure cli
```bash
pacaur -S azure-cli
az login
az acr login --name demoregistry
```
after the az login it will show 

now let's package up the node app
```bash
cd ~/Projects
git clone https://github.com/loeken/kubernetes_nodejs_postgresql_demo
cd kubernetes_nodejs_postgresql_demo

docker build -t kubernetes_nodejs_postgresql_demo:latest .                                                                                                                                            0.00   22:28  
Sending build context to Docker daemon  914.9kB
Step 1/7 : FROM node:alpine
alpine: Pulling from library/node
cbdbe7a5bc2a: Pull complete 
fb0e3739aee1: Pull complete 
738de7869598: Pull complete 
ffd68be3d86c: Pull complete 
Digest: sha256:7d11fea6d901bfe59999dda0fa3514438628a134d43c27c2eaec43cc8f4b98d5
Status: Downloaded newer image for node:alpine
 ---> 3bf5a7d41d77
Step 2/7 : WORKDIR /usr/src/app
 ---> Running in b35c1c830dd5
Removing intermediate container b35c1c830dd5
 ---> 72b783d36c39
Step 3/7 : COPY package*.json ./
 ---> 19e398b02edd
Step 4/7 : RUN npm install
 ---> Running in 14c532d4db10
added 17 packages from 9 contributors and audited 17 packages in 1.02s
found 0 vulnerabilities

Removing intermediate container 14c532d4db10
 ---> 215e96a458b4
Step 5/7 : COPY . .
 ---> e3337bb735e9
Step 6/7 : EXPOSE 1337
 ---> Running in fef14992b60f
Removing intermediate container fef14992b60f
 ---> 2efacffecc53
Step 7/7 : CMD [ "node", "server.js" ]
 ---> Running in ed0ccc95fd1f
Removing intermediate container ed0ccc95fd1f
 ---> 693448b5fc7b
Successfully built 693448b5fc7b
Successfully tagged kubernetes_nodejs_postgresql_demo:latest

docker images
REPOSITORY                          TAG                 IMAGE ID            CREATED             SIZE
kubernetes_nodejs_postgresql_demo   latest              693448b5fc7b        4 seconds ago       118MB
postgres                            latest              b97bae343e06        4 hours ago         313MB
node                                alpine              3bf5a7d41d77        6 days ago          117MB
docker tag 3bf5a7d41d77
docker images | head -2 | tail -1 | awk '{print $3}'
693448b5fc7b
docker tag 693448b5fc7b demoregistry.azurecr.io/node:1.0.0
docker push demoregistry.azurecr.io/node:1.0.0  

```


The <SUBSCRIPTION_ID> is returned after az login as "id" in the response array.
For <RG_NAME> enter the resource you used when creating the registry.
The <REGISTRY_NAME> is the name of the registry.

Not that i am createing a "Reader" here as in most production environments you want to only pull from within the k3s cluster
- Owner: (pull, push, and assign roles to other users)
- Contributor: (pull and push)
- Reader: (pull only access)

```bash
az ad sp create-for-rbac \
  --scopes /subscriptions/<SUBSCRIPTION_ID>/resourcegroups/<RG_NAME>/providers/Microsoft.ContainerRegistry/registries/<REGISTRY_NAME> \
  --role Reader \
  --name registry
Changing "registry" to a valid URI of "http://registry", which is the required format used for service principal names
Creating a role assignment under the scope of "/subscriptions/<SUBSCRIPTION_ID>/resourcegroups/<RG_NAME>/providers/Microsoft.ContainerRegistry/registries/<REGISTRY_NAME>"
{
  "appId": "asdfg",
  "displayName": "registry",
  "name": "http://registry",
  "password": "TOPSECRET",
  "tenant": "TENANT_ID"
}
```

```bash
kubectl create secret docker-registry regcred \
  --docker-server demoregistry.azurecr.io \
  --docker-email azure@demoregistry.com \
  --docker-username=asdfg \
  --docker-password TOPSECRET
```