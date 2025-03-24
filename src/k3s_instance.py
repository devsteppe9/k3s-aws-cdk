from constructs import Construct
from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    CfnOutput,
    Tags,
)
from src.variables import Variables
from src.security_groups import create_security_group
from src.key_pair import create_key_pair
from src.instance_role import create_instance_role
from src.user_data import create_user_data

class K3sInstance(Stack):

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

        sg = create_security_group(self, vpc, vars)

        key = create_key_pair(self, vars)
        
        instance_name = vars.common_prefix + "-master-instance-" + vars.environment

        user_data = create_user_data(self, vars, instance_name)

        ec2_instance_profile = create_instance_role(self, vars)

        # create instance
        instance = ec2.Instance(
            self, instance_name,
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.T2, ec2.InstanceSize.SMALL),
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

        CfnOutput(
            self, "SrcInstanceId",
            value=instance.instance_id,
            description="Instance ID"
        )
