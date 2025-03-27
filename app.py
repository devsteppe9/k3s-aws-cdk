#!/usr/bin/env python3

import aws_cdk as cdk

from src.ec2_instance.k3s_instance import K3sInstance
from src.launch_template import LaunchTemplate
from src.variables import Variables
from dotenv import load_dotenv
from aws_cdk import Tags

app = cdk.App()
load_dotenv(dotenv_path="config/.env")
vars = Variables()

K3sInstance(
    app,
    vars.common_prefix + "-master-instance-" + vars.environment,
    env=cdk.Environment(
        account=vars.AWS_ACCOUNT,
        region=vars.AWS_REGION
    ), 
    vars=vars
)

LaunchTemplate(
    app,
    vars.common_prefix + "-launch-template-" + vars.environment,
    env=cdk.Environment(
        account=vars.AWS_ACCOUNT,
        region=vars.AWS_REGION
    ),
    vars=vars
)

# APPLY COMMON TAGS TO ALL RESOURCES
Tags.of(app).add("environment", "dev")
Tags.of(app).add("provisioner", "cdk")
Tags.of(app).add("cdk_module", "")
Tags.of(app).add("k3s_cluster_name", "k3s-cluster") 
Tags.of(app).add("application", "k3s")

app.synth()
