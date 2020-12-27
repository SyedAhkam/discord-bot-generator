from . import generator
from .__version__ import __version__
from .config import (
    GITHUB_REPO_URL,
    SUCCESS_COLOR,
    PROMPT_COLOR,
    ERROR_COLOR,
    ROCKET_EMOJI,
    SPARKLES_EMOJI,
    DISAPPOINTING_EMOJI,
)

import os
import click

CWD = os.getcwd()
CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=__version__)
def cli():
    """Fastest and easiest way to create a new discord bot project ✨🚀"""
    pass


@cli.command()
@click.pass_context
@click.option(
    "-n",
    "--name",
    prompt=click.style("? Project Name", fg=PROMPT_COLOR),
    type=click.STRING,
    help="The project name",
)
@click.option(
    "-d",
    "--dest",
    prompt=click.style("? Project Location", fg=PROMPT_COLOR),
    default=CWD,
    type=click.Path(exists=True),
    help="The destination folder path",
)
@click.option(
    "-t", "--template", default="default", help="The template to use", type=click.STRING
)
@click.option(
    "-bp", "--botprefix", default="+", help="The default bot prefix", type=click.STRING
)
@click.option(
    "-ng", "--nogit", is_flag=True, help="If passed, git won't be initialized"
)
@click.option(
    "-nc", "--nocommit", is_flag=True, help="If passed, no initial commit would be done"
)
@click.option("-np", "--nopipenv", is_flag=True, help="If passed, pipenv won't be used")
def new(
    ctx: click.Context,
    name: str,
    dest: str,
    template: str,
    botprefix: str,
    nogit: bool,
    nocommit: bool,
    nopipenv: bool,
):
    """Creates a new project"""
    dest_folder_name = os.path.basename(dest)

    click.echo()
    click.secho(
        f"{ROCKET_EMOJI} Generating a discord.py project in {dest_folder_name}",
        fg=SUCCESS_COLOR,
        nl=True,
    )
    click.echo()

    if name in os.listdir(dest):
        click.secho(
            f"{DISAPPOINTING_EMOJI} Project name already exists!", fg=ERROR_COLOR
        )
        ctx.abort()

    generator.generate(
        template,
        dest,
        name,
        botprefix,
        False if nogit else True,
        False if nocommit else True,
        False if nopipenv else True,
    )

    success_message = (
        f"-  $ cd {name}\n-  $ {'python bot.py' if nopipenv else 'pipenv run start'}"
    )

    click.secho(f"{SPARKLES_EMOJI} Done!", fg=SUCCESS_COLOR)
    click.secho(success_message, fg=PROMPT_COLOR)


@cli.command()
@click.option("--nobrowser", is_flag=True)
def github(nobrowser: bool):
    """Links to the github project"""
    if nobrowser:
        click.secho(f"{SPARKLES_EMOJI} {GITHUB_REPO_URL}", fg=SUCCESS_COLOR)
    else:
        click.launch(GITHUB_REPO_URL)


if __name__ == "__main__":
    cli()
