---
title: "Kubernetes Namespaces"
date: 2020-06-10T11:54:27+02:00
draft: true
toc: false
description: 
author: loeken
images:
tags:
  - kubernetes
  - k3s
---

## Kubernetes namespaces
Imagine two teams build similar apps running in the same cluster. in order to avoid duplicated names etc and in order to group resources namespaces can be used  to logically separate things.
You could also use it to separate staging/production
You could also use it if you want to run multiple different production environments.
Notes:
 - ConfigMap and Secrets can only be used inside a namespace
 - Namespaces can be used to limit access to namespaces
 - Namespaces can be used to limit resources to namespaces ( cpu / mem / storage )

### the default namespaces
```bash
kubectl get namespaces
NAME                   STATUS   AGE
default                Active   5d14h
kube-system            Active   5d14h
kube-public            Active   5d14h
kube-node-lease        Active   5d14h
kubernetes-dashboard   Active   5d14h
```

### manage namespaces via command line

```bash
kubectl create namespace mynamespace
namespace/mynamespace created

kubectl get namespaces
NAME                   STATUS   AGE
default                Active   5d14h
kube-system            Active   5d14h
kube-public            Active   5d14h
kube-node-lease        Active   5d14h
kubernetes-dashboard   Active   5d14h
mynamespace            Active   6s

kubectl delete namespace mynamespace
namespace "mynamespace" deleted
```

to use namespaces in yaml markup simply add:
```yaml
namespace: mynamespace
```
into the metadata section


there are 3rd party tools that can be used to "permanently switch" to another namespace
```
kubens
```

this can be found in the package kubectx
```bash
sudo apt install kubectx

or

sudo pacaur -S kubectx
```