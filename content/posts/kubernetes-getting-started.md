---
title: "Kubernetes Getting Started"
date: 2020-06-07T18:19:55+02:00
draft: true
toc: false
description: 
author: loeken
summary: an introduction into kubernetes and the most commonly used components
images:
tags:
  - kubernetes
  - docker
---

# Kubernetes getting started

kubernetes - a tool for managing and automating containerized workloads in the cloud

simply put: you define the desired state of your application and kubernetes ensures that all parts of your application are in the desired state.

it do this work across multiple machines ( nodes ) that together form a kubernetes cluster it can autoscale and autoheal ( add nodes / replace nodes )

the heart of kubernetes is known as "the control plane" - which is an api endpoint which can be called internally/externally  to manage the cluster and all resources of it. it also contains a datastore ( most commonly etcd ) which it uses to store information about the cluster.

there are two types of nodes that can be part of the cluster:
- master nodes: run the control plane api endpoint
- worker nodes: run containers

each node runs kubelet - an application with a small footprint that communicates with the control plane

then next to kubelet we also have pods - which are the smallest deployable unit - you can think of a pod as a pod of whales ( each whale being one of the containers, which in turn form the pod ).

as the workload of the containers increase kubernetes can scale horizontally by adding more worker nodes and then running more containers on this new hardware that we added.

kubernets also takes care of networking between the containers, secret management, persistent storage for the containers. 

It has been designed for high availability - which is mostly achived by keeping replica sets - for example an nginx deployment which has a replica set of 3 - so we always have 3 containers running and no downtime if one of the containers go down.

<div class="flex">

![](/media/img/kubernetes_getting_started.png)

</div>
[Download Image Markup](/media/imgmarkup/kubernetes-getting-started.py)

all following tutorials are done with k3s version: v1.19

## Terminology
### Node
#### Worker Node
A server - a physical or virtual machine. pods are running here.
https://stackoverflow.com/questions/21889053/what-is-the-runtime-performance-cost-of-a-docker-container

### Master Node
Manages Pods on all Worker and Master nodes

### Pod
Abstraction ontop of a docker container. Creates running environment. Abstracting away the runtime/technology ( replace docker/containerd etc )
expect pods to be ephemeral.
```
apiVersion: v1
kind: Pod
metadata:
  name: static-web
  labels:
    role: myrole
spec:
  containers:
    - name: web
      image: nginx
      ports:
        - name: web
          containerPort: 80
          protocol: TCP
```

### Service/Network
each pod gets a virtual ip / internal ip. on the base of pods being ephemeral use dns within the code.
Service is running on it's own not part of Pod
Acts similar to Load Balancer in front of Pod
```
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  selector:
    app: MyApp
  ports:
    - protocol: TCP
      port: 80
      targetPort: 9376
```

### External Service
a service that opens communication from external sources ( frontend vms ).

Service Type: LoadBalancer
```
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  selector:
    app: MyApp
  type: LoadBalancer
  ports:
    - protocol: TCP
      port: 80
      targetPort: 9376
```

### Internal Servicee
for communication between services interally

Service Type: ClusterIP
```
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  selector:
    app: MyApp
  type: ClusterIP
  ports:
    - protocol: TCP
      port: 80
      targetPort: 9376
```

### Ingress
preferred production communication from the outside world that are reaching pods via services.
```
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: minimal-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - http:
      paths:
      - path: /testpath
        pathType: Prefix
        backend:
          service:
            name: test
            port:
              number: 80
```

- can update public ips of loadbalancers/NodeIps with external-dns to services like azure/gcp/cloudflare
- can create letsencrypt certificates for ssl termination with cert-manager

### ConfigMap
contains configuration ( environment variables ) data like
POSTGRESQL_USER=postgres
Pods read from configMap. this is ideal for config updates without having to build a new image and redeploy.
```
apiVersion: v1
kind: ConfigMap
metadata:
  creationTimestamp: 2017-12-27T18:36:28Z
  name: game-config-env-file
  namespace: default
  resourceVersion: "809965"
  uid: d9d1ca5b-eb34-11e7-887b-42010a8002b8
data:
  allowed: '"true"'
  enemies: aliens
  lives: "3
```

### Secret
similar to ConfigMap for storing passwords ( encrypted at rest )

```
apiVersion: v1
data:
  username: YWRtaW4=
  password: MWYyZDFlMmU2N2Rm
kind: Secret
metadata:
  name: mysecret
  namespace: default
type: Opaque
```

```
echo -n 'topsecret' | base64
dG9wc2VjcmV0
```

### Volumes
Pods being ephemeral you want your data persistent, by using volumes 
Volumes are local or remote storage devices.
```
apiVersion: v1
kind: Pod
metadata:
  name: configmap-pod
spec:
  containers:
    - name: test
      image: busybox
      volumeMounts:
        - name: config-vol
          mountPath: /etc/config
  volumes:
    - name: config-vol
      configMap:
        name: log-config
        items:
          - key: log_level
            path: log_level
```

### Deployment
an abstraction layer that defines the creation of pods but also includes replication for convenient scaling/updates.
this way you can run containers on multiple workers improving the overall uptime.

Stateful pods such as databases are not managed via deployments.
```
apiVersion: v1
kind: Deployment
metadata:
  name: static-web
  labels:
    role: myrole
spec:
  containers:
    - name: web
      image: nginx
      ports:
        - name: web
          containerPort: 80
          protocol: TCP
```

### Replication
clones of pods running on different Worker Nodes.
```
apiVersion: v1
kind: Deployment
metadata:
  name: static-web
  labels:
    role: myrole
spec:
  replicas: 2
  containers:
    - name: web
      image: nginx
      ports:
        - name: web
          containerPort: 80
          protocol: TCP
```

### StatefulSet 
Similar to Deployment but this is used for stateful pods ( postgresql/redis/mongodb/mysql ... )
```
apiVersion: v1
kind: Service
metadata:
  name: nginx
  labels:
    app: nginx
spec:
  ports:
  - port: 80
    name: web
  clusterIP: None
  selector:
    app: nginx
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: web
spec:
  serviceName: "nginx"
  replicas: 2
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: k8s.gcr.io/nginx-slim:0.8
        ports:
        - containerPort: 80
          name: web
        volumeMounts:
        - name: www
          mountPath: /usr/share/nginx/html
  volumeClaimTemplates:
  - metadata:
      name: www
    spec:
      accessModes: [ "ReadWriteOnce" ]
      resources:
        requests:
          storage: 1Gi
```

<style type="text/css">
.flex { 
    display: flex; 
    justify-content: center; 
    align-items: center;
}
</style>