"""Conservative Git publication and consumer fast-forward primitives."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from .config import Config
from .errors import GitSafetyError
from .state import StateStore

GIT = "/usr/bin/git"


@dataclass(frozen=True)
class ComponentChange:
    name: str
    action: str

    def record(self) -> dict[str, str]:
        return {"name": self.name, "action": self.action}


@dataclass(frozen=True)
class PublicationCommit:
    sha: str
    components: tuple[ComponentChange, ...]
    message: str


def _run(
    repo: Path,
    arguments: list[str],
    *,
    capture: bool = True,
    input_text: str | None = None,
) -> str:
    try:
        result = subprocess.run(
            [GIT, *arguments],
            cwd=repo,
            check=True,
            capture_output=capture,
            text=True,
            input=input_text,
            timeout=120,
        )
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        detail = getattr(exc, "stderr", None) or str(exc)
        raise GitSafetyError(f"git {' '.join(arguments)} failed: {detail.strip()}") from exc
    return result.stdout.rstrip("\n") if capture else ""


def _tree_contains(repo: Path, revision: str, path: str) -> bool:
    if revision == "INDEX":
        return bool(_run(repo, ["ls-files", "--cached", "--", path]))
    return bool(_run(repo, ["ls-tree", "-r", "--name-only", revision, "--", path]))


def repository_status(config: Config) -> dict[str, object]:
    repo = config.paths.repo_root
    branch = _run(repo, ["branch", "--show-current"])
    head = _run(repo, ["rev-parse", "HEAD"])
    upstream = f"{config.git.remote}/{config.git.branch}"
    remote = _run(repo, ["remote", "get-url", config.git.remote])
    tracking = _run(repo, ["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}"])
    if tracking != upstream:
        raise GitSafetyError(f"branch tracks {tracking!r}, expected {upstream!r}")
    if config.git.url is not None and remote != config.git.url:
        raise GitSafetyError(f"remote URL {remote!r} does not match configured repository identity")
    porcelain = _run(repo, ["status", "--porcelain=v1"])
    counts = _run(repo, ["rev-list", "--left-right", "--count", f"HEAD...{upstream}"])
    ahead, behind = (int(value) for value in counts.split())
    return {
        "branch": branch,
        "head": head,
        "upstream": upstream,
        "tracking": tracking,
        "remote_url": remote,
        "dirty": bool(porcelain),
        "ahead": ahead,
        "behind": behind,
    }


def fetch(config: Config) -> None:
    _run(config.paths.repo_root, ["fetch", "--quiet", config.git.remote, config.git.branch])


def require_clean_base(config: Config) -> dict[str, object]:
    repo = config.paths.repo_root
    if not (repo / ".git").is_dir():
        raise GitSafetyError("repository .git directory is missing")
    fetch(config)
    status = repository_status(config)
    if status["branch"] != config.git.branch:
        raise GitSafetyError(f"expected branch {config.git.branch}, found {status['branch']}")
    if status["dirty"]:
        raise GitSafetyError("repository contains pre-existing worktree or index changes")
    if status["ahead"] or status["behind"]:
        if status["behind"] and not status["ahead"]:
            _run(repo, ["merge", "--ff-only", f"{config.git.remote}/{config.git.branch}"])
            status = repository_status(config)
        else:
            raise GitSafetyError("repository is ahead or diverged without a recognized pending publication")
    return status


def _allowed_path(path: str, allowed_skills: set[str]) -> bool:
    if path == "README.md" or path == "latest" or path.startswith("latest/"):
        return True
    if path == "upload-ready/global-agents.zip":
        return True
    parts = PurePosixPath(path).parts
    return (
        len(parts) == 3
        and parts[:2] == ("upload-ready", "skills")
        and parts[2].endswith(".zip")
        and parts[2][:-4] in allowed_skills
    )


def _status_paths(repo: Path) -> list[str]:
    output = _run(
        repo,
        ["status", "--porcelain=v1", "--no-renames", "--untracked-files=all", "-z"],
    )
    if not output:
        return []
    records = output.split("\x00")
    paths: list[str] = []
    for record in records:
        if not record:
            continue
        if len(record) < 4:
            raise GitSafetyError("malformed porcelain status")
        paths.append(record[3:])
    return paths


def stage_managed_transaction(config: Config, expected_skills: tuple[str, ...]) -> list[str]:
    repo = config.paths.repo_root
    expected = set(expected_skills)
    has_agents_zip = (config.paths.upload_ready_root / "global-agents.zip").is_file()
    tracked_artifacts = _run(repo, ["ls-files", "--", "upload-ready/global-agents.zip", "upload-ready/skills"])
    previous_skills = {
        PurePosixPath(line).name[:-4]
        for line in tracked_artifacts.splitlines()
        if line.startswith("upload-ready/skills/") and line.endswith(".zip")
    }
    allowed_skills = expected | previous_skills
    dirty = _status_paths(repo)
    forbidden = [path for path in dirty if not _allowed_path(path, allowed_skills)]
    if forbidden:
        raise GitSafetyError(f"unattended publication refuses unrelated changes: {forbidden}")
    paths = ["latest", "README.md"]
    if has_agents_zip or "upload-ready/global-agents.zip" in tracked_artifacts.splitlines():
        paths.append("upload-ready/global-agents.zip")
    current = [f"upload-ready/skills/{name}.zip" for name in expected_skills]
    previous = [line for line in tracked_artifacts.splitlines() if line.startswith("upload-ready/skills/")]
    paths.extend(sorted(set(current + previous)))
    _run(repo, ["add", "-A", "--", *paths])
    staged = _run(repo, ["diff", "--cached", "--name-only", "--no-renames"])
    staged_paths = [line for line in staged.splitlines() if line]
    forbidden = [path for path in staged_paths if not _allowed_path(path, allowed_skills)]
    if forbidden:
        raise GitSafetyError(f"Git index contains forbidden publication paths: {forbidden}")
    return staged_paths


def derive_components(config: Config) -> tuple[ComponentChange, ...]:
    repo = config.paths.repo_root
    names = _run(repo, ["diff", "--cached", "--name-only", "--no-renames", "--", "latest"])
    components: set[str] = set()
    for path in names.splitlines():
        parts = PurePosixPath(path).parts
        if parts == ("latest", "AGENTS.md"):
            components.add("AGENTS.md")
        elif len(parts) >= 3 and parts[:2] == ("latest", "skills") and not parts[2].startswith("."):
            components.add(parts[2])
        else:
            raise GitSafetyError(f"unmappable staged managed path: {path}")
    changes: list[ComponentChange] = []
    for name in sorted(components, key=lambda item: (item != "AGENTS.md", item)):
        suffix = "AGENTS.md" if name == "AGENTS.md" else f"skills/{name}"
        before = _tree_contains(repo, "HEAD", f"latest/{suffix}")
        after = _tree_contains(repo, "INDEX", f"latest/{suffix}")
        action = "updated" if before and after else "added" if after else "removed"
        changes.append(ComponentChange(name, action))
    return tuple(changes)


def render_message(components: tuple[ComponentChange, ...], machine_id: str) -> str:
    if not components:
        raise GitSafetyError("cannot render a managed publication without components")
    verb = {"added": "add", "updated": "update", "removed": "remove"}
    fragments = [f"{verb[item.action]} {item.name}" for item in components]
    direct = "managed-state: " + " and ".join(fragments)
    subject = direct if len(direct) <= 72 and len(components) <= 2 else f"managed-state: publish {len(components)} component changes"
    lines = [subject, ""]
    agents = [item for item in components if item.name == "AGENTS.md"]
    if agents:
        lines.extend(["AGENTS.md:", f"  {agents[0].action}", ""])
    skills = [item for item in components if item.name != "AGENTS.md"]
    if skills:
        lines.append("skills:")
        for action in ("added", "updated", "removed"):
            group = [item.name for item in skills if item.action == action]
            if group:
                lines.append(f"  {action}:")
                lines.extend(f"    - {name}" for name in group)
        lines.append("")
    lines.append(f"publisher: {machine_id}")
    return "\n".join(lines) + "\n"


def commit_and_push(
    config: Config,
    state_store: StateStore,
    state: dict[str, object],
    *,
    source_fingerprint: str,
) -> PublicationCommit | None:
    repo = config.paths.repo_root
    staged = _run(repo, ["diff", "--cached", "--name-only"])
    if not staged:
        return None
    components = derive_components(config)
    message = render_message(components, config.machine_id)
    base = _run(repo, ["rev-parse", "HEAD"])
    tree = _run(repo, ["write-tree"])
    state["pending_publication"] = {
        "base_sha": base,
        "tree_sha": tree,
        "source_fingerprint": source_fingerprint,
        "machine_id": config.machine_id,
        "message": message,
        "components": [item.record() for item in components],
        "commit_sha": None,
    }
    state_store.save(state)
    _run(repo, ["commit", "--file=-"], input_text=message)
    commit_sha = _run(repo, ["rev-parse", "HEAD"])
    pending = state["pending_publication"]
    assert isinstance(pending, dict)
    pending["commit_sha"] = commit_sha
    state_store.save(state)
    _run(repo, ["push", config.git.remote, f"HEAD:{config.git.branch}"])
    return PublicationCommit(commit_sha, components, message)


def retry_pending(
    config: Config, state_store: StateStore, state: dict[str, object]
) -> PublicationCommit | None:
    pending = state.get("pending_publication")
    if not isinstance(pending, dict):
        return None
    repo = config.paths.repo_root
    fetch(config)
    head = _run(repo, ["rev-parse", "HEAD"])
    remote = _run(repo, ["rev-parse", f"{config.git.remote}/{config.git.branch}"])
    commit_sha = pending.get("commit_sha")
    base_sha = pending.get("base_sha")
    tree_sha = pending.get("tree_sha")
    message = pending.get("message")
    if not all(isinstance(item, str) for item in (base_sha, tree_sha, message)):
        raise GitSafetyError("pending publication receipt is incomplete")
    if isinstance(commit_sha, str):
        if head != commit_sha:
            raise GitSafetyError("pending publication does not match local HEAD")
        actual_tree = _run(repo, ["show", "-s", "--format=%T", head])
        actual_parent = _run(repo, ["show", "-s", "--format=%P", head])
        if actual_tree != tree_sha or actual_parent != base_sha:
            raise GitSafetyError("pending commit identity does not match its bound base and tree")
        if _run(repo, ["status", "--porcelain=v1"]):
            raise GitSafetyError("pending publication retry requires a clean worktree and index")
        if remote == commit_sha:
            pass
        elif remote == base_sha:
            _run(repo, ["push", config.git.remote, f"HEAD:{config.git.branch}"])
        else:
            raise GitSafetyError("pending publication overlaps unknown remote history")
    else:
        if head != base_sha or remote != base_sha:
            raise GitSafetyError("pre-commit publication overlaps unknown local or remote history")
        if _run(repo, ["write-tree"]) != tree_sha:
            raise GitSafetyError("pending publication index no longer matches its bound tree")
        status = _run(repo, ["status", "--porcelain=v1", "--no-renames"])
        if any(line.startswith("??") or (len(line) >= 2 and line[1] != " ") for line in status.splitlines()):
            raise GitSafetyError("pending publication has new untracked or unstaged changes")
        _run(repo, ["commit", "--file=-"], input_text=message)
        commit_sha = _run(repo, ["rev-parse", "HEAD"])
        pending["commit_sha"] = commit_sha
        state_store.save(state)
        _run(repo, ["push", config.git.remote, f"HEAD:{config.git.branch}"])
    components = tuple(
        ComponentChange(item["name"], item["action"])
        for item in pending.get("components", [])
        if isinstance(item, dict) and isinstance(item.get("name"), str) and isinstance(item.get("action"), str)
    )
    assert isinstance(commit_sha, str)
    return PublicationCommit(commit_sha, components, message)


def consumer_fast_forward(config: Config) -> tuple[bool, str]:
    repo = config.paths.repo_root
    if _run(repo, ["status", "--porcelain=v1"]):
        raise GitSafetyError("consumer refuses a dirty worktree or index")
    fetch(config)
    status = repository_status(config)
    if status["ahead"]:
        raise GitSafetyError("consumer repository is ahead or diverged")
    if not status["behind"]:
        return False, str(status["head"])
    _run(repo, ["merge", "--ff-only", f"{config.git.remote}/{config.git.branch}"])
    return True, _run(repo, ["rev-parse", "HEAD"])
