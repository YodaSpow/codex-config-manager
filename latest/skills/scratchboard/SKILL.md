---
name: scratchboard
description: "Create or update a repo-local Scratchboard: a persistent UK-day working board with safe static HTML, localhost preview, and concise handoff. Use for provisional project thinking, not formal documentation."
---

# Scratchboard

**Version:** 1.0 · **Updated:** 2 September 2026

Scratchboard is a self-contained, globally installed skill that creates output only in the active repository. It maintains one current board per `Europe/London` calendar day, freezes earlier days under Recent, and renders a static, browser-visible working layer.

## Use

Run `scripts/scratchboard.py update` from the selected repository, with a `--content` value. The command discovers the existing `docs`/`Docs` directory. It must ask before creating `docs/` if none exists. It returns a concise JSON handoff containing the canonical direct localhost URL, server state, skill version, and renderer UI build.

The normal interactive route is server-first: start or reuse the repo's localhost server and provide the direct link. Whenever the current host exposes a native Web preview or `Open in` adapter, use that adapter alongside the direct link to keep the active Today board in place. If the server cannot start or serve the board, report that interactive preview is unavailable and offer an in-scope workaround; do not pretend it is live.

## Non-negotiable behaviour

- Resolve the canonical UK day before every capture. Reuse its board if present; if a prior active day exists, freeze it under Recent before creating the new board.
- Keep new captures at the top. Sequence an invoking agent's own updates; use the included lock and atomic replacement for genuinely concurrent writers.
- Render captured text safely. Never turn captured HTML, JavaScript URLs, unsafe image URLs, or unsanitised SVG into executable browser content.
- Keep `.SKILL` identity on the parent only. Every generated operator page shows the same muted renderer-supplied UI build.
- The release line above changes for skill capability or behaviour changes. The renderer derives its UI build from UI assets; ordinary content captures do not change it.
- Respect applicable repository and global rules as bounded overrides. Adapt only a genuinely conflicting detail; surface a conflict that blocks a core Scratchboard capability.

## Commands

```text
update --content TEXT [--repo PATH] [--date YYYY-MM-DD] [--create-docs]
serve [--repo PATH] [--idle-seconds SECONDS]
close [--repo PATH]
redirect --repo PATH --old-path PATH --target PATH
validate
```

`--date` exists for deterministic validation. Normal use must omit it so the canonical UK day is used.

## References

- Read [references/contract.md](references/contract.md) for generated layout, safety, handoff, and validation rules.
- The reusable behaviour is packaged here. Do not use Keymaker documents or prototype files as an invocation dependency.
