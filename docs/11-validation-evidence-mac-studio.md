# Doc 11 — Validation Evidence — Mac Studio

**Status:** Gate 0–14 Mac Studio evidence complete
**Evidence window:** 24–25 August 2026
**Machine:** `MacStudio`, model `Mac Studio`, identifier `Mac16,9`
**Deferred:** Real Mac mini Phase 15 evidence

## Proven implementation baseline

The implementation was developed and published through normal SSH commits on `main`. The initial real managed-state publication is:

```text
SHA:      6ce5c2d3b67ffdeeeb7d6a1f57f2a80e7dc69a0a
subject:  managed-state: publish 4 component changes
source:   MacStudio
```

Its component body records:

```text
AGENTS.md: added
skills added:
  chat-handoff
  operational-modes
  semantic-compression
```

The receipt, status command, local HEAD and `origin/main` all agreed on the full SHA. The immediate subsequent publisher invocation returned `matches last published source` and created no commit.

## Environment and tooling proof

Validated runtime facts:

```text
Python:       3.14.4, CPython, arm64
environment:  repository .venv, receipt-backed development closure
PyYAML:       6.0.3
pytest:       9.1.1
pip-tools:    7.6.1
rsync:        3.5.0, protocol 32, repository-owned arm64 executable
```

`otool -L` reported only:

```text
/usr/lib/libiconv.2.dylib
/usr/lib/libSystem.B.dylib
/usr/lib/libcharset.1.dylib
```

No `/opt/homebrew` or Homebrew Cellar runtime linkage exists in rsync. A missing environment was built from the hashed development lock. A later deliberate stale-receipt change was repaired through the bounded `.venv --repair` path. Validation then reported the environment valid.

The first interrupted rsync configure attempt exposed generated Autotools debris at repository root. The exact generated files/symlinks were removed before Git staging, the build ran from its private source directory under a sanitized system `PATH`, and no debris entered history.

## Scope and publication proof

The live bounded source fingerprint before publication was:

```text
9e66c8ca1c97d80bbcbcdc92743abff1d8b7192fb6f15306f924c413c1ebba97
```

Dynamic user-skill roots were:

```text
chat-handoff
operational-modes
semantic-compression
```

The `.system` directory was observed only as an excluded root and never traversed for ingestion. Existing `.DS_Store` files were observed as ignored noise and left untouched. Neither name appears in `latest/`, any ZIP or the managed commit.

The initial generated artifacts were:

```text
upload-ready/global-agents.zip
upload-ready/skills/chat-handoff.zip
upload-ready/skills/operational-modes.zip
upload-ready/skills/semantic-compression.zip
```

The global archive contains exactly root `AGENTS.md`. Every skill archive contains the matching parent wrapper and recursive contents.

The initial publication’s first staging attempt stopped before Git mutation because porcelain status initially collapsed the new artifact directory. The implementation was corrected to enumerate all untracked files, a regression test was added, and the already validated projection was resumed through the same path-scoped staging, deterministic change-set, commit, push and receipt functions. No force operation or broad staging occurred.

## Automated and isolated proof

The decisive complete suite result was:

```text
75 passed in 2.90s
```

Independent suites also passed:

```text
managed scope + consumer:       19 passed
Git publication + state:       16 passed
portable artifact suite:        7 passed
```

Coverage includes:

- all four publication modes and strict Europe/London scheduling;
- conservative settlement restart after boot/time uncertainty;
- dynamic current and future skill discovery;
- recursive content and executable identity;
- `.system` exclusion and `.DS_Store` preservation;
- checksum change detection with identical size/timestamp;
- dry-run non-mutation and second-dry-run equivalence;
- bounded file, directory, skill and `AGENTS.md` deletion;
- symlink, special-name, collision and traversal rejection;
- deterministic ZIP bytes, wrappers, permissions and unsafe-member rejection;
- bounded README reconciliation;
- exact Git path staging, no-op suppression and deterministic component classification;
- failed-push preservation and exact retry without duplicate commits;
- safe consumer fast-forward and dirty-state refusal;
- isolated consumer initial deployment, update, no-op and deletion;
- preservation of `.system`, `.DS_Store` and unrelated consumer sentinels;
- hard refusal of the Mac Studio authoritative target by the consumer;
- publisher/consumer role separation and Mac Studio consumer-install refusal.

The live Mac Studio source fingerprint was captured immediately before and after the full and targeted simulation suites. Both values were identical:

```text
9e66c8ca1c97d80bbcbcdc92743abff1d8b7192fb6f15306f924c413c1ebba97
```

No live managed canary was created or deleted. The real meaningful publication used existing authoritative managed content; nested/new/deletion behaviour was proved only in isolated test trees, honoring the goal’s separate canary-authorization boundary.

## Launchd proof

The installed publisher service is:

```text
label:     com.yodaspow.codex-config-manager.publisher
interval:  60 seconds
program:   /Users/spowart/Scripts/codex-config-manager/.venv/bin/codex-config-manager-publisher
working:   /Users/spowart/Scripts/codex-config-manager
```

The generated plist passed `plutil -lint`, was loaded in `gui/<uid>`, and produced a headless `matches last published source` result. The consumer plist and service were both absent on the Mac Studio.

GitHub SSH authentication was executed through the launchd user domain using batch mode. GitHub returned its expected authenticated/no-shell message and exit status `1`.

The publisher service was uninstalled and reinstalled through its operator commands. Python SHA-256 and manifest checks proved that uninstall preserved the live source, `latest/`, private config, `.venv` receipt and rsync executable; runtime state and logs remained present. The publisher service was then restored and loaded.

## Gate disposition

| Gates | Result |
| --- | --- |
| 0–1 | Governing inputs, bounded source and normal SSH Git history revalidated. |
| 2–4 | Hashed Python closures, receipt-backed `.venv` and isolated rsync proven. |
| 5–7 | Config/identity, shared exclusions, private candidate and `latest/` proven. |
| 8–9 | Publisher, artifacts, deterministic Git publication and retry proven. |
| 10–11 | Consumer implementation and isolated simulation proven; no live consumer activation. |
| 12 | Publisher-only LaunchAgent installed and validated on the Mac Studio. |
| 13–14 | Permanent implementation/operations record, evidence and bounded Mac mini handoff published. |

Phase 15 remains deferred by design and is not a failure of the Mac Studio gate set.
