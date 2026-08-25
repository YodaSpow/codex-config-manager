from __future__ import annotations

import pytest

from codex_config_manager.errors import GitSafetyError
from codex_config_manager.git import github_raw_base


@pytest.mark.parametrize(
    "remote_url",
    (
        "git@github.com:octo-org/example-repo.git",
        "ssh://git@github.com/octo-org/example-repo.git",
        "https://github.com/octo-org/example-repo.git",
        "https://github.com/octo-org/example-repo",
    ),
)
def test_github_raw_base_supports_canonical_transport_forms(remote_url: str) -> None:
    assert github_raw_base(remote_url, "stable") == (
        "https://raw.githubusercontent.com/octo-org/example-repo/stable"
    )


def test_github_raw_base_derives_each_identity_component() -> None:
    assert github_raw_base("git@github.com:different-owner/different-repo.git", "release-2") == (
        "https://raw.githubusercontent.com/different-owner/different-repo/release-2"
    )


@pytest.mark.parametrize(
    ("remote_url", "branch"),
    (
        ("git@gitlab.com:owner/repo.git", "main"),
        ("git@github.com:owner/", "main"),
        ("https://github.com/owner/repo/extra", "main"),
        ("https://github.com/owner/../repo", "main"),
        ("https://github.com/owner/%2e%2e", "main"),
        ("https://github.com/owner/repo.git?token=value", "main"),
        ("https://github.com/owner/repo.git#fragment", "main"),
        ("https://token@github.com/owner/repo.git", "main"),
        ("https://user:password@github.com/owner/repo.git", "main"),
        ("ssh://other@github.com/owner/repo.git", "main"),
        ("ssh://git@github.com:22/owner/repo.git", "main"),
        ("git@github.com:owner/repo.git\n", "main"),
        ("git@github.com:owner/repo.git", ""),
        ("git@github.com:owner/repo.git", "feature/topic"),
        ("git@github.com:owner/repo.git", ".."),
        ("git@github.com:owner/repo.git", "main?download=1"),
    ),
)
def test_github_raw_base_rejects_unsafe_or_ambiguous_identity(
    remote_url: str, branch: str
) -> None:
    with pytest.raises(GitSafetyError):
        github_raw_base(remote_url, branch)
