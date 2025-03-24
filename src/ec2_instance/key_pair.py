from aws_cdk import aws_ec2 as ec2, RemovalPolicy

def create_key_pair(scope, vars):
    if vars.key_pair_name:
        key = ec2.KeyPair.from_key_pair_name(
            scope, vars.key_pair_name,
            key_pair_name=vars.key_pair_name
        )
    else:
        key = ec2.KeyPair(
            scope, vars.common_prefix + "-master-keypair-" + vars.environment,
            description="K3s key pair",
            removal_policy=RemovalPolicy.DESTROY
        )
    return key