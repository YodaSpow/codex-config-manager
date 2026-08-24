#!/usr/bin/env python3
"""Create, validate, or deliberately repair the repository virtual environment."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
from datetime import UTC, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
VENV = REPO_ROOT / ".venv"
RECEIPT = VENV / "ccm-environment-receipt.json"


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def safe_venv_target() -> None:
    if VENV.parent.resolve() != REPO_ROOT.resolve() or VENV.name != ".venv":
        raise SystemExit(f"refusing unsafe environment target: {VENV}")


def run(command: list[str]) -> None:
    subprocess.run(command, cwd=REPO_ROOT, check=True)


def receipt_for(environment: str, lock: Path) -> dict[str, object]:
    python = VENV / "bin" / "python"
    probe = subprocess.run(
        [
            str(python),
            "-c",
            "import json,platform,sys; print(json.dumps({"
            "'executable':sys.executable,'version':platform.python_version(),"
            "'implementation':platform.python_implementation(),"
            "'cache_tag':sys.implementation.cache_tag,'architecture':platform.machine(),"
            "'base_executable':getattr(sys,'_base_executable',None)}))",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    result = json.loads(probe.stdout)
    result.update(
        {
            "receipt_version": 1,
            "environment": environment,
            "lock_path": lock.relative_to(REPO_ROOT).as_posix(),
            "lock_sha256": digest(lock),
            "project_version": "0.1.0",
            "repo_root": str(REPO_ROOT),
            "pyproject_sha256": digest(REPO_ROOT / "pyproject.toml"),
            "validated_at": datetime.now(UTC).isoformat(),
        }
    )
    return result


def atomic_json(path: Path, value: dict[str, object]) -> None:
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(value, stream, indent=2, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def validate(environment: str) -> bool:
    lock_name = "development.lock" if environment == "development" else "runtime.lock"
    lock = REPO_ROOT / "requirements" / lock_name
    python = VENV / "bin" / "python"
    commands = [
        VENV / "bin" / "codex-config-manager-validate",
        VENV / "bin" / "codex-config-manager-status",
        VENV / "bin" / "codex-config-manager-publisher",
        VENV / "bin" / "codex-config-manager-consumer",
    ]
    if not python.is_file() or not RECEIPT.is_file() or any(not item.is_file() for item in commands):
        return False
    try:
        current = json.loads(RECEIPT.read_text(encoding="utf-8"))
        expected = receipt_for(environment, lock)
        stable = (
            "environment",
            "lock_path",
            "lock_sha256",
            "project_version",
            "repo_root",
            "pyproject_sha256",
            "implementation",
            "cache_tag",
            "architecture",
        )
        if any(current.get(key) != expected.get(key) for key in stable):
            return False
        subprocess.run(
            [str(python), "-c", "import yaml, codex_config_manager"],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
        )
    except (OSError, ValueError, subprocess.CalledProcessError):
        return False
    return True


def build(environment: str) -> None:
    safe_venv_target()
    lock_name = "development.lock" if environment == "development" else "runtime.lock"
    lock = REPO_ROOT / "requirements" / lock_name
    if not lock.is_file():
        raise SystemExit(f"missing lock: {lock}")
    backup = REPO_ROOT / ".venv.previous"
    if backup.exists():
        if backup.parent.resolve() != REPO_ROOT.resolve() or backup.name != ".venv.previous":
            raise SystemExit(f"refusing unsafe environment backup: {backup}")
        shutil.rmtree(backup)
    if VENV.exists():
        VENV.rename(backup)
    try:
        run([sys.executable, "-m", "venv", str(VENV)])
        candidate_python = VENV / "bin" / "python"
        run(
            [
                str(candidate_python),
                "-m",
                "pip",
                "install",
                "--disable-pip-version-check",
                "--require-hashes",
                "--no-deps",
                "-r",
                str(lock),
            ]
        )
        run(
            [
                str(candidate_python),
                "-m",
                "pip",
                "install",
                "--disable-pip-version-check",
                "--no-build-isolation",
                "--no-deps",
                "-e",
                str(REPO_ROOT),
            ]
        )
        atomic_json(RECEIPT, receipt_for(environment, lock))
    except Exception:
        if VENV.exists():
            safe_venv_target()
            shutil.rmtree(VENV)
        if backup.exists():
            backup.rename(VENV)
        raise
    if backup.exists():
        shutil.rmtree(backup)
    if not validate(environment):
        raise SystemExit("environment validation failed after bootstrap")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--environment", choices=("runtime", "development"), default="development")
    parser.add_argument("--repair", action="store_true")
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    if validate(args.environment):
        print(f"environment valid: {VENV}")
        return 0
    if args.validate_only:
        print(f"environment invalid: {VENV}", file=sys.stderr)
        return 1
    if VENV.exists() and not args.repair:
        print("environment is stale; rerun with --repair", file=sys.stderr)
        return 1
    build(args.environment)
    print(f"environment ready: {VENV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
