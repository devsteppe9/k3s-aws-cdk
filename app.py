#!/usr/bin/env python3

import aws_cdk as cdk

from src.ec2_instance.k3s_instance import K3sInstance
from src.variables import Variables
from dotenv import load_dotenv

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

app.synth()
