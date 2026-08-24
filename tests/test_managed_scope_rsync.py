from __future__ import annotations

import os
from pathlib import Path

import pytest

from codex_config_manager.errors import ValidationError
from codex_config_manager.managed_scope import manifests_equal, snapshot_manifest, source_manifest
from codex_config_manager.rsync import arguments, sync_tree, validate_rsync
from codex_config_manager.snapshot import private_candidate, reconcile_latest

from conftest import RSYNC


def populate(codex: Path) -> None:
    (codex / "skills" / ".system" / "internal").mkdir(parents=True)
    (codex / "skills" / ".system" / "internal" / "secret.txt").write_text("system")
    (codex / "skills" / "future-skill" / "nested").mkdir(parents=True)
    (codex / "skills" / "future-skill" / "SKILL.md").write_text("skill")
    (codex / "skills" / "future-skill" / "nested" / "data.txt").write_text("nested")
    (codex / "skills" / ".DS_Store").write_bytes(b"finder")
    (codex / "skills" / "future-skill" / ".DS_Store").write_bytes(b"nested finder")
    (codex / "AGENTS.md").write_text("global")
    (codex / "unrelated.json").write_text("unmanaged")


def test_repository_owned_rsync_contract() -> None:
    receipt = validate_rsync(RSYNC)
    assert receipt["rsync_version"] == "3.5.0"
    assert "/opt/homebrew" not in "\n".join(receipt["linkage"])


def test_source_manifest_excludes_system_dsstore_and_unrelated(tmp_path: Path) -> None:
    codex = tmp_path / "codex"
    (codex / "skills").mkdir(parents=True)
    populate(codex)
    manifest = source_manifest(codex)
    paths = {entry.path for entry in manifest.entries}
    assert "skills/future-skill/SKILL.md" in paths
    assert not any(".system" in path or ".DS_Store" in path or "unrelated" in path for path in paths)
    assert manifest.skills == ("future-skill",)


def test_candidate_and_latest_are_equivalent_and_dynamic(tmp_path: Path) -> None:
    codex = tmp_path / "codex"
    (codex / "skills").mkdir(parents=True)
    populate(codex)
    latest = tmp_path / "latest"
    with private_candidate(codex, RSYNC) as (candidate, candidate_manifest):
        assert reconcile_latest(candidate, latest, RSYNC)
        assert manifests_equal(candidate_manifest, snapshot_manifest(latest))
    assert not (latest / "skills" / ".system").exists()
    assert not any(path.name == ".DS_Store" for path in latest.rglob(".DS_Store"))
    with private_candidate(codex, RSYNC) as (candidate, _):
        assert not reconcile_latest(candidate, latest, RSYNC)


def test_dry_run_is_non_mutating_when_destination_missing(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    (source / "file").write_text("x")
    destination = tmp_path / "missing"
    result = sync_tree(RSYNC, source, destination, dry_run=True)
    assert result.changed
    assert not destination.exists()


def test_checksum_detects_same_size_and_timestamp_change(tmp_path: Path) -> None:
    source = tmp_path / "source"
    target = tmp_path / "target"
    source.mkdir()
    target.mkdir()
    left = source / "value"
    right = target / "value"
    left.write_text("aaaa")
    right.write_text("bbbb")
    stamp = 1_700_000_000
    os.utime(left, (stamp, stamp))
    os.utime(right, (stamp, stamp))
    assert sync_tree(RSYNC, source, target, dry_run=True).changed
    sync_tree(RSYNC, source, target, dry_run=False)
    assert right.read_text() == "aaaa"
    assert not sync_tree(RSYNC, source, target, dry_run=True).changed


def test_manifest_fingerprint_detects_executable_mode(tmp_path: Path) -> None:
    codex = tmp_path / "codex"
    skill = codex / "skills" / "mode-skill"
    skill.mkdir(parents=True)
    script = skill / "run.sh"
    script.write_text("#!/bin/sh\n")
    before = source_manifest(codex).fingerprint
    script.chmod(0o755)
    after = source_manifest(codex).fingerprint
    assert before != after


def test_delete_preserves_excluded_noise(tmp_path: Path) -> None:
    source = tmp_path / "source"
    target = tmp_path / "target"
    source.mkdir()
    target.mkdir()
    (target / "remove.txt").write_text("remove")
    (target / ".DS_Store").write_text("preserve")
    sync_tree(RSYNC, source, target, dry_run=False)
    assert not (target / "remove.txt").exists()
    assert (target / ".DS_Store").read_text() == "preserve"


def test_system_exclusion_is_not_delete_excluded(tmp_path: Path) -> None:
    source = tmp_path / "source"
    target = tmp_path / "target"
    (source / ".system").mkdir(parents=True)
    (target / ".system").mkdir(parents=True)
    (source / ".system" / "source").write_text("source")
    (target / ".system" / "preserved").write_text("target")
    command = arguments(RSYNC, source, target, dry_run=False, exclude_system=True)
    assert "--delete-excluded" not in command
    sync_tree(RSYNC, source, target, dry_run=False, exclude_system=True)
    assert (target / ".system" / "preserved").read_text() == "target"
    assert not (target / ".system" / "source").exists()


def test_snapshot_rejects_system_and_symlink(tmp_path: Path) -> None:
    latest = tmp_path / "latest"
    (latest / "skills" / ".system").mkdir(parents=True)
    with pytest.raises(ValidationError):
        snapshot_manifest(latest)
    (latest / "skills" / ".system").rmdir()
    outside = tmp_path / "outside"
    outside.write_text("x")
    (latest / "skills" / "bad").symlink_to(outside)
    with pytest.raises(ValidationError):
        snapshot_manifest(latest)


def test_control_characters_in_skill_names_are_rejected(tmp_path: Path) -> None:
    codex = tmp_path / "codex"
    (codex / "skills" / "bad\nname").mkdir(parents=True)
    with pytest.raises(ValidationError, match="unsafe"):
        source_manifest(codex)
