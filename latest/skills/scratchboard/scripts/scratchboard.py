#!/usr/bin/env python3
"""Repo-bound Scratchboard renderer and localhost interactive server."""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import html
import json
import os
import re
import signal
import socket
import subprocess
import sys
import tempfile
import time
import uuid
from datetime import UTC, datetime
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.request import urlopen
from zoneinfo import ZoneInfo

try:
    import fcntl
except ImportError:  # pragma: no cover - the supported environment is macOS/Linux
    fcntl = None


SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL_VERSION = "1.0"
LONDON = ZoneInfo("Europe/London")
NO_CACHE = "no-store, no-cache, must-revalidate, max-age=0"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def ui_build_id() -> str:
    inputs = ("assets/scratchboard.css", "assets/copy-code.js", "templates/index.html", "templates/date-board.html", "scripts/scratchboard.py", "scripts/highlight-code.mjs")
    source = b"".join((SKILL_ROOT / path).read_bytes() for path in inputs)
    return hashlib.sha256(source).hexdigest()[:12]


def docs_dir(repo: Path, create: bool) -> Path:
    for name in ("docs", "Docs"):
        candidate = repo / name
        if candidate.is_dir():
            return candidate
    if not create:
        raise RuntimeError("No existing docs/ or Docs/ directory. Re-run with --create-docs after approval.")
    candidate = repo / "docs"
    candidate.mkdir(parents=True, exist_ok=True)
    return candidate


def root_for(repo: Path, create_docs: bool) -> Path:
    root = docs_dir(repo, create_docs) / "scratchboard"
    (root / "sessions").mkdir(parents=True, exist_ok=True)
    (root / "state").mkdir(parents=True, exist_ok=True)
    return root


def state_path(root: Path, day: str) -> Path:
    return root / "state" / f"{day}.json"


