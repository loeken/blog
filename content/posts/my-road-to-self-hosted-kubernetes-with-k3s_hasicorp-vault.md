---
title: "My Road to Self Hosted Kubernetes With K3s Hasicorp Vault"
date: 2020-12-13T16:41:35+01:00
summary: we ll be setting up hashicorps vault, which we ll be using to inject secrets into containers and provider credentials to database etc
toc: false
author: loeken
images:
tags:
- kubernetes
- k3s
- ceph
---

### Vault

"Secure, store and tightly control access to tokens, passwords, certificates, encryption keys for protecting secrets and other sensitive data using a UI, CLI, or HTTP API."


Hashicorp does have a docs page which covers most of the things quite well https://learn.hashicorp.com/vault the process of getting vault running in k3s with helm wasn't that smooth here so glad i finally figured this one out ...


Anyways, hop over to the hashicorp learn subdomain and take a look at the concepts of the vault.


### The scenario

So my goal is to setup vault into it's seperated namespace: vault I then want to create a testnamespace: pgtest

In the pgtest namespace we'll create a simple example deployment and then we ll inject some secret ( in a future tutorial we ll also install a postgresql cluster into this pgtest namespace - and we will link that cluster to the vault )


### preparing ca/certificate generation

windows users can just use docker to generate these:
```
docker run -it --rm -v ${PWD}:/work -w /work debian:buster bash

# in container:
apt-get update && apt-get install -y curl &&
curl https://pkg.cfssl.org/R1.2/cfssl_linux-amd64 -o /usr/local/bin/cfssl && \
curl https://pkg.cfssl.org/R1.2/cfssljson_linux-amd64 -o /usr/local/bin/cfssljson && \
chmod +x /usr/local/bin/cfssl && \
chmod +x /usr/local/bin/cfssljson
```

### generate ca
I will now be genearting a ca

```
cfssl gencert -initca ca-csr.json | cfssljson -bare ca
2020/12/16 11:37:38 [INFO] generating a new CA key and certificate from CSR
2020/12/16 11:37:38 [INFO] generate received request
2020/12/16 11:37:38 [INFO] received CSR
2020/12/16 11:37:38 [INFO] generating key: rsa-2048
2020/12/16 11:37:38 [INFO] encoded CSR
2020/12/16 11:37:38 [INFO] signed certificate with serial number *HIDDEN*
```

### generate server certificate/key
then we create a server certificate/key and sign it with the ca we created above, im just simply hardcoding the hostnames for vault-0 - vault5 which allows me to use a total of 6 vaults running - however i only do plan to start with 3 ( in our helm values override ) 
```
cat ca-config.json
{
  "signing": {
    "default": {
      "expiry": "8760h"
    },
    "profiles": {
      "default": {
        "usages": ["signing", "key encipherment", "server auth", "client auth"],
        "expiry": "8760h"
      }
    }
  }
}

cat vault-csr.json
{
  "CN": "vault",
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "UK",
      "L": "London",
      "O": "Mafia",
      "OU": "Devops",
      "ST": "London"
    }
  ]
}

cfssl gencert \
  -ca=ca.pem \
  -ca-key=ca-key.pem \
  -config=ca-config.json \
  -hostname="vault-0.vault-internal,vault-1.vault-internal,vault-2.vault-internal,vault-3.vault-internal,vault-4.vault-internal,vault-5.vault-internal,vault.vault.svc,localhost,127.0.0.1" \
  -profile=default \
  vault-csr.json | cfssljson -bare vault
2020/12/16 11:39:25 [INFO] generate received request
2020/12/16 11:39:25 [INFO] received CSR
2020/12/16 11:39:25 [INFO] generating key: rsa-2048
2020/12/16 11:39:25 [INFO] encoded CSR
2020/12/16 11:39:25 [INFO] signed certificate with serial number *HIDDEN*
```

