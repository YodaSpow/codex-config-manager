from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import subprocess

import pytest

from codex_config_manager.consumer import deploy_latest
from codex_config_manager.errors import PathSafetyError, ValidationError
from codex_config_manager.errors import GitSafetyError
from codex_config_manager.git import consumer_fast_forward
from codex_config_manager.managed_scope import manifests_equal, snapshot_manifest, source_manifest


def make_latest(config) -> None:
    (config.paths.latest_root / "skills" / "future-skill" / "nested").mkdir(parents=True)
    (config.paths.latest_root / "skills" / "future-skill" / "SKILL.md").write_text("one")
    (config.paths.latest_root / "skills" / "future-skill" / "nested" / "x").write_text("x")
    (config.paths.latest_root / "AGENTS.md").write_text("agents")


def test_isolated_consumer_initial_update_noop_and_deletion(make_config) -> None:
    config = make_config(role="consumer", machine="MacMini")
    make_latest(config)
    (config.paths.codex_root / "unrelated.json").write_text("sentinel")
    (config.paths.codex_root / "skills" / ".system").mkdir()
    (config.paths.codex_root / "skills" / ".system" / "preserve").write_text("system")
    (config.paths.codex_root / "skills" / ".DS_Store").write_text("finder")
    assert deploy_latest(config)
    assert not deploy_latest(config)
    assert manifests_equal(snapshot_manifest(config.paths.latest_root), source_manifest(config.paths.codex_root))
    assert (config.paths.codex_root / "unrelated.json").read_text() == "sentinel"
    assert (config.paths.codex_root / "skills" / ".system" / "preserve").read_text() == "system"
    assert (config.paths.codex_root / "skills" / ".DS_Store").read_text() == "finder"
    (config.paths.latest_root / "skills" / "future-skill" / "nested" / "x").unlink()
    assert deploy_latest(config)
    assert not (config.paths.codex_root / "skills" / "future-skill" / "nested" / "x").exists()


def test_consumer_propagates_skill_and_agents_deletion(make_config) -> None:
    config = make_config(role="consumer", machine="MacMini")
    make_latest(config)
    deploy_latest(config)
    for path in sorted((config.paths.latest_root / "skills" / "future-skill").rglob("*"), reverse=True):
        path.unlink() if path.is_file() else path.rmdir()
    (config.paths.latest_root / "skills" / "future-skill").rmdir()
    (config.paths.latest_root / "AGENTS.md").unlink()
    assert deploy_latest(config)
    assert not (config.paths.codex_root / "skills" / "future-skill").exists()
    assert not (config.paths.codex_root / "AGENTS.md").exists()


def test_invalid_latest_stops_before_live_mutation(make_config) -> None:
    config = make_config(role="consumer", machine="MacMini")
    make_latest(config)
    (config.paths.latest_root / "skills" / ".system").mkdir()
    sentinel = config.paths.codex_root / "sentinel"
    sentinel.write_text("unchanged")
    with pytest.raises(ValidationError):
        deploy_latest(config)
    assert sentinel.read_text() == "unchanged"


def test_mac_studio_authoritative_target_is_forbidden(make_config) -> None:
    config = make_config(role="consumer", machine="MacStudio")
    make_latest(config)
    config = replace(
        config,
        paths=replace(config.paths, codex_root=Path("/Users/spowart/.codex")),
    )
    with pytest.raises(PathSafetyError):
        deploy_latest(config)


def _git(repo: Path, *arguments: str) -> str:
    return subprocess.run(
        ["/usr/bin/git", *arguments], cwd=repo, check=True, capture_output=True, text=True
    ).stdout.strip()


def test_consumer_repository_only_fast_forwards(make_config, tmp_path: Path) -> None:
    remote = tmp_path / "remote.git"
    seed = tmp_path / "seed"
    subprocess.run(["/usr/bin/git", "init", "--bare", str(remote)], check=True, capture_output=True)
    seed.mkdir()
    _git(seed, "init", "-b", "main")
    _git(seed, "config", "user.name", "Test")
    _git(seed, "config", "user.email", "test@example.invalid")
    (seed / "README.md").write_text("one")
    _git(seed, "add", "README.md")
    _git(seed, "commit", "-m", "one")
    _git(seed, "remote", "add", "origin", str(remote))
    _git(seed, "push", "-u", "origin", "main")
    config = make_config(role="consumer", machine="MacMini")
    config.paths.repo_root.rmdir()
    subprocess.run(
        ["/usr/bin/git", "clone", "--branch", "main", str(remote), str(config.paths.repo_root)],
        check=True,
        capture_output=True,
    )
    (seed / "README.md").write_text("two")
    _git(seed, "commit", "-am", "two")
    _git(seed, "push")
    updated, sha = consumer_fast_forward(config)
    assert updated
    assert sha == _git(seed, "rev-parse", "HEAD")
    assert consumer_fast_forward(config) == (False, sha)


def test_consumer_repository_rejects_dirty_state(make_config, tmp_path: Path) -> None:
    config = make_config(role="consumer", machine="MacMini")
    repo = config.paths.repo_root
    _git(repo, "init", "-b", "main")
    (repo / "dirty").write_text("x")
    with pytest.raises(GitSafetyError, match="dirty"):
        consumer_fast_forward(config)
