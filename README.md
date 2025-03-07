# k3s-aws-cdk

This is a CDK project to deploy a k3s cluster on AWS.

## Prerequisites

- Python 3.8+
- Pip 24.0+
- AWS CLI (Installation guide [here](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html))
- AWS CDK Toolkit (Installation guide [here](https://docs.aws.amazon.com/cdk/latest/guide/cli.html))

## Setup

```bash
# Create virtualenv
python -m venv .venv

# Activate virtualenv
source .venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

# Check pip version
pip --version  #My version is 25.0.1
# Check Python version
python --version  #My version is 3.13.1

# Install requirements
pip install -r requirements.txt
```


At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

You can now begin exploring the source code, contained in the hello directory.
There is also a very trivial test included that can be run like this:

```
$ pytest
```

To add additional dependencies, for example other CDK libraries, just add to
your requirements.txt file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
