from aws_cdk import aws_ec2 as ec2
from jinja2 import Environment, PackageLoader, select_autoescape

def get_rendered_script(vars) -> str:
    jinja_env = Environment(
        loader=PackageLoader('scripts', '.'),
        autoescape=select_autoescape("sh"),
        variable_start_string='{{',
        variable_end_string='}}'
    )
    
    variables = {
        "k3s_version": vars.k3s_version,
        "k3s_token": vars.k3s_token,
        "is_k3s_server": True,
        "install_nginx_ingress": vars.install_nginx_ingress,
        "nginx_ingress_release": vars.nginx_ingress_release,
        "expose_kubeapi": vars.expose_kubeapi,
    }

    master_install_template = jinja_env.get_template('k3s-master-install.sh')
    scripts = master_install_template.render(variables)

    return scripts

def create_user_data(scope, vars, instance_name):
    user_data = ec2.UserData.for_linux()
    user_data.add_commands(
        get_rendered_script(vars),
        "/opt/aws/bin/cfn-signal --success=true --stack " + scope.stack_name + " --resource " + instance_name + " --region " + scope.region
    )
    return user_data