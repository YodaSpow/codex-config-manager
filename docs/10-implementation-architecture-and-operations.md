# Doc 10 — Implementation Architecture and Operations

**Status:** Implemented and validated on the Mac Studio through Doc 3 Gates 0–14
**Implemented:** 24 August 2026
**Runtime role:** Mac Studio publisher
**Deferred:** Real Mac mini installation and live consumer validation under Phase 15
**Evidence:** [Doc 11 — Mac Studio Validation Evidence](11-validation-evidence-mac-studio.md)
**Consumer handoff:** [Doc 12 — Mac mini Phase 15 Handoff](12-mac-mini-phase-15-handoff.md)

## Purpose and authority

Codex Config Manager publishes one bounded part of the Mac Studio global Codex state and later deploys it to the Mac mini. The direction is fixed:

```text
Mac Studio ~/.codex managed source
        ↓ publisher ingestion
private per-transaction candidate
        ↓ validation
repository latest/
        ↓ deterministic derivation
upload-ready/ + bounded README section
        ↓ path-scoped commit and SSH push
GitHub origin/main
        ↓ future safe fast-forward
Mac mini latest/
        ↓ future consumer deployment
Mac mini ~/.codex managed targets
```

The live Mac Studio `~/.codex` is the authoring authority. `latest/`, `upload-ready/`, GitHub, and the Mac mini are downstream representations. The publisher has no code path that deploys repository state back into the Mac Studio live source.

## Managed universe

The managed source is exactly:

```text
~/.codex/AGENTS.md                  included when present
~/.codex/skills/<user-skill>/**    included dynamically and recursively
```

The following are outside the managed universe:

- `~/.codex/skills/.system/**` — excluded recursively at ingestion and preserved on consumers;
- `.DS_Store` — ignored at every depth and never deliberately removed;
- every other file or directory under `~/.codex`;
- symlinks and special filesystem entries, which cause validation failure rather than traversal or silent loss.

No current skill name is allowlisted. Every normal immediate directory below `skills/` participates automatically. Control characters and hidden top-level skill names are rejected; case-colliding paths are rejected for portable Git/ZIP behaviour. Regular file bytes and executable identity are managed. Empty directories inside a skill are rejected because Git cannot represent them truthfully; a completely empty skill set is represented without requiring a placeholder file. Timestamps, xattrs and ACLs are not semantic publication identity.

## Repository topology

```text
config/
├── config.example.yaml            public complete schema
└── config.yaml                    private ignored machine truth
docs/                              architecture, evidence and handoff
latest/                            canonical unpacked published state
launchd/                           tracked role templates
requirements/                      hashed runtime/development locks
scripts/bootstrap.py               pre-environment bootstrap and repair
src/codex_config_manager/          Python implementation
tests/                             unit and isolated integration suite
tooling/rsync/                     tracked rsync source/build contract
upload-ready/
├── global-agents.zip
└── skills/<skill-name>.zip
.tools/rsync/                       ignored repository-owned runtime
.venv/                              ignored repository-owned Python environment
```

There is no persistent `staging/` mirror. A private temporary candidate exists only for one publisher transaction. `latest/` is Git-tracked transported state, not a Mac Studio authoring surface.

## Environment ownership

The first validated environment uses:

- Python `3.14.4` on Apple Silicon;
- PyYAML `6.0.3` as the direct runtime dependency;
- pytest `9.1.1` and pip-tools `7.6.1` in the development closure;
- exact hashes in `requirements/runtime.lock` and `requirements/development.lock`;
- upstream rsync `3.5.0`, source SHA-256 `c7ffd1ef653e99540f661e47cb00b7f9cad1ee6b972399b16f93d672656e0d33`.

The public Python compatibility declaration is `>=3.12,<3.15`; the evidence above records the interpreter actually tested. Normal scheduled operation uses only `.venv` and `.tools/rsync/bin/rsync`. It never searches interactive `PATH`, falls back to Apple rsync, or resolves a Homebrew rsync. The rsync binary links only to permitted macOS system libraries.

Bootstrap a development environment:

```bash
cd "/Users/spowart/Scripts/codex-config-manager" \
&& /opt/homebrew/opt/python@3.14/bin/python3.14 scripts/bootstrap.py --environment development \
&& echo "✅ Command ran successfully"
```

