import os
import string
import secrets

class Variables:
    def __init__(self):
        self.AWS_REGION = os.getenv("AWS_REGION", "us-west-2")
        self.key_pair_name = os.getenv("AWS_KEY_PAIR_NAME", None)
        self.common_prefix = "k3s"
        self.k3s_version = "latest"
        self.environment = "dev"
        self.k3s_subnet = "default_route_table"
        self.k3s_url = "127.0.0.1:6443"
        self.k3s_token = self.generate_token()
        self.install_node_termination_handler = True
        self.node_termination_handler_release = "v1.17.3"
        self.install_nginx_ingress = True,
        self.nginx_ingress_release = "v1.3.1",
        self.install_certmanager = True,
        self.efs_persistent_storage = False,
        self.efs_csi_driver_release = "v1.4.2",
        self.efs_filesystem_id = "",
        self.certmanager_release = "v1.9.1",
        self.certmanager_email_address = "",
        self.expose_kubeapi = False,
        self.k3s_tls_san_public = "",
    

    def generate_token(self, length: int = 20) -> str:
        alphabet = string.ascii_letters + string.digits  # No special characters
        return ''.join(secrets.choice(alphabet) for _ in range(length))