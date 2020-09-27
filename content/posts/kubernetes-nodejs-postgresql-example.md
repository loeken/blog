---
title: "Kubernetes Nodejs Postgresql Example"
date: 2020-06-09T13:50:41+02:00
draft: true
toc: false
description: 
author: loeken
images:
tags:
  - kubernetes
---

## Deployment example with nodejs / postgresql

![](/media/img/kubernetes_deployment_nodejs_postgresql.png)
[Download Image Markup](/media/imgmarkup/kubernetes-deployment-nodejs-postgresql.py)

In this demo example we'll be deploying the app from  [the previous docker example](/posts/docker-nodejs-postgresql-example/) which consists of one node and one postgresql container.
In the docker example we used a hardcoded username/password combination - which is bad practise: this time we ll be working cleaner by moving the username/password for PG into environmental variables
We are going to create a deployment that uses a Secret and a ConfigMap to define values for these 2 environmental variables.
We ll create an external service for the nodejs instance and create an internal service for the postgresql server.
So users coming from the "Internet" will only be able to access the External Service.

#### Creating a configMap

#### Creating a secret
```bash
echo -n "postgresql" | base64                                                                                                                                         0.01   21:45  
cG9zdGdyZXNxbA==

echo -n "topsecure" | base64                                                                                                                                          0.00   21:45  
dG9wc2VjdXJl

```

#### **`postgres-secret.yaml`**
```yaml
apiVersion: v1
kind: Secret
metadata:
    name: postgres-secret
type: Opaque
data:
    postgres-user: cG9zdGdyZXNxbA==
    postgres-password: dG9wc2VjdXJl
```
#### **`postgres-configmap.yaml`**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
    name: postgres-configmap
data:
    postgres-host: postgres-service:5432
    postgres-dbname: api
```

apply configuration
```bash
kubectl apply -f postgres-secret.yaml
kubectl apply -f postgres-configmap.yaml

kubectl get pods
NAME                        READY   STATUS    RESTARTS   AGE
postgres-784d9d978c-f67gs   1/1     Running   0          57s
root@k3s-01:~/demo_nodejs_pg# kubectl get service
NAME               TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
kubernetes         ClusterIP   10.43.0.1       <none>        443/TCP    4d1h
postgres-service   ClusterIP   10.43.122.189   <none>        5432/TCP   60s

kubectl describe service postgres-service
Name:              postgres-service
Namespace:         default
Labels:            <none>
Annotations:       kubectl.kubernetes.io/last-applied-configuration:
                     {"apiVersion":"v1","kind":"Service","metadata":{"annotations":{},"name":"postgres-service","namespace":"default"},"spec":{"ports":[{"port"...
Selector:          app=postgres
Type:              ClusterIP
IP:                10.43.122.189
Port:              <unset>  5432/TCP
TargetPort:        5432/TCP
Endpoints:         10.42.1.9:5432
Session Affinity:  None
Events:            <none>

kubectl get pod -o wide
NAME                        READY   STATUS    RESTARTS   AGE     IP          NODE     NOMINATED NODE   READINESS GATES
postgres-784d9d978c-f67gs   1/1     Running   0          5m22s   10.42.1.9   k3s-02   <none>           <none>
```


## postgres deployment
#### **`postgres-deployment.yaml`**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
  labels:
    app: postgres
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:latest
        ports:
        - containerPort: 80
        env:
        - name: POSTGRES_USER
          valueFrom:
            secretKeyRef:
              name: postgres-secret
              key: postgres-user
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: postgres-secret
              key: postgres-password
        - name: POSTGRES_HOST
          valueFrom:
            configMapKeyRef:
              name: postgres-configmap
              key: postgres-host
        - name: POSTGRES_DBNAME
          valueFrom:
            configMapKeyRef:
              name: postgres-configmap
              key: postgres-dbname
---
apiVersion: v1
kind: Service
metadata:
  name: postgres-service
spec:
  selector:
    app: postgres
  type: ClusterIP
  ports:
    - protocol: TCP
      port: 5432
      targetPort: 5432
```

## node deployment
#### **`node-deployment.yaml`**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: node
  labels:
    app: node
spec:
  replicas: 1
  selector:
    matchLabels:
      app: node
  template:
    metadata:
      labels:
        app: node
    spec:
      containers:
      - name: node
        image: demoregistry.azurecr.io/node:1.0.0
        imagePullPolicy: Always
        ports:
        - containerPort: 1337
        env:
        - name: POSTGRES_USER
          valueFrom:
            secretKeyRef:
              name: postgres-secret
              key: postgres-user
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: postgres-secret
              key: postgres-password
        - name: POSTGRES_HOST
          valueFrom:
            configMapKeyRef:
              name: postgres-configmap
              key: postgres-host
        - name: POSTGRES_DBNAME
          valueFrom:
            configMapKeyRef:
              name: postgres-configmap
              key: postgres-dbname
      imagePullSecrets:
        - name: regcred
---
apiVersion: v1
kind: Service
metadata:
  name: node-service
spec:
  selector:
    app: node
  type: LoadBalancer
  ports:
    - protocol: TCP
      port: 1337
      targetPort: 1337
      nodePort: 30000
```