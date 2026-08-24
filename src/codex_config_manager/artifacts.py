"""Deterministic portable ZIP artifacts and bounded README projection."""

from __future__ import annotations

import hashlib
import os
import zipfile
from pathlib import Path, PurePosixPath

from .errors import ValidationError
from .managed_scope import IGNORED_NAME, snapshot_manifest

PACKAGING_CONTRACT_VERSION = 1
ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
MAX_FILES = 10_000
MAX_MEMBER_BYTES = 50 * 1024 * 1024
MAX_TOTAL_BYTES = 250 * 1024 * 1024
MAX_COMPRESSION_RATIO = 1000
BEGIN_MARKER = "<!-- BEGIN CODEX CONFIG MANAGER DOWNLOADS -->"
END_MARKER = "<!-- END CODEX CONFIG MANAGER DOWNLOADS -->"


def _zip_info(name: str, *, directory: bool, executable: bool = False) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(name + ("/" if directory and not name.endswith("/") else ""), ZIP_TIMESTAMP)
    info.create_system = 3
    mode = 0o40755 if directory else 0o100755 if executable else 0o100644
    info.external_attr = mode << 16
    info.compress_type = zipfile.ZIP_DEFLATED
    return info


def _members(root: Path, wrapper: str | None) -> list[tuple[Path, str, bool, bool]]:
    result: list[tuple[Path, str, bool, bool]] = []
    total = 0
    for physical in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()):
        if physical.name == IGNORED_NAME:
            continue
        if physical.is_symlink():
            raise ValidationError(f"portable artifacts do not support symlinks: {physical}")
        relative = physical.relative_to(root).as_posix()
        archive_name = f"{wrapper}/{relative}" if wrapper else relative
        if physical.is_dir():
            result.append((physical, archive_name, True, False))
        elif physical.is_file():
            size = physical.stat().st_size
            if size > MAX_MEMBER_BYTES:
                raise ValidationError(f"artifact member exceeds size limit: {relative}")
            total += size
            result.append((physical, archive_name, False, bool(physical.stat().st_mode & 0o111)))
        else:
            raise ValidationError(f"unsupported artifact entry: {relative}")
    if wrapper:
        result.insert(0, (root, wrapper, True, False))
    file_count = sum(not directory for _, _, directory, _ in result)
    if file_count > MAX_FILES or total > MAX_TOTAL_BYTES:
        raise ValidationError("artifact exceeds file-count or total-size limit")
    return result


def build_zip(source: Path, target: Path, *, wrapper: str | None) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(
        target,
        "w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
        strict_timestamps=True,
    ) as archive:
        for physical, name, directory, executable in _members(source, wrapper):
            info = _zip_info(name, directory=directory, executable=executable)
            archive.writestr(info, b"" if directory else physical.read_bytes())


def build_distribution(latest: Path, target: Path) -> tuple[str, ...]:
    manifest = snapshot_manifest(latest)
    target.mkdir(parents=True, exist_ok=True)
    skills_target = target / "skills"
    skills_target.mkdir(parents=True, exist_ok=True)
    agents = latest / "AGENTS.md"
    if agents.exists():
        with zipfile.ZipFile(
            target / "global-agents.zip",
            "w",
            compression=zipfile.ZIP_DEFLATED,
            compresslevel=9,
            strict_timestamps=True,
        ) as archive:
            archive.writestr(
                _zip_info(
                    "AGENTS.md",
                    directory=False,
                    executable=bool(agents.stat().st_mode & 0o111),
                ),
                agents.read_bytes(),
            )
    for name in manifest.skills:
        build_zip(latest / "skills" / name, skills_target / f"{name}.zip", wrapper=name)
    return manifest.skills


def _safe_member(name: str) -> PurePosixPath:
    path = PurePosixPath(name)
    if path.is_absolute() or ".." in path.parts or any(part in {"", "."} for part in path.parts):
        raise ValidationError(f"unsafe archive member: {name!r}")
    if any(part == "__MACOSX" or part.startswith("._") or part == IGNORED_NAME for part in path.parts):
        raise ValidationError(f"excluded archive member: {name!r}")
    return path


