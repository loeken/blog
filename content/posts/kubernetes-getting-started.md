---
title: "Kubernetes Getting Started"
date: 2020-06-07T18:19:55+02:00
draft: true
toc: false
description: 
author: loeken
images:
tags:
  - kubernetes
  - docker
---

# Kubernetes
![](/media/img/kubernetes_getting_started.png)
[Download Image Markup](/media/imgmarkup/kubernetes-getting-started.py)
all following tutorials are done with k3s version:
k3s version v1.17.2+k3s1 (cdab19b0)

## Node
### Worker Node
A server - a physical or virtual machine. pods are running here.
https://stackoverflow.com/questions/21889053/what-is-the-runtime-performance-cost-of-a-docker-container

### Master Node
Manages Pods on all Worker and Master nodes

## Pod
Abstraction ontop of a docker container. Creates running environment. Abstracting away the runtime/technology ( replace docker/containerd etc )
expect pods to be ephemeral.

## Service/Network
each pod gets a virtual ip / internal ip. on the base of pods being ephemeral use dns within the code.
Service is running on it's own not part of Pod
Acts similar to Load Balancer in front of Pod

## External Service
a service that opens communication from external sources ( frontend vms ).

Service Type: LoadBalancer

## Internal Service
for communication between services interally

Service Type: ClusterIP

## Ingress
preferred production communication from the outside world that are reaching pods via services.
- can update public ips of loadbalancers/NodeIps with external-dns to services like azure/gcp/cloudflare
- can create letsencrypt certificates for ssl termination with cert-managere

## ConfigMap
contains confiruation data like
POSTGRESQL_USER=postgres
Pods read from configMap. this is ideal for config updates without having to build a new image and redeploy.


## Secret
similar to ConfigMap
base64 encoded
```bash
echo -n 'topsecret' | base64
dG9wc2VjcmV0
```
for storing passwords


## Volumes
Pods being ephemeral you want your data persistent, by using volumes 
Volumes are local or remote storage devices.


## Replication
clones of pods running on different Worker Nodes.

## Deployment
an abstraction layer that defines the creation of pods but also includes replication for convenient scaling/updates.
this way you can run containers on multiple workers improving the overall uptime.

Stateful pods such as databases are not managed via deployments.

## StatefulSet 
Similar to Deployment but this is used for stateful pods ( postgresql/redis/mongodb/mysql ... )
