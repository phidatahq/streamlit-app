from pathlib import Path

from phidata.workspace.settings import WorkspaceSettings

#
# -*- Define workspace settings using the WorkspaceSettings class
#
ws_settings = WorkspaceSettings(
    # Workspace name: used for naming cloud resources
    ws_name="llm",
    # Path to the workspace root
    ws_root=Path(__file__).parent.parent.resolve(),
    # -*- Dev settings
    dev_env="dev",
    # -*- Dev Apps
    dev_app_enabled=True,
    dev_api_enabled=True,
    dev_jupyter_enabled=True,
    # -*- Production settings
    prd_env="prd",
    # -*- Production Apps
    prd_app_enabled=True,
    prd_api_enabled=True,
    # -*- AWS settings
    # Region for AWS resources
    aws_region="us-east-2",
    # Availability Zones for AWS resources
    aws_az1="us-east-2a",
    aws_az2="us-east-2b",
    # Subnet IDs in the aws_region
    # subnet_ids=["subnet-xyz", "subnet-xyz"],
    # -*- Image Settings
    # Repository for images
    # image_repo="[ACCOUNT_ID].dkr.ecr.us-east-2.amazonaws.com",
    # Build images locally
    # build_images=True,
    # Push images after building
    # push_images=True,
)
