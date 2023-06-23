from os import getenv

from phidata.app.fastapi import FastApiServer
from phidata.app.streamlit import StreamlitApp
from phidata.docker.config import DockerConfig
from phidata.docker.resource.image import DockerImage

from workspace.jupyter.lab import dev_jupyter
from workspace.settings import ws_settings

#
# -*- Resources for the Development Environment
#

# -*- Development Image
dev_image = DockerImage(
    name=f"{ws_settings.image_repo}/{ws_settings.ws_name}",
    tag=ws_settings.dev_env,
    enabled=ws_settings.build_images,
    path=str(ws_settings.ws_root),
    pull=ws_settings.force_pull_images,
    push_image=ws_settings.push_images,
    skip_docker_cache=ws_settings.skip_image_cache,
)

# -*- StreamlitApp running on port 9095
dev_streamlit = StreamlitApp(
    name=f"{ws_settings.dev_key}-app",
    enabled=ws_settings.dev_app_enabled,
    image=dev_image,
    command="app start Home",
    mount_workspace=True,
    # Get the OpenAI API key from the local environment
    env={"OPENAI_API_KEY": getenv("OPENAI_API_KEY", None)},
    use_cache=ws_settings.use_cache,
    # Read secrets from secrets/dev_app_secrets.yml
    secrets_file=ws_settings.ws_root.joinpath("workspace/secrets/dev_app_secrets.yml"),
)

# -*- FastApiServer running on port 9090
dev_fastapi = FastApiServer(
    name=f"{ws_settings.dev_key}-api",
    enabled=ws_settings.dev_api_enabled,
    image=dev_image,
    command="api start -r",
    mount_workspace=True,
    # Get the OpenAI API key from the local environment
    env={"OPENAI_API_KEY": getenv("OPENAI_API_KEY", None)},
    use_cache=ws_settings.use_cache,
    # Read secrets from secrets/dev_app_secrets.yml
    secrets_file=ws_settings.ws_root.joinpath("workspace/secrets/dev_app_secrets.yml"),
)

# -*- DockerConfig defining the dev resources
dev_docker_config = DockerConfig(
    env=ws_settings.dev_env,
    network=ws_settings.ws_name,
    apps=[dev_streamlit, dev_fastapi, dev_jupyter],
)
