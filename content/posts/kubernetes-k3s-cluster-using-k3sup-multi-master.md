---
title: "Kubernetes K3s Cluster Using K3sup Multi Master"
date: 2020-06-08T13:01:40+02:00
draft: true
toc: false
description: summary of blogpost
author: loeken
images:
tags:
  - untagged
---

### getting started information


##### Terminology
- kubernetes: Full blown container orchestration tool
- minicube: a 1 node kubernetes cluster running inside a vm ( good for local testing )
- k3s a lightweight alternative to Kubernetes  with a lot of unneeded code removed
- k3sup a small extra tool that helps you getting your k3s cluster going quickly 

##### What is this docker/kuberentes stuff?
{{<  youtube_lazy ytid="1xo-0gCVhTU" yttitle="Introduction to micrososervices, docker and kubernetes" >}}

##### Why k3s what's the difference to kubernetes

{{<  youtube_lazy ytid="-HchRyqNtkU" yttitle="k3s under the hood" >}}

### prepare 3 virtual machines

I span up 3 virtual machines each of them having 2 network interfaces
the first interface has a public ip faceing the internet
the second interface has a private ip connected to an internal vpn. I've created it like this so i can expose services publicly on the 1 public interface to start with. 
while I can use the secondary interface to securely connect to the servers
<style type="text/css">
.flex { 
    display: flex; 
    justify-content: center; 
    align-items: center;
}
</style>
<div class="flex">

![Prepare the Disk](/media/img/k3s_testlab_01.png)

</div>

[Download Image Markup](/media/imgmarkup/k3s_testlab_01.py)

I used debian 10 netinstaller. these are the dependencies k3s needs in order to run. I created a user called ansible which i ll be using in this tutorial.
the ips of these test vms are in the 192.168.122.0/24 subnet
k3s-01: 10.0.4.82
k3s-02: 10.0.4.83
k3s-03: 10.0.4.84
```
sudo apt install curl sudo
```

sudo expects to be configured to not use a password we are doing this by editing the /etc/sudoers config
```
%sudo	ALL=(ALL:ALL) NOPASSWD:ALL
```

now we add the user to the sudo group
```
usermod -a -G sudo ansible
```

we also transfer our id_rsa.pub onto the 3 vms so we can login. k3sup uses id_rsa.pub/id_rsa it seems 
( it did not support my kr ssh agent forwarding )
```
ssh-copy-id ansible@10.0.4.82
ssh-copy-id ansible@10.0.4.83 
ssh-copy-id ansible@10.0.4.84 
```

### installing k3sup locally on my workstation:

```
curl -sLS https://get.k3sup.dev | sh
sudo install k3sup /usr/local/bin/

k3sup --help
```


### installation of k3s using k3sup on the first virtual machine
creating the cluster on the first node. this will create a kubeconfig file in the home folder of the user you are running this command from, i ran this from my workstation.
not the added extra --bind-address and the advertise address params which tells the server to not bind on the ip of the primary but only on the secondary interface
and also to advertise this address to others to be used for communication.

