from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from codex_config_manager.consumer import deploy_latest
from codex_config_manager.errors import PathSafetyError, ValidationError
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
