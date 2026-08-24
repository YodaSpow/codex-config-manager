from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime
from pathlib import Path

from codex_config_manager.config import PublicationConfig, PublisherConfig, ScheduleConfig
from codex_config_manager.state import StateStore


def publisher(mode: str = "after_settle") -> PublisherConfig:
    return PublisherConfig(
        check_interval=60,
        settle_period=300,
        publication=PublicationConfig(
            mode=mode,
            schedule=ScheduleConfig("daily", "18:00", "Europe/London"),
            minimum_interval=3600,
        ),
    )


def observe(store: StateStore, fingerprint: str, seconds: int, config: PublisherConfig, *, day: int = 24):
    return store.observe(
        fingerprint,
        config,
        now=datetime(2026, 8, day, 16, 0, tzinfo=UTC),
        monotonic_ns=seconds * 1_000_000_000,
        boot_id="boot-a",
    )


def test_after_settle_waits_full_period(tmp_path: Path) -> None:
    store = StateStore(tmp_path)
    assert not observe(store, "one", 100, publisher())[1].eligible
    assert not observe(store, "one", 399, publisher())[1].eligible
    eligible = observe(store, "one", 400, publisher())[1]
    assert eligible.eligible and eligible.settled


def test_new_change_restarts_settlement(tmp_path: Path) -> None:
    store = StateStore(tmp_path)
    observe(store, "one", 100, publisher())
    observe(store, "one", 400, publisher())
    changed = observe(store, "two", 401, publisher())[1]
    assert not changed.eligible and changed.quiet_seconds == 0


def test_boot_change_restarts_settlement(tmp_path: Path) -> None:
    store = StateStore(tmp_path)
    observe(store, "one", 100, publisher())
    _, eligibility = store.observe(
        "one",
        publisher(),
        now=datetime(2026, 8, 24, 16, 10, tzinfo=UTC),
        monotonic_ns=10,
        boot_id="boot-b",
    )
    assert not eligibility.eligible


def test_pause_observes_but_never_eligible(tmp_path: Path) -> None:
    store = StateStore(tmp_path)
    observe(store, "one", 100, publisher("paused"))
    result = observe(store, "one", 400, publisher("paused"))[1]
    assert result.settled and not result.eligible
    assert "paused" in result.reason


def test_throttle_uses_last_success_not_failed_attempt(tmp_path: Path) -> None:
    store = StateStore(tmp_path)
    config = publisher("throttled")
    observe(store, "one", 100, config)
    assert observe(store, "one", 400, config)[1].eligible
    store.record_success(
        source_fingerprint="one",
        commit_sha="a" * 40,
        machine_id="MacStudio",
        components=[],
        now=datetime(2026, 8, 24, 16, 0, tzinfo=UTC),
        monotonic_ns=400 * 1_000_000_000,
    )
    observe(store, "two", 500, config)
    held = observe(store, "two", 800, config)[1]
    assert not held.eligible and "throttle" in held.reason
    assert observe(store, "two", 4000, config)[1].eligible


def test_strict_scheduled_boundary_and_london_date(tmp_path: Path) -> None:
    store = StateStore(tmp_path)
    config = publisher("scheduled")
    store.observe(
        "one",
        config,
        now=datetime(2026, 8, 24, 16, 54, tzinfo=UTC),
        monotonic_ns=100 * 1_000_000_000,
        boot_id="boot-a",
    )
    _, boundary = store.observe(
        "one",
        config,
        now=datetime(2026, 8, 24, 17, 0, tzinfo=UTC),
        monotonic_ns=460 * 1_000_000_000,
        boot_id="boot-a",
    )
    assert boundary.eligible
    state = store.record_success(
        source_fingerprint="one",
        commit_sha="b" * 40,
        machine_id="MacStudio",
        components=[],
        now=datetime(2026, 8, 24, 23, 30, tzinfo=UTC),
        monotonic_ns=470 * 1_000_000_000,
        scheduled_timezone="Europe/London",
    )
    assert state["last_scheduled_date"] == "2026-08-25"


def test_missed_schedule_does_not_catch_up(tmp_path: Path) -> None:
    store = StateStore(tmp_path)
    config = publisher("scheduled")
    store.observe(
        "one", config, now=datetime(2026, 8, 24, 16, 0, tzinfo=UTC), monotonic_ns=0, boot_id="boot"
    )
    _, result = store.observe(
        "one", config, now=datetime(2026, 8, 24, 18, 0, tzinfo=UTC), monotonic_ns=7200_000_000_000, boot_id="boot"
    )
    assert not result.eligible


def test_success_receipt_clears_pending_and_remains_bounded(tmp_path: Path) -> None:
    store = StateStore(tmp_path)
    state, _ = observe(store, "one", 100, publisher())
    state["pending_publication"] = {"commit_sha": "x"}
    store.save(state)
    saved = store.record_success(
        source_fingerprint="one",
        commit_sha="c" * 40,
        machine_id="MacStudio",
        components=[{"name": "AGENTS.md", "action": "updated"}],
        monotonic_ns=500,
    )
    assert saved["pending_publication"] is None
    assert saved["last_successful_sha"] == "c" * 40
    assert list(tmp_path.glob("*.json")) == [store.path]
