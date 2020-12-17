---
title: "My road to self hosted Kubernetes with k3s"
date: 2020-12-05T20:39:41+01:00
draft: false
toc: false
summary: this is the main post of a series of posts that has a log of the process from moving 300 vms from a proxmox cluster into a k3s environment.
author: loeken
images:
tags:
  - kubernetes
  - k3s
  - debian 10
  - ansible
  - k3sup
---

## 0. introduction

This post will be the structure of a series of posts that will act as a log to my job of migrating roughly 300 vms from a proxmox cluster to a k3s environment. I will try to keep a log of the steps, the gottchas, what I learned etc.

## 0.1 the starting point
![](/media/img/proxmox_cluster.png#center)
<style type="text/css">
img[src$='#center']
{
    display: block;
    margin: 0.7rem auto;
}
</style>

For the last 3 years this Proxmox Cluster has done a great job ( and saved us quite some money ). When we built that cluster kubernetes wasn't what it was today ( or at least it wasn't percevied as that by us :) ) - but a lot happens in three years. I for example changed my local dev workflow a bit and started using containers more ( as a qubes user i was used to qube's vm eco system ), which lead me to experiment with kubernetes ( k3s in particular ).... a few months later - and loads of reading/testing/repeating - I have now started to enjoy the benefits kubernetes ( and the docker / helm ecosystem ) brings me - and i would like to share them with the other users of this cluster ( the actual developers maintaining the applications on that are running on this proxmox cluster ).

## 0.2 this article series
This article is written in simple markdown syntax ( articles can be found: https://github.com/loeken/blog/tree/master/content/posts ) I then use hugo to genearte html and netlify to serve these files. Long story short: "If you spot any mistake in these articles scroll down and click on 'improve this page', that way you can create a PR on the github repo and correct what you think is wrong and after approval I can merge it into my master and publish the updated version easily".


## 1. the planned stack

### 1.1 orchestration

- k3s - v1.19.4-rc2+k3s2 - https://github.com/k3s-io/k3s/tags
- k3sup - https://github.com/alexellis/k3sup
- ansible - https://ansible.com

### 1.2 service mesh

linkerd - https://linkderd.io

### 1.3 storage

rook.io ceph - https://github.com/rook/rook

### 1.4 secret management

hashicorp vault - https://github.com/hashicorp/vault

### 1.5 user management

permission manager - https://github.com/sighupio/permission-manager

### 1.6 logging
https://blog.internetz.me/posts/my-road-to-self-hosted-kubernetes-with-k3s_logging-with-EFK

EFK ( elasticsearch Fluentd Kibana) 
  - https://artifacthub.io/packages/helm/t3n/elasticsearch 
  - https://artifacthub.io/packages/helm/bitnami/fluentd 
  - https://artifacthub.io/packages/helm/bitnami/kibana

### 1.7 databases

- postgresql ( cluster ) - https://bitnami.com/stack/postgresql-ha/containers
- redis ( cluster ) - https://bitnami.com/stack/redis-cluster/helm

### 1.8 message systems

nsqd ( cluster )

### 1.9 helpers

- cert-manager - https://cert-manager.io/docs/installation/kubernetes/
- external-dns - https://github.com/kubernetes-sigs/external-dns

### 1.10 ingress

nginx-ingress - https://github.com/kubernetes/ingress-nginx

### 1.11 applications

- nodejs ( various different services - frontends / backends )
- golang ( various different services - frontends / backends )

## 2 the journey begins

### 2.1 base installation of debian 10 64 + k3s

https://blog.internetz.me/posts/setup_k3s_cluster_on_debian10_using_ansible_and_k3sup/


### 2.2 linkerd service mesh
posts/my-road-to-self-hosted-kubernetes-with-k3s_linkerd-service-mesh/

### 2.3 storage

https://blog.internetz.me/posts/my-road-to-self-hosted-kubernetes-with-k3s_distributed-storage-with-ceph

### 2.4 secret management
https://blog.internetz.me/posts/my-road-to-self-hosted-kubernetes-with-k3s_hasicorp-vault

### 2.5 user management

Permission manager
awaiting merge @ https://github.com/sighupio/permission-manager/pull/44

### 2.6 EFK
https://blog.internetz.me/posts/my-road-to-self-hosted-kubernetes-with-k3s_logging-with-efk


### 2.7 Databases
https://blog.internetz.me/posts/my-road-to-self-hosted-kubernetes-with-k3s_ha-postgresql-cluster-using-helm-chart


sources:
https://rook.github.io/docs/rook/master/ceph-quickstart.html