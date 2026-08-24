"""Deterministic model-derived machine identity."""

from __future__ import annotations

import json
import subprocess

from .errors import IdentityError

SYSTEM_PROFILER = "/usr/sbin/system_profiler"


def normalize_model_name(value: object) -> str:
    if not isinstance(value, str):
        raise IdentityError("native Model Name must be text")
    words = value.split()
    if not words:
        raise IdentityError("native Model Name is empty")
    identity = words[0] + "".join(word[:1].upper() + word[1:] for word in words[1:])
    if not identity or any(not (character.isalnum() or character in "_-") for character in identity):
        raise IdentityError("derived machine identity is malformed")
    return identity


def native_model_name() -> str:
    try:
        result = subprocess.run(
            [SYSTEM_PROFILER, "SPHardwareDataType", "-json"],
            check=True,
            capture_output=True,
            text=True,
            timeout=30,
        )
        payload = json.loads(result.stdout)
        records = payload.get("SPHardwareDataType")
        value = records[0].get("machine_name") if isinstance(records, list) and records else None
    except (OSError, ValueError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        raise IdentityError(f"unable to read native Model Name: {exc}") from exc
    if not isinstance(value, str) or not value.strip():
        raise IdentityError("structured system_profiler output did not contain Model Name")
    return value


def detected_machine_id() -> str:
    return normalize_model_name(native_model_name())


def require_identity(configured: str, *, detected: str | None = None) -> str:
    actual = detected if detected is not None else detected_machine_id()
    if configured != actual:
        raise IdentityError(
            f"machine identity mismatch: configured={configured!r}, detected={actual!r}"
        )
    return actual
