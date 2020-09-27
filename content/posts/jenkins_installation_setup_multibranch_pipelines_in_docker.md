---
title: "Jenkins installation in Docker"
date: 2020-02-08T15:57:31+01:00
draft: true
---

# jenkins to build, test and deploy your projects

## 1. Introduction

Jenkins is a software written in java which allows you to setup a CI/CD pipeline. There are many ways to setup Jenkins depending on your environment. In this example I will try to set it up from the perspective of a single user, who wants a simple method to deploy/test their code easily. This approach does allow other users to submit code too.
We are not going to use github enterprise but a normal free github account instead. We'll also setup the projects in a way that does NOT require the server to have a public ip ( you will not need to open ports for it or expose jenkins publicly ). We will also take a look at security and isolate each project ( with github repositories ) with their independent deploy keys, security by compartmentalization is one of the best approaches one can go for.
Furthermore I'll be using the jenkins credential store and explain how we can use the jenkins credential store to save passwords/credentials and keep these outside the github repository. I will also explain how we can then run these projects locally for development. And last but not least I will also provide an example project in nodejs on github which can be used to follow this tutorial

#### Continuous Integration

Continuous integration (CI) is the practice of automating the integration of code changes from multiple contributors into a single software project. The CI process is comprised of automatic tools that assert the new code's correctness before integration.

#### Continuous Delivery
Continuous delivery (CD or CDE) is a software engineering approach in which teams produce software in short cycles, ensuring that the software can be reliably released at any time and, when releasing the software, doing so manually.

#### Pipeline
In computing, a pipeline, also known as a data pipeline, is a set of data processing elements connected in series, where the output of one element is the input of the next one. The elements of a pipeline are often executed in parallel or in time-sliced fashion.

## 2.nodejs example:

### 2.1. Installation of Jenkins

{{< youtube_lazy ytid="HSUyxzsKZaY" yttitle="Install Jenkins" >}}

Because jenkins is written in java it can be run on almost any operating system ( the can run java applications ). So depending on your use case pick the appropriate jenkins image ( i recommend the Long Term Support version ( LTS ))

