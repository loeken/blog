---
title: "My road to self hosted kubernetes with k3s - distributed storage with ceph"
date: 2021-04-11T10:43:21+01:00
draft: false
summary: here we ll cover how to setup ceph storage and create a storage class which we can use in other deployments to store data persistent across the nodes
toc: false
author: loeken
images:
tags:
- kubernetes
- k3s
- ceph
---
As usual we start out by taking a peak at the docs: https://rook.github.io/docs/rook/master/ceph-quickstart.html

### dependencies
in order to install this the servers will need lvm2 installed, if you used the ansible playbook from the previous post then you ll already have this package on the k3s servers.

```
apt install -y lvm2
```

### install the operator
```
wget https://raw.githubusercontent.com/rook/rook/master/cluster/examples/kubernetes/ceph/crds.yaml
wget https://raw.githubusercontent.com/rook/rook/master/cluster/examples/kubernetes/ceph/common.yaml
wget https://raw.githubusercontent.com/rook/rook/master/cluster/examples/kubernetes/ceph/operator.yaml
kubectl apply -f crs.yaml common.yaml operator.yaml
```

we now wait for the operator pod to become available
```
kubectl get pods -n rook-ceph
```

###install the cluster

```
wget https://raw.githubusercontent.com/rook/rook/master/cluster/examples/kubernetes/ceph/cluster.yaml
kubectl apply -f cluster.yaml
```

watch pods & wait for them to come online:
```
kubectl -n rook-ceph get pod
```

### access the dashboard
next thing we wanna do is access the build in ceph dashboard which provides great info about the storage/usage you can do so by exporting the password from the secret store and then creating a tunnel to the service

```
kubectl -n rook-ceph get secret rook-ceph-dashboard-password -o jsonpath="{['data']['password']}" | base64 --decode && echo
kubectl -n rook-ceph port-forward service/rook-ceph-mgr-dashboard 8443:8443
```

visit: 

```
https://localhost:8443/#/mgr-modules
```

![](/media/img/ceph-dashboard.png#center)
<style type="text/css">
img[src$='#center']
{
    display: block;
    margin: 0.7rem auto;
}
</style>

note:
if you experiment with rook/ceph make sure to clean your devices and the /var/lib/rook folders for leftovers from the previous test, else you might ruin a beautiful sunday by learning how to debug ceph - which in itself is not bad either ;)

