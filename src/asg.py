# /usr/bin/python3

from constructs import Construct
from aws_cdk import (
    Stack,
    aws_autoscaling as autoscaling,
    aws_ec2 as ec2,
    Tags,
    Duration,
    Fn
)
from src.variables import Variables

class AutoScalingGroup(Stack):
    
    def __init__(self, scope: Construct, construct_id: str,vars: Variables, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.vars = vars

        vpc = ec2.Vpc.from_lookup(self, "VPC", is_default=True)
        asg_name = vars.common_prefix + "-asg-" + vars.environment

        launch_template_id = Fn.import_value(vars.common_prefix + "-launch-template-id-" + vars.environment)

        asg = autoscaling.AutoScalingGroup(
            self,asg_name,
            vpc=vpc,
            mixed_instances_policy=autoscaling.MixedInstancesPolicy(
                instances_distribution=autoscaling.InstancesDistribution(
                    on_demand_base_capacity=0,
                    on_demand_percentage_above_base_capacity=20,
                    spot_allocation_strategy=autoscaling.SpotAllocationStrategy.CAPACITY_OPTIMIZED,
                ),
                launch_template=ec2.LaunchTemplate.from_launch_template_attributes(
                    scope=self,
                    id="LaunchTemplate",
                    launch_template_id=launch_template_id,
                ),
                launch_template_overrides=[
                    autoscaling.LaunchTemplateOverrides( # Mix multiple instance types
                        instance_type=ec2.InstanceType.of(ec2.InstanceClass.T2, ec2.InstanceSize.SMALL),
                    ),
                    autoscaling.LaunchTemplateOverrides( # Mix multiple instance types
                        instance_type=ec2.InstanceType.of(ec2.InstanceClass.T2, ec2.InstanceSize.MEDIUM),
                    ),
                    autoscaling.LaunchTemplateOverrides( # Mix multiple instance types
                        instance_type=ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.SMALL),
                    ),
                    autoscaling.LaunchTemplateOverrides( # Mix multiple instance types
                        instance_type=ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.MEDIUM),
                    ),
                    autoscaling.LaunchTemplateOverrides( # Mix multiple instance types
                        instance_type=ec2.InstanceType.of(ec2.InstanceClass.T3A, ec2.InstanceSize.SMALL),
                    ),
                    autoscaling.LaunchTemplateOverrides( # Mix multiple instance types
                        instance_type=ec2.InstanceType.of(ec2.InstanceClass.T3A, ec2.InstanceSize.MEDIUM),
                    ),
                ],
                
            ),
            desired_capacity=1,
            min_capacity=1,
            max_capacity=2,
            health_check=autoscaling.HealthCheck.ec2(
                grace=Duration.seconds(300)
            ),
        )

        Tags.of(asg).add("k3s-instance-type", "k3s-master")