we will be going with version v1.19.1-rc2+k3s1 as it does not have this dqlite crap that keeps on breaking but uses etcd
```
k3sup install --k3s-version v1.19.1-rc2+k3s1 --ip 10.0.4.82 --user ansible --cluster --k3s-extra-args '--no-deploy=traefik --bind-address=10.0.4.82 --advertise-address=10.0.4.82 --node-ip=10.0.4.82 --node-external-ip 1.2.3.4'
Running: k3sup install
Public IP: 10.0.4.82
ssh -i /home/loeken/.ssh/id_rsa -p 22 ansible@10.0.4.82
ssh: curl -sLS https://get.k3s.io | INSTALL_K3S_EXEC='server --cluster-init --tls-san 10.0.4.82 --bind-address=10.0.4.82 --advertise-address=10.0.4.82 --node-ip=10.0.4.82' INSTALL_K3S_VERSION='v1.17.2+k3s1' sh -

[INFO]  Using v1.17.2+k3s1 as release
[INFO]  Downloading hash https://github.com/rancher/k3s/releases/download/v1.17.2+k3s1/sha256sum-amd64.txt
[INFO]  Downloading binary https://github.com/rancher/k3s/releases/download/v1.17.2+k3s1/k3s
[INFO]  Verifying binary download
[INFO]  Installing k3s to /usr/local/bin/k3s
[INFO]  Creating /usr/local/bin/kubectl symlink to k3s
[INFO]  Creating /usr/local/bin/crictl symlink to k3s
[INFO]  Creating /usr/local/bin/ctr symlink to k3s
[INFO]  Creating killall script /usr/local/bin/k3s-killall.sh
[INFO]  Creating uninstall script /usr/local/bin/k3s-uninstall.sh
[INFO]  env: Creating environment file /etc/systemd/system/k3s.service.env
[INFO]  systemd: Creating service file /etc/systemd/system/k3s.service
[INFO]  systemd: Enabling k3s unit
Created symlink /etc/systemd/system/multi-user.target.wants/k3s.service → /etc/systemd/system/k3s.service.
[INFO]  systemd: Starting k3s
Result: [INFO]  Using v1.17.2+k3s1 as release
[INFO]  Downloading hash https://github.com/rancher/k3s/releases/download/v1.17.2+k3s1/sha256sum-amd64.txt
[INFO]  Downloading binary https://github.com/rancher/k3s/releases/download/v1.17.2+k3s1/k3s
[INFO]  Verifying binary download
[INFO]  Installing k3s to /usr/local/bin/k3s
[INFO]  Creating /usr/local/bin/kubectl symlink to k3s
[INFO]  Creating /usr/local/bin/crictl symlink to k3s
[INFO]  Creating /usr/local/bin/ctr symlink to k3s
[INFO]  Creating killall script /usr/local/bin/k3s-killall.sh
[INFO]  Creating uninstall script /usr/local/bin/k3s-uninstall.sh
[INFO]  env: Creating environment file /etc/systemd/system/k3s.service.env
[INFO]  systemd: Creating service file /etc/systemd/system/k3s.service
[INFO]  systemd: Enabling k3s unit
[INFO]  systemd: Starting k3s
 Created symlink /etc/systemd/system/multi-user.target.wants/k3s.service → /etc/systemd/system/k3s.service.

ssh: sudo cat /etc/rancher/k3s/k3s.yaml

apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUJXRENCL3FBREFnRUNBZ0VBTUFvR0NDcUdTTTQ5QkFNQ01DTXhJVEFmQmdOVkJBTU1HR3N6Y3kxelpYSjIKWlhJdFkyRkFNVFU1TVRJNE1qVTVOekFlRncweU1EQTJNRFF4TkRVMk16ZGFGdzB6TURBMk1ESXhORFUyTXpkYQpNQ014SVRBZkJnTlZCQU1NR0dzemN5MXpaWEoyWlhJdFkyRkFNVFU1TVRJNE1qVTVOekJaTUJNR0J5cUdTTTQ5CkFnRUdDQ3FHU000OUF3RUhBMElBQkFoWFlkWW5ZWjVCcVUwS3JhdmpkZVNIQXFJcVNoKzRnT1N0cDFrOUVNQUMKS1RLbyt6RjNoQmZ3UGF4VzRZOHF1Q2hjdDNPZVBPekVvdzAwanFmT0t1MmpJekFoTUE0R0ExVWREd0VCL3dRRQpBd0lDcERBUEJnTlZIUk1CQWY4RUJUQURBUUgvTUFvR0NDcUdTTTQ5QkFNQ0Ewa0FNRVlDSVFDL3hYeCthQm5pCmZzUk9kMG53dkczaGlaWURlcmJYK3A1MmgzNVI5QUpYWGdJaEFMcWxkZVZMVXlRR1R3Z1JVY01TYTE0enF1ekQKaUdxc2JQZkViUVZpbHpxRQotLS0tLUVORCBDRVJUSUZJQ0FURS0tLS0tCg==
    server: https://10.0.4.82:6443
  name: default
contexts:
- context:
    cluster: default
    user: default
  name: default
current-context: default
kind: Config
preferences: {}
users:
- name: default
  user:
    password: afd3bd64ed2aef936b904d13dee80739
    username: admin
Result: apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUJXRENCL3FBREFnRUNBZ0VBTUFvR0NDcUdTTTQ5QkFNQ01DTXhJVEFmQmdOVkJBTU1HR3N6Y3kxelpYSjIKWlhJdFkyRkFNVFU1TVRJNE1qVTVOekFlRncweU1EQTJNRFF4TkRVMk16ZGFGdzB6TURBMk1ESXhORFUyTXpkYQpNQ014SVRBZkJnTlZCQU1NR0dzemN5MXpaWEoyWlhJdFkyRkFNVFU1TVRJNE1qVTVOekJaTUJNR0J5cUdTTTQ5CkFnRUdDQ3FHU000OUF3RUhBMElBQkFoWFlkWW5ZWjVCcVUwS3JhdmpkZVNIQXFJcVNoKzRnT1N0cDFrOUVNQUMKS1RLbyt6RjNoQmZ3UGF4VzRZOHF1Q2hjdDNPZVBPekVvdzAwanFmT0t1MmpJekFoTUE0R0ExVWREd0VCL3dRRQpBd0lDcERBUEJnTlZIUk1CQWY4RUJUQURBUUgvTUFvR0NDcUdTTTQ5QkFNQ0Ewa0FNRVlDSVFDL3hYeCthQm5pCmZzUk9kMG53dkczaGlaWURlcmJYK3A1MmgzNVI5QUpYWGdJaEFMcWxkZVZMVXlRR1R3Z1JVY01TYTE0enF1ekQKaUdxc2JQZkViUVZpbHpxRQotLS0tLUVORCBDRVJUSUZJQ0FURS0tLS0tCg==
    server: https://10.0.4.82:6443
  name: default
contexts:
- context:
    cluster: default
    user: default
  name: default
current-context: default
kind: Config
preferences: {}
users:
- name: default
  user:
    password: afd3bd64ed2aef936b904d13dee80739
    username: admin
 
Saving file to: /home/loeken/kubeconfig

# Test your cluster with:
export KUBECONFIG=/home/loeken/kubeconfig
kubectl get node -o wide
```