Validate an existing environment without mutation:

```bash
cd "/Users/spowart/Scripts/codex-config-manager" \
&& .venv/bin/python scripts/bootstrap.py --environment development --validate-only \
&& echo "✅ Command ran successfully"
```

If validation reports a stale or corrupt repository-local environment, repair only the verified `.venv` target:

```bash
cd "/Users/spowart/Scripts/codex-config-manager" \
&& /opt/homebrew/opt/python@3.14/bin/python3.14 scripts/bootstrap.py --environment development --repair \
&& echo "✅ Command ran successfully"
```

Dependency refresh is deliberate, never scheduled. The exact pip-tools compile commands are recorded in `requirements/README.md`. Review lock diffs, rebuild `.venv`, run the full suite, and publish the change as a normal development commit.

Rebuild rsync only after a deliberate tracked contract change:

```bash
cd "/Users/spowart/Scripts/codex-config-manager" \
&& /opt/homebrew/opt/python@3.14/bin/python3.14 tooling/rsync/build.py \
&& echo "✅ Command ran successfully"
```

The build downloads only the pinned upstream archive, verifies its SHA-256, builds with Apple tooling under a sanitized system `PATH`, installs beneath `.tools/rsync`, and writes `build-receipt.json`.

## Configuration and identity

`config/config.example.yaml` is the public union schema. `config/config.yaml` is ignored and contains truthful machine-local values. Role is always explicit and never inferred from hardware.

Machine identity is derived mechanically from macOS `Model Name` and compared with `machine.id`. The proven identities are `MacStudio` and `MacMini`. A mismatch fails before runtime mutation.

The initial publisher settings are:

```yaml
publisher:
  check_interval: 1m
  settle_period: 5m
  publication:
    mode: "after_settle"
    schedule:
      frequency: "daily"
      local_time: "18:00"
      timezone: "Europe/London"
    minimum_interval: 1h
```

Supported modes are:

- `after_settle` — publish on the next check after the full quiet period;
- `paused` — continue observation and settlement but freeze candidate, repository and retry mutation;
- `scheduled` — publish only at the strict daily `18:00` Europe/London boundary when already settled; a missed or unsettled boundary waits for the next day;
- `throttled` — publish settled state only when the minimum interval since the last successful publication has also elapsed.

Durations use one whole number plus one lowercase `s`, `m`, `h`, or `d`. Schema limits and cross-field validation are enforced before mutation.

Git identity is also configured: remote name, `main` branch, and exact SSH URL. Runtime validates the current branch, tracking ref, remote URL, ahead/behind state and worktree/index safety.

## Publisher operation

Each invocation:

1. loads and validates private configuration, machine identity and publisher role;
2. acquires a non-blocking single-instance lock;
3. validates the `.venv` receipt and exact repository-owned rsync;
4. computes a canonical SHA-256 manifest of managed source content and executable identity;
5. updates one atomic, bounded local settlement receipt;
6. stops without repository mutation when unchanged, unsettled, paused, outside schedule, or throttled;
7. validates Git and remote history before an eligible transaction;
8. builds a private candidate with `.system` excluded at source and `.DS_Store` ignored;
9. proves source stability and candidate equivalence;
10. reconciles `latest/` using checksum dry-run, real rsync and a second equivalence dry-run;
11. builds and validates deterministic ZIP artifacts and the bounded README section;
12. permits only `latest/**`, validated artifacts and `README.md` in unattended staging;
13. derives one deterministic component-level change set from the Git index;
14. commits and pushes normally over SSH, then records the full SHA and component summary atomically.

The publisher creates no commit on no-op, no automatic tag, no GitHub Release and no force push. Commit context is limited to `AGENTS.md` and dynamic top-level skill actions (`added`, `updated`, `removed`). It never interprets nested content semantically.

If push fails after commit, the exact base, tree, message, component list and commit SHA remain in the local receipt. A later eligible unpaused run retries only when local and remote history still prove that exact transaction safe. Unknown divergence stops for operator recovery.

## Portable distribution

