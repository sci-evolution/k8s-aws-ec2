# AWS Setup Guide for Kubernetes Project (Draft)

## Prerequisites:
- Previous knowledge on AWS;
- An IAM User with the required permissions;

## Steps:
1. Create a "VPC and More" resources (Subnets, Route Tables, Internet Gateways, etc...);
2. Create a Security Group for the Control Plane EC2 (attach it to the above VPC)(see notes below);
3. Create a Security Group for the Worker EC2 (attach it to the above VPC)(see notes below);
4. Create a Security Group for the RDS (attach it to the above VPC);
5. Create a Security Group for the NLB (Network Load Balancer) (attach it to the above VPC);
6. Create a domain at Route53 (which will automaticaly create a Hosted Zone);
7. Create a CA Certificate at ACM (use the above domain to validate);
8. Create en EC2 instance for Control Plane (attach it th the above VPC). Use the Security Group we createc to it;
9. Set Up the Kubernetes Control Plane
    - Use [control-plane](scripts/ec2-control-plane-node.sh) as EC2 User Data or run manually to set up the control plane node.
    - During kubeadm init, use the NLB DNS as the --control-plane-endpoint.
10. Set Up Kubernetes Worker Nodes
    - Use [worker](scripts/ec2-worker-node.sh) as EC2 User Data or run manually to set up each worker node.
    - Join each worker node to the cluster using the kubeadm join command from the control plane output.
11. Deploy Your Application
    - Deploy PostgreSQL using [postgresql](k8s/postgresql.yaml).
    - Deploy your Django app using [django-app](k8s/django-app.yaml).
    - Ensure the Django Service is of type LoadBalancer so AWS provisions an ELB/NLB for external access.

## Notes about Inbound and Outbound Rules for EC2 Security Groups:
   ### Control Plane Nodes
   | Rule Type | Protocol | Port | Source/Destination (Example) | Purpose |
   |-----------|----------|------|-----------------------------|---------|
   | **Inbound** | TCP | 6443 | Worker Nodes' Security Group (`sg-yyyyyyyy`) | Kubernetes API |
   | **Inbound** | TCP | 4240 | Worker Nodes' Security Group (`sg-yyyyyyyy`) | Cilium Health Check |
   | **Inbound** | UDP | 8472 | Worker Nodes' Security Group (`sg-yyyyyyyy`) | VXLAN Overlay (Cilium) |
   | **Inbound** | TCP | 4244 | Worker Nodes' Security Group (`sg-yyyyyyyy`) | Hubble Observability (Optional) |
   | **Inbound** | TCP | 53 | VPC CIDR Block (`10.0.0.0/16`) | DNS Resolution |
   | **Inbound** | UDP | 53 | VPC CIDR Block (`10.0.0.0/16`) | DNS Resolution |
   | **Inbound** | TCP | 22 | Admins' IP Range (`203.0.113.10/32`) | SSH Access |
   | **Inbound** | UDP | 123 | Public NTP Servers (`129.6.15.30/32`) | Network Time Protocol |
   | **Inbound** | TCP | 80 | Public Internet (`0.0.0.0/0`) | HTTP (if needed) |
   | **Inbound** | TCP | 443 | Public Internet (`0.0.0.0/0`) | HTTPS (if needed) |
   | **Outbound** | All | Any | `0.0.0.0/0` | Allow all outgoing traffic |
   
   ### Worker Nodes
   | Rule Type | Protocol | Port | Source/Destination (Example) | Purpose |
   |-----------|----------|------|-----------------------------|---------|
   | **Inbound** | TCP | 4240 | Control Plane Nodes' Security Group (`sg-xxxxxxxx`) | Cilium Health Check |
   | **Inbound** | UDP | 8472 | Control Plane Nodes' Security Group (`sg-xxxxxxxx`) | VXLAN Overlay (Cilium) |
   | **Inbound** | TCP | 4244 | Control Plane Nodes' Security Group (`sg-xxxxxxxx`) | Hubble Observability (Optional) |
   | **Inbound** | TCP | 53 | VPC CIDR Block (`10.0.0.0/16`) | DNS Resolution |
   | **Inbound** | UDP | 53 | VPC CIDR Block (`10.0.0.0/16`) | DNS Resolution |
   | **Inbound** | TCP | 22 | Admins' IP Range (`203.0.113.10/32`) | SSH Access |
   | **Inbound** | UDP | 123 | Public NTP Servers (`129.6.15.30/32`) | Network Time Protocol |
   | **Inbound** | TCP | 80 | Public Internet (`0.0.0.0/0`) | HTTP (if needed) |
   | **Inbound** | TCP | 443 | Public Internet (`0.0.0.0/0`) | HTTPS (if needed) |
   | **Outbound** | All | Any | `0.0.0.0/0` | Allow all outgoing traffic |
