import configparser
from pathlib import Path

import pytest

from journal import config as config_module


@pytest.fixture(autouse=True)
def reset_config():
    """Reset the config module's config object before each test."""
    config_module.config = configparser.ConfigParser()


def set_tmp_config_path(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Set the config path to a temporary file."""
    config_path = tmp_path / "config.ini"
    monkeypatch.setattr(config_module, "CONFIG_PATH", config_path)
    return config_path


def test_add_project(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    config_path = set_tmp_config_path(tmp_path, monkeypatch)
    project_path: Path = tmp_path / "my-project"
    config_module.add_project("my_project", project_path)

    assert config_path.exists()
    saved_config = configparser.ConfigParser()
    _ = saved_config.read(config_path)
    assert saved_config["projects.my_project"]["path"] == str(project_path)


def test_save_config(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    # Test for empty config
    config_path = set_tmp_config_path(tmp_path, monkeypatch)
    config_module.save_config()

    assert config_path.exists()
    saved_config = configparser.ConfigParser()
    _ = saved_config.read(config_path)
    assert saved_config == config_module.config

    # Test for non-empty config
    config_module.config["projects.my_project"] = {"path": str(tmp_path)}
    config_module.save_config()

    assert config_path.exists()
    saved_config = configparser.ConfigParser()
    _ = saved_config.read(config_path)
    assert saved_config["projects.my_project"]["path"] == str(tmp_path)
