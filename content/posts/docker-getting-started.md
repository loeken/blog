---
title: "Docker Getting Started"
date: 2020-06-05T13:55:43+02:00
draft: false
toc: false
description: summary of blogpost
author: loeken
Summary: An introduction into docker 
images:
tags:
  - docker
  - tutorial
  - blog
  - devops
  - sre
  - containerd
  - runc
  - kernel namespaces
  - docker containers
  - docker images
  - intro do docker
  - intro to kubernetes
---
## Docker - what is it?

A docker container is a packaged application with all necessary dependencies and configuration included to move, share and run an application.

### The video version of this:
{{<  youtube_lazy ytid="krQfc6q7LS4" yttitle="Road to Kubernetes - 01-  docker basics & getting started - k3s / k8s" >}}

### Why use it ?
- Docker compared to virtual machines do not have their own kernel running but use the kernel from the host system. ( less ram usage )
- Developer friendly. Docker client/images/repositories/docker-compose etc makes it easier for the non op
- A standard between devs / a standard between ops/devs (emergence of devops....)
- public image repositories. since docker became famous often images available from the application maintainers themselved.
- easy to run different versions of the application(s)

### Why maybe not ?
- easy to get working, easy to fuck up too
- resource starvation: As all the containers share the same kernel and the same resources, if the access to some resource is not constrained, one container can use it all up and starve the host OS and the other containers.
  On a VM, the resources are defined by the hypervisor, so no VM can deny the host OS from any resource, as the hypervisor itself can be configured to make restricted use of resources
