---
title: "My road to self hosted kubernetes with k3s - argocd"
date: 2021-03-29T23:38:59+02:00
draft: false
summary: In this article we are going to setup argocd in minikube, argocd will be the tool that we use to apply configuration changes to our kubernetes yaml files.

---

## How it works
Argo CD follows the GitOps pattern of using Git repositories as the source of truth for defining the desired application state. Kubernetes manifests can be specified in several ways:

- kustomize applications
- helm charts
- ksonnet applications
- jsonnet files
- Plain directory of YAML/json manifests
- Any custom config management tool configured as a config management plugin

## Simply put?
argocd connects to github repos where you publish your kubernetes manifests, argocd also connects to your kubernetes clusters. you then define apps in argocd ( which things to run in which cluster ), argocd then ensures stuff matches the state of the github repo, when that updates, argocd rolls out the updates too ).

## Installation

I am now going to intall argocd into my local minikube installation
```
❯ kubectl config use-context minikube
❯ kubectl create namespace argocd
❯ kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

This will create a new namespace, argocd, where Argo CD services and application resources will live.

#### argocd client

Next i need to be able run argocd commands on my system so i also need to install the cli i ll be grabbing this off AUR

```
❯ pacaur -S argocd-cli
```

#### access argocd UI

argocd ships with a (very nice) UI. we could expose it as a service/ingress etc but since im running locally a simple port forward will suffice. in order to login we first must grab the admin password

```
❯ kubectl get pods -n argocd -l app.kubernetes.io/name=argocd-server -o name | cut -d'/' -f 2
❯ kubectl port-forward svc/argocd-server -n argocd 8080:443
```

the we can login with "admin" and the password returned from the first kubectl command. since we forwarded to port 8080 we ll now login with our cli client via

```
❯ argocd login localhost:8080
WARNING: server certificate had error: x509: certificate signed by unknown authority. Proceed insecurely (y/n)? y
Username: admin 
Password: 
'admin' logged in successfully
Context 'localhost:8080' updated
```

#### update argocd admin password
after login one should change the admin password
```
❯ argocd account update-password
```

#### link cluster

argocd cli client extracts the cluster information from your ~/.kube/config you can list your clusters with:

```
❯ kubectl config get-contexts -o name
```

then we can specify which cluster to add i called my ovh vps cluster "ime"
```
❯ argocd cluster add ime
```


#### prepare github repository

so my prefered way is to generate a new keypair and then add the pubkey of that to github as a deploy key. this limits this keypair read only access - which is ideal for this pipeline.
```
❯ ssh-keygen -t rsa -b 4096 -f myproject
Generating public/private rsa key pair.
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in myproject
Your public key has been saved in myproject.pub
The key fingerprint is:
SHA256:O07yv+fi78oNN5oC/U1bzWfI4LYSD/SzZhu5qc9fQao loeken@0x00E
The key's randomart image is:
+---[RSA 4096]----+
|                 |
|                 |
|               . |
|          . . o  |
|       .S. o + = |
|      . ..o B.+ *|
|      ..+..E=* .o|
|       =.o+BX= . |
|        o+X#@o.  |
+----[SHA256]-----+
❯ ls myproject*
myproject  myproject.pub
```

now head to your github project that contains your code and add the pubkey as a deploy key

#### link github repository to argocd

<div class="row">
    <div class="col-sm-6">

![argocd link repo](/media/img/argocd_link_repo.png)

</div>
<div class="col-sm-6">

we then use the contents of the privateky ( myproject ) and insert it as the private key in argocd, then it can authenticate with github.

the repository url shouldnt start with https:// but use the git:// syntax ( ssh for auth )


</div>
</div>

#### create argocd app

now that we have added a repo ( to read kubernetes yaml manifest from ) and added a cluster to argocd ( where to deploy these manifests too ) - we can now create an app in argocd.

you can either specify manual sync policy - where argocd will only apply configuration changes when you manually tell it to, or selected the automated sync policy, which will check the git repo in certain intervals and automatically apply the configuration changes ( as long as minikube is running ).

when creating a new app we simply select our repository and cluster and click "create".
