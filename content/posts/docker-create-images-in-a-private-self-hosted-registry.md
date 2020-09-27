---
title: "Docker Create Images in a Private Self Hosted Registry"
date: 2020-06-05T20:14:18+02:00
draft: true
toc: false
description: 
author: loeken
images:
tags:
  - untagged
---

first we need a docker registry where we can  push our own application to in this demo we ll be using a self hosted ( unsecured ) docker registry running inside docker:
```bash
docker run -d -p 5000:5000 --restart=always --name registry registry:2
Unable to find image 'registry:2' locally
2: Pulling from library/registry
486039affc0a: Pull complete 
ba51a3b098e6: Pull complete 
8bb4c43d6c8e: Pull complete 
6f5f453e5f2d: Pull complete 
42bc10b72f42: Pull complete 
Digest: sha256:7d081088e4bfd632a88e3f3bcd9e007ef44a796fddfe3261407a3f9f04abe1e7
Status: Downloaded newer image for registry:2
8c6960c8d64962c1054f617e0b141bcdbb8f234ebf3b03c9c52411b3c3062a40
``` 

then we tell docker to login: just type any username you want and an emtpy password.
```bash
docker login localhost:5000
Username: loeken
Password: 
WARNING! Your password will be stored unencrypted in /home/loeken/.docker/config.json.
Configure a credential helper to remove this warning. See
https://docs.docker.com/engine/reference/commandline/login/#credentials-store

Login Succeeded
```

Let's package the app that we build in the previous blogpost. this process uses the Dockerfile that ships with the github example repo.

```bash
mkdir -p ~/Projects
cd ~/Projects
git clone https://github.com/loeken/docker_nodejs_postgresql_demo
cd docker_nodejs_postgresql_demo

docker build -t docker_nodejs_postgresql_demo:1.0.0 .                                        
Sending build context to Docker daemon  922.1kB
Step 1/4 : FROM node
 ---> 2c52ab475b70
Step 2/4 : RUN mkdir -p /usr/src/app
 ---> Running in a4657b2583e0
Removing intermediate container a4657b2583e0
 ---> 54a28005f7f6
Step 3/4 : COPY index.js /usr/src/app
 ---> 8d040b12e927
Step 4/4 : CMD ["node", "index.js"]
 ---> Running in 4faed6f071c8
Removing intermediate container 4faed6f071c8
 ---> b77da0a970cc
Successfully built b77da0a970cc
Successfully tagged docker_nodejs_postgresql_demo:1.0.0
```

```bash
docker images|grep demo 
docker_nodejs_postgresql_demo   1.0.0               b77da0a970cc        2 minutes ago       941MB
```

let's push the image
```bash
docker tag docker_nodejs_postgresql_demo:1.0.0 localhost:5000/docker_nodejs_postgresql_demo

docker push localhost:5000/docker_nodejs_postgresql_demo 
The push refers to repository [localhost:5000/docker_nodejs_postgresql_demo]
2a7029e871f8: Pushed 
66ef83808cb6: Pushed 
a18892f26272: Pushed 
ee67a955c9b7: Pushed 
879c2fce68a8: Pushed 
5aea01ea0a0f: Pushed 
05f4935ad90a: Pushed 
c96f2308ab16: Pushed 
38c2f9ead82d: Pushed 
0dabcc98eeef: Pushed 
6885f9305c0a: Pushed 
latest: digest: sha256:5271a66adcd3881ae7c645a102a8dbe5cbcd43ce2c88fcf9d83cd1dde3b6d6dd size: 2629
```