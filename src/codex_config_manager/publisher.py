"""Mac Studio publisher orchestration."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

from .artifacts import (
    build_distribution,
    reconcile_readme,
    validate_distribution,
)
from .config import Config
from .errors import GitSafetyError, ValidationError
from .environment import validate_environment
from .git import (
    commit_and_push,
    github_raw_base,
    require_clean_base,
    retry_pending,
    stage_managed_transaction,
)
from .locking import execution_lock
from .logging_setup import configure_logging
from .managed_scope import snapshot_manifest, source_manifest
from .rsync import sync_tree, validate_rsync
from .snapshot import private_candidate, reconcile_latest
from .state import StateStore


def _validate_existing_uploads(config: Config, current_skills: set[str]) -> None:
    root = config.paths.upload_ready_root
    if not root.exists():
        return
    allowed_root = {"global-agents.zip", "skills", ".DS_Store"}
    unexpected = sorted(item.name for item in root.iterdir() if item.name not in allowed_root)
    if unexpected:
        raise ValidationError(f"unexpected upload-ready entries: {unexpected}")
    skills = root / "skills"
    if skills.exists():
        invalid = sorted(
            item.name
            for item in skills.iterdir()
            if item.name != ".DS_Store"
            and (not item.is_file() or not item.name.endswith(".zip"))
        )
        if invalid:
            raise ValidationError(f"unexpected upload-ready skill entries: {invalid}")


def _atomic_readme(path: Path, value: str) -> None:
    temporary = path.with_name(f".{path.name}.ccm.tmp")
    temporary.write_text(value, encoding="utf-8")
    os.replace(temporary, path)


def _apply_projection(
    config: Config,
    candidate: Path,
    skills: tuple[str, ...],
    *,
    download_base: str,
) -> bool:
    repo = config.paths.repo_root
    readme = repo / "README.md"
    original = readme.read_text(encoding="utf-8")
    rendered = reconcile_readme(
        original,
        has_agents=(candidate / "AGENTS.md").is_file(),
        skills=skills,
        download_base=download_base,
    )
    with tempfile.TemporaryDirectory(prefix="codex-config-manager-artifacts-") as directory:
        projected = Path(directory) / "upload-ready"
        build_distribution(candidate, projected)
        validate_distribution(candidate, projected)
        _validate_existing_uploads(config, set(skills))
        latest_changed = reconcile_latest(candidate, config.paths.latest_root, config.paths.rsync_binary)
        upload_changed = sync_tree(
            config.paths.rsync_binary,
            projected,
            config.paths.upload_ready_root,
            dry_run=True,
        ).changed
        if upload_changed:
            sync_tree(
                config.paths.rsync_binary,
                projected,
                config.paths.upload_ready_root,
                dry_run=False,
            )
            if sync_tree(
                config.paths.rsync_binary,
                projected,
                config.paths.upload_ready_root,
                dry_run=True,
            ).changed:
                raise ValidationError("upload-ready projection is not equivalent after reconciliation")
        if rendered != original:
            _atomic_readme(readme, rendered)
        snapshot_manifest(config.paths.latest_root)
        validate_distribution(config.paths.latest_root, config.paths.upload_ready_root)
        return latest_changed or upload_changed or rendered != original


def run_publisher(config: Config) -> str:
    logger = configure_logging(config.paths.log_root, "publisher")
    state_store = StateStore(config.paths.runtime_state_root)
    with execution_lock(config.paths.lock_root, "publisher"):
        validate_environment(config.paths.repo_root)
        validate_rsync(config.paths.rsync_binary)
        state, _ = state_store.load()
        pending = state.get("pending_publication")
        if isinstance(pending, dict):
            if config.publisher.publication.mode == "paused":
                logger.info("pending publication held because mode is paused")
                return "pending publication held: paused"
            commit = retry_pending(config, state_store, state)
            if commit is None:
                raise GitSafetyError("pending publication state is incomplete")
            fingerprint = str(pending.get("source_fingerprint"))
            state_store.record_success(
                source_fingerprint=fingerprint,
                commit_sha=commit.sha,
                machine_id=config.machine_id,
                components=[item.record() for item in commit.components],
                scheduled_timezone=config.publisher.publication.schedule.timezone,
            )
            logger.info("retried publication sha=%s components=%s", commit.sha, len(commit.components))
            return f"publication retry pushed: {commit.sha}"

        manifest = source_manifest(config.paths.codex_root)
        state, eligibility = state_store.observe(manifest.fingerprint, config.publisher)
        logger.info(
            "observation mode=%s settled=%s eligible=%s reason=%s",
            config.publisher.publication.mode,
            eligibility.settled,
            eligibility.eligible,
            eligibility.reason,
        )
        if not eligibility.eligible:
            return eligibility.reason
        git_status = require_clean_base(config)
        download_base = github_raw_base(str(git_status["remote_url"]), config.git.branch)
        with private_candidate(config.paths.codex_root, config.paths.rsync_binary) as (candidate, candidate_manifest):
            if candidate_manifest.fingerprint != manifest.fingerprint:
                raise ValidationError("eligible source changed before private candidate completed")
            _apply_projection(
                config,
                candidate,
                candidate_manifest.skills,
                download_base=download_base,
            )
        staged = stage_managed_transaction(config, candidate_manifest.skills)
        if not staged:
            head = subprocess_head(config.paths.repo_root)
            state_store.record_success(
                source_fingerprint=manifest.fingerprint,
                commit_sha=head,
                machine_id=config.machine_id,
                components=[],
                scheduled_timezone=config.publisher.publication.schedule.timezone,
            )
            logger.info("source already equals current repository state sha=%s", head)
            return "managed source already equals published repository state"
        commit = commit_and_push(
            config,
            state_store,
            state,
            source_fingerprint=manifest.fingerprint,
        )
        if commit is None:
            raise GitSafetyError("staged transaction disappeared before commit")
        state_store.record_success(
            source_fingerprint=manifest.fingerprint,
            commit_sha=commit.sha,
            machine_id=config.machine_id,
            components=[item.record() for item in commit.components],
            scheduled_timezone=config.publisher.publication.schedule.timezone,
        )
        logger.info("publication pushed sha=%s components=%s", commit.sha, len(commit.components))
        return f"publication pushed: {commit.sha}"


def subprocess_head(repo: Path) -> str:
    import subprocess

    result = subprocess.run(
        ["/usr/bin/git", "rev-parse", "HEAD"],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
        timeout=30,
    )
    return result.stdout.strip()
