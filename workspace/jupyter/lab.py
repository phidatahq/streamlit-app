from os import getenv

from phidata.app.jupyter import Jupyter
from phidata.docker.resource.image import DockerImage

from workspace.settings import ws_settings

#
# -*- Jupyter Docker resources
#

# -*- Jupyter image
jupyter_image = DockerImage(
    name=f"{ws_settings.image_repo}/{ws_settings.ws_name}-jupyter",
    tag=ws_settings.dev_env,
    enabled=(ws_settings.build_images and ws_settings.dev_jupyter_enabled),
    path=str(ws_settings.ws_root),
    dockerfile="workspace/jupyter/jupyter.Dockerfile",
    pull=ws_settings.force_pull_images,
    push_image=ws_settings.push_images,
    skip_docker_cache=ws_settings.skip_image_cache,
)

# -*- Jupyter running on port 8888
dev_jupyter = Jupyter(
    name=f"{ws_settings.ws_name}-jupyter",
    enabled=ws_settings.dev_jupyter_enabled,
    image=jupyter_image,
    mount_workspace=True,
    # Get the OpenAI API key from the environment if available
    env={"OPENAI_API_KEY": getenv("OPENAI_API_KEY", None)},
    use_cache=ws_settings.use_cache,
    # Read secrets from secrets/dev_jupyter_secrets.yml
    secrets_file=ws_settings.ws_root.joinpath(
        "workspace/secrets/dev_jupyter_secrets.yml"
    ),
)
