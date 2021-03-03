---
title: "My Road to Self Hosted Kubernetes With K3s_ha Postgresql Cluster Using Helm Chart"
date: 2020-12-17T10:00:43+01:00
draft: false
toc: false
summary: in this round we are going to configure a ha postgresql cluster.
author: loeken
images:
tags:
  - kubernetes
  - k3s
  - debian 10
  - ansible
  - k3sup
---

# Postgresql ha via helm chart

### **`values-production.yaml`**
```
## Global Docker image parameters
## Please, note that this will override the image parameters, including dependencies, configured to use the global value
## Current available global Docker image parameters: imageRegistry, imagePullSecrets and storageClass
##
global:
#   imageRegistry: myRegistryName
#   imagePullSecrets:
#     - myRegistryKeySecretName
  storageClass: rook-ceph-block
#  postgresql:
#    username: customuser
#    password: custompassword
#    database: customdatabase
#    repmgrUsername: repmgruser
#    repmgrPassword: repmgrpassword
#    repmgrDatabase: repmgrdatabase
#    existingSecret: myExistingSecret
#  ldap:
#    bindpw: bindpassword
#    existingSecret: myExistingSecret
  pgpool:
    adminUsername: adminuser
    adminPassword: adminpassword
#    existingSecret: myExistingSecret

## Bitnami PostgreSQL image
## ref: https://hub.docker.com/r/bitnami/postgresql/tags/
##
postgresqlImage:
  registry: docker.io
  repository: bitnami/postgresql-repmgr
  tag: 13.1.0
  ## Specify a imagePullPolicy. Defaults to 'Always' if image tag is 'latest', else set to 'IfNotPresent'
  ## ref: http://kubernetes.io/docs/user-guide/images/#pre-pulling-images
  ##
  pullPolicy: IfNotPresent
  ## Optionally specify an array of imagePullSecrets (secrets must be manually created in the namespace)
  ## ref: https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/
  ##
  # pullSecrets:
  #   - myRegistryKeySecretName

  ## Set to true if you would like to see extra information on logs
  ## ref:  https://github.com/bitnami/minideb-extras/#turn-on-bash-debugging
  ##
  debug: false

## Bitnami Pgpool image
## ref: https://hub.docker.com/r/bitnami/pgpool/tags/
##
pgpoolImage:
  registry: docker.io
  repository: bitnami/pgpool
  tag: 4.2.0-debian-10-r14
  ## Specify a imagePullPolicy. Defaults to 'Always' if image tag is 'latest', else set to 'IfNotPresent'
  ## ref: http://kubernetes.io/docs/user-guide/images/#pre-pulling-images
  ##
  pullPolicy: IfNotPresent
  ## Optionally specify an array of imagePullSecrets (secrets must be manually created in the namespace)
  ## ref: https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/
  ##
  # pullSecrets:
  #   - myRegistryKeySecretName

  ## Set to true if you would like to see extra information on logs
  ## ref:  https://github.com/bitnami/minideb-extras/#turn-on-bash-debugging
  ##
  debug: false

## Bitnami Minideb image
## ref: https://hub.docker.com/r/bitnami/pgpool/tags/
##
volumePermissionsImage:
  registry: docker.io
  repository: bitnami/minideb
  tag: buster
  ## Specify a imagePullPolicy. Defaults to 'Always' if image tag is 'latest', else set to 'IfNotPresent'
  ## ref: http://kubernetes.io/docs/user-guide/images/#pre-pulling-images
  ##
  pullPolicy: Always
  ## Optionally specify an array of imagePullSecrets (secrets must be manually created in the namespace)
  ## ref: https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/
  ##
  # pullSecrets:
  #   - myRegistryKeySecretName

## Bitnami PostgreSQL Prometheus exporter image
## ref: https://hub.docker.com/r/bitnami/pgpool/tags/
##
metricsImage:
  registry: docker.io
  repository: bitnami/postgres-exporter
  tag: 0.8.0-debian-10-r298
  ## Specify a imagePullPolicy. Defaults to 'Always' if image tag is 'latest', else set to 'IfNotPresent'
  ## ref: http://kubernetes.io/docs/user-guide/images/#pre-pulling-images
  ##
  pullPolicy: IfNotPresent
  ## Optionally specify an array of imagePullSecrets (secrets must be manually created in the namespace)
  ## ref: https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/
  ##
  # pullSecrets:
  #   - myRegistryKeySecretName

  ## Set to true if you would like to see extra information on logs
  ## ref:  https://github.com/bitnami/minideb-extras/#turn-on-bash-debugging
  ##
  debug: false

## String to partially override common.names.fullname template (will maintain the release name)
##
# nameOverride:

## String to fully override common.names.fullname template
##
# fullnameOverride:

## Kubernetes Cluster Domain
##
clusterDomain: cluster.local

## Common annotations to add to all resources (sub-charts are not considered). Evaluated as a template
##
commonAnnotations: {}

## Common labels to add to all resources (sub-charts are not considered). Evaluated as a template
##
commonLabels: {}

## PostgreSQL parameters
##
postgresql:
  ## Labels to add to the StatefulSet. Evaluated as template
  ##
  labels: {}

  ## Labels to add to the StatefulSet pods. Evaluated as template
  ##
  podLabels: {}

  ## Number of replicas to deploy
  ##
  replicaCount: 3

  ## Update strategy for PostgreSQL statefulset
  ## ref: https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/#update-strategies
  ##
  updateStrategyType: RollingUpdate

  ## Additional pod annotations
  ## ref: https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/
  ##
  podAnnotations: {}

  ## Pod priority class
  ## Ref: https://kubernetes.io/docs/concepts/configuration/pod-priority-preemption/
  ##
  priorityClassName: ""

  ## PostgreSQL pod affinity preset
  ## ref: https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#inter-pod-affinity-and-anti-affinity
  ## Allowed values: soft, hard
  ##
  podAffinityPreset: ""

  ## PostgreSQL pod anti-affinity preset
  ## ref: https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#inter-pod-affinity-and-anti-affinity
  ## Allowed values: soft, hard
  ##
  podAntiAffinityPreset: soft

  ## PostgreSQL node affinity preset
  ## ref: https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#node-affinity
  ## Allowed values: soft, hard
  ##
  nodeAffinityPreset:
    ## Node affinity type
    ## Allowed values: soft, hard
    type: ""
    ## Node label key to match
    ## E.g.
    ## key: "kubernetes.io/e2e-az-name"
    ##
    key: ""
    ## Node label values to match
    ## E.g.
    ## values:
    ##   - e2e-az1
    ##   - e2e-az2
    ##
    values: []

  ## Affinity for PostgreSQL pods assignment
  ## ref: https://kubernetes.io/docs/concepts/configuration/assign-pod-node/#affinity-and-anti-affinity
  ## Note: postgresql.podAffinityPreset, postgresql.podAntiAffinityPreset, and postgresql.nodeAffinityPreset will be ignored when it's set
  ##
  affinity: {}

  ## Node labels for PostgreSQL pods assignment
  ## ref: https://kubernetes.io/docs/user-guide/node-selection/
  ##
  nodeSelector: {}

  ## Tolerations for PostgreSQL pods assignment
  ## ref: https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/
  ##
  tolerations: []

  ## K8s Security Context
  ## https://kubernetes.io/docs/tasks/configure-pod-container/security-context/
  ##
  securityContext:
    enabled: true
    fsGroup: 1001

  ## Container Security Context
  ## https://kubernetes.io/docs/tasks/configure-pod-container/security-context/
  ##
  containerSecurityContext:
    enabled: true
    runAsUser: 1001

  ## Custom Liveness probe
  ##
  customLivenessProbe: {}

  ## Custom Readiness probe
  ##
  customReadinessProbe: {}

  ## Container command (using container default if not set)
  ##
  command:

  ## Container args (using container default if not set)
  ##
  args:

  ## lifecycleHooks for the container to automate configuration before or after startup.
  ##
  lifecycleHooks:

  ## An array to add extra env vars
  ## For example:
  ##
  extraEnvVars: []
  #  - name: BEARER_AUTH
  #    value: true

  ## ConfigMap with extra environment variables
  ##
  extraEnvVarsCM:

  ## Secret with extra environment variables
  ##
  extraEnvVarsSecret:

  ## Extra volumes to add to the deployment
  ##
  extraVolumes: []

  ## Extra volume mounts to add to the container
  ##
  extraVolumeMounts: []

  ## Extra init containers to add to the deployment
  ##
  initContainers: []

  ## Extra sidecar containers to add to the deployment
  ##
  sidecars: []

  ## PostgreSQL containers' resource requests and limits
  ## ref: http://kubernetes.io/docs/user-guide/compute-resources/
  ##
  resources:
    # We usually recommend not to specify default resources and to leave this as a conscious
    # choice for the user. This also increases chances charts run on environments with little
    # resources, such as Minikube. If you do want to specify resources, uncomment the following
    # lines, adjust them as necessary, and remove the curly braces after 'resources:'.
    limits: {}
    #   cpu: 250m
    #   memory: 256Mi
    requests: {}
    #   cpu: 250m
    #   memory: 256Mi

  ## PostgreSQL container's liveness and readiness probes
  ## ref: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#container-probes
  ##
  livenessProbe:
    enabled: true
    initialDelaySeconds: 30
    periodSeconds: 10
    timeoutSeconds: 5
    successThreshold: 1
    failureThreshold: 6
  readinessProbe:
    enabled: true
    initialDelaySeconds: 5
    periodSeconds: 10
    timeoutSeconds: 5
    successThreshold: 1
    failureThreshold: 6

  ## Pod disruption budget configuration
  ##
  pdb:
    ## Specifies whether a Pod disruption budget should be created
    ##
    create: false
    minAvailable: 1
    # maxUnavailable: 1

  ## PostgreSQL configuration parameters
  ##
  username: postgres
  password: testing
  # database:

  ## PostgreSQL password using existing secret
  # existingSecret: secret

  ## PostgreSQL admin password (used when `postgresql.username` is not `postgres`)
  ## ref: https://github.com/bitnami/bitnami-docker-postgresql/blob/master/README.md#creating-a-database-user-on-first-run (see note!)
  # postgresPassword:

  ## Mount PostgreSQL secret as a file instead of passing environment variable
  # usePasswordFile: false

  ## Upgrade repmgr extension in the database
  ##
  upgradeRepmgrExtension: false

  ## Configures pg_hba.conf to trust every user
  ##
  pgHbaTrustAll: false

  ## Synchronous replication
  ##
  syncReplication: false

  ## Repmgr configuration parameters
  ##
  repmgrUsername: repmgr
  repmgrPassword: testing
  repmgrDatabase: repmgr
  repmgrLogLevel: NOTICE
  repmgrConnectTimeout: 5
  repmgrReconnectAttempts: 3
  repmgrReconnectInterval: 5

  ## Audit settings
  ## https://github.com/bitnami/bitnami-docker-postgresql#auditing
  ##
  audit:
    ## Log client hostnames
    ##
    logHostname: true
    ## Log connections to the server
    ##
    logConnections: true
    ## Log disconnections
    ##
    logDisconnections: true
    ## Operation to audit using pgAudit (default if not set)
    ##
    pgAuditLog: ""
    ## Log catalog using pgAudit
    ##
    pgAuditLogCatalog: "off"
    ## Log level for clients
    ##
    clientMinMessages: error
    ## Template for log line prefix (default if not set)
    ##
    logLinePrefix: ""
    ## Log timezone
    ##
    logTimezone: ""

  ## Shared preload libraries
  ##
  sharedPreloadLibraries: "pgaudit, repmgr"

  ## Maximum total connections
  ##
  maxConnections:

  ## Maximum connections for the postgres user
  ##
  postgresConnectionLimit:

  ## Maximum connections for the created user
  ##
  dbUserConnectionLimit:

  ## TCP keepalives interval
  ##
  tcpKeepalivesInterval:

  ## TCP keepalives idle
  ##
  tcpKeepalivesIdle:

  ## TCP keepalives count
  ##
  tcpKeepalivesCount:

  ## Statement timeout
  ##
  statementTimeout:

  ## Remove pg_hba.conf lines with the following comma-separated patterns
  ## (cannot be used with custom pg_hba.conf)
  ##
  pghbaRemoveFilters:

  ## Extra init containers
  ## Example
  ##
  ## extraInitContainers:
  ##   - name: do-something
  ##     image: busybox
  ##     command: ['do', 'something']
  ##
  extraInitContainers: []

  ## Repmgr configuration
  ## Specify content for repmgr.conf
  ## Default: do not create repmgr.conf
  ## Alternatively, you can put your repmgr.conf under the files/ directory
  ## ref: https://github.com/bitnami/bitnami-docker-postgresql-repmgr#configuration-file
  ##
  # repmgrConfiguration: |-
  ## PostgreSQL configuration
  ## Specify runtime configuration parameters as a dict, using camelCase, e.g.
  ## {"sharedBuffers": "500MB"}
  ## Alternatively, you can put your postgresql.conf under the files/ directory
  ## ref: https://github.com/bitnami/bitnami-docker-postgresql-repmgr#configuration-file
  ##
  # configuration:
  ## PostgreSQL client authentication configuration
  ## Specify content for pg_hba.conf
  ## Default: do not create pg_hba.conf
  ## Alternatively, you can put your pg_hba.conf under the files/ directory
  ## ref: https://github.com/bitnami/bitnami-docker-postgresql-repmgr#configuration-file
  ##
  # pgHbaConfiguration: |-
  #   local all all trust
  #   host all all localhost trust
  #   host mydatabase mysuser 192.168.0.0/24 md5
  ## ConfigMap with PostgreSQL configuration
  ## NOTE: This will override repmgrConfiguration, configuration and pgHbaConfiguration
  ##
  # configurationCM:
  ## PostgreSQL extended configuration
  ## As above, but _appended_ to the main configuration
  ## Alternatively, you can put your *.conf under the files/conf.d/ directory
  ## ref: https://github.com/bitnami/bitnami-docker-postgresql-repmgr#allow-settings-to-be-loaded-from-files-other-than-the-default-postgresqlconf
  ##
  # extendedConf:
  ## ConfigMap with PostgreSQL extended configuration
  ## NOTE: This will override extendedConf
  ##
  # extendedConfCM:
  ## initdb scripts
  ## Specify dictionary of scripts to be run at first boot
  ## Alternatively, you can put your scripts under the files/docker-entrypoint-initdb.d directory
  ##
  # initdbScripts:
  #   my_init_script.sh: |
  #      #!/bin/sh
  #      echo "Do something."
  ## ConfigMap with scripts to be run at first boot
  ## NOTE: This will override initdbScripts
  ##
  # initdbScriptsCM:
  ## Secret with scripts to be run at first boot
  ## Note: can be used with initdbScriptsCM or initdbScripts
  ##
  # initdbScriptsSecret:

## Pgpool parameters
##
pgpool:
  ## Additional users that will be performing connections to the database using
  ## pgpool. Use this property in order to create new user/password entries that
  ## will be appended to the "pgpool_passwd" file
  ##
  customUsers:
  ##  Comma or semicolon separated list of postgres usernames
    usernames: 'user01;user02'

  ##  Comma or semicolon separated list of the associated passwords for the
  ##  users above
    passwords: 'pass01;pass02'

  ## Alternatively, you can provide the name of a secret containing this information.
  ## The secret must contain the keys "usernames" and "passwords" respectively.
  ##
  customUsersSecret:

  ## Database to perform streaming replication checks
  ##
  srCheckDatabase: postgres

  ## Labels to add to the Deployment. Evaluated as template
  ##
  labels: {}

  ## Labels to add to the pods. Evaluated as template
  ##
  podLabels: {}

  ## Number of replicas to deploy
  ##
  replicaCount: 2

  ## Additional pod annotations
  ## ref: https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/
  ##
  podAnnotations: {}

  ## Pod priority class
  ## Ref: https://kubernetes.io/docs/concepts/configuration/pod-priority-preemption/
  ##
  priorityClassName: ""

  ## Pgpool pod affinity preset
  ## ref: https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#inter-pod-affinity-and-anti-affinity
  ## Allowed values: soft, hard
  ##
  podAffinityPreset: ""

  ## Pgpool pod anti-affinity preset
  ## ref: https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#inter-pod-affinity-and-anti-affinity
  ## Allowed values: soft, hard
  ##
  podAntiAffinityPreset: soft

  ## Pgpool node affinity preset
  ## ref: https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#node-affinity
  ## Allowed values: soft, hard
  ##
  nodeAffinityPreset:
    ## Node affinity type
    ## Allowed values: soft, hard
    type: ""
    ## Node label key to match
    ## E.g.
    ## key: "kubernetes.io/e2e-az-name"
    ##
    key: ""
    ## Node label values to match
    ## E.g.
    ## values:
    ##   - e2e-az1
    ##   - e2e-az2
    ##
    values: []

  ## Affinity for Pgpool pods assignment
  ## ref: https://kubernetes.io/docs/concepts/configuration/assign-pod-node/#affinity-and-anti-affinity
  ## Note: pgpool.podAffinityPreset, pgpool.podAntiAffinityPreset, and pgpool.nodeAffinityPreset will be ignored when it's set
  ##
  affinity: {}

  ## Node labels for Pgpool pods assignment
  ## ref: https://kubernetes.io/docs/user-guide/node-selection/
  ##
  nodeSelector: {}

  ## Tolerations for Pgpool pods assignment
  ## ref: https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/
  ##
  tolerations: []

  ## K8s Security Context
  ## https://kubernetes.io/docs/tasks/configure-pod-container/security-context/
  ##
  securityContext:
    enabled: true
    fsGroup: 1001

  ## Container Security Context
  ## https://kubernetes.io/docs/tasks/configure-pod-container/security-context/
  ##
  containerSecurityContext:
    enabled: true
    runAsUser: 1001

  ## Pgpool containers' resource requests and limits
  ## ref: http://kubernetes.io/docs/user-guide/compute-resources/
  ##
  resources:
    # We usually recommend not to specify default resources and to leave this as a conscious
    # choice for the user. This also increases chances charts run on environments with little
    # resources, such as Minikube. If you do want to specify resources, uncomment the following
    # lines, adjust them as necessary, and remove the curly braces after 'resources:'.
    limits: {}
    #   cpu: 250m
    #   memory: 256Mi
    requests: {}
    #   cpu: 250m
    #   memory: 256Mi

  ## Pgpool container's liveness and readiness probes
  ## ref: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#container-probes
  ##
  livenessProbe:
    enabled: true
    initialDelaySeconds: 30
    periodSeconds: 10
    timeoutSeconds: 5
    successThreshold: 1
    failureThreshold: 5
  readinessProbe:
    enabled: true
    initialDelaySeconds: 5
    periodSeconds: 5
    timeoutSeconds: 5
    successThreshold: 1
    failureThreshold: 5

  ## Pod disruption budget configuration
  ##
  pdb:
    ## Specifies whether a Pod disruption budget should be created
    ##
    create: false
    minAvailable: 1
    # maxUnavailable: 1
    ## Custom Liveness probe
  ##
  customLivenessProbe: {}

  ## Custom Readiness probe
  ##
  customReadinessProbe: {}

  ## Container command (using container default if not set)
  ##
  command:

  ## Container args (using container default if not set)
  ##
  args:

  ## lifecycleHooks for the container to automate configuration before or after startup.
  ##
  lifecycleHooks:

  ## An array to add extra env vars
  ## For example:
  ##
  extraEnvVars: []
  #  - name: BEARER_AUTH
  #    value: true

  ## ConfigMap with extra environment variables
  ##
  extraEnvVarsCM:

  ## Secret with extra environment variables
  ##
  extraEnvVarsSecret:

  ## Extra volumes to add to the deployment
  ##
  extraVolumes: []

  ## Extra volume mounts to add to the container
  ##
  extraVolumeMounts: []

  ## Extra init containers to add to the deployment
  ##
  initContainers: []

  ## Extra sidecar containers to add to the deployment
  ##
  sidecars: []

  ## strategy used to replace old Pods by new ones
  ## ref: https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#strategy
  ##
  updateStrategy: {}

  ## minReadySeconds to avoid killing pods before we are ready
  ##
  # minReadySeconds: 0

  ## Credentials for the pgpool administrator
  ##
  adminUsername: admin
  adminPassword: testing

  ## Log all client connections (PGPOOL_ENABLE_LOG_CONNECTIONS)
  ## ref: https://github.com/bitnami/bitnami-docker-pgpool#configuration
  ##
  logConnections: true

  ## Log the client hostname instead of IP address (PGPOOL_ENABLE_LOG_HOSTNAME)
  ## ref: https://github.com/bitnami/bitnami-docker-pgpool#configuration
  ##
  logHostname: true

  ## Log every SQL statement for each DB node separately (PGPOOL_ENABLE_LOG_PER_NODE_STATEMENT)
  ## ref: https://github.com/bitnami/bitnami-docker-pgpool#configuration
  ##
  logPerNodeStatement: true

  ## Format of the log entry lines (PGPOOL_LOG_LINE_PREFIX)
  ## ref: https://github.com/bitnami/bitnami-docker-pgpool#configuration
  ## ref: https://www.pgpool.net/docs/latest/en/html/runtime-config-logging.html
  ##
  logLinePrefix:

  ## Log level for clients
  ## ref: https://github.com/bitnami/bitnami-docker-pgpool#configuration
  ##
  clientMinMessages: error

  ## The number of preforked Pgpool-II server processes. It is also the concurrent
  ## connections limit to Pgpool-II from clients. Must be a positive integer. (PGPOOL_NUM_INIT_CHILDREN)
  ## ref: https://github.com/bitnami/bitnami-docker-pgpool#configuration
  ##
  numInitChildren:

  ## The maximum number of cached connections in each child process (PGPOOL_MAX_POOL)
  ## ref: https://github.com/bitnami/bitnami-docker-pgpool#configuration
  ##
  maxPool:

  ## The maximum number of client connections in each child process (PGPOOL_CHILD_MAX_CONNECTIONS)
  ## ref: https://github.com/bitnami/bitnami-docker-pgpool#configuration
  ##
  childMaxConnections:

  ## The time in seconds to terminate a Pgpool-II child process if it remains idle (PGPOOL_CHILD_LIFE_TIME)
  ## ref: https://github.com/bitnami/bitnami-docker-pgpool#configuration
  ##
  childLifeTime:

  ## The time in seconds to disconnect a client if it remains idle since the last query (PGPOOL_CLIENT_IDLE_LIMIT)
  ## ref: https://github.com/bitnami/bitnami-docker-pgpool#configuration
  ##
  clientIdleLimit:

  ## The time in seconds to terminate the cached connections to the PostgreSQL backend (PGPOOL_CONNECTION_LIFE_TIME)
  ## ref: https://github.com/bitnami/bitnami-docker-pgpool#configuration
  ##
  connectionLifeTime:

  ## Use Pgpool Load-Balancing
  ##
  useLoadBalancing: true

  ## Pgpool configuration
  ## Specify content for pgpool.conf
  ## Alternatively, you can put your pgpool.conf under the files/ directory
  ## ref: https://github.com/bitnami/bitnami-docker-pgpool#configuration-file
  ##
  # configuration:

  ## ConfigMap with Pgpool configuration
  ## NOTE: This will override pgpool.configuration parameter
  ##
  # configurationCM:

  ## initdb scripts
  ## Specify dictionary of scripts to be run every time Pgpool container is initialized
  ## Alternatively, you can put your scripts under the files/pgpool-entrypoint-initdb.d directory
  ##
  # initdbScripts:
  #   my_init_script.sh: |
  #      #!/bin/sh
  #      echo "Do something."

  ## ConfigMap with scripts to be run every time Pgpool container is initialized
  ## NOTE: This will override pgpool.initdbScripts
  ##
  # initdbScriptsCM:

  ## Secret with scripts to be run at first boot
  ## Note: can be used with initdbScriptsCM or initdbScripts
  ##
  # initdbScriptsSecret:

  ##
  ## TLS configuration
  ##
  tls:
    ## Enable TLS traffic
    ##
    enabled: false
    ##
    ## Whether to use the server's TLS cipher preferences rather than the client's.
    ##
    preferServerCiphers: true
    ##
    ## Name of the Secret that contains the certificates
    ##
    certificatesSecret: ""
    ##
    ## Certificate filename
    ##
    certFilename: ""
    ##
    ## Certificate Key filename
    ##
    certKeyFilename: ""
    ##
    ## CA Certificate filename
    ## If provided, PgPool will authenticate TLS/SSL clients by requesting them a certificate
    ## ref: https://www.pgpool.net/docs/latest/en/html/runtime-ssl.html
    ##
    certCAFilename:

## LDAP parameters
##
ldap:
  enabled: false
  ## Retrieve LDAP bindpw from existing secret
  ##
  # existingSecret: myExistingSecret
  uri:
  base:
  binddn:
  bindpw:
  bslookup:
  scope:
  tlsReqcert:
  nssInitgroupsIgnoreusers: root,nslcd

## Init Container parameters
##
volumePermissions:
  enabled: false
  ## K8s Security Context
  ## https://kubernetes.io/docs/tasks/configure-pod-container/security-context/
  ##
  securityContext:
    runAsUser: 0
  ## Init container' resource requests and limits
  ## ref: http://kubernetes.io/docs/user-guide/compute-resources/
  ##
  resources:
    # We usually recommend not to specify default resources and to leave this as a conscious
    # choice for the user. This also increases chances charts run on environments with little
    # resources, such as Minikube. If you do want to specify resources, uncomment the following
    # lines, adjust them as necessary, and remove the curly braces after 'resources:'.
    limits: {}
    #   cpu: 100m
    #   memory: 128Mi
    requests: {}
    #   cpu: 100m
    #   memory: 128Mi

## PostgreSQL Prometheus exporter parameters
##
metrics:
  enabled: true
  ## K8s Security Context
  ## https://kubernetes.io/docs/tasks/configure-pod-container/security-context/
  ##
  securityContext:
    enabled: true
    runAsUser: 1001

  ## Prometheus exporter containers' resource requests and limits
  ## ref: http://kubernetes.io/docs/user-guide/compute-resources/
  ##
  resources:
    # We usually recommend not to specify default resources and to leave this as a conscious
    # choice for the user. This also increases chances charts run on environments with little
    # resources, such as Minikube. If you do want to specify resources, uncomment the following
    # lines, adjust them as necessary, and remove the curly braces after 'resources:'.
    limits: {}
    #   cpu: 250m
    #   memory: 256Mi
    requests: {}
    #   cpu: 250m
    #   memory: 256Mi

  ## Prometheus exporter container's liveness and readiness probes
  ## ref: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#container-probes
  ##
  livenessProbe:
    enabled: true
    initialDelaySeconds: 30
    periodSeconds: 10
    timeoutSeconds: 5
    successThreshold: 1
    failureThreshold: 6
  readinessProbe:
    enabled: true
    initialDelaySeconds: 5
    periodSeconds: 10
    timeoutSeconds: 5
    successThreshold: 1
    failureThreshold: 6

  ## Annotations for Prometheus exporter
  ##
  annotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "9187"

  ## Enable this if you're using Prometheus Operator
  ##
  serviceMonitor:
    enabled: false
    ## Specify a namespace if needed
    # namespace: monitoring
    # fallback to the prometheus default unless specified
    # interval: 10s
    # scrapeTimeout: 10s
    ## Defaults to what's used if you follow CoreOS [Prometheus Install Instructions](https://github.com/bitnami/charts/tree/master/bitnami/prometheus-operator#tldr)
    ## [Prometheus Selector Label](https://github.com/bitnami/charts/tree/master/bitnami/prometheus-operator#prometheus-operator-1)
    ## [Kube Prometheus Selector Label](https://github.com/bitnami/charts/tree/master/bitnami/prometheus-operator#exporters)
    ##
    selector:
      prometheus: kube-prometheus

    ## RelabelConfigs to apply to samples before scraping
    ## ref: https://github.com/coreos/prometheus-operator/blob/master/Documentation/api.md#relabelconfig
    ## Value is evalued as a template
    ##
    relabelings: []

    ## MetricRelabelConfigs to apply to samples before ingestion
    ## ref: https://github.com/coreos/prometheus-operator/blob/master/Documentation/api.md#relabelconfig
    ## Value is evalued as a template
    ##
    metricRelabelings: []

## Persistence parameters
##
persistence:
  enabled: true
  ## A manually managed Persistent Volume and Claim
  ## If defined, PVC must be created manually before volume will be bound
  ## The value is evaluated as a template
  ##
  # existingClaim:
  ## Persistent Volume Storage Class
  ## If defined, storageClassName: <storageClass>
  ## If set to "-", storageClassName: "", which disables dynamic provisioning
  ## If undefined (the default) or set to null, no storageClassName spec is
  ## set, choosing the default provisioner.
  ##
  storageClass: "rook-ceph-block"
  ## The path the volume will be mounted at, useful when using different
  ## PostgreSQL images.
  ##
  mountPath: /bitnami/postgresql
  ## Persistent Volume Access Mode
  ##
  accessModes:
    - ReadWriteOnce
  ## Persistent Volume Claim size
  ##
  size: 8Gi
  ## Persistent Volume Claim annotations
  ##
  annotations: {}
  ## selector can be used to match an existing PersistentVolume
  ## selector:
  ##   matchLabels:
  ##     app: my-app
  selector: {}

## PgPool service parameters
##
service:
  ## Service type
  ##
  type: ClusterIP
  ## Service Port
  ##
  port: 5432
  ## Specify the nodePort value for the LoadBalancer and NodePort service types.
  ## ref: https://kubernetes.io/docs/concepts/services-networking/service/#type-nodeport
  ##
  # nodePort:
  ## Set the LoadBalancer service type to internal only.
  ## ref: https://kubernetes.io/docs/concepts/services-networking/service/#internal-load-balancer
  ##
  # loadBalancerIP:
  ## Load Balancer sources
  ## https://kubernetes.io/docs/tasks/access-application-cluster/configure-cloud-provider-firewall/#restrict-access-for-loadbalancer-service
  ##
  # loadBalancerSourceRanges:
  # - 10.10.10.0/24
  ## Set the Cluster IP to use
  ## ref: https://kubernetes.io/docs/concepts/services-networking/service/#choosing-your-own-ip-address
  ##
  # clusterIP: None
  ## Provide any additional annotations which may be required
  ##
  annotations: {}

## NetworkPolicy parameters
##
networkPolicy:
  enabled: true

  ## The Policy model to apply. When set to false, only pods with the correct
  ## client labels will have network access to the port PostgreSQL is listening
  ## on. When true, PostgreSQL will accept connections from any source
  ## (with the correct destination port).
  ##
  allowExternal: false

## Array with extra yaml to deploy with the chart. Evaluated as a template
##
extraDeploy: []
```

### install postgresql
```
helm install pgtest -n pgtest bitnami/postgresql-ha -f values-production.yaml
```