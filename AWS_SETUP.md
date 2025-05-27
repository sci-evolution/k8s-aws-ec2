# AWS Setup Guide for Kubernetes Project

## 1. Launch EC2 Instances
   - Launch control plane and worker nodes in the same VPC/subnet.
   - Assign security groups with correct inbound rules (see [control-plane](ec2-control-plane-node.sh) and [worker](ec2-worker-node.sh)).

## 2. (Optional) Set Up Route53 for Custom Domain
   - If you already have a custom domain managed by another DNS provider, you can skip this step.
   - If not, create a hosted zone for your domain in Route53.
   - You will use this domain in the ACM certificate request in the next step.

## 3. Create an ACM Certificate
   - Go to the ACM console and request a public certificate for your domain (e.g., app.example.com).
   - Validate the certificate via DNS or email as instructed by ACM.
   - If your DNS is managed outside Route53, add the validation records at your DNS provider.

## 4. Create a Network Load Balancer (NLB)
   - In the EC2 console, create a new NLB. Ensure it is in the same VPC as your EC2 instances.
   - Add listeners for HTTP (80) and HTTPS (443).
   - Create a target group for your control plane node(s) (port 6443 for Kubernetes API, and for app traffic as needed).
   - Register your EC2 instances as targets.
   - Associate the ACM certificate with the HTTPS listener.
   - If using Route53, create an A record (Alias) or CNAME pointing to the NLB DNS name. If using another DNS provider, create the record there.
   - You will use this NLB DNS name as the control plane endpoint in the next step.

## 5. Set Up the Kubernetes Control Plane
   - Use [control-plane](ec2-control-plane-node.sh) as EC2 User Data or run manually to set up the control plane node.
   - During kubeadm init, use the NLB DNS as the --control-plane-endpoint.

## 6. Set Up Kubernetes Worker Nodes
   - Use [worker](ec2-worker-node.sh) as EC2 User Data or run manually to set up each worker node.
   - Join each worker node to the cluster using the kubeadm join command from the control plane output.

## 7. Deploy Your Application
   - Deploy PostgreSQL using [postgresql](postgresql.yaml).
   - Deploy your Django app using [django-app](django-app.yaml).
   - Ensure the Django Service is of type LoadBalancer so AWS provisions an ELB/NLB for external access.
