from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from journal.config import CONFIG_PATH, add_project, list_projects
from journal.helper import sanitize_text

app = typer.Typer(help="A CLI to journal your hardware projects")
console = Console(markup=False)


@app.command()
def project(
    proj_name: str,
    path: Annotated[Path, typer.Option(prompt=True)],
    content: Annotated[str, typer.Option(prompt=True)],
) -> None:
    typer.echo(f"name: {proj_name}")
    typer.echo(f"path: {path}")
    typer.echo(f"content: {content}")

    proj_name = sanitize_text(proj_name)
    path = path.expanduser().resolve()
    content = sanitize_text(content, strict=False) + "\n"

    if not proj_name in list_projects():
        typer.echo(f"Creating new project {proj_name}")
        add_project(proj_name, path)
    else:
        typer.echo(f"Updating project {proj_name}")

    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)

    with open(path / "JOURNAL.md", "w") as f:
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