I now end up with these files in that directory:
```
-rw-r--r--  1 loeken loeken  229 Dec 16 11:32 ca-config.json
-rw-r--r--  1 loeken loeken 1041 Dec 16 11:37 ca.csr
-rw-r--r--  1 loeken loeken  232 Dec 16 11:32 ca-csr.json
-rw-------  1 loeken loeken 1679 Dec 16 11:37 ca-key.pem
-rw-r--r--  1 loeken loeken 1273 Dec 16 11:37 ca.pem
-rw-r--r--  1 loeken loeken 3972 Dec 16 11:32 notes.txt
-rw-r--r--  1 loeken loeken 3580 Dec 16 11:32 override-values.yaml
-rw-r--r--  1 loeken loeken 1269 Dec 16 11:39 vault.csr
-rw-r--r--  1 loeken loeken  211 Dec 16 11:32 vault-csr.json
-rw-------  1 loeken loeken 1675 Dec 16 11:39 vault-key.pem
-rw-r--r--  1 loeken loeken 1623 Dec 16 11:39 vault.pem
```
### create namespace vault & pgtest
I want to keep the vault in it's own little namespace
```
kubectl create namespace vault
kubectl create namespace pgtest
```

### save certs/ca/key in secret
copy the generate ca/cert/key into a secret so the helm chart override-values.yaml can access it through this secret.

```
cat <<EOF > ./tls-server-secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: tls-server
type: Opaque
data:
  tls.crt: $(cat vault.pem | base64 | tr -d '\n')
  tls.key: $(cat vault-key.pem | base64 | tr -d '\n') 
  ca.crt: $(cat ca.pem | base64 | tr -d '\n')
EOF
kubectl apply -n vault -f tls-server-secret.yaml
kubectl apply -n pgtest -f tls-server-secret.yaml
```


#### **`override-values.yaml`**