so we are doing what we are told:
```
export KUBECONFIG=/home/loeken/kubernetes/kubeconfig                                                                                                                                                                                                                 0.01   12:18  
kubectl get node -o wide
NAME     STATUS   ROLES    AGE     VERSION        INTERNAL-IP     EXTERNAL-IP   OS-IMAGE                       KERNEL-VERSION   CONTAINER-RUNTansible
k3s-01   Ready    master   7m13s   v1.17.2+k3s1   94.23.161.209   <none>        Debian GNU/Linux 10 (buster)   4.19.0-9-amd64   containerd://1.3.3-k3s1
```

this will set the environment variable but this won't remain after reboot so i ll make it persistent via:
```
echo "export KUBECONFIG=/home/loeken/kubernetes/kubeconfig" >> .zshrc
```

notice that im using the zsh shell if you are not using zsh you might want to use the ~/.bashrc or the ~/.profile file instead

joining in the second node
```
k3sup join --k3s-version v1.19.1-rc2+k3s1 --ip 10.0.4.83 --server-ip 10.0.4.82 --user ansible --server  --k3s-extra-args '--no-deploy=traefik --bind-address=10.0.4.83 --advertise-address=10.0.4.83 --node-ip=10.0.4.83 --node-external-ip=1.2.3.4'  

Running: k3sup join
Server IP: 10.0.4.82
ssh -i /home/loeken/.ssh/id_rsa -p 22 ansible@10.0.4.82
ssh: sudo cat /var/lib/rancher/k3s/server/node-token

K104c8b3d5e41e6aaf0c5af72ea741ed730b85f6e937244ed2436df5ac3152c38ca::server:feee10ccbf5c359452d0ed73a44396e5
ssh: curl -sfL https://get.k3s.io/ | K3S_URL='https://10.0.4.82:6443' INSTALL_K3S_EXEC='server --server https://10.0.4.82:6443' K3S_TOKEN='K104c8b3d5e41e6aaf0c5af72ea741ed730b85f6e937244ed2436df5ac3152c38ca::server:feee10ccbf5c359452d0ed73a44396e5' INSTALL_K3S_VERSION='v1.17.2+k3s1' sh -s - --bind-address=10.0.4.83 --advertise-address=10.0.4.83 --node-ip=10.0.4.83
[INFO]  Using v1.17.2+k3s1 as release
[INFO]  Downloading hash https://github.com/rancher/k3s/releases/download/v1.17.2+k3s1/sha256sum-amd64.txt
[INFO]  Downloading binary https://github.com/rancher/k3s/releases/download/v1.17.2+k3s1/k3s
[INFO]  Verifying binary download
[INFO]  Installing k3s to /usr/local/bin/k3s
[INFO]  Creating /usr/local/bin/kubectl symlink to k3s
[INFO]  Creating /usr/local/bin/crictl symlink to k3s
[INFO]  Creating /usr/local/bin/ctr symlink to k3s
[INFO]  Creating killall script /usr/local/bin/k3s-killall.sh
[INFO]  Creating uninstall script /usr/local/bin/k3s-uninstall.sh
[INFO]  env: Creating environment file /etc/systemd/system/k3s.service.env
[INFO]  systemd: Creating service file /etc/systemd/system/k3s.service
[INFO]  systemd: Enabling k3s unit
Created symlink /etc/systemd/system/multi-user.target.wants/k3s.service → /etc/systemd/system/k3s.service.
[INFO]  systemd: Starting k3s
Logs: Created symlink /etc/systemd/system/multi-user.target.wants/k3s.service → /etc/systemd/system/k3s.service.
Output: [INFO]  Using v1.17.2+k3s1 as release
[INFO]  Downloading hash https://github.com/rancher/k3s/releases/download/v1.17.2+k3s1/sha256sum-amd64.txt
[INFO]  Downloading binary https://github.com/rancher/k3s/releases/download/v1.17.2+k3s1/k3s
[INFO]  Verifying binary download
[INFO]  Installing k3s to /usr/local/bin/k3s
[INFO]  Creating /usr/local/bin/kubectl symlink to k3s
[INFO]  Creating /usr/local/bin/crictl symlink to k3s
[INFO]  Creating /usr/local/bin/ctr symlink to k3s
[INFO]  Creating killall script /usr/local/bin/k3s-killall.sh
[INFO]  Creating uninstall script /usr/local/bin/k3s-uninstall.sh
[INFO]  env: Creating environment file /etc/systemd/system/k3s.service.env
[INFO]  systemd: Creating service file /etc/systemd/system/k3s.service
[INFO]  systemd: Enabling k3s unit
[INFO]  systemd: Starting k3s

```

