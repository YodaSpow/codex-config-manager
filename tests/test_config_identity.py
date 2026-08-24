from __future__ import annotations

from pathlib import Path

import pytest

from codex_config_manager.config import load_config
from codex_config_manager.duration import parse_duration
from codex_config_manager.errors import ConfigurationError, IdentityError, PathSafetyError
from codex_config_manager.identity import normalize_model_name


def yaml_text(root: Path, *, mode: str = "after_settle", machine: str = "MacStudio") -> str:
    codex = root / "codex"
    repo = root / "repo"
    (codex / "skills").mkdir(parents=True)
    repo.mkdir()
    return f"""contract_version: 1
machine:
  id: {machine}
role: publisher
paths:
  codex_root: {codex}
  repo_root: {repo}
  runtime_state_root: {root / 'state'}
  lock_root: {root / 'locks'}
  log_root: {root / 'logs'}
publisher:
  check_interval: 1m
  settle_period: 5m
  publication:
    mode: {mode}
    schedule:
      frequency: daily
      local_time: "18:00"
      timezone: Europe/London
    minimum_interval: 1h
consumer:
  check_interval: 5m
git:
  remote: origin
  branch: main
  url: git@github.com:YodaSpow/codex-config-manager.git
"""


def test_model_identity_is_generic_and_deterministic() -> None:
    assert normalize_model_name("Mac Studio") == "MacStudio"
    assert normalize_model_name("Mac mini") == "MacMini"
    assert normalize_model_name("Future Mac Pro") == "FutureMacPro"


@pytest.mark.parametrize("bad", [None, "", "   ", "Mac Studio!"])
def test_bad_model_names_fail(bad: object) -> None:
    with pytest.raises(IdentityError):
        normalize_model_name(bad)


@pytest.mark.parametrize("value,seconds", [("10s", 10), ("1m", 60), ("2h", 7200), ("3d", 259200)])
def test_duration_grammar(value: str, seconds: int) -> None:
    assert parse_duration(value, field="x", minimum=1, maximum=300000) == seconds


@pytest.mark.parametrize("bad", ["0s", "1M", "1.5m", "60", "1h30m", 60, True])
def test_invalid_duration_fails(bad: object) -> None:
    with pytest.raises(ConfigurationError):
        parse_duration(bad, field="x", minimum=1, maximum=300000)


@pytest.mark.parametrize("mode", ["after_settle", "paused", "scheduled", "throttled"])
def test_all_publication_modes_load(tmp_path: Path, mode: str) -> None:
    path = tmp_path / "config.yaml"
    path.write_text(yaml_text(tmp_path, mode=mode), encoding="utf-8")
    config = load_config(path, invoked_role="publisher", detected_machine="MacStudio")
    assert config.publisher.publication.mode == mode
    assert config.publisher.check_interval == 60
    assert config.publisher.settle_period == 300


def test_machine_mismatch_fails(tmp_path: Path) -> None:
    path = tmp_path / "config.yaml"
    path.write_text(yaml_text(tmp_path), encoding="utf-8")
    with pytest.raises(IdentityError):
        load_config(path, detected_machine="MacMini")


def test_wrong_role_fails(tmp_path: Path) -> None:
    path = tmp_path / "config.yaml"
    path.write_text(yaml_text(tmp_path), encoding="utf-8")
    with pytest.raises(ConfigurationError):
        load_config(path, invoked_role="consumer", detected_machine="MacStudio")


def test_overlapping_repo_and_codex_fail(tmp_path: Path) -> None:
    text = yaml_text(tmp_path).replace(str(tmp_path / "repo"), str(tmp_path / "codex" / "repo"))
    (tmp_path / "codex" / "repo").mkdir()
    path = tmp_path / "config.yaml"
    path.write_text(text, encoding="utf-8")
    with pytest.raises(PathSafetyError):
        load_config(path, detected_machine="MacStudio")
