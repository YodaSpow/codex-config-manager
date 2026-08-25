from __future__ import annotations

from contextlib import contextmanager
from dataclasses import replace
from pathlib import Path

from codex_config_manager.publisher import run_publisher
from codex_config_manager.state import Eligibility


def test_paused_publisher_never_reaches_candidate_or_git(make_config, monkeypatch) -> None:
    config = make_config()
    config = replace(
        config,
        publisher=replace(
            config.publisher,
            publication=replace(config.publisher.publication, mode="paused"),
        ),
    )
    monkeypatch.setattr("codex_config_manager.publisher.validate_environment", lambda unused: {})
    monkeypatch.setattr("codex_config_manager.publisher.validate_rsync", lambda unused: {})
    manifest = type("Manifest", (), {"fingerprint": "fingerprint", "skills": ()})()
    monkeypatch.setattr("codex_config_manager.publisher.source_manifest", lambda unused: manifest)
    monkeypatch.setattr(
        "codex_config_manager.publisher.StateStore.observe",
        lambda self, fingerprint, publisher: (
            self.default(),
            Eligibility(False, True, "settled; publication paused", 300),
        ),
    )
    monkeypatch.setattr(
        "codex_config_manager.publisher.require_clean_base",
        lambda unused: (_ for _ in ()).throw(AssertionError("Git must not run")),
    )
    assert run_publisher(config) == "settled; publication paused"
    assert not config.paths.latest_root.exists()
    assert not config.paths.upload_ready_root.exists()


def test_unsettled_publisher_does_not_mutate_repository(make_config, monkeypatch) -> None:
    config = make_config()
    monkeypatch.setattr("codex_config_manager.publisher.validate_environment", lambda unused: {})
    monkeypatch.setattr("codex_config_manager.publisher.validate_rsync", lambda unused: {})
    manifest = type("Manifest", (), {"fingerprint": "fingerprint", "skills": ()})()
    monkeypatch.setattr("codex_config_manager.publisher.source_manifest", lambda unused: manifest)
    monkeypatch.setattr(
        "codex_config_manager.publisher.StateStore.observe",
        lambda self, fingerprint, publisher: (
            self.default(),
            Eligibility(False, False, "settling", 1),
        ),
    )
    assert run_publisher(config) == "settling"
    assert not config.paths.latest_root.exists()


def test_eligible_publisher_passes_validated_git_identity_to_projection(
    make_config, monkeypatch
) -> None:
    config = make_config()
    monkeypatch.setattr("codex_config_manager.publisher.validate_environment", lambda unused: {})
    monkeypatch.setattr("codex_config_manager.publisher.validate_rsync", lambda unused: {})
    manifest = type("Manifest", (), {"fingerprint": "fingerprint", "skills": ("a-skill",)})()
    monkeypatch.setattr("codex_config_manager.publisher.source_manifest", lambda unused: manifest)
    monkeypatch.setattr(
        "codex_config_manager.publisher.StateStore.observe",
        lambda self, fingerprint, publisher: (
            self.default(),
            Eligibility(True, True, "eligible", 300),
        ),
    )
    monkeypatch.setattr(
        "codex_config_manager.publisher.require_clean_base",
        lambda unused: {"remote_url": "git@github.com:example-owner/example-repo.git"},
    )

    candidate = config.paths.repo_root / "candidate"
    candidate.mkdir(parents=True)

    @contextmanager
    def candidate_context(unused_root, unused_rsync):
        yield candidate, manifest

    monkeypatch.setattr("codex_config_manager.publisher.private_candidate", candidate_context)
    captured: dict[str, str] = {}

    def apply_projection(unused_config, unused_candidate, unused_skills, *, download_base):
        captured["download_base"] = download_base
        return True

    monkeypatch.setattr("codex_config_manager.publisher._apply_projection", apply_projection)
    monkeypatch.setattr("codex_config_manager.publisher.stage_managed_transaction", lambda *args: [])
    monkeypatch.setattr("codex_config_manager.publisher.subprocess_head", lambda unused: "a" * 40)

    assert run_publisher(config) == "managed source already equals published repository state"
    assert captured == {
        "download_base": "https://raw.githubusercontent.com/example-owner/example-repo/main"
    }
