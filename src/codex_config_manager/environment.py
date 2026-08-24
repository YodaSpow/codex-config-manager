"""Read-only validation of the repository-owned Python environment."""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
from pathlib import Path

from .errors import ValidationError


def _digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def validate_environment(repo_root: Path) -> dict[str, object]:
    venv = repo_root / ".venv"
    receipt_path = venv / "ccm-environment-receipt.json"
    python = venv / "bin" / "python"
    commands = (
        "codex-config-manager-publisher",
        "codex-config-manager-consumer",
        "codex-config-manager-install",
        "codex-config-manager-uninstall",
        "codex-config-manager-status",
        "codex-config-manager-validate",
    )
    if not python.is_file() or not receipt_path.is_file():
        raise ValidationError("repository-owned Python environment or receipt is missing")
    if any(not (venv / "bin" / name).is_file() for name in commands):
        raise ValidationError("repository-owned Python environment is missing console commands")
    try:
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ValidationError(f"environment receipt is invalid: {exc}") from exc
    lock_name = "development.lock" if receipt.get("environment") == "development" else "runtime.lock"
    lock = repo_root / "requirements" / lock_name
    if not lock.is_file() or receipt.get("lock_sha256") != _digest(lock):
        raise ValidationError("environment receipt does not match the selected dependency lock")
    if receipt.get("repo_root") != str(repo_root.resolve()):
        raise ValidationError("environment receipt belongs to a different repository root")
    pyproject = repo_root / "pyproject.toml"
    if not pyproject.is_file() or receipt.get("pyproject_sha256") != _digest(pyproject):
        raise ValidationError("environment receipt does not match project metadata")
    try:
        probe = subprocess.run(
            [
                str(python),
                "-c",
                "import json,platform,sys,yaml,codex_config_manager; "
                "print(json.dumps({'version':platform.python_version(),"
                "'architecture':platform.machine(),'cache_tag':sys.implementation.cache_tag}))",
            ],
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
            timeout=30,
        )
        actual = json.loads(probe.stdout)
    except (OSError, ValueError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        raise ValidationError(f"environment import validation failed: {exc}") from exc
    for key in ("version", "architecture", "cache_tag"):
        if receipt.get(key) != actual.get(key):
            raise ValidationError(f"environment receipt {key} mismatch")
    if actual.get("architecture") != platform.machine():
        raise ValidationError("environment architecture differs from the current machine")
    return receipt
