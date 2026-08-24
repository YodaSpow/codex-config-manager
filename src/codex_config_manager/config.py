"""Safe YAML configuration loading and role-aware validation."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import yaml

from .duration import parse_duration
from .errors import ConfigurationError
from .identity import require_identity
from .paths import canonical, reject_overlap, repository_paths, require_absolute_directory

MACHINE_ID = re.compile(r"^[A-Za-z][A-Za-z0-9_-]{1,63}$")
LOCAL_TIME = re.compile(r"^(?:[01][0-9]|2[0-3]):[0-5][0-9]$")
PUBLICATION_MODES = {"after_settle", "paused", "scheduled", "throttled"}


@dataclass(frozen=True)
class ScheduleConfig:
    frequency: str
    local_time: str
    timezone: str


@dataclass(frozen=True)
class PublicationConfig:
    mode: str
    schedule: ScheduleConfig
    minimum_interval: int


@dataclass(frozen=True)
class PublisherConfig:
    check_interval: int
    settle_period: int
    publication: PublicationConfig


@dataclass(frozen=True)
class ConsumerConfig:
    check_interval: int


@dataclass(frozen=True)
class PathConfig:
    codex_root: Path
    repo_root: Path
    runtime_state_root: Path
    lock_root: Path
    log_root: Path
    latest_root: Path
    upload_ready_root: Path
    rsync_binary: Path


@dataclass(frozen=True)
class GitConfig:
    remote: str
    branch: str
    url: str | None


@dataclass(frozen=True)
class Config:
    contract_version: int
    machine_id: str
    role: str
    paths: PathConfig
    publisher: PublisherConfig
    consumer: ConsumerConfig
    git: GitConfig


def _mapping(value: object, label: str) -> dict[str, object]:
    if not isinstance(value, dict) or any(not isinstance(key, str) for key in value):
        raise ConfigurationError(f"{label} must be a mapping with string keys")
    return value


def _keys(value: dict[str, object], *, label: str, required: set[str]) -> None:
    missing = required - value.keys()
    unknown = value.keys() - required
    if missing:
        raise ConfigurationError(f"{label} missing keys: {', '.join(sorted(missing))}")
    if unknown:
        raise ConfigurationError(f"{label} unknown keys: {', '.join(sorted(unknown))}")


def _text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ConfigurationError(f"{label} must be non-empty text")
    return value


def load_config(
    path: str | Path,
    *,
    invoked_role: str | None = None,
    detected_machine: str | None = None,
) -> Config:
    config_path = Path(path).expanduser().resolve(strict=False)
    if not config_path.is_file():
        raise ConfigurationError(f"configuration file is missing: {config_path}")
    try:
        raw = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        raise ConfigurationError(f"unable to load configuration safely: {exc}") from exc
    root = _mapping(raw, "configuration")
    _keys(
        root,
        label="configuration",
        required={"contract_version", "machine", "role", "paths", "publisher", "consumer", "git"},
    )
    if root["contract_version"] != 1:
        raise ConfigurationError("contract_version must be 1")
    machine = _mapping(root["machine"], "machine")
    _keys(machine, label="machine", required={"id"})
    machine_id = _text(machine["id"], "machine.id")
    if not MACHINE_ID.fullmatch(machine_id):
        raise ConfigurationError("machine.id is malformed")
    role = _text(root["role"], "role")
    if role not in {"publisher", "consumer"}:
        raise ConfigurationError("role must be publisher or consumer")
    if invoked_role is not None and role != invoked_role:
        raise ConfigurationError(f"configured role {role!r} cannot run {invoked_role!r}")
    require_identity(machine_id, detected=detected_machine)

    paths = _mapping(root["paths"], "paths")
    _keys(
        paths,
        label="paths",
        required={"codex_root", "repo_root", "runtime_state_root", "lock_root", "log_root"},
    )
    codex_root = require_absolute_directory(_text(paths["codex_root"], "paths.codex_root"), label="Codex root")
    repo_root = require_absolute_directory(_text(paths["repo_root"], "paths.repo_root"), label="repository root")
    latest_root, uploads_root, _ = repository_paths(repo_root)
    runtime_root = require_absolute_directory(
        _text(paths["runtime_state_root"], "paths.runtime_state_root"),
        label="runtime state root",
        exists=False,
    )
    lock_root = require_absolute_directory(
        _text(paths["lock_root"], "paths.lock_root"), label="lock root", exists=False
    )
    log_root = require_absolute_directory(
        _text(paths["log_root"], "paths.log_root"), label="log root", exists=False
    )
    reject_overlap(codex_root, repo_root)
    rsync_binary = canonical(repo_root / ".tools" / "rsync" / "bin" / "rsync")

    publisher = _mapping(root["publisher"], "publisher")
    _keys(publisher, label="publisher", required={"check_interval", "settle_period", "publication"})
    check_interval = parse_duration(
        publisher["check_interval"], field="publisher.check_interval", minimum=10, maximum=3600
    )
    settle_period = parse_duration(
        publisher["settle_period"], field="publisher.settle_period", minimum=60, maximum=604800
    )
    if settle_period < check_interval:
        raise ConfigurationError("publisher.settle_period must be >= check_interval")
    publication = _mapping(publisher["publication"], "publisher.publication")
    _keys(publication, label="publisher.publication", required={"mode", "schedule", "minimum_interval"})
    mode = _text(publication["mode"], "publisher.publication.mode")
    if mode not in PUBLICATION_MODES:
        raise ConfigurationError(f"unknown publication mode: {mode}")
    schedule = _mapping(publication["schedule"], "publisher.publication.schedule")
    _keys(schedule, label="publisher.publication.schedule", required={"frequency", "local_time", "timezone"})
    frequency = _text(schedule["frequency"], "publisher.publication.schedule.frequency")
    if frequency != "daily":
        raise ConfigurationError("scheduled frequency must be daily")
    local_time = _text(schedule["local_time"], "publisher.publication.schedule.local_time")
    if not LOCAL_TIME.fullmatch(local_time):
        raise ConfigurationError("scheduled local_time must use strict HH:MM")
    timezone = _text(schedule["timezone"], "publisher.publication.schedule.timezone")
    try:
        ZoneInfo(timezone)
    except ZoneInfoNotFoundError as exc:
        raise ConfigurationError(f"unknown IANA timezone: {timezone}") from exc
    minimum_interval = parse_duration(
        publication["minimum_interval"],
        field="publisher.publication.minimum_interval",
        minimum=60,
        maximum=2592000,
    )
    if minimum_interval < check_interval:
        raise ConfigurationError("publisher.publication.minimum_interval must be >= check_interval")

    consumer = _mapping(root["consumer"], "consumer")
    _keys(consumer, label="consumer", required={"check_interval"})
    consumer_interval = parse_duration(
        consumer["check_interval"], field="consumer.check_interval", minimum=10, maximum=86400
    )
    git = _mapping(root["git"], "git")
    _keys(git, label="git", required={"remote", "branch", "url"})
    remote = _text(git["remote"], "git.remote")
    branch = _text(git["branch"], "git.branch")
    url = _text(git["url"], "git.url")
    if any(character.isspace() for character in remote + branch + url):
        raise ConfigurationError("git remote, branch, and URL cannot contain whitespace")

    return Config(
        contract_version=1,
        machine_id=machine_id,
        role=role,
        paths=PathConfig(
            codex_root=codex_root,
            repo_root=repo_root,
            runtime_state_root=runtime_root,
            lock_root=lock_root,
            log_root=log_root,
            latest_root=latest_root,
            upload_ready_root=uploads_root,
            rsync_binary=rsync_binary,
        ),
        publisher=PublisherConfig(
            check_interval=check_interval,
            settle_period=settle_period,
            publication=PublicationConfig(
                mode=mode,
                schedule=ScheduleConfig(frequency, local_time, timezone),
                minimum_interval=minimum_interval,
            ),
        ),
        consumer=ConsumerConfig(check_interval=consumer_interval),
        git=GitConfig(remote=remote, branch=branch, url=url),
    )
