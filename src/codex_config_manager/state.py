"""Atomic, bounded publisher state and settled-mode eligibility."""

from __future__ import annotations

import json
import os
import subprocess
import time
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from .config import PublisherConfig
from .errors import ValidationError


def _iso(value: datetime) -> str:
    return value.astimezone(UTC).isoformat()


def _parse(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return None
    return parsed


def current_boot_id() -> str:
    try:
        result = subprocess.run(
            ["/usr/sbin/sysctl", "-n", "kern.boottime"],
            check=True,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        raise ValidationError(f"unable to establish boot identity: {exc}") from exc
    value = result.stdout.strip()
    if not value:
        raise ValidationError("boot identity is empty")
    return value


@dataclass(frozen=True)
class Eligibility:
    eligible: bool
    settled: bool
    reason: str
    quiet_seconds: float


class StateStore:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.path = root / "publisher-state.json"
        self.temporary = root / ".publisher-state.json.tmp"

    def default(self) -> dict[str, object]:
        return {
            "receipt_version": 1,
            "boot_id": None,
            "last_observed_monotonic_ns": None,
            "last_observed_at": None,
            "last_published_fingerprint": None,
            "last_successful_publication_at": None,
            "last_successful_publication_monotonic_ns": None,
            "last_successful_sha": None,
            "last_scheduled_date": None,
            "pending_fingerprint": None,
            "pending_first_observed_at": None,
            "quiet_since_at": None,
            "quiet_since_monotonic_ns": None,
            "publication_mode": None,
            "pending_publication": None,
            "last_result": None,
        }

    def load(self) -> tuple[dict[str, object], str | None]:
        if not self.path.exists():
            return self.default(), "state receipt missing; settlement restarted"
        try:
            value = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return self.default(), "state receipt corrupt; settlement restarted"
        if not isinstance(value, dict) or value.get("receipt_version") != 1:
            return self.default(), "state receipt incompatible; settlement restarted"
        result = self.default()
        result.update(value)
        return result, None

    def save(self, value: dict[str, object]) -> None:
        self.root.mkdir(parents=True, exist_ok=True, mode=0o700)
        if self.temporary.exists():
            self.temporary.unlink()
        with self.temporary.open("w", encoding="utf-8") as stream:
            json.dump(value, stream, indent=2, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(self.temporary, self.path)
        directory = os.open(self.root, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)

    def observe(
        self,
        fingerprint: str,
        publisher: PublisherConfig,
        *,
        now: datetime | None = None,
        monotonic_ns: int | None = None,
        boot_id: str | None = None,
    ) -> tuple[dict[str, object], Eligibility]:
        state, recovery = self.load()
        current = now or datetime.now(UTC)
        mono = monotonic_ns if monotonic_ns is not None else time.monotonic_ns()
        boot = boot_id or current_boot_id()
        previous_mono = state.get("last_observed_monotonic_ns")
        same_boot = state.get("boot_id") == boot
        clock_valid = same_boot and isinstance(previous_mono, int) and mono >= previous_mono
        if not clock_valid:
            state["pending_fingerprint"] = None
            state["quiet_since_monotonic_ns"] = None
            state["quiet_since_at"] = None
            state["pending_first_observed_at"] = None
            if state.get("last_successful_sha"):
                state["last_successful_publication_monotonic_ns"] = mono
        state["boot_id"] = boot
        state["last_observed_monotonic_ns"] = mono
        state["last_observed_at"] = _iso(current)
        state["publication_mode"] = publisher.publication.mode

        if fingerprint == state.get("last_published_fingerprint"):
            state["pending_fingerprint"] = None
            state["quiet_since_monotonic_ns"] = None
            state["quiet_since_at"] = None
            state["pending_first_observed_at"] = None
            state["last_result"] = "no managed change"
            self.save(state)
            return state, Eligibility(False, True, "matches last published source", 0.0)

        if fingerprint != state.get("pending_fingerprint"):
            state["pending_fingerprint"] = fingerprint
            state["pending_first_observed_at"] = _iso(current)
            state["quiet_since_at"] = _iso(current)
            state["quiet_since_monotonic_ns"] = mono
            state["last_result"] = recovery or "managed change observed; settlement started"
            self.save(state)
            return state, Eligibility(False, False, state["last_result"], 0.0)

        quiet_since = state.get("quiet_since_monotonic_ns")
        if not isinstance(quiet_since, int) or mono < quiet_since:
            state["quiet_since_monotonic_ns"] = mono
            state["quiet_since_at"] = _iso(current)
            state["last_result"] = "untrusted elapsed time; settlement restarted"
            self.save(state)
            return state, Eligibility(False, False, state["last_result"], 0.0)
        quiet = (mono - quiet_since) / 1_000_000_000
        settled = quiet >= publisher.settle_period
        if not settled:
            remaining = max(0, publisher.settle_period - quiet)
            state["last_result"] = f"settling; {remaining:.0f}s remaining"
            self.save(state)
            return state, Eligibility(False, False, state["last_result"], quiet)

        mode = publisher.publication.mode
        eligible = False
        reason = ""
        if mode == "after_settle":
            eligible, reason = True, "settled and eligible"
        elif mode == "paused":
            reason = "settled; publication paused"
        elif mode == "throttled":
            last = state.get("last_successful_publication_monotonic_ns")
            if state.get("last_successful_sha") is None:
                eligible, reason = True, "settled; first publication is not throttled"
            elif isinstance(last, int) and mono >= last:
                elapsed = (mono - last) / 1_000_000_000
                eligible = elapsed >= publisher.publication.minimum_interval
                reason = (
                    "settled and throttle interval elapsed"
                    if eligible
                    else f"settled; throttle has {publisher.publication.minimum_interval - elapsed:.0f}s remaining"
                )
            else:
                reason = "settled; throttle timing cannot be proven"
        elif mode == "scheduled":
            schedule = publisher.publication.schedule
            local = current.astimezone(ZoneInfo(schedule.timezone))
            target_hour, target_minute = (int(part) for part in schedule.local_time.split(":"))
            boundary = local.replace(hour=target_hour, minute=target_minute, second=0, microsecond=0)
            quiet_wall = _parse(state.get("quiet_since_at"))
            at_boundary = local.hour == target_hour and local.minute == target_minute
            already = state.get("last_scheduled_date") == local.date().isoformat()
            settled_before = quiet_wall is not None and quiet_wall.astimezone(ZoneInfo(schedule.timezone)) <= boundary
            eligible = at_boundary and not already and settled_before
            reason = (
                "settled and scheduled boundary eligible"
                if eligible
                else "settled; waiting for next strict scheduled boundary"
            )
        state["last_result"] = reason
        self.save(state)
        return state, Eligibility(eligible, True, reason, quiet)

    def record_success(
        self,
        *,
        source_fingerprint: str,
        commit_sha: str,
        machine_id: str,
        components: list[dict[str, str]],
        now: datetime | None = None,
        monotonic_ns: int | None = None,
        scheduled_timezone: str | None = None,
    ) -> dict[str, object]:
        state, _ = self.load()
        current = now or datetime.now(UTC)
        mono = monotonic_ns if monotonic_ns is not None else time.monotonic_ns()
        state.update(
            {
                "last_published_fingerprint": source_fingerprint,
                "last_successful_publication_at": _iso(current),
                "last_successful_publication_monotonic_ns": mono,
                "last_successful_sha": commit_sha,
                "last_publisher": machine_id,
                "last_components": components,
                "pending_fingerprint": None,
                "pending_first_observed_at": None,
                "quiet_since_at": None,
                "quiet_since_monotonic_ns": None,
                "pending_publication": None,
                "last_result": "publication pushed successfully",
            }
        )
        if state.get("publication_mode") == "scheduled":
            if scheduled_timezone is None:
                raise ValidationError("scheduled publication success requires its configured timezone")
            state["last_scheduled_date"] = current.astimezone(
                ZoneInfo(scheduled_timezone)
            ).date().isoformat()
        self.save(state)
        return state
