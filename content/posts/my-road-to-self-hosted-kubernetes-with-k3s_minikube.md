---
title: "My Road to Self Hosted Kubernetes With K3s_minikube"
date: 2021-03-27T22:05:10+01:00
draft: true
---

## Installation Minikube

Minikube is available for Mac/Windows/Linux you can find more information on https://minikube.sigs.k8s.io/docs/start/

It does require you to have docker in a working state ( [docker getting started ](/posts/docker-getting-started/) )

I'll be installing it from the AUR arch user repository.

```
❯ pacaur -S minikube
[sudo] Passwort für loeken: 
Löse Abhängigkeiten auf...
Suche nach in Konflikt stehenden Paketen...
Pakete (1) minikube-1.17.1-1
Gesamtgröße des Downloads:           11,16 MiB
Gesamtgröße der installierten Pakete:  49,45 MiB
:: Installation fortsetzen? [J/n] J
:: Empfange Pakete...
 minikube-1.17.1-1-x86_64                                                                                           11,2 MiB  10,2 MiB/s 00:01 [########################################################################################] 100%
(1/1) Prüfe Schlüssel im Schlüsselring                                                                                                         [########################################################################################] 100%
(1/1) Überprüfe Paket-Integrität                                                                                                               [########################################################################################] 100%
(1/1) Lade Paket-Dateien                                                                                                                       [########################################################################################] 100%
(1/1) Prüfe auf Dateikonflikte                                                                                                                 [########################################################################################] 100%
(1/1) Überprüfe verfügbaren Festplattenspeicher                                                                                                [########################################################################################] 100%
:: Verarbeite Paketänderungen...
(1/1) Installiere minikube                                                                                                                     [########################################################################################] 100%
Optionale Abhängigkeiten für minikube
    kubectl: to manage the cluster
    virtualbox: to use --vm-driver=virtualbox
:: Starte post-transaction hooks...
(1/1) Arming ConditionNeedsUpdate...
 ~                                                                                                                                                                                                                           6s  22:01:41 
❯ minikube start
😄  minikube v1.17.1 auf Arch 21.0
✨  Automatically selected the docker driver. Other choices: none, ssh
🎉  minikube 1.18.1 is available! Download it: https://github.com/kubernetes/minikube/releases/tag/v1.18.1
💡  To disable this notice, run: 'minikube config set WantUpdateNotification false'
👍  Starting control plane node minikube in cluster minikube
🚜  Pulling base image ...
💾  Downloading Kubernetes v1.20.2 preload ...
    > preloaded-images-k8s-v8-v1....: 491.22 MiB / 491.22 MiB  100.00% 10.79 Mi
🔥  Creating docker container (CPUs=2, Memory=3900MB) ...
🐳  Vorbereiten von Kubernetes v1.20.2 auf Docker 20.10.2...
    ▪ Generating certificates and keys ...
    ▪ Booting up control plane ...
    ▪ Configuring RBAC rules ...
🔎  Verifying Kubernetes components...
🌟  Enabled addons: storage-provisioner, default-storageclass
💡  kubectl not found. If you need it, try: 'minikube kubectl -- get pods -A'
🏄  Done! kubectl is now configured to use "minikube" cluster and "default" namespace by default
```