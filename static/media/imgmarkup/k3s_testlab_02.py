from diagrams import Cluster, Diagram
from diagrams.onprem.compute import Server
from diagrams.onprem.network import Internet

with Diagram("k3s testlab 02", show=False):
    lan = Internet("lan")
    wan = Internet("wan")

    with Cluster("k3s master-master-master cluster"):
        cluster = [Server("k3s-node-01"),
                   Server("k3s-node-02"),
                   Server("k3s-node-03")]
    wan << cluster
    cluster >> lan
    wan


