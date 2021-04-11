---
title: "My road to self hosted kubernetes with k3s - external-dns"
date: 2021-04-11T20:15:54+02:00
draft: false
summary: External-Dns is used to update dns records with ips of the kubernetes cluster. We'll use the cloudflare integration.
---

## external dns
API Token will be preferred for authentication if CF_API_TOKEN environment variable is set. Otherwise CF_API_KEY and CF_API_EMAIL should be set to run ExternalDNS with Cloudflare.

When using API Token authentication, the token should be granted Zone Read, DNS Edit privileges, and access to All zones.

If you would like to further restrict the API permissions to a specific zone (or zones), you also need to use the --zone-id-filter so that the underlying API requests only access the zones that you explicitly specify, as opposed to accessing all zones.

external-dns is quite easy to setup:

#### **`external-dns.yaml`**
```
apiVersion: v1
kind: ServiceAccount
metadata:
  name: external-dns
---
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRole
metadata:
  name: external-dns
rules:
- apiGroups: [""]
  resources: ["services","endpoints","pods"]
  verbs: ["get","watch","list"]
- apiGroups: ["extensions","networking.k8s.io"]
  resources: ["ingresses"] 
  verbs: ["get","watch","list"]
- apiGroups: [""]
  resources: ["nodes"]
  verbs: ["list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRoleBinding
metadata:
  name: external-dns-viewer
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: external-dns
subjects:
- kind: ServiceAccount
  name: external-dns
  namespace: default
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: external-dns
spec:
  strategy:
    type: Recreate
  selector:
    matchLabels:
      app: external-dns
  template:
    metadata:
      labels:
        app: external-dns
    spec:
      serviceAccountName: external-dns
      containers:
      - name: external-dns
        image: k8s.gcr.io/external-dns/external-dns:v0.7.6
        args:
        - --source=service # ingress is also possible
        - --domain-filter=example.com # (optional) limit to only example.com domains; change to match the zone created above.
        - --zone-id-filter=023e105f4ecef8ad9ca31a8372d0c353 # (optional) limit to a specific zone.
        - --provider=cloudflare
        - --cloudflare-proxied # (optional) enable the proxy feature of Cloudflare (DDOS protection, CDN...)
        env:
        - name: CF_API_KEY
          value: "YOUR_CLOUDFLARE_API_KEY"
        - name: CF_API_EMAIL
          value: "YOUR_CLOUDFLARE_EMAIL"
```
```
kubectl apply -f external-dns.yaml
```

note: if you want to install it into a different namesapce make sure you change the service account too:

```
- kind: ServiceAccount
  name: external-dns
  namespace: default
```