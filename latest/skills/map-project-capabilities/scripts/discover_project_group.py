#!/usr/bin/env python3
"""Resolve project groups and produce a content-free folder/loose-item census."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import stat
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

SCRIPT_SUFFIXES = (
    ".py",
    ".sh",
    ".zsh",
    ".bash",
    ".fish",
    ".js",
    ".mjs",
    ".cjs",
    ".ts",
    ".rb",
    ".pl",
    ".ps1",
    ".command",
    ".user.js",
)

DOCUMENT_DATA_SUFFIXES = (
    ".md",
    ".markdown",
    ".txt",
    ".rst",
    ".csv",
    ".tsv",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".xml",
    ".log",
    ".pdf",
)

ARCHIVE_SUFFIXES = (
    ".zip",
    ".tar",
    ".tar.gz",
    ".tgz",
    ".gz",
    ".bz2",
    ".xz",
    ".7z",
    ".rar",
    ".dmg",
)

SYSTEM_METADATA_NAMES = {".ds_store", "thumbs.db", "desktop.ini"}

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


def folder_record(path: Path, classification: str) -> dict[str, str]:
    return {
        "name": path.name,
        "path": str(path.absolute()),
        "classification": classification,
    }


def unavailable_record(name: str, path: Path, reason: str) -> dict[str, str]:
    return {"name": name, "path": str(path.absolute()), "reason": reason}


def has_suffix(name: str, suffixes: Iterable[str]) -> bool:
    lowered = name.casefold()
    return any(lowered.endswith(suffix) for suffix in suffixes)


def loose_item_record(path: Path, sensitive_index: int) -> dict[str, str | None]:
    if SENSITIVE_NAME_PATTERN.search(path.name):
        return {
            "name": f"[sensitive-name-redacted-{sensitive_index}]",
            "path": None,
            "classification": "sensitive-name-redacted",
            "reason": "loose-item-name-redacted",
        }

    lowered = path.name.casefold()
    mode = path.stat().st_mode
    is_executable = bool(mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
    if lowered in SYSTEM_METADATA_NAMES:
        classification = "system-metadata"
    elif has_suffix(lowered, ARCHIVE_SUFFIXES):
        classification = "archive"
    elif has_suffix(lowered, SCRIPT_SUFFIXES) or is_executable:
        classification = "standalone-script-or-executable"
    elif has_suffix(lowered, DOCUMENT_DATA_SUFFIXES):
        classification = "document-or-data"
    else:
        classification = "other-loose-file"

    return {
        "name": path.name,
        "path": str(path.absolute()),
        "classification": classification,
        "reason": "outside-default-folder-audit",
    }


def enumerate_census(root: Path, allowlist: Iterable[str]) -> dict[str, object]:
    requested = validate_allowlist(allowlist)
    recognised: list[dict[str, str]] = []
    unclassified: list[dict[str, str]] = []
    loose_items: list[dict[str, str | None]] = []
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
                if SENSITIVE_NAME_PATTERN.search(child.name):
                    sensitive_index += 1
                loose_items.append(loose_item_record(child, sensitive_index))
                continue
            if not os.access(child, os.R_OK | os.X_OK):
                unavailable.append(unavailable_record(child.name, child, "directory-not-readable"))
                continue
            if has_git_marker(child):
                record = folder_record(child, "recognised-git-project-folder")
                recognised.append(record)
            elif has_project_marker(child):
                record = folder_record(child, "recognised-marker-project-folder")
                recognised.append(record)
            else:
                record = folder_record(child, "unclassified-project-folder-candidate")
                unclassified.append(record)
            selectable[child.name] = record
        except OSError as exc:
            unavailable.append(unavailable_record(child.name, child, f"entry-unavailable: {exc.__class__.__name__}"))

    observed_unavailable_count = len(unavailable)
    requested_unavailable_count = 0
    all_folder_candidates = [*recognised, *unclassified]

    if requested:
        proposed: list[dict[str, str]] = []
        for name in requested:
            record = selectable.get(name)
            if record is None:
                unavailable.append(unavailable_record(name, root / name, "requested-entry-not-selectable"))
                requested_unavailable_count += 1
            else:
                proposed.append(record)
        selected_names = {record["name"] for record in proposed}
        not_selected = [record for record in all_folder_candidates if record["name"] not in selected_names]
        selection_basis = "explicit-allowlist"
    else:
        proposed = list(all_folder_candidates)
        not_selected = []
        selection_basis = "inclusive-default-all-readable-folders"

    loose_counts: dict[str, int] = {}
    for record in loose_items:
        classification = str(record["classification"])
        loose_counts[classification] = loose_counts.get(classification, 0) + 1

    return {
        "confirmed_root": str(root),
        "recognised_project_folders": recognised,
        "unclassified_project_folder_candidates": unclassified,
        "loose_items": loose_items,
        "excluded_symlinks": excluded_symlinks,
        "unavailable_paths": unavailable,
        "proposed_folder_inspection": proposed,
        "not_selected_folders": not_selected,
        "selection_basis": selection_basis,
        "inspection_confirmation_required": True,
        "loose_item_review_requires_separate_approval": bool(loose_items),
        "symlinks_followed": False,
        "census_counts": {
            "recognised_project_folders": len(recognised),
            "unclassified_project_folder_candidates": len(unclassified),
            "total_folder_candidates": len(all_folder_candidates),
            "proposed_folder_inspection": len(proposed),
            "not_selected_folders": len(not_selected),
            "loose_items": len(loose_items),
            "loose_item_classes": loose_counts,
            "excluded_symlinks": len(excluded_symlinks),
            "unavailable_paths": len(unavailable),
            "observed_unavailable_paths": observed_unavailable_count,
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
    folders: list[dict[str, str]] = []
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
            classification = "recognised-git-project-folder"
        elif has_project_marker(path):
            classification = "recognised-marker-project-folder"
        else:
            classification = "unclassified-project-folder-candidate"
        folders.append(folder_record(path, classification))
    emit(
        {
            "operation": "resolve-paths",
            "folder_candidates": folders,
            "proposed_folder_inspection": folders,
            "not_selected_folders": [],
            "unavailable_paths": unavailable,
            "selection_basis": "explicit-paths",
            "inspection_confirmation_required": True,
            "loose_item_review_requires_separate_approval": False,
            "symlinks_followed": False,
        }
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Resolve bounded project scopes and census folders and loose items without reading contents."
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
        "enumerate", help="Census every immediate folder and loose item under a confirmed safe root."
    )
    enumerate_parser.add_argument("--root", required=True, help="Already confirmed project-group root.")
    enumerate_parser.add_argument(
        "--allow",
        action="append",
        default=[],
        help="Immediate folder name to propose; repeat as needed. Without this, all folders are proposed.",
    )
    enumerate_parser.add_argument(
        "--include-markers",
        action="store_true",
        help="Compatibility flag; conservative project markers are always recognised.",
    )
    enumerate_parser.set_defaults(handler=command_enumerate)

    resolve = subparsers.add_parser(
        "resolve-paths", help="Resolve exact approved project-folder paths in one or several locations."
    )
    resolve.add_argument("path", nargs="+", help="One or more exact project-folder paths.")
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
