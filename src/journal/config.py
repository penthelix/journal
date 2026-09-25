import configparser
from pathlib import Path

CONFIG_PATH: Path = Path.home() / ".config" / "journal" / "config.ini"
config = configparser.ConfigParser()


def add_project(proj_name: str, proj_path: Path):
    config[f"projects.{proj_name}"] = {"path": str(proj_path)}
    save_config()


def list_projects() -> set[str]:
    return set(config.sections())


def save_config():
    if not CONFIG_PATH.parent.exists():
        CONFIG_PATH.parent.mkdir(parents=True)

    with open(CONFIG_PATH, "w") as configfile:
        config.write(configfile)
