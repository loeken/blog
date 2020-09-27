from diagrams import Cluster, Diagram, Edge
from diagrams.k8s.compute import Pod
from diagrams.k8s.compute import Deployment
from diagrams.k8s.compute import ReplicaSet
from diagrams.onprem.container import Docker

with Diagram("kubernetes configuration files", show=False):
    depl = Deployment("Deployment")
    rs = ReplicaSet("ReplicaSet")
    pod = Pod("Pod")
    docker = Docker("Container")
    depl >> rs >>  pod >> docker

