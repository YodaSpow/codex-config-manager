#!/usr/bin/env python3
"""Deterministic Scratchboard behavioural checks in an isolated temporary repo."""

from __future__ import annotations

import json
import fcntl
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from urllib.request import urlopen


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "scratchboard.py"


def run(*args: str) -> str:
    return subprocess.check_output([sys.executable, str(SCRIPT), *args], text=True)


def main() -> None:
    with tempfile.TemporaryDirectory() as temp:
        repo = Path(temp); (repo / "Docs").mkdir()
        first = json.loads(run("update", "--repo", str(repo), "--content", "first", "--date", "2026-09-02"))
        second = json.loads(run("update", "--repo", str(repo), "--content", "<script>alert(1)</script>\n\n[bad](javascript:alert(1))", "--date", "2026-09-02"))
        run("update", "--repo", str(repo), "--content", "```python\nprint('safe')\n```", "--date", "2026-09-02")
        run("update", "--repo", str(repo), "--content", "Confirmed", "--kind", "signal", "--date", "2026-09-02")
        run("update", "--repo", str(repo), "--content", "Needs attention", "--kind", "callout", "--date", "2026-09-02")
        run("update", "--repo", str(repo), "--content", "input -> output", "--kind", "diagram", "--date", "2026-09-02")
        run("update", "--repo", str(repo), "--content", "Safe SVG concept", "--kind", "svg", "--date", "2026-09-02")
        root = repo / "Docs" / "scratchboard"; day = json.loads((root / "state" / "2026-09-02.json").read_text())
        assert len(day["blocks"]) == 7 and day["state"] == "active"
        page = (root / "sessions" / "2026-09-02.html").read_text()
        assert "&lt;script&gt;alert(1)&lt;/script&gt;" in page and 'href="javascript:' not in page and "data-copy=" in page and "class=\"shiki " in page
        assert "class=\"signal\"" in page and "class=\"callout\"" in page and 'role="img"' in page
        assert first["url"].split("?")[0] == second["url"].split("?")[0]
        with (root / "state" / ".write.lock").open("a+") as lock:
            fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
            blocked = subprocess.run([sys.executable, str(SCRIPT), "update", "--repo", str(repo), "--content", "blocked", "--date", "2026-09-02"], text=True, capture_output=True)
            fcntl.flock(lock.fileno(), fcntl.LOCK_UN)
        assert blocked.returncode != 0 and "Another agent is updating" in blocked.stderr
        run("update", "--repo", str(repo), "--content", "next day", "--date", "2026-09-03")
        assert json.loads((root / "state" / "2026-09-02.json").read_text())["state"] == "frozen"
        run("redirect", "--repo", str(repo), "--old-path", "sessions/old.html", "--target", "sessions/2026-09-03.html")
        redirect = (root / "sessions" / "old.html").read_text(); assert "location.replace" in redirect
        run("close", "--repo", str(repo))
        server = json.loads(run("serve", "--repo", str(repo), "--idle-seconds", "1"));
        with urlopen(server["url"] + "index.html") as response:
            assert response.headers["Cache-Control"] == "no-store, no-cache, must-revalidate, max-age=0"
            assert response.headers["Pragma"] == "no-cache" and response.headers["Expires"] == "0"
        time.sleep(1.4)
        restarted = json.loads(run("serve", "--repo", str(repo), "--idle-seconds", "1")); assert restarted["server"] == "started"
        run("close", "--repo", str(repo))
    print("Scratchboard behavioural validation passed")


if __name__ == "__main__":
    main()
