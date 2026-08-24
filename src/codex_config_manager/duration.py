"""Strict human-readable duration parsing."""

from __future__ import annotations

import re

from .errors import ConfigurationError

_DURATION = re.compile(r"^(?P<number>[1-9][0-9]*)(?P<unit>[smhd])$")
_MULTIPLIERS = {"s": 1, "m": 60, "h": 3600, "d": 86400}


def parse_duration(value: object, *, field: str, minimum: int, maximum: int) -> int:
    if not isinstance(value, str):
        raise ConfigurationError(f"{field} must be a duration string")
    match = _DURATION.fullmatch(value)
    if not match:
        raise ConfigurationError(
            f"{field} must be one positive whole number followed by s, m, h, or d"
        )
    seconds = int(match.group("number")) * _MULTIPLIERS[match.group("unit")]
    if not minimum <= seconds <= maximum:
        raise ConfigurationError(
            f"{field} must be between {minimum} and {maximum} seconds"
        )
    return seconds
