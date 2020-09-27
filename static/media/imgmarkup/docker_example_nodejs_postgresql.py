from diagrams import Cluster, Diagram
from diagrams.onprem.compute import Server
from diagrams.onprem.network import Internet

with Diagram("docker_postgresql_nodejs", show=False):
    with Cluster("Docker Host"):
        with Cluster("Docker Container/Network"):
            servers = [Server("postgresql"),Server("nodejs")]



