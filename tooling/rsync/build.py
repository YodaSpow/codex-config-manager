#!/usr/bin/env python3
"""Build the pinned upstream rsync into the repository-owned runtime."""

from __future__ import annotations

import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import tarfile
import tempfile
import urllib.request
from datetime import UTC, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CONTRACT_PATH = Path(__file__).with_name("contract.json")
TOOLS_ROOT = REPO_ROOT / ".tools"
ACTIVE = TOOLS_ROOT / "rsync"


def sha256(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(chunk)
    return result.hexdigest()


def run(command: list[str], *, cwd: Path | None = None, capture: bool = False) -> str:
    result = subprocess.run(
        command,
        cwd=cwd,
        check=True,
        text=True,
        capture_output=capture,
        env={
            **os.environ,
            "LC_ALL": "C",
            "LANG": "C",
            "PATH": "/usr/bin:/bin:/usr/sbin:/sbin",
        },
    )
    return result.stdout if capture else ""


def safe_target(path: Path) -> None:
    if path.parent.resolve() != TOOLS_ROOT.resolve() or path.name not in {
        "rsync",
        "rsync.previous",
    }:
        raise SystemExit(f"refusing unsafe rsync target: {path}")


def validate(binary: Path, contract: dict[str, object]) -> dict[str, object]:
    if binary.resolve() != (ACTIVE / "bin" / "rsync").resolve():
        raise SystemExit(f"unexpected rsync path: {binary}")
    version = run([str(binary), "--version"], capture=True)
    if f"rsync  version {contract['version']}" not in version:
        raise SystemExit("rsync version does not match contract")
    help_output = run([str(binary), "--help"], capture=True)
    for argument in contract["required_arguments"]:
        if argument not in help_output:
            raise SystemExit(f"required rsync argument unavailable: {argument}")
    linkage = run(["/usr/bin/otool", "-L", str(binary)], capture=True)
    for prefix in contract["forbidden_runtime_prefixes"]:
        if prefix in linkage:
            raise SystemExit(f"forbidden runtime linkage: {prefix}")
    file_output = run(["/usr/bin/file", str(binary)], capture=True)
    if platform.machine() == "arm64" and "arm64" not in file_output:
        raise SystemExit("rsync is not arm64")
    return {
        "executable_sha256": sha256(binary),
        "file_output": file_output.strip(),
        "linkage": linkage.splitlines()[1:],
        "version_first_line": version.splitlines()[0],
    }


def main() -> int:
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    TOOLS_ROOT.mkdir(mode=0o700, exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix="rsync-build-", dir=TOOLS_ROOT))
    archive = work / f"rsync-{contract['version']}.tar.gz"
    source = work / f"rsync-{contract['version']}"
    stage = work / "stage"
    try:
        with urllib.request.urlopen(contract["source_url"], timeout=60) as response:
            archive.write_bytes(response.read())
        if sha256(archive) != contract["source_sha256"]:
            raise SystemExit("rsync source SHA-256 mismatch")
        with tarfile.open(archive, "r:gz") as bundle:
            root = source.name + "/"
            if any(
                (member.name != source.name and not member.name.startswith(root))
                or member.name.startswith("/")
                or ".." in Path(member.name).parts
                for member in bundle.getmembers()
            ):
                raise SystemExit("unsafe rsync source archive member")
            bundle.extractall(work, filter="data")
        configure = [str(source / "configure"), f"--prefix={stage}", *contract["configure_flags"]]
        run(configure, cwd=source)
        run(["/usr/bin/make", f"-j{max(1, os.cpu_count() or 1)}"], cwd=source)
        run(["/usr/bin/make", "install"], cwd=source)
        installed = stage / "bin" / "rsync"
        if not installed.is_file():
            raise SystemExit("rsync build did not produce bin/rsync")
        candidate = TOOLS_ROOT / "rsync.candidate"
        if candidate.exists():
            shutil.rmtree(candidate)
        candidate.mkdir(mode=0o700)
        (candidate / "bin").mkdir()
        (candidate / "lib").mkdir()
        shutil.copy2(installed, candidate / "bin" / "rsync")
        safe_target(ACTIVE)
        backup = TOOLS_ROOT / "rsync.previous"
        safe_target(backup)
        if backup.exists():
            shutil.rmtree(backup)
        if ACTIVE.exists():
            ACTIVE.rename(backup)
        candidate.rename(ACTIVE)
        evidence = validate(ACTIVE / "bin" / "rsync", contract)
        receipt = {
            "receipt_version": 1,
            "contract_version": contract["contract_version"],
            "rsync_version": contract["version"],
            "source_url": contract["source_url"],
            "source_sha256": contract["source_sha256"],
            "configure_flags": contract["configure_flags"],
            "architecture": platform.machine(),
            "platform": platform.platform(),
            "compiler": run(["/usr/bin/clang", "--version"], capture=True).splitlines()[0],
            "built_at": datetime.now(UTC).isoformat(),
            **evidence,
        }
        temporary = ACTIVE / ".build-receipt.json.tmp"
        temporary.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        os.replace(temporary, ACTIVE / "build-receipt.json")
        if backup.exists():
            shutil.rmtree(backup)
    finally:
        if work.exists():
            shutil.rmtree(work)
    print(f"rsync ready: {ACTIVE / 'bin' / 'rsync'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
