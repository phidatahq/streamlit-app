"""The `api` cli
Usage:
    $ api --help
"""

import typer


cli = typer.Typer(
    help="Run Api commands",
    no_args_is_help=True,
    invoke_without_command=True,
    # https://typer.tiangolo.com/tutorial/exceptions/#disable-local-variables-for-security
    pretty_exceptions_show_locals=False,
)


@cli.command(short_help="Start Api Server")
def start(
    reload: bool = typer.Option(
        False, "--reload", "-r", help="Reload", show_default=True
    ),
):
    """
    \b
    Start Api server.

    \b
    Examples:
    * `api start`    -> Start App
    * `api start -r` -> Start App with reload
    """
    import uvicorn
    from api.settings import api_settings
    from utils.log import logger

    logger.info("Starting Api")
    uvicorn.run(
        "api.main:app",
        host=api_settings.host,
        port=api_settings.port,
        reload=reload,
    )


@cli.command(short_help="Print Settings")
def settings():
    """
    \b
    Print Api settings.

    \b
    Examples:
    * `api settings`    -> Print Api settings
    """
    from api.settings import api_settings
    from utils.log import logger

    logger.info("Api Settings:")
    logger.info(api_settings.json(indent=2))
