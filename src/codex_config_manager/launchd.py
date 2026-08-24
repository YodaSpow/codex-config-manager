"""Role-specific LaunchAgent rendering, installation, and inspection."""

from __future__ import annotations

import os
import plistlib
import subprocess
from pathlib import Path

from .config import Config
from .environment import validate_environment
from .errors import ValidationError

LABELS = {
    "publisher": "com.yodaspow.codex-config-manager.publisher",
    "consumer": "com.yodaspow.codex-config-manager.consumer",
}


def label_for(role: str) -> str:
    try:
        return LABELS[role]
    except KeyError as exc:
        raise ValidationError(f"unsupported launchd role: {role}") from exc


def agent_path(role: str) -> Path:
    return Path.home() / "Library" / "LaunchAgents" / f"{label_for(role)}.plist"


def render(config: Config) -> bytes:
    role = config.role
    label = label_for(role)
    interval = (
        config.publisher.check_interval if role == "publisher" else config.consumer.check_interval
    )
    executable = config.paths.repo_root / ".venv" / "bin" / f"codex-config-manager-{role}"
    plist = {
        "Label": label,
        "ProgramArguments": [
            str(executable),
            "--config",
            str(config.paths.repo_root / "config" / "config.yaml"),
        ],
        "WorkingDirectory": str(config.paths.repo_root),
        "StartInterval": interval,
        "RunAtLoad": True,
        "ProcessType": "Background",
        "StandardOutPath": str(config.paths.log_root / f"{role}-launchd.stdout.log"),
        "StandardErrorPath": str(config.paths.log_root / f"{role}-launchd.stderr.log"),
    }
    return plistlib.dumps(plist, fmt=plistlib.FMT_XML, sort_keys=True)


def _launchctl(arguments: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["/bin/launchctl", *arguments],
        check=check,
        capture_output=True,
        text=True,
        timeout=30,
    )


def inspect(role: str) -> dict[str, object]:
    label = label_for(role)
    domain = f"gui/{os.getuid()}"
    result = _launchctl(["print", f"{domain}/{label}"], check=False)
    return {
        "label": label,
        "path": str(agent_path(role)),
        "plist_exists": agent_path(role).is_file(),
        "loaded": result.returncode == 0,
    }


def install(config: Config) -> Path:
    if config.role == "consumer" and config.machine_id == "MacStudio":
        raise ValidationError("consumer LaunchAgent installation is forbidden on the Mac Studio")
    validate_environment(config.paths.repo_root)
    for directory in (config.paths.runtime_state_root, config.paths.lock_root, config.paths.log_root):
        directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    destination = agent_path(config.role)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(f".{destination.name}.ccm.tmp")
    temporary.write_bytes(render(config))
    os.chmod(temporary, 0o600)
    os.replace(temporary, destination)
    domain = f"gui/{os.getuid()}"
    _launchctl(["bootout", f"{domain}/{label_for(config.role)}"], check=False)
    try:
        _launchctl(["bootstrap", domain, str(destination)])
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        raise ValidationError(f"launchd bootstrap failed: {exc}") from exc
    state = inspect(config.role)
    if not state["loaded"]:
        raise ValidationError("LaunchAgent was written but is not loaded")
    return destination


def uninstall(config: Config) -> Path:
    destination = agent_path(config.role)
    domain = f"gui/{os.getuid()}"
    _launchctl(["bootout", f"{domain}/{label_for(config.role)}"], check=False)
    if destination.exists():
        if destination.is_symlink() or not destination.is_file():
            raise ValidationError(f"refusing unexpected LaunchAgent target: {destination}")
        destination.unlink()
    return destination
