from diagrams import Cluster, Diagram, Edge
from diagrams.k8s.network import Service
from diagrams.k8s.compute import Pod
from diagrams.onprem.network import Internet
from diagrams.onprem.network import Internet
from diagrams.k8s.compute import Deploy
from diagrams.k8s.podconfig import Secret
from diagrams.k8s.podconfig import ConfigMap
with Diagram("kubernetes deployment nodejs postgresql", show=False):
    with Cluster("Kubernetes Components"):
        with Cluster("Services"):
            service_internal = Service("Internal Service")
            service_external = Service("External Service")
        with Cluster("Pods"):
            postgresql = Pod("Postgresql")
            nodejs = Pod("Nodejs")

        with Cluster("configuration"):
            deployment = Deploy("Deployment")
            configmap = ConfigMap("ConfigMap")
            secret = Secret("Secret")
        deployment >> secret
        deployment >> configmap
        deployment >> Edge(label="defines") >> service_internal
        deployment >> Edge(label="defines") >> service_external
        nodejs >> service_internal >> postgresql
    inet = Internet("Internet")
    inet >> service_external >> nodejs


