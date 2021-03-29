---
title: "My road to self hosted kubernetes with k3s kubectl"
date: 2021-03-27T23:08:08+01:00
draft: false
summary: Kubectl is a command line client that allows us to control multiple kubernetes clusters (k3s/k8s) it does this by calling the kubernetes endpoints and providing a set of certificate/keys to authenticate.
---

# kubectl

kubectl is a command line tool you can use to interact with the kubernetes api server.

we already installed minikube which includes kubectl and already creates a default config for us. the default config can be found in ~/.kube/config

you can extend your ~/.kube/config and add further clusters/users/contexts this allows us to define different credentials for different clusters and helps us to switch between various clusters easily. here is an example of a "REDACTED" ~/.kube/config and how i switch my context from using the minikube cluster to using my baremetall cluster

```
❯ cat ~/.kube/config
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: REDACTED
    server: https://REDACTED:6443
  name: baremetall
- cluster:
    certificate-authority-data: REDACTED
    server: https://REDACTED:6443
  name: enso
- cluster:
    certificate-authority-data: REDACTED
    server: https://REDACTED:6443
  name: ime
- cluster:
    certificate-authority-data: REDACTED
    server: https://REDACTED:6443
  name: jp
- cluster:
    certificate-authority-data: REDACTED
    server: https://REDACTED:8443
  name: minikube
contexts:
- context:
    cluster: baremetall
    user: baremetall
  name: baremetall
- context:
    cluster: enso
    user: enso
  name: enso
- context:
    cluster: ime
    user: ime
  name: ime
- context:
    cluster: jp
    user: jp
  name: jp
- context:
    cluster: minikube
    namespace: default
    user: minikube
  name: minikube
current-context: enso
kind: Config
preferences: {}
users:
- name: baremetall
  user:
    client-certificate-data: REDACTED
    client-key-data: REDACTED
- name: enso
  user:
    client-certificate-data: REDACTED
    client-key-data: REDACTED
- name: ime
  user:
    client-certificate-data: REDACTED
    client-key-data: REDACTED
- name: jp
  user:
    client-certificate-data: REDACTED
- name: minikube
  user:
    client-certificate-data: REDACTED
    client-key-data: REDACTED
```
```
❯ kubectl get nodes
NAME       STATUS   ROLES                  AGE     VERSION
minikube   Ready    control-plane,master   4d23h   v1.20.2
```
```
❯ kubectl config get-contexts                                                                                                                                          
CURRENT   NAME         CLUSTER      AUTHINFO     NAMESPACE
          baremetall   baremetall   baremetall   
          enso         enso         enso         
          ime          ime          ime          
          jp           jp           jp           
*         minikube     minikube     minikube     default

❯ kubectl config use-context baremetall                                                                                                                        

Switched to context "baremetall".

❯ kubectl get nodes
NAME          STATUS   ROLES         AGE    VERSION
k3s-node-01   Ready    etcd,master   106d   v1.20.2
k3s-node-02   Ready    etcd,master   106d   v1.20.2
k3s-node-03   Ready    etcd,master   106d   v1.20.2

```
the rest of the commands all follow a simple structure you can use kubectl help to list all commands
```
❯ kubectl help
kubectl controls the Kubernetes cluster manager.

 Find more information at: https://kubernetes.io/docs/reference/kubectl/overview/

Basic Commands (Beginner):
  create        Create a resource from a file or from stdin.
  expose        Take a replication controller, service, deployment or pod and expose it as a new Kubernetes Service
  run           Run a particular image on the cluster
  set           Set specific features on objects

Basic Commands (Intermediate):
  explain       Documentation of resources
  get           Display one or many resources
  edit          Edit a resource on the server
  delete        Delete resources by filenames, stdin, resources and names, or by resources and label selector

Deploy Commands:
  rollout       Manage the rollout of a resource
  scale         Set a new size for a Deployment, ReplicaSet or Replication Controller
  autoscale     Auto-scale a Deployment, ReplicaSet, or ReplicationController

Cluster Management Commands:
  certificate   Modify certificate resources.
  cluster-info  Display cluster info
  top           Display Resource (CPU/Memory/Storage) usage.
  cordon        Mark node as unschedulable
  uncordon      Mark node as schedulable
  drain         Drain node in preparation for maintenance
  taint         Update the taints on one or more nodes

Troubleshooting and Debugging Commands:
  describe      Show details of a specific resource or group of resources
  logs          Print the logs for a container in a pod
  attach        Attach to a running container
  exec          Execute a command in a container
  port-forward  Forward one or more local ports to a pod
  proxy         Run a proxy to the Kubernetes API server
  cp            Copy files and directories to and from containers.
  auth          Inspect authorization
  debug         Create debugging sessions for troubleshooting workloads and nodes

Advanced Commands:
  diff          Diff live version against would-be applied version
  apply         Apply a configuration to a resource by filename or stdin
  patch         Update field(s) of a resource
  replace       Replace a resource by filename or stdin
  wait          Experimental: Wait for a specific condition on one or many resources.
  kustomize     Build a kustomization target from a directory or a remote url.

Settings Commands:
  label         Update the labels on a resource
  annotate      Update the annotations on a resource
  completion    Output shell completion code for the specified shell (bash or zsh)

Other Commands:
  api-resources Print the supported API resources on the server
  api-versions  Print the supported API versions on the server, in the form of "group/version"
  config        Modify kubeconfig files
  plugin        Provides utilities for interacting with plugins.
  version       Print the client and server version information

Usage:
  kubectl [flags] [options]

Use "kubectl <command> --help" for more information about a given command.
Use "kubectl options" for a list of global command-line options (applies to all commands).
```