three times the charm:
```
k3sup join --k3s-version v1.19.1-rc2+k3s1 --ip 10.0.4.84 --server-ip 10.0.4.82 --user ansible --server  --k3s-extra-args '--no-deploy=traefik --bind-address=10.0.4.84 --advertise-address=10.0.4.84 --node-ip=10.0.4.84 --node-external-ip=1.2.3.4'  

Running: k3sup join
Server IP: 10.0.4.82
ssh -i /home/loeken/.ssh/id_rsa -p 22 ansible@10.0.4.82
ssh: sudo cat /var/lib/rancher/k3s/server/node-token

K104c8b3d5e41e6aaf0c5af72ea741ed730b85f6e937244ed2436df5ac3152c38ca::server:feee10ccbf5c359452d0ed73a44396e5
ssh: curl -sfL https://get.k3s.io/ | K3S_URL='https://10.0.4.82:6443' INSTALL_K3S_EXEC='server --server https://10.0.4.82:6443' K3S_TOKEN='K104c8b3d5e41e6aaf0c5af72ea741ed730b85f6e937244ed2436df5ac3152c38ca::server:feee10ccbf5c359452d0ed73a44396e5' INSTALL_K3S_VERSION='v1.17.2+k3s1' sh -s - --bind-address=10.0.4.84 --advertise-address=10.0.4.84 --node-ip=10.0.4.84
[INFO]  Using v1.17.2+k3s1 as release
[INFO]  Downloading hash https://github.com/rancher/k3s/releases/download/v1.17.2+k3s1/sha256sum-amd64.txt
[INFO]  Downloading binary https://github.com/rancher/k3s/releases/download/v1.17.2+k3s1/k3s
[INFO]  Verifying binary download
[INFO]  Installing k3s to /usr/local/bin/k3s
[INFO]  Creating /usr/local/bin/kubectl symlink to k3s
[INFO]  Creating /usr/local/bin/crictl symlink to k3s
[INFO]  Creating /usr/local/bin/ctr symlink to k3s
[INFO]  Creating killall script /usr/local/bin/k3s-killall.sh
[INFO]  Creating uninstall script /usr/local/bin/k3s-uninstall.sh
[INFO]  env: Creating environment file /etc/systemd/system/k3s.service.env
[INFO]  systemd: Creating service file /etc/systemd/system/k3s.service
[INFO]  systemd: Enabling k3s unit
Created symlink /etc/systemd/system/multi-user.target.wants/k3s.service → /etc/systemd/system/k3s.service.
[INFO]  systemd: Starting k3s
Logs: Created symlink /etc/systemd/system/multi-user.target.wants/k3s.service → /etc/systemd/system/k3s.service.
Output: [INFO]  Using v1.17.2+k3s1 as release
[INFO]  Downloading hash https://github.com/rancher/k3s/releases/download/v1.17.2+k3s1/sha256sum-amd64.txt
[INFO]  Downloading binary https://github.com/rancher/k3s/releases/download/v1.17.2+k3s1/k3s
[INFO]  Verifying binary download
[INFO]  Installing k3s to /usr/local/bin/k3s
[INFO]  Creating /usr/local/bin/kubectl symlink to k3s
[INFO]  Creating /usr/local/bin/crictl symlink to k3s
[INFO]  Creating /usr/local/bin/ctr symlink to k3s
[INFO]  Creating killall script /usr/local/bin/k3s-killall.sh
[INFO]  Creating uninstall script /usr/local/bin/k3s-uninstall.sh
[INFO]  env: Creating environment file /etc/systemd/system/k3s.service.env
[INFO]  systemd: Creating service file /etc/systemd/system/k3s.service
[INFO]  systemd: Enabling k3s unit
[INFO]  systemd: Starting k3s


```

