from os import getenv

from phidata.app.fastapi import FastApiServer
from phidata.app.streamlit import StreamlitApp
from phidata.aws.config import AwsConfig
from phidata.aws.resource.group import (
    AwsResourceGroup,
    EcsCluster,
    S3Bucket,
    SecretsManager,
    SecurityGroup,
    InboundRule,
)
from phidata.docker.config import DockerConfig, DockerImage
from phidata.resource.reference import AwsReference

from workspace.settings import ws_settings

#
# -*- Resources for the Production Environment
#
# Skip resource deletion when running `phi ws down`
skip_delete: bool = False
# Save resource outputs to workspace/outputs
save_output: bool = True
# Create load balancer for the application
create_load_balancer: bool = True

# -*- Production Image
prd_image = DockerImage(
    name=f"{ws_settings.image_repo}/{ws_settings.ws_name}",
    tag=ws_settings.prd_env,
    enabled=ws_settings.build_images,
    path=str(ws_settings.ws_root),
    platform="linux/amd64",
    pull=ws_settings.force_pull_images,
    push_image=ws_settings.push_images,
    skip_docker_cache=ws_settings.skip_image_cache,
)

# -*- S3 bucket for production data
prd_data_s3_bucket = S3Bucket(
    name=f"{ws_settings.prd_key}-data",
    enabled=False,
    acl="private",
    skip_delete=skip_delete,
    save_output=save_output,
)

# -*- Secrets for production application
prd_app_secret = SecretsManager(
    name=f"{ws_settings.prd_key}-app-secret",
    # Create secret from workspace/secrets/prd_app_secrets.yml
    secret_files=[
        ws_settings.ws_root.joinpath("workspace/secrets/prd_app_secrets.yml")
    ],
    skip_delete=skip_delete,
    save_output=save_output,
)

# -*- Security Group for the load balancer
prd_lb_sg = SecurityGroup(
    name=f"{ws_settings.prd_key}-lb-security-group",
    enabled=create_load_balancer,
    description="Security group for the load balancer",
    inbound_rules=[
        InboundRule(
            description="Allow HTTP traffic from the internet",
            port=80,
            cidr_ip="0.0.0.0/0",
        ),
        InboundRule(
            description="Allow HTTPS traffic from the internet",
            port=443,
            cidr_ip="0.0.0.0/0",
        ),
    ],
    skip_delete=skip_delete,
    save_output=save_output,
)
# -*- Security Group for the application
prd_app_sg = SecurityGroup(
    name=f"{ws_settings.prd_key}-app-security-group",
    enabled=ws_settings.prd_api_enabled or ws_settings.prd_app_enabled,
    description="Security group for the production application",
    inbound_rules=[
        InboundRule(
            description="Allow traffic from LB to the FastAPI server",
            port=9090,
            source_security_group_id=AwsReference(prd_lb_sg.get_security_group_id),
        ),
        InboundRule(
            description="Allow traffic from LB to the Streamlit app",
            port=9095,
            source_security_group_id=AwsReference(prd_lb_sg.get_security_group_id),
        ),
    ],
    depends_on=[prd_lb_sg],
    skip_delete=skip_delete,
    save_output=save_output,
)

# -*- ECS cluster
launch_type = "FARGATE"
prd_ecs_cluster = EcsCluster(
    name=f"{ws_settings.prd_key}-cluster",
    ecs_cluster_name=ws_settings.prd_key,
    capacity_providers=[launch_type],
    skip_delete=skip_delete,
    save_output=save_output,
)

# -*- StreamlitApp running on ECS
prd_streamlit = StreamlitApp(
    name=f"{ws_settings.prd_key}-app",
    enabled=ws_settings.prd_app_enabled,
    image=prd_image,
    command=["app", "start", "Home"],
    ecs_task_cpu="2048",
    ecs_task_memory="4096",
    ecs_cluster=prd_ecs_cluster,
    ecs_service_count=1,
    aws_subnets=ws_settings.subnet_ids,
    aws_secrets=[prd_app_secret],
    aws_security_groups=[prd_app_sg],
    load_balancer_security_groups=[prd_lb_sg],
    create_load_balancer=create_load_balancer,
    # Get the OpenAI API key from the local environment
    env={"OPENAI_API_KEY": getenv("OPENAI_API_KEY", None)},
    use_cache=ws_settings.use_cache,
    skip_delete=skip_delete,
    save_output=save_output,
    # Do not wait for the service to stabilize
    wait_for_creation=False,
    # Do not wait for the service to be deleted
    wait_for_deletion=False,
    # Uncomment to read secrets from secrets/prd_app_secrets.yml
    # secrets_file=ws_settings.ws_root.joinpath("workspace/secrets/prd_app_secrets.yml"),
)

# -*- FastApiServer running on ECS
prd_fastapi = FastApiServer(
    name=f"{ws_settings.prd_key}-api",
    enabled=ws_settings.prd_api_enabled,
    image=prd_image,
    command=["api", "start"],
    ecs_task_cpu="2048",
    ecs_task_memory="4096",
    ecs_cluster=prd_ecs_cluster,
    ecs_service_count=1,
    aws_subnets=ws_settings.subnet_ids,
    aws_secrets=[prd_app_secret],
    aws_security_groups=[prd_app_sg],
    load_balancer_security_groups=[prd_lb_sg],
    create_load_balancer=create_load_balancer,
    health_check_path="/v1/ping",
    # Get the OpenAI API key from the local environment
    env={"OPENAI_API_KEY": getenv("OPENAI_API_KEY", None)},
    use_cache=ws_settings.use_cache,
    skip_delete=skip_delete,
    save_output=save_output,
    # Do not wait for the service to stabilize
    wait_for_creation=False,
    # Uncomment to read secrets from secrets/prd_app_secrets.yml
    # secrets_file=ws_settings.ws_root.joinpath("workspace/secrets/prd_app_secrets.yml"),
)

# -*- DockerConfig defining the prd resources
prd_docker_config = DockerConfig(
    env=ws_settings.prd_env,
    network=ws_settings.ws_name,
    images=[prd_image],
)

# -*- AwsConfig defining the prd resources
prd_aws_config = AwsConfig(
    env=ws_settings.prd_env,
    apps=[prd_streamlit, prd_fastapi],
    resources=AwsResourceGroup(
        secrets=[prd_app_secret],
        security_groups=[prd_lb_sg, prd_app_sg],
        s3_buckets=[prd_data_s3_bucket],
    ),
)
