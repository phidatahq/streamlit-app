from typing import List, Optional

from pydantic import BaseSettings, validator


class ApiSettings(BaseSettings):
    """Api settings that can be derived from environment variables.

    Reference: https://pydantic-docs.helpmanual.io/usage/settings/
    """

    # Api title and version
    title: str = "Api"
    version: str = "1.0"

    # Api runtime_env derived from the `runtime_env` environment variable.
    # Valid values include "dev", "stg", "prd"
    runtime_env: str = "dev"

    # Set to False to disable docs server at /docs and /redoc
    docs_enabled: bool = True

    # Host and port to run the api server on.
    host: str = "0.0.0.0"
    port: int = 9090

    # Cors origin list to allow requests from.
    # This list is set using the set_cors_origin_list validator
    # which uses the runtime_env variable to set the
    # default cors origin list.
    cors_origin_list: Optional[List[str]] = None

    @validator("runtime_env")
    def validate_runtime_env(cls, runtime_env):
        """Validate runtime_env"""

        valid_runtime_envs = ["dev", "stg", "prd"]
        if runtime_env not in valid_runtime_envs:
            raise ValueError(f"Invalid runtime_env: {runtime_env}")

        return runtime_env

    @validator("cors_origin_list", always=True)
    def set_cors_origin_list(cls, cors_origin_list, values):
        valid_cors = cors_origin_list or []

        runtime_env = values.get("runtime_env")
        if runtime_env == "dev":
            # 9095 is the default port for streamlit
            # 3000 is the default port for create-react-app
            valid_cors.extend(["http://localhost:9095", "http://localhost:3000"])

        return valid_cors


# Create ApiSettings object
api_settings = ApiSettings()
