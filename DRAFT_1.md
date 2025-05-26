# Kubernetes: Step-by-Step Guide for AWS EC2

This guide will help you set up a 3-node Kubernetes (k8s) cluster on AWS EC2 instances. Each command is explained for clarity. All steps are tailored for EC2 and AWS best practices.

---

## AWS EC2 Prerequisites
Before starting, ensure you:
- Launch all EC2 instances in the same VPC and subnet (or ensure routing between subnets).
- Assign security groups to your instances with the same rules as described in the "Required Network Ports (OS Firewall)" section below.
- Use private IPs for inter-node communication (handled automatically by AWS when using the same VPC/subnet).
- (Optional) Tag your instances for easier management.

---

## Load Balancing (Highly Available Control Plane)
- For production/high availability, use an AWS Network Load Balancer (NLB) in front of your control plane nodes, forwarding TCP 6443 to all control plane nodes.
- Point your kubeconfig to the NLB’s DNS name for API access.

---

## Required Network Ports (OS Firewall)
If you use UFW on your EC2 instances, configure as follows:

#### Control Plane Node
```bash
# Set default policies
ufw default deny incoming
ufw default allow outgoing
ufw default deny routed

# Allow required ports
ufw allow 6443/tcp         # Kubernetes API
ufw allow 4240/tcp         # Cilium health
ufw allow 8472/udp         # VXLAN (if overlay)
ufw allow 30000:32767/tcp  # NodePort
ufw allow 30000:32767/udp  # NodePort
ufw allow 4244/tcp         # Hubble (optional)
ufw allow 2379/tcp         # etcd (if external)
ufw allow 2379/udp         # etcd (if external)
ufw allow 53/tcp           # DNS
ufw allow 53/udp           # DNS
ufw allow 22/tcp           # SSH
ufw allow 123/udp          # NTP
ufw allow 80/tcp           # HTTP (if needed)
ufw allow 443/tcp          # HTTPS (if needed)
ufw allow proto icmp       # ICMP

# Enable UFW
ufw enable
```

#### Worker Node
```bash
# Set default policies
ufw default deny incoming
ufw default allow outgoing
ufw default deny routed

# Allow required ports
ufw allow 4240/tcp         # Cilium health
ufw allow 8472/udp         # VXLAN (if overlay)
ufw allow 30000:32767/tcp  # NodePort
ufw allow 30000:32767/udp  # NodePort
ufw allow 4244/tcp         # Hubble (optional)
ufw allow 53/tcp           # DNS
ufw allow 53/udp           # DNS
ufw allow 22/tcp           # SSH
ufw allow 123/udp          # NTP
ufw allow 80/tcp           # HTTP (if needed)
ufw allow 443/tcp          # HTTPS (if needed)
ufw allow proto icmp       # ICMP

# Enable UFW
ufw enable
```

> **Note:** UFW rules are persistent and will remain after a system restart. Always ensure SSH is allowed before enabling UFW to avoid locking yourself out.

---

## Become Root User
Switch to the root user to ensure all commands run with the necessary privileges:
```bash
sudo -i
```
- `sudo -i`: Opens a root shell. All subsequent commands should be run as root unless specified otherwise.

---

## 1. Disable Swap (Required by Kubernetes)
```bash
swapoff -a
sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab
```
- Disables swap immediately and comments out swap in `/etc/fstab` to prevent it from being enabled after reboot.

---

## 2. Enable Required Kernel Modules
```bash
cat <<EOF | tee /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF

modprobe overlay
modprobe br_netfilter
```
- Loads `overlay` and `br_netfilter` modules now and at boot.

---

## 3. Set Kernel Parameters for Kubernetes Networking
```bash
cat <<EOF | tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables  = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward                 = 1
EOF

sysctl --system
```
- Configures sysctl for network bridging and forwarding, required for Kubernetes networking.

---

## 4. Install Container Runtime (containerd)
```bash
apt-get update && apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

apt-get update && apt-get install -y containerd.io

mkdir -p /etc/containerd
containerd config default | tee /etc/containerd/config.toml
sed -i 's/SystemdCgroup = false/SystemdCgroup = true/g' /etc/containerd/config.toml
systemctl restart containerd
```
- Installs dependencies, adds Docker's GPG key and repo, installs `containerd`, generates default config, enables systemd cgroup driver, and restarts containerd.

---

## 5. Install Kubernetes Components
```bash
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.32/deb/Release.key | gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg

echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.32/deb/ /' | tee /etc/apt/sources.list.d/kubernetes.list

apt-get update
apt-get install -y kubelet kubeadm kubectl
apt-mark hold kubelet kubeadm kubectl
systemctl enable --now kubelet
```
- Adds Kubernetes apt repo, installs `kubelet`, `kubeadm`, and `kubectl`, holds their versions, and enables kubelet.

---

## 6. Initialize the Control Plane (Run on Master Node Only)
First, run as root:
```bash
kubeadm init
```
- Initializes the Kubernetes control plane. This command will output a `kubeadm join` command for worker nodes.
- If using a load balancer, set `--control-plane-endpoint <NLB-DNS-or-IP>:6443`.

Switch back to your regular user (e.g., `ubuntu`) to set up kubeconfig for kubectl access:
```bash
exit  # Exit root shell to return to your normal user

mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
export KUBECONFIG=$HOME/.kube/config
```
- Sets up kubeconfig for kubectl access as the current user.

---

## 7. Verify Cluster Status
```bash
kubectl get nodes

# Wait until the cluster is ready
while [ $? -ne 0 ]; do
  sleep 10
  kubectl get nodes
done
```
- Checks if the cluster is up and nodes are ready. The loop waits until `kubectl get nodes` succeeds.

---

## 8. Install a Pod Network Add-on (Cilium)
Cilium is a modern, high-performance, and secure networking solution for Kubernetes, suitable for bare-metal and cloud environments.

Install Cilium:
```bash
kubectl create -f https://raw.githubusercontent.com/cilium/cilium/v1.17.0/install/kubernetes/quick-install.yaml
```
- Wait until all Cilium pods are running:
```bash
kubectl -n kube-system get pods -l k8s-app=cilium
```

---

## Notes
- Repeat steps 1–5 on all worker nodes.
- To join worker nodes, use the `kubeadm join ...` command output by `kubeadm init`.

---

**Your Kubernetes cluster is now ready!**