the contents of the generated ca.crt will be added to the injector.certs.caBundle in the override-values.yaml
```# Vault Helm Chart Value Overrides
global:
  enabled: true
  tlsDisable: false

injector:
  enabled: true
  # Use the Vault K8s Image https://github.com/hashicorp/vault-k8s/
  image:
    repository: "hashicorp/vault-k8s"
    tag: "latest"

  resources:
      requests:
        memory: 256Mi
        cpu: 250m
      limits:
        memory: 256Mi
        cpu: 250m
  metrics:
    enabled: false
  certs:
    secretName: tls-server
    caBundle: "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURjRENDQWxpZ0F3SUJBZ0lVRnZvM242TW5E
dGVwY3pNb2twNFVsc3lPVDZJd0RRWUpLb1pJaHZjTkFRRUwKQlFBd1VERUxNQWtHQTFVRUJoTUNW
VXN4RHpBTkJnTlZCQWdUQmt4dmJtUnZiakVQTUEwR0ExVUVCeE1HVEc5dQpaRzl1TVE0d0RBWURW
UVFLRXdWTllXWnBZVEVQTUEwR0ExVUVDeE1HUkdWMmIzQnpNQjRYRFRJd01USXlPREE1Ck1UZ3dN
Rm9YRFRJMU1USXlOekE1TVRnd01Gb3dVREVMTUFrR0ExVUVCaE1DVlVzeER6QU5CZ05WQkFnVEJr
eHYKYm1SdmJqRVBNQTBHQTFVRUJ4TUdURzl1Wkc5dU1RNHdEQVlEVlFRS0V3Vk5ZV1pwWVRFUE1B
MEdBMVVFQ3hNRwpSR1YyYjNCek1JSUJJakFOQmdrcWhraUc5dzBCQVFFRkFBT0NBUThBTUlJQkNn
S0NBUUVBMGlTOStHWDJRbFY5CjhFeDVJQ1l3VVRXdkZvS0Vib01VRGNCSWgwMWlac1p0b29QSCtT
QzA5R2ovbkl2aGJLRTExRmc3MGRuQVkrZWgKRHkvQ3UxSzNIN2NCTEVrWmxzL0VKcTNIWmJTK3NN
Qkp1OUxQeXBweUtTUTdCVGpWVnN6QlIzbnVIb1FJLzZBbgp6RHhUYjhEOXllZms3QnJFc3ZjdXZ4
czhFL2RLbXRwSGNDNXBsaTk0dTJWOUszZVNNNkJVU3kwck9MMUdIbjlpCnBmVU15UzBYd2gxTFJK
T2crUmN6ZDRBTmdzVFBxUFF3c2V3UkRuSUJCa1FlR1l2UmRFUWZSRDNzdFZFc0QyNUsKalZJRGk2
ckMxU1dBelprK0JzYjgwcTZJeVRvSEp6MzM1SWl1alM5ZXZGdWlZWkczMnF5a0ZuSTdTZ1FRZDdR
SwpPM3JlTVRtcDNRSURBUUFCbzBJd1FEQU9CZ05WSFE4QkFmOEVCQU1DQVFZd0R3WURWUjBUQVFI
L0JBVXdBd0VCCi96QWRCZ05WSFE0RUZnUVVnbER5ZkF1Vmduby82d3Jlc250SjE5VmZXR0V3RFFZ
SktvWklodmNOQVFFTEJRQUQKZ2dFQkFETnRsSW4wMzFKV3RsdFJKZVJ1WExUam1wd25OZldCMUQ2
Mitrd0cwYXR5dUNBNTBFM05STlFXMXFXdQpiTmVVaGI5YlpOZmhEZHVJcDBpRVl2WUl3VVRHSDdP
R0VEU0hOdEs0ZXNGMXFBejA0ZlllRmd2bDFDbUsrM0dOClVvQzJrTlY5YjhVSmU2Q2xJM0dsdnhC
NStIaW1PeW9PQ09nVGRad1lxQkZxSGM0by8rWHhPTWZkQklUcWUyMWcKeTZzNmF1dDV5SXFzeldp
TUJDTkVPMUZXaTMveDJKTk1tNjJEUlRFS0ZPUTZ2NThhd0VmVkxkR3lwdU91V3ZNQQppaWJBZ2dE
cGhOa3RBMjZxMHVlNTlubjgzaEZhNXd6WitzNUhZRXJEWU1EQnZUdlh3d0YxSlNtelNQcWdnSjcw
ClhtUUZUeTBvQ0FKdHpyQ1Y2VC9seXdBVFp1WT0KLS0tLS1FTkQgQ0VSVElGSUNBVEUtLS0tLQo="

server:
  # Use the non Enterprise Image
  image:
    repository: "vault"
    tag: "1.5.4"
    # Overrides the default Image Pull Policy
    pullPolicy: IfNotPresent

  # These Resource Limits are in line with node requirements in the
  # Vault Reference Architecture for a Small Cluster
  resources:
    requests:
      memory: 8Gi
      cpu: 2000m
    limits:
      memory: 16Gi
      cpu: 2000m
  dataStorage:
    enabled: true
    storageClass: rook-ceph-block
    size: 5Gi

  # For HA configuration and because we need to manually init the vault,
  # we need to define custom readiness/liveness Probe settings
  readinessProbe:
    enabled: true
    path: "/v1/sys/health?standbyok=true&sealedcode=204&uninitcode=204"
  livenessProbe:
    enabled: true
    path: "/v1/sys/health?standbyok=true"
    initialDelaySeconds: 60

  # extraEnvironmentVars is a list of extra enviroment variables to set with the stateful set. These could be
  # used to include variables required for auto-unseal.
  extraEnvironmentVars:
    VAULT_CACERT: /vault/userconfig/tls-server/ca.crt

  # extraVolumes is a list of extra volumes to mount. These will be exposed
  # to Vault in the path `/vault/userconfig/<name>/`.
  extraVolumes:
    - type: secret
      name: tls-server

  # This configures the Vault Statefulset to create a PVC for audit logs.
  # See https://www.vaultproject.io/docs/audit/index.html to know more
  auditStorage:
    enabled: true

  standalone:
    enabled: false

  # Run Vault in "HA" mode.
  ha:
    enabled: true
    replicas: 3
    raft:
      enabled: true
      setNodeId: true

      config: |
        ui = true
        listener "tcp" {
          address = "[::]:8200"
          cluster_address = "[::]:8201"
          tls_cert_file = "/vault/userconfig/tls-server/tls.crt"
          tls_key_file = "/vault/userconfig/tls-server/tls.key"
          tls_ca_cert_file = "/vault/userconfig/tls-server/ca.crt"
        }

        storage "raft" {
          path = "/vault/data"
            retry_join {
            leader_api_addr = "https://vault-0.vault-internal:8200"
            leader_ca_cert_file = "/vault/userconfig/tls-server/ca.crt"
            leader_client_cert_file = "/vault/userconfig/tls-server/tls.crt"
            leader_client_key_file = "/vault/userconfig/tls-server/tls.key"
          }
          retry_join {
            leader_api_addr = "https://vault-1.vault-internal:8200"
            leader_ca_cert_file = "/vault/userconfig/tls-server/ca.crt"
            leader_client_cert_file = "/vault/userconfig/tls-server/tls.crt"
            leader_client_key_file = "/vault/userconfig/tls-server/tls.key"
          }
          retry_join {
            leader_api_addr = "https://vault-2.vault-internal:8200"
            leader_ca_cert_file = "/vault/userconfig/tls-server/ca.crt"
            leader_client_cert_file = "/vault/userconfig/tls-server/tls.crt"
            leader_client_key_file = "/vault/userconfig/tls-server/tls.key"
          }
        }

        service_registration "kubernetes" {}

# Vault UI
ui:
  enabled: true
  serviceType: "LoadBalancer"
  serviceNodePort: null
  externalPort: 8200

  # For Added Security, edit the below
  #loadBalancerSourceRanges:
  #   - < Your IP RANGE Ex. 10.0.0.0/16 >
  #   - < YOUR SINGLE IP Ex. 1.78.23.3/32 >
```

