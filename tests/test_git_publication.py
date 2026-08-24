from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from codex_config_manager.errors import GitSafetyError
from codex_config_manager.git import (
    commit_and_push,
    derive_components,
    render_message,
    retry_pending,
    stage_managed_transaction,
)
from codex_config_manager.state import StateStore

from conftest import run_git


def init_repo(repo: Path) -> None:
    run_git(repo, "init", "-b", "main")
    run_git(repo, "config", "user.name", "Test")
    run_git(repo, "config", "user.email", "test@example.invalid")
    (repo / "README.md").write_text("# Test\n")
    (repo / "latest" / "skills" / "old-skill").mkdir(parents=True)
    (repo / "latest" / "skills" / "old-skill" / "SKILL.md").write_text("old")
    (repo / "latest" / "AGENTS.md").write_text("old agents")
    (repo / "upload-ready" / "skills").mkdir(parents=True)
    (repo / "upload-ready" / "skills" / "old-skill.zip").write_bytes(b"old zip")
    (repo / "upload-ready" / "global-agents.zip").write_bytes(b"old agents zip")
    run_git(repo, "add", ".")
    run_git(repo, "commit", "-m", "initial")


def test_component_classification_and_order(make_config) -> None:
    config = make_config()
    init_repo(config.paths.repo_root)
    (config.paths.latest_root / "AGENTS.md").write_text("new agents")
    (config.paths.latest_root / "skills" / "old-skill" / "SKILL.md").write_text("updated")
    (config.paths.latest_root / "skills" / "new-skill").mkdir()
    (config.paths.latest_root / "skills" / "new-skill" / "SKILL.md").write_text("new")
    (config.paths.upload_ready_root / "skills" / "new-skill.zip").write_bytes(b"new zip")
    paths = stage_managed_transaction(config, ("new-skill", "old-skill"))
    assert "latest/AGENTS.md" in paths
    components = derive_components(config)
    assert [(item.name, item.action) for item in components] == [
        ("AGENTS.md", "updated"),
        ("new-skill", "added"),
        ("old-skill", "updated"),
    ]
    message = render_message(components, "MacStudio")
    assert message.startswith("managed-state:")
    assert message.endswith("publisher: MacStudio\n")
    assert "SKILL.md" not in message


def test_initial_untracked_artifact_tree_is_enumerated_by_file(make_config) -> None:
    config = make_config()
    repo = config.paths.repo_root
    run_git(repo, "init", "-b", "main")
    run_git(repo, "config", "user.name", "Test")
    run_git(repo, "config", "user.email", "test@example.invalid")
    (repo / "README.md").write_text("# Test\n")
    run_git(repo, "add", "README.md")
    run_git(repo, "commit", "-m", "initial")
    (config.paths.latest_root / "skills" / "new-skill").mkdir(parents=True)
    (config.paths.latest_root / "skills" / "new-skill" / "SKILL.md").write_text("new")
    (config.paths.upload_ready_root / "skills").mkdir(parents=True)
    (config.paths.upload_ready_root / "skills" / "new-skill.zip").write_bytes(b"zip")
    staged = stage_managed_transaction(config, ("new-skill",))
    assert "latest/skills/new-skill/SKILL.md" in staged
    assert "upload-ready/skills/new-skill.zip" in staged


def test_deletion_is_staged_and_classified(make_config) -> None:
    config = make_config()
    init_repo(config.paths.repo_root)
    for path in (
        config.paths.latest_root / "skills" / "old-skill" / "SKILL.md",
        config.paths.upload_ready_root / "skills" / "old-skill.zip",
    ):
        path.unlink()
    (config.paths.latest_root / "skills" / "old-skill").rmdir()
    stage_managed_transaction(config, ())
    components = derive_components(config)
    assert [(item.name, item.action) for item in components] == [("old-skill", "removed")]


def test_unrelated_dirty_file_is_rejected(make_config) -> None:
    config = make_config()
    init_repo(config.paths.repo_root)
    (config.paths.repo_root / "unrelated.txt").write_text("no")
    with pytest.raises(GitSafetyError):
        stage_managed_transaction(config, ("old-skill",))
    assert not run_git(config.paths.repo_root, "diff", "--cached", "--name-only")


def test_noop_suppresses_staging(make_config) -> None:
    config = make_config()
    init_repo(config.paths.repo_root)
    assert stage_managed_transaction(config, ("old-skill",)) == []


def test_long_component_set_has_fixed_fallback() -> None:
    from codex_config_manager.git import ComponentChange

    components = tuple(ComponentChange(f"skill-{index:02d}", "updated") for index in range(10))
    message = render_message(components, "MacStudio")
    assert message.splitlines()[0] == "managed-state: publish 10 component changes"


def test_git_code_contains_no_force_push() -> None:
    source = (Path(__file__).parents[1] / "src" / "codex_config_manager" / "git.py").read_text()
    assert "--force" not in source
    assert "git add ." not in source


def test_failed_push_preserves_exact_commit_and_retry(make_config, tmp_path: Path) -> None:
    config = make_config()
    repo = config.paths.repo_root
    init_repo(repo)
    remote = tmp_path / "remote.git"
    subprocess.run(["/usr/bin/git", "init", "--bare", str(remote)], check=True, capture_output=True)
    run_git(repo, "remote", "add", "origin", str(remote))
    run_git(repo, "push", "-u", "origin", "main")
    (config.paths.latest_root / "AGENTS.md").write_text("updated")
    stage_managed_transaction(config, ("old-skill",))
    hook = remote / "hooks" / "pre-receive"
    hook.write_text("#!/bin/sh\nexit 1\n")
    hook.chmod(0o755)
    store = StateStore(config.paths.runtime_state_root)
    state = store.default()
    with pytest.raises(GitSafetyError):
        commit_and_push(config, store, state, source_fingerprint="fingerprint")
    state, _ = store.load()
    pending = state["pending_publication"]
    assert isinstance(pending, dict) and isinstance(pending["commit_sha"], str)
    failed_sha = pending["commit_sha"]
    hook.unlink()
    retried = retry_pending(config, store, state)
    assert retried is not None and retried.sha == failed_sha
    assert run_git(repo, "rev-parse", "origin/main") == failed_sha
