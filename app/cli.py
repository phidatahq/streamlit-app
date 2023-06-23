"""The `app` cli
Usage:
    $ app --help
"""
import typer


cli = typer.Typer(
    help="Run App commands",
    no_args_is_help=True,
    invoke_without_command=True,
    # https://typer.tiangolo.com/tutorial/exceptions/#disable-local-variables-for-security
    pretty_exceptions_show_locals=False,
)


@cli.command(short_help="Start App Server")
def start(
    name: str = typer.Argument("Home", help="App Name", show_default=True),
):
    """
    \b
    Start App server.

    \b
    Examples:
    * `app start`         -> Start app/Home.py
    * `app start base`    -> Start app/base.py
    """
    import sys
    import streamlit.web.cli as stcli

    from pathlib import Path
    from app.settings import app_settings
    from utils.log import logger

    app_dir = Path(__file__).parent.resolve()
    app_file = app_dir.joinpath(f"{name}.py")
    if not app_file.exists() and not app_file.is_file():
        raise Exception(f"Invalid file {app_file}")

    logger.info(f"Starting App: {app_file}")
    sys.argv = [
        "streamlit",
        "run",
        str(app_file),
        "--server.port",
        str(app_settings.port),
        "--server.headless",
        str(app_settings.headless),
        "--browser.gatherUsageStats",
        str(app_settings.gather_usage_stats),
        "--server.maxUploadSize",
        str(app_settings.max_upload_size),
    ]
    sys.exit(stcli.main())


@cli.command(short_help="Print Settings")
def settings():
    """
    \b
    Print App settings.

    \b
    Examples:
    * `app settings`    -> Print App settings
    """
    from app.settings import app_settings
    from utils.log import logger

    logger.info("App Settings:")
    logger.info(app_settings.json(indent=2))