def atomic_json(path: Path, value: object) -> None:
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        json.dump(value, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
        temp_name = handle.name
    os.replace(temp_name, path)


@contextlib.contextmanager
def write_lock(root: Path, timeout_seconds: float = 3.0):
    lock_path = root / "state" / ".write.lock"
    with lock_path.open("a+") as handle:
        if fcntl is not None:
            deadline = time.monotonic() + timeout_seconds
            while True:
                try:
                    fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                    break
                except BlockingIOError:
                    if time.monotonic() >= deadline:
                        raise RuntimeError("Another agent is updating this Scratchboard. Try again in a moment.")
                    time.sleep(.1)
        try:
            yield
        finally:
            if fcntl is not None:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def read_day(root: Path, day: str) -> dict | None:
    path = state_path(root, day)
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def all_days(root: Path) -> list[dict]:
    return [json.loads(path.read_text(encoding="utf-8")) for path in sorted((root / "state").glob("????-??-??.json"))]


def current_day(value: str | None) -> str:
    if value:
        datetime.strptime(value, "%Y-%m-%d")
        return value
    return datetime.now(LONDON).date().isoformat()


def resolve_day(root: Path, day: str) -> dict:
    """Freeze a prior active board, then return today's existing or new state."""
    now = utc_now()
    for board in all_days(root):
        if board["state"] == "active" and board["date"] != day:
            board["state"] = "frozen"
            board["updatedAtUtc"] = now
            atomic_json(state_path(root, board["date"]), board)
    board = read_day(root, day)
    if board is None:
        board = {"schemaVersion": 1, "date": day, "state": "active", "createdAtUtc": now, "updatedAtUtc": now, "blocks": []}
    else:
        board["state"] = "active"
        board["updatedAtUtc"] = now
    return board


def safe_text(value: str) -> str:
    return html.escape(value, quote=True)


def safe_href(value: str) -> str | None:
    if value.startswith(("https://", "http://", "/", "./", "../")):
        return value
    return None


def highlight_code(source: str, language: str) -> str:
    """Use packaged Shiki where available; preserve a safe text fallback otherwise."""
    try:
        result = subprocess.run(
            ["node", str(SKILL_ROOT / "scripts" / "highlight-code.mjs"), language or "text"],
            input=source, text=True, capture_output=True, timeout=10, check=True,
        )
        if result.stdout.strip():
            return result.stdout
    except (OSError, subprocess.SubprocessError):
        pass
    return f'<pre class="shiki-fallback"><code>{safe_text(source)}</code></pre>'


def render_markdown(value: str, block_id: str) -> str:
    """Small deliberately safe Markdown subset: prose, links, and fenced code."""
    fence = re.fullmatch(r"```([A-Za-z0-9_+.-]*)\n([\s\S]*?)\n?```", value.strip())
    if fence:
        language, code = fence.groups()
        code_id = f"code-{block_id}"
        label = safe_text(language or "text")
        highlighted = highlight_code(code, language)
        return f'<div class="code-card"><button class="copy" data-copy="{code_id}">Copy</button><span class="subtle">{label}</span><code id="{code_id}" hidden>{safe_text(code)}</code>{highlighted}</div>'
    escaped = safe_text(value)
    escaped = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", lambda m: (f'<a href="{html.escape(safe_href(m.group(2)), quote=True)}" target="_blank" rel="noopener noreferrer">{m.group(1)}</a>' if safe_href(m.group(2)) else m.group(0)), escaped)
    return "".join(f"<p>{paragraph.replace(chr(10), '<br>')}</p>" for paragraph in escaped.split("\n\n") if paragraph)


def render_block(block: dict) -> str:
    kind = block.get("type", "prose")
    value = block["markdown"]
    if kind == "signal":
        return f'<p class="signal">{safe_text(value)}</p>'
    if kind == "callout":
        return f'<aside class="callout">{render_markdown(value, block["id"])}</aside>'
    if kind == "diagram":
        return f'<pre aria-label="Text diagram"><code>{safe_text(value)}</code></pre>'
    if kind == "svg":
        label = safe_text(value)
        return f'<figure><svg viewBox="0 0 640 100" role="img" aria-label="{label}" xmlns="http://www.w3.org/2000/svg"><rect width="640" height="100" rx="12" fill="#181818" stroke="#38bdf8"/><text x="24" y="58" fill="#f5f5f5" font-family="system-ui" font-size="18">{label}</text></svg><figcaption>{label}</figcaption></figure>'
    if kind == "figure":
        return f'<figure><pre>{safe_text(value)}</pre><figcaption>{safe_text(block.get("caption", "Figure"))}</figcaption></figure>'
    return render_markdown(value, block["id"])


def html_page(title: str, body: str, build: str) -> str:
    css = f"../assets/scratchboard.css?v={build}" if title != "Scratchboard" else f"assets/scratchboard.css?v={build}"
    js = f"../assets/copy-code.js?v={build}" if title != "Scratchboard" else f"assets/copy-code.js?v={build}"
    template_name = "index.html" if title == "Scratchboard" else "date-board.html"
    template = (SKILL_ROOT / "templates" / template_name).read_text(encoding="utf-8")
    replacements = {"{{title}}": safe_text(title), "{{css}}": css, "{{js}}": js, "{{body}}": body, "{{build}}": build}
    for token, value in replacements.items():
        template = template.replace(token, value)
    return template


def render_day(root: Path, board: dict, build: str) -> Path:
    weekday = datetime.strptime(board["date"], "%Y-%m-%d").strftime("%A, %-d %B %Y")
    cards = "".join(
        f'<article class="item"><time datetime="{block["capturedAtUtc"]}">{safe_text(block["capturedAtUtc"])}</time>{render_block(block)}</article>'
        for block in sorted(board["blocks"], key=lambda item: (item["capturedAtUtc"], item["captureSequence"]), reverse=True)
    ) or '<p class="subtle">No captured items yet.</p>'
    body = f'<header><h1>Today’s working board</h1><p class="subtle">{weekday} · Europe/London</p><p><a href="../index.html?v={build}">Back to Scratchboard</a></p></header>{cards}'
    path = root / "sessions" / f'{board["date"]}.html'
    path.write_text(html_page(f"Scratchboard · {board['date']}", body, build), encoding="utf-8")
    return path


def month_columns(boards: list[dict]) -> str:
    grouped: dict[str, list[dict]] = {}
    for board in boards:
        if board["state"] == "frozen":
            grouped.setdefault(board["date"][:7], []).append(board)
    sections = []
    for month, entries in sorted(grouped.items(), reverse=True):
        entries.sort(key=lambda item: item["date"])
        columns = min(4, max(1, len(entries)))
        links = "".join(f'<div class="month-column"><a class="month-date" href="sessions/{item["date"]}.html?v={ui_build_id()}">{item["date"]}</a></div>' for item in entries)
        sections.append(f'<section class="panel"><h3>{month}</h3><div class="month-grid" style="--columns:{columns}">{links}</div></section>')
    return "".join(sections) or '<p class="subtle">No frozen boards yet.</p>'


def render_index(root: Path, active: dict, build: str) -> Path:
    body = (f'<header><h1>Scratchboard <span class="skill-tag">.SKILL</span></h1></header>'
            f'<section class="panel"><h2>Today’s board</h2><p><a href="sessions/{active["date"]}.html?v={build}">Open today’s working board</a></p></section>'
            f'<section><h2>Recent boards</h2>{month_columns(all_days(root))}</section>')
    path = root / "index.html"
    path.write_text(html_page("Scratchboard", body, build), encoding="utf-8")
    return path


def copy_assets(root: Path) -> None:
    asset_root = root / "assets"; asset_root.mkdir(exist_ok=True)
    for name in ("scratchboard.css", "copy-code.js"):
        (asset_root / name).write_bytes((SKILL_ROOT / "assets" / name).read_bytes())


def compatibility_page(root: Path, old_path: str, target: str) -> Path:
    """Write a static same-tab compatibility redirect inside the board root."""
    old = (root / old_path).resolve(); destination = (root / target).resolve()
    if root.resolve() not in old.parents or root.resolve() not in destination.parents:
        raise RuntimeError("Compatibility paths must remain inside this Scratchboard root.")
    if old == destination:
        raise RuntimeError("Compatibility route cannot target itself.")
    old.parent.mkdir(parents=True, exist_ok=True)
    relative = os.path.relpath(destination, old.parent).replace(os.sep, "/")
    build = ui_build_id()
    page = html_page("Scratchboard compatibility route", f'<main><p>Moving to the current Scratchboard board… <a href="{safe_text(relative)}?v={build}">Continue</a></p></main><script>location.replace({json.dumps(relative + "?v=" + build)});</script>', build)
    old.write_text(page, encoding="utf-8")
    return old


def render(root: Path, active: dict) -> None:
    build = ui_build_id(); copy_assets(root)
    for board in all_days(root):
        render_day(root, board, build)
    render_index(root, active, build)


def registry(root: Path) -> Path:
    return root / "state" / ".server.json"


def health(url: str, root: Path) -> bool:
    try:
        with urlopen(url + "__scratchboard_health", timeout=1) as response:
            return json.loads(response.read())["root"] == str(root.resolve())
    except Exception:
        return False


def ensure_server(root: Path, idle_seconds: int = 3600) -> tuple[str, str]:
    record_path = registry(root)
    if record_path.exists():
        record = json.loads(record_path.read_text())
        if health(record["url"], root):
            return record["url"], "reused"
    command = [sys.executable, str(Path(__file__).resolve()), "_serve", "--root", str(root), "--idle-seconds", str(idle_seconds)]
    process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    for _ in range(30):
        time.sleep(.1)
        if record_path.exists():
            record = json.loads(record_path.read_text())
            if health(record["url"], root):
                return record["url"], "started"
    process.terminate()
    raise RuntimeError("Scratchboard server did not become healthy.")


class BoardServer(ThreadingHTTPServer):
    daemon_threads = True
    def __init__(self, root: Path, idle_seconds: int):
        self.root = root.resolve(); self.idle_seconds = idle_seconds; self.last_activity = time.monotonic()
        super().__init__(("127.0.0.1", 0), partial(BoardHandler, directory=str(self.root)))


class BoardHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args): pass
    def do_GET(self):
        self.server.last_activity = time.monotonic()
        if self.path.split("?", 1)[0] == "/__scratchboard_health":
            payload = json.dumps({"root": str(self.server.root)}).encode()
            self.send_response(200); self.send_header("Content-Type", "application/json"); self.send_header("Content-Length", str(len(payload))); self.end_headers(); self.wfile.write(payload); return
        super().do_GET()
    def end_headers(self):
        self.send_header("Cache-Control", NO_CACHE); self.send_header("Pragma", "no-cache"); self.send_header("Expires", "0"); super().end_headers()


