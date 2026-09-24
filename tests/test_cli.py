from pathlib import Path

from journal.cli import project


def test_project(tmp_path):
    proj_name: str = "macropad project"
    proj_path: Path = tmp_path / proj_name
    content: str = (
        "I added switches.\nI added a case.\nI added a PCB.\nI added a firmware.\n"
    )
    project(proj_name, proj_path, content)

    assert proj_path.exists()
    assert proj_path.is_dir()
    assert (proj_path / "JOURNAL.md").exists()