`upload-ready/global-agents.zip` contains one root-level `AGENTS.md`. Each `upload-ready/skills/<skill-name>.zip` contains one matching wrapper directory. ZIP timestamps, ordering, file permissions and compression are deterministic; unsafe paths, AppleDouble, `__MACOSX`, `.DS_Store`, duplicates, collisions and size/ratio violations fail validation.

The README block between the Codex Config Manager markers is generated. Content outside those markers remains human-authored. Skill additions and deletions dynamically add and remove matching ZIPs and links.

## Consumer contract

The consumer implementation is complete but has only been exercised in isolated Mac Studio simulations. It:

1. requires explicit consumer role and matching machine identity;
2. rejects dirty, ahead or diverged checkouts;
3. fetches and updates only by safe fast-forward;
4. validates `latest/` before touching live consumer state;
5. deploys only `AGENTS.md` and dynamic user skills with checksum dry-run, bounded deletion and equivalence proof;
6. preserves consumer `.system/**`, `.DS_Store` and unrelated `.codex` entries;
7. never commits, republishes or invokes publisher orchestration.

The consumer path guard refuses the Mac Studio authoritative `/Users/spowart/.codex` when the machine identity is `MacStudio`. Consumer launchd installation is also forbidden on the Mac Studio.

## Launchd and operator commands

Installed Mac Studio service:

```text
label:     com.yodaspow.codex-config-manager.publisher
plist:     ~/Library/LaunchAgents/com.yodaspow.codex-config-manager.publisher.plist
interval:  60 seconds
program:   <repo>/.venv/bin/codex-config-manager-publisher
```

The plist uses absolute paths, no shell activation and no interactive environment. `RunAtLoad` performs an initial check; the Python settlement state remains separate from launchd cadence.

Operator commands:

```bash
cd "/Users/spowart/Scripts/codex-config-manager" \
&& .venv/bin/codex-config-manager-validate --config config/config.yaml \
&& echo "✅ Command ran successfully"
```

```bash
cd "/Users/spowart/Scripts/codex-config-manager" \
&& .venv/bin/codex-config-manager-status --config config/config.yaml \
&& echo "✅ Command ran successfully"
```

```bash
cd "/Users/spowart/Scripts/codex-config-manager" \
&& .venv/bin/codex-config-manager-install --config config/config.yaml \
&& echo "✅ Command ran successfully"
```

```bash
cd "/Users/spowart/Scripts/codex-config-manager" \
&& .venv/bin/codex-config-manager-uninstall --config config/config.yaml \
&& echo "✅ Command ran successfully"
```

Uninstall removes only the configured role’s generated LaunchAgent. It preserves live Codex content, `latest/`, artifacts, private config, `.venv`, `.tools`, runtime state and logs.

Logs are metadata-only and rotate at 2 MiB with five backups:

```text
~/Library/Logs/codex-config-manager/publisher.log
~/Library/Logs/codex-config-manager/publisher-launchd.stdout.log
~/Library/Logs/codex-config-manager/publisher-launchd.stderr.log
```

The local state receipt is:

```text
~/Library/Application Support/codex-config-manager/runtime-state/publisher-state.json
```

It is current operational memory, not permanent history. Git commits are the permanent publication record.

## Failure and recovery boundaries

- Invalid config, identity, paths, environment, source, rsync, archive or Git state stops before later stages.
- A corrupt/missing state receipt restarts the full settlement period.
- A boot change or anomalous monotonic relationship cannot make content settle early.
- Direct GitHub edits must be fast-forwarded before a new publication when there is no local pending commit.
- Independent remote history overlapping an exact local pending commit stops; never force-push or discard either side.
- Publisher restoration of Mac Studio live content is not automated.
- Real Mac mini behaviour remains unproven until Doc 12 is executed there.

## Development and release lanes

Normal code/documentation changes use ordinary reviewed development commits. Routine managed-source changes use deterministic `managed-state:` commits. A SemVer tag or GitHub Release is a separate deliberate operator action after evidence review; the unattended publisher never creates one.

Run the full suite:

```bash
cd "/Users/spowart/Scripts/codex-config-manager" \
&& .venv/bin/python -m pytest -q \
&& echo "✅ Command ran successfully"
```
