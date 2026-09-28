import configparser
from pathlib import Path

CONFIG_PATH: Path = Path.home() / ".config" / "journal" / "config.ini"
config = configparser.ConfigParser()


def init_config() -> None:
    global config
    config = configparser.ConfigParser()
    save_config()


def add_project(proj_name: str, proj_path: Path) -> None:
    config[f"projects.{proj_name}"] = {"path": str(proj_path)}
    save_config()


def list_projects() -> set[str]:
    _ = config.read(CONFIG_PATH)
    return {
        key.replace("projects.", "")
        for key in config.sections()
        if key.startswith("projects.")
    }


def get_project_path(proj_name: str) -> Path:
    if proj_name not in list_projects():
        raise ValueError(f"Project {proj_name} not found")
    return Path(config[f"projects.{proj_name}"]["path"])


def save_config() -> None:
    if not CONFIG_PATH.parent.exists():
        CONFIG_PATH.parent.mkdir(parents=True)

    with open(CONFIG_PATH, "w") as config_file:
        config.write(config_file)
