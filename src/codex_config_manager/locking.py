"""Single-instance execution locks."""

from __future__ import annotations

import fcntl
import os
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from .errors import ValidationError


@contextmanager
def execution_lock(root: Path, name: str) -> Iterator[None]:
    if not name.replace("-", "").isalnum():
        raise ValidationError("lock name is malformed")
    root.mkdir(parents=True, exist_ok=True, mode=0o700)
    path = root / f"{name}.lock"
    descriptor = os.open(path, os.O_CREAT | os.O_RDWR, 0o600)
    try:
        try:
            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise ValidationError(f"another {name} process is already running") from exc
        os.ftruncate(descriptor, 0)
        os.write(descriptor, f"{os.getpid()}\n".encode())
        yield
    finally:
        fcntl.flock(descriptor, fcntl.LOCK_UN)
        os.close(descriptor)
