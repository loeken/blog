---
title: "My road to self hosted kubernetes with k3s"
date: 2021-03-27T00:28:41+01:00
draft: false
toc: false
summary: this is a farytale from a devops engineer from Berlin
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

Over the last years ive started to embrace the docker & kubernetes ecosystem. this post links to a bunch of other posts that log will act as a sort of reference on how to create a poor man's cluster on ovh. In contrast to the big cloud providers ovh delivers a cheap (fixed costs per month - at least for the majority of things ) - in a nutshell my plan is to spin up 3 vms with ~ 4GB of ram each in 3 different geographic locations, combine that with ovh's block storage (which you can setup snapshots for too ) and we'll have a cluster for less then 30EUR/month with ~ 9GB of usable ram. we can scale up these instances to 8GB of ram each and also add more instances to the cluster ( scale horizontally ). we are not going to use managed load balancers but we are going to expose applications by using an nginx ingress on the nodes directly.

If you'd need a bit more umpf you could also get dedicated servers from ovh. ovh also does offer a managed kubernetes environment but the nodes start at roughly 25eur for 7GB of ram ( control plane free ), given that i ll have more redundancy with 3 smaller nodes and i ll get more cpu bang for the buck i ve decided to go with the ovh cloud instances instead.

We also want to plan ahead, if we setup 1 cluster we most likely will end up setting up more and more clusters. This is why we want to build a small CI pipeline so we can save our build recipes to git repositories and use argocd to ensure the clusters run - what we want them to run.


<hr>

## 0.1 this article series
This article is written in simple markdown syntax ( articles can be found: https://github.com/loeken/blog/tree/master/content/posts ) I then use hugo to genearte html and netlify to serve these files. Long story short: "If you spot any mistake in these articles scroll down and click on 'improve this page', that way you can create a PR on the github repo and correct what you think is wrong and after approval I can merge it into my master and publish the updated version easily".
[read blogposts about how to edit this blog's content ](/posts/contribute-to-this-blog/)

<hr>

## 1.1 minikube
##### Introduction
Minikube is an easy way for running kubernetes locally. in 1.5 we'll setup argocd - we could run that in the cluster but "waste" resources. I tend to run argocd locally so in case something is wrong with my cluster/some cloud i could reswapn applications in another cluster
##### Article Link
[read full article chapter 1.1 ](/posts/my-road-to-self-hosted-kubernetes-with-k3s_minikube)

##### Resources & Links
- minikube https://kubernetes.io/de/docs/setup/minikube/

<hr>

## 1.2 kubectl
##### Introduction
Kubectl is a command line client that allows us to control multiple kubernetes clusters (k3s/k8s) it does this by calling the kubernetes endpoints and providing a set of certificate/keys to authenticate.
##### Article Link
[read full article chapter 1.2 ](/posts/my-road-to-self-hosted-kubernetes-with-k3s_kubectl)

##### Resources & Links
- kubectl https://kubernetes.io/docs/tasks/tools/

<hr>

## 1.3 bootstrap k3s cluster with k3sup & ansible

##### Introduction
In this article we are going to setup k3s on 3 servers, we ll be using k3sup to do most of the work and trigger the setup by using an ansible playbook.
##### Article Link
[read full article chapter 1.1 ](/posts/my-road-to-self-hosted-kubernetes-with-k3s_bootstrap-cluster-using-ansible-and-k3sup/)

##### Resources & Links
- k3s - v1.20.5-rc1+k3s1 - https://github.com/k3s-io/k3s/tags
- k3sup - https://github.com/alexellis/k3sup
- ansible - https://ansible.com

<hr>

## 1.4 contineous integration with argocd
##### Introduction
In this article we are going to setup argocd in minikube, argocd will be the tool that we use to apply configuration changes to our kubernetes yaml files.
##### Article Link
[read full article chapter 1.5 ](/posts/my-road-to-self-hosted-kubernetes-with-k3s_argocd/)

##### Resources & Links
- https://argoproj.github.io/argo-cd
- https://argoproj.github.io/argo-cd/getting_started/

<hr>

## 1.5 distributed storage with ceph

<hr>

## 1.6 user permission management ( maybe with argo? )

<hr>

## 1.7 ( logging with EFK )

<hr>

## 1.8 cert-manager

<hr>

## 1.9 external-dns

<hr>

## 1.10 nginx ingress

<hr>

## 1.11 hashicorp vault - secret management

<hr>

## 1.12 postgresql ha helm chart

<hr>

## 1.13 linkerd service mesh

<hr>

## 1.14 mysql alpine deployment

