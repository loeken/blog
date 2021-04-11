---
title: "My Road to Self Hosted Kubernetes With K3s_nginx Ingress With Helm"
date: 2021-04-11T20:29:17+02:00
draft: true
draft: false
summary: The ingress is kubernetes way of routing incoming traffic towards the destinations. We'll be using nginx as an ingress controller.
---

So this will be the first thing we're going to install from bitnami, bitnami does not only publish a lot of different charts, they also publish updates if CVEs were published. so we ll be using this bitnami helm chart to install our nginx-ingress

```
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install my-release bitnami/nginx-ingress-controller
```