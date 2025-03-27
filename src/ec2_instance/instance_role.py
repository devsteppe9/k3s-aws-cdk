from aws_cdk import aws_iam as iam

def create_instance_role(scope, vars):
    ec2_instance_role = iam.Role(
        scope, vars.common_prefix + "-master-role-" + vars.environment,
        assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
        managed_policies=[
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEC2ReadOnlyAccess"),
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore"),
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEC2ContainerRegistryPullOnly"),
        ]
    )

    ec2_instance_profile = iam.InstanceProfile(
        scope, vars.common_prefix + "-master-profile-" + vars.environment,
        role=ec2_instance_role
    )

    return ec2_instance_profile