from diagrams import Cluster, Diagram
from diagrams.onprem.compute import Server
from diagrams.onprem.network import Internet

with Diagram("k3s testlab 01", show=False):
    ingress = Internet("failover ip")
    vpn = Internet("vpn")
    with Cluster("k3s master-master-master cluster"):
        proxmox = [ingress >> Server("k3s-01"),
                   Server("k3s-02"),
                   Server("k3s-03")]
    proxmox >> vpn


