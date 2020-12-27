from .config import (
    SUCCESS_COLOR,
    ERROR_COLOR,
    CHECKMARK_EMOJI,
    DISAPPOINTING_EMOJI,
    SPARKLES_EMOJI,
)

import os
import shutil
import time
import subprocess
import glob
import click


abs_path_to_templates = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "templates"
)
abs_path_to_snippets = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "snippets"
)


def _copytree(
    src: os.PathLike, dst: os.PathLike, symlinks: bool = False, ignore=None
) -> None:
    """Copies all the files from one directory to another"""
    src_contents = os.listdir(src)
    with click.progressbar(
        src_contents,
        length=len(src_contents),
        label=click.style(f"{CHECKMARK_EMOJI} Copying template", fg="green", bold=True),
        item_show_func=lambda i: i,
        fill_char=click.style("█", fg="cyan"),
        empty_char=" ",
    ) as items:
        for item in items:
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, symlinks, ignore)
            else:
                shutil.copy2(s, d)
            time.sleep(0.2)  # just to show the progress bar :p


def _copy_template_to_dest(
    template_name: str, dest: os.PathLike, project_name: str
) -> None:
    """Copies a template to dest folder"""
    os.mkdir(f"{dest}/{project_name}")
    click.secho(
        f"{CHECKMARK_EMOJI} Made Base Directory: {project_name}",
        fg=SUCCESS_COLOR,
        bold=True,
        nl=True,
    )

    _copytree(f"{abs_path_to_templates}/{template_name}", f"{dest}/{project_name}")
    click.echo()


def _init_git(dest: os.PathLike) -> None:
    """Initializes git inside a subprocess"""
    child_process = subprocess.Popen("git init", cwd=dest, shell=True)
    child_process.communicate()[0]
    if child_process.returncode == 0:
        click.secho(
            f"{CHECKMARK_EMOJI} Initialized Git Repository",
            fg=SUCCESS_COLOR,
            bold=True,
            nl=True,
        )
        click.echo()
    else:
        click.secho(
            f"{DISAPPOINTING_EMOJI} Failed to initialize git repo",
            fg=ERROR_COLOR,
            nl=True,
        )


def _add_and_commit_git(commit_message: str, git_path: os.PathLike) -> None:
    """Adds and commits git files inside a subprocess"""
    subprocess.Popen(f"git add .", cwd=git_path, shell=True).wait()
    child_process = subprocess.Popen(
        f'git commit -am "{commit_message}"', cwd=git_path, shell=True
    )
    child_process.communicate()[0]
    if child_process.returncode == 0:
        click.secho(
            f"{CHECKMARK_EMOJI} Did an Initial commit",
            fg=SUCCESS_COLOR,
            bold=True,
            nl=True,
        )
        click.echo()
    else:
        click.secho(f"{DISAPPOINTING_EMOJI} Failed to commit", fg=ERROR_COLOR, nl=True)


def _format_keys(file_path: os.PathLike, keys: dict) -> None:
    """Formats keys in a file"""
    original_content = ""
    formatted_content = ""
    with click.open_file(file_path, mode="r") as f:
        original_content = f.read()

    # Could be a better way to do this
    for key, value in keys.items():
        formatted_content = original_content.replace(key, value)

    with click.open_file(file_path, mode="w") as f:
        f.write(formatted_content)


def _format_all_files(files_base_directory: os.PathLike, keys: dict) -> None:
    """Formats all files in a directory"""
    for file_path in glob.iglob(f"{files_base_directory}/**", recursive=True):
        if os.path.isfile(file_path):
            _format_keys(file_path, keys)


def _copy_snippet(
    snippets_dir: os.PathLike,
    project_dir: os.PathLike,
    snippet_name: str,
    keys: dict = None,
) -> None:
    """Copies snippet from snippets dir to project dir"""
    file_path = os.path.join(snippets_dir, snippet_name)
    shutil.copy2(file_path, project_dir)
    _format_keys(file_path, keys)


def _init_and_install_pipenv(project_path: os.PathLike) -> None:
    """"Initializes pipenv and install dependencies"""
    child_process = subprocess.Popen(f"pipenv install", cwd=project_path, shell=True)
    child_process.communicate()[0]
    if child_process.returncode == 0:
        click.secho(
            f"{CHECKMARK_EMOJI} Installed dependencies with pipenv",
            fg=SUCCESS_COLOR,
            bold=True,
            nl=True,
        )
        click.echo()
    else:
        click.secho(
            f"{DISAPPOINTING_EMOJI} Failed to install dependencies with pipenv",
            fg=ERROR_COLOR,
            nl=True,
        )


def generate(
    template_name: str,
    dest: os.PathLike,
    project_name: str,
    default_bot_prefix: str,
    should_init_git: bool,
    should_commit: bool,
    should_use_pipenv: bool,
) -> None:
    """Generates a new project"""
    _copy_template_to_dest(template_name, dest, project_name)

    git_path = os.path.join(dest, project_name)
    project_path = os.path.join(dest, project_name)

    keys_to_format = {
        "{project_name}": project_name,
        "{bot_prefix}": default_bot_prefix,
    }

    _format_all_files(project_path, keys_to_format)

    if should_use_pipenv:
        _copy_snippet(
            abs_path_to_snippets, project_path, "Pipfile", keys=keys_to_format
        )
        _init_and_install_pipenv(project_path)

    if should_init_git:
        _init_git(git_path)

    if should_init_git and should_commit:
        _add_and_commit_git(
            f"Project generated by Discord Bot Generator {SPARKLES_EMOJI}", git_path
        )
