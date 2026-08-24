"""Bounded consumer update and deployment orchestration."""

from __future__ import annotations

import os
from pathlib import Path

from .config import Config
from .errors import PathSafetyError, ValidationError
from .git import consumer_fast_forward
from .locking import execution_lock
from .logging_setup import configure_logging
from .managed_scope import manifests_equal, snapshot_manifest, source_manifest
from .paths import canonical
from .rsync import sync_file, sync_tree, validate_rsync


def deploy_latest(config: Config) -> bool:
    codex_root = canonical(config.paths.codex_root)
    authoritative_studio = Path("/Users/spowart/.codex").resolve()
    if config.machine_id == "MacStudio" and codex_root == authoritative_studio:
        raise PathSafetyError("consumer cannot target the Mac Studio authoritative .codex")
    latest = config.paths.latest_root
    desired = snapshot_manifest(latest)
    codex_root.mkdir(parents=True, exist_ok=True)
    target_skills = codex_root / "skills"
    target_skills.mkdir(parents=True, exist_ok=True)
    changed = False
    desired_agents = latest / "AGENTS.md"
    target_agents = codex_root / "AGENTS.md"
    if desired_agents.exists():
        dry = sync_file(config.paths.rsync_binary, desired_agents, codex_root, dry_run=True)
        if dry.changed:
            sync_file(config.paths.rsync_binary, desired_agents, codex_root, dry_run=False)
            changed = True
    elif target_agents.exists():
        if target_agents.is_symlink() or not target_agents.is_file():
            raise ValidationError("consumer AGENTS.md deletion target is not a regular file")
        target_agents.unlink()
        changed = True
    skills_dry = sync_tree(
        config.paths.rsync_binary,
        latest / "skills",
        target_skills,
        dry_run=True,
        exclude_system=True,
    )
    if skills_dry.changed:
        sync_tree(
            config.paths.rsync_binary,
            latest / "skills",
            target_skills,
            dry_run=False,
            exclude_system=True,
        )
        changed = True
    if sync_tree(
        config.paths.rsync_binary,
        latest / "skills",
        target_skills,
        dry_run=True,
        exclude_system=True,
    ).changed:
        raise ValidationError("consumer skills target is not equivalent after deployment")
    actual = source_manifest(codex_root)
    if not manifests_equal(desired, actual):
        raise ValidationError("consumer live managed state does not equal latest/")
    return changed


def run_consumer(config: Config) -> str:
    logger = configure_logging(config.paths.log_root, "consumer")
    with execution_lock(config.paths.lock_root, "consumer"):
        validate_rsync(config.paths.rsync_binary)
        updated, sha = consumer_fast_forward(config)
        changed = deploy_latest(config)
        logger.info("consumer repository_updated=%s deployed=%s sha=%s", updated, changed, sha)
        return f"consumer complete: repository_updated={updated} deployed={changed} sha={sha}"
