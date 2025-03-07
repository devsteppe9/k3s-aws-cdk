import os
from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_ec2 as ec2,
    aws_sns_subscriptions as subs,
    CfnOutput,
    CfnTag,
    RemovalPolicy
)
from jinja2 import Environment, PackageLoader, select_autoescape


class K3sStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # find default VPC
        vpc = ec2.Vpc.from_lookup(self, "VPC", is_default=True)

        # create security group
        sg = ec2.SecurityGroup(
            self, "SrcSecurityGroup",
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

        check_existing_key = os.getenv("AWS_KEY_PAIR_NAME")
        if check_existing_key:
            key = ec2.KeyPair.from_key_pair_name(
                self, check_existing_key,
                key_pair_name=check_existing_key
            )
        else:
            key = ec2.KeyPair(
                self, "K3sKeyPair",
                key_name="k3skeypair",
                description="K3s key pair",
                removal_policy=RemovalPolicy.DESTROY
            )
        
        # install apache httpd and serve a custom index.html
        user_data = ec2.UserData.for_linux()
        # user_data.add_execute_file_command(file_path="./setup.sh")
        user_data.add_commands(self.get_rendered_script())

        # create instance
        instance = ec2.Instance(
            self, "SrcInstance",
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.T2, ec2.InstanceSize.MICRO),
            machine_image=ec2.MachineImage.latest_amazon_linux2023(),
            vpc=vpc,
            security_group=sg,
            key_pair=key,
            associate_public_ip_address=True,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            user_data=user_data
        )

        CfnOutput(
            self, "SrcInstancePublicIp",
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
            "k3s_version": "latest",
            "k3s_token": "random_token"
        }

        # FIXME: bash file is not formatted correctly to render with jinja
        # self.master_install_template = jinja_env.get_template('k3s-master-install.sh')
        # scripts = self.master_install_template.render(variables)

        self.master_install_template = jinja_env.get_template('demo_setup.sh')
        scripts = self.master_install_template.render({'contents_for_web': 'Hello, World from Jinja!'})

        # print(scripts)
        return scripts