### install 3 vaults via helm chart:
```
helm install vault hashicorp/vault --namespace vault -f override-values.yaml
W1216 11:47:21.697877   65254 warnings.go:67] rbac.authorization.k8s.io/v1beta1 ClusterRoleBinding is deprecated in v1.17+, unavailable in v1.22+; use rbac.authorization.k8s.io/v1 ClusterRoleBinding
W1216 11:47:21.780427   65254 warnings.go:67] rbac.authorization.k8s.io/v1beta1 RoleBinding is deprecated in v1.17+, unavailable in v1.22+; use rbac.authorization.k8s.io/v1 RoleBinding
W1216 11:47:22.168023   65254 warnings.go:67] admissionregistration.k8s.io/v1beta1 MutatingWebhookConfiguration is deprecated in v1.16+, unavailable in v1.22+; use admissionregistration.k8s.io/v1 MutatingWebhookConfiguration
W1216 11:47:22.642235   65254 warnings.go:67] rbac.authorization.k8s.io/v1beta1 ClusterRoleBinding is deprecated in v1.17+, unavailable in v1.22+; use rbac.authorization.k8s.io/v1 ClusterRoleBinding
W1216 11:47:22.732542   65254 warnings.go:67] rbac.authorization.k8s.io/v1beta1 RoleBinding is deprecated in v1.17+, unavailable in v1.22+; use rbac.authorization.k8s.io/v1 RoleBinding
W1216 11:47:22.945899   65254 warnings.go:67] admissionregistration.k8s.io/v1beta1 MutatingWebhookConfiguration is deprecated in v1.16+, unavailable in v1.22+; use admissionregistration.k8s.io/v1 MutatingWebhookConfiguration
NAME: vault
LAST DEPLOYED: Wed Dec 16 11:47:21 2020
NAMESPACE: vault
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
Thank you for installing HashiCorp Vault!

Now that you have deployed Vault, you should look over the docs on using
Vault with Kubernetes available here:

https://www.vaultproject.io/docs/


Your release is named vault. To learn more about the release, try:

  $ helm status vault
  $ helm get manifest vault
```


### initialize the first vault

```
kubectl -n vault exec -ti vault-0 -- vault operator init
Unseal Key 1: 7fmkvTIv11QbUhCWeufGyBeBo/08SLqibnJRAJ3MmHpz
Unseal Key 2: PNmQ8eZ32kP3jP7vj3vahKUWBxeDZ8XtW2Jqav4A1k99
Unseal Key 3: FvofYCdiUGiFM249JbP7vuaH/VFcBsu+ZNXvz5vGsd91
Unseal Key 4: M1Bm8b7BmOYxrxq3nqHkFpZ43Ojfg2M10MQ/iGz9HcUU
Unseal Key 5: kkOaFfGZ+jZuSV5gnNA0rddBBSbsDuW2Zf3KtRkZRlxg

Initial Root Token: s.Tv7fxB7Rlkz6pOkTDuTjh9FH

Vault initialized with 5 key shares and a key threshold of 3. Please securely
distribute the key shares printed above. When the Vault is re-sealed,
restarted, or stopped, you must supply at least 3 of these keys to unseal it
before it can start servicing requests.

Vault does not store the generated master key. Without at least 3 key to
reconstruct the master key, Vault will remain permanently sealed!

It is possible to generate new unseal keys, provided you have a quorum of
existing unseal keys shares. See "vault operator rekey" for more information.
```