def serve_forever(root: Path, idle_seconds: int) -> None:
    server = BoardServer(root, idle_seconds); url = f"http://127.0.0.1:{server.server_port}/"
    atomic_json(registry(root), {"pid": os.getpid(), "url": url, "root": str(root.resolve()), "startedAtUtc": utc_now()})
    try:
        server.timeout = .5
        while time.monotonic() - server.last_activity < idle_seconds:
            server.handle_request()
    finally:
        server.server_close(); registry(root).unlink(missing_ok=True)


def close_server(root: Path) -> bool:
    record_path = registry(root)
    if not record_path.exists(): return False
    record = json.loads(record_path.read_text())
    try: os.kill(int(record["pid"]), signal.SIGTERM)
    except ProcessLookupError: pass
    record_path.unlink(missing_ok=True); return True


def update(args: argparse.Namespace) -> None:
    repo = Path(args.repo).resolve(); root = root_for(repo, args.create_docs); day = current_day(args.date)
    with write_lock(root):
        board = resolve_day(root, day)
        sequence = max((block["captureSequence"] for block in board["blocks"]), default=0) + 1
        block = {"id": f"block_{uuid.uuid4().hex}", "capturedAtUtc": utc_now(), "captureSequence": sequence, "type": args.kind, "markdown": args.content}
        if args.caption: block["caption"] = args.caption
        board["blocks"].append(block)
        board["updatedAtUtc"] = utc_now(); atomic_json(state_path(root, day), board); render(root, board)
    url, lifecycle = ensure_server(root)
    print(json.dumps({"changed": f"Added top item to {day}", "skillVersion": SKILL_VERSION, "uiBuildId": ui_build_id(), "server": lifecycle, "view": "Today’s board", "browserValidation": "native adapter must be used when the host exposes it", "url": f"{url}sessions/{day}.html?v={ui_build_id()}"}, indent=2))


