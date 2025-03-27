# /usr/bin/python3
# -*- coding: utf-8 -*-

from constructs import Construct
from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    Tags,
    CfnOutput
)
from src.ec2_instance.security_groups import create_security_group
from src.ec2_instance.instance_role import create_instance_role
from src.ec2_instance.key_pair import create_key_pair
from src.variables import Variables
from src.ec2_instance.user_data import create_user_data

class LaunchTemplate(Stack):

    def __init__(self, scope: Construct, construct_id: str,vars: Variables, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # find default VPC
        vpc = ec2.Vpc.from_lookup(self, "VPC", is_default=True)
        sg = create_security_group(self, vpc, vars)
        ec2_instance_profile = create_instance_role(self, vars)
        key = create_key_pair(self, vars)
        user_data = create_user_data(self, vars, '')

        template_name = vars.common_prefix + "-launch-template-" + vars.environment

        launch_template = ec2.LaunchTemplate(self, "LaunchTemplate",
            launch_template_name=template_name,
            machine_image=ec2.MachineImage.latest_amazon_linux2023(),
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.T2, ec2.InstanceSize.SMALL),
            instance_profile=ec2_instance_profile,
            block_devices=[
                ec2.BlockDevice(
                    device_name="/dev/sda1",
                    volume=ec2.BlockDeviceVolume.ebs(
                        volume_size=20,
                        encrypted=True,
                        delete_on_termination=True
                    )
                )
            ],
            key_pair=key,
            associate_public_ip_address=True,
            security_group=sg,
            require_imdsv2=True,
            user_data=user_data
        )

        Tags.of(launch_template).add("k3s-instance-type", "k3s-master")

        CfnOutput(
            self, vars.common_prefix + "-launch-template-id-" + vars.environment,
            value=launch_template.launch_template_id,
            description="Launch Template Id"
        )
