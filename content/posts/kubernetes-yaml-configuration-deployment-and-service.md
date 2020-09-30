---
title: "Kubernetes Yaml Configuration Deployment and Service"
date: 2020-06-08T13:31:40+02:00
draft: true
toc: false
description: 
author: loeken
images:
tags:
  - untagged
---

## Deployment & Service Configuration
<style type="text/css">
.flex { 
    display: flex; 
    justify-content: center; 
    align-items: center;
}
</style>
<div class="flex">

![](/media/img/kubernetes_configuration_files.png)

</div>

[Download Image Markup](/media/imgmarkup/kubernetes-configuration_files.py)

Connecting Deployments with Services and Pods. Every configuration in k3s has 3 types
- metadata
- spec
- status ( created/managed by k8/3s - differntiating between desired and actual state )

the current status is held by the k3s cluster.
the attributes of each of those 3 type have different options


### example for deployment
#### **`nginx-deployment.yaml`**
```
apiVersion: apps/v1
#  kind defines the type
kind: Deployment
# this is the metadata section
metadata:
  name: nginx-deployment
  labels:
    # here we define a key/value pair this has to match the selector below services also reference this label
    app: nginx
# this is the spec section
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  # the following part is basically a configuration file inside a configuration file ( has its own metadata/spec sections )
  # this is bascially the part of the configuration file that defines the pod 
  template:
    metadata:
      # same functionality as with the label above
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.14.2
        ports:
        - containerPort: 80
# once deployed a status section would be added here#

```

### example for service
#### **`nginx-service.yaml`**
```
kind: Service
apiVersion: v1
metadata:
  name: "nginx"
spec:
  selector:
    app: "nginx"
  ports:
    - protocol: "TCP"
      port: 1337
      targetPort: 80
  type: LoadBalancer
```

note: The suggested syntax for YAML files is to use 2 spaces for indentation

now save these on a k3s cluster/server and apply

```
kubectl apply -f nginx-deployment.yaml
kubectl apply -f nginx-service.yaml
```

now verify that all has been applied properly
```
kubectl get deployments
NAME               READY   UP-TO-DATE   AVAILABLE   AGE
nginx-deployment   3/3     3            3           6m30s

kubectl get services
NAME         TYPE           CLUSTER-IP     EXTERNAL-IP   PORT(S)          AGE
kubernetes   ClusterIP      10.43.0.1      <none>        443/TCP          3d16h
nginx        LoadBalancer   10.43.37.195   10.0.4.83     1337:31795/TCP   6m16s

kubectl describe service nginx
Name:                     nginx
Namespace:                default
Labels:                   <none>
Annotations:              kubectl.kubernetes.io/last-applied-configuration:
                            {"apiVersion":"v1","kind":"Service","metadata":{"annotations":{},"name":"nginx","namespace":"default"},"spec":{"ports":[{"port":1337,"prot...
Selector:                 app=nginx
Type:                     LoadBalancer
IP:                       10.43.37.195
LoadBalancer Ingress:     10.0.4.83
Port:                     <unset>  1337/TCP
TargetPort:               80/TCP
NodePort:                 <unset>  31795/TCP
Endpoints:                10.42.0.9:80,10.42.1.5:80,10.42.2.5:80
Session Affinity:         None
External Traffic Policy:  Cluster
Events:                   <none>
```