### verfiy that the installation succeeded and all three nodes are up ( executing from local pc )
```
kubectl get node -o wide
NAME     STATUS   ROLES    AGE     VERSION        INTERNAL-IP     EXTERNAL-IP   OS-IMAGE                       KERNEL-VERSION   CONTAINER-RUNTIME
k3s-02   Ready    master   4m35s   v1.17.2+k3s1   10.0.4.83       <none>        Debian GNU/Linux 10 (buster)   4.19.0-8-amd64   containerd://1.3.3-k3s1
k3s-01   Ready    master   14m     v1.17.2+k3s1   94.23.161.209   <none>        Debian GNU/Linux 10 (buster)   4.19.0-9-amd64   containerd://1.3.3-k3s1
k3s-03   Ready    master   80s     v1.17.2+k3s1   10.0.4.84       <none>        Debian GNU/Linux 10 (buster)   4.19.0-8-amd64   containerd://1.3.3-k3s1
```

### installing the kubernetes dashboard:

```
GITHUB_URL=https://github.com/kubernetes/dashboard/releases
VERSION_KUBE_DASHBOARD=$(curl -w '%{url_effective}' -I -L -s -S ${GITHUB_URL}/latest -o /dev/null | sed -e 's|.*/||')
sudo k3s kubectl create -f https://raw.githubusercontent.com/kubernetes/dashboard/${VERSION_KUBE_DASHBOARD}/aio/deploy/recommended.yaml
```

now we create 2 markups to define the user access to the dashboard
#### **`dashboard.admin-user.yaml`**
```
apiVersion: v1
kind: ServiceAccount
metadata:
  name: admin-user
  namespace: kubernetes-dashboard"
```
#### **`dashboard.admin-user-role.yaml`**
```
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: admin-user
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: admin-user
  namespace: kubernetes-dashboard
```
apply the configuration
```
kubectl apply -f dashboard.admin-user.yaml
kubectl apply -f dashboard.admin-user-role.yaml
```


next step is to get the bearer token which we need to login to the dashboard in the following step
```
k3s kubectl -n kubernetes-dashboard describe secret admin-user-token | grep ^token
```

since k3s version 1.19 we have to use the proxy to access the dashboard but this is not tricky at all:
```
kubectl proxy
http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/#/clusterrole?namespace=default
```


create a deployment for nginx:
#### **`nginx-deployment.yaml`**
```
apiVersion: apps/v1 # for versions before 1.9.0 use apps/v1beta2
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  selector:
    matchLabels:
      app: nginx
  replicas: 2 # tells deployment to run 2 pods matching the template
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.16.1
        ports:
        - containerPort: 80
```

```
kubectl apply -f nginx-deployment.yaml
```