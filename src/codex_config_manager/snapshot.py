"""Private candidate creation and canonical snapshot reconciliation."""

from __future__ import annotations

import shutil
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from .errors import ValidationError
from .managed_scope import ManagedManifest, manifests_equal, snapshot_manifest, source_manifest
from .rsync import sync_file, sync_tree


@contextmanager
def private_candidate(codex_root: Path, rsync_binary: Path) -> Iterator[tuple[Path, ManagedManifest]]:
    with tempfile.TemporaryDirectory(prefix="codex-config-manager-candidate-") as directory:
        candidate = Path(directory) / "latest"
        (candidate / "skills").mkdir(parents=True)
        before = source_manifest(codex_root)
        sync_tree(
            rsync_binary,
            codex_root / "skills",
            candidate / "skills",
            dry_run=False,
            exclude_system=True,
        )
        agents = codex_root / "AGENTS.md"
        if agents.exists():
            sync_file(rsync_binary, agents, candidate, dry_run=False)
        candidate_manifest = snapshot_manifest(candidate)
        after = source_manifest(codex_root)
        if not manifests_equal(before, after):
            raise ValidationError("authoritative managed source changed during candidate ingestion")
        if not manifests_equal(before, candidate_manifest):
            raise ValidationError("private candidate is not equivalent to authoritative managed source")
        yield candidate, candidate_manifest


def reconcile_latest(candidate: Path, latest: Path, rsync_binary: Path) -> bool:
    if latest.exists():
        snapshot_manifest(latest)
    dry = sync_tree(rsync_binary, candidate, latest, dry_run=True)
    if not dry.changed:
        return False
    sync_tree(rsync_binary, candidate, latest, dry_run=False)
    if sync_tree(rsync_binary, candidate, latest, dry_run=True).changed:
        raise ValidationError("latest/ is not equivalent after reconciliation")
    if not manifests_equal(snapshot_manifest(candidate), snapshot_manifest(latest)):
        raise ValidationError("latest/ manifest differs from private candidate")
    return True
