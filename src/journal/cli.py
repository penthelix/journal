from pathlib import Path
from typing import Annotated

import typer
from rich import print
from rich.console import Console

from journal.config import CONFIG_PATH, add_project, get_project_path, list_projects
from journal.helper import sanitize_text

app = typer.Typer(help="A CLI to journal your hardware projects")
console = Console(markup=False)


def handle_create_project(proj_name: str, path: Path | None) -> tuple[str, Path]:
    """Handle the case where the project does not exist in the config file"""
    print(f"Creating new project {proj_name}")
    if path is None:
        path = Path(typer.prompt(f"Enter path to project {proj_name}"))
    add_project(proj_name, path)
    return proj_name, path


def handle_existing_project(proj_name: str, path: Path | None) -> tuple[str, Path]:
    """Handle the case where the project already exists in the config file"""
    set_path: Path = get_project_path(proj_name)
    if path is not None:
        if path != set_path and typer.confirm(
            f"Update path for project {proj_name}? (Current: {set_path})"
        ):
            add_project(proj_name, path)
            print(f"Updating path for project {proj_name}")
        else:
            print(
                f"Path for project {proj_name} is already set to {set_path}. You can skip using the --path option."
            )
    else:
        path = set_path
    print(f"Updating project {proj_name}")
    return proj_name, path


def sanitize_inputs(proj_name: str, content: str, path: Path) -> tuple[str, str, Path]:
    """Sanitize the project name, content, and path"""
    proj_name = sanitize_text(proj_name)
    content = sanitize_text(content, strict=False) + "\n"
    path = path.expanduser().resolve()
    return proj_name, content, path


@app.command()
def project(
    proj_name: str,
    content: Annotated[str, typer.Option(prompt=True)],
    path: Annotated[Path | None, typer.Option()] = None,
) -> None:
    if not proj_name in list_projects():
        proj_name, path = handle_create_project(proj_name, path)
    else:
        proj_name, path = handle_existing_project(proj_name, path)

    proj_name, content, path = sanitize_inputs(proj_name, content, path)

    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)

    with open(path / "JOURNAL.md", "a") as f:
        _ = f.write(content)


@app.command()
def config() -> None:
    if not CONFIG_PATH.exists():
        print(f"Config file not found at {CONFIG_PATH}")
        return
    print(f"Fetched config from {CONFIG_PATH}")
    with open(CONFIG_PATH, "r") as f:
        console.print(f.read())


def main() -> None:
    """Main entry point"""
    app()
