from diagrams import Cluster, Diagram
from diagrams.k8s.infra import Master
from diagrams.k8s.storage import Volume
from diagrams.k8s.podconfig import ConfigMap
from diagrams.k8s.podconfig import Secret
from diagrams.k8s.compute import Pod
from diagrams.k8s.network import Ingress
from diagrams.onprem.network import Internet
from diagrams.k8s.compute import Deployment
from diagrams.k8s.compute import StatefulSet
from diagrams.k8s.infra import Node
from diagrams.k8s.compute import ReplicaSet
from diagrams.k8s.network import Service

with Diagram("kubernetes getting started", show=False):
    node = Node("Node")
    inet = Internet("Kubernetes")
    vol = Volume("Volumes")
    cm = ConfigMap("ConfigMap")
    secret = ConfigMap("Secret")
    pod = ConfigMap("Pod")
    ingress = Ingress("Ingress")
    depl = Deployment("Deployment")
    ss = StatefulSet("StatefulSet")
    service = Service("Service")
    rs = ReplicaSet("Replication")
    node << inet
    pod << inet
    service << inet
    ingress << inet
    rs << inet

    inet >> cm
    inet >> secret
    inet >> vol
    inet >> depl
    inet >> ss

