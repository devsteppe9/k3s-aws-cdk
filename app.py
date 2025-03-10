#!/usr/bin/env python3

import os
import aws_cdk as cdk

from src.k3s_stack import K3sStack
from src.variables import Variables
from dotenv import load_dotenv
load_dotenv(dotenv_path=".env")



app = cdk.App()
aws_account = os.getenv("AWS_ACCOUNT")
aws_region = os.getenv("AWS_REGION")
env = cdk.Environment(account=aws_account, region=aws_region)
K3sStack(app, "K3sStack", env=env, vars=Variables())

app.synth()
