# Doc 20 — Postmortem — Skill Runtime Artifacts and Managed-State Publication Deadlock

**Status:** Resolved and validated 10 October 2026

**Incident window:** 20 September–10 October 2026

**Affected lane:** Mac Studio managed-state publisher

**Recovery commit:** `720be77fde489905b3fe388a9b535812b8f3fb54`

**Related contracts:** [Doc 1](01-implementation-discovery-managed-skill-ingestion-exclusions.md), [Doc 10](10-implementation-architecture-and-operations.md), and [Doc 16](16-repository-agent-workflow-and-publication-guardrails.md)

## Current status

- ✅ The publisher is loaded and its latest scheduled result is successful.
- ✅ `computer-use-helper` is present in canonical `latest/`, its portable ZIP,
  and GitHub history.
- ✅ Transient Python caches are excluded consistently from detection,
  ingestion, canonical snapshots, artifacts and consumer deployment.
- ✅ A remaining candidate file that is Git-ignored and not already tracked now
  stops before repository projection begins.
- ✅ Repository-development `build/` and `dist/` ignores are root-anchored, so
  they cannot hide intentionally vendored nested skill distributions.
- ✅ Scratchboard's required vendored distribution files are now represented in
  canonical `latest/`, not only inside its ZIP.
- ▶ Future skill-creation tooling should adopt the requirements and validation
  matrix in this document.
- ⛔ This incident does not prove that every possible runtime-generated filename
  for every language or tool is known or should be globally excluded.

## Executive summary

An installed executable skill was imported as a Python module during normal use.
Python created a bytecode cache inside the live skill directory. Codex Config
Manager's original contract managed every regular skill file except
`.DS_Store`, so it treated that cache as source and copied it into the local
canonical snapshot and Scratchboard ZIP.

The repository's `.gitignore` independently ignored `__pycache__/` and
`*.pyc`. Git therefore omitted the canonical cache file while the ZIP builder
included it. The publisher staged a ZIP-only difference, could not derive a
canonical skill component from `latest/`, failed before commit, and left the
generated ZIP staged. Every later scheduled run correctly refused that dirty
index, so a subsequently added skill was detected and settled but could not be
published.

Investigation then exposed a second form of the same boundary mismatch. The
repository's unanchored `dist/` ignore rule also matched Scratchboard's
intentionally vendored `node_modules/**/dist/` files. Those files existed in
the live skill and portable ZIP but had never entered tracked canonical
`latest/`. A fresh consumer using `latest/` rather than the ZIP could therefore
have received an incomplete executable skill.

The incident was caused by inconsistent classification of package source,
vendored runtime content and generated execution state across the filesystem,
manifest, rsync, artifact and Git layers. The added skill was not defective;
it merely revealed a publisher that had already been jammed by the earlier
Scratchboard projection.

## User-visible impact

- The newly installed `computer-use-helper` skill remained absent from GitHub
  after its five-minute settlement period.
- The Mac Studio launch agent remained loaded and ran on schedule, but each
  eligible publication exited with an error because the repository index was
  already dirty.
- The last successful managed publication remained valid; no published commit
  was rewritten or corrupted.
- No live skill source was lost. The bytecode file was derived from existing
  source, and no credential or private configuration was involved.
- Scratchboard's portable ZIP contained its vendored runtime, but canonical
  `latest/` did not contain all of the same Git-ignored distribution files.

## Detection

The incident was detected when the operator noticed that a newly added skill
had not appeared in Codex Config Manager's published state.

Read-only status established that the service was loaded and still observing
the source, while the repository was dirty:

```text
role: publisher
launchd.loaded: true
repository.dirty: true
repository.ahead: 0
repository.behind: 0
staged path: upload-ready/skills/scratchboard.zip
last exit code: 1
```

The live-versus-published skill comparison showed one delayed component:

```text
live only: computer-use-helper
```

The publisher log showed that it detected the new managed state, completed the
settlement period and repeatedly reached eligibility. Its error stream then
showed the actual gate:

```text
managed change observed; settlement started
settled and eligible
ERROR: repository contains pre-existing worktree or index changes
```

## Timeline

