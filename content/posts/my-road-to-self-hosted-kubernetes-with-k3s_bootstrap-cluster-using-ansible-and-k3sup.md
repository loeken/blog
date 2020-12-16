---
title: "Bootstrap k3s Cluster using ansible and k3sup on debian 10"
date: 2020-12-12T12:07:36+01:00
draft: false
summary: this article describes hwo to setup a k3s cluster on 3 dedicated servers
author: loeken
images:
tags:
  - kubernetes
  - k3s
  - debian 10
  - ansible
  - k3sup
---
<style type="text/css">
.flex { 
    display: flex; 
    justify-content: center; 
    align-items: center;
}
</style>
<div class="flex">

![TestCluster Layout](/media/img/k3s_testlab_02.png)

</div>
so for the test cluster i ll be using 3 dedicated servers with 8 cores and 32GB of ram each. they all have nvme ssds with 500GB ( in raid1 ).
we're going to partion the disk into 2 partitions:

- root: 50GB
- swap:  1GB
- rest: partition create ( but we ll remove the filesystem so ceph can use this space ) ( we ll use this storage with the ceph storage late on )


Each server has two network cards ( eno1 / eno2 ) 

- eno1 has a public ip assigned and is connected to switches that lead towards the internet.
- eno2 is connected to a private network that only operates between my servers. i ll be using a vlan tag for traffic on this network.


### k3sup ( ketchup )
https://github.com/alexellis/k3sup is a tool that downloads the k3s installer and runs it for us

### ansible
https://github.com/loeken/bootstrap-k3s it orchestration tool we ll be using to generate a config for k3sup and execute it via ssh


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