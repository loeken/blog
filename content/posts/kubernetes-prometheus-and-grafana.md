---
title: "Kubernetes Prometheus & Grafana"
date: 2020-06-11T13:50:14+02:00
draft: true
toc: false
description: 
author: loeken
images:
tags:
  - untagged
---

## Kubernetes & Prometheus
Prometheus by defaults pulls info from the hosts via an http endpoint by default this is the /metrics endpoint
Data exposed on this /metrics endpoint needs to support the prometheus endpoint.
Exporter is a standalone tool that gathers data and exposes it on the /metrics endpoint
These exporters are also available via docker ( can be used as sidecar containers ) 

### Promotheus Server
- Data Retrieval Worker ( pulls metrics data)
- Time Series Database ( stores time series metrics data )
- Api ( to access this stored data )


### View Data
- Prometheus Web Ui
- Grafana

### Terms

Targets: anything monitored
Units: a subset of whats monitored
- cpu status
- memory usage
- disk usage
- exception count
- request count

### metrics:

Each monitored target exposes a /metrics endpoint that expose your metrics in a certain [format](https://github.com/prometheus/docs/blob/master/content/docs/instrumenting/exposition_formats.md)

HELP: description of what the metric is
TYPE: one of three metrics types:
- Counter ( how often something happend )
- Gauge ( current value of something )
- Histogram ( How long something took / how big a request was)


### Prometheus Client libraries
[libraries for various languages are available here](https://prometheus.io/docs/instrumenting/clientlibs/)
Official third-party client libraries:
- Go
- Java or Scala
- Python
- Ruby

Unofficial third-party client libraries:
- Bash
- C
- C++
- Common Lisp
- Dart
- Elixir
- Erlang
- Haskell
- Lua for Nginx
- Lua for Tarantool
- .NET / C#
- Node.js
- Perl
- PHP
- R
- Rust


### promoetheus's pull system
controlled pulling of metrics in order to avoid the monitoring becoming the bottleneck.
multiple prometheus instances can pull metrics ( good scalability )


### pushgateway
"short lived jobs" services that only live for short times can use short lived jobs to push data into prometheus

### alert manager
responsible for firing alerts via different channels ( slack / email / sms etc )

### Prometheus data storage
local time series database ( integrates with remote storage systems )


## Setting up prometheus

first we need to create a cluster role:
#### **`prometheus-rbac-setup.yaml`**
```yaml
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRole
metadata:
  name: prometheus
rules:
- apiGroups: [""]
  resources:
  - nodes
  - nodes/proxy
  - services
  - endpoints
  - pods
  - ingresses
  verbs: ["get", "list", "watch"]
- apiGroups:
  - networking.k8s.io
  resources:
  - ingresses
  verbs: ["get", "list", "watch"]
- nonResourceURLs: ["/metrics"]
  verbs: ["get"]
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: prometheus
  namespace: default
---
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRoleBinding
metadata:
  name: prometheus
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: prometheus
subjects:
- kind: ServiceAccount
  name: prometheus
  namespace: default
```

not the prometheus.yml is from prometheus and does not adhere to yaml file name extension - which might be confusing here as we use yaml across this blog 

this configmap basically contains the info on what prometheus scrapes. the most important part of the next section would be 
```yaml
          - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
            action: keep
            regex: true
          - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
            action: replace
            regex: ([^:]+)(?::\d+)?;(\d+)
            replacement: $1:$2
            target_label: __address__
```
this would basically mean in our pod definition ( kind: Deployment ) that we would need two annotations to tell prometheus to scrape this pod, and which port to scrape
#### **`prometheus-configmap.yml`**
```yaml
apiVersion: v1
data:
  prometheus.yml: |
    scrape_configs:
      - job_name: 'kubernetes-apiservers'
        kubernetes_sd_configs:
          - role: endpoints
        scheme: https
        tls_config:
          ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
        bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
        relabel_configs:
          - source_labels: [__meta_kubernetes_namespace, __meta_kubernetes_service_name, __meta_kubernetes_endpoint_port_name]
            action: keep
            regex: default;kubernetes;https
      - job_name: 'kubernetes-nodes'
        scheme: https
        tls_config:
          ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
        bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
        kubernetes_sd_configs:
          - role: node
        relabel_configs:
          - action: labelmap
            regex: __meta_kubernetes_node_label_(.+)
          - target_label: __address__
            replacement: kubernetes.default.svc:443
          - source_labels: [__meta_kubernetes_node_name]
            regex: (.+)
            target_label: __metrics_path__
            replacement: /api/v1/nodes/${1}/proxy/metrics
      - job_name: 'kubernetes-cadvisor'
        scheme: https
        tls_config:
          ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
        bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
        kubernetes_sd_configs:
          - role: node
        relabel_configs:
          - action: labelmap
            regex: __meta_kubernetes_node_label_(.+)
          - target_label: __address__
            replacement: kubernetes.default.svc:443
          - source_labels: [__meta_kubernetes_node_name]
            regex: (.+)
            target_label: __metrics_path__
            replacement: /api/v1/nodes/${1}/proxy/metrics/cadvisor
      - job_name: 'kubernetes-service-endpoints'
        kubernetes_sd_configs:
          - role: endpoints
        relabel_configs:
          - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
            action: keep
            regex: true
          - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
            action: replace
            regex: ([^:]+)(?::\d+)?;(\d+)
            replacement: $1:$2
            target_label: __address__
          - action: labelmap
            regex: __meta_kubernetes_service_label_(.+)
          - source_labels: [__meta_kubernetes_namespace]
            action: replace
            target_label: kubernetes_namespace
          - source_labels: [__meta_kubernetes_service_name]
            action: replace
            target_label: kubernetes_name

      - job_name: 'kubernetes-services'
        metrics_path: /probe
        params:
          module: [http_2xx]
        kubernetes_sd_configs:
          - role: service
        relabel_configs:
          - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
            action: keep
            regex: true
          - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
            action: replace
            regex: ([^:]+)(?::\d+)?;(\d+)
            replacement: $1:$2
            target_label: __address__
          - source_labels: [__address__]
            target_label: __param_target
          - source_labels: [__param_target]
            target_label: instance
          - action: labelmap
            regex: __meta_kubernetes_service_label_(.+)
          - source_labels: [__meta_kubernetes_namespace]
            target_label: kubernetes_namespace
          - source_labels: [__meta_kubernetes_service_name]
            target_label: kubernetes_name
      - job_name: 'kubernetes-ingresses'
        metrics_path: /metrics
        basic_auth:
          username: "loeken"
          password: "topsecure"
        params:
          module: [http_2xx]
        kubernetes_sd_configs:
          - role: ingress
        relabel_configs:
          - source_labels: [__meta_kubernetes_service_annotation_example_io_should_be_probed]
            action: keep
            regex: true
          - source_labels: [__meta_kubernetes_ingress_scheme,__address__,__meta_kubernetes_ingress_path]
            regex: (.+);(.+);(.+)
            replacement: ${1}://${2}${3}
            target_label: __param_target
          - source_labels: [__param_target]
            target_label: instance
          - action: labelmap
            regex: __meta_kubernetes_ingress_label_(.+)
          - source_labels: [__meta_kubernetes_namespace]
            target_label: kubernetes_namespace
          - source_labels: [__meta_kubernetes_ingress_name]
            target_label: kubernetes_name
      - job_name: 'kubernetes-pods'
        kubernetes_sd_configs:
          - role: pod
        relabel_configs:
        # Example relabel to scrape only pods that have
        # "example.io/should_be_scraped = true" annotation.
          - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
            action: keep
            regex: true
        #
        # Example relabel to customize metric path based on pod
        # "example.io/metric_path = <metric path>" annotation.
        #  - source_labels: [__meta_kubernetes_pod_annotation_example_io_metric_path]
        #    action: replace
        #    target_label: __metrics_path__
        #    regex: (.+)
        #
        # Example relabel to scrape only single, desired port for the pod
        # based on pod "example.io/scrape_port = <port>" annotation.
          - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
            action: replace
            regex: ([^:]+)(?::\d+)?;(\d+)
            replacement: $1:$2
            target_label: __address__
          - action: labelmap
            regex: __meta_kubernetes_pod_label_(.+)
          - source_labels: [__meta_kubernetes_namespace]
            action: replace
            target_label: kubernetes_namespace
          - source_labels: [__meta_kubernetes_pod_name]
            action: replace
            target_label: kubernetes_pod_name
kind: ConfigMap
metadata:
  name: prometheus-cm
  namespace: default
```

```bash
kubectl apply -f prometheus-configmap.yaml
```

Similar to the last node example we are deploying this the same way with a service exposing it via the ingress
#### **`prometheus-deplyoment.yaml`**
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: prometheus-deployment
  labels:
    app: prometheus-server
spec:
  replicas: 1
  selector:
    matchLabels:
      app: prometheus-server
  template:
    metadata:
      labels:
        app: prometheus-server
    spec:
      containers:
        - name: prometheus
          image: prom/prometheus
          args:
            - "--config.file=/etc/prometheus/prometheus.yml"
            - "--storage.tsdb.path=/prometheus/"
          ports:
            - containerPort: 9090
          volumeMounts:
            - name: config-volume
              mountPath: /etc/prometheus
            - name: prometheus-storage-volume
              mountPath: /prometheus
      volumes:
        - name: config-volume
          configMap:
            name: prometheus-cm  
        - name: prometheus-storage-volume
          emptyDir: {}
---
apiVersion: v1
kind: Service
metadata:
  name: prometheus-service
spec:
  selector:
    app: prometheus-server
  ports:
  - name: promui
    protocol: TCP
    port: 9090
    targetPort: 9090
---
apiVersion: networking.k8s.io/v1beta1
kind: Ingress
metadata:
  name: prometheus-ingress
  annotations:
    kubernetes.io/ingress.class: "nginx"
spec:
  rules:
  - host: prometheus.example.com
    http:
      paths:
      - path: /
        backend:
          serviceName: prometheus-service
          servicePort: 9090
```
apply deployment

```bash
kubectl apply -f prometheus-deplyoment.yaml
```

afterwards you can view it via http://prometheus.example.com/ if you point prometheus.example.com at any of the k3s nodes

## Grafana
Grafana is a really nice ui to create dashboars from the data prometheus gathers

grafana-datasource.yaml 
#### **`grafana-datasource.yaml`**
```
apiVersion: v1
kind: ConfigMap
metadata:
  name: grafana-datasources
data:
  prometheus.yaml: |-
    {
        "apiVersion": 1,
        "datasources": [
            {
               "access":"proxy",
                "editable": true,
                "name": "prometheus",
                "orgId": 1,
                "type": "prometheus",
                "url": "http://prometheus.example.com",
                "version": 1
            }
        ]
    }
```


#### **`grafana-deployment.yaml`**
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: grafana
spec:
  replicas: 1
  selector:
    matchLabels:
      app: grafana
  template:
    metadata:
      name: grafana
      labels:
        app: grafana
    spec:
      containers:
      - name: grafana
        image: grafana/grafana:latest
        ports:
        - name: grafana
          containerPort: 3000
        resources:
          limits:
            memory: "1Gi"
            cpu: "1000m"
          requests: 
            memory: "1Gi"
            cpu: "500m"
        volumeMounts:
          - mountPath: /var/lib/grafana
            name: grafana-storage
          - mountPath: /etc/grafana/provisioning/datasources
            name: grafana-datasources
            readOnly: false
      volumes:
        - name: grafana-storage
          emptyDir: {}
        - name: grafana-datasources
          configMap:
              defaultMode: 420
              name: grafana-datasources
---
kind: Service
apiVersion: v1
metadata:
  name: grafana-service
  annotations:
    prometheus.io/scrape: 'true'
    prometheus.io/port:   '3000'
spec:
  selector:
    app: grafana
  ports:
  - name: grafanaui
    protocol: TCP
    port: 3000
    targetPort: 3000
---
apiVersion: networking.k8s.io/v1beta1
kind: Ingress
metadata:
  name: grafana-ingress
  annotations:
    kubernetes.io/ingress.class: "nginx"
spec:
  rules:
  - host: grafana.example.com
    http:
      paths:
      - path: /
        backend:
          serviceName: grafana-service
          servicePort: 3000
```
afterwards you can view it via http://grafana
.example.com/ if you point prometheus.example.com at any of the k3s nodes

an example for a website that is using nginx to host a static site ( and has nginx /stub_status exposed ) and a second
container which reads the /stub_status endpoint and converts it to prometheus format

note: something still seems buggy with the cloudflare integration

#### **`blog-deployment.yml`**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: blog
  labels:
    app: blog
spec:
  replicas: 1
  selector:
    matchLabels:
      app: blog
  template:
    metadata:
      labels:
        app: blog
        monitoring: '1'
    spec:
      containers:
        - name: blog
          image: gcr.io/example/blog
          imagePullPolicy: Always
          ports:
            - containerPort: 80
        - name: adapter
          image: nginx/nginx-prometheus-exporter:0.4.2
          args: ["-nginx.scrape-uri","http://localhost/stub_status"]
          ports:
            - containerPort: 9113
      imagePullSecrets:
        - name: gcr-json-key
      volumes:
        - name: dhparam-volume
          configMap:
            name: dhparam
---
apiVersion: v1
kind: Service
metadata:
  name: blog-service
  annotations:
    prometheus.io/port: "9113"
    prometheus.io/scrape: "true"
spec:
  selector:
    app: blog
  type: LoadBalancer
  ports:
    - protocol: TCP
      port: 20001
      targetPort: 80
      nodePort: 30001


---
apiVersion: networking.k8s.io/v1beta1
kind: Ingress
metadata:
  name: blog-ingress
  annotations:
    cert-manager.io/cluster-issue: letsencrypt-prod
    #external-dns.alpha.kubernetes.io/hostname: blog.internetz.me
    #external-dns.alpha.kubernetes.io/cloudflare-proxied: "false"
    #external-dns.alpha.kuberentes.io/ttl: "1"
    prometheus.io/port: "9113"
    prometheus.io/scrape: "true"

  labels:
    monitoring: '1'

spec:
  rules:
    - host: blog.internetz.me
      http:
        paths:
          - path: /
            backend:
              serviceName: blog-service
              servicePort: 80
  tls:
    - hosts:
        - blog.internetz.me
      secretName: blog-internetz-me-tls
---
apiVersion: cert-manager.io/v1alpha2
kind: Certificate
metadata:
  name: blog-internetz-me
  namespace: default
spec:
  secretName: blog-internetz-me-tls
  issuerRef:
    name: letsencrypt-prod
    kind: ClusterIssuer
  commonName: blog.internetz.me
  dnsNames:
    - blog.internetz.me
```