[You can download Jenkins here](https://jenkins.io/download/)

[You can follow this guide to learn how to install Jenkins natively on your operating system](https://jenkins.io/doc/book/installing/)
In the following example I'll be using docker in the following version:

If you do not have docker installed yet run a 
```bash
sudo apt update && sudo apt install docker-ce -y
```
this will install the last docker community edition
```bash
$ docker --version
Docker version 19.03.5, build 633a0ea838
```

make sure to change the user to whatever your current user is ( whoami )
```bash
user@docker:~$ cat docker_jenkins.sh 
#!/bin/bash
mkdir /home/user/jenkins_home
docker run --name jenkins -p 8080:8080 -p 12345:12345 -v /home/user/jenkins_home:/var/jenkins_home jenkins/jenkins:lts

user@docker:~$ ./docker_jenkins.sh 
Unable to find image 'jenkins/jenkins:lts' locally
lts: Pulling from jenkins/jenkins
146bd6a88618: Pull complete 
9935d0c62ace: Pull complete 
db0efb86e806: Pull complete 
e705a4c4fd31: Pull complete 
3d3bf7f7e874: Pull complete 
49371c5b9ff6: Pull complete 
3f7eaaf7ad75: Pull complete 
c174316783db: Pull complete 
024826a29afe: Pull complete 
51f2bbab8803: Pull complete 
6ce657881f7a: Pull complete 
a5270cffee3a: Pull complete 
083f0f43b51d: Pull complete 
215073008675: Pull complete 
ffda073f8127: Pull complete 
3672d2dcba21: Pull complete 
906db372d194: Pull complete 
66fb46692c0e: Pull complete 
3a9a81b17595: Pull complete 
Digest: sha256:54486ebab0d42582a84fc35b184c4f5cf9998d139bbec552bc6ec8c617c4a055
Status: Downloaded newer image for jenkins/jenkins:lts
Running from: /usr/share/jenkins/jenkins.war
webroot: EnvVars.masterEnvVars.get("JENKINS_HOME")
2020-02-08 15:34:24.694+0000 [id=1]	INFO	org.eclipse.jetty.util.log.Log#initialized: Logging initialized @503ms to org.eclipse.jetty.util.log.JavaUtilLog
2020-02-08 15:34:24.836+0000 [id=1]	INFO	winstone.Logger#logInternal: Beginning extraction from war file
2020-02-08 15:34:26.716+0000 [id=1]	WARNING	o.e.j.s.handler.ContextHandler#setContextPath: Empty contextPath
2020-02-08 15:34:26.786+0000 [id=1]	INFO	org.eclipse.jetty.server.Server#doStart: jetty-9.4.z-SNAPSHOT; built: 2019-05-02T00:04:53.875Z; git: e1bc35120a6617ee3df052294e433f3a25ce7097; jvm 1.8.0_242-b08
2020-02-08 15:34:27.072+0000 [id=1]	INFO	o.e.j.w.StandardDescriptorProcessor#visitServlet: NO JSP Support for /, did not find org.eclipse.jetty.jsp.JettyJspServlet
2020-02-08 15:34:27.122+0000 [id=1]	INFO	o.e.j.s.s.DefaultSessionIdManager#doStart: DefaultSessionIdManager workerName=node0
2020-02-08 15:34:27.123+0000 [id=1]	INFO	o.e.j.s.s.DefaultSessionIdManager#doStart: No SessionScavenger set, using defaults
2020-02-08 15:34:27.126+0000 [id=1]	INFO	o.e.j.server.session.HouseKeeper#startScavenging: node0 Scavenging every 660000ms
2020-02-08 15:34:27.579+0000 [id=1]	INFO	hudson.WebAppMain#contextInitialized: Jenkins home directory: /var/jenkins_home found at: EnvVars.masterEnvVars.get("JENKINS_HOME")
2020-02-08 15:34:27.708+0000 [id=1]	INFO	o.e.j.s.handler.ContextHandler#doStart: Started w.@26be6ca7{Jenkins v2.204.2,/,file:///var/jenkins_home/war/,AVAILABLE}{/var/jenkins_home/war}
2020-02-08 15:34:27.725+0000 [id=1]	INFO	o.e.j.server.AbstractConnector#doStart: Started ServerConnector@19932c16{HTTP/1.1,[http/1.1]}{0.0.0.0:8080}
2020-02-08 15:34:27.726+0000 [id=1]	INFO	org.eclipse.jetty.server.Server#doStart: Started @3536ms
2020-02-08 15:34:27.727+0000 [id=22]	INFO	winstone.Logger#logInternal: Winstone Servlet Engine v4.0 running: controlPort=disabled
2020-02-08 15:34:29.338+0000 [id=29]	INFO	jenkins.InitReactorRunner$1#onAttained: Started initialization
2020-02-08 15:34:29.383+0000 [id=27]	INFO	jenkins.InitReactorRunner$1#onAttained: Listed all plugins
2020-02-08 15:34:30.898+0000 [id=31]	INFO	jenkins.InitReactorRunner$1#onAttained: Prepared all plugins
2020-02-08 15:34:30.904+0000 [id=31]	INFO	jenkins.InitReactorRunner$1#onAttained: Started all plugins
2020-02-08 15:34:30.915+0000 [id=37]	INFO	jenkins.InitReactorRunner$1#onAttained: Augmented all extensions
2020-02-08 15:34:31.588+0000 [id=40]	INFO	jenkins.InitReactorRunner$1#onAttained: Loaded all jobs
2020-02-08 15:34:31.603+0000 [id=55]	INFO	hudson.model.AsyncPeriodicWork#lambda$doRun$0: Started Download metadata
2020-02-08 15:34:31.614+0000 [id=55]	INFO	hudson.util.Retrier#start: Attempt #1 to do the action check updates server
2020-02-08 15:34:32.605+0000 [id=29]	INFO	o.s.c.s.AbstractApplicationContext#prepareRefresh: Refreshing org.springframework.web.context.support.StaticWebApplicationContext@27206905: display name [Root WebApplicationContext]; startup date [Sat Feb 08 15:34:32 UTC 2020]; root of context hierarchy
2020-02-08 15:34:32.605+0000 [id=29]	INFO	o.s.c.s.AbstractApplicationContext#obtainFreshBeanFactory: Bean factory for application context [org.springframework.web.context.support.StaticWebApplicationContext@27206905]: org.springframework.beans.factory.support.DefaultListableBeanFactory@23f9ae9b
2020-02-08 15:34:32.619+0000 [id=29]	INFO	o.s.b.f.s.DefaultListableBeanFactory#preInstantiateSingletons: Pre-instantiating singletons in org.springframework.beans.factory.support.DefaultListableBeanFactory@23f9ae9b: defining beans [authenticationManager]; root of factory hierarchy
2020-02-08 15:34:32.841+0000 [id=29]	INFO	o.s.c.s.AbstractApplicationContext#prepareRefresh: Refreshing org.springframework.web.context.support.StaticWebApplicationContext@5427a84: display name [Root WebApplicationContext]; startup date [Sat Feb 08 15:34:32 UTC 2020]; root of context hierarchy
2020-02-08 15:34:32.841+0000 [id=29]	INFO	o.s.c.s.AbstractApplicationContext#obtainFreshBeanFactory: Bean factory for application context [org.springframework.web.context.support.StaticWebApplicationContext@5427a84]: org.springframework.beans.factory.support.DefaultListableBeanFactory@7fa32661
2020-02-08 15:34:32.843+0000 [id=29]	INFO	o.s.b.f.s.DefaultListableBeanFactory#preInstantiateSingletons: Pre-instantiating singletons in org.springframework.beans.factory.support.DefaultListableBeanFactory@7fa32661: defining beans [filter,legacy]; root of factory hierarchy
2020-02-08 15:34:33.235+0000 [id=29]	INFO	jenkins.install.SetupWizard#init: 

*************************************************************
*************************************************************
*************************************************************

Jenkins initial setup is required. An admin user has been created and a password generated.
Please use the following password to proceed to installation:

ff31c02226674d3085fd33aa4c75a9ac

This may also be found at: /var/jenkins_home/secrets/initialAdminPassword

*************************************************************
*************************************************************
*************************************************************
```

```bash
user@docker:~$ ip a show docker0
3: docker0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default 
    link/ether 02:42:29:6e:e0:90 brd ff:ff:ff:ff:ff:ff
    inet 172.17.0.1/16 brd 172.17.255.255 scope global docker0
       valid_lft forever preferred_lft forever
    inet6 fe80::42:29ff:fe6e:e090/64 scope link 
       valid_lft forever preferred_lft forever
```

we can now access jenkins in the browser via http://172.17.0.1:8080
a second port which we can use to talk to our node app is port 12345


##### installing node inside the container
```bash
docker exec -it --user root jenkins /bin/bash
```
now that we are inside the docker container we can install nodejs version 12 with the following commands:
```bash
curl -sL https://deb.nodesource.com/setup_12.x | bash -
apt install -y nodejs
```

### 2.2. example project
{{< youtube_lazy ytid="yeF7x6kPCWs" yttitle="example project in nodejs" >}}

you can find an example node js project on https://github.com/loeken/node_example

### 2.3. creating our first job in jenkins
{{< youtube_lazy ytid="nMBqIn3Wx4o" yttitle="example project in nodejs" >}}

### 2.4. private repositories
{{< youtube_lazy ytid="SXzgJf8fjYE" yttitle="create private repository" >}}

```bash
ssh-keygen -t rsa -f id_rsa -C "node_example"
```

### 2.5. add agent node in jenkins
{{< youtube_lazy ytid="iC6tjCVuNq8" yttitle="add agent node in jenkins" >}}

we now switch to https://github.com/loeken/node_example2

```bash
user@docker:~$ cat docker_agent.sh
#!/bin/bash
docker run -it --user root --rm --name agent -p 3001:3001 -p 3002:3002 debian
```

```bash
apt update
apt install nano openjdk-11-jre openssh-server git curl -y
curl -sL https://deb.nodesource.com/setup_12.x | bash -
apt install -y nodejs
service ssh start

adduser jenkins
usermod -p '*' jenkins
su jenkins
ssh-keygen -t rsa
nano ~/.ssh/authorized_keys

```

### 2.6. deploy node project to jenkins agent over ssh
{{< youtube_lazy ytid="Z2AnXbxVzfc" yttitle="deploy node project to a jenkins agent over ssh" >}}