### unseal the first vault
```
kubectl -n vault exec -ti vault-0 -- vault operator unseal
Unseal Key (will be hidden): 
Key                Value
---                -----
Seal Type          shamir
Initialized        true
Sealed             true
Total Shares       5
Threshold          3
Unseal Progress    1/3
Unseal Nonce       954918f2-ac92-4314-b717-2ead5ae07168
Version            1.5.4
HA Enabled         true

kubectl -n vault exec -ti vault-0 -- vault operator unseal
Unseal Key (will be hidden): 
Key                Value
---                -----
Seal Type          shamir
Initialized        true
Sealed             true
Total Shares       5
Threshold          3
Unseal Progress    2/3
Unseal Nonce       954918f2-ac92-4314-b717-2ead5ae07168
Version            1.5.4
HA Enabled         true

kubectl -n vault exec -ti vault-0 -- vault operator unseal
Unseal Key (will be hidden): 
Key                     Value
---                     -----
Seal Type               shamir
Initialized             true
Sealed                  false
Total Shares            5
Threshold               3
Version                 1.5.4
Cluster Name            vault-cluster-01ea7605
Cluster ID              2368db47-0f05-47cf-50f6-0e99ebb045cc
HA Enabled              true
HA Cluster              n/a
HA Mode                 standby
Active Node Address     <none>
Raft Committed Index    24
Raft Applied Index      24

```

then repeat the same process for the other 2 vaults


### preparing sidecar injection
```
kubectl exec -n vault -it vault-0 -- /bin/sh
export VAULT_TOKEN=YOUR_ROOT_TOKEN_FROM_INIT
vault secrets enable -path=internal kv-v2
vault kv put internal/database/config username="db-readonly-username" password="db-secret-password"
vault kv get internal/database/config
```

### enable kubernetes authentication
```
vault auth enable kubernetes
Success! Enabled kubernetes auth method at: kubernetes/

vault write auth/kubernetes/config \
    token_reviewer_jwt="$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)" \
    kubernetes_host="https://$KUBERNETES_PORT_443_TCP_ADDR:443" \
    kubernetes_ca_cert=@/var/run/secrets/kubernetes.io/serviceaccount/ca.crt
Success! Data written to: auth/kubernetes/config
```


create a policy
```
vault policy write internal-app - <<EOF
path "internal/data/database/config" {
  capabilities = ["read"]
}
EOF
Success! Uploaded policy: internal-app


vault write auth/kubernetes/role/internal-app \
   bound_service_account_names=internal-app \
   bound_service_account_namespaces=pgtest \
   policies=internal-app \
   ttl=72h
```

### create a service account
```
cat service-account-pgtest.yml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: internal-app
```

#### **`deployment-orgchart.yaml`**
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: orgchart
  labels:
    app: orgchart
spec:
  selector:
    matchLabels:
      app: orgchart
  replicas: 1
  template:
    metadata:
      annotations:
      labels:
        app: orgchart
    spec:
      serviceAccountName: internal-app
      containers:
        - name: orgchart
          image: jweissig/app:0.0.1
```

### now lets apply this deployment to our pgtest namespace
```
kubectl apply -n pgtest -f deployment-orgchart.yaml
```


### test for non existant secrets
```
// get a pod name
kubectl get pods -n pgtest -o jsonpath="{.items[0].metadata.name}"
orgchart-7457f8489d-gk4qw

kubectl -n pgtest exec orgchart-7457f8489d-gk4qw -- ls /vault/secrets
ls: /vault/secrets: No such file or directory
command terminated with exit code 1
```


```
cat inject_secret.yaml

spec:
  template:
    metadata:
      annotations:
        vault.hashicorp.com/agent-inject: "true"
        vault.hashicorp.com/role: "internal-app"
        vault.hashicorp.com/agent-inject-secret-database: "internal/data/database/config"
        vault.hashicorp.com/agent-inject-template-database: |
          {{- with secret "internal/data/database/config" -}}
          postgres://{{ .Data.data.username }}:{{ .Data.data.password }}@postgres:5432/mydb?sslmode=disable
          {{- end }}
        vault.hashicorp.com/tls-secret: tls-server
        vault.hashicorp.com/ca-cert: /vault/tls/ca.crt

kubectl patch deployment orgchart --patch "$(cat inject_secret.yaml)" -n pgtest
deployment.apps/orgchart patched

kubectl patch deployment orgchart --patch "$(cat patch-inject-secrets.yaml)" -n pgtest

kubectl patch deployment app --patch "$(cat patch-basic-annotations.yaml)" -n pgtest
```