import os
from constructs import Construct
from aws_cdk import (
    CfnCreationPolicy,
    CfnResourceSignal,
    Duration,
    Stack,
    aws_iam as iam,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_ec2 as ec2,
    aws_sns_subscriptions as subs,
    CfnOutput,
    RemovalPolicy,
    Tags,
)
from jinja2 import Environment, PackageLoader, select_autoescape
from src.variables import Variables


class K3sStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vars: Variables, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.vars = vars

        # APPLY COMMON TAGS TO ALL RESOURCES
        Tags.of(scope).add("environment", vars.environment)
        Tags.of(scope).add("provisioner", "cdk")
        Tags.of(scope).add("cdk_module", "https://github.com/devsteppe9/k3s-aws-cdk")
        Tags.of(scope).add("k3s_cluster_name", vars.common_prefix)
        Tags.of(scope).add("application", "k3s")

        # find default VPC
        vpc = ec2.Vpc.from_lookup(self, "VPC", is_default=True)

        # create security group
        sg = ec2.SecurityGroup(
            self, vars.common_prefix + "-master-sg-" + vars.environment,
            vpc=vpc,
            allow_all_outbound=True,
        )

        sg.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(22),
            description="Allow ssh access from the world"
        )

        sg.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(80),
            description="Allow http access from the world"
        )

        if vars.key_pair_name:
            key = ec2.KeyPair.from_key_pair_name(
                self, vars.key_pair_name,
                key_pair_name=vars.key_pair_name
            )
        else:
            key = ec2.KeyPair(
                self, vars.common_prefix + "-master-keypair-" + vars.environment,
                description="K3s key pair",
                removal_policy=RemovalPolicy.DESTROY
            )
        
        instance_name = vars.common_prefix + "-master-instance-" + vars.environment
        user_data = ec2.UserData.for_linux()
        user_data.add_commands(
            self.get_rendered_script(),
            "/opt/aws/bin/cfn-signal --success=true --stack " + self.stack_name + " --resource " + instance_name + " --region " + self.region
        )


        ec2_instance_role = iam.Role(
            self, vars.common_prefix + "-master-role-" + vars.environment,
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEC2ReadOnlyAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore")
            ]
        )

        ec2_instance_profile = iam.InstanceProfile(
            self, vars.common_prefix + "-master-profile-" + vars.environment,
            role=ec2_instance_role
        )

        # create instance
        instance = ec2.Instance(
            self, instance_name,
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.T2, ec2.InstanceSize.MICRO),
            machine_image=ec2.MachineImage.latest_amazon_linux2023(),
            vpc=vpc,
            security_group=sg,
            key_pair=key,
            associate_public_ip_address=True,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            instance_profile=ec2_instance_profile,
            user_data=user_data,
            require_imdsv2=True,
        )

        Tags.of(instance).add("k3s-instance-type", "k3s-master")

        CfnOutput(
            self, vars.common_prefix + "-master-public-ip-" + vars.environment,
            value=instance.instance_public_ip,
            description="Public IP address of the instance"
        )

        # output instance ID
        CfnOutput(
            self, "SrcInstanceId",
            value=instance.instance_id,
            description="Instance ID"
        )
    
    def get_rendered_script(self) -> str:
        jinja_env = Environment(
            loader=PackageLoader('k3s_cluster', 'bash_scripts'),
            autoescape=select_autoescape("sh"),
            variable_start_string='{{',
            variable_end_string='}}'
        )
        
        variables = {
            "k3s_version": self.vars.k3s_version,
            "k3s_token": self.vars.k3s_token,
            "k3s_subnet": self.vars.k3s_subnet,
            "is_k3s_server": True,
            "install_node_termination_handler": self.vars.install_node_termination_handler,
            "node_termination_handler_release": self.vars.node_termination_handler_release,
            "install_nginx_ingress": self.vars.install_nginx_ingress,
            "nginx_ingress_release": self.vars.nginx_ingress_release,
            "install_certmanager": self.vars.install_certmanager,
            "efs_persistent_storage": self.vars.efs_persistent_storage,
            "efs_csi_driver_release": self.vars.efs_csi_driver_release,
            "efs_filesystem_id": self.vars.efs_persistent_storage,
            "certmanager_release": self.vars.certmanager_release,
            "certmanager_email_address": self.vars.certmanager_email_address,
            "expose_kubeapi": self.vars.expose_kubeapi,
            "k3s_tls_san_public": self.vars.k3s_tls_san_public,
            "k3s_url": self.vars.k3s_url,
            "k3s_tls_san": self.vars.k3s_url,
            "kubeconfig_secret_name": "" #TODO: add this
        }

        # FIXME: bash file is not formatted correctly to render with jinja
        self.master_install_template = jinja_env.get_template('k3s-master-install.sh')
        scripts = self.master_install_template.render(variables)

        # self.master_install_template = jinja_env.get_template('demo_setup.sh')
        # scripts = self.master_install_template.render({'contents_for_web': 'Hello, World from Jinja!'})

        # print(scripts)
        return scripts