- security
  - kernel exploits from container
  - Data separation ( On a docker container, there're some resources that are not namespaced / If any attacker can exploit any of those elements, they will own the host OS.):
    - SELinux
    - Cgroups
    - file systems under /sys, /proc/sys,
    - /proc/sysrq-trigger, /proc/irq, /proc/bus
    - /dev/mem, /dev/sd* file system
    - Kernel Modules
    A VM OS will not have direct access to any of those elements. It will talk to the hypervisor, and the hypervisor will make the appropriate system calls to the host OS. It will filter out invalid calls, adding a layer of security.
  - Raw Sockets
    The default Docker Unix socket (/var/run/docker.sock) can be mounted by any container if not properly secured. If some container mounts this socket, it can shutdown, start or create new images.

## How do they work?
Docker is written in Go and takes advantage of several features of the Linux kernel to deliver its functionality.
Docker uses a technology called namespaces to provide the isolated workspace called the container. When you run a container, Docker creates a set of namespaces for that container.
These namespaces provide a layer of isolation. Each aspect of a containers runs in a separate namespace its access is limited to the namespace..

Docker uses the following namespaces on Linux:
- the pid namespace ( processes )
- the net namespace ( networking )s
- the ipc namespace ( inter process communication )
- the mnt namespace ( mounting )
- the uts namespace ( unix timesharing system )

there are further  things used like cgroups etc., but the core of docker is archived by using kernel namespaces.

TLDR:
Take a look at the dockerd section: ( containerd is running but no containers )

![](/media/img/pstree_docker_no_container_running.png)

We now startup a docker with an interactive terminal ( -it ) which opens up bash inside the containerd-shim

We'll use the following docker container to take a look how docker works
#### **`Dockerfile`**
```
FROM debian:latest
RUN groupadd -g 1000 dockergroup && \
    useradd -d /home/dockeruser -r -u 1000 -g dockergroup dockeruser
RUN apt update -y
RUN apt install -y procps
USER dockeruser
CMD ["tail", "/dev/null"]
```

we now build the image and start it up
```
docker buid -t debian-nonroot .
docker run -v $PWD:/home/dockeruser/shared_folder -it debian-nonroot /bin/bash
```
![](/media/img/pstree_docker_container_running.png)

now inside the docker terminal we got from the docker run command we can run a long lasting process
```
watch "ps ax"
```
![](/media/img/pstree_docker_with_watch.png)

if we now compare pids from the host to the container you will notice that both host/container show the watch process but with different pids
(namespaces do the mapping)

### Containerd
Runtime requirments for containerd are minimal and are handeled via runc
Is started by dockerd

### RunC
runc is a cli tool for spawning and running containers to OCI specification

### Docker Client
a command line tool that communicates with a docker daemon

A good deep dive into this can be found: [on LiveOverflow's youtube video](https://www.youtube.com/watch?v=-YnMr1lj4Z8)

### Docker Containers
Container is a running environment for an Image

### Docker Images
Images can be found on https://hub.docker.com


### difference between containers and images:

TLDR: You grab an image from dockerhub and the moment you run the image you are basically creating a container that is based on this image.
with docker start/stop/log you are then working with the container not the image. 
```
docker pull redis
```

list images
```
docker images                                                                                                                                                      
 REPOSITORY                TAG                 IMAGE ID            CREATED             SIZE
 redis                     latest              36304d3b4540        7 days ago          104MB
 atlassian/jira-software   latest              b221dfd59c57        3 weeks ago         766MB
 blacklabelops/jira        latest              167698547c34        12 months ago       702MB
 tutum/mysql               5.6                 ffe19c282aec        4 years ago         472MB
```

### Manage Dockers
start docker in attached mode
```
docker run redis                                                                                                                                                 
1:C 05 Jun 2020 12:05:35.520 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
1:C 05 Jun 2020 12:05:35.520 # Redis version=6.0.4, bits=64, commit=00000000, modified=0, pid=1, just started
1:C 05 Jun 2020 12:05:35.520 # Warning: no config file specified, using the default config. In order to specify a config file use redis-server /path/to/redis.conf
1:M 05 Jun 2020 12:05:35.522 * Running mode=standalone, port=6379.
1:M 05 Jun 2020 12:05:35.522 # Server initialized
1:M 05 Jun 2020 12:05:35.522 # WARNING overcommit_memory is set to 0! Background save may fail under low memory condition. To fix this issue add 'vm.overcommit_memory = 1' to /etc/sysctl.conf and then reboot or run the command 'sysctl vm.overcommit_memory=1' for this to take effect.
1:M 05 Jun 2020 12:05:35.522 # WARNING you have Transparent Huge Pages (THP) support enabled in your kernel. This will create latency and memory usage issues with Redis. To fix this issue run the command 'echo never > /sys/kernel/mm/transparent_hugepage/enabled' as root, and add it to your /etc/rc.local in order to retain the setting after a reboot. Redis must be restarted after THP is disabled.
1:M 05 Jun 2020 12:05:35.522 * Ready to accept connections
```

start docker in detached mode ( returns id which can be used to interact with it later on, or just the first 12 chars of it )
```
docker run -d --name redistest redis                                                                                                                                             
770cc49014c42afdda5ff60e1db6f4a8903c5f6c0e755c4dac51d5c7138a9ebc
```

simple commands to start/stop
```
docker ps                                                                                                                                                              1.14   14:25  
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS               NAMES
770cc49014c4        redis               "docker-entrypoint.s…"   2 seconds ago       Up 1 second         6379/tcp            redistest

docker stop 770cc49014c4                                                                                                                                          
do770cc49014c4

docker ps                                                                                                                                                    
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES

docker start 770cc49014c4                                                                                                                                          
docker 770cc49014c4

docker stop redistest                                                                                                                                             
redistest

docker start redistest                                                                                                                                             
redistest

docker stop 770cc49014c4                                                                                                                                          
770cc49014c4

```

Bind port 12345 on the hostsystem to port 6379 inside the container
```
docker run -p 12345:6379 -d --name redistest2 redis                                                                                                              125 ↵  0.06   14:28  
a900c1787086d2bbbb1c025d6b8bdf242a7f0cd38c1f82f92a44aad0a17efaec
```

Logs:
```
docker logs redistest2
```

Debugging Docker by starting it with the "-it - interactive terminal" flag
```
docker run -it --name redistest3 redis /bin/bash                                                                                                                       4.48   14:31  
root@1c83696bfd23:/data# 
```

TLDR:
```
docker run - creates container from image
docker start/stop - starts a container
```