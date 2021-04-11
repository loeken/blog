---
title: "My road to self hosted kubernetes with k3s - Permission Manager"
date: 2021-04-11T13:09:49+02:00
draft: true
---


```
❯ k config get-contexts
CURRENT   NAME         CLUSTER      AUTHINFO     NAMESPACE
          baremetall   baremetall   baremetall   
          enso         enso         enso         
          ime          ime          ime          
          jp           jp           jp           
*         minikube     minikube     minikube     default
❯ kubectl config use-context ime
❯ kubectl create namespace argocd
```

now we tell argocd to create an app in the namespace on the ime cluster
```
❯ kubectl config use-context minikube
❯ argocd app create permission-manager-ime \
    --repo https://github.com/kfirfer/helm \
    --path charts/permission-manager \
    --dest-namespace permission-manager \
    --dest-server https://135.125.217.121:6443 \
    --helm-set basicAuthPassword=defineyourpasswordhere

❯ argocd app sync permission-manager-ime
```