| Time | Event |
| --- | --- |
| 20 September 2026, 15:11 BST | A Codex task imported `scripts.scratchboard` with Python 3.13 to call renderer functions directly. Python created `scripts/__pycache__/scratchboard.cpython-313.pyc`. |
| 20 September 2026, 15:16 BST | The publisher ingested the new regular file, rebuilt `scratchboard.zip`, and staged that artifact. Git ignored the corresponding canonical cache path. |
| 20 September 2026 onward | Publication failed because the staged transaction had no canonical `latest/` component. The staged ZIP then caused every later run to stop at the clean-base gate. |
| 10 October 2026, 20:31 BST | `computer-use-helper` appeared in the live skill set. The publisher detected it and began settlement. |
| 10 October 2026, 20:37 BST | The new state became settled and eligible, but the existing dirty index prevented publication. |
| 10 October 2026, 21:22 BST | Commit `7ed0782` added transient Python cache exclusions and pre-projection Git-trackability validation. |
| 10 October 2026, 21:29 BST | Commit `7bbe9f1` refined the guard so already-tracked vendored files remain valid even if a later broad ignore pattern matches them. |
| 10 October 2026, 21:31 BST | Commit `a6f6388` root-anchored repository `build/` and `dist/` ignores, preventing them from hiding nested managed distributions. |
| 10 October 2026, 21:31 BST | Managed commit `720be77` added `computer-use-helper`, reconciled Scratchboard, rebuilt artifacts without caches, and published the complete canonical state. |

## Exact initiating action

The cache was not created by Codex Config Manager. It was created by normal
Python import behaviour when another Codex task used a command of this form:

```bash
cd ~/.codex/skills/scratchboard \
&& python -c 'from scripts.scratchboard import read_day, render; ...'
```

Executing a Python file as the main script normally does not cache that main
module. Importing it as `scripts.scratchboard` allowed Python 3.13 to write the
compiled module beneath `scripts/__pycache__/`. The cache's creation timestamp,
bytecode tag and embedded source filename aligned exactly with that command.

This was a legitimate use of an executable skill. The system must tolerate it;
operator discipline alone is not an adequate control.

## Causal chain

```text
installed skill module imported
        ↓
Python writes __pycache__/scratchboard.cpython-313.pyc
        ↓
source manifest classifies every regular file as managed
        ↓
rsync copies the cache into candidate and latest/
        ↓
ZIP builder includes the cache
        ↓
repository .gitignore suppresses the canonical latest/ cache path
        ↓
only scratchboard.zip is staged
        ↓
commit-message derivation finds no canonical latest/ component
        ↓
publication fails before commit and leaves the ZIP staged
        ↓
clean-base protection rejects every later scheduled run
        ↓
new skill is detected and settled but cannot reach GitHub
```

## Root causes

### 1. Runtime state and skill source shared one directory

The installed Scratchboard package was executable in place. Python was allowed
to write interpreter state beside source files, while Codex Config Manager
treated the entire skill tree as durable source.

### 2. Exclusion policy was incomplete and inconsistent

Only `.system/**` and `.DS_Store` were explicitly excluded. Python bytecode and
tool caches were absent from the manifest and rsync contract, even though the
repository's ordinary development `.gitignore` already treated them as noise.

### 3. Artifact and canonical representations disagreed

The ZIP builder traversed the physical snapshot and included files that Git
would not stage. Publication semantics were correctly derived only from
canonical `latest/`, but there was no earlier proof that every candidate file
could be represented there.

### 4. Repository ignore patterns crossed the payload boundary

The unanchored `dist/` pattern was intended for Codex Config Manager's own root
build output. Git also applied it to nested skill payloads. This silently hid
Scratchboard's vendored JavaScript distribution files from canonical history
while the ZIP still contained them.

### 5. A pre-commit failure could strand publisher-owned staged state

The clean-base rule correctly prevents unattended publication over a dirty
checkout. Once the publisher itself left a generated file staged, however, the
same protection converted one failed transaction into a persistent deadlock.
The current repair prevents this incident class before projection. A general
rollback design for every possible failure after repository mutation remains a
separate hardening opportunity.

## Contributing conditions

- The cache file contained valid bytecode derived from public skill source, so
  content validation did not identify it as unsafe.
- Deterministic ZIP generation made the cache addition reproducible rather than
  filtering it as timestamp noise.
