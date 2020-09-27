from diagrams import Cluster, Diagram, Edge
from diagrams.k8s.network import Service
from diagrams.k8s.compute import Pod
from diagrams.onprem.network import Internet
from diagrams.onprem.network import Internet
from diagrams.k8s.compute import Deploy
from diagrams.k8s.network import Ingress
from diagrams.k8s.podconfig import Secret
from diagrams.k8s.podconfig import ConfigMap
with Diagram("kubernetes deployment nodejs postgresql ingress", show=False):
    with Cluster("Kubernetes Components"):
        with Cluster("Services"):
            service_internal_node = Service("Internal Node Service")
            service_internal_postgres = Service("Internal Postgres Service")
        with Cluster("Ingress"):
            ingress = Ingress("Ingress")
        with Cluster("Pods"):
            postgresql = Pod("Postgresql")
            nodejs = Pod("Nodejs")

        with Cluster("configuration"):
            deployment = Deploy("Deployment")
            configmap = ConfigMap("ConfigMap")
            secret = Secret("Secret")
        deployment >> secret
        deployment >> configmap
        deployment >> Edge(label="defines") >> service_internal_node
        deployment >> Edge(label="defines") >> service_internal_postgres
        nodejs >> service_internal_postgres >> postgresql
    inet = Internet("Internet")
    inet >> ingress >> service_internal_node >> nodejs


