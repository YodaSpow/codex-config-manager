"""Canonical repository and mutation-boundary path helpers."""

from __future__ import annotations

from pathlib import Path

from .errors import PathSafetyError


def canonical(path: str | Path) -> Path:
    return Path(path).expanduser().resolve(strict=False)


def require_absolute_directory(path: str | Path, *, label: str, exists: bool = True) -> Path:
    raw = Path(path).expanduser()
    if not raw.is_absolute():
        raise PathSafetyError(f"{label} must be absolute")
    resolved = raw.resolve(strict=False)
    if resolved == Path("/") or resolved == Path.home().resolve():
        raise PathSafetyError(f"{label} cannot be a broad system or home root")
    if exists and not resolved.is_dir():
        raise PathSafetyError(f"{label} is not an existing directory: {resolved}")
    return resolved


def require_within(path: str | Path, parent: str | Path, *, label: str) -> Path:
    child = canonical(path)
    boundary = canonical(parent)
    if child == boundary:
        raise PathSafetyError(f"{label} must be below, not equal to, {boundary}")
    try:
        child.relative_to(boundary)
    except ValueError as exc:
        raise PathSafetyError(f"{label} escapes {boundary}: {child}") from exc
    return child


def reject_overlap(source: str | Path, destination: str | Path) -> None:
    src = canonical(source)
    dst = canonical(destination)
    if src == dst or src in dst.parents or dst in src.parents:
        raise PathSafetyError(f"source and destination overlap: {src} / {dst}")


def repository_paths(repo_root: Path) -> tuple[Path, Path, Path]:
    root = require_absolute_directory(repo_root, label="repository root")
    latest = require_within(root / "latest", root, label="latest root")
    uploads = require_within(root / "upload-ready", root, label="upload-ready root")
    runtime = require_within(root / ".runtime", root, label="runtime root")
    return latest, uploads, runtime
