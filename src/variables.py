import os
import string
import secrets

class Variables:
    def __init__(self):
        self.AWS_REGION = os.getenv("AWS_REGION", "us-west-2")
        self.AWS_ACCOUNT = os.getenv("AWS_ACCOUNT", None)
        self.key_pair_name = os.getenv("AWS_KEY_PAIR_NAME", None)
        self.common_prefix = "k3s"
        self.k3s_version = "v1.31.6+k3s1"
        self.environment = "dev"
        self.k3s_token = self.generate_token()
        self.install_nginx_ingress = True
        self.nginx_ingress_release = "v1.12.0"
        self.expose_kubeapi = True
        self.expose_nodeports = False
    

    def generate_token(self, length: int = 20) -> str:
        alphabet = string.ascii_letters + string.digits  # No special characters
        return ''.join(secrets.choice(alphabet) for _ in range(length))