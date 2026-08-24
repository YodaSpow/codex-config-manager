from __future__ import annotations

import zipfile
from pathlib import Path

import pytest

from codex_config_manager.artifacts import (
    BEGIN_MARKER,
    build_distribution,
    reconcile_readme,
    sha256,
    validate_distribution,
    validate_zip,
)
from codex_config_manager.errors import ValidationError


def make_latest(root: Path) -> Path:
    latest = root / "latest"
    (latest / "skills" / "chat-handoff" / "nested").mkdir(parents=True)
    (latest / "skills" / "chat-handoff" / "SKILL.md").write_text("chat")
    script = latest / "skills" / "chat-handoff" / "run.sh"
    script.write_text("#!/bin/sh\n")
    script.chmod(0o755)
    (latest / "skills" / "chat-handoff" / "nested" / "x.txt").write_text("x")
    (latest / "skills" / "semantic-compression").mkdir()
    (latest / "skills" / "semantic-compression" / "SKILL.md").write_text("semantic")
    (latest / "AGENTS.md").write_text("global")
    return latest


def test_distribution_is_deterministic_and_exact(tmp_path: Path) -> None:
    latest = make_latest(tmp_path)
    first = tmp_path / "first"
    second = tmp_path / "second"
    assert build_distribution(latest, first) == ("chat-handoff", "semantic-compression")
    build_distribution(latest, second)
    validate_distribution(latest, first)
    validate_distribution(latest, second)
    for relative in (
        "global-agents.zip",
        "skills/chat-handoff.zip",
        "skills/semantic-compression.zip",
    ):
        assert sha256(first / relative) == sha256(second / relative)


def test_zip_wrappers_and_global_name(tmp_path: Path) -> None:
    latest = make_latest(tmp_path)
    target = tmp_path / "upload-ready"
    build_distribution(latest, target)
    with zipfile.ZipFile(target / "global-agents.zip") as archive:
        assert archive.namelist() == ["AGENTS.md"]
        assert archive.read("AGENTS.md") == b"global"
    with zipfile.ZipFile(target / "skills" / "chat-handoff.zip") as archive:
        assert all(name.startswith("chat-handoff") for name in archive.namelist())
        script = archive.getinfo("chat-handoff/run.sh")
        assert (script.external_attr >> 16) & 0o111


def test_distribution_rejects_stale_artifact(tmp_path: Path) -> None:
    latest = make_latest(tmp_path)
    target = tmp_path / "upload-ready"
    build_distribution(latest, target)
    (target / "skills" / "stale.zip").write_bytes(b"bad")
    with pytest.raises(ValidationError):
        validate_distribution(latest, target)


def test_distribution_ignores_ds_store_without_removing_it(tmp_path: Path) -> None:
    latest = make_latest(tmp_path)
    target = tmp_path / "upload-ready"
    build_distribution(latest, target)
    noise = target / "skills" / ".DS_Store"
    noise.write_bytes(b"finder")
    validate_distribution(latest, target)
    assert noise.read_bytes() == b"finder"


def test_unsafe_zip_members_rejected(tmp_path: Path) -> None:
    archive_path = tmp_path / "bad.zip"
    with zipfile.ZipFile(archive_path, "w") as archive:
        archive.writestr("../escape", "bad")
    root = tmp_path / "root"
    root.mkdir()
    with pytest.raises(ValidationError):
        validate_zip(archive_path, expected_root=root, wrapper=None)


def test_readme_reconciliation_is_bounded_and_dynamic() -> None:
    original = "# Project\n\nHuman text.\n"
    rendered = reconcile_readme(original, has_agents=True, skills=("a-skill", "z-skill"))
    assert rendered.startswith(original.rstrip())
    assert rendered.count(BEGIN_MARKER) == 1
    assert "[View the current global - AGENTS.md](latest/AGENTS.md)" in rendered
    assert "[Download a-skill](upload-ready/skills/a-skill.zip)" in rendered
    updated = reconcile_readme(rendered, has_agents=True, skills=("z-skill",))
    assert "Human text." in updated
    assert "a-skill.zip" not in updated
    assert updated.count(BEGIN_MARKER) == 1
