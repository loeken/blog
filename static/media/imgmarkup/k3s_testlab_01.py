from diagrams import Cluster, Diagram
from diagrams.onprem.compute import Server
from diagrams.onprem.network import Internet

with Diagram("k3s testlab 01", show=False):
    vpn = Internet("lan")
    with Cluster("k3s master-master-master cluster"):
        virtualbox = [Server("k3s-01"),
                   Server("k3s-02"),
                   Server("k3s-03")]
    virtualbox >> vpn