- The original Scratchboard managed commit had a legitimate canonical skill
  change, allowing ZIP-only omissions inside that larger transaction to remain
  unnoticed.
- Service health and publication health were different: launchd was loaded and
  scheduling runs, but each invocation exited at a safety gate.
- Status reported the dirty repository and last successful publication, but it
  did not classify publisher-owned stranded projection state separately.

## Corrective actions completed

### Consistent transient Python exclusions

The following are excluded at every depth across source and snapshot manifests,
rsync, candidate equivalence, ZIP construction and validation, publication
comparison, and consumer deployment:

```text
__pycache__/
*.pyc
*.pyo
.pytest_cache/
.mypy_cache/
.ruff_cache/
```

Existing excluded caches on live endpoints are preserved. They are not copied,
deleted, published or treated as meaningful changes.

### Pre-projection Git representability check

After private candidate validation but before repository mutation, the publisher
maps each candidate file to its intended `latest/` path and checks Git ignore
rules. A path is representable when either:

1. it is already tracked, even if a later broad pattern also matches it; or
2. Git does not ignore it.

An ignored, untracked candidate path stops before `latest/`, ZIPs, README or the
Git index are changed.

### Root-scoped project build ignores

The repository's development-only patterns are now:

```gitignore
/build/
/dist/
```

They no longer suppress nested `dist/` directories that form part of a managed
skill's declared runtime package.

### Canonical reconciliation and recovery

The stale staged ZIP was reverted, the publisher was held during repair, and
generated downstream files were reconciled without modifying the live
Scratchboard skill. Managed commit `720be77` then:

- added five `computer-use-helper` files;
- added 1,873 previously hidden Scratchboard distribution files to canonical
  `latest/`;
- rebuilt `scratchboard.zip` without Python caches; and
- pushed the validated transaction normally to `origin/main`.

## Validation evidence

The decisive post-recovery repository validation reported:

```text
distribution_valid: true
repository.dirty: false
repository.ahead: 0
repository.behind: 0
source_fingerprint: f02385032e402173c5c9b17d71a48bc58780d49f77cfa654a929a81ab0e6a0e7
latest_fingerprint: f02385032e402173c5c9b17d71a48bc58780d49f77cfa654a929a81ab0e6a0e7
```

The complete automated suite passed:

```text
101 passed in 3.18s
```

The final content checks reported:

```text
computer_use_helper_tracked_files=5
scratchboard_tracked_dist_files=1873
tracked_transient_cache_files=0
scratchboard_zip_transient_cache_files=0
```

Git publication identity was aligned:

```text
HEAD=720be77fde489905b3fe388a9b535812b8f3fb54
TRACKING=720be77fde489905b3fe388a9b535812b8f3fb54
REMOTE=720be77fde489905b3fe388a9b535812b8f3fb54
```

After an explicit launchd check, the publisher's latest exit code was `0`.

## Requirements for future skill-creation tooling

A project or global skill maker should treat an installed skill as a portable
package with an explicit boundary between durable package content and mutable
runtime state.

### Package classification

Every generated path must be classified as one of:

| Class | Examples | Required treatment |
| --- | --- | --- |
| Authored source | `SKILL.md`, scripts, references, templates | Include and validate |
| Declared vendored runtime | packaged JavaScript, WASM, schemas, static assets | Include, ensure Git representability, and test from a fresh clone |
| Derived build output required at runtime | deliberately shipped compiled bundle | Include only by explicit package decision; do not rely on a broad ignore exception |
| Execution state | bytecode, caches, PID files, sockets, logs, temporary files | Keep outside the skill root or exclude consistently |
| Operator or project state | boards, generated reports, databases, local configuration | Store in the selected project or approved application-support/config location |
| Secrets | tokens, private configuration, credentials | Keep outside published skill content and fail validation if encountered |

### Creation and update gates

A skill maker should not declare a package ready until it proves:

1. the package contains no known interpreter, test, type-checker or linter
   caches;
2. running and importing the skill does not create a meaningful package diff;
3. any unavoidable cache is ignored consistently by source manifest, transport,
   archive and consumer logic;
4. required vendored files survive a clean Git clone and are not hidden by
   repository-level ignore patterns;
5. the portable ZIP and canonical unpacked representation contain the same
   meaningful files;
