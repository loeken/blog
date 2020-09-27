---
title: "Kubernetes Cert Manager for Letsencrypt Based Certificates With Nginx Ingress"
date: 2020-06-13T22:07:15+02:00
draft: true
toc: false
description: 
author: loeken
images:
tags:
  - k3s
  - cert-manager
  - letsencrypt
---

## Cert Manager
cert manager stores certificates in kubernetes secret store and we can configure the nginx-ingress to use these certificates.

#### **`cert-manager.yaml`**
```bash
wget https://github.com/jetstack/cert-manager/releases/download/v0.15.1/cert-manager.yaml
kubectl apply --validate=false -f cert-manager.yaml
```

#### **`cert-manager.crds.yaml`**
```bash
wget https://github.com/jetstack/cert-manager/releases/download/v0.15.1/cert-manager.crds.yaml
kubectl apply --validate=false -f cert-manager.crds.yaml
```

using the ClusterIssuer allows us to create certificates across all namespaces
#### **`letsencrypt-issuer.yaml`**
```yaml
apiVersion: cert-manager.io/v1alpha2
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    # The ACME server URL
    server: https://acme-v02.api.letsencrypt.org/directory
    # Email address used for ACME registration
    email: loeken@internetz.me
    # Name of a secret used to store the ACME account private key
    privateKeySecretRef:
      name: letsencrypt-prod
    # Enable the HTTP-01 challenge provider
    solvers:
    - http01:
        ingress:
          class:  nginx
```

if  this is your "first time" you can also point at the acme staging servers to not get rate limited
make sure to create a privateKeySecretRef called letsencrypt-staging same as as did for prod 
#### **`letsencrypt-issuer-staging.yaml`**
```yaml
apiVersion: cert-manager.io/v1alpha2
kind: ClusterIssuer
metadata:
  name: letsencrypt-staging
spec:
  acme:
    # The ACME server URL
    server: https://acme-staging-v02.api.letsencrypt.org/directory
    # Email address used for ACME registration
    email: loeken@internetz.me
    # Name of a secret used to store the ACME account private key
    privateKeySecretRef:
      name: letsencrypt-staging
    # Enable the HTTP-01 challenge provider
    solvers:
    - http01:
        ingress:
          class:  nginx
```

now apply  either letsencrypt-issuer or the letsencrypt-issues-staging
```bash
kubectl apply -f letsencrypt-issuer.yaml
```

verify
```bash
kubectrl get clusterissuers
```

### creating an actual certificate

#### **`test-certificate.yaml`**
```yaml
---
apiVersion: cert-manager.io/v1alpha2
kind: Certificate
metadata:
  name: test-internetz-me
  namespace: default
spec:
  secretName: test-internetz-me-tls
  issuerRef:
    name: letsencrypt-prod
    kind: ClusterIssuer
  commonName: test.internetz.me
  dnsNames:
  - test.internetz.me
```

apply
```bash
kubectl apply -f letsencrypt-issuer.yaml
```

verify
```bash
kubectrl get certificates
NAME                READY   SECRET                  AGE
test-internetz-me   True    test-internetz-me-tls   1m
```

more debug options by describing the various resources
```bash
kubectl describe certificate test-internetz-me
```

https://cert-manager.io/docs/faq/acme/ lists other resources that might be worth checking.

and example deployment that uses the nginx-ingress from one of the last tutorials can be found [here](https://github.com/loeken/k3s-nginx)

so now that we have a certificate we still need to tell the ingress of the deployment to use it



#### **`nginx-static-deployment.yaml`**
```yaml
---
apiVersion: networking.k8s.io/v1beta1
kind: Ingress
metadata:
  name: test-ingress
  annotations:
    cert-manager.io/cluster-issue: letsencrypt-prod
spec:
  rules:
  - host: test.internetz.me
    http:
      paths:
      - path: /
        backend:
          serviceName: test-service
          servicePort: 80
  tls:
  - hosts:
    - test.internetz.me
    secretName: test-internetz-me-tls
```