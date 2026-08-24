"""One canonical managed-source, manifest, and exclusion contract."""

from __future__ import annotations

import hashlib
import json
import os
import unicodedata
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from .errors import ValidationError

IGNORED_NAME = ".DS_Store"
SYSTEM_SKILL = ".system"


@dataclass(frozen=True, order=True)
class ManifestEntry:
    path: str
    kind: str
    sha256: str | None = None
    size: int | None = None
    executable: bool | None = None

    def record(self) -> dict[str, object]:
        value: dict[str, object] = {"kind": self.kind, "path": self.path}
        if self.sha256 is not None:
            value["sha256"] = self.sha256
            value["size"] = self.size
            value["executable"] = self.executable
        return value


@dataclass(frozen=True)
class ManagedManifest:
    entries: tuple[ManifestEntry, ...]

    @property
    def fingerprint(self) -> str:
        encoded = json.dumps(
            [entry.record() for entry in self.entries],
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()

    @property
    def skills(self) -> tuple[str, ...]:
        names = {
            PurePosixPath(entry.path).parts[1]
            for entry in self.entries
            if len(PurePosixPath(entry.path).parts) >= 2
            and PurePosixPath(entry.path).parts[0] == "skills"
        }
        return tuple(sorted(names))

    def by_path(self) -> dict[str, ManifestEntry]:
        return {entry.path: entry for entry in self.entries}


def _file_digest(path: Path) -> tuple[str, int, bool]:
    result = hashlib.sha256()
    size = 0
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            size += len(chunk)
            result.update(chunk)
    executable = bool(path.stat().st_mode & 0o111)
    return result.hexdigest(), size, executable


def _validate_name(name: str, *, top_level_skill: bool = False) -> None:
    if (
        name in {"", ".", ".."}
        or "/" in name
        or any(unicodedata.category(character).startswith("C") for character in name)
    ):
        raise ValidationError(f"unsafe managed name: {name!r}")
    if top_level_skill and name.startswith("."):
        raise ValidationError(f"hidden top-level skill is unsupported: {name!r}")


def _walk(root: Path, *, prefix: PurePosixPath) -> list[ManifestEntry]:
    entries: list[ManifestEntry] = []
    case_map: dict[str, str] = {}
    stack: list[tuple[Path, PurePosixPath]] = [(root, prefix)]
    while stack:
        physical, logical = stack.pop()
        logical_text = logical.as_posix()
        folded = logical_text.casefold()
        previous = case_map.get(folded)
        if previous is not None and previous != logical_text:
            raise ValidationError(f"case-colliding managed paths: {previous!r}, {logical_text!r}")
        case_map[folded] = logical_text
        if physical.is_symlink():
            raise ValidationError(f"managed symlinks are unsupported: {logical_text}")
        if physical.is_dir():
            entries.append(ManifestEntry(logical_text, "directory"))
            children: list[tuple[Path, PurePosixPath]] = []
            try:
                iterator = os.scandir(physical)
            except OSError as exc:
                raise ValidationError(f"cannot read managed directory {logical_text}: {exc}") from exc
            with iterator:
                for child in iterator:
                    if child.name == IGNORED_NAME:
                        continue
                    _validate_name(child.name)
                    children.append((Path(child.path), logical / child.name))
            stack.extend(sorted(children, key=lambda pair: pair[1].as_posix(), reverse=True))
        elif physical.is_file():
            digest, size, executable = _file_digest(physical)
            entries.append(ManifestEntry(logical_text, "file", digest, size, executable))
        else:
            raise ValidationError(f"unsupported managed filesystem entry: {logical_text}")
    return entries


def source_manifest(codex_root: Path) -> ManagedManifest:
    if not codex_root.is_dir():
        raise ValidationError(f"authoritative Codex root is unavailable: {codex_root}")
    skills_root = codex_root / "skills"
    if not skills_root.is_dir() or skills_root.is_symlink():
        raise ValidationError(f"authoritative skills root is unavailable: {skills_root}")
    entries: list[ManifestEntry] = [ManifestEntry("skills", "directory")]
    agents = codex_root / "AGENTS.md"
    if agents.exists():
        if agents.is_symlink() or not agents.is_file():
            raise ValidationError("authoritative AGENTS.md must be a regular file")
        digest, size, executable = _file_digest(agents)
        entries.append(ManifestEntry("AGENTS.md", "file", digest, size, executable))
    try:
        children = list(os.scandir(skills_root))
    except OSError as exc:
        raise ValidationError(f"cannot read authoritative skills root: {exc}") from exc
    top_level_names: dict[str, str] = {}
    for child in sorted(children, key=lambda item: item.name):
        if child.name in {SYSTEM_SKILL, IGNORED_NAME}:
            continue
        _validate_name(child.name, top_level_skill=True)
        previous = top_level_names.get(child.name.casefold())
        if previous is not None and previous != child.name:
            raise ValidationError(f"case-colliding top-level skills: {previous!r}, {child.name!r}")
        top_level_names[child.name.casefold()] = child.name
        path = Path(child.path)
        if path.is_symlink() or not path.is_dir():
            raise ValidationError(f"top-level user skill must be a directory: {child.name}")
        entries.extend(_walk(path, prefix=PurePosixPath("skills") / child.name))
    return ManagedManifest(tuple(sorted(entries)))


def snapshot_manifest(root: Path) -> ManagedManifest:
    if not root.is_dir() or root.is_symlink():
        raise ValidationError(f"managed snapshot root is unavailable: {root}")
    allowed = {"AGENTS.md", "skills", IGNORED_NAME}
    unexpected = sorted(item.name for item in os.scandir(root) if item.name not in allowed)
    if unexpected:
        raise ValidationError(f"unexpected managed snapshot entries: {', '.join(unexpected)}")
    entries: list[ManifestEntry] = []
    agents = root / "AGENTS.md"
    if agents.exists():
        if agents.is_symlink() or not agents.is_file():
            raise ValidationError("snapshot AGENTS.md must be a regular file")
        digest, size, executable = _file_digest(agents)
        entries.append(ManifestEntry("AGENTS.md", "file", digest, size, executable))
    skills = root / "skills"
    if not skills.is_dir() or skills.is_symlink():
        raise ValidationError("snapshot skills/ must exist as a directory")
    top_level_names: dict[str, str] = {}
    for child in sorted(os.scandir(skills), key=lambda item: item.name):
        if child.name == IGNORED_NAME:
            continue
        if child.name == SYSTEM_SKILL:
            raise ValidationError("snapshot contains forbidden skills/.system")
        _validate_name(child.name, top_level_skill=True)
        previous = top_level_names.get(child.name.casefold())
        if previous is not None and previous != child.name:
            raise ValidationError(f"case-colliding snapshot skills: {previous!r}, {child.name!r}")
        top_level_names[child.name.casefold()] = child.name
        path = Path(child.path)
        if path.is_symlink() or not path.is_dir():
            raise ValidationError(f"snapshot skill must be a directory: {child.name}")
        entries.extend(_walk(path, prefix=PurePosixPath("skills") / child.name))
    entries.append(ManifestEntry("skills", "directory"))
    return ManagedManifest(tuple(sorted(entries)))


def manifests_equal(left: ManagedManifest, right: ManagedManifest) -> bool:
    return left.entries == right.entries
