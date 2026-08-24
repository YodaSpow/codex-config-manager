"""Non-mutating role-aware validation and status projection."""

from __future__ import annotations

import json
from pathlib import Path

from .artifacts import validate_distribution
from .config import Config
from .environment import validate_environment
from .errors import GitSafetyError
from .git import repository_status
from .launchd import inspect
from .managed_scope import snapshot_manifest, source_manifest
from .rsync import validate_rsync


def validate_runtime(config: Config) -> dict[str, object]:
    receipt = validate_environment(config.paths.repo_root)
    rsync_receipt = validate_rsync(config.paths.rsync_binary)
    git = repository_status(config)
    if git["dirty"]:
        raise GitSafetyError("repository contains worktree or index changes")
    if git["ahead"]:
        raise GitSafetyError("repository is ahead or diverged from configured upstream")
    result: dict[str, object] = {
        "machine_id": config.machine_id,
        "role": config.role,
        "environment": receipt.get("environment"),
        "python": receipt.get("version"),
        "rsync": rsync_receipt.get("rsync_version"),
        "git": git,
        "launchd": inspect(config.role),
    }
    if config.role == "publisher":
        source = source_manifest(config.paths.codex_root)
        result["source_fingerprint"] = source.fingerprint
        result["source_skills"] = list(source.skills)
    if config.paths.latest_root.exists():
        latest = snapshot_manifest(config.paths.latest_root)
        result["latest_fingerprint"] = latest.fingerprint
        result["latest_skills"] = list(latest.skills)
        if config.paths.upload_ready_root.exists():
            validate_distribution(config.paths.latest_root, config.paths.upload_ready_root)
            result["distribution_valid"] = True
    return result


def status(config: Config) -> dict[str, object]:
    state_path = config.paths.runtime_state_root / "publisher-state.json"
    runtime: dict[str, object] = {}
    if state_path.is_file():
        try:
            value = json.loads(state_path.read_text(encoding="utf-8"))
            if isinstance(value, dict):
                for key in (
                    "last_result",
                    "last_successful_sha",
                    "last_publisher",
                    "last_components",
                    "pending_fingerprint",
                    "publication_mode",
                ):
                    runtime[key] = value.get(key)
        except (OSError, ValueError):
            runtime["state_error"] = "publisher state is unreadable"
    environment_valid = True
    environment_error = None
    try:
        validate_environment(config.paths.repo_root)
    except Exception as exc:  # Status must report, rather than hide, a failed local environment.
        environment_valid = False
        environment_error = str(exc)
    result = {
        "machine_id": config.machine_id,
        "role": config.role,
        "environment_valid": environment_valid,
        "repository": repository_status(config),
        "launchd": inspect(config.role),
        "paths": {
            "codex_root": str(config.paths.codex_root),
            "repo_root": str(config.paths.repo_root),
            "latest_root": str(config.paths.latest_root),
            "upload_ready_root": str(config.paths.upload_ready_root),
            "runtime_state_root": str(config.paths.runtime_state_root),
            "log_root": str(config.paths.log_root),
        },
        "runtime": runtime,
    }
    if environment_error:
        result["environment_error"] = environment_error
    sha = runtime.get("last_successful_sha")
    if isinstance(sha, str):
        result["last_successful_sha_short"] = sha[:12]
    return result
