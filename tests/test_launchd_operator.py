from __future__ import annotations

import plistlib
import shutil
from pathlib import Path

import pytest

from codex_config_manager.errors import GitSafetyError, ValidationError
from codex_config_manager.launchd import install, render
from codex_config_manager.validation import status, validate_runtime

from conftest import REPO_ROOT


def install_templates(config) -> None:
    target = config.paths.repo_root / "launchd"
    target.mkdir()
    for role in ("publisher", "consumer"):
        shutil.copy2(REPO_ROOT / "launchd" / f"{role}.plist.template", target)


def test_publisher_plist_uses_absolute_repo_owned_command(make_config) -> None:
    config = make_config()
    install_templates(config)
    plist = plistlib.loads(render(config))
    assert plist["Label"].endswith(".publisher")
    assert plist["ProgramArguments"][0] == str(
        config.paths.repo_root / ".venv" / "bin" / "codex-config-manager-publisher"
    )
    assert plist["ProgramArguments"][1:] == [
        "--config",
        str(config.paths.repo_root / "config" / "config.yaml"),
    ]
    assert plist["StartInterval"] == 60
    assert "PATH" not in plist.get("EnvironmentVariables", {})


def test_consumer_plist_uses_separate_interval(make_config) -> None:
    config = make_config(role="consumer", machine="MacMini")
    install_templates(config)
    plist = plistlib.loads(render(config))
    assert plist["Label"].endswith(".consumer")
    assert plist["StartInterval"] == 300


def test_consumer_install_is_forbidden_on_mac_studio(make_config) -> None:
    config = make_config(role="consumer", machine="MacStudio")
    with pytest.raises(ValidationError, match="forbidden"):
        install(config)


def test_status_does_not_create_runtime_directories(make_config, monkeypatch) -> None:
    config = make_config()
    monkeypatch.setattr(
        "codex_config_manager.validation.repository_status",
        lambda unused: {"branch": "main", "head": "a" * 40, "dirty": False},
    )
    monkeypatch.setattr(
        "codex_config_manager.validation.inspect",
        lambda unused: {"loaded": False, "plist_exists": False},
    )
    monkeypatch.setattr(
        "codex_config_manager.validation.validate_environment",
        lambda unused: {"environment": "development"},
    )
    result = status(config)
    assert result["environment_valid"] is True
    assert not config.paths.runtime_state_root.exists()
    assert not config.paths.log_root.exists()


def test_validation_rejects_dirty_repository_before_source_checks(make_config, monkeypatch) -> None:
    config = make_config()
    monkeypatch.setattr("codex_config_manager.validation.validate_environment", lambda unused: {})
    monkeypatch.setattr("codex_config_manager.validation.validate_rsync", lambda unused: {})
    monkeypatch.setattr(
        "codex_config_manager.validation.repository_status",
        lambda unused: {"dirty": True, "ahead": 0, "behind": 0},
    )
    with pytest.raises(GitSafetyError, match="worktree"):
        validate_runtime(config)
