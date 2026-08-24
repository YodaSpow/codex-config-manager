"""Exact repository-owned rsync execution and validation."""

from __future__ import annotations

import hashlib
import json
import subprocess
from dataclasses import dataclass
from pathlib import Path

from .errors import RsyncError


@dataclass(frozen=True)
class RsyncResult:
    changed: bool
    itemized: tuple[str, ...]


def _sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def validate_rsync(binary: Path) -> dict[str, object]:
    expected = binary.parent.parent / "build-receipt.json"
    if binary.name != "rsync" or binary.parent.name != "bin" or not binary.is_file():
        raise RsyncError(f"repository-owned rsync is missing: {binary}")
    if not expected.is_file():
        raise RsyncError(f"rsync build receipt is missing: {expected}")
    try:
        receipt = json.loads(expected.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise RsyncError(f"invalid rsync build receipt: {exc}") from exc
    if receipt.get("executable_sha256") != _sha256(binary):
        raise RsyncError("rsync executable hash does not match its build receipt")
    try:
        version = subprocess.run(
            [str(binary), "--version"], check=True, capture_output=True, text=True, timeout=15
        ).stdout
        linkage = subprocess.run(
            ["/usr/bin/otool", "-L", str(binary)],
            check=True,
            capture_output=True,
            text=True,
            timeout=15,
        ).stdout
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        raise RsyncError(f"rsync validation failed: {exc}") from exc
    if "rsync  version 3.5.0" not in version:
        raise RsyncError("rsync version is outside the selected contract")
    if "/opt/homebrew" in linkage or "/usr/local/Cellar" in linkage:
        raise RsyncError("rsync has forbidden Homebrew runtime linkage")
    return receipt


def arguments(
    binary: Path,
    source: Path,
    destination: Path,
    *,
    dry_run: bool,
    exclude_system: bool,
) -> list[str]:
    command = [
        str(binary),
        "--archive",
        "--checksum",
        "--delete",
        "--omit-dir-times",
        "--itemize-changes",
        "--out-format=%i|%n%L",
        "--exclude=.DS_Store",
    ]
    if exclude_system:
        command.append("--exclude=/.system/")
    if dry_run:
        command.append("--dry-run")
    command.extend([f"{source}/", f"{destination}/"])
    if "--delete-excluded" in command:
        raise AssertionError("forbidden rsync option constructed")
    return command


def sync_tree(
    binary: Path,
    source: Path,
    destination: Path,
    *,
    dry_run: bool,
    exclude_system: bool = False,
) -> RsyncResult:
    if not source.is_dir():
        raise RsyncError(f"rsync source is not a directory: {source}")
    if dry_run and not destination.is_dir():
        return RsyncResult(changed=True, itemized=("missing-destination|.",))
    destination.mkdir(parents=True, exist_ok=True)
    command = arguments(
        binary, source, destination, dry_run=dry_run, exclude_system=exclude_system
    )
    try:
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
            timeout=300,
        )
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        detail = getattr(exc, "stderr", None) or str(exc)
        raise RsyncError(f"rsync failed: {detail.strip()}") from exc
    lines = tuple(line for line in result.stdout.splitlines() if line.strip())
    return RsyncResult(changed=bool(lines), itemized=lines)


def sync_file(binary: Path, source: Path, destination_directory: Path, *, dry_run: bool) -> RsyncResult:
    if not source.is_file() or source.is_symlink():
        raise RsyncError(f"rsync file source is invalid: {source}")
    if dry_run and not destination_directory.is_dir():
        return RsyncResult(changed=True, itemized=("missing-destination|.",))
    destination_directory.mkdir(parents=True, exist_ok=True)
    command = [
        str(binary),
        "--archive",
        "--checksum",
        "--itemize-changes",
        "--out-format=%i|%n%L",
    ]
    if dry_run:
        command.append("--dry-run")
    command.extend([str(source), f"{destination_directory}/"])
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True, timeout=300)
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        detail = getattr(exc, "stderr", None) or str(exc)
        raise RsyncError(f"rsync file copy failed: {detail.strip()}") from exc
    lines = tuple(line for line in result.stdout.splitlines() if line.strip())
    return RsyncResult(changed=bool(lines), itemized=lines)
