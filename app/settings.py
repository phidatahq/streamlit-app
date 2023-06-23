from pydantic import BaseSettings


class AppSettings(BaseSettings):
    """App settings that can be derived from environment variables.

    Reference: https://pydantic-docs.helpmanual.io/usage/settings/
    """

    # Port to run the streamlit app
    port: int = 9095
    # If false, will attempt to open a browser window on start.
    headless: bool = True
    gather_usage_stats: bool = False
    # Max size, in megabytes, for files uploaded with the file_uploader.
    max_upload_size: int = 256


# Create AppSettings object
app_settings = AppSettings()
