from pathlib import Path
from typing import Annotated

import typer

from journal.helper import sanitize_text

app = typer.Typer(help="A CLI to journal your hardware projects")


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
    content = sanitize_text(content) + "\n"

    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)

    with open(path / "JOURNAL.md", "w") as f:
        _ = f.write(content)


def main() -> None:
    """Main entry point"""
    app()
