---
title: "My road to self hosted kubernetes with k3s - logging with EFK"
date: 2020-12-16T20:58:06+01:00
draft: false
summary: 
toc: false
author: loeken
images:
tags:
- kubernetes
- k3s
- elasticsearch
- fluentd
- kibana
---
# EFK ( Elasticsearch Fluentd Kibana )

### create override values

we'll be using the storage that we created using ceph https://blog.internetz.me/posts/my-road-to-self-hosted-kubernetes-with-k3s_distributed-storage-with-ceph

```
cat override-values.yaml
# Shrink default JVM heap.
esJavaOpts: "-Xmx128m -Xms128m"

# Allocate smaller chunks of memory per pod.
resources:
  requests:
    cpu: "100m"
    memory: "512M"
  limits:
    cpu: "1000m"
    memory: "512M"

# Request smaller persistent volumes.
volumeClaimTemplate:
  accessModes: [ "ReadWriteOnce" ]
  storageClassName: "rook-ceph-block"
  resources:
    requests:
      storage: 1G
```

### install elasticsearch via helm chart

```
kubectl create namespace logging
helm repo add elastic https://Helm.elastic.co
helm install -n logging elasticsearch elastic/elasticsearch -f override-values.yaml
```


### install kibana

``` 
helm install kibana elastic/kibana -n logging
```

### access kibana via port forward

```
kubectl -n logging port-forward deployment/kibana-kibana 5601
```

### install fluentd

```
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install fluentd bitnami/fluentd -n logging
```


kubectl -n logging port-forward deployment/kibana-kibana 5601