#!/usr/bin/env python3

from aws_cdk import aws_ec2 as ec2

def create_security_group(scope, vpc, vars):
    sg = ec2.SecurityGroup(
        scope, vars.common_prefix + "-master-sg-" + vars.environment,
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

    sg.add_ingress_rule(
        peer=ec2.Peer.any_ipv4(),
        connection=ec2.Port.tcp(443),
        description="Allow https access from the world"
    )

    if vars.expose_nodeports:
        sg.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp_range(30000, 32767),
        )

    if vars.expose_kubeapi:
        sg.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(6443),
            description="Allow kubernetes API access from the world. This is not recommended for production."
        )

    return sg