"""Console entry points for runtime and operator commands."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Callable

from .config import Config, load_config
from .consumer import run_consumer
from .errors import CCMError
from .launchd import install, uninstall
from .publisher import run_publisher
from .validation import status, validate_runtime

DEFAULT_CONFIG = Path(__file__).resolve().parents[2] / "config" / "config.yaml"


def _parser(description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    return parser


def _execute(action: Callable[[], object]) -> int:
    try:
        result = action()
    except (CCMError, OSError, subprocess.SubprocessError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    if isinstance(result, (dict, list)):
        print(json.dumps(result, indent=2, sort_keys=True))
    elif result is not None:
        print(result)
    return 0


def _load(path: Path, role: str | None = None) -> Config:
    return load_config(path, invoked_role=role)


def publisher_main() -> int:
    args = _parser("Run one Mac Studio publisher observation.").parse_args()
    return _execute(lambda: run_publisher(_load(args.config, "publisher")))


def consumer_main() -> int:
    args = _parser("Run one Mac mini consumer update.").parse_args()
    return _execute(lambda: run_consumer(_load(args.config, "consumer")))


def install_main() -> int:
    args = _parser("Install the configured role's LaunchAgent.").parse_args()
    def action() -> str:
        config = _load(args.config)
        validate_runtime(config)
        return f"installed: {install(config)}"

    return _execute(action)


def uninstall_main() -> int:
    args = _parser("Uninstall only the configured role's LaunchAgent.").parse_args()
    return _execute(lambda: f"uninstalled: {uninstall(_load(args.config))}")


def status_main() -> int:
    args = _parser("Show read-only Codex Config Manager status.").parse_args()
    return _execute(lambda: status(_load(args.config)))


def validate_main() -> int:
    args = _parser("Run a non-mutating role-aware validation.").parse_args()
    return _execute(lambda: validate_runtime(_load(args.config)))


def bootstrap_main() -> int:
    parser = argparse.ArgumentParser(description="Run the explicit repository environment bootstrap.")
    parser.add_argument("--environment", choices=("runtime", "development"), default="development")
    parser.add_argument("--repair", action="store_true")
    args = parser.parse_args()
    script = Path(__file__).resolve().parents[2] / "scripts" / "bootstrap.py"
    command = [sys.executable, str(script), "--environment", args.environment]
    if args.repair:
        command.append("--repair")
    return subprocess.run(command, check=False).returncode
