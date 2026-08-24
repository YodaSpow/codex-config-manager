from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from codex_config_manager.config import (
    Config,
    ConsumerConfig,
    GitConfig,
    PathConfig,
    PublicationConfig,
    PublisherConfig,
    ScheduleConfig,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
RSYNC = REPO_ROOT / ".tools" / "rsync" / "bin" / "rsync"


def run_git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["/usr/bin/git", *args], cwd=repo, check=True, capture_output=True, text=True
    )
    return result.stdout.strip()


@pytest.fixture
def make_config(tmp_path: Path):
    def factory(*, role: str = "publisher", machine: str = "MacStudio") -> Config:
        repo = tmp_path / "repo"
        codex = tmp_path / "codex"
        repo.mkdir(exist_ok=True)
        (codex / "skills").mkdir(parents=True, exist_ok=True)
        return Config(
            contract_version=1,
            machine_id=machine,
            role=role,
            paths=PathConfig(
                codex_root=codex,
                repo_root=repo,
                runtime_state_root=tmp_path / "state",
                lock_root=tmp_path / "locks",
                log_root=tmp_path / "logs",
                latest_root=repo / "latest",
                upload_ready_root=repo / "upload-ready",
                rsync_binary=RSYNC,
            ),
            publisher=PublisherConfig(
                check_interval=60,
                settle_period=300,
                publication=PublicationConfig(
                    mode="after_settle",
                    schedule=ScheduleConfig("daily", "18:00", "Europe/London"),
                    minimum_interval=3600,
                ),
            ),
            consumer=ConsumerConfig(check_interval=300),
            git=GitConfig(remote="origin", branch="main"),
        )

    return factory
