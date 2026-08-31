#!/usr/bin/env python3
"""Resolve and enumerate project groups without reading or changing projects."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
from typing import Iterable


PROJECT_MARKERS = (
    "pyproject.toml",
    "package.json",
    "Cargo.toml",
    "go.mod",
    "pom.xml",
    "build.gradle",
    "build.gradle.kts",
)


class DiscoveryError(ValueError):
    """A path or scope cannot be resolved safely."""


def existing_directory(raw: str | os.PathLike[str]) -> Path:
    path = Path(raw).expanduser().resolve(strict=False)
    if not path.exists():
        raise DiscoveryError(f"Path does not exist: {path}")
    if not path.is_dir():
        raise DiscoveryError(f"Path is not a directory: {path}")
    if not os.access(path, os.R_OK | os.X_OK):
        raise DiscoveryError(f"Path is not readable: {path}")
    return path


def has_git_marker(path: Path) -> bool:
    marker = path / ".git"
    return marker.is_dir() or marker.is_file()


def has_project_marker(path: Path) -> bool:
    return any((path / marker).is_file() for marker in PROJECT_MARKERS)


def resolve_project_root(raw: str | os.PathLike[str]) -> tuple[Path, str]:
    start = existing_directory(raw)
    git_candidates: list[Path] = []
    marker_candidates: list[Path] = []
    for candidate in (start, *start.parents):
        if has_git_marker(candidate):
            git_candidates.append(candidate)
        if has_project_marker(candidate):
            marker_candidates.append(candidate)
    if git_candidates:
        return git_candidates[0], "version-control"
    if marker_candidates:
        return marker_candidates[0], "project-marker"
    raise DiscoveryError(f"Could not resolve a project root from: {start}")


def root_safety(path: Path) -> tuple[str, str | None]:
    resolved = path.resolve(strict=False)
    if resolved == Path(resolved.anchor):
        return "unsafe", "filesystem-or-drive-root"
    if resolved == Path.home().resolve(strict=False):
        return "unsafe", "user-home-directory"
    return "candidate", None


def validate_enumeration_root(raw: str | os.PathLike[str]) -> Path:
    root = existing_directory(raw)
    state, reason = root_safety(root)
    if state != "candidate":
        raise DiscoveryError(f"Unsafe automatic enumeration root ({reason}): {root}")
    return root


def candidate_kind(path: Path, include_markers: bool) -> str | None:
    if path.is_symlink() or not path.is_dir():
        return None
    if has_git_marker(path):
        return "git"
    if include_markers and has_project_marker(path):
        return "project-marker"
    return None


def enumerate_projects(
    root: Path, allowlist: Iterable[str], include_markers: bool
) -> tuple[list[dict[str, str]], list[str]]:
    requested = list(dict.fromkeys(allowlist))
    for name in requested:
        if not name or name in {".", ".."} or Path(name).name != name:
            raise DiscoveryError(f"Allowlist entries must be immediate child names: {name!r}")

    entries: dict[str, tuple[Path, str]] = {}
    try:
        children = sorted(root.iterdir(), key=lambda item: item.name.casefold())
    except OSError as exc:
        raise DiscoveryError(f"Cannot enumerate root: {root}: {exc}") from exc

    for child in children:
        kind = candidate_kind(child, include_markers)
        if kind:
            entries[child.name] = (child.resolve(strict=False), kind)

    unavailable: list[str] = []
    selected_names = requested or list(entries)
    projects: list[dict[str, str]] = []
    for name in selected_names:
        selected = entries.get(name)
        if selected is None:
            unavailable.append(str(root / name))
            continue
        path, kind = selected
        projects.append({"name": name, "path": str(path), "kind": kind})
    return projects, unavailable


def emit(payload: dict[str, object]) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True))


def command_suggest(args: argparse.Namespace) -> None:
    project, method = resolve_project_root(args.current)
    suggested = project.parent
    state, reason = root_safety(suggested)
    emit(
        {
            "operation": "suggest",
            "current_project": str(project),
            "resolution_method": method,
            "suggested_group_root": str(suggested),
            "root_safety_state": state,
            "root_safety_reason": reason,
            "candidate_projects": None,
            "confirmation_required_before_enumeration": True,
        }
    )


def command_validate_roots(args: argparse.Namespace) -> None:
    roots: list[dict[str, str | None]] = []
    unavailable: list[str] = []
    for raw in args.root:
        try:
            root = existing_directory(raw)
        except DiscoveryError:
            unavailable.append(str(Path(raw).expanduser().resolve(strict=False)))
            continue
        state, reason = root_safety(root)
        roots.append({"path": str(root), "root_safety_state": state, "reason": reason})
    emit({"operation": "validate-roots", "roots": roots, "unavailable_paths": unavailable})


def command_enumerate(args: argparse.Namespace) -> None:
    root = validate_enumeration_root(args.root)
    projects, unavailable = enumerate_projects(root, args.allow, args.include_markers)
    emit(
        {
            "operation": "enumerate",
            "confirmed_root": str(root),
            "candidate_projects": projects,
            "unavailable_paths": unavailable,
            "symlinks_followed": False,
        }
    )


def command_resolve_paths(args: argparse.Namespace) -> None:
    projects: list[dict[str, str]] = []
    unavailable: list[str] = []
    seen: set[Path] = set()
    for raw in args.path:
        try:
            path = existing_directory(raw)
        except DiscoveryError:
            unavailable.append(str(Path(raw).expanduser().resolve(strict=False)))
            continue
        if path in seen:
            continue
        seen.add(path)
        if has_git_marker(path):
            kind = "git"
        elif has_project_marker(path):
            kind = "project-marker"
        else:
            kind = "directory"
        projects.append({"name": path.name, "path": str(path), "kind": kind})
    emit({"operation": "resolve-paths", "projects": projects, "unavailable_paths": unavailable})


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Resolve bounded project scopes without reading project contents."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    suggest = subparsers.add_parser(
        "suggest", help="Resolve the current project and suggest one parent; never enumerate siblings."
    )
    suggest.add_argument(
        "--current", default=os.getcwd(), help="Starting directory (default: current working directory)."
    )
    suggest.set_defaults(handler=command_suggest)

    validate = subparsers.add_parser(
        "validate-roots", help="Validate one or more explicitly supplied roots without enumeration."
    )
    validate.add_argument(
        "--root", action="append", required=True, help="Root to validate; repeat for several roots."
    )
    validate.set_defaults(handler=command_validate_roots)

    enumerate_parser = subparsers.add_parser(
        "enumerate", help="Enumerate immediate project children of an already confirmed safe root."
    )
    enumerate_parser.add_argument("--root", required=True, help="Already confirmed project-group root.")
    enumerate_parser.add_argument(
        "--allow", action="append", default=[], help="Immediate child name to select; repeat as needed."
    )
    enumerate_parser.add_argument(
        "--include-markers", action="store_true", help="Include non-Git directories with conservative project markers."
    )
    enumerate_parser.set_defaults(handler=command_enumerate)

    resolve = subparsers.add_parser(
        "resolve-paths", help="Resolve exact approved project paths, including paths in several locations."
    )
    resolve.add_argument("path", nargs="+", help="One or more exact project directories.")
    resolve.set_defaults(handler=command_resolve_paths)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        args.handler(args)
    except DiscoveryError as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
