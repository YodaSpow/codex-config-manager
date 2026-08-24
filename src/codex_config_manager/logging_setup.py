"""Metadata-only rotating operational logging."""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def configure_logging(root: Path, role: str) -> logging.Logger:
    root.mkdir(parents=True, exist_ok=True, mode=0o700)
    logger = logging.getLogger(f"codex_config_manager.{role}")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    handler = RotatingFileHandler(
        root / f"{role}.log", maxBytes=2 * 1024 * 1024, backupCount=5, encoding="utf-8"
    )
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger.addHandler(handler)
    logger.propagate = False
    return logger
