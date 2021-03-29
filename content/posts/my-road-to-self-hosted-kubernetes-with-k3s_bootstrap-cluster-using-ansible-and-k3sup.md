---
title: "Bootstrap k3s Cluster using ansible and k3sup on debian 10"
date: 2021-03-28T10:15:08+01:00
draft: false
summary: In this article we are going to setup k3s on 3 dedicated servers, we ll be using k3sup to do most of the work and trigger the setup by using an ansible playbook
author: loeken
images:
tags:
  - kubernetes
  - k3s
  - debian 10
  - ansible
  - k3sup
---
## the kubernetes cluster

![TestCluster Layout](/media/img/components-of-kubernetes.svg)

A kubernetes cluster consists of 1 or more nodes, a production cluster usually has as least 3 nodes. There are 2 major types of nodes
#### master nodes
The master nodes are also known as <i>control plane</i>, which manages the worker nodes and the Pods in the cluster. In production environments, the control plane usually runs across multiple servers and a cluster usually runs multiple master(at least 3)/worker nodes, providing fault-tolerance and high availability.

#### worker nodes
The worker node(s) host the Pods that are the components of the application workload. While the master nodes run etcd and schedulers the worker nodes only run the actual pods - and their dependencies.

More info can be found on kubernetes docs: https://kubernetes.io/docs/concepts/overview/components/

<div class="row">
<div class="col-sm-6">

![TestCluster Layout](/media/img/k3s_testlab_02.png)

</div>
<div class="col-sm-6">

## planned setup

##### vps
so for the test cluster i ll be using 3 vps ( https://www.ovhcloud.com/de/public-cloud/prices/#388 ) of the type sandbox S1-4 - if you are on a really small budget you could pick 1 smaller size too however i ll be roughly needing the amount of ram 3 of those vps can provide me. these vps can be setup easily to use a common LAN which we ll use as our communications network for traffic between our k3s nodes.

##### dedicated servers
If you need more power you can grab one of ovh's dedicated servers and use the vrack to connect these, currently the best bang for the buck ( cpu/mem for money ) you d get with the ADVANCE-2 dedis: https://www.ovhcloud.com/de/bare-metal/advance/adv-2/


## disk layout
##### vps
If you pick a vps just use the entire disk for / we ll setup rook-ceph on ovh's blockstorage
Each of ovh's vpss has two network cards ( eth0 / eth1 ) 

- eth0 has a public ip assigned and is connected to switches that lead towards the internet.
- eth1 is connected to a private network that only operates between the vpss.
##### dedicated servers
If you pick a dedi don't use the whole diskspace to install the operating system on rather make a small partition for the OS, and then we can use the rest for our rook ceph storage cluster.
recommended for dedi
- root: 50GB
- swap:  1GB
- rest: partition create ( but we ll remove the filesystem so ceph can use this space ) ( we ll use this storage with the ceph storage later on )


Each server has two network cards ( eno1 / eno2 ) 

- eno1 has a public ip assigned and is connected to switches that lead towards the internet.
- eno2 is connected to a private network that only operates between the servers. i ll be using a vlan tag for traffic on this network with ovh's vrack

</div>
</div>





### k3sup ( ketchup )
https://github.com/alexellis/k3sup is a tool that downloads the k3s installer and runs it for us

### ansible
it orchestration tool we ll be using to generate a config for k3sup and execute it via ssh

### the bootstrap part

I published a small repo @ https://github.com/loeken/bootstrap-k3s all you need is ansible installed locally ( pip install ansible ) 
- edit the inventory and define username/passwords/ips
- run the ansible ping command from the README.md in this project to test connection with ansible
- run the playbook

```
cd /tmp
git clone https://github.com/loeken/bootstrap-k3s
cd bootstrap-k3s
nano inventory 
ansible-playbook -i inventory playbook.yml
```