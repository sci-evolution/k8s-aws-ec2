#!/bin/bash
# control-plane-node-ec2-userdata.sh
# Kubernetes Control Plane Node Setup for AWS EC2 (User Data version)
# This script is intended to be pasted into the EC2 User Data field.
# It will run as root on first boot.

set -e

# Log output for debugging
exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1

# Wait for cloud-init to finish (ensures networking and hostname are set)
cloud-init status --wait || true

# 1. Set up UFW firewall
ufw default deny incoming
ufw default allow outgoing
ufw default deny routed
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
ufw --force enable

# 2. Disable swap (required by Kubernetes)
swapoff -a
sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab

# 3. Enable required kernel modules
cat <<EOF | tee /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF
modprobe overlay
modprobe br_netfilter

# 4. Set kernel parameters for Kubernetes networking
cat <<EOF | tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables  = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward                 = 1
EOF
sysctl --system

# 5. Install containerd (container runtime)
apt-get update && apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
apt-get update && apt-get install -y containerd.io
mkdir -p /etc/containerd
containerd config default | tee /etc/containerd/config.toml
sed -i 's/SystemdCgroup = false/SystemdCgroup = true/g' /etc/containerd/config.toml
systemctl restart containerd

# 6. Install Kubernetes components
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.32/deb/Release.key | gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.32/deb/ /' | tee /etc/apt/sources.list.d/kubernetes.list
apt-get update
apt-get install -y kubelet kubeadm kubectl
apt-mark hold kubelet kubeadm kubectl
systemctl enable --now kubelet

# 7. Initialize the Kubernetes control plane
kubeadm init \
  --apiserver-advertise-address=<CONTROL_PLANE_PRIVATE_IP> \
  --control-plane-endpoint=<NLB_DNS_NAME>:6443 \
  --pod-network-cidr=192.168.0.0/16 \
  --kubernetes-version=v1.32 \
  --upload-certs \
  --skip-phases=addon/kube-proxy # This is important for Cilium's kube-proxy replacement

# 8. Set up kubectl for the default user (ubuntu)
export HOME_DIR="/home/ubuntu"
mkdir -p $HOME_DIR/.kube
cp -i /etc/kubernetes/admin.conf $HOME_DIR/.kube/config
chown ubuntu:ubuntu $HOME_DIR/.kube/config

# 9. Install Cilium (network add-on)
# Install Cilium CLI
CILIUM_CLI_VERSION=$(curl -s https://raw.githubusercontent.com/cilium/cilium-cli/main/stable.txt)
CLI_ARCH=amd64
curl -L --fail --remote-name-all https://github.com/cilium/cilium-cli/releases/download/${CILIUM_CLI_VERSION}/cilium-linux-${CLI_ARCH}.tar.gz{,.sha256sum}
sha256sum --check cilium-linux-${CLI_ARCH}.tar.gz.sha256sum
sudo tar xzvfC cilium-linux-${CLI_ARCH}.tar.gz /usr/local/bin
rm cilium-linux-${CLI_ARCH}.tar.gz{,.sha256sum}

# Install Cilium CNI
cilium install \
  --version ${CILIUM_CLI_VERSION} \
  --kube-proxy-replacement=strict \
  --cluster-pool-ipv4-cidr=192.168.0.0/16 \
  --enable-endpoint-health-checking=true \
  --enable-hubble=true \
  --hubble-relay=true \
  --hubble-ui=true \
  --azure=false \
  --eni=false

# 10. Print join command for worker nodes
echo "Run the kubeadm join command below on each worker node:"
kubeadm token create --print-join-command

# End of script