def validate_zip(path: Path, *, expected_root: Path, wrapper: str | None) -> None:
    seen: set[str] = set()
    folded: dict[str, str] = {}
    total = 0
    files = 0
    with zipfile.ZipFile(path) as archive:
        for info in archive.infolist():
            member = _safe_member(info.filename.rstrip("/"))
            text = member.as_posix()
            if text in seen:
                raise ValidationError(f"duplicate archive member: {text}")
            seen.add(text)
            previous = folded.get(text.casefold())
            if previous is not None and previous != text:
                raise ValidationError(f"case-colliding archive members: {previous}, {text}")
            folded[text.casefold()] = text
            if info.file_size > MAX_MEMBER_BYTES:
                raise ValidationError(f"archive member exceeds size limit: {text}")
            if info.compress_size and info.file_size / info.compress_size > MAX_COMPRESSION_RATIO:
                raise ValidationError(f"archive member exceeds compression ratio: {text}")
            if not info.is_dir():
                files += 1
                total += info.file_size
                relative = PurePosixPath(*member.parts[1:]) if wrapper else member
                if wrapper and (not member.parts or member.parts[0] != wrapper):
                    raise ValidationError("skill archive wrapper mismatch")
                source = expected_root.joinpath(*relative.parts)
                if not source.is_file() or archive.read(info) != source.read_bytes():
                    raise ValidationError(f"archive content mismatch: {text}")
                archived_executable = bool((info.external_attr >> 16) & 0o111)
                source_executable = bool(source.stat().st_mode & 0o111)
                if archived_executable != source_executable:
                    raise ValidationError(f"archive executable mode mismatch: {text}")
        if files > MAX_FILES or total > MAX_TOTAL_BYTES:
            raise ValidationError("archive exceeds aggregate limits")


def validate_distribution(latest: Path, target: Path) -> tuple[str, ...]:
    manifest = snapshot_manifest(latest)
    expected = {f"{name}.zip" for name in manifest.skills}
    skills_root = target / "skills"
    actual = {item.name for item in skills_root.iterdir()} if skills_root.is_dir() else set()
    if actual != expected:
        raise ValidationError(f"skill artifact membership mismatch: expected={expected}, actual={actual}")
    agents_zip = target / "global-agents.zip"
    if (latest / "AGENTS.md").exists() != agents_zip.exists():
        raise ValidationError("global AGENTS.md artifact membership mismatch")
    if agents_zip.exists():
        validate_zip(agents_zip, expected_root=latest, wrapper=None)
        with zipfile.ZipFile(agents_zip) as archive:
            if [item.filename for item in archive.infolist()] != ["AGENTS.md"]:
                raise ValidationError("global-agents.zip must contain only root AGENTS.md")
    for name in manifest.skills:
        validate_zip(skills_root / f"{name}.zip", expected_root=latest / "skills" / name, wrapper=name)
    return manifest.skills


def render_download_section(has_agents: bool, skills: tuple[str, ...]) -> str:
    lines = [BEGIN_MARKER]
    if has_agents:
        lines.extend(
            [
                "## Global AGENTS.md",
                "",
                "The global `AGENTS.md` contains guidance intended for the user’s global Codex environment.",
                "",
                "- [View the current global - AGENTS.md](latest/AGENTS.md)",
                "- [Download the current global - AGENTS.md](upload-ready/global-agents.zip)",
                "",
            ]
        )
    lines.extend(["## Skills", "", "Each download contains one complete user-managed skill.", ""])
    lines.extend(f"- [Download {name}](upload-ready/skills/{name}.zip)" for name in skills)
    lines.extend([END_MARKER, ""])
    return "\n".join(lines)


def reconcile_readme(original: str, *, has_agents: bool, skills: tuple[str, ...]) -> str:
    section = render_download_section(has_agents, skills)
    begin_count = original.count(BEGIN_MARKER)
    end_count = original.count(END_MARKER)
    if begin_count != end_count or begin_count > 1:
        raise ValidationError("README managed-section markers are malformed")
    if begin_count == 0:
        return original.rstrip() + "\n\n" + section
    before, remainder = original.split(BEGIN_MARKER, 1)
    _, after = remainder.split(END_MARKER, 1)
    return before.rstrip() + "\n\n" + section + after.lstrip("\n")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
