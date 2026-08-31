#!/usr/bin/env python3
"""Resolve project groups and produce a content-free immediate-child census."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
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

SENSITIVE_NAME_PATTERN = re.compile(
    r"(^\.env(?:\.|$)|token|secret|password|credential|cookie|\.pem$|\.key$)",
    re.IGNORECASE,
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


def validate_allowlist(allowlist: Iterable[str]) -> list[str]:
    requested = list(dict.fromkeys(allowlist))
    for name in requested:
        if not name or name in {".", ".."} or Path(name).name != name:
            raise DiscoveryError(f"Allowlist entries must be immediate child names: {name!r}")
    return requested


def project_record(path: Path, kind: str) -> dict[str, str]:
    return {"name": path.name, "path": str(path.absolute()), "kind": kind}


def unavailable_record(name: str, path: Path, reason: str) -> dict[str, str]:
    return {"name": name, "path": str(path.absolute()), "reason": reason}


def excluded_file_record(path: Path, sensitive_index: int) -> dict[str, str | None]:
    if SENSITIVE_NAME_PATTERN.search(path.name):
        return {
            "name": f"[sensitive-name-redacted-{sensitive_index}]",
            "path": None,
            "reason": "non-directory-sensitive-name-redacted",
        }
    return {"name": path.name, "path": str(path.absolute()), "reason": "non-directory"}


def enumerate_census(root: Path, allowlist: Iterable[str]) -> dict[str, object]:
    requested = validate_allowlist(allowlist)
    recognised: list[dict[str, str]] = []
    unclassified: list[dict[str, str]] = []
    excluded_files: list[dict[str, str | None]] = []
    excluded_symlinks: list[dict[str, str]] = []
    unavailable: list[dict[str, str]] = []
    selectable: dict[str, dict[str, str]] = {}
    sensitive_index = 0

    try:
        children = sorted(root.iterdir(), key=lambda item: item.name.casefold())
    except OSError as exc:
        raise DiscoveryError(f"Cannot enumerate root: {root}: {exc}") from exc

    for child in children:
        try:
            if child.is_symlink():
                excluded_symlinks.append(
                    {"name": child.name, "path": str(child.absolute()), "reason": "symlink-not-followed"}
                )
                continue
            if not child.is_dir():
                sensitive_index += 1
                excluded_files.append(excluded_file_record(child, sensitive_index))
                continue
            if not os.access(child, os.R_OK | os.X_OK):
                unavailable.append(unavailable_record(child.name, child, "directory-not-readable"))
                continue
            if has_git_marker(child):
                record = project_record(child, "git")
                recognised.append(record)
            elif has_project_marker(child):
                record = project_record(child, "project-marker")
                recognised.append(record)
            else:
                record = project_record(child, "unclassified-directory")
                unclassified.append(record)
            selectable[child.name] = record
        except OSError as exc:
            unavailable.append(unavailable_record(child.name, child, f"entry-unavailable: {exc.__class__.__name__}"))

    observed_unavailable_count = len(unavailable)
    requested_unavailable_count = 0
    selected: list[dict[str, str]] = []
    if requested:
        for name in requested:
            record = selectable.get(name)
            if record is None:
                unavailable.append(unavailable_record(name, root / name, "requested-entry-not-selectable"))
                requested_unavailable_count += 1
            else:
                selected.append(record)
    else:
        selected = list(recognised)

    return {
        "confirmed_root": str(root),
        "recognised_projects": recognised,
        "unclassified_directories": unclassified,
        "excluded_non_directories": excluded_files,
        "excluded_symlinks": excluded_symlinks,
        "unavailable_paths": unavailable,
        "selected_projects": selected,
        "inspection_confirmation_required": True,
        "symlinks_followed": False,
        "census_counts": {
            "recognised_projects": len(recognised),
            "unclassified_directories": len(unclassified),
            "excluded_non_directories": len(excluded_files),
            "excluded_symlinks": len(excluded_symlinks),
            "unavailable_paths": observed_unavailable_count,
            "requested_unavailable_paths": requested_unavailable_count,
            "immediate_entries_observed": len(children),
        },
    }


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
            "project_census": None,
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
    payload = enumerate_census(root, args.allow)
    payload["operation"] = "enumerate"
    emit(payload)


def command_resolve_paths(args: argparse.Namespace) -> None:
    projects: list[dict[str, str]] = []
    unavailable: list[dict[str, str]] = []
    seen: set[Path] = set()
    for raw in args.path:
        unresolved = Path(raw).expanduser().absolute()
        if unresolved.is_symlink():
            unavailable.append(unavailable_record(unresolved.name, unresolved, "symlink-not-followed"))
            continue
        try:
            path = existing_directory(raw)
        except DiscoveryError as exc:
            unavailable.append(unavailable_record(unresolved.name, unresolved, str(exc)))
            continue
        if path in seen:
            continue
        seen.add(path)
        if has_git_marker(path):
            kind = "git"
        elif has_project_marker(path):
            kind = "project-marker"
        else:
            kind = "unclassified-directory"
        projects.append(project_record(path, kind))
    emit(
        {
            "operation": "resolve-paths",
            "projects": projects,
            "unavailable_paths": unavailable,
            "inspection_confirmation_required": True,
            "symlinks_followed": False,
        }
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Resolve bounded project scopes and census entries without reading project contents."
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
        "enumerate", help="Census every immediate entry under an already confirmed safe root."
    )
    enumerate_parser.add_argument("--root", required=True, help="Already confirmed project-group root.")
    enumerate_parser.add_argument(
        "--allow",
        action="append",
        default=[],
        help="Immediate directory name to propose for inspection; repeat as needed. Census remains complete.",
    )
    enumerate_parser.add_argument(
        "--include-markers",
        action="store_true",
        help="Compatibility flag; conservative project markers are always recognised.",
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
