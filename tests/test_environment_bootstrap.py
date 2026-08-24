from __future__ import annotations

import importlib.util
import json
import platform
import sys
from types import SimpleNamespace
from pathlib import Path


def load_bootstrap():
    path = Path(__file__).parents[1] / "scripts" / "bootstrap.py"
    spec = importlib.util.spec_from_file_location("ccm_bootstrap_test", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def create_fake_environment(tmp_path: Path, module, monkeypatch) -> tuple[Path, Path]:
    repo = tmp_path / "repo"
    venv = repo / ".venv"
    bin_root = venv / "bin"
    requirements = repo / "requirements"
    bin_root.mkdir(parents=True)
    requirements.mkdir()
    (repo / "pyproject.toml").write_text("[project]\nname='test'\n")
    lock = requirements / "development.lock"
    lock.write_text("# locked\n")
    (bin_root / "python").symlink_to(sys.executable)
    for name in (
        "codex-config-manager-validate",
        "codex-config-manager-status",
        "codex-config-manager-publisher",
        "codex-config-manager-consumer",
        "codex-config-manager-install",
        "codex-config-manager-uninstall",
    ):
        (bin_root / name).write_text("#!/bin/sh\n")
    module.REPO_ROOT = repo
    module.VENV = venv
    module.RECEIPT = venv / "ccm-environment-receipt.json"
    probe = json.dumps(
        {
            "executable": str(bin_root / "python"),
            "version": platform.python_version(),
            "implementation": platform.python_implementation(),
            "cache_tag": sys.implementation.cache_tag,
            "architecture": platform.machine(),
            "base_executable": getattr(sys, "_base_executable", None),
        }
    )
    monkeypatch.setattr(module.subprocess, "run", lambda *args, **kwargs: SimpleNamespace(stdout=probe))
    module.atomic_json(module.RECEIPT, module.receipt_for("development", lock))
    return repo, lock


def test_receipt_validation_detects_corruption_and_lock_drift(tmp_path: Path, monkeypatch) -> None:
    module = load_bootstrap()
    _, lock = create_fake_environment(tmp_path, module, monkeypatch)
    assert module.validate("development")
    original = module.RECEIPT.read_text()
    module.RECEIPT.write_text("not-json")
    assert not module.validate("development")
    module.RECEIPT.write_text(original)
    lock.write_text("# changed lock\n")
    assert not module.validate("development")


def test_receipt_validation_detects_missing_entry_point(tmp_path: Path, monkeypatch) -> None:
    module = load_bootstrap()
    create_fake_environment(tmp_path, module, monkeypatch)
    (module.VENV / "bin" / "codex-config-manager-consumer").unlink()
    assert not module.validate("development")


def test_safe_venv_target_rejects_broad_or_renamed_target(tmp_path: Path) -> None:
    module = load_bootstrap()
    repo = tmp_path / "repo"
    repo.mkdir()
    module.REPO_ROOT = repo
    module.VENV = repo / "not-the-venv"
    try:
        module.safe_venv_target()
    except SystemExit as exc:
        assert "unsafe" in str(exc)
    else:
        raise AssertionError("unsafe environment target was accepted")