def validate() -> None:
    required = [SKILL_ROOT / "SKILL.md", SKILL_ROOT / "templates" / "index.html", SKILL_ROOT / "templates" / "date-board.html", SKILL_ROOT / "assets" / "scratchboard.css", SKILL_ROOT / "assets" / "copy-code.js", SKILL_ROOT / "schema" / "board-data.schema.json"]
    missing = [str(path) for path in required if not path.exists()]
    if missing: raise RuntimeError("Missing skill assets: " + ", ".join(missing))
    json.loads((SKILL_ROOT / "schema" / "board-data.schema.json").read_text())
    print("Scratchboard static package validation passed")


def main() -> None:
    parser = argparse.ArgumentParser(description="Create and serve a repo-local Scratchboard")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("update", "serve", "close"):
        item = sub.add_parser(name); item.add_argument("--repo", default="."); item.add_argument("--create-docs", action="store_true")
    update_parser = sub.choices["update"]; update_parser.add_argument("--content", required=True); update_parser.add_argument("--date"); update_parser.add_argument("--kind", choices=("prose", "signal", "callout", "diagram", "svg", "figure"), default="prose"); update_parser.add_argument("--caption")
    sub.choices["serve"].add_argument("--idle-seconds", type=int, default=3600)
    redirect = sub.add_parser("redirect"); redirect.add_argument("--repo", default="."); redirect.add_argument("--create-docs", action="store_true"); redirect.add_argument("--old-path", required=True); redirect.add_argument("--target", required=True)
    hidden = sub.add_parser("_serve"); hidden.add_argument("--root", required=True); hidden.add_argument("--idle-seconds", type=int, required=True)
    sub.add_parser("validate")
    args = parser.parse_args()
    if args.command == "update": update(args)
    elif args.command == "serve":
        root = root_for(Path(args.repo).resolve(), args.create_docs); url, state = ensure_server(root, args.idle_seconds); print(json.dumps({"url": url, "server": state}))
    elif args.command == "close": print(json.dumps({"closed": close_server(root_for(Path(args.repo).resolve(), args.create_docs))}))
    elif args.command == "redirect":
        root = root_for(Path(args.repo).resolve(), args.create_docs)
        print(json.dumps({"redirect": str(compatibility_page(root, args.old_path, args.target))}))
    elif args.command == "_serve": serve_forever(Path(args.root), args.idle_seconds)
    else: validate()


if __name__ == "__main__":
    main()