6. validation runs in an isolated temporary directory where practical;
7. runtime writes target project state, application support, cache or temporary
   locations rather than the installed package;
8. deletion and update tests preserve excluded live state without using
   `--delete-excluded`;
9. package validation is rerun after actual execution, not only immediately
   after scaffolding; and
10. a failed publication cannot be mistaken for an offline scheduler merely
    because the service remains loaded.

### Cross-language generated-state review

The Python exclusions are evidence-based, not a universal list. Skill tooling
should assess each runtime deliberately. Examples requiring classification
include:

```text
Python:     __pycache__, *.pyc, test/type/lint caches, virtual environments
Node.js:    npm/yarn/pnpm logs and caches, coverage, temporary bundles
Rust:       target/
Go:         coverage and locally written build outputs
Java/Kotlin: class output, Gradle state and build directories
.NET:       bin/, obj/
Browsers:   profiles, caches, downloaded assets and generated screenshots
Servers:    PID files, sockets, logs, state databases and generated certificates
```

Names such as `dist/`, `build/`, `target/`, `bin/` and `assets/` are ambiguous:
they may be disposable output in one repository and required vendored package
content in another. Global basename exclusions are unsafe without a declared
package contract.

## Scratchboard-specific guardrails

Scratchboard is both a skill package and an executable renderer/server. Its
future maintenance should preserve these boundaries:

- Treat the installed skill directory as immutable package content during
  ordinary use.
- Write boards, rendered pages, state and locks beneath the selected project's
  `docs/scratchboard/`, not beneath the installed skill.
- Keep server process state and temporary material outside the skill package.
- Prefer documented CLI commands over importing the installed script for
  one-off operations.
- When a direct import is genuinely needed, use `python -B` or
  `PYTHONDONTWRITEBYTECODE=1` as a hygiene measure. This is defence in depth;
  Codex Config Manager must still tolerate caches created by another caller.
- Run validation in temporary repositories and ensure it does not write caches
  into the installed package.
- Preserve the explicitly vendored JavaScript/WASM runtime and test it from a
  clean canonical checkout, not only from the authoring machine's live folder.
- After every Scratchboard package update, compare the live manifest,
  canonical `latest/` manifest and ZIP membership after exercising both CLI and
  import paths.

The strongest safeguard is architectural: runtime mutation belongs outside the
installed package. Command-line flags that suppress bytecode are useful but
cannot control every future caller.

## Monitoring and recovery guidance

When a future skill does not publish after settlement, distinguish scheduler
availability from transaction health:

1. confirm detected machine identity and publisher role;
2. inspect read-only status for loaded service, repository dirtiness,
   ahead/behind state and pending publication;
3. compare live and published top-level skill names;
4. inspect the latest publisher observation and error without treating a loaded
   launch agent as proof of successful publication;
5. inspect the exact staged paths before changing anything;
6. determine whether staged state belongs to the publisher or to a human;
7. never broaden the publisher allowlist or sweep unrelated changes merely to
   clear the gate; and
8. after recovery, prove distribution validity, clean Git state, matching
   fingerprints, remote SHA alignment and a successful scheduled exit.

## Remaining hardening opportunities

These are follow-up considerations, not unresolved blockers for the recovered
publisher:

1. Add bounded rollback or a temporary-index transaction so any publisher
   failure after repository projection but before commit cannot leave
   publisher-owned staged state behind.
2. Give status a distinct classification for a cleanly loaded scheduler whose
   last invocation failed, and for stranded publisher-generated paths.
3. Let skill creation declare package-specific runtime and vendored-content
   policies rather than growing one global basename exclusion list indefinitely.
4. Add an end-to-end fixture that executes or imports a representative skill,
   publishes it from a clean repository, clones the result, and validates both
   canonical and ZIP forms.
5. Consider a public-content scan appropriate to generated skill payloads so
   an unignored secret-bearing file fails independently of Git ignore rules.

## Durable conclusion

An executable skill directory cannot safely be treated as both an unrestricted
runtime workspace and an exact publishable package. The manager must exclude
known execution state consistently, prove remaining files are representable
before repository mutation, and preserve declared vendored runtime content.
Skill creators must direct mutable state outside the installed package and test
the package after real execution. Both sides of that boundary are necessary;
neither a larger `.gitignore` nor caller discipline alone is sufficient.
