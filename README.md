# k3s-aws-cdk
This is a CDK project to deploy a k3s cluster on AWS. After running the CDK stack, you will have a k3s cluster running on an EC2 instance in AWS. The k3s cluster will be deployed using the user data script in the `src/user_data.sh` file. The user data script will install k3s on the EC2 instance and configure it as a server node.

## What is k3s?
k3s is a lightweight Kubernetes distribution that is easy to install and run. It is designed for edge computing, IoT, and CI/CD pipelines. For more information, visit the [k3s website](https://docs.k3s.io/).

## Prerequisites

- Python 3.8+
- Pip 24.0+
- AWS CLI (Installation guide [here](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html))
- AWS CDK Toolkit (Instalwith your AWS account credentials. You can do this by running `aws configure` and entering your AWS Access Key ID, AWS Secret Access Key, default region name, and default output format.

## Confugure AWS CLI
Before you can deploy the CDK stack, you need to configure the AWS CLI with your AWS account credentials. You can do this by running `aws configure` and entering your AWS Access Key ID, AWS Secret Access Key, default region name, and default output format.
```bash
aws configure
```

## Installation

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

## Usage

At this point, you can now synthesize the CloudFormation template for this code.

```bash
cdk synth
```

If the CloudFormation template looks good, you can now deploy the stack.

```bash
cdk deploy
```

Before deploying the stack, you can also run a diff to see the changes that will be made to your AWS account.
```bash
cdk diff
```

## Expected Output

After deploying the stack, you will have a k3s cluster running on an EC2 instance in AWS. The expected output includes:

- A security group allowing SSH, HTTP, HTTPS, and Kubernetes API access.
- An IAM role with policies for EC2 read-only access, SSM managed instance core, and ECR pull-only access.
- An EC2 instance running the k3s cluster with the specified user data script.
- Public IP address and instance ID of the deployed EC2 instance.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Enjoy!