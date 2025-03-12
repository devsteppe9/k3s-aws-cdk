#!/bin/bash
# ATTENTION: This script does not work as a standalone script. It must be rendered with the Jinja2 template engine.

check_os() {
  name=$(cat /etc/os-release | grep ^NAME= | sed 's/"//g')
  clean_name=${name#*=}

  version=$(cat /etc/os-release | grep ^VERSION_ID= | sed 's/"//g')
  clean_version=${version#*=}
  major=${clean_version%.*}
  minor=${clean_version#*.}

  if [[ "$clean_name" == "Ubuntu" ]]; then
    operating_system="ubuntu"
  elif [[ "$clean_name" == "Amazon Linux" ]]; then
    operating_system="amazonlinux"
  else
    operating_system="undef"
  fi

  echo "K3S install process running on: "
  echo "OS: $operating_system"
  echo "OS Major Release: $major"
  echo "OS Minor Release: $minor"
}

check_os
AWS_IMDS_TOKEN=$(curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")
echo "HERE IS THE TOKEN: "
echo $AWS_IMDS_TOKEN

if [[ "$operating_system" == "ubuntu" ]]; then
  apt-get update
  apt-get install -y software-properties-common unzip git nfs-common jq
  DEBIAN_FRONTEND=noninteractive apt-get upgrade -y
  curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
  unzip awscliv2.zip
  sudo ./aws/install
  rm -rf aws awscliv2.zip
fi

if [[ "$operating_system" == "amazonlinux" ]]; then
  yum install -y --skip-broken unzip curl jq git
fi

k3s_install_params=()

{% if install_nginx_ingress %}
k3s_install_params+=("--disable traefik")
{% endif %}

{% if expose_kubeapi %}
k3s_install_params+=("--tls-san {{ k3s_tls_san_public }}")
{% endif %}

INSTALL_PARAMS="${k3s_install_params[*]}"
echo "INSTALL_PARAMS: $INSTALL_PARAMS"

{% if k3s_version == "latest" %}
K3S_VERSION=$(curl --silent https://api.github.com/repos/k3s-io/k3s/releases/latest | jq -r '.name')
{% else %}
K3S_VERSION="{{ k3s_version }}"
{% endif %}

until (curl -sfL https://get.k3s.io | INSTALL_K3S_VERSION=$K3S_VERSION K3S_TOKEN={{ k3s_token }} sh -s - --cluster-init $INSTALL_PARAMS); do
  echo 'k3s did not install correctly'
  exit 1
  sleep 2
done

until kubectl get pods -A | grep 'Running'; do
  echo 'Waiting for k3s startup'
  sleep 5
done

{% if install_node_termination_handler %}
#Install node termination handler
echo 'Install node termination handler'
kubectl apply -f https://github.com/aws/aws-node-termination-handler/releases/download/{{ node_termination_handler_release }}/all-resources.yaml
{% endif %}

{% if install_nginx_ingress %}
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-{{ nginx_ingress_release }}/deploy/static/provider/cloud/deploy.yaml
{% endif %}

# Install kubectl alias
echo 'alias k=kubectl' >>~/.bashrc
source ~/.bashrc

# Create demo nginx deployment
until kubectl get pods --namespace=ingress-nginx | grep 'Running'; do
  echo 'Waiting for nginx ingress controller to start'
  sleep 5
done

kubectl create deployment demo --image=httpd --port=80
kubectl expose deployment demo
sleep 5
kubectl create ingress demo-localhost --class=nginx --rule="/*=demo:80"
